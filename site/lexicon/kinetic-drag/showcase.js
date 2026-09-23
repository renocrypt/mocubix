/* Throw the Roman world. The map is a native scroller (touch, trackpad and keys
   move it as they always do); this adds the grab and the throw for a mouse, and
   a click on the small map to go there. The throw keeps a share of its speed
   each frame: the decay chosen under the map. */
(function(){
  var roads = document.querySelector('.tabula .roads');
  if (!roads) return;
  var mini = document.querySelector('.tabula .mini');
  var held = false, v = 0, lastX = 0, lastT = 0, raf = 0;
  var still = matchMedia('(prefers-reduced-motion: reduce)');   /* then the map follows the hand, and stops with it */
  function decay(){ var c = document.querySelector('.tabula input[name=decay]:checked'); return c ? +c.value : 0.94; }

  roads.addEventListener('pointerdown', function(e){
    if (e.pointerType !== 'mouse' || e.button !== 0) return;
    cancelAnimationFrame(raf);
    held = true; v = 0; lastX = e.clientX; lastT = e.timeStamp;
    roads.classList.add('held');
    try { roads.setPointerCapture(e.pointerId); } catch (_) {}   /* the pointer may already be gone */
    e.preventDefault();
  });
  roads.addEventListener('pointermove', function(e){
    if (!held) return;
    var dx = e.clientX - lastX, dt = Math.max(1, e.timeStamp - lastT);
    roads.scrollLeft -= dx;
    v = 0.8 * (-dx / dt) + 0.2 * v;          /* pixels a millisecond, smoothed */
    lastX = e.clientX; lastT = e.timeStamp;
  });
  function release(e){
    if (!held) return;
    held = false;
    roads.classList.remove('held');
    if (still.matches || e.timeStamp - lastT > 90) return;   /* a pause before letting go is a put-down, not a throw */
    var k = decay(), prev = performance.now();
    raf = requestAnimationFrame(function step(now){
      var dt = Math.min(48, now - prev); prev = now;
      roads.scrollLeft += v * dt;
      v *= Math.pow(k, dt / 16.7);
      var end = roads.scrollLeft <= 0 || roads.scrollLeft >= roads.scrollWidth - roads.clientWidth - 1;
      if (Math.abs(v) > 0.02 && !end) raf = requestAnimationFrame(step);
    });
  }
  roads.addEventListener('pointerup', release);
  roads.addEventListener('pointercancel', release);
  roads.addEventListener('wheel', function(){ cancelAnimationFrame(raf); }, {passive: true});

  if (mini) mini.addEventListener('click', function(e){
    var r = mini.getBoundingClientRect();
    cancelAnimationFrame(raf);
    roads.scrollTo({left: (e.clientX - r.left) / r.width * roads.scrollWidth - roads.clientWidth / 2,
                    behavior: still.matches ? 'auto' : 'smooth'});
  });
})();
