/* The Lexicon's demos. Every term page loads this one file after material.js;
   each block finds its own demo and returns at once when it is not on the page. */
var P = SEKKA;
function bg(el, work){ el.style.backgroundImage = 'url("' + work.src + '")'; }

/* ── 02 view progress timeline ─────────────────────────────── */
(function(){
  var host = document.getElementById('plates');
  if (!host) return;
  P.slice(0, 5).forEach(function(w, i){
    var row = document.createElement('div');
    row.className = 'plate';
    row.innerHTML =
      '<figure><img loading="lazy" decoding="async" alt="' + w.label + '" src="' + w.src +
      '" srcset="' + w.srcset + '" sizes="76px"></figure>' +
      '<div><span class="cap">' + String(i + 1).padStart(2, '0') + ' · ' + w.label +
      '</span><div class="bar"><i></i></div></div>';
    host.appendChild(row);
  });
})();

/* ── 03 pin + scrub ────────────────────────────────────────── */
(function(){
  var img = document.getElementById('pinImg'), cover = document.getElementById('pinCover');
  if (!img) return;
  var w = P[1];
  img.src = w.src; img.srcset = w.srcset;
  img.sizes = '(max-width:880px) 76vw, 540px';
  img.alt = 'Kamisaka Sekka — ' + w.label;
  var run = document.querySelector('.pinrun');
  function frame(){
    var r = run.getBoundingClientRect();
    var total = r.height - innerHeight;
    var p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0;
    cover.style.transform = 'scaleX(' + (1 - p) + ')';
  }
  addEventListener('scroll', frame, { passive: true });
  addEventListener('resize', frame, { passive: true });
  frame();
})();

/* ── 04 parallax ───────────────────────────────────────────── */
(function(){
  var a = document.getElementById('paraL1'), b = document.getElementById('paraL2');
  if (!a) return;
  bg(a, P[4]); bg(b, P[2]);
})();

/* ── 05 horizontal track ───────────────────────────────────── */
(function(){
  var track = document.getElementById('htrack');
  if (!track) return;
  P.slice(0, 8).forEach(function(w, i){
    var c = document.createElement('div');
    c.className = 'hcard';
    c.innerHTML = '<figure><img loading="lazy" decoding="async" alt="' + w.label +
      '" src="' + w.src + '" sizes="310px"></figure><p>' +
      String(i + 1).padStart(2, '0') + ' · ' + w.label + '</p>';
    track.appendChild(c);
  });
  var run = document.querySelector('.hrun');
  function frame(){
    var r = run.getBoundingClientRect();
    var total = r.height - innerHeight;
    var p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0;
    var travel = Math.max(0, track.scrollWidth - innerWidth + 44);
    track.style.transform = 'translateX(' + (-p * travel) + 'px)';
  }
  addEventListener('scroll', frame, { passive: true });
  addEventListener('resize', frame, { passive: true });
  frame();
})();

/* ── 07 stacking cards ─────────────────────────────────────── */
(function(){
  var host = document.getElementById('stackrun');
  if (!host) return;
  P.slice(0, 5).forEach(function(w, i){
    var li = document.createElement('li');
    li.innerHTML = '<div class="stackcard"><figure><img loading="lazy" decoding="async" alt="' +
      w.label + '" src="' + w.src + '" sizes="52px"></figure>' +
      '<div><h4>' + w.label + '</h4><p>card ' + String(i + 1).padStart(2, '0') +
      ' · sticks at 72px</p></div></div>';
    host.appendChild(li);
  });
})();

/* ── 08 velocity bars ──────────────────────────────────────── */
(function(){
  var host = document.getElementById('skewinner');
  if (!host) return;
  [92, 64, 78, 46, 86, 58, 72, 40, 88].forEach(function(v){
    var i = document.createElement('i');
    i.style.width = v + '%';
    host.appendChild(i);
  });
})();

