'use strict';
const $=id=>document.getElementById(id);
const LABELS={unreviewed:'Unreviewed',ok:'OK',issue:'Issue',needs_review:'Needs review'};
const TYPES={unmasked_name:'Name not redacted',wrong_target:'Wrong target redacted',mask_geometry:'Wrong redaction region',text_damage:'Surrounding text damaged',token_missing:'Station-member token missing/wrong',token_legibility:'Station-member token placement/legibility',other:'Other'};
const COLORS=['#d05a37','#3576c4','#9472bd','#28896b','#c19128','#c05692','#328f9f','#865f45'];
const G=Geometry;
const IS_HOLD=false;
const state={view:'after',current:null,selected:null,draw:false,drag:null,loaded:false,busy:false,scale:1,fit:true,rotation:0,nameMode:IS_HOLD,pendingBox:null,fitKind:'page',editSeq:0,savedSeq:0,saving:null,conflict:false,dataset:'',query:'',filter:'',offset:0,listTotal:0,historyOffset:0};
let saveTimer,toastTimer,searchTimer,polling=false;
const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const clone=x=>JSON.parse(JSON.stringify(x));
const color=b=>COLORS[b.color%COLORS.length];
const fmt=n=>Number(n).toLocaleString('en-US');
function notify(message){$('toast').textContent=message;$('toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').hidden=true,4500);}
function savedLabel(text,error=false){$('saveState').textContent=text;$('saveState').classList.toggle('error',error);}
async function api(path,body){return PublicReview.request(path,body);}
function params(x){return new URLSearchParams(x).toString();}
function draftKey(pid=state.current?.page_id){return `voku-public-review-draft:${state.dataset}:${pid}`;}
function payload(){const c=state.current;return {page_id:c.page_id,fingerprint:c.fingerprint,revision:c.revision,status:c.status,issues:clone(c.issues),note:c.note,boxes:clone(c.boxes)};}
function persistDraft(){try{localStorage.setItem(draftKey(),JSON.stringify({...payload(),pending_box:state.pendingBox,saved_locally_at:new Date().toISOString()}));}catch(ex){$('draftConflict').hidden=false;savedLabel('Browser backup failed',true);notify('Browser draft storage failed. Download the draft as JSON.');}}
function edited(){if(!state.current)return;state.editSeq++;persistDraft();savedLabel(state.pendingBox?'BBOX awaiting confirmation':'Saving…');clearTimeout(saveTimer);saveTimer=setTimeout(()=>flush().catch(showError),280);}
function showError(ex){savedLabel(ex.status===409?'Conflict · draft retained':'Save failed · check draft',true);$('draftConflict').hidden=!state.current;$('draftConflict').querySelector('p').textContent=ex.status===409?'Another tab has conflicting records. Download your draft or load the latest saved records.':'Save failed. You can download your draft as JSON.';if(ex.status===409){state.conflict=true;}notify(ex.message);controls();}
async function flush(){
  clearTimeout(saveTimer);if(state.drag||state.pendingBox)return;if(state.saving)return state.saving;if(!state.current||state.editSeq===state.savedSeq)return;
  if(state.conflict)throw Object.assign(new Error('Resolve the save conflict first. You can download your draft.'),{status:409});
  state.saving=(async()=>{
    while(state.savedSeq<state.editSeq){
      if(state.drag||state.pendingBox)return;
      const seq=state.editSeq,body=payload();const result=await api('/api/review',body);
      if(state.current.page_id!==result.page_id)throw new Error('Page save order error');
      state.current.revision=result.revision;state.current.updated_at=result.updated_at;state.savedSeq=seq;
      if(state.editSeq===seq&&!state.pendingBox&&!state.drag){localStorage.removeItem(draftKey());savedLabel('✓ Autosaved');}
      else persistDraft();
    }
  })();
  try{await state.saving;await refreshStats();}finally{state.saving=null;}
}
function controls(){
  const blocked=!state.current||!state.loaded||state.busy||state.conflict||!!state.drag||state.view==='before';
  for(const [id,view] of [['beforeView','before'],['afterView','after']]){$(id).disabled=!state.current||state.busy||!!state.drag||!!state.pendingBox;$(id).setAttribute('aria-pressed',String(state.view===view));}
  $('overlay').toggleAttribute('hidden',state.view==='before');
  $('viewHint').textContent=state.view==='before'?'Comparing public input · enter feedback on the final output.':'Leave feedback on the final output.';
  for(const id of ['addBox','reviewStatus','note','okNext','issueNext'])$(id).disabled=blocked;
  $('reviewStatus').disabled=blocked||!!state.pendingBox;
  document.querySelectorAll('#issueTypes input').forEach(el=>el.disabled=blocked);
  $('deleteBox').disabled=blocked||!state.selected;$('clearBoxes').disabled=blocked||!state.current?.boxes.length;
  for(const id of ['previous','next','browseButton'])$(id).disabled=state.busy||!!state.drag;
  for(const id of ['zoomIn','zoomOut','fitButton','rotateButton'])$(id).disabled=!state.loaded||!!state.drag;
  $('addBox').setAttribute('aria-pressed',String(state.draw));$('finishEdit').hidden=!(state.draw||state.selected);
  $('confirmBox').hidden=!state.pendingBox;$('confirmBox').disabled=!!state.drag||state.busy;
  $('issueSection').hidden=nameMode();
  $('widthFitButton').disabled=!state.loaded||!!state.drag;
  $('addBox').title=nameMode()?'Add BBOX (B)':'';
  $('addBox').textContent=nameMode()?'＋ Add BBOX (B)':'＋ Add BBOX';
  $('viewport').classList.toggle('drawing',state.draw);
  const targetLabel=LABELS[!IS_HOLD&&nameMode()?'needs_review':state.filter]||'Unreviewed';
  const okSpan=$('okNext').querySelector('span');if(okSpan)okSpan.textContent=`Next ${targetLabel} →`;
  const issueSpan=$('issueNext').querySelector('span');if(issueSpan)issueSpan.textContent=`Next ${targetLabel} →`;
  $('shortcutHint').textContent=state.pendingBox?'Click the region or press Enter to confirm BBOX → enter name':nameMode()?'B add region · Enter save and next · Space OK'+(IS_HOLD?' · ← → browse':''):(state.draw||state.selected||state.drag?'Editing BBOX · finish editing to resume shortcuts':`↑↓←→ OK · Space Needs review · R rotate → next ${targetLabel}`);
  if(state.view==='before')$('shortcutHint').textContent='Comparing public input · return to final output to continue review.';
  $('okNext').firstChild.textContent=nameMode()?'✓ OK (Space) ':'✓ OK (arrow keys) ';
  $('issueNext').firstChild.textContent=nameMode()?'Save issue (Enter) ':'Save issue ';
  renderNames();
}
function renderForm(){
  const c=state.current;$('reviewStatus').value=c.status;$('note').value=c.note;
  document.querySelectorAll('#issueTypes input').forEach(el=>el.checked=c.issues.includes(el.value));
  $('filename').textContent=c.filename;$('fileMeta').textContent=`${c.page_id} · Final output ${c.sha256.slice(0,12)} · Record #${c.generation}`;
  $('sampleEvidence').innerHTML=`<p>${escapeHTML(c.context)}</p><p>Resolved records from the existing execution demo, separate from visitor review history below.</p><p><a href="${escapeHTML(c.evidence.decisions)}">Public decisions</a> · <a href="${escapeHTML(c.evidence.operations)}">Episode operations</a> · <a href="${escapeHTML(c.evidence.page_map)}">Page/hash mapping</a></p><details><summary>View names, tokens, and regions for this page</summary><pre></pre></details>`;
  $('sampleEvidence').querySelector('pre').textContent=JSON.stringify(c.operations,null,2);
  $('imageSize').textContent=c.width?`${fmt(c.width)} × ${fmt(c.height)} px · Final-output image coordinates`:'Image dimensions unavailable';
  $('generation').textContent=`Record #${c.generation}`;
  const reason=c.source_condition?({manifest_hash_mismatch:'File and manifest hashes differ. Sync after the output update is complete.',file_missing:'Output image is missing. Existing reviews are retained.',removed_from_manifest:'Page removed from the current output index. Existing reviews are retained.'}[c.source_condition]||c.source_condition):c.status==='needs_review'&&c.source_changed_at?'The output changed or needs another review. Earlier reviews and coordinates remain in history.':'';
  $('sourceWarning').textContent=reason;$('sourceWarning').hidden=!reason;
  renderBoxes();controls();
}
function renderBoxes(){
  const c=state.current;if(!c)return;const boxes=c.boxes,scale=state.scale||1;
  $('boxCount').textContent=`${boxes.length}`;$('boxListCount').textContent=boxes.length;
  $('boxList').innerHTML=boxes.length?boxes.map((b,i)=>`<button class="box-row ${state.selected===b.id?'selected':''}" data-box-id="${escapeHTML(b.id)}" style="--box-color:${color(b)}" aria-label="BBOX ${i+1} select"><span class="box-badge">${i+1}</span><span>BBOX ${i+1}<span class="box-coords">x ${b.x} · y ${b.y}<br>w ${b.width} · h ${b.height}　px${b.name?' · '+escapeHTML(b.name):''}</span></span></button>`).join(''):'<p class="empty-boxes">Click Add BBOX, then drag on the image.</p>';
  let markup='';
  boxes.forEach((b,i)=>{
    const selected=state.selected===b.id,col=color(b),id=escapeHTML(b.id);
    markup+=`<g data-box-id="${id}"><rect class="bbox" data-box-id="${id}" x="${b.x}" y="${b.y}" width="${b.width}" height="${b.height}" fill="${col}" fill-opacity="${selected?.16:.08}" stroke="${col}" stroke-width="${selected?3:2}" stroke-dasharray="7 4" vector-effect="non-scaling-stroke"/>`;
    markup+=`<text class="box-number" x="${b.x+5/scale}" y="${b.y+17/scale}" font-size="${14/scale}" fill="${col}" style="stroke-width:${3/scale}px">${i+1}</text>`;
    if(selected){
      const points={nw:[b.x,b.y],n:[b.x+b.width/2,b.y],ne:[b.x+b.width,b.y],e:[b.x+b.width,b.y+b.height/2],se:[b.x+b.width,b.y+b.height],s:[b.x+b.width/2,b.y+b.height],sw:[b.x,b.y+b.height],w:[b.x,b.y+b.height/2]};
      for(const [key,[x,y]] of Object.entries(points))markup+=`<rect class="handle" data-box-id="${id}" data-handle="${key}" x="${x-5/scale}" y="${y-5/scale}" width="${10/scale}" height="${10/scale}" fill="white" stroke="${col}" stroke-width="2" vector-effect="non-scaling-stroke" style="cursor:${key}-resize"/>`;
    }markup+='</g>';
  });
  $('overlay').innerHTML=markup;controls();
}
function selectBox(id){if(state.pendingBox){confirmBox();return;}state.selected=id;state.draw=false;renderBoxes();if(nameMode())focusName(id);}
function setZoom(scale,fit=false){
  if(!state.current?.width||!state.loaded)return;
  const vp=$('viewport'),stage=$('imageStage'),canvas=$('stageCanvas');const old=state.scale;
  const cx=(vp.scrollLeft+vp.clientWidth/2)/old,cy=(vp.scrollTop+vp.clientHeight/2)/old;
  state.fit=fit;state.scale=G.clamp(scale,.05,8);
  const isRotated=(state.rotation%180!==0);
  const visualW=(isRotated?state.current.height:state.current.width)*state.scale;
  const visualH=(isRotated?state.current.width:state.current.height)*state.scale;
  stage.style.width=`${visualW}px`;stage.style.height=`${visualH}px`;
  if(canvas){
    canvas.style.width=`${state.current.width*state.scale}px`;
    canvas.style.height=`${state.current.height*state.scale}px`;
    canvas.style.transform=`translate(-50%,-50%) rotate(${state.rotation}deg)`;
  }
  $('zoomValue').textContent=`${Math.round(state.scale*100)}%`;
  if(fit){vp.scrollTop=0;vp.scrollLeft=0;}else{vp.scrollLeft=cx*state.scale-vp.clientWidth/2;vp.scrollTop=cy*state.scale-vp.clientHeight/2;}
  renderBoxes();
}
function fitImage(kind=state.fitKind){
  const vp=$('viewport');if(!state.current?.width)return;
  state.fitKind=kind;const rotated=state.rotation%180!==0;
  const w=rotated?state.current.height:state.current.width,h=rotated?state.current.width:state.current.height;
  const widthScale=(vp.clientWidth-32)/w;
  setZoom(kind==='width'?widthScale:Math.min(widthScale,(vp.clientHeight-32)/h),true);
}
function rotateLeft(){
  if(!state.loaded||!state.current)return;
  state.rotation=(state.rotation+270)%360;
  fitImage();
  controls();
}
function recoverDraft(){
  const raw=localStorage.getItem(draftKey());if(!raw)return;let draft;
  try{draft=JSON.parse(raw);}catch{return;}
  const c=state.current;
  if(draft.fingerprint===c.fingerprint&&draft.revision===c.revision){
    for(const k of ['status','issues','note','boxes'])c[k]=draft[k];state.pendingBox=draft.pending_box||null;edited();notify('Draft from the previous session recovered.');
  }else if(['status','issues','note','boxes'].every(k=>JSON.stringify(draft[k])===JSON.stringify(c[k]))&&draft.fingerprint===c.fingerprint){localStorage.removeItem(draftKey());}
  else{state.conflict=true;$('draftConflict').hidden=false;savedLabel('Check retained draft',true);}
}
async function openImage(pid){
  if(!pid)return;state.loaded=false;controls();
  const c=await api('/api/image?'+params({page_id:pid}));state.current=c;state.nameMode=IS_HOLD||state.filter==='needs_review'||c.status==='needs_review';state.pendingBox=null;state.fitKind=nameMode()?'width':'page';state.selected=null;state.draw=false;state.drag=null;state.rotation=0;state.fit=true;state.view='after';state.editSeq=state.savedSeq=0;state.conflict=false;
  $('draftConflict').hidden=true;document.querySelector('.review-scroll').scrollTop=0;$('historyDetails').open=false;$('historyList').replaceChildren();state.historyOffset=0;
  savedLabel(c.updated_at?'✓ Autosaved':'Unreviewed · autosave');recoverDraft();renderForm();
  loadImageView();
  await api('/api/session',{page_id:pid,q:state.query,status:state.filter});
}
function loadImageView(){
  const c=state.current;state.loaded=false;controls();
  $('pageImage').onload=()=>{
    if(state.current!==c)return;
    if($('pageImage').naturalWidth!==c.width||$('pageImage').naturalHeight!==c.height){imageFailure('Image dimensions differ from the public catalog.');return;}
    state.loaded=true;$('emptyState').hidden=true;$('imageStage').style.display='block';
    $('overlay').setAttribute('viewBox',`0 0 ${c.width} ${c.height}`);
    if(state.fit)fitImage();else setZoom(state.scale);controls();
  };
  $('pageImage').onerror=()=>imageFailure('Cannot load the public image. Check distribution files and links.');
  $('imageStage').style.display='none';$('emptyState').hidden=false;
  $('emptyState').innerHTML='<span class="empty-icon">▧</span><h2>Loading image…</h2>';
  $('pageImage').alt=state.view==='before'?'Public input image with synthetic personal identifiers':'Final processed image from the public demo';
  $('pageImage').src=c.images[state.view];
}
async function switchView(view){
  await withBusy(async()=>{await flush();state.view=view;state.selected=null;state.draw=false;loadImageView();});
}
$('beforeView').onclick=()=>switchView('before');$('afterView').onclick=()=>switchView('after');
function imageFailure(message){state.loaded=false;$('imageStage').style.display='none';$('emptyState').hidden=false;$('emptyState').innerHTML=`<span class="empty-icon">▧</span><h2>${escapeHTML(message)}</h2>`;controls();}
async function withBusy(fn){if(state.busy||state.drag)return;if(state.pendingBox){notify('Click the BBOX or press Enter to confirm it first.');return;}state.busy=true;controls();try{await fn();}catch(ex){showError(ex);}finally{state.busy=false;controls();}}
async function navigate(direction){await withBusy(async()=>{await flush();const r=await api('/api/neighbor?'+params({page_id:state.current?.page_id||'',direction,q:state.query,status:state.filter}));if(r.page_id)await openImage(r.page_id);else notify(direction==='previous'?'This is the first image.':'This is the last image.');});}
function changeToOk(){
  const c=state.current;
  if(c.boxes.length||c.issues.length){
    if(!confirm('Issue regions and types exist. Clear them and save as OK? Previous contents remain in history. The note is retained.'))return false;
    c.boxes=[];c.issues=[];state.selected=null;state.draw=false;
  }
  c.status='ok';edited();renderForm();return true;
}
async function completeNext(status){
  if(!state.loaded||state.conflict||state.view==='before')return;
  if(nameMode()&&missingName())return;
  await withBusy(async()=>{
    // Commit current annotations first so clearing them can never erase the only copy.
    await flush();
    if(status==='ok'){if(!changeToOk())return;}else{state.current.status=status;edited();renderForm();}
    await flush();await refreshStats();
    const r=await api('/api/neighbor?'+params({page_id:state.current.page_id,direction:'unreviewed',q:state.query,status:(!IS_HOLD&&nameMode()?'needs_review':state.filter)}));
    if(r.page_id)await openImage(r.page_id);
    else{
      const label=LABELS[!IS_HOLD&&nameMode()?'needs_review':state.filter]||'Unreviewed';
      notify(state.query?`All ${label} images in this search have been reviewed.`:`All currently listed ${label} images have been reviewed.${state.filter?'':''}`);
    }
  });
}
function markIssue(){if(state.current.status==='ok'||state.current.status==='unreviewed')state.current.status=nameMode()?'needs_review':'issue';$('reviewStatus').value=state.current.status;}
$('issueTypes').innerHTML=Object.entries(TYPES).map(([key,label])=>`<label class="issue-option"><input type="checkbox" value="${key}"><span>${label}</span></label>`).join('');
$('issueTypes').addEventListener('change',()=>{state.current.issues=[...document.querySelectorAll('#issueTypes input:checked')].map(e=>e.value);if(state.current.issues.length)markIssue();edited();});
$('note').addEventListener('input',()=>{state.current.note=$('note').value;edited();});
$('reviewStatus').addEventListener('change',()=>{const value=$('reviewStatus').value;if(value==='ok'){withBusy(async()=>{await flush();if(!changeToOk())$('reviewStatus').value=state.current.status;});}else{state.current.status=value;if(value==='needs_review'&&!nameMode()){state.nameMode=true;fitImage('width');}edited();renderForm();}});
$('boxList').addEventListener('click',e=>{const el=e.target.closest('[data-box-id]');if(el)selectBox(el.dataset.boxId);});
$('addBox').onclick=startBox;
$('finishEdit').onclick=()=>{if(state.pendingBox){confirmBox();return;}state.draw=false;state.selected=null;renderBoxes();$('viewport').focus();};
$('deleteBox').onclick=()=>{if(!state.selected)return;state.current.boxes=state.current.boxes.filter(b=>b.id!==state.selected);state.selected=null;state.pendingBox=null;edited();renderBoxes();};
$('clearBoxes').onclick=()=>{if(!confirm('Delete all BBOXes on this image? Saved coordinates remain in history.'))return;state.current.boxes=[];state.selected=null;state.pendingBox=null;edited();renderBoxes();};
$('zoomIn').onclick=()=>setZoom(state.scale*1.25);$('zoomOut').onclick=()=>setZoom(state.scale/1.25);$('fitButton').onclick=()=>fitImage('page');$('widthFitButton').onclick=()=>fitImage('width');$('rotateButton').onclick=rotateLeft;
new ResizeObserver(()=>{if(state.fit&&!state.drag)fitImage();}).observe($('viewport'));
function originalPoint(e){
  const c=state.current;
  const svg=$('overlay');
  if(svg.getScreenCTM&&svg.createSVGPoint){
    try{
      const pt=svg.createSVGPoint();pt.x=e.clientX;pt.y=e.clientY;
      const ctm=svg.getScreenCTM();
      if(ctm){
        const p=pt.matrixTransform(ctm.inverse());
        return {x:G.clamp(Math.round(p.x),0,c.width),y:G.clamp(Math.round(p.y),0,c.height)};
      }
    }catch(err){}
  }
  return G.point(e.clientX,e.clientY,$('imageStage').getBoundingClientRect(),c.width,c.height,state.rotation);
}
$('overlay').addEventListener('pointerdown',e=>{
  if(state.view==='before'||e.button!==0||!state.loaded||state.busy||state.conflict||!state.current.available||state.current.source_condition)return;
  if(state.pendingBox){e.preventDefault();confirmBox();return;}
  e.preventDefault();clearTimeout(saveTimer);$('viewport').focus();const p=originalPoint(e),el=e.target.closest('[data-box-id]'),before=clone(state.current.boxes);
  if(state.draw){
    const b={id:crypto.randomUUID(),name:'',color:state.current.boxes.reduce((n,b)=>Math.max(n,b.color+1),0),x:Math.round(p.x),y:Math.round(p.y),width:0,height:0};
    state.current.boxes.push(b);state.selected=b.id;state.drag={kind:'draw',start:p,before,id:b.id,pointer:e.pointerId};
  }else if(el){
    const b=state.current.boxes.find(b=>b.id===el.dataset.boxId);state.selected=b.id;
    state.drag={kind:el.dataset.handle?'resize':'move',handle:el.dataset.handle,start:p,initial:clone(b),before,id:b.id,pointer:e.pointerId};
  }else{state.selected=null;renderBoxes();return;}
  $('overlay').setPointerCapture(e.pointerId);renderBoxes();
});
$('overlay').addEventListener('pointermove',e=>{
  const d=state.drag;if(!d||d.pointer!==e.pointerId)return;e.preventDefault();const p=originalPoint(e),c=state.current;
  const i=c.boxes.findIndex(b=>b.id===d.id),b=c.boxes[i];
  if(d.kind==='draw')c.boxes[i]={...b,...G.rect(d.start,p)};
  if(d.kind==='move')c.boxes[i]=G.move(d.initial,p.x-d.start.x,p.y-d.start.y,c.width,c.height);
  if(d.kind==='resize')c.boxes[i]=G.resize(d.initial,d.handle,p,c.width,c.height);
  renderBoxes();
});
function finishPointer(e,cancel=false){
  const d=state.drag;if(!d||d.pointer!==e.pointerId)return;
  if(cancel){state.current.boxes=d.before;state.selected=null;}
  else{
    const b=state.current.boxes.find(b=>b.id===d.id);
    if(d.kind==='draw'&&(b.width<2||b.height<2)){state.current.boxes=d.before;state.selected=null;}
    else if(JSON.stringify(d.before)!==JSON.stringify(state.current.boxes)){
      if(d.kind==='draw'&&nameMode()){state.pendingBox=b.id;persistDraft();savedLabel('BBOX awaiting confirmation');}
      else{markIssue();edited();}
    }
    state.draw=false;
  }
  state.drag=null;if($('overlay').hasPointerCapture(e.pointerId))$('overlay').releasePointerCapture(e.pointerId);renderBoxes();if(state.editSeq!==state.savedSeq){clearTimeout(saveTimer);saveTimer=setTimeout(()=>flush().catch(showError),280);}
}
$('overlay').addEventListener('pointerup',e=>finishPointer(e));$('overlay').addEventListener('pointercancel',e=>finishPointer(e,true));
$('overlay').addEventListener('lostpointercapture',e=>{if(state.drag)finishPointer(e,true);});
$('okNext').onclick=()=>completeNext('ok');$('issueNext').onclick=()=>completeNext('issue');$('previous').onclick=()=>navigate('previous');$('next').onclick=()=>navigate('next');

