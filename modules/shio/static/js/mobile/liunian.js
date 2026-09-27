(function () {
  const Shio = window.Shio;
  const TOTAL_STEPS = 2;
  let els = null;
  let step = 1;
  let activeCategory = 0;
  let renderedResult = null;

  function byId(id) {
    return document.getElementById(id);
  }

  function showError(message) {
    els.error.hidden = !message;
    els.error.textContent = message || "";
  }

  function renderSteps(state) {
    els.steps.forEach((node) => {
      node.hidden = Number(node.dataset.step) !== step;
    });
    els.progressText.textContent = "Langkah " + step + " dari " + TOTAL_STEPS;
    els.progressFill.style.width = (step / TOTAL_STEPS) * 100 + "%";
    els.back.hidden = step === 1;
    Shio.shio.markPicked(els.root, state.form.shio);
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
        showError("Pilih shio kamu dulu.");
        return;
      }
      showError("");
      step = 2;
      renderSteps(state);
      return;
    }
    activeCategory = 0;
    const data = await Shio.yearly.submit();
    if (data) window.scrollTo(0, 0);
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
        showError("");
        renderSteps(Shio.getState());
      });
    });
    byId("m-year-prev").addEventListener("click", () => {
      Shio.updateForm({ year: Shio.getState().form.year - 1 });
      renderSteps(Shio.getState());
    });
    byId("m-year-next").addEventListener("click", () => {
      Shio.updateForm({ year: Shio.getState().form.year + 1 });
      renderSteps(Shio.getState());
    });
    els.next.addEventListener("click", goNext);
    els.back.addEventListener("click", () => {
      step = 1;
      showError("");
      renderSteps(Shio.getState());
    });
    byId("m-yearly-reset").addEventListener("click", () => {
      step = 1;
      Shio.setState({ result: null });
    });
    byId("m-yearly-share").addEventListener("click", () => {
      const data = Shio.getState().result;
      if (!data) return;
      const relation = data.relation || {};
      Shio.share({
        title: "Liu Nian " + (data.year || ""),
        text: "Shio " + (data.user_shio || {}).name + " di Tahun " + (data.year_shio || {}).name + " " + data.year +
          ": " + (relation.name_id || relation.label || "") + ". Cek proyeksi tahunanmu di Peace Oracle.",
      });
    });
  }

  function activate(state) {
    renderedResult = null;
    render(state);
  }

  Shio.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
