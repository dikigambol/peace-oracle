(function () {
  const Shio = window.Shio;
  const byId = Shio.byId;
  const memo = { result: null, draw: null };
  let els = null;

  function buildStory(section) {
    const story = Shio.el("section", "sh-m-story sh-m-story-" + section.key);
    story.appendChild(Shio.el("p", "sh-m-story-label", section.title));
    story.appendChild(section.node);
    return story;
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
      Shio.roast.renderInto(els, memo, state, {
        container: els.stories,
        wrap: buildStory,
        flash: els.stories,
        instant: instant === true,
      });
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
      pair: Shio.roast.pairElements(root),
    };
    els.loading.appendChild(Shio.loadingBox("Menyalakan api..."));
    Shio.mobileDate(els.date, (value) => {
      Shio.updateForm({ date: value });
      Shio.showError(els.error, "");
    });
    Shio.bindGender(root, () => render(Shio.getState()));
    Shio.roast.bindPairPanel(els.pair);
    els.submit.addEventListener("click", async () => {
      if (!Shio.getState().form.date) {
        Shio.showError(els.error, "Isi tanggal lahir dulu.");
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
    memo.result = null;
    memo.draw = null;
    render(state, true);
  }

  Shio.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
