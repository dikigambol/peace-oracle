(function () {
  const Tarot = window.Tarot;

  Tarot.registerRenderer("desktop", Tarot.drawForm({
    prefix: "d",
    loadingLabel: "Membaca jawaban...",
    fields: { question: "d-question" },
    validate: (form) => Tarot.questionError(form, true),
    renderResult: (result, prefix) => {
      Tarot.renderYesNo(Tarot.byId(prefix + "-cards"), result);
      Tarot.followupChat(prefix, result);
      Tarot.renderFooter(prefix, result);
    },
  }));
})();
