(function () {
  const Tarot = window.Tarot;

  Tarot.registerRenderer("mobile", Tarot.drawForm({
    prefix: "m",
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