/* ── 01 + 08 · one rAF loop for position and velocity ──────── */
(function(){
  var root = document.documentElement;
  var pctOut = document.getElementById('pctOut'), velOut = document.getElementById('velOut');
  if (!pctOut && !velOut && !document.getElementById('skewinner')) return;   /* only the dial and the skew need it */
  var last = scrollY, v = 0, queued = false;
  /* Asymmetric filter: fast attack, slow release. A symmetric smooth either
     lags the gesture or passes trackpad jitter through as visual noise. */
  var ATTACK = 0.34, RELEASE = 0.055, SCALE = 80;
  function frame(){
    queued = false;
    var max = root.scrollHeight - innerHeight;
    if (pctOut) pctOut.textContent = Math.round((max > 0 ? scrollY / max : 0) * 100) + '%';
    var target = Math.min(1, Math.abs(scrollY - last) / SCALE);
    last = scrollY;
    v += (target - v) * (target > v ? ATTACK : RELEASE);
    if (v < 0.0008) v = 0;
    root.style.setProperty('--vel', v.toFixed(4));
    if (velOut) velOut.textContent = v.toFixed(2);
    if (v > 0 && !queued) { queued = true; requestAnimationFrame(frame); }
  }
  addEventListener('scroll', function(){
    if (!queued) { queued = true; requestAnimationFrame(frame); }
  }, { passive: true });
  frame();
})();

/* ── 09 blur-up ────────────────────────────────────────────── */
(function(){
  var host = document.getElementById('lqip'), btn = document.getElementById('lqipBtn');
  if (!host) return;
  var w = P[5];
  host.innerHTML = '<div class="ph"></div><div class="full"></div>';
  var ph = host.querySelector('.ph'), full = host.querySelector('.full');
  /* The placeholder is the smallest bucket, deliberately upscaled and blurred. */
  ph.style.backgroundImage = 'url("' + w.src + '")';
  function load(){
    host.classList.remove('done');
    var img = new Image();
    img.onload = function(){
      full.style.backgroundImage = 'url("' + img.src + '")';
      requestAnimationFrame(function(){ host.classList.add('done'); });
    };
    img.src = w.srcset.split(', ').pop().split(' ')[0] + '?r=' + Date.now();
  }
  btn.addEventListener('click', load);
  load();
})();

/* ── 10 ken burns ──────────────────────────────────────────── */
(function(){ var el = document.getElementById('kb'); if (el) bg(el, P[6]); })();

/* ── 11 duotone ────────────────────────────────────────────── */
(function(){
  var host = document.getElementById('duo'), rng = document.getElementById('duoRange');
  if (!host) return;
  var w = P[7];
  bg(host.querySelector('.duoBase'), w);
  rng.addEventListener('input', function(){
    host.style.setProperty('--duo', rng.value / 100);
  });
})();

/* ── 12 progressive blur ───────────────────────────────────── */
(function(){
  var el = document.querySelector('#pblur .pbImg');
  if (el) bg(el, P[8]);
})();

