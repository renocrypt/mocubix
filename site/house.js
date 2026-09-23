/* Palette switch. Loaded in <head> so a stored choice lands before first paint. */
(function(){
  var KEY = 'mocubix-theme', root = document.documentElement, btn = null;

  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) {}
  if (stored === 'day') root.setAttribute('data-theme', 'day');

  function isDay(){ return root.getAttribute('data-theme') === 'day'; }

  function label(){
    if (!btn) return;
    var day = isDay();
    btn.setAttribute('aria-pressed', day);
    btn.setAttribute('aria-label', day ? 'Switch to the night palette' : 'Switch to the day palette');
    btn.lastChild.textContent = day ? 'Day' : 'Night';
  }

  function set(day){
    if (day) root.setAttribute('data-theme', 'day'); else root.removeAttribute('data-theme');
    try { localStorage.setItem(KEY, day ? 'day' : 'night'); } catch (e) {}
    label();
    dispatchEvent(new CustomEvent('themechange', { detail: { theme: day ? 'day' : 'night' } }));
  }

  function toggle(){
    var day = !isDay();
    var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (document.startViewTransition && !still) document.startViewTransition(function(){ set(day); });
    else set(day);
  }

  /* Commons throttles thumbnail requests under load; a few patient retries catch nearly all of it. */
  addEventListener('error', function(e){
    var t = e.target;
    if (!t || t.tagName !== 'IMG') return;
    var n = +(t.dataset.retried || 0);
    if (n >= 3) return;
    t.dataset.retried = n + 1;
    setTimeout(function(){ var u = t.currentSrc || t.src; t.removeAttribute('srcset'); t.src = u.split('?')[0] + '?r=' + Date.now(); }, [2000, 5000, 10000][n]);
  }, true);

  /* The mark of the link to a page's source: an open tag, drawn here once for every page. */
  var TAG = '<svg viewBox="0 0 15 11" aria-hidden="true"><path d="M4.5 1.5 1 5.5l3.5 4"/>'
    + '<path d="M9.25.75 5.75 10.25" pathLength="1"/><path d="M10.5 1.5 14 5.5l-3.5 4"/></svg>';

  addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('a.source').forEach(function(a){ a.insertAdjacentHTML('afterbegin', TAG); });
    btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'theme';
    btn.appendChild(document.createElement('i')).setAttribute('aria-hidden', 'true');
    btn.appendChild(document.createElement('span'));
    var slot = document.querySelector('[data-theme-slot]');
    if (slot) { slot.appendChild(btn); btn.setAttribute('data-inline', ''); }
    else document.body.appendChild(btn);
    label();
    btn.addEventListener('click', toggle);
  });
})();
