(function () {
  const Weton = window.Weton;
  const byId = Weton.byId;
  const KEY_STEPS = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -7, ArrowDown: 7 };
  let els = null;
  let lahirPicker = null;
  let renderedDays = null;

  function buildCell(result, day) {
    const cell = Weton.el("button", "wt-cal-cell");
    cell.type = "button";
    cell.dataset.date = day.date;
    cell.setAttribute("aria-label", Weton.describeDayForLabel(result, day));
    cell.classList.toggle("is-today", day.today);
    cell.appendChild(Weton.el("span", "wt-cal-num", String(day.day)));
    cell.appendChild(Weton.el("span", "wt-cal-pasaran", day.weton.pasaran));
    const jawa = day.jawa.tanggal === 1 ? "1 " + day.jawa.sasi : String(day.jawa.tanggal);
    cell.appendChild(Weton.el("span", "wt-cal-jawa", jawa));
    cell.appendChild(Weton.renderMarks(day));
    return cell;
  }

  function renderGrid(result) {
    Weton.clear(els.grid);
    for (let index = 0; index < result.month.first_weekday; index += 1) {
      els.grid.appendChild(Weton.el("span", "wt-cal-cell wt-cal-cell-empty"));
    }
    const byDay = {};
    result.days.forEach((day) => {
      byDay[day.day] = day;
    });
    for (let number = 1; number <= result.month.length; number += 1) {
      const day = byDay[number];
      if (day) {
        els.grid.appendChild(buildCell(result, day));
      } else {
        const blank = Weton.el("span", "wt-cal-cell wt-cal-cell-out", String(number));
        blank.setAttribute("aria-hidden", "true");
        els.grid.appendChild(blank);
      }
    }
    renderedDays = result.days;
  }

  function renderSelection(result) {
    els.grid.querySelectorAll("button[data-date]").forEach((cell) => {
      const on = cell.dataset.date === result.selected;
      cell.classList.toggle("is-selected", on);
      cell.setAttribute("aria-pressed", on ? "true" : "false");
      cell.tabIndex = on ? 0 : -1;
    });
    Weton.clear(els.detail);
    els.detail.appendChild(Weton.renderDayDetail(result, result.selected));
  }

  function render(state) {
    els.main.setAttribute("aria-busy", state.loading ? "true" : "false");
    if (!Weton.calendar.renderHeader(els, state)) return;
    const result = state.result;
    if (result.days !== renderedDays) renderGrid(result);
    renderSelection(result);
    Weton.calendar.renderFooter(els, result);
  }

  function select(iso, focus) {
    Weton.patchResult({ selected: iso });
    if (focus) {
      const cell = els.grid.querySelector('button[data-date="' + iso + '"]');
      if (cell) cell.focus();
    }
  }

  function moveSelection(step) {
    const result = Weton.getState().result;
    if (!result) return;
    const index = result.days.findIndex((day) => day.date === result.selected);
    const target = result.days[index + step];
    if (target) select(target.date, true);
  }

  function syncLahir(form) {
    Weton.syncPicker(lahirPicker, byId("d-lahir-tanggal"), form.lahir_tanggal);
    Weton.syncInputs(els.lahirFields, form);
  }

  function init(root) {
    els = {
      main: root.querySelector(".wt-d-cal-main"),
      month: byId("d-cal-month"),
      jawa: byId("d-cal-jawa"),
      prev: byId("d-cal-prev"),
      next: byId("d-cal-next"),
      today: byId("d-cal-today"),
      grid: byId("d-cal-grid"),
      error: byId("d-cal-error"),
      note: byId("d-cal-note"),
      detail: byId("d-cal-detail"),
      form: byId("d-wetonan-form"),
      submit: byId("d-wetonan-submit"),
      clear: byId("d-wetonan-clear"),
      summary: byId("d-wetonan-summary"),
      disclaimer: byId("d-cal-disclaimer"),
      lahirFields: { lahir_jam: byId("d-lahir-jam"), lahir_kota: byId("d-lahir-kota") },
    };
    Weton.initDate(byId("d-cal-date"), (str) => {
      if (str) Weton.calendarGo({ tanggal: str });
    });
    lahirPicker = Weton.initDate(byId("d-lahir-tanggal"), (str) => Weton.updateForm({ lahir_tanggal: str }));
    Weton.bindInputs(els.lahirFields);
    Weton.calendar.bindNav(els, (iso) => select(iso, false));
    els.grid.addEventListener("click", (event) => {
      const cell = event.target.closest("button[data-date]");
      if (cell) select(cell.dataset.date, false);
    });
    els.grid.addEventListener("keydown", (event) => {
      const step = KEY_STEPS[event.key];
      if (!step) return;
      event.preventDefault();
      moveSelection(step);
    });
    els.form.addEventListener("submit", (event) => {
      event.preventDefault();
      Weton.calendar.submitWetonan(els);
    });
    els.clear.addEventListener("click", () => Weton.calendar.clearWetonan(syncLahir));
  }

  function activate(state) {
    syncLahir(state.form);
    renderedDays = null;
    render(state);
  }

  Weton.registerRenderer("desktop", { init: init, render: render, activate: activate });
})();
