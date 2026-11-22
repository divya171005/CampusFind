const $ = id => document.getElementById(id);
const modal = $('modal');

function openModal(){modal.classList.add('open');}
function closeModal(){modal.classList.remove('open');}
['open-form','hero-report','browse-report'].forEach(id => $(id).addEventListener('click', openModal));
$('close-modal').addEventListener('click', closeModal);
modal.addEventListener('click', e => {if(e.target === modal) closeModal();});

function escapeHTML(value='') {
  return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

async function loadItems(){
  const params = new URLSearchParams();
  if($('search').value.trim()) params.set('q',$('search').value.trim());
  if($('type-filter').value) params.set('item_type',$('type-filter').value);
  if($('category-filter').value) params.set('category',$('category-filter').value);
  params.set('status','Open');
  const grid = $('items-grid');
  try{
    const response = await fetch('/api/items?'+params.toString());
    const data = await response.json();
    $('open-count').textContent = data.items.length;
    if(!data.items.length){grid.innerHTML='<div class="empty">No matching listings yet. Be the first to report an item!</div>';return;}
    grid.innerHTML = data.items.map(item => `
      <article class="item-card">
        <div class="item-top"><span class="type-pill ${item.item_type.toLowerCase()}">${escapeHTML(item.item_type)}</span><span class="category">${escapeHTML(item.category)}</span></div>
        <h3>${escapeHTML(item.title)}</h3><p>${escapeHTML(item.description)}</p>
        <div class="item-meta"><span>⌖ ${escapeHTML(item.location)}</span><span>◷ ${escapeHTML(item.date_seen)}</span></div>
        <div class="item-footer"><a class="contact" href="mailto:${encodeURIComponent(item.contact_email)}?subject=${encodeURIComponent('CampusFind: '+item.title)}">Contact ${escapeHTML(item.contact_name)} ↗</a><button class="resolve" data-id="${escapeHTML(item.id)}">Mark resolved</button></div>
      </article>`).join('');
    document.querySelectorAll('.resolve').forEach(btn => btn.addEventListener('click', () => resolveItem(btn.dataset.id)));
  }catch(e){grid.innerHTML='<div class="empty">Could not load listings. Please refresh the page.</div>';}
}

async function resolveItem(id){
  if(!confirm('Mark this listing as resolved?')) return;
  const response = await fetch(`/api/items/${encodeURIComponent(id)}/resolve`,{method:'PATCH'});
  if(response.ok) loadItems(); else alert('Could not update this listing.');
}

$('item-form').addEventListener('submit', async e => {
  e.preventDefault();
  const button = e.target.querySelector('button[type=submit]');
  button.disabled = true; button.textContent = 'Publishing...';
  const body = Object.fromEntries(new FormData(e.target).entries());
  try{
    const response = await fetch('/api/items',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    const data = await response.json();
    if(!response.ok) throw new Error(data.detail || 'Unable to publish listing');
    $('form-message').textContent = 'Your listing has been published!';
    e.target.reset();
    setTimeout(()=>{closeModal();$('form-message').textContent='';loadItems();},900);
  }catch(err){$('form-message').textContent = err.message;}
  finally{button.disabled=false;button.textContent='Publish listing ↗';}
});
let searchTimer;
$('search').addEventListener('input',()=>{clearTimeout(searchTimer);searchTimer=setTimeout(loadItems,250);});
$('type-filter').addEventListener('change',loadItems);
$('category-filter').addEventListener('change',loadItems);
loadItems();
