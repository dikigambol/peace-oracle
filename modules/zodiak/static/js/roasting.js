document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".zodiac-card");
  cards.forEach((card) => {
    let rect = null;
    let ticking = false;
    card.addEventListener("mouseenter", () => {
      rect = card.getBoundingClientRect();
    });
    card.addEventListener("mousemove", (e) => {
      if (!rect) rect = card.getBoundingClientRect();
      if (!ticking) {
        window.requestAnimationFrame(() => {
          if (rect) {
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty("--x", `${x}px`);
            card.style.setProperty("--y", `${y}px`);
          }
          ticking = false;
        });
        ticking = true;
      }
    });
    card.addEventListener("mouseleave", () => {
      rect = null;
    });
  });
  const instructionPanel = document.getElementById("roast-instruction");
  const loaderPanel = document.getElementById("roast-loader");
  const contentPanel = document.getElementById("roast-content");
  const pairCardPanel = document.getElementById("pair-roast-card-panel");
  const btnBackGrid = document.getElementById("btn-back-grid-roast");
  const symbolEl = document.getElementById("roast-symbol");
  const nameEl = document.getElementById("roast-name");
  const datesEl = document.getElementById("roast-dates");
  const elementBadgeEl = document.getElementById("roast-element-badge");
  const headlineTextEl = document.getElementById("roast-headline-text");
  const toxicListEl = document.getElementById("roast-toxic-list");
  const financialTextEl = document.getElementById("roast-financial-text");
  const loveTextEl = document.getElementById("roast-love-text");
  const quoteTextEl = document.getElementById("roast-quote-text");
  const tipTextEl = document.getElementById("roast-tip-text");
  const pairSignANameEl = document.getElementById("pair-sign-a-name");
  const pairSignSelectEl = document.getElementById("pair-sign-select");
  const pairRoastResultEl = document.getElementById("pair-roast-result");
  const pairRoastBadgeEl = document.getElementById("pair-roast-badge");
  const pairRoastHeadlineEl = document.getElementById("pair-roast-headline");
  const pairRoastDescEl = document.getElementById("pair-roast-desc");
  const pairRoastVerdictEl = document.getElementById("pair-roast-verdict");
  const elementClasses = {
    api: "fire",
    tanah: "earth",
    udara: "air",
    air: "water",
  };
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
  let activeSignA = null;
  cards.forEach((card) => {
    card.addEventListener("click", async () => {
      cards.forEach((c) => c.classList.remove("active"));
      card.classList.add("active");
      instructionPanel.classList.add("hidden");
      contentPanel.classList.add("hidden");
      if (pairCardPanel) pairCardPanel.classList.add("hidden");
      loaderPanel.classList.remove("hidden");
      if (window.innerWidth <= 968) {
        const detailsContainer = document.querySelector(
          ".details-panel-container",
        );
        if (detailsContainer) {
          detailsContainer.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      }
      const signKey = card.getAttribute("data-sign");
      activeSignA = signKey;
      if (pairSignSelectEl) pairSignSelectEl.value = "";
      if (pairRoastResultEl) pairRoastResultEl.classList.add("hidden");
      try {
        const response = await fetch(`/api/zodiak/roast?sign=${signKey}`);
        if (!response.ok)
          throw new Error("Gagal mengambil data roasting zodiak");
        const data = await response.json();
        setTimeout(() => {
          loaderPanel.classList.add("hidden");
          displayRoastingDetails(data, signKey);
          if (
            data.roast &&
            data.roast.ai_notice &&
            typeof window.showAiQuotaToast === "function"
          ) {
            window.showAiQuotaToast(data.roast.ai_notice);
          }
        }, 300);
      } catch (err) {
        console.error(err);
        loaderPanel.classList.add("hidden");
        alert("Gagal mengambil data roasting. Silakan coba lagi.");
      }
    });
  });
  if (btnBackGrid) {
    btnBackGrid.addEventListener("click", () => {
      const selectorContainer = document.querySelector(
        ".zodiac-selector-container",
      );
      if (selectorContainer) {
        selectorContainer.scrollIntoView({ behavior: "smooth" });
      }
    });
  }
  function displayRoastingDetails(data, signKey) {
    contentPanel.classList.remove("hidden");
    if (pairCardPanel) pairCardPanel.classList.remove("hidden");
    const roast = data.roast;
    if (symbolEl) symbolEl.innerText = symbols[signKey] || "✨";
    if (nameEl) nameEl.innerText = data.name;
    if (datesEl) datesEl.innerText = data.date_range;
    if (pairSignANameEl) pairSignANameEl.innerText = data.name;
    const elemKey = (data.element || "Api").toLowerCase();
    const cssClass = elementClasses[elemKey] || "fire";
    if (elementBadgeEl) {
      elementBadgeEl.className = `details-element-badge element-badge ${cssClass}`;
      elementBadgeEl.innerText = data.element;
    }
    if (headlineTextEl) headlineTextEl.innerText = roast.headline;
    if (toxicListEl) {
      toxicListEl.innerHTML = "";
      roast.toxic_traits.forEach((trait) => {
        const li = document.createElement("li");
        li.innerText = trait;
        toxicListEl.appendChild(li);
      });
    }
    if (financialTextEl) financialTextEl.innerText = roast.financial_sin;
    if (loveTextEl) loveTextEl.innerText = roast.love_red_flag;
    if (quoteTextEl) quoteTextEl.innerText = `"${roast.catchphrase}"`;
    if (tipTextEl) tipTextEl.innerText = roast.survival_tip;
  }
  const pairLoaderPanel = document.getElementById("pair-roast-loader");
  if (pairSignSelectEl) {
    pairSignSelectEl.addEventListener("change", async () => {
      const signB = pairSignSelectEl.value;
      if (!activeSignA || !signB) {
        if (pairRoastResultEl) pairRoastResultEl.classList.add("hidden");
        if (pairLoaderPanel) pairLoaderPanel.classList.add("hidden");
        return;
      }
      if (pairRoastResultEl) pairRoastResultEl.classList.add("hidden");
      if (pairLoaderPanel) pairLoaderPanel.classList.remove("hidden");
      try {
        const response = await fetch(
          `/api/zodiak/roast?sign=${activeSignA}&sign_b=${signB}`,
        );
        if (!response.ok)
          throw new Error("Gagal mengambil data roasting pasangan");
        const data = await response.json();
        const rel = data.relationship_roast;
        setTimeout(() => {
          if (pairLoaderPanel) pairLoaderPanel.classList.add("hidden");
          if (rel && pairRoastResultEl) {
            pairRoastBadgeEl.innerText = rel.badge;
            pairRoastHeadlineEl.innerText = rel.headline;
            pairRoastDescEl.innerText = rel.desc;
            pairRoastVerdictEl.innerText = rel.verdict;
            pairRoastResultEl.classList.remove("hidden");
            if (
              rel &&
              rel.ai_notice &&
              typeof window.showAiQuotaToast === "function"
            ) {
              window.showAiQuotaToast(rel.ai_notice);
            }
          }
        }, 300);
      } catch (err) {
        console.error(err);
        if (pairLoaderPanel) pairLoaderPanel.classList.add("hidden");
        alert("Gagal mengambil roasting hubungan.");
      }
    });
  }
  const btnRollDiceRoast = document.getElementById("btn-roll-dice-roast");
  const btnRollDicePair = document.getElementById("btn-roll-dice-pair");
  if (btnRollDiceRoast) {
    btnRollDiceRoast.addEventListener("click", async () => {
      if (!activeSignA) return;
      btnRollDiceRoast.classList.add("rolling");
      btnRollDiceRoast.disabled = true;
      loaderPanel.classList.remove("hidden");
      contentPanel.classList.add("hidden");
      if (pairCardPanel) pairCardPanel.classList.add("hidden");
      try {
        const response = await fetch(
          `/api/zodiak/roast?sign=${activeSignA}&roll=1`,
        );
        if (!response.ok) throw new Error("Gagal mengacak roasting");
        const data = await response.json();
        setTimeout(() => {
          loaderPanel.classList.add("hidden");
          displayRoastingDetails(data, activeSignA);
          if (
            data.roast &&
            data.roast.ai_notice &&
            typeof window.showAiQuotaToast === "function"
          ) {
            window.showAiQuotaToast(data.roast.ai_notice);
          }
          btnRollDiceRoast.classList.remove("rolling");
          btnRollDiceRoast.disabled = false;
        }, 300);
      } catch (err) {
        console.error(err);
        loaderPanel.classList.add("hidden");
        contentPanel.classList.remove("hidden");
        if (pairCardPanel) pairCardPanel.classList.remove("hidden");
        btnRollDiceRoast.classList.remove("rolling");
        btnRollDiceRoast.disabled = false;
        alert("Gagal mengacak roasting baru.");
      }
    });
  }
  if (btnRollDicePair) {
    btnRollDicePair.addEventListener("click", async () => {
      const signB = pairSignSelectEl ? pairSignSelectEl.value : "";
      if (!activeSignA || !signB) {
        alert("Pilih zodiak pasangan terlebih dahulu!");
        return;
      }
      btnRollDicePair.classList.add("rolling");
      btnRollDicePair.disabled = true;
      if (pairRoastResultEl) pairRoastResultEl.classList.add("hidden");
      if (pairLoaderPanel) pairLoaderPanel.classList.remove("hidden");
      try {
        const response = await fetch(
          `/api/zodiak/roast?sign=${activeSignA}&sign_b=${signB}&roll=1`,
        );
        if (!response.ok) throw new Error("Gagal mengacak roasting pasangan");
        const data = await response.json();
        const rel = data.relationship_roast;
        setTimeout(() => {
          if (pairLoaderPanel) pairLoaderPanel.classList.add("hidden");
          if (rel && pairRoastResultEl) {
            pairRoastBadgeEl.innerText = rel.badge;
            pairRoastHeadlineEl.innerText = rel.headline;
            pairRoastDescEl.innerText = rel.desc;
            pairRoastVerdictEl.innerText = rel.verdict;
            pairRoastResultEl.classList.remove("hidden");
            if (
              rel &&
              rel.ai_notice &&
              typeof window.showAiQuotaToast === "function"
            ) {
              window.showAiQuotaToast(rel.ai_notice);
            }
          }
          btnRollDicePair.classList.remove("rolling");
          btnRollDicePair.disabled = false;
        }, 300);
      } catch (err) {
        console.error(err);
        if (pairLoaderPanel) pairLoaderPanel.classList.add("hidden");
        btnRollDicePair.classList.remove("rolling");
        btnRollDicePair.disabled = false;
        alert("Gagal mengacak roasting pasangan baru.");
      }
    });
  }
});
