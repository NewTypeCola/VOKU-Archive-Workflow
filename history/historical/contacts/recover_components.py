import numpy as np
from paint_union import union

def area(r):return max(0,r[2]-r[0])*max(0,r[3]-r[1])

def components(a):
 parents=[];bounds=[];prev=[]
 def root(i):
  while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
  return i
 for y,row in enumerate(a):
  es=np.diff(np.r_[False,row,False].astype('int8'));starts=np.flatnonzero(es==1);ends=np.flatnonzero(es==-1);curr=[];j=0
  for l,r in zip(starts,ends):
   l=int(l);r=int(r)
   while j<len(prev) and prev[j][1]<l:j+=1
   hits=[];k=j
   while k<len(prev) and prev[k][0]<=r:
    hits.append(root(prev[k][2]));k+=1
   if not hits:i=len(parents);parents.append(i);bounds.append([l,y,r,y+1])
   else:
    i=hits[0];bounds[i]=union([bounds[i],[l,y,r,y+1]])
    for h in hits[1:]:
     h=root(h);i=root(i)
     if h!=i:parents[h]=i;bounds[i]=union([bounds[i],bounds[h]])
   curr.append((l,r,i))
  prev=curr
 return [bounds[i] for i in range(len(parents)) if root(i)==i and area(bounds[i])>=6]
