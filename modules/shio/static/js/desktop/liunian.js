(function () {
  const Shio = window.Shio;
  const byId = Shio.byId;
  let els = null;
  let renderedResult = null;

  function renderYear(state) {
    const year = state.form.year;
    els.yearNumber.textContent = year;
    els.yearShio.textContent = Shio.yearly.describeYear(year);
  }

  function renderResult(state) {
    const data = state.result;
    els.empty.hidden = Boolean(data);
    els.result.hidden = !data;
    if (!data || data === renderedResult) return;
    Shio.clear(els.result);
    els.result.appendChild(Shio.yearly.buildSummary(data));
    els.result.appendChild(Shio.yearly.buildCategories(data));
    if (data.lichun_note) els.lichun.textContent = data.lichun_note;
    renderedResult = data;
  }

  function render(state) {
    Shio.markChoice(els.root, "shio", state.form.shio);
    renderYear(state);
    window.setButtonLoading(els.submit, state.loading, "Meneropong tahun...", !state.form.shio);
    if (!state.loading) els.submit.disabled = !state.form.shio;
    renderResult(state);
  }

  function init(root) {
    els = {
      root: root,
      yearNumber: byId("d-year-number"),
      yearShio: byId("d-year-shio"),
      lichun: byId("d-lichun"),
      submit: byId("d-yearly-submit"),
      empty: byId("d-yearly-empty"),
      result: byId("d-yearly-result"),
    };
    root.querySelectorAll("[data-shio]").forEach((button) => {
      button.addEventListener("click", () => {
        Shio.updateForm({ shio: button.dataset.shio });
        render(Shio.getState());
      });
    });
    Shio.yearly.bindYearButtons("d", renderYear);
    els.submit.addEventListener("click", async () => {
      const data = await Shio.yearly.submit();
      if (data) Shio.scrollIntoView(els.result);
    });
  }

  function activate(state) {
    renderedResult = null;
    render(state);
  }

  Shio.registerRenderer("desktop", { init: init, render: render, activate: activate });
})();
