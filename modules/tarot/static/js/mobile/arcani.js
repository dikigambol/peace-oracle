(function () {
  const Tarot = window.Tarot;

  function selectGroup(root, buttons, button) {
    const key = button.dataset.filter;
    buttons.forEach((other) => {
      const on = other === button;
      other.classList.toggle("is-active", on);
      other.setAttribute("aria-pressed", on ? "true" : "false");
    });
    root.querySelectorAll("[data-group]").forEach((group) => {
      group.hidden = key !== "semua" && group.dataset.group !== key;
    });
  }

  function init(root) {
    const buttons = Array.from(root.querySelectorAll("[data-filter]"));
    buttons.forEach((button) => {
      button.addEventListener("click", () => selectGroup(root, buttons, button));
    });
  }

  Tarot.registerRenderer("mobile", { init: init, render: () => {}, activate: () => {} });
})();
