(function () {
  const Tarot = window.Tarot;

  Tarot.registerRenderer("mobile", Tarot.drawSteps({
    total: 2,
    fanStep: 2,
    submitLabel: "Lihat jawabannya",
    loadingLabel: "Membaca jawaban...",
    fields: { question: "m-question" },
    validate: (form, step) => (step === 1 ? Tarot.questionError(form, true) : ""),
    renderResult: (result, prefix) => {
      Tarot.renderYesNo(Tarot.byId(prefix + "-cards"), result);
      Tarot.followupChat(prefix, result);
      Tarot.renderFooter(prefix, result);
    },
  }));
})();
