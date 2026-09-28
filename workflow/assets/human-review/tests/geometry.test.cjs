const assert=require('node:assert/strict');
const G=require('../geometry.js');
for(const scale of [.05,.37,1,1.25,3,8]){
  const r={left:93,top:57,width:3000*scale,height:4000*scale};
  const a=G.point(93+123*scale,57+234*scale,r,3000,4000);
  const b=G.point(93+923*scale,57+1234*scale,r,3000,4000);
  assert.deepEqual(G.rect(a,b),{x:123,y:234,width:800,height:1000});
  assert.deepEqual(G.rect(b,a),{x:123,y:234,width:800,height:1000});
}
const b={id:'a',x:10,y:20,width:100,height:200,color:0};
assert.deepEqual(G.move(b,-100,-100,300,400),{...b,x:0,y:0});
assert.deepEqual(G.move(b,10000,10000,300,400),{...b,x:200,y:200});
for(const handle of ['n','s','w','e','nw','ne','sw','se']){
  for(const p of [{x:-100,y:-100},{x:5000,y:6000},{x:55,y:100}]){
    const out=G.resize(b,handle,p,300,400);
    assert(out.x>=0&&out.y>=0&&out.width>=1&&out.height>=1);
    assert(out.x+out.width<=300&&out.y+out.height<=400);
  }
}
for(const scale of [.05,.37,1,1.25,3,8]){
  const r={left:93,top:57,width:4000*scale,height:3000*scale};
  const a=G.point(93+234*scale,57+(3000-123)*scale,r,3000,4000,270);
  assert.equal(Math.round(a.x),123);
  assert.equal(Math.round(a.y),234);
  const b=G.point(93+1234*scale,57+(3000-923)*scale,r,3000,4000,270);
  assert.equal(Math.round(b.x),923);
  assert.equal(Math.round(b.y),1234);
  assert.deepEqual(G.rect(a,b),{x:123,y:234,width:800,height:1000});
}
for(const scale of [1,2]){
  const r180={left:93,top:57,width:3000*scale,height:4000*scale};
  const a180=G.point(93+(3000-123)*scale,57+(4000-234)*scale,r180,3000,4000,180);
  assert.equal(Math.round(a180.x),123);
  assert.equal(Math.round(a180.y),234);
  const r90={left:93,top:57,width:4000*scale,height:3000*scale};
  const a90=G.point(93+(4000-234)*scale,57+123*scale,r90,3000,4000,90);
  assert.equal(Math.round(a90.x),123);
  assert.equal(Math.round(a90.y),234);
}
console.log('PASS: 6 zoom scales, 4 rotations, reversed drags, 8 resize handles, movement and image bounds');
