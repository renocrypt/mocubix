/* Where the ice was. Each divider is a native range input; this hands its value
   to the picture, and pulls each divider back once, the first time its pair is seen. */
(function(){
  var ice = document.querySelector('.ice');
  if (!ice) return;
  var pairs = ice.querySelectorAll('.pair');
  pairs.forEach(function(pair){
    var range = pair.querySelector('input');
    range.addEventListener('input', function(){
      pair.setAttribute('data-held', '');
      pair.style.setProperty('--x', range.value);
    });
  });
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  ice.classList.add('armed');
  var seen = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if (!e.isIntersecting) return;
      e.target.classList.add('seen');
      seen.unobserve(e.target);
    });
  }, {threshold: .6});
  pairs.forEach(function(pair){ seen.observe(pair); });
})();
