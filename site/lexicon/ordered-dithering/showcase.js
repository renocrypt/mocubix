// Ordered Dithering: the photograph is drawn to a canvas over it and dithered there. Each pixel takes the tone just
// below or just above its own, by its cell of the 8×8 Bayer matrix; the choice is made in linear light, so the grain
// averages to the pixel's brightness. Prints with an ink and a paper are dithered between them; the rest per channel.
const BAYER = [0, 32, 8, 40, 2, 34, 10, 42, 48, 16, 56, 24, 50, 18, 58, 26, 12, 44, 4, 36, 14, 46, 6, 38, 60, 28, 52,
  20, 62, 30, 54, 22, 3, 35, 11, 43, 1, 33, 9, 41, 51, 19, 59, 27, 49, 17, 57, 25, 15, 47, 7, 39, 13, 45, 5, 37, 63, 31,
  55, 23, 61, 29, 53, 21].map(v => (v + .5) / 64);
const lin = v => v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4;
const rgb = hex => [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16));

for (const stage of document.querySelectorAll('.tones')) {
  const canvas = stage.querySelector('canvas'), ctx = canvas.getContext('2d', { willReadFrequently: true });
  const range = stage.querySelector('#tones'), out = stage.querySelector('output'), ladder = stage.querySelector('.ladder');
  const per = stage.querySelector('.per');
  let img, src, queued = false;

  // for each 8-bit value: the tone below, the tone above (0…n), and how far between them it lies in linear light
  function table(n) {
    const lo = new Uint8Array(256), f = new Float32Array(256);
    for (let v = 0; v < 256; v++) {
      const k = Math.min(n - 1, Math.floor(v / 255 * n));
      const a = lin(k / n), b = lin((k + 1) / n);
      lo[v] = k; f[v] = (lin(v / 255) - a) / (b - a);
    }
    return { lo, f };
  }

  function draw() {
    queued = false;
    img = stage.querySelector(`.plate img[data-pic="${stage.querySelector('.pictures input:checked').value}"]`);
    stage.querySelectorAll('.plate img').forEach(i => i.hidden = i !== img);
    if (!img.complete || !img.naturalWidth) return img.addEventListener('load', redraw, { once: true });
    const box = img.getBoundingClientRect(), dpr = devicePixelRatio;
    const W = Math.round(box.width * dpr), H = Math.round(box.height * dpr);
    if (!W || !H) return;
    Object.assign(canvas.style, { left: `${img.offsetLeft}px`, top: `${img.offsetTop}px`, width: `${box.width}px`, height: `${box.height}px` });
    if (canvas.width !== W || canvas.height !== H || canvas.dataset.pic !== img.dataset.pic) {
      canvas.width = W; canvas.height = H; canvas.dataset.pic = img.dataset.pic;
      // the part shown (the img crops it with object-view-box): the whole picture, drawn larger and offset so that
      // part fills the canvas (a source rectangle would be in the file's pixels, not the density-corrected ones)
      const [t, r, b, l] = img.dataset.crop.split(' ').map(Number), dw = W / (1 - l - r), dh = H / (1 - t - b);
      ctx.drawImage(img, -l * dw, -t * dh, dw, dh);
      src = ctx.getImageData(0, 0, W, H).data;
    }
    const tones = +range.value, every = tones > 16;
    const ink = img.dataset.ink ? rgb(img.dataset.ink) : null, paper = ink && rgb(img.dataset.paper);
    out.value = every ? 'every tone' : `${tones} tones`;
    per.textContent = every || ink ? '' : `in each of red, green and blue: ${tones ** 3} colours`;
    const n = tones - 1, level = k => ink ? ink.map((c, i) => Math.round(c + (paper[i] - c) * k / n)) : [k / n * 255, k / n * 255, k / n * 255];
    ladder.style.setProperty('--ladder', every ? 'none' : `linear-gradient(90deg, ${Array.from({ length: tones }, (_, k) =>
      `rgb(${level(k).join(' ')}) ${k / tones * 100}% ${(k + 1) / tones * 100}%`).join(', ')})`);
    canvas.hidden = every;
    if (every) return;
    const { lo, f } = table(n), grain = +stage.querySelector('.grain input:checked').value * dpr;
    const dst = ctx.createImageData(W, H), d = dst.data;
    const shades = Array.from({ length: tones }, (_, k) => level(k));
    // a print's tones run from its ink to its paper: stretch its own range onto 0…255 first
    const inkY = ink ? .2126 * ink[0] + .7152 * ink[1] + .0722 * ink[2] : 0;
    const span = ink ? .2126 * paper[0] + .7152 * paper[1] + .0722 * paper[2] - inkY : 255;
    for (let y = 0; y < H; y++) {
      const row = ((y / grain) & 7) * 8;
      for (let x = 0; x < W; x++) {
        const t = BAYER[row + ((x / grain) & 7)], i = (y * W + x) * 4;
        if (ink) {
          const v = Math.max(0, Math.min(255, Math.round(((.2126 * src[i] + .7152 * src[i + 1] + .0722 * src[i + 2]) - inkY) / span * 255)));
          const s = shades[lo[v] + (f[v] > t ? 1 : 0)];
          d[i] = s[0]; d[i + 1] = s[1]; d[i + 2] = s[2];
        } else {
          for (let c = 0; c < 3; c++) { const v = src[i + c]; d[i + c] = (lo[v] + (f[v] > t ? 1 : 0)) / n * 255; }
        }
        d[i + 3] = 255;
      }
    }
    ctx.putImageData(dst, 0, 0);
  }
  const redraw = () => { if (!queued) { queued = true; requestAnimationFrame(draw); } };

  range.addEventListener('input', redraw);
  stage.addEventListener('change', redraw);
  addEventListener('resize', redraw);
  // on arrival, the tones go by themselves, once: every tone down to two
  new IntersectionObserver((seen, io) => {
    if (!seen[0].isIntersecting) return;
    io.disconnect();
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) { range.value = 2; return redraw(); }
    const t0 = performance.now();
    const step = now => {
      const k = Math.min(1, (now - t0) / 2600), v = Math.round(17 - 15 * (1 - (1 - k) ** 2));
      if (+range.value !== v) { range.value = v; draw(); }
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }, { threshold: .6 }).observe(stage);
  redraw();
}
