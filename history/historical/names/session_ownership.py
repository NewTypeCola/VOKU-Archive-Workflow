"""Two fixed reading sessions, exclusive years, and whole-program ownership."""
import contextlib, fcntl, json, re, time, uuid
from collections import defaultdict
from core import *

def tables(c):
    c.executescript("""
    CREATE TABLE IF NOT EXISTS run_settings(key TEXT PRIMARY KEY,value TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS program_groups(
      id TEXT PRIMARY KEY,year INTEGER,semester INTEGER,program TEXT,doc_ids TEXT,basis TEXT);
    CREATE TABLE IF NOT EXISTS program_runs(
      id TEXT PRIMARY KEY,group_id TEXT,owner TEXT,status TEXT,created_at REAL,heartbeat_at REAL,
      documents TEXT,workspace TEXT,agent_id TEXT UNIQUE,summary_rel TEXT);
    CREATE TABLE IF NOT EXISTS program_members(doc_id TEXT PRIMARY KEY,run_id TEXT);
    CREATE TABLE IF NOT EXISTS review_leases(id TEXT PRIMARY KEY,doc_id TEXT,source_version INTEGER,status TEXT,created_at REAL);
    CREATE TABLE IF NOT EXISTS reading_sessions(owner TEXT PRIMARY KEY,year INTEGER UNIQUE,status TEXT,updated_at REAL);
    """)
    columns={r[1] for r in c.execute('PRAGMA table_info(review_leases)')}
    for name in ('owner','job_id'):
        if name not in columns:c.execute('ALTER TABLE review_leases ADD COLUMN '+name+' TEXT')

DIRECTIONS={'main':'ascending','reverse':'descending'}

@contextlib.contextmanager
def session_lock():
    path=out('state/start.lock');path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a+b') as handle:
        fcntl.flock(handle,fcntl.LOCK_EX)
        yield

def session_owner(owner):
    if owner not in DIRECTIONS:raise ValueError('SESSION_OWNER_MUST_BE_MAIN_OR_REVERSE')
    return owner

def activate(c,owner):
    session_owner(owner)
    c.execute("INSERT INTO reading_sessions VALUES(?,NULL,'active',?) ON CONFLICT(owner) DO UPDATE SET status='active',updated_at=excluded.updated_at",(owner,time.time()))

def identity_maintenance_guard(c):
    if mode(c)=='dual' and c.execute("SELECT 1 FROM reading_sessions WHERE status='active' UNION ALL SELECT 1 FROM program_runs WHERE status='running' LIMIT 1").fetchone():
        raise ValueError('STOP_READING_SESSIONS_BEFORE_ROSTER_CORRECTION')

def review_scope(c,job_id=None,owner=None,doc_ids=None):
    if not job_id:
        if mode(c)=='dual':raise ValueError('REVIEW_REQUIRES_JOB_AND_OWNER')
        return None
    r=c.execute('SELECT * FROM program_runs WHERE id=?',(job_id,)).fetchone()
    if not r or r['owner']!=owner:raise ValueError('PROGRAM_OWNER_MISMATCH')
    if r['status'] not in {'running','text_complete'}:raise ValueError('PROGRAM_NOT_REVIEWABLE')
    if mode(c)=='dual':
        s=c.execute('SELECT * FROM reading_sessions WHERE owner=?',(owner,)).fetchone()
        year=c.execute('SELECT year FROM program_groups WHERE id=?',(r['group_id'],)).fetchone()[0]
        if not s or s['status']!='active' or s['year']!=year:raise ValueError('REVIEW_OUTSIDE_SESSION_YEAR')
    allowed={x['id'] for x in json.loads(r['documents'])}
    if doc_ids and not set(doc_ids)<=allowed:raise ValueError('REVIEW_OUTSIDE_ASSIGNED_PROGRAM')
    return allowed