/* ── 13 ordered dithering ──────────────────────────────────── */
(function(){
  var cv = document.getElementById('dithCv'), rng = document.getElementById('dithRange');
  if (!cv) return;
  var ctx = cv.getContext('2d', { willReadFrequently: true });
  var work = ATKINS.length ? ATKINS[1] : P[9];
  /* 8x8 Bayer matrix: a fixed threshold pattern, so the grain is structured.
     Needs crossorigin="anonymous" and a CORS-clean host, or the canvas taints. */
  var B = [
    [ 0,32, 8,40, 2,34,10,42],[48,16,56,24,50,18,58,26],
    [12,44, 4,36,14,46, 6,38],[60,28,52,20,62,30,54,22],
    [ 3,35,11,43, 1,33, 9,41],[51,19,59,27,49,17,57,25],
    [15,47, 7,39,13,45, 5,37],[63,31,55,23,61,29,53,21]];
  var img = new Image();
  img.crossOrigin = 'anonymous';
  var ready = false;
  img.onload = function(){ ready = true; draw(); };
  img.onerror = function(){
    cv.width = 8; cv.height = 5;
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--lift');
    ctx.fillRect(0, 0, 8, 5);
  };
  img.src = work.src;

  function draw(){
    if (!ready) return;
    var W = 380, H = Math.round(W * img.naturalHeight / img.naturalWidth);
    cv.width = W; cv.height = H;
    ctx.drawImage(img, 0, 0, W, H);
    var d = ctx.getImageData(0, 0, W, H), px = d.data;
    var levels = parseInt(rng.value, 10), step = 255 / (levels - 1);
    for (var y = 0; y < H; y++){
      for (var x = 0; x < W; x++){
        var i = (y * W + x) * 4;
        var lum = 0.299 * px[i] + 0.587 * px[i+1] + 0.114 * px[i+2];
        var t = (B[y & 7][x & 7] / 64 - 0.5) * step;
        var q = Math.max(0, Math.min(255, Math.round((lum + t) / step) * step));
        /* tint the result into the house palette rather than flat grey */
        px[i]   = q * 0.94 + 10;
        px[i+1] = q * 0.90 + 9;
        px[i+2] = q * 0.84 + 8;
      }
    }
    ctx.putImageData(d, 0, 0);
  }
  rng.addEventListener('input', draw);
})();

/* ── 14 clip-path reveal ───────────────────────────────────── */
(function(){
  var host = document.getElementById('clipr');
  if (!host) return;
  var imgs = host.querySelectorAll('.clipImg');
  bg(imgs[0], P[10]); bg(imgs[1], P[3]);
})();

/* ── 15 comparison slider ──────────────────────────────────── */
(function(){
  var host = document.getElementById('cmp');
  if (!host) return;
  bg(host.querySelector('.cmpA'), P[9]);
  bg(host.querySelector('.cmpB'), P[0]);
  function set(e){
    var r = host.getBoundingClientRect();
    var cx = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
    host.style.setProperty('--x', Math.max(0, Math.min(r.width, cx)) + 'px');
  }
  host.addEventListener('pointermove', set);
  host.addEventListener('pointerdown', set);
})();

/* ── 16 split reveal, fires once ───────────────────────────── */
(function(){
  var el = document.getElementById('reveal');
  if (!el) return;
  new IntersectionObserver(function(entries, obs){
    entries.forEach(function(e){
      if (e.isIntersecting) { el.classList.add('on'); obs.disconnect(); }
    });
  }, { threshold: 0.4 }).observe(el);
})();

/* ── 17 variable font ──────────────────────────────────────── */
(function(){
  var line = document.getElementById('vfLine'), rng = document.getElementById('vfRange');
  if (!line) return;
  function apply(){
    line.style.setProperty('--w', rng.value);
    line.parentElement.style.setProperty('--w', rng.value);
  }
  rng.addEventListener('input', apply); apply();
})();

/* ── 18 text mask ──────────────────────────────────────────── */
(function(){
  var el = document.getElementById('tmaskTxt');
  if (el) el.style.backgroundImage = 'url("' + P[2].src + '")';
})();

/* ── marquee ───────────────────────────────────────────────── */
(function(){
  var row = document.getElementById('marqrow');
  if (!row) return;
  var words = ['Scrub','Pin','Parallax','Snap','Stack','Skew','Stuck','Snapped',
               'Curtain','Kinetic','Dither','Duotone','Blur-up'];
  /* Duplicate exactly once and travel -50%: that is what makes the loop seamless. */
  words.concat(words).forEach(function(w){
    var s = document.createElement('span');
    s.textContent = w;
    row.appendChild(s);
  });
})();

/* ═══ scroll family · specimens 09–24 ════════════════════════ */

function imgTag(w, sizes){
  return '<img loading="lazy" decoding="async" alt="' + w.label + '" src="' + w.src +
         '" srcset="' + w.srcset + '" sizes="' + sizes + '">';
}
function indexRow(w, i, cls){
  var d = document.createElement('div');
  d.className = cls || 'ssqrow';
  d.innerHTML = '<figure>' + imgTag(w, '44px') + '</figure><span>' +
    String(i + 1).padStart(2, '0') + ' · ' + w.label + '</span>';
  return d;
}

