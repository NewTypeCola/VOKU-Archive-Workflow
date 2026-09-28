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
