// Execute each app's real key handler against independent behavior scenarios.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
for(const root of ['.']){
 const script=fs.readFileSync(require('node:path').join(__dirname,'../app.js'),'utf8');
 const handler=script.slice(script.indexOf("document.addEventListener('keydown',e=>{"),script.indexOf('async function refreshStats(){'));
 let cases=0;
 function run({mode=true,pending=null,selected=null,draw=false,drag=null,input=false,name='',composition=false,key='Enter',code='',repeat=false,hold=root==='hold-review'}={}){
  const calls=[];let fn;
  const elements={browseDialog:{open:false},viewport:{focus:()=>calls.push('focus-viewport')}};
  const state={loaded:true,busy:false,conflict:false,current:{available:1,source_condition:''},pendingBox:pending,selected,draw,drag};
  const context={document:{addEventListener:(type,f)=>fn=f},state,IS_HOLD:hold,$:id=>elements[id],nameMode:()=>mode,notify:()=>calls.push('notify'),renderBoxes:()=>{},focusName:id=>calls.push('focus-'+id),startBox:()=>calls.push('add'),confirmBox:()=>calls.push('confirm'),finishPointer:()=>{state.drag=null;state.pendingBox='drawn'},completeNext:s=>calls.push(s),navigate:d=>calls.push(d),rotateLeft:()=>calls.push('rotate')};
  vm.runInNewContext(handler,context);
  fn({key,code,repeat,isComposing:composition,keyCode:composition?229:0,preventDefault:()=>{},target:{value:name,dataset:input==='name'?{nameInput:'b1'}:{},closest:s=>s.includes('input')?input:false}});
  cases++;return calls;
 }
 assert.deepEqual(run({key:'b',code:'KeyB'}),['add']);
 assert.deepEqual(run({pending:'b1'}),['confirm']);
 assert.deepEqual(run({drag:{pointer:1}}),['confirm']);
 assert.deepEqual(run({input:'name',name:'홍길동'}),['focus-viewport']);
 assert.deepEqual(run({input:'name',name:''}),['notify']);
 assert.deepEqual(run({input:'name',name:'홍',composition:true}),[]);
 assert.deepEqual(run({input:true,key:' '}),[]);
 assert.deepEqual(run({key:'Enter'}),['issue']);
 assert.deepEqual(run({key:' '}),['ok']);
 assert.deepEqual(run({key:'Enter',repeat:true}),[]);
 assert.deepEqual(run({key:' ',selected:'b1'}),[]);
 assert.deepEqual(run({key:'Enter',selected:'b1'}),['focus-b1']);
 assert.deepEqual(run({key:'ArrowRight',hold:true}),['next']);
 assert.deepEqual(run({key:'ArrowLeft',hold:true}),['previous']);
 assert.deepEqual(run({key:'ArrowUp',hold:true}),[]);
 assert.deepEqual(run({mode:false,key:' '}),['needs_review']);
 assert.deepEqual(run({mode:false,key:'ArrowRight'}),['ok']);
 assert.deepEqual(run({mode:false,key:'b'}),[]);
 console.log(`${root}: ${cases} keyboard / IME / focus scenarios passed`);
}
