(function () {
  const Shio = window.Shio;
  const byId = Shio.byId;
  let els = null;
  let picker = null;
  let renderedResult = null;

  function ready(form) {
    return Boolean(form.date && form.gender);
  }

  function heading(section) {
    const title = Shio.el("h3", "destiny-heading");
    title.appendChild(Shio.icon(section.icon));
    title.appendChild(document.createTextNode(" " + section.title));
    return title;
  }

  function renderResult(data) {
    Shio.clear(els.nav);
    Shio.clear(els.notices);
    Shio.clear(els.sections);
    els.notices.appendChild(Shio.destiny.buildNotices(data.meta, data.no_birth_time));
    Shio.destiny.sections(data).forEach((section) => {
      const block = Shio.el("section", "destiny-block");
      block.id = "d-destiny-sec-" + section.key;
      block.appendChild(heading(section));
      block.appendChild(section.build());
      els.sections.appendChild(block);
      const link = Shio.el("a", "sh-d-destiny-link", section.title);
      link.href = "#" + block.id;
      link.addEventListener("click", (event) => {
        event.preventDefault();
        Shio.scrollIntoView(block);
      });
      els.nav.appendChild(link);
    });
    els.disclaimer.textContent = data.meta.disclaimer || "";
    Shio.destiny.refreshChartHints(els.result);
  }

  function render(state) {
    const data = state.result;
    Shio.markChoice(els.root, "gender", state.form.gender);
    Shio.destiny.syncTimeFields(els.time, state.form);
    window.setButtonLoading(els.submit, state.loading, "Membuka gulungan...", !ready(state.form));
    if (!state.loading) els.submit.disabled = !ready(state.form);
    els.empty.hidden = Boolean(data) || state.loading;
    els.loading.hidden = !state.loading;
    els.result.hidden = !data || state.loading;
    if (!data || data === renderedResult) return;
    renderResult(data);
    renderedResult = data;
  }

  function init(root) {
    els = {
      root: root,
      date: byId("d-destiny-date"),
      time: byId("d-destiny-time"),
      city: byId("d-destiny-city"),
      submit: byId("d-destiny-submit"),
      empty: byId("d-destiny-empty"),
      loading: byId("d-destiny-loading"),
      result: byId("d-destiny-result"),
      nav: byId("d-destiny-nav"),
      notices: byId("d-destiny-notices"),
      sections: byId("d-destiny-sections"),
      disclaimer: byId("d-destiny-disclaimer"),
    };
    els.loading.appendChild(Shio.loadingBox("Membuka gulungan..."));
    picker = Shio.desktopDate(els.date, {
      onChange: (dates, value) => {
        Shio.updateForm({ date: value || "" });
        render(Shio.getState());
      },
    });
    Shio.bindGender(root, () => render(Shio.getState()));
    Shio.destiny.bindTimeFields(els.time, () => render(Shio.getState()));
    els.city.addEventListener("input", () => Shio.updateForm({ city: els.city.value }));
    els.submit.addEventListener("click", async () => {
      const data = await Shio.destiny.submit();
      if (data) Shio.showResult(els.result);
    });
    window.addEventListener("resize", () => Shio.destiny.refreshChartHints(els.result));
  }

  function syncForm(state) {
    Shio.setDesktopDate(picker, els.date, state.form.date);
    els.city.value = state.form.city || "";
  }

  function activate(state) {
    syncForm(state);
    renderedResult = null;
    render(state);
  }

  Shio.registerRenderer("desktop", { init: init, render: render, activate: activate, syncForm: syncForm });
})();
