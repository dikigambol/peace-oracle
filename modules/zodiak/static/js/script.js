if (!window.showAiQuotaToast) {
  window.showAiQuotaToast = function (message) {
    if (!message) return;
    let toast = document.getElementById("ai-quota-toast");
    if (toast) toast.remove();
    toast = document.createElement("div");
    toast.id = "ai-quota-toast";
    toast.innerHTML = `
            <div class="ai-quota-toast-card">
                <div class="ai-quota-toast-icon">
                    <i class="fa-solid fa-lock"></i>
                </div>
                <div class="ai-quota-toast-msg">${message}</div>
                <button type="button" class="ai-quota-toast-close" onclick="this.closest('#ai-quota-toast').remove()" aria-label="Tutup">&times;</button>
            </div>
        `;
    document.body.appendChild(toast);
    setTimeout(() => {
      if (toast && toast.parentElement) {
        toast.remove();
      }
    }, 7000);
  };
}
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
  const instructionPanel = document.getElementById("details-instruction");
  const loaderPanel = document.getElementById("details-loader");
  const contentPanel = document.getElementById("details-content");
  cards.forEach((card) => {
    card.addEventListener("click", async () => {
      cards.forEach((c) => c.classList.remove("active"));
      card.classList.add("active");
      instructionPanel.classList.add("hidden");
      contentPanel.classList.add("hidden");
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
      const sign = card.getAttribute("data-sign");
      try {
        const response = await fetch(`/api/zodiak/zodiac/${sign}`);
        if (!response.ok) throw new Error("Gagal mengambil data zodiak");
        const data = await response.json();
        setTimeout(() => {
          loaderPanel.classList.add("hidden");
          displayZodiacDetails(data);
          if (data.genz_readings && data.genz_readings.ai_notice) {
            showAiQuotaToast(data.genz_readings.ai_notice);
          }
        }, 300);
      } catch (err) {
        console.error(err);
        loaderPanel.classList.add("hidden");
        alert("Gagal mengambil data dari server. Silakan coba lagi.");
      }
    });
  });
  function displayZodiacDetails(data) {
    contentPanel.classList.remove("hidden");
    document.getElementById("details-name").innerText = data.name;
    document.getElementById("details-dates").innerText = data.date_range;
    document.getElementById("details-ruler").innerText = data.ruler;
    document.getElementById("details-lucky-number").innerText =
      data.lucky_number;
    document.getElementById("details-lucky-color").innerText = data.lucky_color;
    document.getElementById("details-summary").innerText = data.summary;
    if (data.genz_readings) {
      document.getElementById("genz-love-text").innerText =
        data.genz_readings.love;
      document.getElementById("genz-career-text").innerText =
        data.genz_readings.career;
      document.getElementById("genz-health-text").innerText =
        data.genz_readings.health;
    }
    if (data.youtube_track) {
      document.getElementById("music-title").innerText =
        data.youtube_track.title;
      document.getElementById("music-artist").innerText =
        `by ${data.youtube_track.artist}`;
      document.getElementById("music-genre").innerText =
        data.youtube_track.genre || "✨ Cosmic Vibe";
      document.getElementById("music-vibe-reason").innerText =
        data.youtube_track.vibe_reason || "";
      const youtubeBtn = document.getElementById("music-youtube-btn");
      if (youtubeBtn && data.youtube_track.youtube_url) {
        youtubeBtn.href = data.youtube_track.youtube_url;
      }
    }
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
    const signKey = data.name.toLowerCase();
    document.getElementById("details-symbol").innerText =
      symbols[signKey] || "✨";
    const elementClasses = {
      api: "fire",
      tanah: "earth",
      udara: "air",
      air: "water",
    };
    const elemKey = data.element.toLowerCase();
    const cssClass = elementClasses[elemKey] || "fire";
    const elementBadge = document.getElementById("details-element-badge");
    elementBadge.className = `details-element-badge element-badge ${cssClass}`;
    elementBadge.innerText = data.element;
    if (data.cosmic) {
      const c = data.cosmic;
      document.getElementById("cosmic-date-text").innerText =
        `Ramalan: ${c.date}`;
      document.getElementById("cosmic-moon-emoji").innerText = c.moon_emoji;
      document.getElementById("cosmic-moon-text").innerText =
        `${c.moon_phase} (${c.moon_illumination}%)`;
      const rulerIcon = document.getElementById("cosmic-ruler");
      document.getElementById("cosmic-ruler-text").innerText =
        `${data.ruler}: ${c.ruler_status}`;
      if (c.ruler_is_retrograde) {
        rulerIcon.style.borderColor = "rgba(239, 68, 68, 0.3)";
        rulerIcon.style.background = "rgba(239, 68, 68, 0.06)";
        rulerIcon.querySelector("i").style.color = "#f87171";
        document.getElementById("cosmic-ruler-text").style.color = "#fca5a5";
      } else {
        rulerIcon.style.borderColor = "";
        rulerIcon.style.background = "";
        rulerIcon.querySelector("i").style.color = "";
        document.getElementById("cosmic-ruler-text").style.color = "";
      }
      document.getElementById("cosmic-weather-text").innerText = c.weather;
    }
    const loveBar = document.getElementById("love-bar");
    const careerBar = document.getElementById("career-bar");
    const healthBar = document.getElementById("health-bar");
    loveBar.style.width = "0%";
    careerBar.style.width = "0%";
    healthBar.style.width = "0%";
    document.getElementById("love-percent").innerText = "0%";
    document.getElementById("career-percent").innerText = "0%";
    document.getElementById("health-percent").innerText = "0%";
    setTimeout(() => {
      loveBar.style.width = `${data.ratings.love}%`;
      careerBar.style.width = `${data.ratings.career}%`;
      healthBar.style.width = `${data.ratings.health}%`;
      animateCount("love-percent", data.ratings.love);
      animateCount("career-percent", data.ratings.career);
      animateCount("health-percent", data.ratings.health);
    }, 150);
    const strengthsContainer = document.getElementById("strengths-tags");
    const weaknessesContainer = document.getElementById("weaknesses-tags");
    strengthsContainer.innerHTML = "";
    weaknessesContainer.innerHTML = "";
    data.strengths.forEach((strength) => {
      const tag = document.createElement("span");
      tag.className = "tag";
      tag.innerText = strength;
      strengthsContainer.appendChild(tag);
    });
    data.weaknesses.forEach((weakness) => {
      const tag = document.createElement("span");
      tag.className = "tag";
      tag.innerText = weakness;
      weaknessesContainer.appendChild(tag);
    });
  }
  const btnBackIndex = document.getElementById("btn-back-grid-index");
  if (btnBackIndex) {
    btnBackIndex.addEventListener("click", () => {
      const zodiacGrid = document.getElementById("zodiac-grid");
      if (zodiacGrid) {
        zodiacGrid.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  }
  function animateCount(elementId, targetValue) {
    const element = document.getElementById(elementId);
    let current = 0;
    const duration = 1000;
    const stepTime = Math.abs(Math.floor(duration / targetValue));
    const timer = setInterval(() => {
      current += 1;
      element.innerText = `${current}%`;
      if (current >= targetValue) {
        clearInterval(timer);
        element.innerText = `${targetValue}%`;
      }
    }, stepTime);
  }
});
