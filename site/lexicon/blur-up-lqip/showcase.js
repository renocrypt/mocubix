// Blur-up: every slot shows its stand-in from the start (a 16-pixel WebP written into the page); from here on a print
// is held back until its file has arrived and been decoded, then comes into focus over it. What each cost is measured
// by the browser (Resource Timing, which Wikimedia allows); Replay brings the prints in again, in the order they
// arrived on this visit.
for (const wall of document.querySelectorAll('.edo')) {
  const imgs = [...wall.querySelectorAll('.slot img')];
  const got = wall.querySelector('.got'), count = wall.querySelector('.n'), replay = wall.querySelector('.replay');
  const when = new Map();                 // print → when its file finished arriving, in ms from the page's start
  const size = n => n < 1e6 ? `${Math.round(n / 1e3)} KB` : `${(n / 1e6).toFixed(1)} MB`;
  let sum = 0, timers = [];

  const settle = img => {
    const e = performance.getEntriesByName(img.currentSrc).at(-1);
    when.set(img, e ? e.responseEnd : performance.now());
    if (e?.encodedBodySize) {
      sum += e.encodedBodySize;
      img.closest('.print').querySelector('output').value = size(e.encodedBodySize);
      got.value = size(sum);
    }
    count.value = when.size;
  };

  wall.classList.add('held');
  for (const img of imgs) {
    if (img.complete && img.naturalWidth) { img.classList.add('in'); settle(img); }   // already here: nothing to show
    else img.addEventListener('load', () => img.decode().catch(() => {}).then(() => {
      settle(img);
      img.classList.add('in');
    }), { once: true });
  }

  replay.hidden = false;
  replay.addEventListener('click', () => {
    timers.forEach(clearTimeout);
    const came = imgs.filter(i => when.has(i)).sort((a, b) => when.get(a) - when.get(b));
    if (!came.length) return;
    for (const i of came) i.classList.remove('in');                 // back to the stand-ins
    // in the order they came, evenly spaced: lazy prints arrive seconds later, which would bunch all the others
    timers = came.map((i, k) => setTimeout(() => i.classList.add('in'), 1100 + k * 2600 / Math.max(1, came.length - 1)));
  });
}
