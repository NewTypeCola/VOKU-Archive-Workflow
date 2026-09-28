"""Cardinal text orientation measured from ordered OCR glyph boxes."""
import collections, math
import numpy as np

def rotate_box(b,w,h,turns):
    x0,y0,x1,y1=b
    return ([x0,y0,x1,y1], [y0,w-x1,y1,w-x0],
            [w-x1,h-y1,w-x0,h-y0], [h-y1,x0,h-y0,x1])[turns%4]

def rotated_size(w,h,turns):
    return (h,w) if turns%2 else (w,h)

def rotate_normalized(b,turns):
    x,y,w,h=(b[k] for k in ('x','y','width','height'))
    values=((x,y,w,h),(y,1-x-w,h,w),(1-x-w,1-y-h,w,h),(1-y-h,x,h,w))[turns%4]
    return dict(zip(('x','y','width','height'),values))

def rotate_geometry(obj,turns):
    if isinstance(obj,list):return [rotate_geometry(x,turns) for x in obj]
    if isinstance(obj,dict):
        return {k:rotate_normalized(v,turns) if k in {'boundingBox','line_box'} else rotate_geometry(v,turns) for k,v in obj.items()}
    return obj

def page_turns(ocr,vision,w,h):
    votes={}
    for m in sorted(vision.get('matches',[]),key=lambda x:x['candidate_rank']):
        idx=m['observation_index']
        if idx in votes:continue
        points=[]
        for g in sorted(m.get('glyph_guides',[]),key=lambda g:g['range_utf16'][0]):
            b=g['boundingBox']
            if g['text'].strip() and b['width']>0 and b['height']>0:
                points.append(((b['x']+b['width']/2)*w,(b['y']+b['height']/2)*h))
        if len(points)<2:continue
        dx,dy=points[-1][0]-points[0][0],points[-1][1]-points[0][1]
        if math.hypot(dx,dy)<8:continue
        angle=math.degrees(math.atan2(dy,dx))%360
        k=round(angle/90)%4
        deviation=abs((angle-k*90+180)%360-180)
        if deviation<=12:votes[idx]=k
    if votes:
        counts=collections.Counter(votes.values())
        if len(counts)>1:raise ValueError('MIXED_TEXT_ORIENTATION_REQUIRES_REGION_REVIEW')
        return next(iter(counts)), {'method':'ordered_native_glyph_boxes','observations':len(votes)}
    long=[l['boundingBox'] for l in ocr.get('lines',[]) if len(l.get('text','').strip())>=5]
    if long and sum(b['height']*h>b['width']*w*1.8 for b in long)>len(long)*.6:
        raise ValueError('ROTATED_TEXT_DIRECTION_NOT_CONFIRMED')
    return 0, {'method':'horizontal_saved_ocr','observations':0}

def rotate_mask(m,w,h,turns):
    n=dict(m)
    for key in ['erase','ink','cell']:
        if n.get(key):n[key]=rotate_box(n[key],w,h,turns)
    return n
