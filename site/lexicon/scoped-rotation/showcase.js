// Scoped Rotation: the painting is sampled into its dots from its own image (Wikimedia serves images to canvases),
// and the counter times each frame's style work. Inside requestAnimationFrame the animations have ticked but no style
// has been recomputed yet, so reading a layout value there does this frame's style work on the spot, and it can be
// timed. Out of view, the counting stops and the angle is declared nowhere, so the page stops paying.
const oklch = (r, g, b) => {
  const lin = v => (v /= 255) <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4;
  [r, g, b] = [lin(r), lin(g), lin(b)];
  const l = Math.cbrt(.4122214708 * r + .5363325363 * g + .0514459929 * b);
  const m = Math.cbrt(.2119034982 * r + .6806995451 * g + .1073969566 * b);
  const s = Math.cbrt(.0883024619 * r + .2817188376 * g + .6299787005 * b);
  const L = .2104542553 * l + .7936177850 * m - .0040720468 * s;
  const A = 1.9779984951 * l - 2.4285922050 * m + .4505937099 * s;
  const B = .0259040371 * l + .7827717662 * m - .8086757660 * s;
  return [L, Math.hypot(A, B), (Math.atan2(B, A) * 180 / Math.PI + 360) % 360];
};

for (const stage of document.querySelectorAll('.scope')) {
  const mosaic = stage.querySelector('.mosaic'), img = stage.querySelector('.source img');
  const ms = stage.querySelector('.ms output'), n = stage.querySelector('.n output');
  const spark = stage.querySelector('.meter canvas'), ctx = spark.getContext('2d');
  const cols = +getComputedStyle(mosaic).getPropertyValue('--cols'), rows = +getComputedStyle(mosaic).getPropertyValue('--rows');

  const dots = () => {
    const c = new OffscreenCanvas(cols, rows), g = c.getContext('2d', { willReadFrequently: true });
    g.imageSmoothingQuality = 'high';
    g.drawImage(img, 0, 0, cols, rows);
    const d = g.getImageData(0, 0, cols, rows).data;
    let html = '';
    for (let k = 0; k < d.length; k += 4) {
      const [L, C, h] = oklch(d[k], d[k + 1], d[k + 2]);        // converted once, not by every dot every frame
      html += `<i style="--l:${L.toFixed(3)};--k:${C.toFixed(3)};--h:${h.toFixed(1)}deg"></i>`;
    }
    mosaic.innerHTML = html;
  };
  img.complete && img.naturalWidth ? dots() : img.addEventListener('load', dots, { once: true });

  // where the angle lives: mirrored onto the stage and, for the root, onto <html> (see showcase.css); nowhere while
  // the stage is out of view
  let on = false;
  const scope = () => {
    const where = on ? stage.querySelector('.where input:checked').value : 'still';
    stage.dataset.scope = where;
    document.documentElement.dataset.scope = where === 'root' ? 'root' : '';
  };
  stage.addEventListener('change', scope);

  // how many elements the declared angle reaches: the declaring element and everything below it
  const reach = () => {
    const where = stage.querySelector('.where input:checked').value;
    const root = { swatches: stage.querySelector('.swatches'), root: document.documentElement, painting: mosaic }[where];
    return root ? root.getElementsByTagName('*').length + 1 : 0;
  };

  const costs = [];
  let shown = 0, last = 0;
  const tick = now => {
    if (!on) return;
    if (last) costs.push(now - last);                          // the time from frame to frame, all of it counted
    last = now;
    if (costs.length > 120) costs.shift();
    const W = spark.width, H = spark.height, bar = W / 120, line = H * (1 - 16.7 / 40);
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = '#1F1A14';
    costs.forEach((c, i) => { const h = Math.max(1, Math.min(1, c / 40) * H); ctx.fillRect(i * bar, H - h, bar - 1, h); });
    ctx.fillStyle = '#B4502A';
    ctx.fillRect(0, line, W, 2);
    if (now - shown > 250 && costs.length > 4) {                // numbers a person can read: four times a second
      shown = now;
      const recent = costs.slice(-30).sort((a, b) => a - b);
      ms.value = Math.round(1000 / recent[recent.length >> 1]);
      n.value = reach().toLocaleString('en');
    }
    requestAnimationFrame(tick);
  };
  new IntersectionObserver(([e]) => {
    on = e.isIntersecting;
    scope();
    last = 0;
    if (on) requestAnimationFrame(tick);
  }).observe(stage);
}