def selection(c,owner,year=None):
    """Read-only preview of the same frontier used inside the claim transaction."""
    dual=mode(c)=='dual'
    if dual:session_owner(owner)
    direction='DESC' if dual and owner=='reverse' else 'ASC'
    unfinished=c.execute("SELECT year FROM docs WHERE status IN ('pending','leased') AND year BETWEEN 1988 AND 2019 AND id NOT IN (SELECT doc_id FROM review_leases WHERE status='open') ORDER BY year "+direction+' LIMIT 1').fetchone()
    if not unfinished:
        return {'status':'semantic_queue_drained','remaining_masks_may_be_held':True}
    target=unfinished[0]
    if dual:
        s=c.execute('SELECT * FROM reading_sessions WHERE owner=?',(owner,)).fetchone()
        if s and s['year'] is not None:
            held=c.execute("SELECT 1 FROM docs WHERE year=? AND status IN ('pending','leased') LIMIT 1",(s['year'],)).fetchone()
            if held:target=s['year']
        other=c.execute('SELECT owner FROM reading_sessions WHERE year=? AND owner!=?',(target,owner)).fetchone()
        if other:return {'status':'year_reserved','year':target,'retry_after':'other_session_finishes_year'}
    if year is not None and year!=target:
        raise ValueError('YEAR_OUTSIDE_SESSION_FRONTIER' if dual else 'EARLIER_INVENTORY_YEAR_NOT_READ')
    for g in c.execute('SELECT * FROM program_groups WHERE year=? ORDER BY semester '+direction+',program '+direction,(target,)).fetchall():
        if c.execute("SELECT 1 FROM program_runs WHERE group_id=? AND status='running'",(g['id'],)).fetchone():continue
        ids=json.loads(g['doc_ids'])
        pending=[dict(x) for x in c.execute("SELECT id,name,status,version,lease,leased_at FROM docs WHERE id IN ("+','.join('?' for _ in ids)+") AND status IN ('pending','leased') AND id NOT IN (SELECT doc_id FROM review_leases WHERE status='open') ORDER BY name",ids)]
        if pending:return {'group':dict(g),'pending':pending,'year':target}
    return {'status':'current_year_assigned','year':target}

def exists(c):
    return bool(c.execute("SELECT 1 FROM sqlite_master WHERE name='run_settings'").fetchone())

def mode(c=None):
    own=c is None
    if own:c=db()
    try:
        if not exists(c):return 'single'
        row=c.execute("SELECT value FROM run_settings WHERE key='mode'").fetchone()
        return row[0] if row else 'single'
    finally:
        if own:c.close()

def inventory_groups(documents):
    """Use the inventory title, not inferred broadcast dates or staff identity."""
    known=defaultdict(set); parsed={}
    for d in documents:
        m=re.fullmatch(r'VOKU_(\d{4})_(\d+)학기_(.+)_(\d+)',nfc(d['name']))
        if m:
            y,s,program=int(m[1]),int(m[2]),m[3]
            known[(y,s)].add(program);parsed[d['id']]=(y,s,program,'title')
    groups={}
    for d in documents:
        values=parsed.get(d['id'])
        if not values:
            m=re.fullmatch(r'VOKU_(\d{4})_(\d+)학기_(.+)',nfc(d['name']))
            if m:
                y,s,tail=int(m[1]),int(m[2]),m[3]
                candidates=[k for k in known[(y,s)] if tail==k or tail.startswith(k+'_')]
                program=max(candidates,key=len) if candidates else tail
                values=(y,s,program,'known_program_supplement' if candidates else 'standalone_inventory_title')
            else:values=(d['year'],0,nfc(d['name']),'standalone_inventory_title')
        y,s,program,basis=values
        gid='g-'+digest([y,s,program])[:20]
        g=groups.setdefault(gid,dict(id=gid,year=y,semester=s,program=program,doc_ids=[],basis=[]))
        g['doc_ids'].append(d['id'])
        if basis not in g['basis']:g['basis'].append(basis)
    return sorted(groups.values(),key=lambda g:(g['year'] or 9999,g['semester'],g['program']))

