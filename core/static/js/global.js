(function () {
  function getOrCreateDeviceId() {
    let deviceId = "";
    try {
      deviceId = localStorage.getItem("zodiak_device_id") || "";
    } catch (e) {}
    if (!deviceId || deviceId.length < 8) {
      if (window.crypto && window.crypto.randomUUID) {
        deviceId = window.crypto.randomUUID();
      } else {
        deviceId =
          Date.now().toString(36) +
          "_" +
          Math.random().toString(36).substring(2, 10);
      }
      try {
        localStorage.setItem("zodiak_device_id", deviceId);
      } catch (e) {}
    }
    try {
      document.cookie = `_z_device_id=${deviceId}; path=/; max-age=31536000; SameSite=Lax`;
    } catch (e) {}
    return deviceId;
  }
  const deviceId = getOrCreateDeviceId();
  const originalFetch = window.fetch;
  window.fetch = function (url, options) {
    options = options || {};
    options.headers = options.headers || {};
    if (options.headers instanceof Headers) {
      if (!options.headers.has("X-Device-Id")) {
        options.headers.append("X-Device-Id", deviceId);
      }
    } else if (typeof options.headers === "object") {
      if (!options.headers["X-Device-Id"]) {
        options.headers["X-Device-Id"] = deviceId;
      }
    }
    return originalFetch.call(this, url, options);
  };
})();
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
document.addEventListener("DOMContentLoaded", () => {
  window.addEventListener("load", () => {
    setTimeout(() => {
      const loader = document.getElementById("global-loader");
      if (loader) {
        loader.classList.add("hidden");
      }
    }, 500);
  });
  const modeSwitcherToggle = document.getElementById("mode-switcher-toggle");
  const modeSwitcherContainer = document.querySelector(
    ".mode-switcher-container",
  );
  if (modeSwitcherToggle && modeSwitcherContainer) {
    modeSwitcherToggle.addEventListener("click", (e) => {
      e.stopPropagation();
      modeSwitcherContainer.classList.toggle("active");
    });
    document.addEventListener("click", (e) => {
      if (!modeSwitcherContainer.contains(e.target)) {
        modeSwitcherContainer.classList.remove("active");
      }
    });
  }
  const logoTitles = document.querySelectorAll(".logo-title");
  const zodiacSymbols = [
    "♈",
    "♉",
    "♊",
    "♋",
    "♌",
    "♍",
    "♎",
    "♏",
    "♐",
    "♑",
    "♒",
    "♓",
  ];
  let symbolIndex = 0;
  logoTitles.forEach((logoTitle) => {
    const icon = logoTitle.querySelector(".logo-icon");
    if (icon && !logoTitle.querySelector(".logo-icon-wrapper")) {
      const wrapper = document.createElement("span");
      wrapper.className = "logo-icon-wrapper";
      const badge = document.createElement("span");
      badge.className = "cute-zodiac-badge";
      badge.innerText = zodiacSymbols[0];
      const sparkle1 = document.createElement("span");
      sparkle1.className = "cute-sparkle-dot s1";
      sparkle1.innerText = "✨";
      const sparkle2 = document.createElement("span");
      sparkle2.className = "cute-sparkle-dot s2";
      sparkle2.innerText = "⭐";
      icon.parentNode.insertBefore(wrapper, icon);
      wrapper.appendChild(icon);
      wrapper.appendChild(badge);
      wrapper.appendChild(sparkle1);
      wrapper.appendChild(sparkle2);
    }
    logoTitle.addEventListener("click", (e) => {
      const rect = logoTitle.getBoundingClientRect();
      const popIcons = ["✨", "⭐", "♈", "♌", "💖", "🌟", "🔮", "♒", "♓"];
      for (let i = 0; i < 7; i++) {
        const particle = document.createElement("span");
        particle.className = "cute-pop-particle";
        particle.innerText =
          popIcons[Math.floor(Math.random() * popIcons.length)];
        particle.style.left = `${e.clientX - rect.left + (Math.random() * 50 - 25)}px`;
        particle.style.top = `${e.clientY - rect.top + (Math.random() * 20 - 10)}px`;
        logoTitle.appendChild(particle);
        setTimeout(() => particle.remove(), 900);
      }
    });
  });
  if (logoTitles.length > 0) {
    setInterval(() => {
      symbolIndex = (symbolIndex + 1) % zodiacSymbols.length;
      document.querySelectorAll(".cute-zodiac-badge").forEach((badge) => {
        badge.classList.add("pop-out");
        setTimeout(() => {
          badge.innerText = zodiacSymbols[symbolIndex];
          badge.classList.remove("pop-out");
        }, 200);
      });
    }, 1800);
  }
});
