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

document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("webgl-bg");
  if (!canvas || typeof THREE === "undefined") return;
  const isMobile = window.matchMedia("(max-width: 768px)").matches;
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000,
  );
  camera.position.z = 400;
  const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    alpha: true,
    antialias: false,
    powerPreference: "high-performance",
  });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, isMobile ? 1 : 1.5));
  const particleCount = isMobile ? 500 : 1200;
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(particleCount * 3);
  const colors = new Float32Array(particleCount * 3);
  const colorPalette = [
    new THREE.Color("#c084fc"),
    new THREE.Color("#f472b6"),
    new THREE.Color("#ffd700"),
    new THREE.Color("#38bdf8"),
    new THREE.Color("#ffffff"),
  ];
  for (let i = 0; i < particleCount; i++) {
    const r = 800 * Math.cbrt(Math.random());
    const theta = Math.random() * 2 * Math.PI;
    const phi = Math.acos(2 * Math.random() - 1);
    const x = r * Math.sin(phi) * Math.cos(theta);
    const y = r * Math.sin(phi) * Math.sin(theta);
    const z = r * Math.cos(phi);
    positions[i * 3] = x;
    positions[i * 3 + 1] = y;
    positions[i * 3 + 2] = z;
    const color = colorPalette[Math.floor(Math.random() * colorPalette.length)];
    colors[i * 3] = color.r;
    colors[i * 3 + 1] = color.g;
    colors[i * 3 + 2] = color.b;
  }
  geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));
  const getTexture = () => {
    const tempCanvas = document.createElement("canvas");
    tempCanvas.width = 16;
    tempCanvas.height = 16;
    const ctx = tempCanvas.getContext("2d");
    const gradient = ctx.createRadialGradient(8, 8, 0, 8, 8, 8);
    gradient.addColorStop(0, "rgba(255,255,255,1)");
    gradient.addColorStop(0.2, "rgba(255,255,255,0.8)");
    gradient.addColorStop(0.5, "rgba(255,255,255,0.2)");
    gradient.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 16, 16);
    const texture = new THREE.Texture(tempCanvas);
    texture.needsUpdate = true;
    return texture;
  };
  const material = new THREE.PointsMaterial({
    size: isMobile ? 3 : 4,
    vertexColors: true,
    map: getTexture(),
    transparent: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
  });
  const particles = new THREE.Points(geometry, material);
  scene.add(particles);
  let mouseX = 0;
  let mouseY = 0;
  let targetX = 0;
  let targetY = 0;
  const windowHalfX = window.innerWidth / 2;
  const windowHalfY = window.innerHeight / 2;
  if (!isMobile) {
    document.addEventListener("mousemove", (event) => {
      mouseX = event.clientX - windowHalfX;
      mouseY = event.clientY - windowHalfY;
    });
  }
  const clock = new THREE.Clock();
  function animate() {
    requestAnimationFrame(animate);
    const elapsedTime = clock.getElapsedTime();
    particles.rotation.y = elapsedTime * 0.03;
    particles.rotation.z = elapsedTime * 0.01;
    if (!isMobile) {
      targetX = mouseX * 0.08;
      targetY = mouseY * 0.08;
      camera.position.x += (targetX - camera.position.x) * 0.02;
      camera.position.y += (-targetY - camera.position.y) * 0.02;
      camera.lookAt(scene.position);
    } else {
      camera.lookAt(scene.position);
    }
    renderer.render(scene, camera);
  }
  const reducedMotion = window.prefersReducedMotion();
  if (reducedMotion) {
    camera.lookAt(scene.position);
    renderer.render(scene, camera);
  } else {
    animate();
  }
  window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    if (reducedMotion) renderer.render(scene, camera);
  });
});