def configure(value):
    if value not in {'single','dual'}:raise ValueError('MULTI_AGENT_MODE_RETIRED_USE_SINGLE_OR_DUAL')
    c=db()
    try:
        tables(c)
        groups=inventory_groups([dict(x) for x in c.execute('SELECT id,name,year FROM docs')])
        with tx(c):
            if mode(c)!=value:
                if c.execute("SELECT 1 FROM program_runs WHERE status='running' UNION ALL SELECT 1 FROM reading_sessions WHERE status='active' UNION ALL SELECT 1 FROM review_leases WHERE status='open' LIMIT 1").fetchone():
                    raise ValueError('FINISH_OR_STOP_ACTIVE_PROGRAMS_BEFORE_MODE_SWITCH')
                if c.execute("SELECT 1 FROM jobs WHERE status IN ('queued','running') LIMIT 1").fetchone():raise ValueError('DRAIN_IMAGE_JOBS_BEFORE_MODE_SWITCH')
            c.execute("INSERT OR REPLACE INTO run_settings VALUES('mode',?)",(value,))
            for g in groups:
                c.execute('INSERT OR REPLACE INTO program_groups VALUES(?,?,?,?,?,?)',
                          (g['id'],g['year'],g['semester'],g['program'],json.dumps(g['doc_ids']),json.dumps(g['basis'])))
        return {'mode':value,'semantic_slots':2 if value=='dual' else 1,'groups':len(groups),
                'documents':sum(len(g['doc_ids']) for g in groups),'production_started':False}
    finally:c.close()

def owned(c,job_id,owner,require_active=True):
    if not exists(c):raise ValueError('CONFIGURE_EXECUTION_MODE_FIRST')
    r=c.execute('SELECT * FROM program_runs WHERE id=?',(job_id,)).fetchone()
    if not r or r['owner']!=owner:raise ValueError('PROGRAM_OWNER_MISMATCH')
    if r['status']!='running':raise ValueError('PROGRAM_NOT_RUNNING')
    if require_active and mode(c)=='dual':
        s=c.execute('SELECT status FROM reading_sessions WHERE owner=?',(owner,)).fetchone()
        if not s or s[0]!='active':raise ValueError('SESSION_START_REQUIRED')
    return dict(r)

def guard(c,context=None,doc_ids=None):
    if context and context.get('review_id'):
        row=c.execute("SELECT * FROM review_leases WHERE id=? AND status='open'",(context['review_id'],)).fetchone()
        if not row or row['doc_id']!=context.get('doc_id') or (doc_ids and set(doc_ids)!={row['doc_id']}):raise ValueError('REVIEW_SCOPE_MISMATCH')
        if mode(c)=='dual':
            if row['owner']!=context.get('owner'):raise ValueError('REVIEW_OWNER_MISMATCH')
            review_scope(c,row['job_id'],row['owner'],[row['doc_id']])
        return None
    if context:
        r=owned(c,context['job_id'],context['owner'])
        allowed={x['id'] for x in json.loads(r['documents'])}
        if doc_ids and not set(doc_ids)<=allowed:raise ValueError('DOCUMENT_OUTSIDE_ASSIGNED_PROGRAM')
        for did in doc_ids or []:
            m=c.execute('SELECT run_id FROM program_members WHERE doc_id=?',(did,)).fetchone()
            if not m or m[0]!=r['id']:raise ValueError('PROGRAM_MEMBERSHIP_CHANGED')
        return r
    if mode(c)!='single':raise ValueError('DUAL_MODE_REQUIRES_SCOPED_PROGRAM_COMMAND')
    if exists(c) and c.execute("SELECT 1 FROM program_runs WHERE status='running' LIMIT 1").fetchone():
        raise ValueError('ACTIVE_PROGRAM_REQUIRES_SCOPED_COMMAND')
    return None

