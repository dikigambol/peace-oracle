(function () {
  const Shio = window.Shio;
  const byId = Shio.byId;
  let els = null;

  function render(state, instant) {
    const open = state.ui.view === "cookie" && Boolean(state.form.shio);
    Shio.markChoice(els.root, "shio", open ? state.form.shio : null);
    els.empty.hidden = open;
    els.view.hidden = !open;
    if (open) Shio.cookie.renderStage(els.stage, state, instant === true);
  }

  function init(root) {
    els = {
      root: root,
      empty: byId("d-cookie-empty"),
      view: byId("d-cookie-view"),
      stage: Shio.cookie.stageElements("d"),
    };
    root.querySelectorAll("[data-shio]").forEach((button) => {
      button.addEventListener("click", () => {
        Shio.cookie.pick(button.dataset.shio);
        Shio.scrollIntoView(els.view);
      });
    });
    Shio.cookie.bindCrack(els.stage);
  }

  function activate(state) {
    render(state, true);
  }

  Shio.registerRenderer("desktop", { init: init, render: render, activate: activate });
})();
