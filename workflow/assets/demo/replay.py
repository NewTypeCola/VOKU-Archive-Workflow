"""Replay finalized demo operations against demo-source-safe; never reads private sources.
Requirements: Python 3, Pillow, numpy, and the specified font file. No OCR text is synthesized.
Usage: python3 replay.py 2017/complete --out replayed
"""
from pathlib import Path
import json,hashlib,argparse
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
FONT='/System/Library/Fonts/AppleSDGothicNeo.ttc'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put_rect(mask,rect):
 l,t,r,b=rect;mask[t:b,l:r]=True
def structure_mask(im,b):
 """Only lines that continue beyond the local edit rectangle are protected."""
 a=np.asarray(im.convert('L'));x0,y0,x1,y1=b;h,w=a.shape;mask=np.zeros((y1-y0,x1-x0),bool)
 # Rule must continue on both sides of the edit; word cancellation stays editable.
 left=a[y0:y1,max(0,x0-42):x0];right=a[y0:y1,x1:min(w,x1+42)]
 if left.shape[1]>15 and right.shape[1]>15:
  rr=((left<185).mean(axis=1)>.65)&((right<185).mean(axis=1)>.65)
  mask[rr,:]=True
 above=a[max(0,y0-90):y0,x0:x1];below=a[y1:min(h,y1+90),x0:x1]
 if above.shape[0]>10 and below.shape[0]>10:
  cc=((above<185).mean(axis=0)>.86)&((below<185).mean(axis=0)>.86)
  mask[:,cc]=True
 return mask

def background(im,b,protect=None):
 x0,y0,x1,y1=b;a=np.asarray(im).copy();tile=a[y0:y1,x0:x1];lum=tile.mean(axis=2);values=tile[lum>220]
 color=np.quantile(values,.72,axis=0).astype('uint8') if len(values) else np.array([250,250,250],dtype='uint8')
 fill=np.empty_like(tile);fill[:]=color
 if protect is not None:fill[protect]=tile[protect]
 a[y0:y1,x0:x1]=fill;return Image.fromarray(a)

from PIL import Image, ImageDraw

def union(rs):return [min(r[0] for r in rs),min(r[1] for r in rs),max(r[2] for r in rs),max(r[3] for r in rs)]

def mask_union(size,boxes):
 m=Image.new('L',size,0);d=ImageDraw.Draw(m)
 for l,t,r,b in boxes:d.rectangle((l,t,r-1,b-1),fill=255)
 return m

def paint_union(im,boxes,border):
 import numpy as np
 if not boxes:return
 bounds=union(boxes);local=[[r[0]-bounds[0],r[1]-bounds[1],r[2]-bounds[0],r[3]-bounds[1]] for r in boxes]
 size=(bounds[2]-bounds[0],bounds[3]-bounds[1]);m=mask_union(size,local);a=np.asarray(m)>0
 # Erode the whole union, so overlapping masks have no interior border.
 p=np.pad(a,border);core=a.copy()
 for dy in range(2*border+1):
  for dx in range(2*border+1):core &= p[dy:dy+size[1],dx:dx+size[0]]
 tile=Image.new('RGB',size,'black');tile.paste('white',(0,0,*size),Image.fromarray(core.astype('uint8')*255));im.paste(tile,(bounds[0],bounds[1]),m)


def glyph(text,fs):
 f=ImageFont.truetype(FONT,fs);spacing=max(1,round(fs*.06));bb=ImageDraw.Draw(Image.new('RGBA',(1,1))).multiline_textbbox((0,0),text,font=f,spacing=spacing,align='center')
 im=Image.new('RGBA',(int(bb[2]-bb[0]+4),int(bb[3]-bb[1]+4)),(0,0,0,0));ImageDraw.Draw(im).multiline_text((2-bb[0],2-bb[1]),text,font=f,spacing=spacing,fill=(22,22,22,255),align='center');return im

