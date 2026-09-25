(function () {
  function readToken(name, fallback) {
    const value = getComputedStyle(document.documentElement)
      .getPropertyValue(name)
      .trim();
    return value || fallback;
  }

  window.initBurstParticles = function () {
    const settings = { canvasId: "particle-canvas", surfaceId: "shio-bg", burst: 30, trail: 5 };
    const canvas = document.getElementById(settings.canvasId);
    if (!canvas || !canvas.getContext) return;

    const ctx = canvas.getContext("2d");
    const palette = [readToken("--gold", "#ffd700"), readToken("--flame", "#ff4500")];
    const particles = [];
    let running = false;
    let dragging = false;

    function resize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }

    function spawn(x, y) {
      particles.push({
        x: x,
        y: y,
        size: Math.random() * 5 + 2,
        speedX: Math.random() * 6 - 3,
        speedY: Math.random() * 6 - 3,
        color: palette[Math.random() > 0.5 ? 0 : 1],
        life: 1.0,
        decay: Math.random() * 0.02 + 0.02,
      });
    }

    function frame() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      let alive = 0;
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        p.x += p.speedX;
        p.y += p.speedY;
        p.life -= p.decay;
        if (p.life <= 0) continue;
        ctx.globalAlpha = p.life;
        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
        particles[alive++] = p;
      }
      particles.length = alive;
      ctx.globalAlpha = 1.0;
      if (alive) {
        requestAnimationFrame(frame);
      } else {
        running = false;
      }
    }

    function emit(x, y, count) {
      if (window.prefersReducedMotion()) return;
      for (let i = 0; i < count; i++) spawn(x, y);
      if (!running) {
        running = true;
        requestAnimationFrame(frame);
      }
    }

    window.addEventListener("resize", resize);
    resize();

    const surface = document.getElementById(settings.surfaceId);
    if (surface) {
      surface.addEventListener("mousedown", (e) => {
        dragging = true;
        emit(e.clientX, e.clientY, settings.burst);
      });
      surface.addEventListener("mousemove", (e) => {
        if (dragging) emit(e.clientX, e.clientY, settings.trail);
      });
      surface.addEventListener("touchstart", (e) => {
        dragging = true;
        const touch = e.touches[0];
        emit(touch.clientX, touch.clientY, settings.burst);
      });
      surface.addEventListener("touchmove", (e) => {
        if (!dragging) return;
        const touch = e.touches[0];
        emit(touch.clientX, touch.clientY, settings.trail);
      });
    }
    window.addEventListener("mouseup", () => {
      dragging = false;
    });
    window.addEventListener("touchend", () => {
      dragging = false;
    });
  };
})();
