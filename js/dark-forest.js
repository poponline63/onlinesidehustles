// Starfield animation
(function() {
  var canvas = document.getElementById('starfield');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var stars = [];
  var W, H, frame = 0;

  function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }

  function initStars() {
    stars = [];
    var count = Math.floor((W * H) / 2800);
    for (var i = 0; i < count; i++) {
      var rand = Math.random();
      stars.push({
        x: Math.random() * W,
        y: Math.random() * H * 0.72,
        r: Math.random() * 1.5 + 0.15,
        alpha: Math.random() * 0.85 + 0.15,
        speed: Math.random() * 0.004 + 0.001,
        phase: Math.random() * Math.PI * 2,
        color: rand > 0.88 ? '#c8e6ff' : rand > 0.75 ? '#ffe8c0' : '#ffffff'
      });
    }
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    frame++;
    for (var i = 0; i < stars.length; i++) {
      var s = stars[i];
      var twinkle = 0.45 + 0.55 * Math.sin(frame * s.speed + s.phase);
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = s.color;
      ctx.globalAlpha = s.alpha * twinkle;
      ctx.fill();
    }
    ctx.globalAlpha = 1;
    requestAnimationFrame(draw);
  }

  resize();
  initStars();
  draw();
  window.addEventListener('resize', function() { resize(); initStars(); });
})();

// Scroll fade-in
var faders = document.querySelectorAll('.fade-in');
if (faders.length) {
  var io = new IntersectionObserver(function(entries) {
    entries.forEach(function(e) {
      if (e.isIntersecting) e.target.classList.add('visible');
    });
  }, { threshold: 0.1 });
  faders.forEach(function(f) { io.observe(f); });
}

// Mobile menu
var ham = document.getElementById('hamburger');
var menu = document.getElementById('mobileMenu');
if (ham && menu) {
  ham.addEventListener('click', function() {
    menu.classList.toggle('open');
  });
}
