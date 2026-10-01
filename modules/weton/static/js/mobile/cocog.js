(function () {
  const Weton = window.Weton;
  const byId = Weton.byId;
  const TOTAL_STEPS = 3;
  const STEP_SIDE = { 2: "a", 3: "b" };
  const FIELDS = ["nama", "tanggal", "jam", "kota"];
  let els = null;
  let step = 1;
  let activePetung = 0;

  function renderLens(lens) {
    els.lensButtons.forEach((button) => {
      const on = button.dataset.lens === lens;
      button.classList.toggle("is-active", on);
      button.setAttribute("aria-checked", on ? "true" : "false");
    });
  }

  function renderSteps(state) {
    Weton.renderStepper(els, step, TOTAL_STEPS);
    renderLens(state.form.lens);
    if (state.loading) {
      window.setButtonLoading(els.next, true, "Menghitung petung...");
    } else {
      window.setButtonLoading(els.next, false);
      els.next.textContent = step === TOTAL_STEPS ? "Lihat kecocokan" : "Lanjut";
    }
  }

  function renderPanel(result) {
    Weton.clear(els.panel);
    els.panel.appendChild(Weton.renderPetungCard(result.petung[activePetung]));
    Array.from(els.segment.children).forEach((button, index) => {
      const on = index === activePetung;
      button.classList.toggle("is-active", on);
      button.setAttribute("aria-selected", on ? "true" : "false");
      button.tabIndex = on ? 0 : -1;
    });
  }

  function renderResult(result) {
    els.chip.textContent = result.people.map((person) => person.weton.label).join(" × ") +
      " · Neptu " + result.total_neptu;
    Weton.clear(els.duo);
    els.duo.appendChild(Weton.renderDuo(result));
    els.origin.hidden = !result.lens.origin_note;
    els.origin.textContent = result.lens.origin_note;
    Weton.clear(els.segment);
    activePetung = Math.min(activePetung, result.petung.length - 1);
    result.petung.forEach((item, index) => {
      const button = Weton.el("button", "wt-m-segment-option");
      button.type = "button";
      button.setAttribute("role", "tab");
      button.appendChild(Weton.el("span", "wt-m-segment-name", item.name.replace("Petung ", "")));
      button.appendChild(Weton.el("span", "wt-m-segment-result", item.result.name));
      button.addEventListener("click", () => {
        activePetung = index;
        renderPanel(result);
      });
      els.segment.appendChild(button);
    });
    renderPanel(result);
    els.disclaimer.textContent = result.disclaimer;
  }

  function render(state) {
    const hasResult = Boolean(state.result);
    els.stepsSection.hidden = hasResult;
    els.resultSection.hidden = !hasResult;
    if (hasResult) {
      renderResult(state.result);
      return;
    }
    renderSteps(state);
    Weton.showError(els.error, state.error);
  }

  async function goNext() {
    const state = Weton.getState();
    const side = STEP_SIDE[step];
    if (side && !state.form[side + "_tanggal"]) {
      Weton.showError(els.error, "Isi tanggal lahir " + (side === "a" ? "orang pertama" : "orang kedua") + " dulu.");
      return;
    }
    Weton.showError(els.error, "");
    if (step < TOTAL_STEPS) {
      step += 1;
      renderSteps(state);
      return;
    }
    const ok = await Weton.submit();
    if (!ok) step = 2;
    render(Weton.getState());
    if (ok) Weton.showResult(els.resultSection);
  }

  function init(root) {
    els = {
      stepsSection: byId("m-match-steps"),
      resultSection: byId("m-match-result"),
      steps: Array.from(root.querySelectorAll(".wt-m-step")),
      progressText: byId("m-match-progress-text"),
      progressFill: byId("m-match-progress-fill"),
      lensButtons: Array.from(root.querySelectorAll("[data-lens]")),
      error: byId("m-match-error"),
      back: byId("m-match-back"),
      next: byId("m-match-next"),
      chip: byId("m-match-chip"),
      duo: byId("m-duo"),
      origin: byId("m-origin"),
      segment: byId("m-segment"),
      panel: byId("m-petung-panel"),
      disclaimer: byId("m-disclaimer"),
      reset: byId("m-match-reset"),
      fields: {},
    };
    if (!Weton.getState().form.lens) Weton.updateForm({ lens: root.closest("#wt-app").dataset.defaultLens });
    els.lensButtons.forEach((button) => {
      button.addEventListener("click", () => {
        Weton.updateForm({ lens: button.dataset.lens });
        renderLens(button.dataset.lens);
      });
    });
    ["a", "b"].forEach((side) => {
      FIELDS.forEach((field) => {
        els.fields[side + "_" + field] = byId("m-" + side + "-" + field);
      });
    });
    Weton.bindInputs(els.fields);
    els.next.addEventListener("click", goNext);
    els.back.addEventListener("click", () => {
      step = Math.max(1, step - 1);
      Weton.showError(els.error, "");
      renderSteps(Weton.getState());
    });
    els.reset.addEventListener("click", () => {
      step = 1;
      activePetung = 0;
      Weton.reset();
    });
  }

  function activate(state) {
    Weton.syncInputs(els.fields, state.form);
    render(state);
  }

  Weton.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
