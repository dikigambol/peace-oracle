(function () {
  const Shio = window.Shio;
  const byId = Shio.byId;
  const TOTAL_STEPS = 2;
  let els = null;
  let step = 1;
  let activeCategory = 0;
  let renderedResult = null;

  function renderSteps(state) {
    Shio.renderStepper(els, step, TOTAL_STEPS);
    Shio.markChoice(els.root, "shio", state.form.shio);
    els.yearNumber.textContent = state.form.year;
    els.yearShio.textContent = Shio.yearly.describeYear(state.form.year);
    if (state.loading) {
      window.setButtonLoading(els.next, true, "Meneropong tahun...");
    } else {
      window.setButtonLoading(els.next, false);
      els.next.textContent = step === TOTAL_STEPS ? "Lihat proyeksi" : "Lanjut";
    }
  }

  function renderCategory(data) {
    const items = Shio.yearly.categories(data);
    Array.from(els.segment.children).forEach((button, index) => {
      const on = index === activeCategory;
      button.classList.toggle("is-active", on);
      button.setAttribute("aria-selected", on ? "true" : "false");
    });
    Shio.clear(els.panel);
    els.panel.appendChild(Shio.yearly.buildCategory(items[activeCategory]));
  }

  function renderResult(data) {
    if (data === renderedResult) return;
    const user = data.user_shio || {};
    const year = data.year_shio || {};
    els.chip.textContent = (user.name || "") + " di Tahun " + (year.name || "") + " " + (data.year || "");
    Shio.clear(els.summary);
    els.summary.appendChild(Shio.yearly.buildSummary(data));
    Shio.clear(els.segment);
    Shio.yearly.categories(data).forEach((item, index) => {
      const button = Shio.el("button", "sh-m-segment-option", item.label);
      button.type = "button";
      button.setAttribute("role", "tab");
      button.addEventListener("click", () => {
        activeCategory = index;
        renderCategory(data);
      });
      els.segment.appendChild(button);
    });
    renderCategory(data);
    renderedResult = data;
  }

  function render(state) {
    const hasResult = Boolean(state.result);
    els.stepsSection.hidden = hasResult;
    els.resultSection.hidden = !hasResult;
    if (hasResult) {
      renderResult(state.result);
      return;
    }
    renderedResult = null;
    renderSteps(state);
  }

  async function goNext() {
    const state = Shio.getState();
    if (step === 1) {
      if (!state.form.shio) {
        Shio.showError(els.error, "Pilih shio kamu dulu.");
        return;
      }
      Shio.showError(els.error, "");
      step = 2;
      renderSteps(state);
      return;
    }
    activeCategory = 0;
    const data = await Shio.yearly.submit();
    if (data) Shio.showResult(els.resultSection);
  }

  function init(root) {
    els = {
      root: root,
      stepsSection: byId("m-yearly-steps"),
      resultSection: byId("m-yearly-result"),
      steps: Array.from(root.querySelectorAll(".sh-m-step")),
      progressText: byId("m-yearly-progress-text"),
      progressFill: byId("m-yearly-progress-fill"),
      yearNumber: byId("m-year-number"),
      yearShio: byId("m-year-shio"),
      error: byId("m-yearly-error"),
      back: byId("m-yearly-back"),
      next: byId("m-yearly-next"),
      chip: byId("m-yearly-chip"),
      summary: byId("m-yearly-summary"),
      segment: byId("m-yearly-segment"),
      panel: byId("m-yearly-panel"),
    };
    root.querySelectorAll("[data-shio]").forEach((button) => {
      button.addEventListener("click", () => {
        Shio.updateForm({ shio: button.dataset.shio });
        Shio.showError(els.error, "");
        renderSteps(Shio.getState());
      });
    });
    Shio.yearly.bindYearButtons("m", renderSteps);
    els.next.addEventListener("click", goNext);
    els.back.addEventListener("click", () => {
      step = 1;
      Shio.showError(els.error, "");
      renderSteps(Shio.getState());
    });
    byId("m-yearly-reset").addEventListener("click", () => {
      step = 1;
      Shio.setState({ result: null });
    });
  }

  function activate(state) {
    renderedResult = null;
    render(state);
  }

  Shio.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
