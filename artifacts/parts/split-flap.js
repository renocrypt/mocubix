/* split-flap — one module of a split-flap display, as a custom element.
 *
 *   <script src="parts/split-flap.js"></script>
 *   <split-flap drum="digits">7</split-flap>
 *
 * A module is a drum of printed flaps that only turns forward. Give it a new
 * value and it turns one flap at a time until that value shows, so every
 * change passes each flap printed in between. The distance, not an authored
 * delay, decides how long a module takes; a board of them settles unevenly,
 * the way the real ones do.
 *
 * Attributes
 *   drum   a registered drum — 'digits', 'letters', 'chars', or one added with
 *          SplitFlap.drum(name, values), before or after the element is
 *          parsed — or an inline list: "Dover|Summit|…". Every drum starts
 *          with the blank flap.
 *   step   milliseconds per flap (default 70). Each module also gets a small
 *          personal variation, as real motors do.
 *   ticks  present → the axle shows the pin marks a long word flap has.
 *   depth  present → the flap falls in true perspective. Worth it on a large
 *          module seen close; without it a module falls flat — foreshortened,
 *          not rotated — which at board sizes and flap speeds reads the same
 *          and costs far less.
 *
 * Content
 *   The element's text is its value, and stays real DOM text: assistive
 *   technology and crawlers read the value, never the spinning flaps.
 *
 * Script
 *   el.value = 'Dover'               turn to a value
 *   el.showing                       the flap showing now (trails value mid-turn)
 *   el.set(v, { delay, instant })    turn after a delay (ms), or cut straight to it
 *   el.wake(delay, value)            show the blank flap, then turn to the value
 *                                    (or to its current one); turns even before
 *                                    the module is reported on screen
 *   el.onflap = (value, i) => {}     called as each flap falls (optional)
 *   'settle' event                   the drum has stopped on a new value,
 *                                    by turning or by a cut
 *   SplitFlap.sound(true)            the clack of falling flaps; call from a click
 *
 * Styling — custom properties, set on the element or any ancestor
 *   --flap-face    flap colour                --flap-ink     lettering colour
 *   --flap-font    lettering family           --flap-weight  lettering weight
 *   --flap-size    lettering size             --flap-track   letter-spacing
 *   --flap-justify start | center | end       --flap-pad     inline padding
 *   --flap-shift   nudge the lettering onto the split line (e.g. .04em)
 *   --flap-radius  corner radius              --flap-split   gap at the axle
 *   --flap-axle    axle and pin colour        --flap-stack   'none' hides the flap edges
 *   Size the module itself with width and height.
 *
 * Behaviour
 *   One shared loop keeps time for every module on the page and sleeps when
 *   nothing turns. A flat module writes one leaf per frame while it turns
 *   and nothing at rest: no compositor layers, no restyled subtrees. A deep module hands each flap to the compositor as a
 *   pair of animations. A module outside the viewport, or on a device set to
 *   reduce motion, takes its value at once: a cut, not a spin.
 */
