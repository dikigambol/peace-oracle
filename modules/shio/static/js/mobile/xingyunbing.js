(function () {
  const Shio = window.Shio;
  const byId = Shio.byId;
  let els = null;

  function render(state, instant) {
    const open = state.ui.view === "cookie" && Boolean(state.form.shio);
    Shio.markChoice(els.root, "shio", state.form.shio);
    els.pick.hidden = open;
    els.view.hidden = !open;
    els.home.hidden = open;
    els.back.hidden = !open;
    els.reset.hidden = !(open && state.ui.cracked);
    if (open) Shio.cookie.renderStage(els.stage, state, instant === true);
  }

  function goBack() {
    Shio.updateForm({ shio: null });
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
      stage: Shio.cookie.stageElements("m"),
    };
    root.querySelectorAll("[data-shio]").forEach((button) => {
      button.addEventListener("click", () => {
        Shio.cookie.pick(button.dataset.shio);
        Shio.focusResult(els.view);
      });
    });
    Shio.cookie.bindCrack(els.stage);
    els.back.addEventListener("click", goBack);
    els.reset.addEventListener("click", goBack);
  }

  function activate(state) {
    render(state, true);
  }

  Shio.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
