(function () {
  const Tarot = window.Tarot;

  function renderBond(result, prefix) {
    const people = result.people.a === "Kamu" ? "Kamu dan " + result.people.b : result.people.a + " dan " + result.people.b;
    Tarot.renderSummary(Tarot.byId(prefix + "-summary"), result, people);
    Tarot.renderBoard(Tarot.byId(prefix + "-board"), result, prefix);
    Tarot.renderInsights(Tarot.byId(prefix + "-insights"), result);
    Tarot.renderCardList(Tarot.byId(prefix + "-cards"), result, prefix);
    Tarot.renderFooter(prefix, result);
  }

  Tarot.registerRenderer("mobile", Tarot.drawSteps({
    total: 2,
    fanStep: 2,
    submitLabel: "Buka kartu",
    loadingLabel: "Membuka kartu...",
    fields: { nama_a: "m-nama-a", nama_b: "m-nama-b" },
    renderResult: renderBond,
  }));
})();
