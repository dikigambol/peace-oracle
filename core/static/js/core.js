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
const TOAST_ICONS = {
  quota: "fa-solid fa-lock",
  error: "fa-solid fa-triangle-exclamation",
  info: "fa-solid fa-circle-info",
};

window.showToast = function (message, variant) {
  if (!message) return;
  let toast = document.getElementById("ai-quota-toast");
  if (toast) toast.remove();
  toast = document.createElement("div");
  toast.id = "ai-quota-toast";
  const card = document.createElement("div");
  card.className = "ai-quota-toast-card";
  if (variant && variant !== "quota") {
    card.classList.add("toast-" + variant);
  }
  const icon = document.createElement("div");
  icon.className = "ai-quota-toast-icon";
  const lock = document.createElement("i");
  lock.className = TOAST_ICONS[variant] || TOAST_ICONS.quota;
  icon.appendChild(lock);
  const msg = document.createElement("div");
  msg.className = "ai-quota-toast-msg";
  msg.textContent = message;
  const close = document.createElement("button");
  close.type = "button";
  close.className = "ai-quota-toast-close";
  close.setAttribute("aria-label", "Tutup");
  close.textContent = "\u00d7";
  close.addEventListener("click", () => toast.remove());
  card.appendChild(icon);
  card.appendChild(msg);
  card.appendChild(close);
  toast.appendChild(card);
  document.body.appendChild(toast);
  setTimeout(() => {
    if (toast && toast.parentElement) {
      toast.remove();
    }
  }, 7000);
};

window.showAiQuotaToast = function (message) {
  window.showToast(message, "quota");
};

window.prefersReducedMotion = function () {
  return Boolean(
    window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches
  );
};

window.showErrorToast = function (message) {
  window.showToast(message || "Energi kosmiknya lagi terganggu. Coba lagi ya.", "error");
};

window.initDatePicker = function (selector, options) {
  const input = document.querySelector(selector);
  if (!input) return;
  if (typeof window.flatpickr !== "function") {
    input.removeAttribute("readonly");
    input.type = "date";
    if (options && typeof options.onChange === "function") {
      input.addEventListener("change", () => {
        options.onChange([], input.value);
      });
    }
    return;
  }
  window.flatpickr(input, options || {});
};

window.fetchJson = async function (url, options) {
  const res = await fetch(url, options);
  let payload = null;
  try {
    payload = await res.json();
  } catch (e) {
    throw new Error("Jawaban server tidak terbaca (status " + res.status + ").");
  }
  if (!res.ok) {
    throw new Error(
      (payload && payload.error) || "Server menolak permintaan (status " + res.status + ")."
    );
  }
  return payload;
};

window.setButtonLoading = function (button, isLoading, labelWhenLoading, disabledAfter) {
  if (!button) return;
  if (isLoading) {
    if (!button.dataset.idleHtml) {
      button.dataset.idleHtml = button.innerHTML;
    }
    button.disabled = true;
    button.classList.add("loading");
    button.innerHTML =
      '<i class="fa-solid fa-circle-notch fa-spin"></i> ' +
      (labelWhenLoading || "Membaca energi...");
  } else {
    button.disabled = Boolean(disabledAfter);
    button.classList.remove("loading");
    if (button.dataset.idleHtml) {
      button.innerHTML = button.dataset.idleHtml;
    }
  }
};

function initPageLoader() {
  const loader = document.getElementById("global-loader");
  if (!loader) return;
  const fill = loader.querySelector(".pl-fill");
  const percent = loader.querySelector(".pl-percent");
  const reduceMotion = window.prefersReducedMotion();
  const startedAt = performance.now();
  const pendingImages = Array.from(document.images).filter((img) => !img.complete);
  const totalAssets = pendingImages.length + 1;
  let settledAssets = 0;
  let pageLoaded = document.readyState === "complete";
  let shown = 0;
  let finished = false;

  const settle = () => {
    settledAssets += 1;
  };
  pendingImages.forEach((img) => {
    img.addEventListener("load", settle, { once: true });
    img.addEventListener("error", settle, { once: true });
  });
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(settle, settle);
  } else {
    settle();
  }

  const render = (value) => {
    const rounded = Math.round(value);
    if (fill) fill.style.transform = `scaleX(${value / 100})`;
    if (percent) percent.textContent = `${rounded}%`;
    loader.setAttribute("aria-valuenow", String(rounded));
  };
  const finish = (delay) => {
    finished = true;
    render(100);
    setTimeout(() => loader.classList.add("hidden"), delay);
  };
  const tick = (now) => {
    if (finished) return;
    let target = 100;
    if (!pageLoaded) {
      const timeFloor = 90 * (1 - Math.exp(-(now - startedAt) / 900));
      const assetProgress = 15 + 75 * (settledAssets / totalAssets);
      target = Math.min(90, Math.max(assetProgress, timeFloor));
    }
    const easing = reduceMotion ? 1 : pageLoaded ? 0.2 : 0.12;
    shown = Math.max(shown, shown + (target - shown) * easing);
    if (target === 100 && shown > 99.5) {
      finish(200);
      return;
    }
    render(shown);
    requestAnimationFrame(tick);
  };

  window.addEventListener("load", () => {
    pageLoaded = true;
  }, { once: true });
  window.addEventListener("pageshow", (event) => {
    if (event.persisted) finish(0);
  });
  setTimeout(() => {
    pageLoaded = true;
  }, 8000);
  requestAnimationFrame(tick);
}

