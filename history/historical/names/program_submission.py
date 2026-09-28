def program_submission_scope(c,assignment,data,partial_reason):
    if not assignment:return []
    batch=data.get('packet_id','')
    if not isinstance(batch,str) or not re.fullmatch(r'batch-[0-9a-f]{16}',batch):
        raise ValueError('PROGRAM_PACKET_ID_INVALID')
    packet=read(out(assignment['workspace']+'/packets/'+batch+'.json'))
    if packet.get('packet_id')!=batch:raise ValueError('PROGRAM_PACKET_BINDING_MISMATCH')
    packet_ids={d['doc_id'] for d in packet['documents']}
    incoming={d['doc_id'] for d in data['documents']}
    if not incoming<=packet_ids:raise ValueError('DOCUMENT_OUTSIDE_SAVED_PACKET')
    # Legacy episode packets retain their original submission contract and immutable lease.
    if packet.get('work_unit','episode')!='program':return []
    remaining={r[0] for r in c.execute("SELECT id FROM docs WHERE lease=? AND status='leased'",(batch,))}
    if not remaining<=packet_ids:raise ValueError('SAVED_PACKET_LEASE_COVERAGE_MISMATCH')
    missing=sorted(remaining-incoming)
    if missing and not partial_reason:raise ValueError('ALL_PROGRAM_PACKET_DOCUMENTS_REQUIRED_USE_PARTIAL_REASON_TO_CHECKPOINT')
    return missing

def _submit(c,path,context):
    data=read(path)
    from orchestration import guard
    assignment=guard(c,context,[x['doc_id'] for x in data.get('documents',[])])
    if data.get('policy_sha256')!=policy_hash():raise ValueError('POLICY_CHANGED')
    batch=data.get('packet_id');items=data.get('documents',[])
    if not items:raise ValueError('NO_DOCUMENT_DECISIONS')
    if len({x['doc_id'] for x in items})!=len(items):raise ValueError('DUPLICATE_DOCUMENT_DECISIONS')
    partial_reason=(context or {}).get('partial_reason')
    if partial_reason is not None and (not isinstance(partial_reason,str) or not partial_reason.strip()):
        raise ValueError('PARTIAL_SUBMISSION_REASON_REQUIRED')
    program_submission_scope(c,assignment,data,partial_reason)
    validated=[]
    for item in items:
        d=c.execute('SELECT * FROM docs WHERE id=?',(item['doc_id'],)).fetchone()
        if not d:raise ValueError('UNKNOWN_DOCUMENT')
        if d['lease']!=batch:raise ValueError('PACKET_LEASE_MISMATCH')
        canonical=digest(item)
        if d['version'] and d['decision_rel'] and read(out(d['decision_rel'])).get('submission_sha256')==canonical:
            validated.append((d,None,None));continue
        if d['status']!='leased':raise ValueError('USE_REVISE_TO_REOPEN_DOCUMENT')
        validated.append((d,validate_doc(c,d,item),item))
    results=[]
    with tx(c):
        assignment=guard(c,context,[d['id'] for d,_,_ in validated])
        missing=program_submission_scope(c,assignment,data,partial_reason)
        # Refresh only mechanical validation if a referenced binding changed while
        # waiting for the writer lock. Unrelated registry additions do not matter.
        staff=bindings(c)
        for i,(d,rows,item) in enumerate(validated):
            if rows is not None and any(t.get('staff_id') and t.get('binding_sha256')!=digest(staff.get(t['staff_id'])) for _,targets,_ in rows for t in targets):
                validated[i]=(d,validate_doc(c,d,item),item)
        for d,rows,item in validated:
            fresh=c.execute('SELECT status,version,lease FROM docs WHERE id=?',(d['id'],)).fetchone()
            if fresh['version']!=d['version'] or fresh['lease']!=batch or (rows is not None and fresh['status']!='leased'):
                raise ValueError('DOCUMENT_CHANGED_DURING_SUBMISSION')
            if rows is None:
                if fresh['status']=='leased':refresh_doc(c,d['id'])
                results.append({'doc_id':d['id'],'status':'reused'});continue
            previous=read(out(d['decision_rel'])) if d['decision_rel'] else {}
            old_pages={x['page_id']:x for x in previous.get('pages',[])}
            new_pages={x['page_id']:x for x in item['pages']}
            reusable=bool(previous and policy_accepts(previous.get('policy_sha256')))
            reused_pages=0
            version=d['version']+1;rel=f"work/decisions/{d['id']}.v{version}.json"
            write(rel,{'submission_sha256':digest(item),'policy_sha256':policy_hash(),'packet_id':batch,'submitted_at':time.time(),**item})
            c.execute("UPDATE docs SET version=?,decision_rel=?,status='processing' WHERE id=?",(version,rel,d['id']))
            for p,targets,review in rows:
                if reusable and old_pages.get(p['id'])==new_pages[p['id']] and p['status'] in {'verified','no_changes','partial','hold'}:
                    reused_pages+=1
                    continue
                actionable=any(x['class'] in {'staff','private','staff_pending'} for x in targets)
                unresolved=review!='read' or any(x['class'] in {'uncertain','staff_pending'} for x in targets)
                status='geometry_queued' if actionable else ('hold' if unresolved else 'no_changes')
                c.execute('UPDATE pages SET version=?,status=?,targets=?,geometry_rel=NULL,receipt_rel=NULL,output_rel=NULL WHERE id=?',
                    (version,status,json.dumps(targets,ensure_ascii=False),p['id']))
                if actionable:job(c,p['id'],version,'geometry')
            refresh_doc(c,d['id']);event(c,'semantic',d['id'],'submitted',{'version':version,'pages':len(rows),'mentions':sum(len(x[1]) for x in rows),'pages_reused':reused_pages,'pages_reprocessed':len(rows)-reused_pages})
            results.append({'doc_id':d['id'],'version':version,'status':'queued','pages_reused':reused_pages,'pages_reprocessed':len(rows)-reused_pages})
        if partial_reason and missing and any(rows is not None for _,rows,_ in validated):
            event(c,'semantic',batch,'program_partial_submission',{'reason':partial_reason,
                  'submitted_document_ids':[d['id'] for d,_,_ in validated],'remaining_document_ids':missing,
                  'job_id':assignment['id'],'masking_complete_not_implied':True})
    return results
