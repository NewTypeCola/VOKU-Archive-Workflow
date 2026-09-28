import json
import numpy as np

def runs(a):
    edges=np.diff(np.r_[False,np.asarray(a,dtype=bool),False].astype(np.int8))
    return list(zip(np.flatnonzero(edges==1).tolist(),np.flatnonzero(edges==-1).tolist()))

def segment_characters(gray,rule,b,chars):
    """Accept only measured whitespace-separated glyphs; never equal-width interpolation."""
    x0,y0,x1,y1=b;ink=(gray[y0:y1,x0:x1]<175)&~rule[y0:y1,x0:x1]
    raw=runs(ink.any(axis=0))
    candidates=[]
    for threshold in range(0, max(2,min(12,(y1-y0)//3))):
        merged=[]
        for a,z in raw:
            if merged and a-merged[-1][1]<=threshold:merged[-1][1]=z
            else:merged.append([a,z])
        if len(merged)!=len(chars):continue
        boxes=[];ok=True
        for (a,z),ch in zip(merged,chars):
            ys,xs=np.nonzero(ink[:,a:z])
            if not len(xs):ok=False;break
            bb=[x0+a,y0+int(ys.min()),x0+z,y0+int(ys.max())+1];hh=bb[3]-bb[1];ww=z-a
            if '가'<=ch<='힣' and (hh<.48*(y1-y0) or ww<.27*(y1-y0) or ww>1.65*(y1-y0)):ok=False
            elif not ('가'<=ch<='힣') and ch not in '.,:;!?·':ok=False
            boxes.append(bb)
        if ok:candidates.append(boxes)
    unique={json.dumps(x):x for x in candidates}
    if len(unique)!=1:raise ValueError('CHARACTER_SEGMENTATION_AMBIGUOUS')
    return next(iter(unique.values()))
