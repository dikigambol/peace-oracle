(function () {
  const Tarot = window.Tarot;
  const TYPING = ["INPUT", "TEXTAREA", "SELECT"];

  function init(root) {
    const prev = root.querySelector("[data-carta-prev]");
    const next = root.querySelector("[data-carta-next]");
    document.addEventListener("keydown", (event) => {
      if (root.hidden || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
      if (event.target && (TYPING.includes(event.target.tagName) || event.target.isContentEditable)) return;
      const link = event.key === "ArrowLeft" ? prev : event.key === "ArrowRight" ? next : null;
      if (!link) return;
      event.preventDefault();
      window.location.href = link.href;
    });
  }

  Tarot.registerRenderer("desktop", { init: init, render: () => {}, activate: () => {} });
})();
