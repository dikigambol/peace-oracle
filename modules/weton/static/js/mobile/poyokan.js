(function () {
  const Weton = window.Weton;
  const byId = Weton.byId;
  const FIELDS = { a: ["tanggal", "jam", "kota"], b: ["nama", "tanggal", "jam", "kota"] };
  const SWIPE_DISTANCE = 40;
  let els = null;
  let slides = [];
  let current = 0;
  let renderedResult = null;
  let touchStart = null;

  function renderSlide() {
    const slide = slides[current];
    if (!slide) return;
    els.card.dataset.group = slide.group;
    els.label.textContent = slide.label;
    els.text.textContent = slide.text;
    els.count.textContent = current + 1 + " / " + slides.length;
    Array.from(els.bars.children).forEach((bar, index) => {
      bar.classList.toggle("is-done", index < current);
      bar.classList.toggle("is-active", index === current);
    });
    els.prev.disabled = current === 0;
    els.next.disabled = current === slides.length - 1;
  }

  function renderStory(result) {
    if (result !== renderedResult) {
      slides = Weton.roastSlides(result);
      current = Math.min(current, slides.length - 1);
      Weton.clear(els.bars);
      slides.forEach((slide) => els.bars.appendChild(Weton.el("span", "wt-m-story-bar wt-m-story-bar-" + slide.group)));
      renderedResult = result;
    }
    const weton = result.person.weton;
    els.chip.textContent = weton.label + " · Neptu " + weton.neptu +
      (result.duo ? " · " + result.duo.petung.result_name : "");
    els.disclaimer.textContent = result.disclaimer + " Sumber: " + result.source;
    renderSlide();
  }

  function render(state) {
    const result = state.result;
    els.formSection.hidden = Boolean(result);
    els.story.hidden = !result;
    els.shareTop.hidden = !result;
    window.setButtonLoading(els.submit, state.loading, "Menyiapkan roasting...");
    if (result) {
      renderStory(result);
      return;
    }
    renderedResult = null;
    Weton.showError(els.error, state.error);
  }

  function go(step) {
    const target = current + step;
    if (target < 0 || target >= slides.length) return;
    current = target;
    renderSlide();
  }

  async function submitRoast() {
    const message = Weton.roastError(Weton.getState().form);
    Weton.showError(els.error, message);
    if (message) return;
    current = 0;
    await Weton.submit();
  }

  function init(root) {
    els = {
      formSection: byId("m-roast-form"),
      story: byId("m-roast-story"),
      submit: byId("m-roast-submit"),
      error: byId("m-roast-error"),
      duoToggle: byId("m-duo"),
      duoFields: byId("m-duo-fields"),
      bars: byId("m-story-bars"),
      chip: byId("m-roast-chip"),
      stage: byId("m-story-stage"),
      card: byId("m-story-card"),
      label: byId("m-story-label"),
      text: byId("m-story-text"),
      count: byId("m-story-count"),
      prev: byId("m-story-prev"),
      next: byId("m-story-next"),
      reset: byId("m-roast-reset"),
      shareTop: byId("m-roast-share"),
      shareBottom: byId("m-roast-share-bottom"),
      disclaimer: byId("m-roast-disclaimer"),
      fields: {},
    };
    Object.keys(FIELDS).forEach((side) => {
      FIELDS[side].forEach((field) => {
        els.fields[side + "_" + field] = byId("m-" + side + "-" + field);
      });
    });
    Weton.bindInputs(els.fields);
    els.duoToggle.addEventListener("change", () => {
      Weton.updateForm({ duo: els.duoToggle.checked });
      els.duoFields.hidden = !els.duoToggle.checked;
    });
    els.submit.addEventListener("click", submitRoast);
    els.prev.addEventListener("click", () => go(-1));
    els.next.addEventListener("click", () => go(1));
    els.stage.addEventListener("touchstart", (event) => {
      touchStart = event.touches[0].clientX;
    }, { passive: true });
    els.stage.addEventListener("touchend", (event) => {
      if (touchStart === null) return;
      const distance = event.changedTouches[0].clientX - touchStart;
      touchStart = null;
      if (Math.abs(distance) >= SWIPE_DISTANCE) go(distance < 0 ? 1 : -1);
    });
    els.reset.addEventListener("click", () => {
      current = 0;
      Weton.reset();
    });
    Weton.bindShare([els.shareTop, els.shareBottom], (result) => (slides[current] ? Weton.roastShare(result, slides[current].text) : null));
  }

  function activate(state) {
    Weton.syncInputs(els.fields, state.form);
    els.duoToggle.checked = Boolean(state.form.duo);
    els.duoFields.hidden = !state.form.duo;
    render(state);
  }

  Weton.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
