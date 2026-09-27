(function () {
  const Shio = window.Shio;
  let els = null;

  function byId(id) {
    return document.getElementById(id);
  }

  function render(state, instant) {
    const open = state.ui.view === "cookie" && Boolean(state.form.shio);
    Shio.shio.markPicked(els.root, open ? state.form.shio : null);
    els.empty.hidden = open;
    els.view.hidden = !open;
    if (open) Shio.cookie.renderStage(els.stage, state, instant === true);
  }

  function init(root) {
    els = {
      root: root,
      empty: byId("d-cookie-empty"),
      view: byId("d-cookie-view"),
      stage: {
        hanzi: byId("d-cookie-hanzi"),
        name: byId("d-cookie-name"),
        cookie: byId("d-cookie"),
        hint: byId("d-cookie-hint"),
        slipBox: byId("d-cookie-slip"),
      },
    };
    root.querySelectorAll("[data-shio]").forEach((button) => {
      button.addEventListener("click", () => {
        Shio.cookie.pick(button.dataset.shio);
        Shio.scrollIntoView(els.view);
      });
    });
    els.stage.cookie.addEventListener("click", () => Shio.cookie.crack(els.stage.cookie, els.stage.hint));
  }

  function activate(state) {
    render(state, true);
  }

  Shio.registerRenderer("desktop", { init: init, render: render, activate: activate });
})();
