(function () {
  const Weton = window.Weton;
  const TOTAL_STEPS = 3;
  const STEP_SIDE = { 2: "a", 3: "b" };
  const FIELDS = ["nama", "tanggal", "jam", "kota"];
  let els = null;
  let step = 1;
  let activePetung = 0;

  function byId(id) {
    return document.getElementById(id);
  }

  function showError(message) {
    els.error.hidden = !message;
    els.error.textContent = message || "";
  }

  function renderLens(lens) {
    els.lensButtons.forEach((button) => {
      const on = button.dataset.lens === lens;
      button.classList.toggle("is-active", on);
      button.setAttribute("aria-checked", on ? "true" : "false");
    });
  }

  function renderSteps(state) {
    els.steps.forEach((node) => {
      node.hidden = Number(node.dataset.step) !== step;
    });
    els.progressText.textContent = "Langkah " + step + " dari " + TOTAL_STEPS;
    els.progressFill.style.width = (step / TOTAL_STEPS) * 100 + "%";
    els.back.hidden = step === 1;
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
    els.shareTop.hidden = !hasResult;
    if (hasResult) {
      renderResult(state.result);
      return;
    }
    renderSteps(state);
    showError(state.error);
  }

  async function goNext() {
    const state = Weton.getState();
    const side = STEP_SIDE[step];
    if (side && !state.form[side + "_tanggal"]) {
      showError("Isi tanggal lahir " + (side === "a" ? "orang pertama" : "orang kedua") + " dulu.");
      return;
    }
    showError("");
    if (step < TOTAL_STEPS) {
      step += 1;
      renderSteps(state);
      return;
    }
    const ok = await Weton.submit();
    if (!ok) step = 2;
    render(Weton.getState());
  }

  function init(root) {
    els = {
      root: root,
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
      shareTop: byId("m-match-share"),
      shareBottom: byId("m-match-share-bottom"),
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
        const node = byId("m-" + side + "-" + field);
        node.addEventListener("input", () => Weton.updateForm({ [side + "_" + field]: node.value }));
      });
    });
    els.next.addEventListener("click", goNext);
    els.back.addEventListener("click", () => {
      step = Math.max(1, step - 1);
      showError("");
      renderSteps(Weton.getState());
    });
    els.reset.addEventListener("click", () => {
      step = 1;
      activePetung = 0;
      Weton.reset();
    });
    const shareResult = () => {
      const result = Weton.getState().result;
      if (result) Weton.share(Weton.matchShare(result));
    };
    els.shareTop.addEventListener("click", shareResult);
    els.shareBottom.addEventListener("click", shareResult);
  }

  function activate(state) {
    ["a", "b"].forEach((side) => {
      FIELDS.forEach((field) => {
        byId("m-" + side + "-" + field).value = state.form[side + "_" + field] || "";
      });
    });
    render(state);
  }

  Weton.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
