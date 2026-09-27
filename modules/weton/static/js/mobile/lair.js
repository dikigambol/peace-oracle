(function () {
  const Weton = window.Weton;
  const TOTAL_STEPS = 3;
  const FIELDS = { 1: "tanggal", 2: "jam", 3: "kota" };
  let els = null;
  let step = 1;

  function byId(id) {
    return document.getElementById(id);
  }

  function input(stepNumber) {
    return els.inputs[FIELDS[stepNumber]];
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
    els.skip.hidden = step === 1;
    const label = step === TOTAL_STEPS ? "Lihat wetonku" : "Lanjut";
    if (state.loading) {
      window.setButtonLoading(els.next, true, "Menghitung weton...");
    } else {
      window.setButtonLoading(els.next, false);
      els.next.textContent = label;
    }
  }

  function updateDots() {
    const cards = els.cards.children;
    if (!cards.length) return;
    const width = els.cards.clientWidth || 1;
    const index = Math.round(els.cards.scrollLeft / width);
    Array.from(els.dots.children).forEach((dot, position) => {
      const on = position === index;
      dot.classList.toggle("is-active", on);
      dot.setAttribute("aria-current", on ? "true" : "false");
    });
  }

  function renderResult(result) {
    Weton.clear(els.cards);
    Weton.clear(els.dots);
    const cards = Weton.buildLahirCards(result);
    cards.forEach((card, index) => {
      const node = Weton.renderCard(card, "mobile");
      node.setAttribute("aria-roledescription", "slide");
      node.setAttribute("aria-label", index + 1 + " dari " + cards.length + ": " + card.title);
      if (index === 0) {
        const banner = Weton.el("p", "wt-note wt-note-inline", result.maghrib.text);
        banner.dataset.kind = result.maghrib.kind;
        node.insertBefore(banner, node.children[1]);
      }
      els.cards.appendChild(node);
      const dot = Weton.el("button", "wt-m-dot");
      dot.type = "button";
      dot.setAttribute("aria-label", "Buka kartu " + card.title);
      dot.addEventListener("click", () => {
        els.cards.scrollTo({ left: index * els.cards.clientWidth, behavior: "smooth" });
      });
      els.dots.appendChild(dot);
    });
    els.chip.textContent = result.weton.label + " · Neptu " + result.weton.neptu;
    els.sources.textContent = Weton.describeSources(result);
    els.cards.scrollLeft = 0;
    updateDots();
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
    if (step === 1 && !state.form.tanggal) {
      showError("Isi tanggal lahirmu dulu.");
      return;
    }
    showError("");
    if (step < TOTAL_STEPS) {
      step += 1;
      renderSteps(state);
      input(step).focus();
      return;
    }
    const ok = await Weton.submit();
    if (!ok) step = 1;
    render(Weton.getState());
  }

  function init(root) {
    els = {
      root: root,
      stepsSection: byId("m-steps"),
      resultSection: byId("m-result"),
      steps: Array.from(root.querySelectorAll(".wt-m-step")),
      progressText: byId("m-progress-text"),
      progressFill: byId("m-progress-fill"),
      inputs: { tanggal: byId("m-tanggal"), jam: byId("m-jam"), kota: byId("m-kota") },
      error: byId("m-error"),
      back: byId("m-back"),
      skip: byId("m-skip"),
      next: byId("m-next"),
      chip: byId("m-chip"),
      cards: byId("m-cards"),
      dots: byId("m-dots"),
      sources: byId("m-sources"),
      reset: byId("m-reset"),
      shareTop: byId("m-share"),
      shareBottom: byId("m-share-bottom"),
    };
    Object.entries(els.inputs).forEach(([field, node]) => {
      node.addEventListener("input", () => Weton.updateForm({ [field]: node.value }));
      node.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          event.preventDefault();
          goNext();
        }
      });
    });
    els.next.addEventListener("click", goNext);
    els.back.addEventListener("click", () => {
      step = Math.max(1, step - 1);
      showError("");
      renderSteps(Weton.getState());
    });
    els.skip.addEventListener("click", () => {
      input(step).value = "";
      Weton.updateForm({ [FIELDS[step]]: "" });
      goNext();
    });
    els.reset.addEventListener("click", () => {
      step = 1;
      Weton.reset();
    });
    const shareResult = () => {
      const result = Weton.getState().result;
      if (result) Weton.share(Weton.lahirShare(result));
    };
    els.shareTop.addEventListener("click", shareResult);
    els.shareBottom.addEventListener("click", shareResult);
    let frame = null;
    els.cards.addEventListener("scroll", () => {
      if (frame) cancelAnimationFrame(frame);
      frame = requestAnimationFrame(updateDots);
    });
  }

  function activate(state) {
    Object.entries(els.inputs).forEach(([field, node]) => {
      node.value = state.form[field] || "";
    });
    render(state);
  }

  Weton.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
