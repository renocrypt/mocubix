/* One façade, six lights. Whichever canvas crosses the band at eye level names
   its palette on the stage; the stylesheet does the rest. */
(function(){
  var stage = document.querySelector('.rouen');
  if (!stage) return;
  var eye = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ if (e.isIntersecting) stage.dataset.light = e.target.dataset.light; });
  }, {rootMargin: '-45% 0px -45% 0px'});
  stage.querySelectorAll('.canvas').forEach(function(c){ eye.observe(c); });
})();
