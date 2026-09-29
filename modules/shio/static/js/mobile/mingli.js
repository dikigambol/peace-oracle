(function () {
  const Shio = window.Shio;
  const byId = Shio.byId;
  const TOTAL_STEPS = 3;
  let els = null;
  let step = 1;
  let renderedResult = null;

  function renderSteps(state) {
    Shio.renderStepper(els, step, TOTAL_STEPS);
    els.date.value = state.form.date || "";
    els.city.value = state.form.city || "";
    Shio.markChoice(els.root, "gender", state.form.gender);
    Shio.destiny.syncTimeFields(els.time, state.form);
    if (state.loading) {
      window.setButtonLoading(els.next, true, "Membuka gulungan...");
    } else {
      window.setButtonLoading(els.next, false);
      els.next.textContent = step === TOTAL_STEPS ? "Buka gulungan" : "Lanjut";
    }
  }

  function buildDetails(section, open) {
    const details = Shio.detailsBlock(section.title, section.icon, section.build(), open, "sh-m-destiny-section");
    if (section.key === "chart") {
      details.addEventListener("toggle", () => Shio.destiny.refreshChartHints(details));
    }
    return details;
  }

  function renderResult(data) {
    if (data === renderedResult) return;
    els.chip.textContent = Shio.destiny.summary(data);
    Shio.clear(els.notices);
    els.notices.appendChild(Shio.destiny.buildNotices(data.meta, data.no_birth_time));
    Shio.clear(els.sections);
    Shio.destiny.sections(data).forEach((section, index) => els.sections.appendChild(buildDetails(section, index === 0)));
    els.disclaimer.textContent = data.meta.disclaimer || "";
    Shio.destiny.refreshChartHints(els.sections);
    renderedResult = data;
  }

  function render(state) {
    const data = state.result;
    const viewing = Boolean(data) || state.loading;
    els.stepsSection.hidden = viewing;
    els.loading.hidden = !state.loading;
    els.result.hidden = !data || state.loading;
    els.home.hidden = viewing;
    els.edit.hidden = !viewing;
    if (data) {
      renderResult(data);
      return;
    }
    renderedResult = null;
    if (!state.loading) renderSteps(state);
  }

  function validate(form) {
    if (step !== 1) return "";
    if (!form.date) return "Isi tanggal lahir dulu.";
    if (!form.gender) return "Pilih jenis kelamin dulu.";
    return "";
  }

  async function goNext() {
    const state = Shio.getState();
    const problem = validate(state.form);
    Shio.showError(els.error, problem);
    if (problem) return;
    if (step < TOTAL_STEPS) {
      step += 1;
      renderSteps(state);
      return;
    }
    window.scrollTo(0, 0);
    const data = await Shio.destiny.submit();
    if (data) Shio.showResult(els.result);
  }

  function backToForm() {
    if (Shio.getState().loading) return;
    step = 1;
    Shio.setState({ result: null });
    window.scrollTo(0, 0);
  }

  function init(root) {
    els = {
      root: root,
      home: byId("m-destiny-home"),
      edit: byId("m-destiny-edit"),
      stepsSection: byId("m-destiny-steps"),
      steps: Array.from(root.querySelectorAll(".sh-m-step")),
      progressText: byId("m-destiny-progress-text"),
      progressFill: byId("m-destiny-progress-fill"),
      date: byId("m-destiny-date"),
      time: byId("m-destiny-time"),
      city: byId("m-destiny-city"),
      error: byId("m-destiny-error"),
      back: byId("m-destiny-back"),
      next: byId("m-destiny-next"),
      loading: byId("m-destiny-loading"),
      result: byId("m-destiny-result"),
      chip: byId("m-destiny-chip"),
      notices: byId("m-destiny-notices"),
      sections: byId("m-destiny-sections"),
      disclaimer: byId("m-destiny-disclaimer"),
    };
    els.loading.appendChild(Shio.loadingBox("Membuka gulungan..."));
    Shio.mobileDate(els.date, (value) => {
      Shio.updateForm({ date: value });
      Shio.showError(els.error, "");
    });
    Shio.bindGender(root, () => {
      Shio.markChoice(root, "gender", Shio.getState().form.gender);
      Shio.showError(els.error, "");
    });
    Shio.destiny.bindTimeFields(els.time, () => Shio.destiny.syncTimeFields(els.time, Shio.getState().form));
    els.city.addEventListener("input", () => Shio.updateForm({ city: els.city.value }));
    els.next.addEventListener("click", goNext);
    els.back.addEventListener("click", () => {
      step = Math.max(1, step - 1);
      Shio.showError(els.error, "");
      renderSteps(Shio.getState());
    });
    els.edit.addEventListener("click", backToForm);
    byId("m-destiny-reset").addEventListener("click", backToForm);
  }

  function activate(state) {
    renderedResult = null;
    render(state);
  }

  Shio.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