/* ── 09 sticky state query ─────────────────────────────────── */
(function(){
  var host = document.getElementById('ssqbody');
  if (!host) return;
  P.forEach(function(w, i){ host.appendChild(indexRow(w, i)); });
})();

/* ── 10 snapped state query ────────────────────────────────── */
(function(){
  var host = document.getElementById('snapq');
  if (!host) return;
  ['One','Two','Three','Four'].forEach(function(n){
    var li = document.createElement('li');
    li.innerHTML = '<div class="qcard"><b>Slide ' + n + '</b><i>snapped</i></div>';
    host.appendChild(li);
  });
})();

/* ── 11 scroll markers ─────────────────────────────────────── */
(function(){
  var host = document.getElementById('cml');
  if (!host) return;
  P.slice(0, 6).forEach(function(w, i){
    var li = document.createElement('li');
    li.innerHTML = '<figure>' + imgTag(w, '186px') + '</figure><p>' +
      String(i + 1).padStart(2, '0') + ' · ' + w.label + '</p>';
    host.appendChild(li);
  });
})();

/* ── 12 scroll buttons ─────────────────────────────────────── */
(function(){
  var host = document.getElementById('csb');
  if (!host) return;
  P.slice(0, 8).forEach(function(w){
    var li = document.createElement('li');
    li.innerHTML = '<figure>' + imgTag(w, '148px') + '</figure>';
    host.appendChild(li);
  });
})();

/* ── 13 timeline scope ─────────────────────────────────────── */
(function(){
  var box = document.getElementById('tscbox');
  if (box) box.innerHTML = imgTag(P[3], '(max-width:880px) 78vw, 420px');
})();

/* ── 15 word scrub ─────────────────────────────────────────── */
(function(){
  var host = document.getElementById('wscrub');
  if (!host) return;
  var text = 'Scroll is the one gesture every reader already knows, ' +
             'which is exactly why it is worth spending a whole vocabulary on.';
  var p = document.createElement('p');
  var words = text.split(' ');
  /* Each word takes a different slice of one view timeline. START holds the
     first word until the line is on screen; SPREAD is how much of the pass the
     sentence occupies; WINDOW is the overlap — narrower strobes, wider arrives
     all at once. */
  var START = 12, SPREAD = 56, WINDOW = 22;
  words.forEach(function(word, i){
    var s = document.createElement('span');
    s.className = 'w';
    s.textContent = word;
    var a = START + (words.length > 1 ? i * SPREAD / (words.length - 1) : 0);
    s.style.animationRange = 'cover ' + a.toFixed(1) + '% cover ' + (a + WINDOW).toFixed(1) + '%';
    p.appendChild(s);
    p.appendChild(document.createTextNode(' '));
  });
  host.appendChild(p);
})();

/* ── 16 direction state ────────────────────────────────────── */
(function(){
  var pane = document.getElementById('dirs'), out = document.getElementById('dirOut'),
      body = document.getElementById('dirsbody');
  if (!pane) return;
  P.concat(P).forEach(function(w, i){ body.appendChild(indexRow(w, i)); });
  /* A dead zone is mandatory. Without it a trackpad flips the state every frame. */
  var DEAD = 6, last = 0;
  pane.dataset.dir = 'up';
  pane.addEventListener('scroll', function(){
    var y = pane.scrollTop, d = y - last;
    if (Math.abs(d) < DEAD) return;
    last = y;
    var dir = (d > 0 && y > 40) ? 'down' : 'up';
    if (pane.dataset.dir !== dir){ pane.dataset.dir = dir; out.textContent = dir; }
  }, { passive: true });
})();

/* ── 17 curtain overlap ────────────────────────────────────── */
(function(){ var el = document.getElementById('curtA'); if (el) bg(el, P[10]); })();

