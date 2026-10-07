(function () {
  const Tarot = window.Tarot;

  Tarot.registerRenderer("mobile", Tarot.drawSteps({
    total: 3,
    fanStep: 3,
    submitLabel: "Buka kartu",
    loadingLabel: "Membuka kartu...",
    fields: { question: "m-question" },
    radios: { topic: "m-topic" },
    spreadRadios: "m-spread",
    renderResult: (result, prefix) => {
      Tarot.renderSummary(Tarot.byId(prefix + "-summary"), result);
      Tarot.renderBoard(Tarot.byId(prefix + "-board"), result, prefix);
      Tarot.renderInsights(Tarot.byId(prefix + "-insights"), result);
      Tarot.renderCardList(Tarot.byId(prefix + "-cards"), result, prefix);
      Tarot.renderFooter(prefix, result);
    },
  }));
})();
