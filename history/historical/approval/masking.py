"""Build masks solely from confirmed cell geometry; historical default is 3/5."""
import cv2,numpy as np

def poly_mask(shape,poly):
 a=np.zeros(shape,np.uint8);cv2.fillPoly(a,[np.rint(poly).astype(np.int32)],255);return a

def effective_bbox(mask):
 ys,xs=np.nonzero(mask)
 return [int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)] if len(xs) else None

def plan(shape,grids,target_cells=(3,5)):
 target_cells={str(n) for n in target_cells};assert target_cells and target_cells<=set("357")
 h,w=shape[:2];shape=(h,w);allowed=np.zeros(shape,np.uint8);protected=np.zeros(shape,np.uint8);border=np.zeros(shape,np.uint8)
 regions=[];holds=[];source_cells=[]
 for gi,g in enumerate(grids):
  # Guard width is derived from analysis-to-original scale, not stamp content.
  inv=np.array(g['analysis_to_original']);guard=max(2,int(np.ceil(np.linalg.norm(inv[:2,0])*3)))
  for n,c in g['cells'].items():
   pm=poly_mask(shape,c['polygon'])
   cv2.polylines(border,[np.rint(c['polygon']).astype(np.int32)],True,255,guard*2+1)
   if n not in target_cells:protected|=pm
   if n in target_cells:source_cells.append((gi,n,c,pm,guard))
 protected|=border
 for gi,n,c,full,guard in source_cells:
  inside=cv2.erode(full,np.ones((guard*2+1,guard*2+1),np.uint8));inside[protected>0]=0
  if not inside.any():holds.append({'grid':gi,'cell':n,'reason':'CELL_INTERIOR_TOO_SMALL'});continue
  allowed|=inside
  regions.append({'grid':gi,'cell':int(n),'kind':'cell_interior','method':'seven_column_cell_inset_preserve_boundaries','bbox':effective_bbox(inside),'polygon':c['polygon'],'inset_px':guard})
 allowed[protected>0]=0
 return allowed,protected,regions,holds