document.addEventListener("DOMContentLoaded", () => {
  initPageLoader();
  const modeSwitcherToggle = document.getElementById("mode-switcher-toggle");
  const modeSwitcherContainer = document.querySelector(
    ".mode-switcher-container",
  );
  if (modeSwitcherToggle && modeSwitcherContainer) {
    const setOpen = (open) => {
      modeSwitcherContainer.classList.toggle("active", open);
      modeSwitcherToggle.setAttribute("aria-expanded", String(open));
    };
    modeSwitcherToggle.addEventListener("click", (e) => {
      e.stopPropagation();
      setOpen(!modeSwitcherContainer.classList.contains("active"));
    });
    document.addEventListener("click", (e) => {
      if (!modeSwitcherContainer.contains(e.target)) setOpen(false);
    });
    document.addEventListener("keydown", (e) => {
      if (e.key !== "Escape" || !modeSwitcherContainer.classList.contains("active")) return;
      setOpen(false);
      modeSwitcherToggle.focus();
    });
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const sky = document.querySelector(".co-sky");
  const canvas = document.getElementById("co-stars");
  const context = canvas && canvas.getContext("2d");
  if (!sky || !context) return;
  const astrolabe = sky.querySelector(".co-astrolabe");
  const spin = (running) => {
    if (!astrolabe || !astrolabe.pauseAnimations) return;
    if (running) astrolabe.unpauseAnimations();
    else astrolabe.pauseAnimations();
  };
  const isMobile = window.matchMedia("(max-width: 768px)").matches;
  const reducedMotion = window.prefersReducedMotion();
  const ratio = Math.min(window.devicePixelRatio || 1, 1.5);
  const palette = ["241, 230, 207", "226, 197, 130", "214, 164, 70", "255, 255, 255"];
  const stars = Array.from({ length: isMobile ? 80 : 160 }, () => {
    const bright = Math.random() < 0.08;
    return {
      x: Math.random(),
      y: Math.random(),
      size: bright ? 1.4 + Math.random() * 0.8 : 0.5 + Math.random() * 0.8,
      bright,
      color: palette[Math.floor(Math.random() * palette.length)],
      speed: 0.3 + Math.random() * 1.2,
      phase: Math.random() * Math.PI * 2,
      depth: 0.3 + Math.random() * 0.7,
    };
  });
  const pointer = { x: 0, y: 0 };
  const offset = { x: 0, y: 0 };
  let width = 0;
  let height = 0;
  let frame = 0;
  const resize = () => {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
  };
  const draw = (time) => {
    context.clearRect(0, 0, width, height);
    stars.forEach((star) => {
      const glow = reducedMotion ? 0.75 : 0.35 + 0.65 * Math.abs(Math.sin(time * 0.0006 * star.speed + star.phase));
      const x = star.x * width - offset.x * 6 * star.depth;
      const y = star.y * height - offset.y * 6 * star.depth;
      context.fillStyle = `rgba(${star.color}, ${(glow * 0.85).toFixed(3)})`;
      context.beginPath();
      context.arc(x, y, star.size, 0, Math.PI * 2);
      context.fill();
      if (!star.bright) return;
      const reach = star.size * 5 * glow;
      context.strokeStyle = `rgba(${star.color}, ${(glow * 0.4).toFixed(3)})`;
      context.lineWidth = 0.6;
      context.beginPath();
      context.moveTo(x - reach, y);
      context.lineTo(x + reach, y);
      context.moveTo(x, y - reach);
      context.lineTo(x, y + reach);
      context.stroke();
    });
  };
  const loop = (time) => {
    offset.x += (pointer.x - offset.x) * 0.04;
    offset.y += (pointer.y - offset.y) * 0.04;
    draw(time);
    frame = requestAnimationFrame(loop);
  };
  resize();
  if (reducedMotion) {
    spin(false);
    if (astrolabe && astrolabe.setCurrentTime) astrolabe.setCurrentTime(0);
    draw(0);
    window.addEventListener("resize", () => {
      resize();
      draw(0);
    });
    return;
  }
  if (!isMobile) {
    document.addEventListener("mousemove", (event) => {
      pointer.x = (event.clientX / width) * 2 - 1;
      pointer.y = (event.clientY / height) * 2 - 1;
    });
  }
  window.addEventListener("resize", resize);
  document.addEventListener("visibilitychange", () => {
    cancelAnimationFrame(frame);
    spin(!document.hidden);
    if (!document.hidden) frame = requestAnimationFrame(loop);
  });
  frame = requestAnimationFrame(loop);
});
