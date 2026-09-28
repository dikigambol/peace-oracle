(function () {
  const Weton = window.Weton;
  const byId = Weton.byId;
  let els = null;
  let step = 1;

  function usesPetung(hajat) {
    const button = els.hajatButtons.find((item) => item.dataset.hajat === hajat);
    return Boolean(button) && button.dataset.petung === "true";
  }

  function totalSteps(form) {
    return usesPetung(form.hajat) ? 3 : 2;
  }

  function renderHajat(hajat) {
    els.hajatButtons.forEach((button) => {
      const on = button.dataset.hajat === hajat;
      button.classList.toggle("is-active", on);
      button.setAttribute("aria-checked", on ? "true" : "false");
    });
  }

  function renderSteps(state) {
    const total = totalSteps(state.form);
    Weton.renderStepper(els, step, total);
    renderHajat(state.form.hajat);
    els.skip.hidden = step !== 3;
    if (state.loading) {
      window.setButtonLoading(els.next, true, "Mencari hari...");
    } else {
      window.setButtonLoading(els.next, false);
      els.next.textContent = step === total ? "Cari hari baik" : "Lanjut";
    }
  }

  function render(state) {
    const result = state.result;
    els.stepsSection.hidden = Boolean(result);
    els.resultSection.hidden = !result;
    els.shareTop.hidden = !result;
    if (!result) {
      renderSteps(state);
      Weton.showError(els.error, state.error);
      return;
    }
    els.chip.textContent = result.hajat.label + " · " + result.range.days + " hari";
    els.title.textContent = Weton.dinaTitle(result);
    Weton.renderDina(els, result);
  }

  async function search() {
    const ok = await Weton.submit();
    if (!ok) step = 2;
    render(Weton.getState());
  }

  function goNext() {
    const state = Weton.getState();
    if (step === 2) {
      const message = Weton.dinaError(state.form);
      if (message) {
        Weton.showError(els.error, message);
        return;
      }
    }
    Weton.showError(els.error, "");
    if (step < totalSteps(state.form)) {
      step += 1;
      renderSteps(state);
      return;
    }
    search();
  }

  function init(root) {
    els = {
      stepsSection: byId("m-dina-steps"),
      resultSection: byId("m-dina-result"),
      steps: Array.from(root.querySelectorAll(".wt-m-step")),
      progressText: byId("m-dina-progress-text"),
      progressFill: byId("m-dina-progress-fill"),
      hajatButtons: Array.from(root.querySelectorAll("[data-hajat]")),
      error: byId("m-dina-error"),
      back: byId("m-dina-back"),
      skip: byId("m-dina-skip"),
      next: byId("m-dina-next"),
      chip: byId("m-dina-chip"),
      title: byId("m-dina-title"),
      basis: byId("m-dina-basis"),
      maghrib: byId("m-dina-maghrib"),
      sasi: byId("m-dina-sasi"),
      none: byId("m-dina-none"),
      recommended: byId("m-dina-recommended"),
      avoidWrap: byId("m-dina-avoid-wrap"),
      avoidTitle: byId("m-dina-avoid-title"),
      avoid: byId("m-dina-avoid"),
      note: byId("m-dina-note"),
      disclaimer: byId("m-dina-disclaimer"),
      reset: byId("m-dina-reset"),
      shareTop: byId("m-dina-share"),
      shareBottom: byId("m-dina-share-bottom"),
      fields: {
        dari: byId("m-dina-dari"),
        sampai: byId("m-dina-sampai"),
        a_tanggal: byId("m-a-tanggal"),
        a_jam: byId("m-a-jam"),
        a_kota: byId("m-a-kota"),
      },
    };
    Weton.dinaDefaults(root.closest("#wt-app"));
    Weton.bindInputs(els.fields);
    els.hajatButtons.forEach((button) => {
      button.addEventListener("click", () => {
        Weton.updateForm({ hajat: button.dataset.hajat });
        renderSteps(Weton.getState());
      });
    });
    els.next.addEventListener("click", goNext);
    els.back.addEventListener("click", () => {
      step = Math.max(1, step - 1);
      Weton.showError(els.error, "");
      renderSteps(Weton.getState());
    });
    els.skip.addEventListener("click", () => {
      Weton.updateForm({ a_tanggal: "", a_jam: "", a_kota: "" });
      Weton.syncInputs(els.fields, Weton.getState().form);
      search();
    });
    els.reset.addEventListener("click", () => {
      step = 1;
      Weton.reset();
    });
    Weton.bindShare([els.shareTop, els.shareBottom], Weton.dinaShare);
  }

  function activate(state) {
    Weton.syncInputs(els.fields, state.form);
    render(state);
  }

  Weton.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