function nameMode(){return state.nameMode;}
function focusName(id){
  const input=[...document.querySelectorAll('[data-name-input]')].find(el=>el.dataset.nameInput===id);
  if(input){input.focus();input.scrollIntoView({block:'nearest'});}
}
function renderNames(){
  const visible=!!state.current&&(nameMode()||state.current.boxes.some(b=>b.name));
  $('namesSection').hidden=!visible;$('issueSection').hidden=nameMode();
  if(!visible)return;
  const boxes=state.current.boxes,key=boxes.map(b=>b.id).join('|');
  if($('nameFields').dataset.key!==key){
    $('nameFields').dataset.key=key;
    $('nameFields').innerHTML=boxes.length?boxes.map((b,i)=>`<label class="name-row" style="--box-color:${color(b)}"><span><b>BBOX ${i+1}</b><small data-name-coords="${escapeHTML(b.id)}"></small></span><input data-name-input="${escapeHTML(b.id)}" aria-label="BBOX ${i+1} name" placeholder="Enter a synthetic name" maxlength="200" autocomplete="off" spellcheck="false"></label>`).join(''):'<p class="empty-boxes">Press B and draw a region to add a name field.</p>';
  }
  boxes.forEach(b=>{
    const input=[...document.querySelectorAll('[data-name-input]')].find(el=>el.dataset.nameInput===b.id);
    if(!input)return;
    if(document.activeElement!==input)input.value=b.name||'';
    input.disabled=state.view==='before'||!state.loaded||state.busy||state.conflict||!!state.drag||b.id===state.pendingBox||!state.current.available||!!state.current.source_condition;
    input.closest('.name-row').classList.toggle('selected',state.selected===b.id);
    const coords=[...document.querySelectorAll('[data-name-coords]')].find(el=>el.dataset.nameCoords===b.id);
    coords.textContent=`x ${b.x} · y ${b.y} · ${b.width} × ${b.height} px${b.id===state.pendingBox?' · awaiting confirmation':''}`;
  });
}
function missingName(){
  const box=state.current.boxes.find(b=>!(b.name||'').trim());
  if(!box)return false;
  state.selected=box.id;renderBoxes();focusName(box.id);
  notify('Check BBOXes with empty name fields.');return true;
}
function startBox(){
  if($('addBox').disabled)return;
  if(state.pendingBox){confirmBox();return;}
  state.draw=!state.draw;state.selected=null;renderBoxes();$('viewport').focus();
}
function confirmBox(){
  if(!state.pendingBox)return;
  const id=state.pendingBox;state.pendingBox=null;state.draw=false;state.selected=id;
  markIssue();edited();renderBoxes();focusName(id);
}
$('nameFields').addEventListener('input',e=>{
  const id=e.target.dataset.nameInput;if(!id||!state.current)return;
  const b=state.current.boxes.find(b=>b.id===id);if(!b)return;
  b.name=e.target.value;markIssue();edited();
});
$('nameFields').addEventListener('focusin',e=>{
  if(!e.target.dataset.nameInput)return;state.selected=e.target.dataset.nameInput;state.draw=false;renderBoxes();
});
$('confirmBox').onclick=confirmBox;
document.addEventListener('keydown',e=>{
  if(state.view==='before')return;
  if(e.isComposing||e.keyCode===229||e.altKey||e.ctrlKey||e.metaKey||e.shiftKey||e.repeat)return;
  if($('browseDialog').open||e.target.closest('#holdContext'))return;
  const typing=e.target.closest('input,textarea,select,[contenteditable]:not([contenteditable="false"])');
  if(typing){
    if(nameMode()&&e.key==='Enter'&&e.target.dataset.nameInput){
      e.preventDefault();
      if(!e.target.value.trim()){notify('Enter a name.');return;}
      state.selected=null;renderBoxes();$('viewport').focus();
    }
    return;
  }
  if(!state.loaded||state.busy||state.conflict||!state.current?.available||state.current?.source_condition)return;
  if(nameMode()){
    if(e.key==='Enter'&&state.drag){
      e.preventDefault();finishPointer({pointerId:state.drag.pointer});
      if(state.pendingBox)confirmBox();else if(state.selected)focusName(state.selected);
      return;
    }
    if(state.drag)return;
    if(e.key==='Enter'&&state.pendingBox){e.preventDefault();confirmBox();return;}
    if((e.code==='KeyB'||e.key.toLowerCase()==='b'||e.key==='ㅠ')&&!state.pendingBox){e.preventDefault();startBox();return;}
    if(state.pendingBox||state.draw)return;
    if(e.key==='Enter'){
      e.preventDefault();
      if(state.selected){focusName(state.selected);return;}
      completeNext('issue');return;
    }
    if(state.selected)return;
    if(e.key===' '){e.preventDefault();completeNext('ok');return;}
    if(IS_HOLD&&['ArrowLeft','ArrowRight'].includes(e.key)){e.preventDefault();navigate(e.key==='ArrowLeft'?'previous':'next');return;}
    // Reading a correction page with the other arrows never changes its review.
    if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key))return;
  }
  if((e.key.toLowerCase()==='r'||e.code==='KeyR'||e.key==='ㄱ')&&!state.drag){e.preventDefault();rotateLeft();return;}
  if(nameMode())return;
  const isSpace=e.key===' ';
  if(!isSpace&&!['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key))return;
  if(state.draw||state.drag||state.selected)return;
  e.preventDefault();completeNext(isSpace?'needs_review':'ok');
});
async function refreshStats(){
  const r=await api('/api/stats'),c=r.counts;state.dataset=r.settings.dataset_id;
  const done=c.ok+c.issue,percent=c.total?done/c.total*100:0;
  $('counts').innerHTML=[['','All',c.total],...Object.entries(LABELS).map(([s,l])=>[s,l,c[s]])].map(([s,l,n])=>`<button class="stat" data-status="${s}" aria-label="${l} ${n} items"><i></i><span>${l}</span><strong>${fmt(n)}</strong></button>`).join('');
  $('progressText').textContent=`${percent.toFixed(1)}%`;$('progressFill').style.width=`${percent}%`;
  $('syncInfo').textContent='8 public sample panels · autosaved in this browser';
  $('position').textContent=state.filter||state.query?' · filtered':'';
  return r;
}
$('counts').onclick=e=>{const el=e.target.closest('[data-status]');if(el){state.filter=el.dataset.status;showBrowse();}};
async function listFiles(edge=''){
  const r=await api('/api/images?'+params({q:state.query,status:state.filter,offset:state.offset,limit:60,edge}));state.listTotal=r.total;state.offset=r.offset;
  $('listSummary').textContent=`${fmt(r.total)} matches · ${r.sort==='recent_review'?'recent review edits':'file order'} · previous/next follows file order.`;
  $('fileList').innerHTML=r.items.map(x=>`<button class="file-entry" data-page-id="${escapeHTML(x.page_id)}"><span>${escapeHTML(x.filename)}<small>${escapeHTML(x.page_id)} · Record #${x.generation}${x.source_condition?' · check output':''}${r.sort==='recent_review'&&x.updated_at?' · updated '+escapeHTML(new Date(x.updated_at).toLocaleString('en-US')):''}</small></span><span class="status-badge ${x.status}">${LABELS[x.status]}</span></button>`).join('')||'<p class="empty-boxes">No results found.</p>';
  $('listPage').textContent=`${fmt(Math.min(state.offset+1,r.total))}–${fmt(Math.min(state.offset+60,r.total))} / ${fmt(r.total)}`;
  $('listFirst').disabled=$('listPrev').disabled=state.offset===0;$('listLast').disabled=$('listNext').disabled=state.offset+60>=r.total;
}
async function showBrowse(){state.offset=0;$('search').value=state.query;$('filter').value=state.filter;if(!$('browseDialog').open)$('browseDialog').showModal();try{await listFiles();}catch(ex){notify(ex.message);}}
$('browseButton').onclick=showBrowse;$('closeBrowse').onclick=()=>$('browseDialog').close();
$('search').oninput=()=>{state.query=$('search').value;state.offset=0;clearTimeout(searchTimer);searchTimer=setTimeout(()=>listFiles().catch(showError),200);};
$('filter').onchange=()=>{state.filter=$('filter').value;state.offset=0;listFiles().catch(showError);};
$('listFirst').onclick=()=>listFiles('first').catch(showError);$('listLast').onclick=()=>listFiles('last').catch(showError);
$('listPrev').onclick=()=>{state.offset=Math.max(0,state.offset-60);listFiles().catch(showError);};$('listNext').onclick=()=>{state.offset+=60;listFiles().catch(showError);};
$('fileList').onclick=e=>{const el=e.target.closest('[data-page-id]');if(el)withBusy(async()=>{await flush();await openImage(el.dataset.pageId);$('browseDialog').close();});};
$('browseDialog').addEventListener('close',()=>{if(state.current)api('/api/session',{page_id:state.current.page_id,q:state.query,status:state.filter}).catch(showError);refreshStats().catch(()=>{});});
$('syncButton').onclick=()=>withBusy(async()=>{await flush();if(state.current)await openImage(state.current.page_id);await refreshStats();notify('Saved records in this browser refreshed.');});
async function exportReviews(history=false){await withBusy(async()=>{await flush();const r=await api('/api/export',{history});notify('JSONL download requested: '+r.filename);$('exportButton').title='Last export: '+r.path;});}
$('exportButton').onclick=()=>exportReviews();$('exportHistory').onclick=()=>exportReviews(true);
async function loadHistory(append=false){
  if(!state.current)return;if(!append){state.historyOffset=0;$('historyList').replaceChildren();}
  const r=await api('/api/history?'+params({page_id:state.current.page_id,offset:state.historyOffset}));
  for(const h of r.items){const el=document.createElement('details');const summary=document.createElement('summary');summary.textContent=`${new Date(h.created_at).toLocaleString('en-US')} · ${LABELS[h.snapshot.status]} · Record #${h.snapshot.generation} · ${h.event}`;const pre=document.createElement('pre');pre.textContent=JSON.stringify({filename:h.snapshot.filename,sha256:h.snapshot.sha256,width:h.snapshot.width,height:h.snapshot.height,status:LABELS[h.snapshot.status],issues:h.snapshot.issues.map(x=>TYPES[x]),note:h.snapshot.note,boxes:h.snapshot.boxes},null,2);el.append(summary,pre);$('historyList').append(el);}
  if(!r.total)$('historyList').textContent='No saved change history yet.';
  state.historyOffset+=r.items.length;$('moreHistory').hidden=state.historyOffset>=r.total;
}
$('historyDetails').addEventListener('toggle',()=>{if($('historyDetails').open)loadHistory().catch(showError);});$('moreHistory').onclick=()=>loadHistory(true).catch(showError);
$('downloadDraft').onclick=()=>{const raw=JSON.stringify({...payload(),pending_box:state.pendingBox});const url=URL.createObjectURL(new Blob([raw],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=`draft-${state.current.page_id}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
$('loadServer').onclick=()=>{if(!confirm('Load the latest saved records in this browser instead of the retained draft? Download any draft you need as JSON first.'))return;localStorage.removeItem(draftKey());state.editSeq=state.savedSeq;state.conflict=false;withBusy(()=>openImage(state.current.page_id));};
window.addEventListener('beforeunload',e=>{if(state.drag||state.pendingBox){persistDraft();e.preventDefault();e.returnValue='';}else if(state.editSeq!==state.savedSeq){persistDraft();e.preventDefault();e.returnValue='';}});
document.addEventListener('visibilitychange',()=>{if(document.hidden&&state.current&&state.editSeq!==state.savedSeq){persistDraft();flush().catch(showError);}});
window.addEventListener('online',()=>{if(!state.conflict)flush().catch(showError);});
async function poll(){
  if(polling)return;polling=true;
  try{
    const r=await refreshStats();
    if(!state.current&&r.counts.total){const session=r.settings.session||{};state.query=session.q||'';state.filter=session.status||'';let pid=session.page_id;if(!pid){const first=await api('/api/neighbor?direction=unreviewed');pid=first.page_id|| (await api('/api/images?limit=1')).items[0]?.page_id;}if(pid)await withBusy(()=>openImage(pid));}
    else if(state.current&&!state.busy&&!state.drag&&!state.pendingBox&&!state.saving&&!state.conflict){
      if(state.editSeq!==state.savedSeq){await flush();}
      const latest=await api('/api/image?'+params({page_id:state.current.page_id}));
      if(latest.revision!==state.current.revision||latest.fingerprint!==state.current.fingerprint){
        if(state.editSeq!==state.savedSeq)throw Object.assign(new Error('The output or records in another tab changed. Check your draft.'),{status:409});
        await withBusy(()=>openImage(latest.page_id));notify('Updated image or review records loaded. Earlier records remain in history.');
      }
    }
  }catch(ex){if(state.current&&state.editSeq!==state.savedSeq)showError(ex);else{$('syncInfo').textContent=ex.message;savedLabel('Cannot open storage',true);notify(ex.message);if(!state.current)imageFailure(ex.message);}}finally{polling=false;}
}
controls();poll();setInterval(poll,3000);
