document.addEventListener("DOMContentLoaded", () => {
  const Zodiak = window.Zodiak;
  const cards = document.querySelectorAll(".zodiac-card");
  const byId = (id) => document.getElementById(id);
  const panels = {
    instruction: byId("roast-instruction"),
    loader: byId("roast-loader"),
    content: byId("roast-content"),
  };
  const pairCardPanel = byId("pair-roast-card-panel");
  const pairSignSelectEl = byId("pair-sign-select");
  const pairRoastResultEl = byId("pair-roast-result");
  const pairLoaderPanel = byId("pair-roast-loader");
  const btnRollDiceRoast = byId("btn-roll-dice-roast");
  const btnRollDicePair = byId("btn-roll-dice-pair");
  let activeSignA = null;
  Zodiak.bindSpotlight(cards);

  function setRolling(button, rolling) {
    if (!button) return;
    button.classList.toggle("rolling", rolling);
    button.disabled = rolling;
  }

  function setText(id, value) {
    const node = byId(id);
    if (node) node.innerText = value;
  }

  function displayRoastingDetails(data, signKey) {
    panels.content.classList.remove("hidden");
    if (pairCardPanel) pairCardPanel.classList.remove("hidden");
    const roast = data.roast;
    setText("roast-symbol", Zodiak.symbolFor(signKey));
    setText("roast-name", data.name);
    setText("roast-dates", data.date_range);
    setText("pair-sign-a-name", data.name);
    Zodiak.setElementBadge(
      byId("roast-element-badge"),
      data.element || "Api",
      "details-element-badge element-badge",
    );
    setText("roast-headline-text", roast.headline);
    Zodiak.fillList(byId("roast-toxic-list"), roast.toxic_traits);
    setText("roast-financial-text", roast.financial_sin);
    setText("roast-love-text", roast.love_red_flag);
    setText("roast-quote-text", `"${roast.catchphrase}"`);
    setText("roast-tip-text", roast.survival_tip);
  }

  async function loadRoast(roll) {
    panels.content.classList.add("hidden");
    if (pairCardPanel) pairCardPanel.classList.add("hidden");
    panels.loader.classList.remove("hidden");
    setRolling(roll ? btnRollDiceRoast : null, true);
    try {
      const data = await window.fetchJson(
        `/api/zodiak/roast?sign=${activeSignA}${roll ? "&roll=1" : ""}`,
      );
      setTimeout(() => {
        panels.loader.classList.add("hidden");
        displayRoastingDetails(data, activeSignA);
        if (data.roast) Zodiak.notifyQuota(data.roast.ai_notice);
        setRolling(roll ? btnRollDiceRoast : null, false);
      }, 300);
    } catch (err) {
      panels.loader.classList.add("hidden");
      if (roll) {
        panels.content.classList.remove("hidden");
        if (pairCardPanel) pairCardPanel.classList.remove("hidden");
      }
      setRolling(roll ? btnRollDiceRoast : null, false);
      window.showErrorToast(roll ? "Gagal mengacak roasting baru." : "Gagal mengambil data roasting. Silakan coba lagi.");
    }
  }

  async function loadPairRoast(signB, roll) {
    if (pairRoastResultEl) pairRoastResultEl.classList.add("hidden");
    if (pairLoaderPanel) pairLoaderPanel.classList.remove("hidden");
    setRolling(roll ? btnRollDicePair : null, true);
    try {
      const data = await window.fetchJson(
        `/api/zodiak/roast?sign=${activeSignA}&sign_b=${signB}${roll ? "&roll=1" : ""}`,
      );
      const rel = data.relationship_roast;
      setTimeout(() => {
        if (pairLoaderPanel) pairLoaderPanel.classList.add("hidden");
        if (rel && pairRoastResultEl) {
          setText("pair-roast-badge", rel.badge);
          setText("pair-roast-headline", rel.headline);
          setText("pair-roast-desc", rel.desc);
          setText("pair-roast-verdict", rel.verdict);
          pairRoastResultEl.classList.remove("hidden");
          Zodiak.notifyQuota(rel.ai_notice);
        }
        setRolling(roll ? btnRollDicePair : null, false);
      }, 300);
    } catch (err) {
      if (pairLoaderPanel) pairLoaderPanel.classList.add("hidden");
      setRolling(roll ? btnRollDicePair : null, false);
      window.showErrorToast(roll ? "Gagal mengacak roasting pasangan baru." : "Gagal mengambil roasting hubungan.");
    }
  }

  cards.forEach((card) => {
    card.addEventListener("click", () => {
      Zodiak.selectCard(cards, card, panels);
      activeSignA = card.getAttribute("data-sign");
      if (pairSignSelectEl) pairSignSelectEl.value = "";
      if (pairRoastResultEl) pairRoastResultEl.classList.add("hidden");
      loadRoast(false);
    });
  });
  Zodiak.bindBackToGrid(byId("btn-back-grid-roast"));
  if (pairSignSelectEl) {
    pairSignSelectEl.addEventListener("change", () => {
      const signB = pairSignSelectEl.value;
      if (!activeSignA || !signB) {
        if (pairRoastResultEl) pairRoastResultEl.classList.add("hidden");
        if (pairLoaderPanel) pairLoaderPanel.classList.add("hidden");
        return;
      }
      loadPairRoast(signB, false);
    });
  }
  if (btnRollDiceRoast) {
    btnRollDiceRoast.addEventListener("click", () => {
      if (activeSignA) loadRoast(true);
    });
  }
  if (btnRollDicePair) {
    btnRollDicePair.addEventListener("click", () => {
      const signB = pairSignSelectEl ? pairSignSelectEl.value : "";
      if (!activeSignA || !signB) {
        window.showErrorToast("Pilih zodiak pasangan terlebih dahulu!");
        return;
      }
      loadPairRoast(signB, true);
    });
  }
});
