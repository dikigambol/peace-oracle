(function () {
  const Shio = window.Shio;
  let els = null;

  function byId(id) {
    return document.getElementById(id);
  }

  function render(state, instant) {
    const open = state.ui.view === "cookie" && Boolean(state.form.shio);
    Shio.shio.markPicked(els.root, state.form.shio);
    els.pick.hidden = open;
    els.view.hidden = !open;
    els.home.hidden = open;
    els.back.hidden = !open;
    els.reset.hidden = !(open && state.ui.cracked);
    if (open) Shio.cookie.renderStage(els.stage, state, instant === true);
  }

  function goBack() {
    Shio.cookie.back();
    window.scrollTo(0, 0);
  }

  function init(root) {
    els = {
      root: root,
      home: byId("m-cookie-home"),
      back: byId("m-cookie-back"),
      pick: byId("m-cookie-pick"),
      view: byId("m-cookie-view"),
      reset: byId("m-cookie-reset"),
      stage: {
        hanzi: byId("m-cookie-hanzi"),
        name: byId("m-cookie-name"),
        cookie: byId("m-cookie"),
        hint: byId("m-cookie-hint"),
        slipBox: byId("m-cookie-slip"),
      },
    };
    root.querySelectorAll("[data-shio]").forEach((button) => {
      button.addEventListener("click", () => {
        window.scrollTo(0, 0);
        Shio.cookie.pick(button.dataset.shio);
      });
    });
    els.stage.cookie.addEventListener("click", () => Shio.cookie.crack(els.stage.cookie, els.stage.hint));
    els.back.addEventListener("click", goBack);
    els.reset.addEventListener("click", goBack);
  }

  function activate(state) {
    render(state, true);
  }

  Shio.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
