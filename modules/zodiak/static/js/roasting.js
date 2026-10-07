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
  const btnCalcPairRoast = byId("btn-calc-pair-roast");

  const symbolEl = byId("roast-symbol");
  const nameEl = byId("roast-name");
  const datesEl = byId("roast-dates");
  const pairSignANameEl = byId("pair-sign-a-name");
  const elementBadgeEl = byId("roast-element-badge");
  const headlineTextEl = byId("roast-headline-text");
  const toxicListEl = byId("roast-toxic-list");
  const financialTextEl = byId("roast-financial-text");
  const loveTextEl = byId("roast-love-text");
  const quoteTextEl = byId("roast-quote-text");
  const tipTextEl = byId("roast-tip-text");

  const symbols = {
    aries: "♈",
    taurus: "♉",
    gemini: "♊",
    cancer: "♋",
    leo: "♌",
    virgo: "♍",
    libra: "♎",
    scorpio: "♏",
    sagittarius: "♐",
    capricorn: "♑",
    aquarius: "♒",
    pisces: "♓",
  };

  const elementClasses = {
    api: "fire",
    tanah: "earth",
    udara: "air",
    air: "water",
  };

  let activeSignA = null;
  if (Zodiak && Zodiak.bindSpotlight) {
    Zodiak.bindSpotlight(cards);
  }

  function setRolling(button, rolling) {
    if (!button) return;
    button.classList.toggle("rolling", rolling);
    button.disabled = rolling;
  }

  function setText(id, value) {
    const node = byId(id);
    if (node) node.innerText = value ?? "";
  }

  function displayRoastingDetails(data, signKey) {
    if (panels.content) panels.content.classList.remove("hidden");
    if (pairCardPanel) pairCardPanel.classList.remove("hidden");
    const roast = data.roast || {};
    if (symbolEl) {
      if (typeof window.getZodiacSvg === "function") {
        symbolEl.innerHTML = window.getZodiacSvg(signKey, 64);
      } else {
        symbolEl.innerText = symbols[signKey] || "";
      }
    }
    if (nameEl) nameEl.innerText = data.name || "";
    if (datesEl) datesEl.innerText = data.date_range || "";
    if (pairSignANameEl) pairSignANameEl.innerText = data.name || "Zodiak Ini";
    const elemKey = (data.element || "Api").toLowerCase();
    const cssClass = elementClasses[elemKey] || "fire";
    if (elementBadgeEl) {
      elementBadgeEl.className = `details-element-badge element-badge ${cssClass}`;
      elementBadgeEl.innerText = data.element || "";
    }
    if (headlineTextEl) headlineTextEl.innerText = roast.headline || "";
    if (toxicListEl) {
      toxicListEl.innerHTML = "";
      (roast.toxic_traits || []).forEach((trait) => {
        const li = document.createElement("li");
        li.innerText = trait;
        toxicListEl.appendChild(li);
      });
    }
    if (financialTextEl) financialTextEl.innerText = roast.financial_sin || "";
    if (loveTextEl) loveTextEl.innerText = roast.love_red_flag || "";
    if (quoteTextEl) quoteTextEl.innerText = roast.catchphrase ? `"${roast.catchphrase}"` : "";
    if (tipTextEl) tipTextEl.innerText = roast.survival_tip || "";
  }

  async function loadRoast(roll) {
    if (panels.content) panels.content.classList.add("hidden");
    if (pairCardPanel) pairCardPanel.classList.add("hidden");
    if (panels.loader) panels.loader.classList.remove("hidden");
    setRolling(roll ? btnRollDiceRoast : null, true);
    try {
      const data = await window.fetchJson(
        `/api/zodiak/roast?sign=${activeSignA}${roll ? "&roll=1" : ""}`,
      );
      setTimeout(() => {
        if (panels.loader) panels.loader.classList.add("hidden");
        displayRoastingDetails(data, activeSignA);
        if (data.roast && Zodiak && Zodiak.notifyQuota) {
          Zodiak.notifyQuota(data.roast.ai_notice);
        }
        setRolling(roll ? btnRollDiceRoast : null, false);
      }, 300);
    } catch (err) {
      if (panels.loader) panels.loader.classList.add("hidden");
      if (roll) {
        if (panels.content) panels.content.classList.remove("hidden");
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
          if (Zodiak && Zodiak.notifyQuota) {
            Zodiak.notifyQuota(rel.ai_notice);
          }
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
      if (Zodiak && Zodiak.selectCard) {
        Zodiak.selectCard(cards, card, panels);
      } else {
        cards.forEach((c) => c.classList.remove("active"));
        card.classList.add("active");
        if (panels.instruction) panels.instruction.classList.add("hidden");
        if (panels.content) panels.content.classList.add("hidden");
        if (panels.loader) panels.loader.classList.remove("hidden");
      }
      activeSignA = card.getAttribute("data-sign");
      if (pairSignSelectEl) pairSignSelectEl.value = "";
      if (pairRoastResultEl) pairRoastResultEl.classList.add("hidden");
      loadRoast(false);
    });
  });

  if (Zodiak && Zodiak.bindBackToGrid) {
    Zodiak.bindBackToGrid(byId("btn-back-grid-roast"));
  }

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

  if (btnCalcPairRoast) {
    btnCalcPairRoast.addEventListener("click", () => {
      const signB = pairSignSelectEl ? pairSignSelectEl.value : "";
      if (!activeSignA) {
        window.showErrorToast("Pilih salah satu zodiak pada dial di atas terlebih dahulu!");
        return;
      }
      if (!signB) {
        window.showErrorToast("Pilih zodiak pasangan terlebih dahulu!");
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
