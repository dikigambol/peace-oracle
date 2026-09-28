(function () {
  const Weton = window.Weton;
  const byId = Weton.byId;
  const DATE_FIELDS = { dari: "d-dina-dari", sampai: "d-dina-sampai", a_tanggal: "d-a-tanggal" };
  let els = null;
  const pickers = {};

  function renderPerson(hajat) {
    const radio = byId("d-hajat-" + hajat);
    els.person.hidden = !radio || radio.dataset.petung !== "true";
  }

  function render(state) {
    window.setButtonLoading(els.submit, state.loading, "Mencari hari...");
    Weton.showError(els.error, state.error);
    const result = state.result;
    els.empty.hidden = Boolean(result);
    els.result.hidden = !result;
    if (!result) return;
    els.meta.textContent = result.hajat.label + " · " + result.range.label;
    els.title.textContent = Weton.dinaTitle(result);
    Weton.renderDina(els, result);
  }

  function init(root) {
    els = {
      form: byId("d-dina-form"),
      submit: byId("d-dina-submit"),
      error: byId("d-dina-error"),
      person: byId("d-dina-person"),
      empty: byId("d-dina-empty"),
      result: byId("d-dina-result"),
      meta: byId("d-dina-meta"),
      title: byId("d-dina-title"),
      share: byId("d-dina-share"),
      basis: byId("d-dina-basis"),
      maghrib: byId("d-dina-maghrib"),
      sasi: byId("d-dina-sasi"),
      none: byId("d-dina-none"),
      recommended: byId("d-dina-recommended"),
      avoidWrap: byId("d-dina-avoid-wrap"),
      avoidTitle: byId("d-dina-avoid-title"),
      avoid: byId("d-dina-avoid"),
      note: byId("d-dina-note"),
      disclaimer: byId("d-dina-disclaimer"),
      fields: { a_jam: byId("d-a-jam"), a_kota: byId("d-a-kota") },
    };
    Weton.dinaDefaults(root.closest("#wt-app"));
    Object.entries(DATE_FIELDS).forEach(([key, id]) => {
      pickers[key] = Weton.initDate(byId(id), (str) => Weton.updateForm({ [key]: str }));
    });
    Weton.bindInputs(els.fields);
    root.querySelectorAll('input[name="d-hajat"]').forEach((radio) => {
      radio.addEventListener("change", () => {
        if (!radio.checked) return;
        Weton.updateForm({ hajat: radio.value });
        renderPerson(radio.value);
      });
    });
    els.form.addEventListener("submit", (event) => {
      event.preventDefault();
      const message = Weton.dinaError(Weton.getState().form);
      if (message) {
        Weton.showError(els.error, message);
        return;
      }
      Weton.submit();
    });
    Weton.bindShare([els.share], Weton.dinaShare);
  }

  function activate(state) {
    Object.entries(DATE_FIELDS).forEach(([key, id]) => {
      Weton.syncPicker(pickers[key], byId(id), state.form[key]);
    });
    Weton.syncInputs(els.fields, state.form);
    const radio = byId("d-hajat-" + state.form.hajat);
    if (radio) radio.checked = true;
    renderPerson(state.form.hajat);
    render(state);
  }

  Weton.registerRenderer("desktop", { init: init, render: render, activate: activate });
})();
