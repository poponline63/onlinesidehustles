(function () {
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }

  var frameCount = 10;
  var frame = 0;
  var cacheBust = 'edge-v1';
  var link = document.querySelector('link[data-animated-favicon]');

  if (!link) {
    link = document.createElement('link');
    link.setAttribute('rel', 'icon');
    link.setAttribute('type', 'image/png');
    link.setAttribute('sizes', '32x32');
    link.setAttribute('data-animated-favicon', 'true');
    document.head.appendChild(link);
  }

  function setFrame() {
    var next = String(frame).padStart(2, '0');
    link.setAttribute('href', '/favicon-frame-' + next + '.png?v=' + cacheBust);
    frame = (frame + 1) % frameCount;
    window.setTimeout(setFrame, document.hidden ? 850 : 180);
  }

  setFrame();
})();
