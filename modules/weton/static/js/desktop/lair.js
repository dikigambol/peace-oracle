(function () {
  const Weton = window.Weton;
  const byId = Weton.byId;
  let els = null;
  let picker = null;

  function renderResult(result) {
    Weton.clear(els.cards);
    const hasResult = Boolean(result);
    els.empty.hidden = hasResult;
    els.note.hidden = !hasResult;
    els.sources.hidden = !hasResult;
    if (!hasResult) return;
    els.note.textContent = result.maghrib.text;
    els.note.dataset.kind = result.maghrib.kind;
    Weton.buildLahirCards(result).forEach((card) => {
      els.cards.appendChild(Weton.renderCard(card, "desktop"));
    });
    els.sources.textContent = Weton.describeSources(result);
  }

  function render(state) {
    window.setButtonLoading(els.submit, state.loading, "Menghitung weton...");
    Weton.showError(els.error, state.error);
    renderResult(state.result);
  }

  function init(root) {
    els = {
      form: byId("d-form"),
      result: byId("d-result"),
      tanggal: byId("d-tanggal"),
      fields: { jam: byId("d-jam"), kota: byId("d-kota") },
      submit: byId("d-submit"),
      error: byId("d-error"),
      empty: byId("d-empty"),
      note: byId("d-note"),
      cards: byId("d-cards"),
      sources: byId("d-sources"),
    };
    picker = Weton.initDate(els.tanggal, (str) => Weton.updateForm({ tanggal: str }));
    Weton.bindInputs(els.fields);
    els.form.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (!Weton.getState().form.tanggal) {
        Weton.showError(els.error, "Isi tanggal lahirmu dulu.");
        return;
      }
      if (await Weton.submit()) Weton.showResult(els.result);
    });
  }

  function activate(state) {
    Weton.syncPicker(picker, els.tanggal, state.form.tanggal);
    Weton.syncInputs(els.fields, state.form);
    render(state);
  }

  Weton.registerRenderer("desktop", { init: init, render: render, activate: activate });
})();