/* ── 18 depth of field ─────────────────────────────────────── */
(function(){
  var host = document.getElementById('dof');
  if (!host) return;
  P.slice(0, 7).forEach(function(w, i){
    var row = document.createElement('div');
    row.className = 'dofrow';
    row.innerHTML = '<div class="dofinner"><figure>' + imgTag(w, '64px') +
      '</figure><span>' + String(i + 1).padStart(2, '0') + ' · ' + w.label + '</span></div>';
    host.appendChild(row);
  });
})();

/* ── 19 infinite loop scroll ───────────────────────────────── */
(function(){
  var pane = document.getElementById('loopx');
  if (!pane) return;
  /* Chrome's scroll anchoring would also try to correct for the moved row,
     and the two corrections fight. Turn it off and do it by hand. */
  pane.style.overflowAnchor = 'none';
  function row(w, i){
    var d = document.createElement('div');
    d.className = 'lrow';
    d.innerHTML = '<figure>' + imgTag(w, '50px') + '</figure><b>' + w.label +
      '</b><em>' + String((i % P.length) + 1).padStart(2, '0') + '</em>';
    return d;
  }
  for (var i = 0; i < P.length * 2; i++) pane.appendChild(row(P[i % P.length], i));
  var busy = false;
  pane.addEventListener('scroll', function(){
    if (busy) return;
    busy = true;
    var first = pane.firstElementChild, last = pane.lastElementChild;
    var edge = first.offsetHeight * 1.5;
    if (pane.scrollTop < edge){
      var lh = last.offsetHeight;
      pane.insertBefore(last, first);
      pane.scrollTop += lh;                    /* same frame, or the seam shows */
    } else if (pane.scrollHeight - pane.scrollTop - pane.clientHeight < edge){
      var fh = first.offsetHeight;
      pane.appendChild(first);
      pane.scrollTop -= fh;
    }
    busy = false;
  }, { passive: true });
  pane.scrollTop = pane.scrollHeight / 3;
})();

/* ── 20 kinetic drag ───────────────────────────────────────── */
(function(){
  var pane = document.getElementById('kin'), track = document.getElementById('kintrack');
  if (!pane) return;
  P.slice(0, 9).forEach(function(w, i){
    var c = document.createElement('div');
    c.className = 'kincard';
    c.innerHTML = '<figure>' + imgTag(w, '172px') + '</figure><p>' +
      String(i + 1).padStart(2, '0') + ' · ' + w.label + '</p>';
    track.appendChild(c);
  });
  var x = 0, v = 0, dragging = false, lastX = 0, raf = 0, min = 0;
  function bounds(){ min = Math.min(0, pane.clientWidth - track.scrollWidth - 32); }
  function apply(){ track.style.transform = 'translateX(' + x.toFixed(2) + 'px)'; }
  function glide(){
    /* 0.94 per frame. 0.90 stops dead and feels cheap; 0.98 never settles. */
    v *= 0.94; x += v;
    if (x > 0){ x = 0; v = 0; }
    if (x < min){ x = min; v = 0; }
    apply();
    raf = Math.abs(v) > 0.1 ? requestAnimationFrame(glide) : 0;
  }
  pane.addEventListener('pointerdown', function(e){
    bounds(); dragging = true; v = 0; lastX = e.clientX;
    pane.classList.add('drag'); pane.setPointerCapture(e.pointerId);
    if (raf){ cancelAnimationFrame(raf); raf = 0; }
  });
  pane.addEventListener('pointermove', function(e){
    if (!dragging) return;
    var d = e.clientX - lastX; lastX = e.clientX;
    v = d;
    x = Math.max(min - 60, Math.min(60, x + d));   /* a little give at each end */
    apply();
  });
  function release(){
    if (!dragging) return;
    dragging = false; pane.classList.remove('drag');
    if (!raf) raf = requestAnimationFrame(glide);
  }
  pane.addEventListener('pointerup', release);
  pane.addEventListener('pointercancel', release);
  addEventListener('resize', bounds, { passive: true });
  bounds(); apply();
})();

