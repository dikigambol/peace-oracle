(function () {
  const Shio = window.Shio;
  const byId = Shio.byId;
  const memo = { result: null, draw: null };
  let els = null;
  let picker = null;

  function render(state, instant) {
    const data = state.result;
    Shio.markChoice(els.root, "gender", state.form.gender);
    window.setButtonLoading(els.submit, state.loading, "Menyalakan api...", !state.form.date);
    if (!state.loading) els.submit.disabled = !state.form.date;
    els.empty.hidden = Boolean(data) || state.loading;
    els.loading.hidden = !state.loading;
    els.result.hidden = !data || state.loading;
    if (data) {
      Shio.roast.renderInto(els, memo, state, {
        container: els.sections,
        wrap: (section) => section.node,
        flash: els.card,
        instant: instant === true,
      });
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
      pair: Shio.roast.pairElements(root),
    };
    els.loading.appendChild(Shio.loadingBox("Menyalakan api..."));
    picker = Shio.desktopDate(els.date, {
      onChange: (dates, value) => {
        Shio.updateForm({ date: value || "" });
        render(Shio.getState());
      },
    });
    Shio.bindGender(root, () => render(Shio.getState()));
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
    memo.result = null;
    memo.draw = null;
    render(state, true);
  }

  Shio.registerRenderer("desktop", { init: init, render: render, activate: activate });
})();
