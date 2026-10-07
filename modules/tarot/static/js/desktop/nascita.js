(function () {
  const Tarot = window.Tarot;

  Tarot.registerRenderer("desktop", Tarot.drawForm({
    prefix: "d",
    keepForm: true,
    loadingLabel: "Menghitung kartu...",
    fields: { tanggal: "d-tanggal", tahun: "d-tahun" },
    validate: (form) => (form.tanggal ? "" : "Isi tanggal lahirmu dulu."),
    renderResult: (result, prefix) => {
      Tarot.renderBirth(Tarot.byId(prefix + "-cards"), result);
      Tarot.renderFooter(prefix, result);
    },
    clearResult: (prefix) => Tarot.clear(Tarot.byId(prefix + "-cards")),
  }));
})();
