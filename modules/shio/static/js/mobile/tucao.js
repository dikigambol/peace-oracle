(function () {
  const Shio = window.Shio;
  let els = null;
  let renderedResult = null;
  let renderedDraw = null;

  function byId(id) {
    return document.getElementById(id);
  }

  function showError(message) {
    els.error.hidden = !message;
    els.error.textContent = message || "";
  }

  function buildStory(section) {
    const story = Shio.el("section", "sh-m-story sh-m-story-" + section.key);
    story.appendChild(Shio.el("p", "sh-m-story-label", section.title));
    story.appendChild(section.node);
    return story;
  }

  function renderRoast(state, instant) {
    const data = state.result;
    if (data !== renderedResult) {
      Shio.clear(els.header);
      els.header.appendChild(Shio.roast.buildHeader(data));
      renderedResult = data;
    }
    if (state.draw === renderedDraw) return;
    Shio.clear(els.stories);
    Shio.roast.sections(data, state.draw).forEach((section) => els.stories.appendChild(buildStory(section)));
    els.count.textContent = Shio.roast.comboLabel(data, state.draw);
    els.reroll.hidden = !Shio.roast.canReroll(data);
    if (!instant && renderedDraw && renderedDraw.count < state.draw.count) Shio.replay(els.stories, "roast-flash");
    renderedDraw = state.draw;
  }

  function render(state, instant) {
    const data = state.result;
    const viewing = Boolean(data) || state.loading;
    Shio.markChoice(els.root, "gender", state.form.gender);
    els.date.value = state.form.date || "";
    els.form.hidden = viewing;
    els.loading.hidden = !state.loading;
    els.result.hidden = !data || state.loading;
    els.home.hidden = viewing;
    els.back.hidden = !viewing;
    if (data) {
      renderRoast(state, instant === true);
      Shio.roast.renderPairPanel(els.pair, state);
    }
  }

  function init(root) {
    els = {
      root: root,
      home: byId("m-roast-home"),
      back: byId("m-roast-back"),
      form: byId("m-roast-form"),
      date: byId("m-roast-date"),
      error: byId("m-roast-error"),
      submit: byId("m-roast-submit"),
      loading: byId("m-roast-loading"),
      result: byId("m-roast-result"),
      header: byId("m-roast-header"),
      stories: byId("m-roast-stories"),
      count: byId("m-roast-count"),
      reroll: byId("m-roast-reroll"),
      pair: {
        toggle: root.querySelector("[data-pair-toggle]"),
        body: root.querySelector("[data-pair-body]"),
        loading: root.querySelector("[data-pair-loading]"),
        card: root.querySelector("[data-pair-card]"),
      },
    };
    els.loading.appendChild(Shio.loadingBox("Menyalakan api..."));
    Shio.mobileDate(els.date, (value) => {
      Shio.updateForm({ date: value });
      showError("");
    });
    Shio.roast.bindGender(root, () => render(Shio.getState()));
    Shio.roast.bindPairPanel(els.pair);
    els.submit.addEventListener("click", async () => {
      if (!Shio.getState().form.date) {
        showError("Isi tanggal lahir dulu.");
        return;
      }
      Shio.particles.emitFrom(els.submit, 34);
      window.scrollTo(0, 0);
      await Shio.roast.submit();
    });
    els.reroll.addEventListener("click", () => {
      Shio.roast.reroll();
      Shio.scrollIntoView(els.stories);
    });
    els.back.addEventListener("click", () => {
      if (Shio.getState().loading) return;
      Shio.setState({ result: null, draw: null, pair: null });
      window.scrollTo(0, 0);
    });
  }

  function activate(state) {
    renderedResult = null;
    renderedDraw = null;
    render(state, true);
  }

  Shio.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
