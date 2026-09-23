// Variable Font Animation: the dial sets the weight every live line takes (the stylesheet does the rest).
for (const dial of document.querySelectorAll('.specimen input[type=range]')) {
  const stage = dial.closest('.specimen'), out = stage.querySelector('output');
  const set = () => { stage.style.setProperty('--dial', dial.value); out.value = dial.value; };
  dial.addEventListener('input', set);
  set();
}
