(function () {
  const Shio = window.Shio;
  const byId = Shio.byId;
  const TOTAL_STEPS = 3;
  const LENS_LABEL = { asmara: "Asmara", pertemanan: "Pertemanan", kerja: "Rekan Kerja" };
  let els = null;
  let step = 1;
  let renderedResult = null;

  function renderSteps(state) {
    Shio.renderStepper(els, step, TOTAL_STEPS);
    Shio.markRadio(els.root, "lens", state.form.lens);
    els.date1.value = state.form.date1 || "";
    els.date2.value = state.form.date2 || "";
    if (state.loading) {
      window.setButtonLoading(els.next, true, "Menimbang energi...");
    } else {
      window.setButtonLoading(els.next, false);
      els.next.textContent = step === TOTAL_STEPS ? "Ukur kecocokan" : "Lanjut";
    }
  }

  function renderResult(data, instant) {
    if (data === renderedResult) return;
    const form = Shio.getState().form;
    const one = data.shio1 || {};
    const two = data.shio2 || {};
    els.chip.textContent = (one.name || "") + " × " + (two.name || "") + " · " + (LENS_LABEL[form.lens] || "");
    Shio.renderCompatLayers(els.layers, data);
    Shio.compat.renderScore(els.layers, Shio.compat.scoreOf(data), !instant);
    renderedResult = data;
  }

  function render(state, instant) {
    const hasResult = Boolean(state.result);
    els.stepsSection.hidden = hasResult;
    els.resultSection.hidden = !hasResult;
    if (hasResult) {
      renderResult(state.result, instant === true);
      return;
    }
    renderedResult = null;
    renderSteps(state);
  }

  function validate(form) {
    if (step === 2 && !form.date1) return "Isi tanggal lahir orang pertama dulu.";
    if (step === 3 && !form.date2) return "Isi tanggal lahir orang kedua dulu.";
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
    const data = await Shio.compat.submit();
    if (data) Shio.showResult(els.resultSection);
  }

  function init(root) {
    els = {
      root: root,
      stepsSection: byId("m-compat-steps"),
      resultSection: byId("m-compat-result"),
      steps: Array.from(root.querySelectorAll(".sh-m-step")),
      progressText: byId("m-compat-progress-text"),
      progressFill: byId("m-compat-progress-fill"),
      date1: byId("m-compat-date1"),
      date2: byId("m-compat-date2"),
      error: byId("m-compat-error"),
      back: byId("m-compat-back"),
      next: byId("m-compat-next"),
      chip: byId("m-compat-chip"),
      layers: byId("m-compat-layers"),
    };
    root.querySelectorAll("[data-lens]").forEach((chip) => {
      chip.addEventListener("click", () => {
        Shio.updateForm({ lens: chip.dataset.lens });
        Shio.markRadio(root, "lens", chip.dataset.lens);
      });
    });
    Shio.mobileDate(els.date1, (value) => {
      Shio.updateForm({ date1: value });
      Shio.showError(els.error, "");
    });
    Shio.mobileDate(els.date2, (value) => {
      Shio.updateForm({ date2: value });
      Shio.showError(els.error, "");
    });
    els.next.addEventListener("click", goNext);
    els.back.addEventListener("click", () => {
      step = Math.max(1, step - 1);
      Shio.showError(els.error, "");
      renderSteps(Shio.getState());
    });
    byId("m-compat-reset").addEventListener("click", () => {
      step = 1;
      Shio.setState({ result: null });
      window.scrollTo(0, 0);
    });
  }

  function activate(state) {
    renderedResult = null;
    render(state, true);
  }

  Shio.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
