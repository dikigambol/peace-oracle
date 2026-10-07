(function () {
  const Tarot = window.Tarot;
  const SWIPE_DISTANCE = 60;

  function init(root) {
    const art = root.querySelector(".tr-carta-art");
    const prev = root.querySelector("[data-carta-prev]");
    const next = root.querySelector("[data-carta-next]");
    if (!art) return;
    let start = null;
    art.addEventListener("touchstart", (event) => {
      const touch = event.changedTouches[0];
      start = { x: touch.clientX, y: touch.clientY };
    }, { passive: true });
    art.addEventListener("touchend", (event) => {
      if (!start) return;
      const touch = event.changedTouches[0];
      const dx = touch.clientX - start.x;
      const dy = touch.clientY - start.y;
      start = null;
      if (Math.abs(dx) < SWIPE_DISTANCE || Math.abs(dx) < Math.abs(dy) * 1.5) return;
      const link = dx > 0 ? prev : next;
      if (link) window.location.href = link.href;
    }, { passive: true });
  }

  Tarot.registerRenderer("mobile", { init: init, render: () => {}, activate: () => {} });
})();
