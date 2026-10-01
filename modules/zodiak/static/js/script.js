document.addEventListener("DOMContentLoaded", () => {
  const Zodiak = window.Zodiak;
  const cards = document.querySelectorAll(".zodiac-card");
  const panels = {
    instruction: document.getElementById("details-instruction"),
    loader: document.getElementById("details-loader"),
    content: document.getElementById("details-content"),
  };
  Zodiak.bindSpotlight(cards);
  cards.forEach((card) => {
    card.addEventListener("click", async () => {
      Zodiak.selectCard(cards, card, panels);
      try {
        const data = await window.fetchJson(`/api/zodiak/zodiac/${card.getAttribute("data-sign")}`);
        setTimeout(() => {
          panels.loader.classList.add("hidden");
          displayZodiacDetails(data);
          if (data.genz_readings) Zodiak.notifyQuota(data.genz_readings.ai_notice);
        }, 300);
      } catch (err) {
        panels.loader.classList.add("hidden");
        window.showErrorToast("Gagal mengambil data dari server. Silakan coba lagi.");
      }
    });
  });
  function setText(id, value) {
    document.getElementById(id).innerText = value;
  }
  function displayZodiacDetails(data) {
    panels.content.classList.remove("hidden");
    setText("details-name", data.name);
    setText("details-dates", data.date_range);
    setText("details-ruler", data.ruler);
    setText("details-lucky-number", data.lucky_number);
    setText("details-lucky-color", data.lucky_color);
    setText("details-summary", data.summary);
    if (data.genz_readings) {
      setText("genz-love-text", data.genz_readings.love);
      setText("genz-career-text", data.genz_readings.career);
      setText("genz-health-text", data.genz_readings.health);
    }
    if (data.youtube_track) {
      setText("music-title", data.youtube_track.title);
      setText("music-artist", `by ${data.youtube_track.artist}`);
      setText("music-genre", data.youtube_track.genre || "✨ Cosmic Vibe");
      setText("music-vibe-reason", data.youtube_track.vibe_reason || "");
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
    if (typeof window.getZodiacSvg === "function") {
      document.getElementById("details-symbol").innerHTML = window.getZodiacSvg(signKey, 64);
    } else {
      document.getElementById("details-symbol").innerText = symbols[signKey] || "";
    }
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
      setText("cosmic-date-text", `Ramalan: ${c.date}`);
      setText("cosmic-moon-emoji", c.moon_emoji);
      setText("cosmic-moon-text", `${c.moon_phase} (${c.moon_illumination}%)`);
      const rulerIcon = document.getElementById("cosmic-ruler");
      const rulerText = document.getElementById("cosmic-ruler-text");
      rulerText.innerText = `${data.ruler}: ${c.ruler_status}`;
      const retro = c.ruler_is_retrograde;
      rulerIcon.style.borderColor = retro ? "rgba(239, 68, 68, 0.3)" : "";
      rulerIcon.style.background = retro ? "rgba(239, 68, 68, 0.06)" : "";
      rulerIcon.querySelector("i").style.color = retro ? "#f87171" : "";
      rulerText.style.color = retro ? "#fca5a5" : "";
      setText("cosmic-weather-text", c.weather);
    }
    ["love", "career", "health"].forEach((key) => {
      document.getElementById(`${key}-bar`).style.width = "0%";
      setText(`${key}-percent`, "0%");
    });
    setTimeout(() => {
      ["love", "career", "health"].forEach((key) => {
        document.getElementById(`${key}-bar`).style.width = `${data.ratings[key]}%`;
        Zodiak.animateCount(`${key}-percent`, data.ratings[key]);
      });
    }, 150);
    Zodiak.fillList(document.getElementById("strengths-tags"), data.strengths, "tag");
    Zodiak.fillList(document.getElementById("weaknesses-tags"), data.weaknesses, "tag");
  }
  Zodiak.bindBackToGrid(document.getElementById("btn-back-grid-index"));
});
