/* Pure geometry, in original image pixels. Shared by UI and boundary tests. */
(function(root){
  const clamp=(v,low,high)=>Math.max(low,Math.min(high,v));
  const point=(x,y,r,w,h,rot=0)=>{
    const deg=((rot%360)+360)%360;
    if(deg===90) return {x:clamp((y-r.top)*w/r.height,0,w),y:clamp(h-(x-r.left)*h/r.width,0,h)};
    if(deg===180) return {x:clamp(w-(x-r.left)*w/r.width,0,w),y:clamp(h-(y-r.top)*h/r.height,0,h)};
    if(deg===270) return {x:clamp(w-(y-r.top)*w/r.height,0,w),y:clamp((x-r.left)*h/r.width,0,h)};
    return {x:clamp((x-r.left)*w/r.width,0,w),y:clamp((y-r.top)*h/r.height,0,h)};
  };
  const rect=(a,b)=>({x:Math.round(Math.min(a.x,b.x)),y:Math.round(Math.min(a.y,b.y)),width:Math.round(Math.max(a.x,b.x))-Math.round(Math.min(a.x,b.x)),height:Math.round(Math.max(a.y,b.y))-Math.round(Math.min(a.y,b.y))});
  const move=(b,dx,dy,w,h)=>({...b,x:clamp(Math.round(b.x+dx),0,w-b.width),y:clamp(Math.round(b.y+dy),0,h-b.height)});
  const resize=(b,handle,p,w,h)=>{
    let l=b.x,t=b.y,r=b.x+b.width,bt=b.y+b.height;
    if(handle.includes('w')) l=clamp(Math.round(p.x),0,r-1);
    if(handle.includes('e')) r=clamp(Math.round(p.x),l+1,w);
    if(handle.includes('n')) t=clamp(Math.round(p.y),0,bt-1);
    if(handle.includes('s')) bt=clamp(Math.round(p.y),t+1,h);
    return {...b,x:l,y:t,width:r-l,height:bt-t};
  };
  const api={clamp,point,rect,move,resize};
  if(typeof module!=='undefined') module.exports=api; else root.Geometry=api;
})(typeof window==='undefined'?{}:window);
