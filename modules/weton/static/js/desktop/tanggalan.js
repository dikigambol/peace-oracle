(function () {
  const Weton = window.Weton;
  const LAHIR_FIELDS = ["jam", "kota"];
  const KEY_STEPS = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -7, ArrowDown: 7 };
  let els = null;
  let lahirPicker = null;
  let renderedDays = null;

  function byId(id) {
    return document.getElementById(id);
  }

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
    els.main.setAttribute("aria-busy", state.loading ? "true" : "false");
    window.setButtonLoading(els.submit, state.loading && Boolean(state.form.lahir_tanggal), "Menandai...");
    if (!result) return;
    els.month.textContent = result.month.label;
    els.jawa.textContent = result.month.jawa_label;
    els.prev.disabled = !result.month.prev;
    els.next.disabled = !result.month.next;
    if (result.days !== renderedDays) renderGrid(result);
    renderSelection(result);
    renderWetonan(result);
    els.note.textContent = result.note;
    els.disclaimer.textContent = result.disclaimer + " Sumber: " + Object.values(result.sources).join("; ") + ".";
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

  function goToday() {
    const result = Weton.getState().result;
    if (result && result.days.some((day) => day.date === result.today)) {
      select(result.today, false);
      return;
    }
    Weton.calendarGo({ tanggal: result ? result.today : "" });
  }

  function init(root) {
    els = {
      root: root,
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
    };
    const jump = byId("d-cal-date");
    window.initDatePicker("#d-cal-date", {
      dateFormat: "Y-m-d",
      altInput: true,
      altFormat: "j F Y",
      locale: "id",
      minDate: jump.dataset.min,
      maxDate: jump.dataset.max,
      disableMobile: true,
      onChange: (dates, str) => {
        if (str) Weton.calendarGo({ tanggal: str });
      },
    });
    const lahir = byId("d-lahir-tanggal");
    window.initDatePicker("#d-lahir-tanggal", {
      dateFormat: "Y-m-d",
      altInput: true,
      altFormat: "j F Y",
      locale: "id",
      minDate: lahir.dataset.min,
      maxDate: lahir.dataset.max,
      disableMobile: true,
      onChange: (dates, str) => Weton.updateForm({ lahir_tanggal: str }),
    });
    lahirPicker = lahir._flatpickr || null;
    LAHIR_FIELDS.forEach((field) => {
      const node = byId("d-lahir-" + field);
      node.addEventListener("input", () => Weton.updateForm({ ["lahir_" + field]: node.value }));
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
      syncLahir(Weton.getState().form);
      const result = Weton.getState().result;
      Weton.calendarGo({ tanggal: result ? result.selected : "" });
    });
  }

  function syncLahir(form) {
    if (lahirPicker) {
      if (form.lahir_tanggal) lahirPicker.setDate(form.lahir_tanggal, false);
      else lahirPicker.clear(false);
    }
    LAHIR_FIELDS.forEach((field) => {
      byId("d-lahir-" + field).value = form["lahir_" + field] || "";
    });
  }

  function activate(state) {
    syncLahir(state.form);
    renderedDays = null;
    render(state);
  }

  Weton.registerRenderer("desktop", { init: init, render: render, activate: activate });
})();