def cancellation_lines(n,peers=()):
 """New 1 px strokes inside each displayed token row; never restore source ink.

 Rectangles use exclusive right/bottom coordinates. A 2+2 token keeps its layout
 and receives one horizontal stroke per row, not a line in the inter-row gap.
 """
 if n['class']!='staff' or not n.get('input_cancelled'):return []
 token=n['token'];text=token[:2]+'\n'+token[2:] if n['token_layout']=='2+2' else token
 g=glyph(text,n['font_raster_px']);alpha=np.asarray(g.getchannel('A'))>0
 cuts=[(0,g.height//2),(g.height//2,g.height)] if n['token_layout']=='2+2' else [(0,g.height)]
 bx,by,_,_=n['token_box'];lines=[]
 for top,bottom in cuts:
  yy,xx=np.nonzero(alpha[top:bottom]);assert len(xx)
  y=by+top+(int(yy.min())+int(yy.max()))//2
  left,right=bx+int(xx.min()),bx+int(xx.max())+1;segments=[(left,right)]
  for peer in peers:
   if peer['region_id']==n['region_id'] or 'token_box' not in peer:continue
   x0,y0,x1,y1=peer['token_box']
   if not y0<=y<y1:continue
   # Leave a 1 px gap at an adjacent token, without moving either token.
   cut0,cut1=x0-1,x1+1;remaining=[]
   for l,r in segments:
    if cut1<=l or cut0>=r:remaining.append((l,r))
    else:
     if l<cut0:remaining.append((l,cut0))
     if cut1<r:remaining.append((cut1,r))
   segments=remaining
  assert segments,'Cancellation would cross another token'
  l,r=max(segments,key=lambda s:s[1]-s[0]);assert r-l>=(right-left)//2
  lines.append([l,y,r,y+1])
 return lines

def render_layers(safe,p):
 # Keep the repaired order: erase every confirmed name before placing any token.
 name=safe.copy();nmask=np.zeros((safe.height,safe.width),bool);names={n['region_id']:n for n in p['names']}
 for rid in p['erase_sequence']:
  n=names[rid];b=n['erase_box'];put_rect(nmask,b)
  if n['class']=='private':paint_union(name,[b],2)
  else:name=background(name,b,structure_mask(name,b))
 for n in p['names']:
  if n['class']=='private':continue
  token=n['token'];g=glyph(token[:2]+'\n'+token[2:] if n['token_layout']=='2+2' else token,n['font_raster_px']);b=n['token_box'];assert g.size==(b[2]-b[0],b[3]-b[1]);name.paste(g,(b[0],b[1]),g);put_rect(nmask,b)
 # Cancellation belongs to the name layer and its mask, after all token placement.
 for n in p['names']:
  lines=cancellation_lines(n,p['names'])
  if 'cancellation_lines' in n:assert lines==n['cancellation_lines']
  for l,t,r,b in lines:
   ImageDraw.Draw(name).line((l,t,r-1,t),fill=(22,22,22),width=1);put_rect(nmask,[l,t,r,b])
 am=Image.new('L',safe.size,0);ad=ImageDraw.Draw(am)
 for c in p['approval_cells']:
  l,t,r,b=c['box'];ad.rectangle((l,t,r-1,b-1),fill=255)
 approval=safe.copy();approval.paste(safe.filter(ImageFilter.GaussianBlur(22)),(0,0),am)
 contact=safe.copy();paint_union(contact,p['contact_boxes'],2);cm=mask_union(safe.size,p['contact_boxes'])
 return [(name,Image.fromarray(nmask.astype('uint8')*255)),(approval,am),(contact,cm)]

def render(safe,p):
 final=safe.copy()
 for im,mask in render_layers(safe,p):final.paste(im,(0,0),mask)
 return final

def main():
 global FONT
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('bundle',type=Path);ap.add_argument('--out',required=True,type=Path);ap.add_argument('--font',default=FONT);a=ap.parse_args();FONT=a.font
 spec=json.loads((a.bundle/'operations.json').read_text());assert sha(Path(FONT))==spec['font_sha256'],'Font differs; exact pixel replay requires the recorded font.'
 results=[]
 for p in spec['pages']:
  src=a.bundle/'demo-source-safe'/p['filename'];assert sha(src)==p['safe_input_sha256'];safe=Image.open(src).convert('RGB');assert hashlib.sha256(safe.tobytes()).hexdigest()==p['safe_input_pixel_sha256'];final=render(safe,p)
  pixel_sha=hashlib.sha256(final.tobytes()).hexdigest();assert pixel_sha==p['final_pixel_sha256'],p['filename']+' pixels differ'
  dest=a.out/p['filename'];dest.parent.mkdir(parents=True,exist_ok=True);final.save(dest,'WEBP',**{k:spec['delivery_encoding'][k] for k in ['lossless','quality','method','exact']})
  assert sha(dest)==p['final_sha256'],p['filename']+' encoding differs; use the Pillow/libwebp versions recorded in operations.json'
  results.append({'page':p['filename'],'sha256':sha(dest),'pixel_sha256':pixel_sha,'matches_recorded_final':True})
 (a.out/'replay-verification.json').write_text(json.dumps(results,indent=2)+'\n');print('Verified',len(results),'images against recorded final SHA-256.')
if __name__=='__main__':main()