def claim(owner,year=None):
    if not owner or len(owner)>180:raise ValueError('PROGRAM_OWNER_REQUIRED')
    c=db()
    try:
        if not exists(c):raise ValueError('CONFIGURE_EXECUTION_MODE_FIRST')
        with tx(c):
            dual=mode(c)=='dual';cap=2 if dual else 1
            if dual:
                session_owner(owner)
                s=c.execute('SELECT status FROM reading_sessions WHERE owner=?',(owner,)).fetchone()
                if (s and s[0]!='active') or out('state/STOP').exists():raise ValueError('SESSION_START_REQUIRED')
                if c.execute("SELECT 1 FROM program_runs WHERE owner=? AND status='running'",(owner,)).fetchone():
                    raise ValueError('OWNER_ALREADY_HAS_PROGRAM_USE_RESUME')
            if c.execute("SELECT count(*) FROM program_runs WHERE status='running'").fetchone()[0]>=cap:
                return {'status':'slots_full','slots':cap}
            if c.execute("SELECT 1 FROM program_runs WHERE owner=? AND status='running'",(owner,)).fetchone():
                raise ValueError('OWNER_ALREADY_HAS_PROGRAM')
            picked=selection(c,owner,year)
            if 'group' not in picked:return picked
            g=picked['group'];pending=picked['pending']
            if dual:
                activate(c,owner)
                c.execute('UPDATE reading_sessions SET year=? WHERE owner=?',(picked['year'],owner))
            if pending:
                jid='program-'+uuid.uuid4().hex[:16];workspace='work/programs/'+jid;now=time.time()
                documents=[{'id':x['id'],'name':x['name'],'base_version':x['version']} for x in pending]
                c.execute('INSERT INTO program_runs VALUES(?,?,?,?,?,?,?,?,NULL,NULL)',
                          (jid,g['id'],owner,'running',now,now,json.dumps(documents,ensure_ascii=False),workspace))
                for d in pending:
                    c.execute('INSERT INTO program_members VALUES(?,?)',(d['id'],jid))
                    if d['status']=='leased':
                        event(c,'orchestration',d['id'],'adopted_legacy_lease',{'lease':d['lease'],'leased_at':d['leased_at'],'program':jid})
                        c.execute("UPDATE docs SET status='pending',lease=NULL WHERE id=?",(d['id'],))
                manifest={'job_id':jid,'owner':owner,'workspace':workspace,'group':dict(g),'documents':documents,
                          'mode':mode(c),'completion':'all assigned semantic decisions submitted and unresolved evidence handed off; image holds are not masked completion'}
                write(workspace+'/assignment.json',manifest)
                return manifest
    finally:c.close()

def renew(job_id,owner):
    c=db()
    try:
        with tx(c):
            r=owned(c,job_id,owner);now=time.time()
            c.execute('UPDATE program_runs SET heartbeat_at=? WHERE id=?',(now,job_id))
            c.execute("UPDATE docs SET leased_at=? WHERE status='leased' AND id IN (SELECT doc_id FROM program_members WHERE run_id=?)",(now,job_id))
        return {'job_id':job_id,'heartbeat_at':now}
    finally:c.close()

def packet(job_id,owner,limit=2,max_chars=45000,since_context=None,unit='program'):
    from workflow import enrich_packet,reading_rules
    reading_rules()  # Validate the required live policy before acquiring any new lease.
    renew(job_id,owner)
    from text_stage import packet as get_packet
    result=get_packet(limit,max_chars,context={'job_id':job_id,'owner':owner},unit=unit)
    return enrich_packet(result,job_id,since_context)

def submit(job_id,owner,path,advance=False,limit=2,max_chars=45000,since_context=None,unit='program',partial_reason=None):
    if partial_reason is not None:
        if not isinstance(partial_reason,str) or not partial_reason.strip():raise ValueError('PARTIAL_SUBMISSION_REASON_REQUIRED')
        if advance:raise ValueError('PARTIAL_SUBMISSION_REQUIRES_PROGRAM_SUBMIT_WITHOUT_ADVANCE')
    c=db()
    try:
        r=owned(c,job_id,owner)
        resolved=out(path)
        if not resolved.is_relative_to(out(r['workspace'])):raise ValueError('PROGRAM_SUBMISSION_OUTSIDE_WORKSPACE')
    finally:c.close()
    from text_stage import submit as put
    result=put(path,context={'job_id':job_id,'owner':owner,'partial_reason':partial_reason})
    renew(job_id,owner)
    answer={'submitted':result}
    if partial_reason is not None:
        answer['partial_submission_reason']=partial_reason
        answer['program_completion_not_implied']=True
    if advance:
        answer['next']=packet(job_id,owner,limit,max_chars,since_context,unit)
        if answer['next'].get('status')=='no_pending_documents':
            from workflow import program_summary
            answer['next']['program_summary']=program_summary(job_id,save=True)
    return answer

