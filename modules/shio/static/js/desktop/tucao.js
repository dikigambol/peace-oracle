(function () {
  const Shio = window.Shio;
  let els = null;
  let picker = null;
  let renderedResult = null;
  let renderedDraw = null;

  function byId(id) {
    return document.getElementById(id);
  }

  function renderRoast(state, instant) {
    const data = state.result;
    if (data !== renderedResult) {
      Shio.clear(els.header);
      els.header.appendChild(Shio.roast.buildHeader(data));
      renderedResult = data;
    }
    if (state.draw === renderedDraw) return;
    Shio.clear(els.sections);
    Shio.roast.sections(data, state.draw).forEach((section) => els.sections.appendChild(section.node));
    els.count.textContent = Shio.roast.comboLabel(data, state.draw);
    els.reroll.hidden = !Shio.roast.canReroll(data);
    if (!instant && renderedDraw && renderedDraw.count < state.draw.count) Shio.replay(els.card, "roast-flash");
    renderedDraw = state.draw;
  }

  function render(state, instant) {
    const data = state.result;
    Shio.markChoice(els.root, "gender", state.form.gender);
    window.setButtonLoading(els.submit, state.loading, "Menyalakan api...", !state.form.date);
    if (!state.loading) els.submit.disabled = !state.form.date;
    els.empty.hidden = Boolean(data) || state.loading;
    els.loading.hidden = !state.loading;
    els.result.hidden = !data || state.loading;
    if (data) {
      renderRoast(state, instant === true);
      Shio.roast.renderPairPanel(els.pair, state);
    }
  }

  function init(root) {
    els = {
      root: root,
      date: byId("d-roast-date"),
      submit: byId("d-roast-submit"),
      empty: byId("d-roast-empty"),
      loading: byId("d-roast-loading"),
      result: byId("d-roast-result"),
      card: byId("d-roast-card"),
      header: byId("d-roast-header"),
      sections: byId("d-roast-sections"),
      count: byId("d-roast-count"),
      reroll: byId("d-roast-reroll"),
      pair: {
        toggle: root.querySelector("[data-pair-toggle]"),
        body: root.querySelector("[data-pair-body]"),
        loading: root.querySelector("[data-pair-loading]"),
        card: root.querySelector("[data-pair-card]"),
      },
    };
    els.loading.appendChild(Shio.loadingBox("Menyalakan api..."));
    picker = Shio.desktopDate(els.date, {
      onChange: (dates, value) => {
        Shio.updateForm({ date: value || "" });
        render(Shio.getState());
      },
    });
    Shio.roast.bindGender(root, () => render(Shio.getState()));
    Shio.roast.bindPairPanel(els.pair);
    els.submit.addEventListener("click", async () => {
      Shio.particles.emitFrom(els.submit, 34);
      const data = await Shio.roast.submit();
      if (data) Shio.scrollIntoView(els.result);
    });
    els.reroll.addEventListener("click", Shio.roast.reroll);
  }

  function activate(state) {
    Shio.setDesktopDate(picker, els.date, state.form.date);
    renderedResult = null;
    renderedDraw = null;
    render(state, true);
  }

  Shio.registerRenderer("desktop", { init: init, render: render, activate: activate });
})();
