(function () {
  const Tarot = window.Tarot;

  Tarot.registerRenderer("desktop", Tarot.drawForm({
    prefix: "d",
    loadingLabel: "Membuka kartu...",
    fields: { question: "d-question" },
    radios: { topic: "d-topic" },
    spreadRadios: "d-spread",
    renderResult: (result, prefix) => {
      Tarot.renderSummary(Tarot.byId(prefix + "-summary"), result);
      Tarot.renderBoard(Tarot.byId(prefix + "-board"), result, prefix);
      Tarot.renderInsights(Tarot.byId(prefix + "-insights"), result);
      Tarot.renderCardList(Tarot.byId(prefix + "-cards"), result, prefix);
      Tarot.renderFooter(prefix, result);
    },
  }));
})();