/* ── 21 scroll-triggered count ─────────────────────────────── */
(function(){
  var host = document.getElementById('cnt'), btn = document.getElementById('cntBtn');
  if (!host) return;
  var STATS = [
    { to: 12,    suf: '',   cap: 'Sekka plates<br>Momoyogusa, 1909' },
    { to: 10430, suf: 'px', cap: 'widest native scan<br>Rijksmuseum CC0' },
    { to: 1843,  suf: '',   cap: 'Atkins cyanotypes<br>first photographic book' }
  ];
  STATS.forEach(function(s){
    var d = document.createElement('div');
    d.className = 'cntcell';
    d.innerHTML = '<b data-to="' + s.to + '" data-suf="' + s.suf + '">0</b><span>' + s.cap + '</span>';
    host.appendChild(d);
  });
  var cells = host.querySelectorAll('b');
  function run(){
    cells.forEach(function(el){
      var to = +el.dataset.to, t0 = performance.now(), D = 1150;
      (function step(t){
        var p = Math.min(1, (t - t0) / D);
        var e = 1 - Math.pow(1 - p, 3);                    /* ease-out cubic */
        el.textContent = Math.round(to * e).toLocaleString() + el.dataset.suf;
        if (p < 1) requestAnimationFrame(step);
      })(t0);
    });
  }
  /* Fires once. A counter that replays on every pass is a tell that nobody looked twice. */
  new IntersectionObserver(function(entries, obs){
    entries.forEach(function(e){ if (e.isIntersecting){ run(); obs.disconnect(); } });
  }, { threshold: 0.6 }).observe(host);
  btn.addEventListener('click', run);
})();

/* ── 22 scrollspy ──────────────────────────────────────────── */
(function(){
  var pane = document.getElementById('spy'), rail = document.getElementById('spyrail'),
      body = document.getElementById('spybody');
  if (!pane) return;
  var SECS = [
    ['Ground',  'The darkest surface on the page. Everything else is measured against it, which is why it is chosen first and changed last.'],
    ['Ink',     'Three weights of text, not five. Every additional grey is a decision the reader has to make on your behalf.'],
    ['Accent',  'Terra, held under half a percent of painted area. An accent stops being an accent the moment it gets comfortable.'],
    ['Curve',   'One authored easing curve, used everywhere. Fast departure, long quiet arrival — the one thing every motion on these pages has in common.']
  ];
  SECS.forEach(function(s, i){
    var a = document.createElement('a');
    a.href = '#'; a.textContent = String(i + 1).padStart(2, '0') + ' ' + s[0];
    a.addEventListener('click', function(e){
      e.preventDefault();
      var sec = body.children[i];
      pane.scrollTo({ top: sec.offsetTop - body.offsetTop, behavior: 'smooth' });
    });
    rail.appendChild(a);
    var sec = document.createElement('div');
    sec.className = 'spysec';
    sec.innerHTML = '<h5>' + s[0] + '</h5><p>' + s[1] + '</p>';
    body.appendChild(sec);
  });
  var links = rail.querySelectorAll('a');
  links[0].classList.add('on');
  /* The margin collapses the scrollport to a thin band across its middle, so
     "current" means what is at eye level, not what is merely on screen. */
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if (!e.isIntersecting) return;
      var i = [].indexOf.call(body.children, e.target);
      links.forEach(function(l, j){ l.classList.toggle('on', j === i); });
    });
  }, { root: pane, rootMargin: '-45% 0px -45% 0px' });
  [].forEach.call(body.children, function(sec){ io.observe(sec); });
})();

/* ── 23 overscroll containment ─────────────────────────────── */
(function(){
  var a = document.getElementById('osbA'), b = document.getElementById('osbB');
  if (!a) return;
  var LINES = ['Scroll this panel to the bottom.', 'Then keep going.',
               'Watch the page behind it.', 'The left panel hands the gesture on —',
               'the page lurches.', 'The right panel absorbs it.',
               'overscroll-behavior: contain', 'It is the same property that stops',
               'a modal from scrolling the page behind it.', '— end —'];
  [a, b].forEach(function(pane){
    LINES.forEach(function(t){
      var p = document.createElement('p'); p.textContent = t; pane.appendChild(p);
    });
  });
})();


