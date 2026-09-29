(function () {
  const Shio = window.Shio;
  const byId = Shio.byId;
  let els = null;
  let renderedResult = null;

  function renderResult(data) {
    if (data === renderedResult) return;
    Shio.clear(els.hero);
    els.hero.appendChild(Shio.guardian.buildHero(data));
    els.hero.appendChild(Shio.guardian.buildHighlights(data));
    Shio.clear(els.sections);
    Shio.guardian.sections(data).forEach((section, index) => {
      els.sections.appendChild(Shio.detailsBlock(section.title, section.icon, section.build(), index === 0));
    });
    els.sections.appendChild(Shio.detailsBlock("Waktu & Arah Sakral", "fa-compass", Shio.guardian.buildMeta(data), false));
    renderedResult = data;
  }

  function render(state) {
    const data = state.result;
    const viewing = Boolean(data) || state.loading;
    Shio.markChoice(els.root, "shio", state.form.shio);
    els.pick.hidden = viewing;
    els.view.hidden = !viewing;
    els.home.hidden = viewing;
    els.back.hidden = !viewing;
    els.back.disabled = state.loading;
    els.loading.hidden = !state.loading;
    els.result.hidden = !data || state.loading;
    if (data) renderResult(data);
  }

  function reset() {
    if (Shio.getState().loading) return;
    Shio.updateForm({ shio: null });
    Shio.setState({ result: null });
    window.scrollTo(0, 0);
  }

  function init(root) {
    els = {
      root: root,
      home: byId("m-guardian-home"),
      back: byId("m-guardian-back"),
      pick: byId("m-guardian-pick"),
      view: byId("m-guardian-view"),
      loading: byId("m-guardian-loading"),
      result: byId("m-guardian-result"),
      hero: byId("m-guardian-hero"),
      sections: byId("m-guardian-sections"),
    };
    els.loading.appendChild(Shio.loadingBox("Memanggil penjaga shio-mu..."));
    root.querySelectorAll("[data-shio]").forEach((button) => {
      button.addEventListener("click", async () => {
        window.scrollTo(0, 0);
        const data = await Shio.guardian.submit(button.dataset.shio);
        if (data) Shio.focusResult(els.result);
      });
    });
    els.back.addEventListener("click", reset);
    byId("m-guardian-reset").addEventListener("click", reset);
  }

  function activate(state) {
    renderedResult = null;
    render(state);
  }

  Shio.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
