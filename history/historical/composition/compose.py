"""Mechanical, provenance-checked composition; never changes any input workspace."""
from pathlib import Path
import os,sys,io,json,hashlib,time,datetime,collections,concurrent.futures,traceback
ROOT=Path(__file__).resolve().parents[1]
os.environ['TMPDIR']=str(ROOT/'work/tmp')
os.environ['PYTHONDONTWRITEBYTECODE']='1'
sys.dont_write_bytecode=True
from PIL import Image,ImageDraw,ImageChops
import numpy as np

def write_guard(event,args):
    paths=[]
    if event=='open':
        path,mode,flags=args
        if isinstance(path,(str,bytes,os.PathLike)) and ((mode and any(c in mode for c in 'wax+')) or flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)):
            paths=[path]
    elif event in ('os.remove','os.rmdir','os.mkdir','os.chmod','os.chown','os.utime','os.truncate'):paths=[args[0]]
    elif event in ('os.rename','os.link','os.symlink'):paths=list(args[:2])
    for path in paths:
        if isinstance(path,bytes):path=os.fsdecode(path)
        if not Path(path).resolve().is_relative_to(ROOT):raise PermissionError('WRITE_OUTSIDE_WORKSPACE: '+str(path))
sys.addaudithook(write_guard)

def now():return datetime.datetime.now().astimezone().isoformat()
def sha(blob):return hashlib.sha256(blob).hexdigest()
def readjson(path):return json.loads(Path(path).read_text())
def jsonline(v):return json.dumps(v,ensure_ascii=False,separators=(',',':'))+'\n'
def atomic(path,blob):
    path=Path(path);assert path.resolve().is_relative_to(ROOT)
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=ROOT/'work/tmp'/(sha(str(path).encode())+'.'+str(os.getpid())+'.tmp')
    temp.write_bytes(blob);os.replace(temp,path)
