// Marquee: each band's greetings are set twice and the pair travels half its width. The duration is one set's width
// over the band's speed in pixels a second, so bands of any length keep their pace; it is measured again whenever the
// width changes, as it does when the fonts arrive.
for (const band of document.querySelectorAll('.voyager .band')) {
  const set = band.querySelector('.set');
  new ResizeObserver(() => band.style.setProperty('--dur', `${(set.offsetWidth / band.dataset.speed).toFixed(1)}s`)).observe(set);
}
