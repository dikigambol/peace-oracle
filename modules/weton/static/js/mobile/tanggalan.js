(function () {
  const Weton = window.Weton;
  const WEEKDAYS = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"];
  const LAHIR_FIELDS = ["tanggal", "jam", "kota"];
  let els = null;
  let renderedDays = null;
  let scrolledTo = null;

  function byId(id) {
    return document.getElementById(id);
  }

  function buildChip(result, day) {
    const chip = Weton.el("button", "wt-m-day");
    chip.type = "button";
    chip.dataset.date = day.date;
    chip.setAttribute("role", "option");
    chip.setAttribute("aria-label", Weton.describeDayForLabel(result, day));
    chip.classList.toggle("is-today", day.today);
    chip.appendChild(Weton.el("span", "wt-m-day-week", WEEKDAYS[day.weekday]));
    chip.appendChild(Weton.el("span", "wt-m-day-num", String(day.day)));
    chip.appendChild(Weton.el("span", "wt-m-day-pasaran", day.weton.pasaran));
    chip.appendChild(Weton.renderMarks(day));
    return chip;
  }

  function renderStrip(result) {
    Weton.clear(els.strip);
    result.days.forEach((day) => els.strip.appendChild(buildChip(result, day)));
    renderedDays = result.days;
    scrolledTo = null;
  }

  function scrollToSelected(result) {
    if (scrolledTo === result.selected) return;
    const chip = els.strip.querySelector('[data-date="' + result.selected + '"]');
    if (!chip || !els.strip.clientWidth) return;
    els.strip.scrollLeft = chip.offsetLeft - (els.strip.clientWidth - chip.offsetWidth) / 2;
    scrolledTo = result.selected;
  }

  function renderSelection(result) {
    Array.from(els.strip.children).forEach((chip) => {
      const on = chip.dataset.date === result.selected;
      chip.classList.toggle("is-selected", on);
      chip.setAttribute("aria-selected", on ? "true" : "false");
    });
    scrollToSelected(result);
    Weton.clear(els.detail);
    els.detail.appendChild(Weton.renderDayDetail(result, result.selected));
  }

  function renderWetonan(result) {
    const wetonan = result.wetonan;
    els.summary.hidden = !wetonan;
    els.clear.hidden = !wetonan;
    Weton.clear(els.summary);
    if (wetonan) els.summary.appendChild(Weton.renderWetonanSummary(wetonan));
  }

  function render(state) {
    const result = state.result;
    els.error.hidden = !state.error;
    els.error.textContent = state.error;
    els.strip.setAttribute("aria-busy", state.loading ? "true" : "false");
    window.setButtonLoading(els.submit, state.loading && Boolean(state.form.lahir_tanggal), "Menandai...");
    if (!result) return;
    els.month.textContent = result.month.label;
    els.jawa.textContent = result.month.jawa_label;
    els.prev.disabled = !result.month.prev;
    els.next.disabled = !result.month.next;
    if (result.days !== renderedDays) renderStrip(result);
    renderSelection(result);
    renderWetonan(result);
    els.note.textContent = result.note;
    els.disclaimer.textContent = result.disclaimer + " Sumber: " + Object.values(result.sources).join("; ") + ".";
  }

  function goToday() {
    const result = Weton.getState().result;
    if (result && result.days.some((day) => day.date === result.today)) {
      Weton.patchResult({ selected: result.today });
      return;
    }
    Weton.calendarGo({ tanggal: result ? result.today : "" });
  }

  function init(root) {
    els = {
      root: root,
      month: byId("m-cal-month"),
      jawa: byId("m-cal-jawa"),
      prev: byId("m-cal-prev"),
      next: byId("m-cal-next"),
      strip: byId("m-cal-strip"),
      error: byId("m-cal-error"),
      detail: byId("m-cal-detail"),
      submit: byId("m-wetonan-submit"),
      clear: byId("m-wetonan-clear"),
      summary: byId("m-wetonan-summary"),
      note: byId("m-cal-note"),
      disclaimer: byId("m-cal-disclaimer"),
      today: byId("m-cal-today"),
      share: byId("m-cal-share"),
    };
    LAHIR_FIELDS.forEach((field) => {
      const node = byId("m-lahir-" + field);
      node.addEventListener("input", () => Weton.updateForm({ ["lahir_" + field]: node.value }));
    });
    els.strip.addEventListener("click", (event) => {
      const chip = event.target.closest("[data-date]");
      if (!chip) return;
      scrolledTo = chip.dataset.date;
      Weton.patchResult({ selected: chip.dataset.date });
    });
    els.prev.addEventListener("click", () => {
      const result = Weton.getState().result;
      if (result && result.month.prev) Weton.calendarGo({ bulan: result.month.prev });
    });
    els.next.addEventListener("click", () => {
      const result = Weton.getState().result;
      if (result && result.month.next) Weton.calendarGo({ bulan: result.month.next });
    });
    els.today.addEventListener("click", goToday);
    els.submit.addEventListener("click", () => {
      const state = Weton.getState();
      if (!state.form.lahir_tanggal) {
        els.error.hidden = false;
        els.error.textContent = "Isi tanggal lahir dulu.";
        return;
      }
      Weton.calendarGo({ tanggal: state.result ? state.result.selected : "" });
    });
    els.clear.addEventListener("click", () => {
      Weton.updateForm({ lahir_tanggal: "", lahir_jam: "", lahir_kota: "" });
      LAHIR_FIELDS.forEach((field) => {
        byId("m-lahir-" + field).value = "";
      });
      const result = Weton.getState().result;
      Weton.calendarGo({ tanggal: result ? result.selected : "" });
    });
    els.share.addEventListener("click", () => {
      const result = Weton.getState().result;
      if (result) Weton.share(Weton.calendarShare(result, result.selected));
    });
  }

  function activate(state) {
    LAHIR_FIELDS.forEach((field) => {
      byId("m-lahir-" + field).value = state.form["lahir_" + field] || "";
    });
    renderedDays = null;
    render(state);
  }

  Weton.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
