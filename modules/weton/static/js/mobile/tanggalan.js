(function () {
  const Weton = window.Weton;
  const byId = Weton.byId;
  const WEEKDAYS = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"];
  let els = null;
  let renderedDays = null;
  let scrolledTo = null;

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

  function render(state) {
    els.strip.setAttribute("aria-busy", state.loading ? "true" : "false");
    if (!Weton.calendar.renderHeader(els, state)) return;
    const result = state.result;
    if (result.days !== renderedDays) renderStrip(result);
    renderSelection(result);
    Weton.calendar.renderFooter(els, result);
  }

  function init(root) {
    els = {
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
      lahirFields: {
        lahir_tanggal: byId("m-lahir-tanggal"),
        lahir_jam: byId("m-lahir-jam"),
        lahir_kota: byId("m-lahir-kota"),
      },
    };
    Weton.bindInputs(els.lahirFields);
    els.strip.addEventListener("click", (event) => {
      const chip = event.target.closest("[data-date]");
      if (!chip) return;
      scrolledTo = chip.dataset.date;
      Weton.patchResult({ selected: chip.dataset.date });
    });
    Weton.calendar.bindNav(els, (iso) => Weton.patchResult({ selected: iso }));
    els.submit.addEventListener("click", () => Weton.calendar.submitWetonan(els));
    els.clear.addEventListener("click", () => Weton.calendar.clearWetonan((form) => Weton.syncInputs(els.lahirFields, form)));
  }

  function activate(state) {
    Weton.syncInputs(els.lahirFields, state.form);
    renderedDays = null;
    render(state);
  }

  Weton.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