def finish(job_id,owner,summary_path=None):
    c=db()
    try:
        with tx(c):
            r=owned(c,job_id,owner)
            notes={};documents=json.loads(r['documents'])
            if summary_path:
                path=out(summary_path)
                if not path.is_relative_to(out(r['workspace'])):raise ValueError('PROGRAM_SUMMARY_OUTSIDE_WORKSPACE')
                notes=read(path)
            if not isinstance(notes,dict):raise ValueError('PROGRAM_HANDOFF_NOTES_OBJECT_REQUIRED')
            if 'covered_document_ids' in notes and set(notes['covered_document_ids'])!={x['id'] for x in documents}:
                raise ValueError('PROGRAM_HANDOFF_COVERAGE')
            if any(not isinstance(notes[k],list) for k in ('context_notes','exception_notes','unresolved') if k in notes):
                raise ValueError('PROGRAM_HANDOFF_NOTES_MUST_BE_LISTS')
            for d in documents:
                current=c.execute('SELECT * FROM docs WHERE id=?',(d['id'],)).fetchone()
                if current['version']<=d['base_version'] or current['status'] in ('pending','leased'):
                    raise ValueError('UNREAD_DOCUMENTS_REMAIN_IN_PROGRAM')
            from workflow import program_report,save_report
            summary=program_report(c,job_id)
            if not all(d['page_count_matches_inventory'] for d in summary['documents']):
                raise ValueError('PROGRAM_PAGE_COUNT_MISMATCH')
            summary.update(program_status='text_complete',agent_notes=notes,
                           agent_notes_are_not_aggregate_authority=True,
                           notes_source=summary_path,notes_sha256=sha(out(summary_path)) if summary_path else None)
            rel=save_report(summary,r['workspace']+'/handoff-generated')
            c.execute("UPDATE program_runs SET status='text_complete',summary_rel=?,heartbeat_at=? WHERE id=?",(rel,time.time(),job_id))
            c.execute('DELETE FROM program_members WHERE run_id=?',(job_id,))
            event(c,'orchestration',job_id,'text_complete',{'summary':rel,'masking_complete_not_implied':True})
        return {'job_id':job_id,'status':'text_complete','masking_complete_not_implied':True,
                'summary_file':str(out(rel)),'counts':summary['counts'],'unresolved_items':len(summary['unresolved'])}
    finally:c.close()

def release(job_id,owner,previous_worker_stopped=False,reason=''):
    if not previous_worker_stopped or not reason.strip():raise ValueError('CONFIRM_PREVIOUS_WORKER_STOPPED_AND_REASON')
    c=db()
    try:
        with tx(c):
            r=owned(c,job_id,owner,require_active=False)
            c.execute("UPDATE docs SET status='pending',lease=NULL WHERE status='leased' AND id IN (SELECT doc_id FROM program_members WHERE run_id=?)",(job_id,))
            c.execute("UPDATE program_runs SET status='stopped',heartbeat_at=? WHERE id=?",(time.time(),job_id))
            c.execute('DELETE FROM program_members WHERE run_id=?',(job_id,))
            event(c,'orchestration',job_id,'released_after_worker_stop',{'reason':reason,'previous_agent_id':r['agent_id']})
        return {'job_id':job_id,'status':'stopped','decisions_and_history_preserved':True}
    finally:c.close()

def status():
    c=db()
    try:
        if not exists(c):return {'mode':'single','configured':False,'active':[]}
        active=[dict(x) for x in c.execute("SELECT * FROM program_runs WHERE status='running' ORDER BY created_at")]
        now=time.time()
        for x in active:
            x['heartbeat_age_seconds']=round(now-x['heartbeat_at'],1)
            x['needs_liveness_check']=now-x['heartbeat_at']>config()['lease_seconds']
        return {'mode':mode(c),'configured':True,'active':active,'stale_claims_never_reassigned_automatically':True}
    finally:c.close()
