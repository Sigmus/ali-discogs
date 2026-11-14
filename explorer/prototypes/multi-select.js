(() => {
  const defs=[['sp','Spotify match'],['qb','Qobuz match'],['composer','Composer'],['label','Label'],['genre','Genre or style'],['decade','Decade']];
  const titles={found:'Found',probable:'Probable',not_found:'Not found',unchecked:'Unchecked',pending:'Pending'};
  const variants=[['A','Compact checklist','Keep the familiar dropdown shape. Check several options; the field shows a short summary. Changes apply immediately.'],['B','Searchable picker + chips','Search long lists and see each selection underneath. Remove a selection without reopening the menu. Changes apply immediately.'],['C','Filter panel','Make several selections in one panel, then apply them together. Keeps the collection view compact.']];
  let rows=[],values={},active=null,draft=null;
  const states=variants.map(()=>Object.fromEntries(defs.map(([key])=>[key,new Set()])));
  const esc=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const label=(key,v)=>['sp','qb'].includes(key)?titles[v]||v:v;
  function read(row,key){
    if(key==='sp')return [row.spotify?.status||'unchecked'];
    if(key==='qb')return [row._qobuz||'unchecked'];
    if(key==='composer')return row.composers||[];
    if(key==='label')return (row.labels||[]).map(v=>v.name);
    if(key==='genre')return [...(row.genres||[]),...(row.styles||[])];
    return row.year?[`${Math.floor(Number(row.year)/10)*10}s`]:['Undated'];
  }
  const matched=state=>rows.filter(row=>defs.every(([key])=>!state[key].size||read(row,key).some(v=>state[key].has(v))));
  function summary(key,set){const a=[...set].map(v=>label(key,v));return a.length===0?(['sp','qb'].includes(key)?'All statuses':'Any'):a.length===1?a[0]:a.length===2?a.join(', '):`${a.length} selected`;}
  function chips(i,key){return [...states[i][key]].map(v=>`<button class="chip" data-remove="${esc(v)}" data-i="${i}" data-key="${key}" aria-label="Remove ${esc(label(key,v))}">${esc(label(key,v))}<span aria-hidden="true">×</span></button>`).join('');}
  function render(){
    document.querySelector('#options').innerHTML=variants.map(([letter,title,desc],i)=>`<section class="option"><div class="option-head"><span class="letter">OPTION ${letter}</span><h2>${title}</h2><p>${desc}</p>${i===0?'<span class="recommend">My starting recommendation</span>':''}</div><div class="demo"><div class="fields">${defs.map(([key,name])=>`<div class="field"><label id="label-${i}-${key}">${name}</label><button class="trigger" data-open="${key}" data-i="${i}" aria-labelledby="label-${i}-${key} value-${i}-${key}" aria-expanded="false"><span id="value-${i}-${key}">${esc(summary(key,states[i][key]))}</span><span class="chevron" aria-hidden="true"></span></button>${i===1?`<div class="chips">${chips(i,key)}</div>`:''}</div>`).join('')}</div><div class="toolbar">${i===2?'<button data-panel>Open all filters</button>':'<span class="statusline">Apply immediately</span>'}<button data-reset="${i}">Clear</button></div><div class="result" id="result-${i}"></div></div></section>`).join('');
    states.forEach((_,i)=>renderResult(i));
  }
  function renderResult(i){const hits=matched(states[i]);document.querySelector(`#result-${i}`).innerHTML=`<div class="result-count" aria-live="polite">${hits.length} <span class="quiet">releases</span></div><p>Preview of matching albums</p>${hits.slice(0,3).map(r=>`<div class="album-title" title="${esc(r.title)}">${esc(r.title)}</div>`).join('')}${!hits.length?'<p>No matches. Remove a selection to broaden the results.</p>':''}`;}
  function choices(key,state,query=''){
    const items=values[key].filter(([v])=>label(key,v).toLowerCase().includes(query.toLowerCase()));
    return items.map(([v,count])=>`<label class="choice"><input type="checkbox" data-value="${esc(v)}" data-key="${key}" ${state[key].has(v)?'checked':''}><span class="choice-name">${esc(label(key,v))}</span><span class="count">${count}</span></label>`).join('')||'<div class="no-options">No options match your search.</div>';
  }
  function close(){document.querySelectorAll('.popover').forEach(p=>p.remove());document.querySelectorAll('[data-open]').forEach(b=>b.setAttribute('aria-expanded','false'));active=null;}
  function open(i,key,button){
    if(i===2){openPanel(key);return;}
    if(active?.i===i&&active.key===key){close();return;}
    close();active={i,key};button.setAttribute('aria-expanded','true');
    const panel=document.createElement('div');panel.className='popover'+(i===1?' searchable':'');
    panel.innerHTML=`${i===1?`<input type="search" class="picker-search" placeholder="Search ${esc(defs.find(d=>d[0]===key)[1].toLowerCase())}" aria-label="Search options">`:''}<div class="choices">${choices(key,states[i])}</div><div class="popover-foot"><span class="selection-count">${states[i][key].size} selected</span><button class="text-button" data-clear-picker>Clear selection</button></div>`;
    button.after(panel);panel.querySelector('input')?.focus();
    if(panel.getBoundingClientRect().right>innerWidth-12){panel.style.left='auto';panel.style.right='0';}
  }
  function updateField(i,key){const button=document.querySelector(`[data-i="${i}"][data-open="${key}"]`);button.querySelector('span:first-child').textContent=summary(key,states[i][key]);if(i===1)button.parentElement.querySelector('.chips').innerHTML=chips(i,key);renderResult(i);}
  function openPanel(focusKey){
    close();draft=Object.fromEntries(defs.map(([k])=>[k,new Set(states[2][k])]));
    document.querySelector('#drawer-root').innerHTML=`<div class="drawer-backdrop"><section class="drawer" role="dialog" aria-modal="true" aria-labelledby="drawer-title"><div class="drawer-head"><h2 id="drawer-title">Filter collection</h2><button class="text-button" data-cancel aria-label="Close filters">✕</button></div><div class="drawer-body">${defs.map(([key,name])=>`<details ${key===focusKey||key==='sp'?'open':''}><summary>${name}<span class="badge" id="badge-${key}">${draft[key].size||''}</span></summary>${['composer','label','genre'].includes(key)?`<input class="picker-search" type="search" placeholder="Search ${name.toLowerCase()}" aria-label="Search ${name}" data-panel-search="${key}">`:''}<div class="choices" data-panel-choices="${key}">${choices(key,draft)}</div></details>`).join('')}</div><div class="drawer-footer"><button class="text-button" data-reset-draft>Clear all</button><button class="apply" data-apply>Show ${matched(draft).length} releases</button></div></section></div>`;
    document.querySelector('[data-cancel]').focus();
  }
  function closePanel(){document.querySelector('#drawer-root').innerHTML='';draft=null;document.querySelector('[data-panel]').focus();}
  document.addEventListener('click',e=>{
    const button=e.target.closest('button');
    if(button?.hasAttribute('data-open'))return open(Number(button.dataset.i),button.dataset.open,button);
    if(button?.hasAttribute('data-panel'))return openPanel('sp');
    if(button?.hasAttribute('data-reset')){close();const i=Number(button.dataset.reset);defs.forEach(([k])=>states[i][k].clear());render();return;}
    if(button?.hasAttribute('data-remove')){states[+button.dataset.i][button.dataset.key].delete(button.dataset.remove);updateField(+button.dataset.i,button.dataset.key);close();return;}
    if(button?.hasAttribute('data-clear-picker')&&active){const {i,key}=active;states[i][key].clear();updateField(i,key);button.closest('.popover').querySelectorAll('input[type=checkbox]').forEach(c=>c.checked=false);button.closest('.popover').querySelector('.selection-count').textContent='0 selected';return;}
    if(button?.hasAttribute('data-cancel')||e.target.classList.contains('drawer-backdrop'))return closePanel();
    if(button?.hasAttribute('data-apply')){states[2]=draft;closePanel();render();return;}
    if(button?.hasAttribute('data-reset-draft')){defs.forEach(([k])=>draft[k].clear());document.querySelectorAll('.drawer input[type=checkbox]').forEach(c=>c.checked=false);document.querySelectorAll('.badge').forEach(b=>b.textContent='');document.querySelector('[data-apply]').textContent=`Show ${matched(draft).length} releases`;return;}
    if(!e.target.closest('.popover'))close();
  });
  document.addEventListener('change',e=>{if(!e.target.matches('[data-value]'))return;const {key,value}=e.target.dataset;const state=draft||states[active.i];e.target.checked?state[key].add(value):state[key].delete(value);if(draft){document.querySelector(`#badge-${key}`).textContent=state[key].size||'';document.querySelector('[data-apply]').textContent=`Show ${matched(draft).length} releases`;}else{updateField(active.i,key);e.target.closest('.popover').querySelector('.selection-count').textContent=`${state[key].size} selected`;}});
  document.addEventListener('input',e=>{if(e.target.matches('[data-panel-search]')){const key=e.target.dataset.panelSearch;document.querySelector(`[data-panel-choices="${key}"]`).innerHTML=choices(key,draft,e.target.value);}else if(e.target.matches('.popover .picker-search'))e.target.closest('.popover').querySelector('.choices').innerHTML=choices(active.key,states[active.i],e.target.value);});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'){if(draft)closePanel();else{const b=active&&document.querySelector(`[data-i="${active.i}"][data-open="${active.key}"]`);close();b?.focus();}}if(e.key==='Tab'&&draft){const nodes=[...document.querySelectorAll('.drawer button,.drawer input,.drawer summary')].filter(n=>n.getClientRects().length);const first=nodes[0],last=nodes.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}}});
  document.querySelector('#theme-prototype').onclick=()=>document.documentElement.dataset.theme=document.documentElement.dataset.theme==='dark'?'light':'dark';
  Promise.all([fetch('../data/collection_matches.json').then(r=>r.json()),fetch('../data/qobuz_matches.json').then(r=>r.json())]).then(([collection,qobuz])=>{
    rows=collection.map(r=>({...r,_qobuz:qobuz.releases[String(r.discogs_id)]?.status||'unchecked'}));
    defs.forEach(([key])=>{const counts=new Map();rows.forEach(r=>new Set(read(r,key)).forEach(v=>counts.set(v,(counts.get(v)||0)+1)));values[key]=[...counts].sort((a,b)=>b[1]-a[1]||String(a[0]).localeCompare(String(b[0])));});render();document.querySelector('#loading').textContent=`${rows.length} collection copies loaded · Counts use the whole collection · Each option has independent selections`;
  }).catch(()=>document.querySelector('#loading').textContent='Could not load collection. Serve this page with make serve.');
})();
