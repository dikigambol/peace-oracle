(function () {
  const Weton = window.Weton;
  const FIELDS = { a: ["tanggal", "jam", "kota"], b: ["nama", "tanggal", "jam", "kota"] };
  const SWIPE_DISTANCE = 40;
  let els = null;
  let slides = [];
  let current = 0;
  let renderedResult = null;
  let touchStart = null;

  function byId(id) {
    return document.getElementById(id);
  }

  function showError(message) {
    els.error.hidden = !message;
    els.error.textContent = message || "";
  }

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
    showError(state.error);
  }

  function go(step) {
    const target = current + step;
    if (target < 0 || target >= slides.length) return;
    current = target;
    renderSlide();
  }

  async function submitRoast() {
    const form = Weton.getState().form;
    if (!form.a_tanggal) {
      showError("Isi tanggal lahirmu dulu.");
      return;
    }
    if (form.duo && !form.b_tanggal) {
      showError("Isi tanggal lahir orang kedua dulu, atau matikan opsi orang kedua.");
      return;
    }
    showError("");
    current = 0;
    await Weton.submit();
  }

  function init(root) {
    els = {
      root: root,
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
    };
    Object.keys(FIELDS).forEach((side) => {
      FIELDS[side].forEach((field) => {
        const node = byId("m-" + side + "-" + field);
        node.addEventListener("input", () => Weton.updateForm({ [side + "_" + field]: node.value }));
      });
    });
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
    const shareSlide = () => {
      const result = Weton.getState().result;
      if (result && slides[current]) Weton.share(Weton.roastShare(result, slides[current].text));
    };
    els.shareTop.addEventListener("click", shareSlide);
    els.shareBottom.addEventListener("click", shareSlide);
  }

  function activate(state) {
    Object.keys(FIELDS).forEach((side) => {
      FIELDS[side].forEach((field) => {
        byId("m-" + side + "-" + field).value = state.form[side + "_" + field] || "";
      });
    });
    els.duoToggle.checked = Boolean(state.form.duo);
    els.duoFields.hidden = !state.form.duo;
    render(state);
  }

  Weton.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
