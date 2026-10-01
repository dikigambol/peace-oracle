document.addEventListener("DOMContentLoaded", () => {
  const Zodiak = window.Zodiak;
  const cards = document.querySelectorAll(".zodiac-card");
  const panels = {
    instruction: document.getElementById("gen-instruction"),
    loader: document.getElementById("gen-loader"),
    content: document.getElementById("gen-content"),
  };
  Zodiak.bindSpotlight(cards);
  cards.forEach((card) => {
    card.addEventListener("click", async () => {
      Zodiak.selectCard(cards, card, panels);
      try {
        const data = await window.fetchJson(`/api/zodiak/general/${card.getAttribute("data-sign")}`);
        setTimeout(() => {
          panels.loader.classList.add("hidden");
          displayGeneralDetails(data);
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
  function displayGeneralDetails(data) {
    contentPanel.classList.remove("hidden");
    document.getElementById("gen-name").innerText = data.name;
    document.getElementById("gen-dates").innerText = data.date_range;
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
      document.getElementById("gen-symbol").innerHTML = window.getZodiacSvg(signKey, 64);
    } else {
      document.getElementById("gen-symbol").innerText = symbols[signKey] || "";
    }
    const elementClasses = {
      api: "fire",
      tanah: "earth",
      udara: "air",
      air: "water",
    };
    const elemKey = data.element.toLowerCase();
    const cssClass = elementClasses[elemKey] || "fire";
    const elementBadge = document.getElementById("gen-element-badge");
    elementBadge.className = `details-element-badge element-badge ${cssClass}`;
    elementBadge.innerText = data.element;
    const physicalContainer = document.getElementById("gen-physical-tags");
    physicalContainer.innerHTML = "";
    data.physical_traits.forEach((trait) => {
      const item = document.createElement("div");
      item.className = "physical-trait-item";
      const icon = document.createElement("i");
      icon.className = "fa-solid fa-check-circle";
      const text = document.createElement("span");
      text.innerText = trait;
      item.appendChild(icon);
      item.appendChild(document.createTextNode(" "));
      item.appendChild(text);
      physicalContainer.appendChild(item);
    });
    setText("gen-personality-text", data.personality);
    Zodiak.fillList(document.getElementById("gen-habits-list"), data.habits);
    if (data.animal_soulmate) {
      setText("gen-animal-name", data.animal_soulmate.name);
      setText("gen-animal-desc", data.animal_soulmate.description);
    }
    if (data.cosmic_pantry) {
      setText("gen-pantry-profile", data.cosmic_pantry.taste_profile);
      setText("gen-pantry-food", data.cosmic_pantry.favorite_food);
      setText("gen-pantry-habit", data.cosmic_pantry.food_habit);
    }
    if (data.astro_decor) {
      setText("gen-decor-style", data.astro_decor.style);
      setText("gen-decor-elements", data.astro_decor.key_elements);
      setText("gen-decor-vibe", data.astro_decor.vibe);
    }
    setText("gen-fun-fact-text", data.fun_fact);
  }
  Zodiak.bindBackToGrid(document.getElementById("btn-back-grid-gen"));
});
