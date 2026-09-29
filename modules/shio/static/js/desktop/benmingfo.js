(function () {
  const Shio = window.Shio;
  const byId = Shio.byId;
  let els = null;
  let renderedResult = null;

  function buildCard(data) {
    const card = Shio.el("article", "fortune-card sh-d-guardian-card");
    card.appendChild(Shio.guardian.buildHero(data));
    card.appendChild(Shio.guardian.buildHighlights(data));
    card.appendChild(Shio.guardian.buildCategories(data));
    card.appendChild(Shio.guardian.buildMeta(data));
    return card;
  }

  function render(state) {
    const data = state.result;
    Shio.markChoice(els.root, "shio", state.form.shio);
    els.root.querySelectorAll("[data-shio]").forEach((button) => {
      button.disabled = state.loading;
    });
    els.empty.hidden = Boolean(data) || state.loading;
    els.loading.hidden = !state.loading;
    els.result.hidden = !data || state.loading;
    if (!data || data === renderedResult) return;
    Shio.clear(els.result);
    els.result.appendChild(buildCard(data));
    renderedResult = data;
  }

  function init(root) {
    els = {
      root: root,
      empty: byId("d-guardian-empty"),
      loading: byId("d-guardian-loading"),
      result: byId("d-guardian-result"),
    };
    els.loading.appendChild(Shio.loadingBox("Memanggil penjaga shio-mu..."));
    root.querySelectorAll("[data-shio]").forEach((button) => {
      button.addEventListener("click", async () => {
        const data = await Shio.guardian.submit(button.dataset.shio);
        if (data) Shio.focusResult(els.result);
      });
    });
  }

  function activate(state) {
    renderedResult = null;
    render(state);
  }

  Shio.registerRenderer("desktop", { init: init, render: render, activate: activate });
})();
