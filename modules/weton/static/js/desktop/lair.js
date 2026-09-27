(function () {
  const Weton = window.Weton;
  let els = null;
  let picker = null;

  function byId(id) {
    return document.getElementById(id);
  }

  function syncInputs(form) {
    if (picker) {
      if (form.tanggal) picker.setDate(form.tanggal, false);
      else picker.clear(false);
    } else {
      els.tanggal.value = form.tanggal || "";
    }
    els.jam.value = form.jam || "";
    els.kota.value = form.kota || "";
  }

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
    els.error.hidden = !state.error;
    els.error.textContent = state.error;
    renderResult(state.result);
  }

  function init(root) {
    els = {
      root: root,
      form: byId("d-form"),
      tanggal: byId("d-tanggal"),
      jam: byId("d-jam"),
      kota: byId("d-kota"),
      submit: byId("d-submit"),
      error: byId("d-error"),
      empty: byId("d-empty"),
      note: byId("d-note"),
      cards: byId("d-cards"),
      sources: byId("d-sources"),
    };
    window.initDatePicker("#d-tanggal", {
      dateFormat: "Y-m-d",
      altInput: true,
      altFormat: "j F Y",
      locale: "id",
      minDate: els.tanggal.dataset.min,
      maxDate: els.tanggal.dataset.max,
      disableMobile: true,
      onChange: (dates, str) => Weton.updateForm({ tanggal: str }),
    });
    picker = els.tanggal._flatpickr || null;
    els.jam.addEventListener("input", () => Weton.updateForm({ jam: els.jam.value }));
    els.kota.addEventListener("input", () => Weton.updateForm({ kota: els.kota.value }));
    els.form.addEventListener("submit", (event) => {
      event.preventDefault();
      if (!Weton.getState().form.tanggal) {
        els.error.hidden = false;
        els.error.textContent = "Isi tanggal lahirmu dulu.";
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