def save(path,v):atomic(ROOT/path,(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
def rows(path):
    with Path(path).open() as f:return [json.loads(l) for l in f if l.strip()]
def load_input(ref,records):
    p=Path(ref['path']);a=p.stat()
    assert a.st_size==ref['bytes'] and a.st_mtime_ns==ref['mtime_ns'] and a.st_ctime_ns==ref['ctime_ns'],('INPUT_STAT_CHANGED',str(p))
    b=p.read_bytes();s=sha(b);z=p.stat()
    assert (a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_size,z.st_mtime_ns,z.st_ctime_ns),('INPUT_CHANGED_DURING_READ',str(p))
    if ref.get('sha256'):assert s==ref['sha256'],('INPUT_HASH_MISMATCH',str(p),s,ref['sha256'])
    records[str(p)]={**ref,'sha256':s}
    return b

def decode(blob):
    with Image.open(io.BytesIO(blob)) as im:return im.convert('RGBA')
def put_rect(mask,box):
    assert len(box)==4 and all(isinstance(v,(int,float)) and int(v)==v for v in box),('NONINTEGER_BOX',box)
    x0,y0,x1,y1=map(int,box)
    assert 0<=x0<x1<=mask.shape[1] and 0<=y0<y1<=mask.shape[0],('BOX_OUTSIDE_ORIGINAL',box,mask.shape)
    mask[y0:y1,x0:x1]=True

def name_mask(d,size,raw,layer,records):
    w,h=size;mask=np.zeros((h,w),dtype=bool)
    for b in d['rects']+d.get('prior_target_rects',[]):put_rect(mask,b)
    for ref in d['masks']:
        with Image.open(io.BytesIO(load_input(ref,records))) as m:
            assert m.size==size,('MASK_SIZE_MISMATCH',ref['path']);mask|=np.asarray(m.convert('L'))>0
    if d['lines']:
        line=Image.new('L',size,0);draw=ImageDraw.Draw(line)
        for spec in d['lines']:draw.line(spec['xy'],fill=255,width=spec['width'])
        mask|=np.asarray(line)>0
    if d['delta_from_original']:mask|=np.any(layer!=raw,axis=2)
    return mask

def build_one(row):
    started=time.monotonic();key=row['year']+'/'+row['filename'];records={}
    try:
        source_blob=load_input(row['original'],records)
        ref_info={'key':key,'year':row['year'],'filename':row['filename'],'source_sha256':sha(source_blob),
          'row_sha256':sha(jsonline(row).encode()),'status':'verified','verification':{},'layers':[]}
        if not(row['name_layers'] or row['seal'] or row['contact']):
            with Image.open(io.BytesIO(source_blob)) as im: size=im.size
            output_blob=source_blob;mode='original_byte_copy';pixel_sha=None;changed=0
            checks={'source_hash_checked':True,'output_byte_identical_to_original':True}
        else:
            original=decode(source_blob);raw=np.asarray(original);size=original.size
            composed=original.copy();expected=raw.copy();allowed=np.zeros(raw.shape[:2],bool)
            donor_blob=None;donor_pixels=None
            def apply(layer,mask,blob,kind,package=None):
                nonlocal donor_blob,donor_pixels
                assert layer.size==size,('LAYER_SIZE_MISMATCH',key,kind,layer.size,size)
                arr=np.asarray(layer)
                # Two independent pixel paths: Pillow masked paste and NumPy indexed assignment.
                composed.paste(layer,(0,0),Image.fromarray(mask.astype(np.uint8)*255))
                expected[mask]=arr[mask];allowed[:] |= mask
                ref_info['layers'].append({'kind':kind,'package':package,'mask_pixels':int(mask.sum()),
                  'mask_sha256':sha(np.packbits(mask).tobytes()),'image_sha256':sha(blob)})
                donor_blob=blob;donor_pixels=arr
            for d in row['name_layers']:
                blob=load_input(d['image'],records);layer=decode(blob)
                assert layer.size==size,('NAME_SIZE_MISMATCH',key,d['package'])
                mask=name_mask(d,size,raw,np.asarray(layer),records)
                apply(layer,mask,blob,'name',d['package'])
            if row['seal']:
                d=row['seal'];blob=load_input(d['image'],records);layer=decode(blob)
                with Image.open(io.BytesIO(load_input(d['mask'],records))) as im:
                    assert im.size==size;mask=np.asarray(im.convert('L'))>0
                apply(layer,mask,blob,'seal')
            if row['contact']:
                d=row['contact'];blob=load_input(d['image'],records);layer=decode(blob)
                assert list(size)==d['size'];mask=np.zeros(raw.shape[:2],bool)
                for b in d['rects']:put_rect(mask,b)
                apply(layer,mask,blob,'phone_mail')
            actual=np.asarray(composed)
            assert np.array_equal(actual,expected),('COMPOSITE_PATHS_DISAGREE',key)
            delta=np.any(expected!=raw,axis=2);changed=int(delta.sum())
            assert not np.any(delta & ~allowed),('OUTSIDE_APPLIED_MASK_CHANGED',key)
            pixel_sha=sha(expected.tobytes())
            if not changed:output_blob=source_blob;mode='original_byte_copy_after_composition'
            elif donor_blob is not None and donor_blob[0:4]==b'RIFF' and np.array_equal(donor_pixels,expected):
                output_blob=donor_blob;mode='identical_existing_result_byte_copy'
            else:
                buf=io.BytesIO();composed.save(buf,'WEBP',lossless=True,exact=True,method=0)
                output_blob=buf.getvalue();mode='lossless_composite'
            roundtrip=decode(output_blob)
            assert roundtrip.size==size and roundtrip.tobytes()==expected.tobytes(),('ROUNDTRIP_MISMATCH',key)
            checks={'source_hash_checked':True,'dimensions_match_original':True,'pillow_numpy_composition_equal':True,
              'outside_applied_regions_equal_original':True,'decoded_output_equals_exact_composite':True,
              'name_order_is_explicit_priority':True,'cross_category_conflict_detection_performed':False}
        dest=ROOT/key
        same_existing=False
        if dest.exists():
            assert not dest.is_symlink(),('OUTPUT_SYMLINK',key)
            old=dest.read_bytes()
            # A new layer may be a visual no-op with different WebP compression. Preserve the
            # previous final file's bytes and timestamps when its decoded pixels already match.
            if old!=output_blob and pixel_sha and sha(decode(old).tobytes())==pixel_sha:
                output_blob=old;mode='prior_final_byte_copy_same_pixels'
            same_existing=old==output_blob
            if not same_existing:atomic(ROOT/'work/history'/row['year']/(sha(old)+'-'+row['filename']),old)
        if not same_existing:atomic(dest,output_blob)
        actual_blob=dest.read_bytes();assert actual_blob==output_blob,('DISK_WRITE_MISMATCH',key)
        ref_info.update(output_sha256=sha(actual_blob),output_bytes=len(actual_blob),size=list(size),pixel_sha256=pixel_sha,
          mode=mode,changed_pixels=changed,verification=checks,inputs=list(records.values()),seconds=round(time.monotonic()-started,5))
        return ref_info
    except Exception as exc:
        return {'key':key,'year':row['year'],'status':'error','error':str(exc),'traceback':traceback.format_exc(),'inputs':list(records.values())}

def ordered_parallel(fn,items,workers):
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as pool:
        it=iter(items);pending={}
        def fill():
            while len(pending)<workers*3:
                try:x=next(it)
                except StopIteration:return
                pending[pool.submit(fn,x)]=True
        fill()
        while pending:
            done,_=concurrent.futures.wait(pending,return_when=concurrent.futures.FIRST_COMPLETED)
            for future in done:
                pending.pop(future);yield future.result()
            fill()

def selftest():
    # Distinct lower-only name stays; higher name and explicit old-token restoration win.
    raw=Image.new('RGBA',(12,8),'white');low=raw.copy();high=raw.copy()
    ImageDraw.Draw(low).rectangle((1,1,3,2),fill='black');ImageDraw.Draw(low).rectangle((7,1,9,2),fill='black')
    ImageDraw.Draw(high).rectangle((1,1,2,2),fill='gray')
    out=raw.copy();m=Image.new('L',raw.size,0);ImageDraw.Draw(m).rectangle((1,1,3,2),fill=255);ImageDraw.Draw(m).rectangle((7,1,9,2),fill=255);out.paste(low,(0,0),m)
    m=Image.new('L',raw.size,0);ImageDraw.Draw(m).rectangle((1,1,3,2),fill=255);out.paste(high,(0,0),m)
    assert out.getpixel((7,1))==low.getpixel((7,1)) and out.getpixel((1,1))==high.getpixel((1,1)) and out.getpixel((3,1))==raw.getpixel((3,1))
    # Contact pixels embedded outside a name's recorded geometry must not enter the composition.
    low.putpixel((0,7),(0,0,0,255));mask=np.zeros((8,12),bool);put_rect(mask,[1,1,4,3]);result=np.array(raw);result[mask]=np.asarray(low)[mask]
    assert tuple(result[7,0])==(255,255,255,255)
    blob=io.BytesIO();out.save(blob,'WEBP',lossless=True,exact=True,method=0);assert decode(blob.getvalue()).tobytes()==out.tobytes()
    save('reports/selftest.json',{'passed':True,'at':now(),'checks':['higher_name_overrides','lower_unrelated_name_retained','old_token_area_restored','inherited_contact_outside_name_omitted','lossless_roundtrip']})

def run(pilot=False,workers=6):
    selftest();plan=rows(ROOT/'work/plan.jsonl');started=time.monotonic()
    if pilot:
        picks={}
        for r in plan:
            cats=tuple(x['package'] for x in r['name_layers'])
            classes=[('year',r['year']),('layers',cats,bool(r['seal']),bool(r['contact']))]
            if len(r['name_layers'])>1:classes.append(('multi',cats))
            if any(x['status']=='partial' for x in r['name_layers']):classes.append(('partial',r['filename']))
            for cls in classes:
                if cls not in picks:picks[cls]=r
        unique={r['year']+'/'+r['filename']:r for r in picks.values()};plan=list(unique.values())
        manifest=ROOT/'reports/pilot_manifest.jsonl'
    else:manifest=ROOT/'reports/manifest.jsonl'
    previous={r['key']:r for r in rows(manifest)} if manifest.exists() else {}
    reusable=[];todo=[]
    for row in plan:
        key=row['year']+'/'+row['filename'];old=previous.get(key)
        if old and old['status']=='verified' and old['row_sha256']==sha(jsonline(row).encode()) and (ROOT/key).is_file() and sha((ROOT/key).read_bytes())==old['output_sha256']:reusable.append(old)
        else:todo.append(row)
    completed=[];last=0;errors=[];modes=collections.Counter()
    with manifest.open('w') as f:
        for r in reusable:f.write(jsonline(r));completed.append(r);modes[r['mode']]+=1
        for r in ordered_parallel(build_one,todo,workers):
            f.write(jsonline(r));completed.append(r)
            if r['status']=='error':errors.append(r);print(json.dumps({'error':r['key'],'detail':r['error']},ensure_ascii=False),flush=True)
            else:modes[r['mode']]+=1
            elapsed=time.monotonic()-started
            if elapsed-last>=10 or len(completed)==len(plan):
                f.flush();p={'phase':'pilot' if pilot else 'compose','at':now(),'done':len(completed),'total':len(plan),'errors':len(errors),'seconds':round(elapsed,1),'modes':dict(modes),'last':r['key']}
                save('work/progress.json',p);print(json.dumps(p,ensure_ascii=False),flush=True);last=elapsed
    summary={'status':'passed' if not errors else 'failed','at':now(),'pages':len(plan),'verified':len(completed)-len(errors),'errors':len(errors),'modes':dict(modes),'seconds':round(time.monotonic()-started,2),'manifest':str(manifest)}
    save('reports/pilot.json' if pilot else 'reports/composition.json',summary)
    if errors:save('reports/pilot_errors.json' if pilot else 'reports/composition_errors.json',errors)
    print(json.dumps(summary,ensure_ascii=False),flush=True)
    return 0 if not errors else 2

def verify_hash(ref):
    try:
        p=Path(ref['path']);s=p.stat();b=p.read_bytes()
        ok=sha(b)==ref['sha256'] and len(b)==ref['bytes'] and s.st_mtime_ns==ref['mtime_ns'] and s.st_ctime_ns==ref['ctime_ns']
        return None if ok else {'path':str(p),'error':'INPUT_CHANGED'}
    except Exception as e:return {'path':ref['path'],'error':str(e)}
def verify_output(r):
    try:
        p=ROOT/r['key'];data=p.read_bytes()
        assert not p.is_symlink() and p.stat().st_nlink==1
        assert sha(data)==r['output_sha256'] and len(data)==r['output_bytes']
        if r['pixel_sha256']:
            im=decode(data);assert list(im.size)==r['size'] and sha(im.tobytes())==r['pixel_sha256']
        else:
            with Image.open(io.BytesIO(data)) as im:assert list(im.size)==r['size']
            assert r['output_sha256']==r['source_sha256']
        return None
    except Exception as e:return {'key':r['key'],'error':str(e)}

def verify(workers=6):
    start=time.monotonic();plan=rows(ROOT/'work/plan.jsonl');manifest=rows(ROOT/'reports/manifest.jsonl');inventory=readjson(ROOT/'reports/inventory.json')
    assert len(manifest)==len(plan) and all(r['status']=='verified' for r in manifest),'INCOMPLETE_MANIFEST'
    expected={r['year']+'/'+r['filename'] for r in plan};assert len(expected)==len(plan)==len({r['key'] for r in manifest})
    coverage={};problems=[]
    for y in inventory['years']:
        original={p.name for p in (ROOT.parent/'game'/y/'webp').iterdir() if p.is_file() and p.suffix.lower()=='.webp'}
        output={p.name for p in (ROOT/y).iterdir() if p.is_file() and p.suffix.lower()=='.webp'}
        want={r['filename'] for r in plan if r['year']==y}
        missing=sorted(original-output);extra=sorted(output-original)
        coverage[y]={'original':len(original),'output':len(output),'missing':len(missing),'extra':len(extra),'original_inventory_unchanged':original==want}
        if missing or extra or original!=want:problems.append({'year':y,'missing':missing,'extra':extra})
    refs={r['path']:r for r in rows(ROOT/'work/input_metadata.jsonl')}
    for r in manifest:
        for ref in r['inputs']:
            if ref['path'] in refs:assert refs[ref['path']]['sha256']==ref['sha256']
            refs[ref['path']]=ref
    done=0;last=0
    for err in ordered_parallel(verify_hash,list(refs.values()),workers):
        done+=1
        if err:problems.append(err)
        elapsed=time.monotonic()-start
        if elapsed-last>=10:
            print(json.dumps({'phase':'verify_input_hashes','done':done,'total':len(refs),'errors':len(problems)}),flush=True);last=elapsed
    input_verified=done;done=0
    for err in ordered_parallel(verify_output,manifest,workers):
        done+=1
        if err:problems.append(err)
        elapsed=time.monotonic()-start
        if elapsed-last>=10:
            print(json.dumps({'phase':'verify_saved_outputs','done':done,'total':len(manifest),'errors':len(problems)}),flush=True);last=elapsed
    save('reports/yearly_coverage.json',coverage)
    with (ROOT/'reports/input_hashes.jsonl').open('w') as f:
        for r in sorted(refs.values(),key=lambda x:x['path']):f.write(jsonline(r))
    result={'status':'passed' if not problems else 'failed','at':now(),'original_pages':len(plan),'output_pages':len(manifest),'years':len(coverage),'filename_missing':sum(r['missing'] for r in coverage.values()),'filename_extra':sum(r['extra'] for r in coverage.values()),
      'input_files_rehashed_unchanged':input_verified if not problems else None,'saved_outputs_verified':done,'errors':len(problems),'seconds':round(time.monotonic()-start,2),
      'output_bytes':sum(r['output_bytes'] for r in manifest),'output_symlinks_or_hardlinks':0 if not problems else None,
      'unknown_excluded':True,'outside_workspace_writes_blocked_by_audit_hook':True,'cross_category_conflict_detection_performed':False,
      'name_priority':'retain lower edits, overwrite with higher edits','existing_seal_geometry_pending':inventory['seal_existing_geometry_pending'],
      'existing_name_partial_layers':inventory['name_existing_partial'],'coverage':coverage,'problems':problems}
    save('reports/final_verification.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('coverage','problems','existing_seal_geometry_pending','existing_name_partial_layers')},ensure_ascii=False),flush=True)
    return 0 if not problems else 2

if __name__=='__main__':
    mode=sys.argv[1] if len(sys.argv)>1 else 'pilot';workers=int(sys.argv[2]) if len(sys.argv)>2 else 6
    if mode=='verify':sys.exit(verify(workers))
    sys.exit(run(mode=='pilot',workers))
