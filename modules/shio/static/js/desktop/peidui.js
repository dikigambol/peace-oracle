(function () {
  const Shio = window.Shio;
  const byId = Shio.byId;
  let els = null;
  let pickers = {};
  let renderedResult = null;

  function ready(form) {
    return Boolean(form.date1 && form.date2);
  }

  function render(state, instant) {
    const data = state.result;
    Shio.markRadio(els.root, "lens", state.form.lens);
    window.setButtonLoading(els.submit, state.loading, "Menimbang energi...", !ready(state.form));
    if (!state.loading) els.submit.disabled = !ready(state.form);
    els.empty.hidden = Boolean(data);
    els.result.hidden = !data;
    if (!data || data === renderedResult) return;
    const animate = instant !== true;
    Shio.renderCompatLayers(els.result, data);
    Shio.compat.renderScore(els.result, Shio.compat.scoreOf(data), animate);
    if (animate) Shio.replay(els.result, "animate-in");
    else els.result.classList.remove("animate-in");
    renderedResult = data;
  }

  async function submit() {
    const data = await Shio.compat.submit();
    if (data) setTimeout(() => Shio.showResult(els.result), 200);
  }

  function setupDate(key) {
    const input = byId("d-compat-" + key);
    pickers[key] = Shio.desktopDate(input, {
      onChange: (dates, value) => {
        Shio.updateForm({ [key]: value || "" });
        render(Shio.getState());
      },
    });
  }

  function init(root) {
    els = {
      root: root,
      submit: byId("d-compat-submit"),
      empty: byId("d-compat-empty"),
      result: byId("d-compat-result"),
    };
    setupDate("date1");
    setupDate("date2");
    root.querySelectorAll("[data-lens]").forEach((chip) => {
      chip.addEventListener("click", () => {
        const state = Shio.getState();
        if (state.form.lens === chip.dataset.lens || state.loading) return;
        Shio.updateForm({ lens: chip.dataset.lens });
        render(Shio.getState());
        if (state.result && state.submitted) Shio.compat.submit(Object.assign({}, state.submitted, { lens: chip.dataset.lens }));
      });
    });
    els.submit.addEventListener("click", submit);
  }

  function syncForm(state) {
    Shio.setDesktopDate(pickers.date1, byId("d-compat-date1"), state.form.date1);
    Shio.setDesktopDate(pickers.date2, byId("d-compat-date2"), state.form.date2);
  }

  function activate(state) {
    syncForm(state);
    renderedResult = null;
    render(state, true);
  }

  Shio.registerRenderer("desktop", { init: init, render: render, activate: activate, syncForm: syncForm });
})();