(() => {
  if (customElements.get('split-flap')) return;

  const DRUMS = {
    digits:  ['', ...'0123456789'],
    letters: ['', ...'ABCDEFGHIJKLMNOPQRSTUVWXYZ'],
    chars:   ['', ...'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789&-./()\':'],
  };

  /* A flap falls under gravity: its angle grows with the square of time, so
     it reaches the vertical at 1/√2 of the step and lands at full speed. */
  const HALF = Math.SQRT1_2;
  const TOP = { easing: 'cubic-bezier(.333,0,.667,.333)', fill: 'forwards' };      // angle ∝ u²
  const BOTTOM = { easing: 'cubic-bezier(.333,.276,.667,.609)', fill: 'both' };    // the rest of the same fall
  const FALLING = [{ transform: 'rotateX(0deg)', filter: 'brightness(1)' }, { transform: 'rotateX(-90deg)', filter: 'brightness(.5)' }];
  const LANDING = [{ transform: 'rotateX(90deg)', filter: 'brightness(.5)', opacity: 1 }, { transform: 'rotateX(0deg)', filter: 'brightness(1)', opacity: 1 }];

  const sheet = new CSSStyleSheet();
  sheet.replaceSync(`
:host{display:inline-block;position:relative;vertical-align:top;inline-size:1.1em;block-size:1.7em;contain:size layout style}
.sr{position:absolute;inline-size:1px;block-size:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.m{position:absolute;inset:0;
  font:var(--flap-weight,500) var(--flap-size,1em)/1 var(--flap-font,system-ui,sans-serif);
  letter-spacing:var(--flap-track,0);color:var(--flap-ink,#f4f1ea)}
.face,.h{position:absolute;inset-inline:0;background-color:var(--flap-face,#2b2a28)}
.face b,.h b{position:absolute;inset-inline:0;display:flex;align-items:center;justify-content:var(--flap-justify,center);
  padding-inline:var(--flap-pad,0);white-space:pre;font-weight:inherit}
/* At rest a module is one face with the axle drawn across it: nothing to
   clip, nothing to transform. The four half-flaps exist only while it turns. */
.face{inset-block:0;border-radius:var(--flap-radius,.06em);
  background-image:linear-gradient(rgb(255 255 255 / .07),rgb(255 255 255 / 0) 32%,rgb(0 0 0 / .03) 50%,rgb(0 0 0 / .13) 50%,rgb(0 0 0 / .02) 67%,rgb(0 0 0 / 0) 85%,rgb(0 0 0 / .1))}
.face b{inset-block:var(--flap-shift,0) calc(var(--flap-shift,0) * -1)}
.h{display:none;block-size:calc(50% - var(--flap-split,1px) / 2);overflow:hidden}
.on .h{display:block}
.on .face{display:none}
.t,.ft{inset-block-start:0;border-radius:var(--flap-radius,.06em) var(--flap-radius,.06em) 0 0;
  transform-origin:50% calc(100% + var(--flap-split,1px) / 2);
  background-image:linear-gradient(rgb(255 255 255 / .07),rgb(255 255 255 / 0) 65%,rgb(0 0 0 / .06))}
.b,.fb{inset-block-end:0;border-radius:0 0 var(--flap-radius,.06em) var(--flap-radius,.06em);
  transform-origin:50% calc(var(--flap-split,1px) / -2);
  background-image:linear-gradient(rgb(0 0 0 / .13),rgb(0 0 0 / .02) 35%,rgb(0 0 0 / 0) 70%,rgb(0 0 0 / .1))}
.h b{block-size:calc(200% + var(--flap-split,1px))}
.t b,.ft b{inset-block-start:var(--flap-shift,0)}
.b b,.fb b{inset-block-end:calc(var(--flap-shift,0) * -1)}
.ft,.fb{z-index:2}
.fb{opacity:0}
.face::before,.b::before{content:var(--flap-stack,'');position:absolute;inset:auto 0 0;block-size:6%;pointer-events:none;
  background:repeating-linear-gradient(to top,rgb(0 0 0 / .22) 0 1px,rgb(0 0 0 / 0) 1px 3px)}
.b::before{block-size:12%}
.x{position:absolute;inset-inline:0;inset-block-start:calc(50% - var(--flap-split,1px) / 2);block-size:var(--flap-split,1px);z-index:3;
  background:var(--flap-axle,rgb(0 0 0 / .5))}
.x::before,.x::after{content:'';position:absolute;inset-block-start:calc(var(--flap-split,1px) / 2 - .16em);inline-size:max(1px,.07em);block-size:.32em;
  border-radius:1px;background:var(--flap-axle,rgb(0 0 0 / .5))}
:host([depth]) .m{perspective:calc(var(--flap-size,1em) * 9)}
.x::before{inset-inline-start:.05em}
.x::after{inset-inline-end:.05em}
:host([ticks]) .x{inset-block-start:calc(50% - .13em);block-size:.26em;background:
  linear-gradient(var(--flap-axle,rgb(0 0 0 / .5)),var(--flap-axle,rgb(0 0 0 / .5))) 0 50% / 100% var(--flap-split,1px) no-repeat,
  repeating-linear-gradient(90deg,rgb(0 0 0 / 0) 0 calc(4.2em - 1px),var(--flap-axle,rgb(0 0 0 / .5)) calc(4.2em - 1px) 4.2em) 1.4em 0 / 100% 100% no-repeat}
:host([ticks]) .x::before,:host([ticks]) .x::after{inset-block-start:calc(.13em - .16em)}
`);

  const template = document.createElement('template');
  template.innerHTML = '<span class="sr"><slot></slot></span><div class="m" aria-hidden="true"><div class="face"><b></b></div>'
    + '<div class="h t"><b></b></div><div class="h b"><b></b></div>'
    + '<div class="h ft"><b></b></div><div class="h fb"><b></b></div><i class="x"></i></div>';

  const still = matchMedia('(prefers-reduced-motion: reduce)');
  const turning = new Set();
  let raf = 0, fallen = 0;

  function frame(now){
    fallen = 0;
    for (const m of turning) m._frame(now);
    if (fallen) clack(fallen);
    raf = turning.size ? requestAnimationFrame(frame) : 0;
  }
  function run(){ if (!raf) raf = requestAnimationFrame(frame); }
  still.addEventListener('change', () => { if (still.matches) for (const m of [...turning]) m._land(); });

  /* Off screen, a module has nobody to turn for: it lands at once. */
  const seen = new IntersectionObserver(entries => {
    for (const e of entries){
      e.target._visible = e.isIntersecting;
      if (!e.isIntersecting && turning.has(e.target)) e.target._land();
    }
  }, { rootMargin: '10% 0px' });

  function drumFor(name){
    if (!name) return DRUMS.chars;
    if (DRUMS[name]) return DRUMS[name];
    return ['', ...name.split('|').filter(Boolean)];
  }

  class SplitFlap extends HTMLElement {
    static drum(name, values){ DRUMS[name] = ['', ...values.filter(v => v !== '')]; return DRUMS[name]; }

    constructor(){
      super();
      const root = this.attachShadow({ mode: 'open' });
      root.adoptedStyleSheets = [sheet];
      root.appendChild(template.content.cloneNode(true));
      const [t, b, ft, fb] = root.querySelectorAll('.h');
      this._m = root.querySelector('.m');
      this._leaf = { ft, fb };
      this._drawn = '';
      this._f = { face: root.querySelector('.face b'), t: t.firstChild, b: b.firstChild, ft: ft.firstChild, fb: fb.firstChild };
      this._shown = { face: null, t: null, b: null, ft: null, fb: null };
      this._anim = null;
      this._visible = false;
      this._jit = 0.93 + Math.random() * 0.14;
      this.onflap = null;
    }

    /* While the parser is still running, an element connects before its text
       arrives; it then reads its value when parsing ends, or the first time
       it is asked to do anything, whichever comes first. */
    connectedCallback(){
      if (!this._drum){
        if (document.readyState !== 'loading' || this.firstChild) this._init();
        else document.addEventListener('DOMContentLoaded', () => this._init(), { once: true });
      }
      seen.observe(this);
    }
    disconnectedCallback(){ seen.unobserve(this); if (turning.has(this)) this._land(); }

    /* A named drum may be registered after the element is parsed; until then
       the module holds only what it shows, and adopts the drum the first time
       it is asked to turn. */
    _init(){
      if (this._drum) return;
      const name = this.getAttribute('drum');
      this._pending = name && !DRUMS[name] && !name.includes('|') ? name : null;
      this._drum = this._pending ? [''] : drumFor(name);
      const i = this._index(this.textContent.trim());
      this._cur = this._next = this._target = i;
      this._paint(i, i);
    }
    _resolve(){
      if (!this._pending || !DRUMS[this._pending]) return;
      const shown = this._drum[this._cur];
      this._drum = DRUMS[this._pending]; this._pending = null;
      this._cur = this._next = this._target = this._index(shown);
    }

    get value(){ return this._drum ? this._drum[this._target] : this.textContent.trim(); }
    set value(v){ this.set(v); }
    get showing(){ return this._drum ? this._drum[this._cur] : this.textContent.trim(); }

    set(v, { delay = 0, instant = false } = {}){ this._set(v, delay, instant, false); }

    /* wake() is an explicit request to turn, so it turns even before the
       module has been reported on screen — only reduced motion cuts it. */
    wake(delay = 0, value){
      this._init(); this._resolve();
      const v = value === undefined ? this.value : value;
      this._stop(); turning.delete(this);
      this._cur = this._next = this._target = 0;
      this._paint(0, 0);
      this._set(v, delay, false, true);
    }

    _set(v, delay, instant, force){
      v = v == null ? '' : String(v);
      this._init(); this._resolve();
      const i = this._index(v);
      if (this.textContent !== v) this.textContent = v;
      if (instant || still.matches || !this.isConnected || (!this._visible && !force)){ this._target = i; this._land(); return; }
      if (turning.has(this)){ this._target = i; return; }
      if (i === this._cur) return;
      this._target = i;
      this._startAt = performance.now() + delay;
      this._end = null;
      this._dur = (+this.getAttribute('step') || 70) * this._jit;
      turning.add(this); run();
    }

    _index(v){
      let i = this._drum.indexOf(v);
      if (i < 0){ this._drum = this._drum.concat(v); i = this._drum.length - 1; }
      return i;
    }

    _paint(cur, next){
      const d = this._drum, f = this._f, s = this._shown;
      const want = this._on ? { t: d[next], ft: d[cur], fb: d[next], b: d[cur] } : { face: d[cur] };
      for (const k in want) if (s[k] !== want[k]){ f[k].textContent = want[k]; s[k] = want[k]; }
    }

    /* One flap: the upper leaf, printed with the current value, falls to the
       vertical and uncovers the next value's upper half; the lower leaf,
       printed with the next value, lands over the current lower half. */
    _fall(now){
      if (!this._on){ this._on = true; this._m.classList.add('on'); }
      this._next = (this._cur + 1) % this._drum.length;
      this._paint(this._cur, this._next);
      const d = this._dur, L = this._leaf;
      if (this.hasAttribute('depth')) this._anim = [
        L.ft.animate(FALLING, { ...TOP, duration: d * HALF }),
        L.fb.animate(LANDING, { ...BOTTOM, duration: d * (1 - HALF), delay: d * HALF }),
      ];
      this._begin = now; this._end = now + d;
    }

    /* The flat fall: each leaf is foreshortened by the cosine of its angle and
       darkens as it turns away from the light — one write per leaf. */
    _draw(now){
      const t = Math.min(1, (now - this._begin) / this._dur), a = Math.PI * t * t, L = this._leaf;
      const top = a < Math.PI / 2, c = Math.abs(Math.cos(a)).toFixed(3), dark = Math.round(50 * Math.sin(a));
      const key = c + dark;
      if (key === this._drawn) return;
      this._drawn = key;
      const shade = `background-color:color-mix(in srgb,var(--flap-face,#2b2a28),#000 ${dark}%);color:color-mix(in srgb,var(--flap-ink,#f4f1ea),#000 ${dark}%)`;
      if (top){ L.ft.style.cssText = `transform:scaleY(${c});${shade}`; if (this._half !== 1){ L.fb.style.cssText = 'opacity:1;transform:scaleY(0)'; this._half = 1; } }
      else { L.fb.style.cssText = `opacity:1;transform:scaleY(${c});${shade}`; if (this._half !== 2){ L.ft.style.cssText = 'transform:scaleY(0)'; this._half = 2; } }
    }

    _stop(){
      if (this._anim){ this._anim[0].cancel(); this._anim[1].cancel(); this._anim = null; }
      if (this._drawn){ this._leaf.ft.style.cssText = this._leaf.fb.style.cssText = ''; this._drawn = ''; this._half = 0; }
    }

    _frame(now){
      if (now < this._startAt) return;
      if (this._end === null){ this._fall(now); if (!this._anim) this._draw(now); return; }
      if (now < this._end){ if (!this._anim) this._draw(now); return; }
      const n = this._drum.length, left = (this._target - this._cur + n) % n;
      const k = Math.min(left, 1 + Math.floor((now - this._end) / this._dur));   // a late frame may owe more than one flap
      this._stop();
      fallen += k;
      if (k >= left){ this._land(); return; }
      this._cur = (this._cur + k) % n;
      if (this.onflap) this.onflap(this._drum[this._cur], this._cur);
      this._fall(now);
      if (!this._anim) this._draw(now);
    }

    /* Stop on the target, whether by arriving or by a cut. */
    _land(){
      this._stop();
      const moved = turning.delete(this) || this._cur !== this._target;
      this._cur = this._next = this._target;
      if (this._on){ this._on = false; this._m.classList.remove('on'); }
      this._paint(this._cur, this._cur);
      if (!moved) return;
      if (this.onflap) this.onflap(this._drum[this._cur], this._cur);
      this.dispatchEvent(new Event('settle'));
    }
  }

  /* The sound: short bursts of filtered noise with a small body, rendered once,
     played a few at a time per frame so a board turning at once reads as a
     rattle rather than a buzz. */
  let audio = null, audible = false;
  function voice(){
    const ctx = new AudioContext(), out = ctx.createGain();
    out.gain.value = 0.55;
    out.connect(ctx.createDynamicsCompressor()).connect(ctx.destination);
    const clicks = [];
    for (let v = 0; v < 10; v++){
      const len = Math.round(ctx.sampleRate * 0.035), buf = ctx.createBuffer(1, len, ctx.sampleRate), d = buf.getChannelData(0);
      const ring = 1500 + Math.random() * 1900, body = 160 + Math.random() * 140;
      for (let i = 0; i < len; i++){
        const s = i / ctx.sampleRate;
        d[i] = (Math.random() * 2 - 1) * Math.exp(-s / 0.0014) * 0.85
             + Math.sin(2 * Math.PI * ring * s) * Math.exp(-s / 0.0026) * 0.22
             + Math.sin(2 * Math.PI * body * s) * Math.exp(-s / 0.007) * 0.4;
      }
      clicks.push(buf);
    }
    return { ctx, out, clicks };
  }
  function clack(n){
    if (!audible) return;
    const { ctx, out, clicks } = audio, k = Math.min(n, 5), at = ctx.currentTime;
    const level = Math.min(1, 0.3 + Math.log2(n + 1) * 0.12) / Math.sqrt(k);
    for (let i = 0; i < k; i++){
      const src = ctx.createBufferSource(), g = ctx.createGain();
      src.buffer = clicks[(Math.random() * clicks.length) | 0];
      src.playbackRate.value = 0.85 + Math.random() * 0.35;
      g.gain.value = level * (0.55 + Math.random() * 0.45);
      src.connect(g).connect(out);
      src.start(at + Math.random() * 0.016);
    }
  }
  SplitFlap.sound = on => {
    audible = !!on;
    if (audible && !audio) audio = voice();
    if (audio) audible ? audio.ctx.resume() : audio.ctx.suspend();
    return audible;
  };

  window.SplitFlap = SplitFlap;
  customElements.define('split-flap', SplitFlap);
})();
