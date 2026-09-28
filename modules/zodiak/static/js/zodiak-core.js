(function () {
  const ZODIAC_SYMBOLS = {
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
  const ELEMENT_CLASS = {
    api: "fire",
    tanah: "earth",
    udara: "air",
    air: "water",
  };
  const MOBILE_WIDTH = 968;

  function symbolFor(signKey) {
    return ZODIAC_SYMBOLS[(signKey || "").toLowerCase()] || "✨";
  }

  function setElementBadge(badge, element, baseClass, fallback) {
    if (!badge) return;
    const cssClass = ELEMENT_CLASS[(element || "").toLowerCase()] || fallback || "fire";
    badge.className = `${baseClass} ${cssClass}`;
    badge.innerText = element;
  }

  function bindSpotlight(cards) {
    cards.forEach((card) => {
      let rect = null;
      let ticking = false;
      card.addEventListener("mouseenter", () => {
        rect = card.getBoundingClientRect();
      });
      card.addEventListener("mousemove", (e) => {
        if (!rect) rect = card.getBoundingClientRect();
        if (ticking) return;
        ticking = true;
        window.requestAnimationFrame(() => {
          if (rect) {
            card.style.setProperty("--x", `${e.clientX - rect.left}px`);
            card.style.setProperty("--y", `${e.clientY - rect.top}px`);
          }
          ticking = false;
        });
      });
      card.addEventListener("mouseleave", () => {
        rect = null;
      });
    });
  }

  function scrollToDetailsOnMobile() {
    if (window.innerWidth > MOBILE_WIDTH) return;
    const details = document.querySelector(".details-panel-container");
    if (details) details.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function showLoading(panels) {
    panels.instruction.classList.add("hidden");
    panels.content.classList.add("hidden");
    panels.loader.classList.remove("hidden");
    scrollToDetailsOnMobile();
  }

  function selectCard(cards, card, panels) {
    cards.forEach((c) => c.classList.remove("active"));
    card.classList.add("active");
    showLoading(panels);
  }

  function bindBackToGrid(button) {
    if (!button) return;
    button.addEventListener("click", () => {
      const selector = document.querySelector(".zodiac-selector-container");
      if (selector) selector.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  function animateCount(elementId, targetValue) {
    const element = document.getElementById(elementId);
    if (!element) return;
    let current = 0;
    const stepTime = Math.abs(Math.floor(1000 / Math.max(1, targetValue)));
    const timer = setInterval(() => {
      current += 1;
      element.innerText = `${current}%`;
      if (current >= targetValue) {
        clearInterval(timer);
        element.innerText = `${targetValue}%`;
      }
    }, stepTime);
  }

  function notifyQuota(notice) {
    if (notice) window.showAiQuotaToast(notice);
  }

  function fillList(container, items, itemClass) {
    if (!container) return;
    container.innerHTML = "";
    (items || []).forEach((text) => {
      const node = document.createElement(itemClass ? "span" : "li");
      if (itemClass) node.className = itemClass;
      node.innerText = text;
      container.appendChild(node);
    });
  }

  function setupLogo() {
    const logoTitles = document.querySelectorAll(".logo-title");
    if (!logoTitles.length) return;
    const glyphs = Object.values(ZODIAC_SYMBOLS);
    const popIcons = ["✨", "⭐", "♈", "♌", "💖", "🌟", "🔮", "♒", "♓"];
    let glyphIndex = 0;
    logoTitles.forEach((logoTitle) => {
      const icon = logoTitle.querySelector(".logo-icon");
      if (icon && !logoTitle.querySelector(".logo-icon-wrapper")) {
        const wrapper = document.createElement("span");
        wrapper.className = "logo-icon-wrapper";
        const badge = document.createElement("span");
        badge.className = "cute-zodiac-badge";
        badge.innerText = glyphs[0];
        const sparkleOne = document.createElement("span");
        sparkleOne.className = "cute-sparkle-dot s1";
        sparkleOne.innerText = "✨";
        const sparkleTwo = document.createElement("span");
        sparkleTwo.className = "cute-sparkle-dot s2";
        sparkleTwo.innerText = "⭐";
        icon.parentNode.insertBefore(wrapper, icon);
        wrapper.appendChild(icon);
        wrapper.appendChild(badge);
        wrapper.appendChild(sparkleOne);
        wrapper.appendChild(sparkleTwo);
      }
      logoTitle.addEventListener("click", (e) => {
        const rect = logoTitle.getBoundingClientRect();
        for (let i = 0; i < 7; i++) {
          const particle = document.createElement("span");
          particle.className = "cute-pop-particle";
          particle.innerText = popIcons[Math.floor(Math.random() * popIcons.length)];
          particle.style.left = `${e.clientX - rect.left + (Math.random() * 50 - 25)}px`;
          particle.style.top = `${e.clientY - rect.top + (Math.random() * 20 - 10)}px`;
          logoTitle.appendChild(particle);
          setTimeout(() => particle.remove(), 900);
        }
      });
    });
    setInterval(() => {
      glyphIndex = (glyphIndex + 1) % glyphs.length;
      document.querySelectorAll(".cute-zodiac-badge").forEach((badge) => {
        badge.classList.add("pop-out");
        setTimeout(() => {
          badge.innerText = glyphs[glyphIndex];
          badge.classList.remove("pop-out");
        }, 200);
      });
    }, 1800);
  }

  window.Zodiak = {
    symbolFor: symbolFor,
    setElementBadge: setElementBadge,
    bindSpotlight: bindSpotlight,
    scrollToDetailsOnMobile: scrollToDetailsOnMobile,
    showLoading: showLoading,
    selectCard: selectCard,
    bindBackToGrid: bindBackToGrid,
    animateCount: animateCount,
    notifyQuota: notifyQuota,
    fillList: fillList,
  };

  document.addEventListener("DOMContentLoaded", setupLogo);
})();