/* ── 38 scoped rotation ────────────────────────────────────── */
(function(){
  var host = document.getElementById('scgrid'), btn = document.getElementById('scBtn');
  var ms = document.getElementById('scMs'), nOut = document.getElementById('scN');
  if (!host) return;
  var big = false;   /* ships cheap; the expensive state is opt-in */
  function fill(n){
    host.innerHTML = '';
    var frag = document.createDocumentFragment();
    for (var i = 0; i < n; i++) frag.appendChild(document.createElement('i'));
    host.appendChild(frag);
    host.parentNode.style.setProperty('--cols', n > 100 ? 40 : 6);
    nOut.textContent = n;
  }
  btn.addEventListener('click', function(){
    big = !big; fill(big ? 960 : 24);
    btn.textContent = big ? '960 consumers' : '24 consumers';
  });
  fill(24);

  /* Frame cost while this stage is on screen — the subtree is the variable. */
  var last = performance.now(), acc = [], live = false;
  new IntersectionObserver(function(es){ live = es[0].isIntersecting; },
    { threshold: 0.2 }).observe(host);
  (function tick(t){
    if (live){
      var d = t - last;
      if (d < 200){ acc.push(d); if (acc.length > 45) acc.shift(); }
      if (acc.length > 8){
        var sorted = acc.slice().sort(function(a, b){ return a - b; });
        ms.textContent = sorted[sorted.length >> 1].toFixed(1) + 'ms';
      }
    }
    last = t;
    requestAnimationFrame(tick);
  })(performance.now());
})();

/* ── 40 difference inversion ─────────────────────── */
(function(){
  var host = document.getElementById('dirun');
  if (!host) return;
  /* Fixed reference grounds rather than house tokens: the claim is about
     photographs, white, black, saturated colour and mid-grey specifically.
     Grey sits fourth so the words cross it mid-pan. */
  var GROUND = [P[1].src, '#fff', '#000', '#808080', '#D4673F',
                (ATKINS[0] || P[4]).src];
  GROUND.forEach(function(m){
    var i = document.createElement('i');
    i.style.background = m.slice(0, 4) === 'http'
      ? 'url("' + m + '") center/cover' : m;
    host.appendChild(i);
  });
})();

/* ── 41 threshold flip ─────────────────────────────────────── */
(function(){
  var pane = document.getElementById('tf'), host = document.getElementById('tfpanels');
  if (!pane) return;
  [['a', 'Ground', 'Ink on near-black, one warm accent.'],
   ['b', 'Violet', 'A different set, not a turn of the last one.'],
   ['c', 'Steel',  'And again, arriving whole at a single instant.']
  ].forEach(function(t){
    var d = document.createElement('div');
    d.dataset.i = t[0];
    d.innerHTML = '<b>' + t[1] + '</b><p>' + t[2] + '</p>'
                + '<span class="tfchips"><i></i><i></i><i></i></span>';
    host.appendChild(d);
  });
  [].forEach.call(host.children, function(panel){
    new IntersectionObserver(function(es){
      es.forEach(function(e){ if (e.isIntersecting) pane.dataset.flip = e.target.dataset.i; });
    }, { root: pane, rootMargin: '-45% 0px -45% 0px' }).observe(panel);
  });
  pane.dataset.flip = 'a';
})();

/* ── 24 snap stop ──────────────────────────────────────────── */
(function(){
  var A = document.getElementById('snstA'), B = document.getElementById('snstB');
  if (!A) return;
  [A, B].forEach(function(track){
    P.forEach(function(w, i){
      var li = document.createElement('li');
      li.innerHTML = imgTag(w, '118px') + '<b>' + String(i + 1).padStart(2, '0') + '</b>';
      track.appendChild(li);
    });
  });
})();

