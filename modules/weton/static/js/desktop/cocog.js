(function () {
  const Weton = window.Weton;
  const SIDES = ["a", "b"];
  const TEXT_FIELDS = ["nama", "jam", "kota"];
  let els = null;
  const pickers = {};

  function byId(id) {
    return document.getElementById(id);
  }

  function syncInputs(form) {
    SIDES.forEach((side) => {
      const value = form[side + "_tanggal"] || "";
      if (pickers[side]) {
        if (value) pickers[side].setDate(value, false);
        else pickers[side].clear(false);
      } else {
        byId("d-" + side + "-tanggal").value = value;
      }
      TEXT_FIELDS.forEach((field) => {
        byId("d-" + side + "-" + field).value = form[side + "_" + field] || "";
      });
    });
    const lens = form.lens || els.root.closest("#wt-app").dataset.defaultLens;
    const radio = byId("d-lens-" + lens);
    if (radio) radio.checked = true;
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
    els.error.hidden = !state.error;
    els.error.textContent = state.error;
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
    };
    SIDES.forEach((side) => {
      const input = byId("d-" + side + "-tanggal");
      window.initDatePicker("#d-" + side + "-tanggal", {
        dateFormat: "Y-m-d",
        altInput: true,
        altFormat: "j F Y",
        locale: "id",
        minDate: input.dataset.min,
        maxDate: input.dataset.max,
        disableMobile: true,
        onChange: (dates, str) => Weton.updateForm({ [side + "_tanggal"]: str }),
      });
      pickers[side] = input._flatpickr || null;
      TEXT_FIELDS.forEach((field) => {
        const node = byId("d-" + side + "-" + field);
        node.addEventListener("input", () => Weton.updateForm({ [side + "_" + field]: node.value }));
      });
    });
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
        els.error.hidden = false;
        els.error.textContent = "Isi tanggal lahir " + (missing === "a" ? "orang pertama" : "orang kedua") + " dulu.";
        return;
      }
      Weton.submit();
    });
  }

  function activate(state) {
    syncInputs(state.form);
    render(state);
  }

  Weton.registerRenderer("desktop", { init: init, render: render, activate: activate });
})();
