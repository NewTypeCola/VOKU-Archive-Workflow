"""Small, explicit signatures for occurrence identity and pixel-producing inputs."""
from storage import digest,sha,ROOT

RENDER_CONTRACT_VERSION=2

def extent_pixels(t):
    """Legacy needs_geometry notes are not a physical range when precise geometry already succeeded."""
    e=t.get('extent')
    if not isinstance(e,dict):return e if e else None
    fields={k:e[k] for k in ('source_surface','surface','full_name','observed_surface','spans','start','end','ranges','boxes','required_span') if k in e}
    compact=lambda x:''.join(str(x).split())
    actual=compact(t.get('source_surface') or t.get('logical_surface') or t.get('quote',''))
    candidates=[compact(x) for x in e.get('candidate_names',[]) if compact(x)!=actual]
    if candidates:fields['different_candidate_names']=sorted(candidates)
    if e.get('quote_complete') is False:fields['quote_complete']=False
    return fields or None

def occurrence(t):
    spans=t.get('spans')
    if spans:
        ranges=[{'ref':s.get('ref'),'start':s.get('start'),'end':s.get('end'),'surface':s.get('surface')} for s in spans]
    elif any(t.get(k) is not None for k in ('ref','start','end')):
        ranges=[{'ref':t.get('ref'),'start':t.get('start'),'end':t.get('end'),'surface':t.get('quote')}]
    else:ranges=[]
    return {'quote':t.get('quote'),'source_surface':t.get('source_surface'),'logical_surface':t.get('logical_surface'),'extent':extent_pixels(t),'member_target_ids':t.get('member_target_ids'),'ranges':ranges,
            'class':t.get('class'),'staff_id':t.get('staff_id'),'token':t.get('token')}

def spatial_occurrence(t):
    """Physical name identity only; output identity remains in occurrence/page_key."""
    o=occurrence(t)
    return {k:v for k,v in o.items() if k not in ('class','staff_id','token')}

def same_spatial_occurrence(a,b):return spatial_occurrence(a)==spatial_occurrence(b)

def spatial_key(p,t,g):
    return digest({'page':{k:p.get(k) for k in ('id','version','source_sha','width','height')},
                   'occurrence':spatial_occurrence(t),
                   'geometry':{k:g.get(k) for k in ('erase_boxes','rotation_degrees','source_sha256','crop_id','method')}})

def same_occurrence(a,b):return occurrence(a)==occurrence(b)

def geometry_pixels(g):
    if not g:return None
    # Only fields consumed by the renderer, normalized to their actual defaults.
    return {'erase_boxes':g.get('erase_boxes',[]),'restore_boxes':g.get('restore_boxes',[]),
            'token_box':g.get('token_box'),'rotation_degrees':g.get('rotation_degrees',0),
            'source_sha256':g.get('source_sha256'),'form_contact_reviewed':bool(g.get('form_contact_reviewed')),
            'unresolved':bool(g.get('unresolved'))}

def render_engine():
    return digest({'contract':RENDER_CONTRACT_VERSION,'files':{n:sha(ROOT/'src'/n) for n in ('patch_verify.py','spatial.py','render_contract.py','geometry_images.py','token_layout.py','base_review.py','source_adapter.py','token_repair.py')}})

def page_key(p,targets,overrides,style,base_review=None):
    base=base_review or {}
    return digest({'engine':render_engine(),'page':{k:p.get(k) for k in ('id','version','source_sha','parent_sha','width','height')},
       'baseline':p.get('receipt',{}).get('output_sha256'),
       'base_review':{k:base.get(k) for k in ('choice','sha256','layer_inventory_sha256')},
       'targets':[{'id':t['id'],**occurrence(t)} for t in sorted(targets,key=lambda t:t['id'])],
       'geometry':{t['id']:geometry_pixels(overrides.get(t['id'])) for t in targets},
       'legacy_geometry':p.get('receipt',{}).get('geometry_sha256') or digest(p.get('geometry',{})),
       'style':style})


def fragmented_name_groups(targets):
    """Flag exact OCR-contiguous pieces of a known full name; never infer a grouping from distance."""
    import re
    groups=[]
    for t in targets:
        if t.get('class')!='staff' or t.get('member_target_ids'):continue
        canonical=t.get('canonical_name','')
        if len(canonical)!=3:continue
        peers=[q for q in targets if q.get('staff_id')==t.get('staff_id') and q.get('ref')==t.get('ref') and q.get('ref')]
        def start(q):
            return q.get('spans',[{}])[0].get('start',q.get('start')) if q.get('spans') else q.get('start')
        peers=[q for q in peers if start(q) is not None]
        peers.sort(key=start)
        for i in range(len(peers)):
            for n in (2,3):
                seq=peers[i:i+n]
                if len(seq)!=n or re.sub(r'\s','', ''.join(q.get('quote','') for q in seq))!=canonical:continue
                line=seq[0].get('line_text') or (seq[0].get('spans') or [{}])[0].get('text','')
                end=start(seq[-1])+len(seq[-1].get('quote',''))
                if re.sub(r'\s','',line[start(seq[0]):end])!=canonical:continue
                ids=[q['id'] for q in seq]
                if ids not in groups:groups.append(ids)
    return groups
