(function () {
  const Tarot = window.Tarot;

  Tarot.registerRenderer("desktop", Tarot.drawForm({
    prefix: "d",
    keepForm: true,
    loadingLabel: "Membuka kartu...",
    renderResult: (result, prefix) => {
      Tarot.renderStage(Tarot.byId(prefix + "-stage"), result.card);
      Tarot.renderDaily(Tarot.byId(prefix + "-cards"), result);
      Tarot.renderFooter(prefix, result);
    },
    clearResult: (prefix) => {
      Tarot.resetStage(Tarot.byId(prefix + "-stage"));
      Tarot.clear(Tarot.byId(prefix + "-cards"));
    },
  }));
})();
