(function () {
  const Weton = window.Weton;
  const byId = Weton.byId;
  const SIDES = ["a", "b"];
  const TEXT_FIELDS = ["nama", "jam", "kota"];
  let els = null;
  const pickers = {};

  function sideFields() {
    const fields = {};
    SIDES.forEach((side) => {
      TEXT_FIELDS.forEach((field) => {
        fields[side + "_" + field] = byId("d-" + side + "-" + field);
      });
    });
    return fields;
  }

  function renderResult(result) {
    els.result.hidden = !result;
    if (!result) return;
    Weton.clear(els.duo);
    els.duo.appendChild(Weton.renderDuo(result));
    els.origin.hidden = !result.lens.origin_note;
    els.origin.textContent = result.lens.origin_note;
    Weton.clear(els.rows);
    Weton.clear(els.cards);
    result.petung.forEach((item) => {
      const row = document.createElement("tr");
      [item.name, item.formula].forEach((text) => row.appendChild(Weton.el("td", null, text)));
      const outcome = Weton.el("td");
      outcome.appendChild(Weton.el("strong", null, item.result.name));
      outcome.appendChild(Weton.el("span", "wt-tone wt-tone-" + item.result.tone, item.result.tone_label));
      row.appendChild(outcome);
      row.appendChild(Weton.el("td", "wt-table-source", item.source));
      els.rows.appendChild(row);
      els.cards.appendChild(Weton.renderPetungCard(item));
    });
    els.disclaimer.textContent = result.disclaimer;
  }

  function render(state) {
    window.setButtonLoading(els.submit, state.loading, "Menghitung petung...");
    Weton.showError(els.error, state.error);
    renderResult(state.result);
  }

  function init(root) {
    els = {
      root: root,
      form: byId("d-match-form"),
      submit: byId("d-match-submit"),
      error: byId("d-match-error"),
      result: byId("d-match-result"),
      duo: byId("d-duo"),
      origin: byId("d-origin"),
      rows: byId("d-petung-rows"),
      cards: byId("d-petung-cards"),
      disclaimer: byId("d-disclaimer"),
      fields: sideFields(),
    };
    SIDES.forEach((side) => {
      pickers[side] = Weton.initDate(byId("d-" + side + "-tanggal"), (str) => Weton.updateForm({ [side + "_tanggal"]: str }));
    });
    Weton.bindInputs(els.fields);
    root.querySelectorAll('input[name="d-lens"]').forEach((radio) => {
      radio.addEventListener("change", () => {
        if (radio.checked) Weton.updateForm({ lens: radio.value });
      });
    });
    if (!Weton.getState().form.lens) Weton.updateForm({ lens: root.closest("#wt-app").dataset.defaultLens });
    els.form.addEventListener("submit", (event) => {
      event.preventDefault();
      const form = Weton.getState().form;
      const missing = SIDES.find((side) => !form[side + "_tanggal"]);
      if (missing) {
        Weton.showError(els.error, "Isi tanggal lahir " + (missing === "a" ? "orang pertama" : "orang kedua") + " dulu.");
        return;
      }
      Weton.submit();
    });
  }

  function activate(state) {
    SIDES.forEach((side) => {
      Weton.syncPicker(pickers[side], byId("d-" + side + "-tanggal"), state.form[side + "_tanggal"]);
    });
    Weton.syncInputs(els.fields, state.form);
    const lens = state.form.lens || els.root.closest("#wt-app").dataset.defaultLens;
    const radio = byId("d-lens-" + lens);
    if (radio) radio.checked = true;
    render(state);
  }

  Weton.registerRenderer("desktop", { init: init, render: render, activate: activate });
})();
