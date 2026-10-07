(function () {
  const Tarot = window.Tarot;

  Tarot.registerRenderer("mobile", Tarot.drawSteps({
    total: 2,
    submitLabel: "Hitung kartuku",
    loadingLabel: "Menghitung kartu...",
    fields: { tanggal: "m-tanggal", tahun: "m-tahun" },
    validate: (form, step) => (step === 1 && !form.tanggal ? "Isi tanggal lahirmu dulu." : ""),
    renderResult: (result, prefix) => {
      Tarot.renderBirth(Tarot.byId(prefix + "-cards"), result);
      Tarot.renderFooter(prefix, result);
    },
  }));
})();