/* ── the entrance: find an effect by any name it goes by ─────── */
(function(){
  var input = document.getElementById('find'), index = document.querySelector('.entrance .index');
  if (!input || !index) return;
  var caption = document.querySelector('.entrance .caption'), rest = caption.textContent;
  var links = [].slice.call(index.querySelectorAll('ol a')), sel = -1;   /* the terms, not the pillar names */
  var norm = function(s){ return s.toLowerCase().normalize('NFKD').replace(/[^a-z0-9]+/g, ' ').trim(); };
  /* every word typed must begin a word of the name, as people expect: 'pin' finds pinning, not snapping */
  var starts = function(text, q){ var w = text.split(' '); return q.split(' ').every(function(t){ return w.some(function(x){ return x.indexOf(t) === 0; }); }); };
  var words = links.map(function(a){ return { a: a, name: norm(a.querySelector('span').textContent),
    aka: a.dataset.aka.split('·').map(function(x){ return x.trim(); }) }; });
  function label(a){
    caption.textContent = a ? '' : rest;
    if (!a) return;
    var b = document.createElement('b'); b.textContent = a.querySelector('span').textContent;
    caption.append(b, ' — ' + a.dataset.gloss);
  }
  function hits(){ return links.filter(function(a){ return a.classList.contains('hit'); }); }
  function choose(i){
    links.forEach(function(a){ a.classList.remove('on'); });
    var h = hits(); sel = h.length ? (i + h.length) % h.length : -1;
    if (sel >= 0){ h[sel].classList.add('on'); label(h[sel]); } else label(null);
  }
  input.addEventListener('input', function(){
    var q = norm(input.value);
    index.classList.toggle('finding', !!q);
    words.forEach(function(w){
      var shown = w.a.querySelector('.aka-hit'); if (shown) shown.remove();
      if (!q){ w.a.classList.remove('hit'); return; }
      var inName = starts(w.name, q), alias = !inName && w.aka.find(function(x){ return starts(norm(x), q); });
      w.a.classList.toggle('hit', inName || !!alias);
      if (alias){ var i = document.createElement('i'); i.className = 'aka-hit'; i.textContent = alias; w.a.append(i); }
    });
    choose(0);
    if (!q){ links.forEach(function(a){ a.classList.remove('on'); }); label(null); }
    else if (sel < 0) caption.textContent = 'No effect goes by “' + input.value.trim() + '” here yet.';
  });
  input.addEventListener('keydown', function(e){
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp'){ e.preventDefault(); choose(sel + (e.key === 'ArrowDown' ? 1 : -1)); }
    else if (e.key === 'Enter'){ var h = hits()[Math.max(sel, 0)]; if (h) location.href = h.href; }
    else if (e.key === 'Escape'){ input.value = ''; input.dispatchEvent(new Event('input')); }
  });
  links.forEach(function(a){
    a.addEventListener('pointerenter', function(){ label(a); });
    a.addEventListener('focus', function(){ label(a); });
    a.addEventListener('pointerleave', function(){ var h = hits()[sel]; label(h || null); });
  });
  /* start typing anywhere and the field takes it */
  addEventListener('keydown', function(e){
    if (document.activeElement !== input && e.key.length === 1 && !e.metaKey && !e.ctrlKey && !e.altKey) input.focus();
  });
})();

/* ── a term: ← and → turn to its neighbours ──────────────────── */
(function(){
  var prev = document.querySelector('.pager .prev'), next = document.querySelector('.pager .next');
  if (!prev && !next) return;
  addEventListener('keydown', function(e){
    var t = e.target;
    if (e.metaKey || e.ctrlKey || e.altKey || /INPUT|TEXTAREA|SELECT/.test(t.tagName) || t.closest('.stage')) return;
    if (e.key === 'ArrowRight' && next) location.href = next.href;
    if (e.key === 'ArrowLeft' && prev) location.href = prev.href;
  });
})();
