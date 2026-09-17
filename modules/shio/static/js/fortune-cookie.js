document.addEventListener("DOMContentLoaded", () => {
  const SHIO_HANZI = {
    tikus: "鼠",
    kerbau: "牛",
    macan: "虎",
    kelinci: "兔",
    naga: "龍",
    ular: "蛇",
    kuda: "馬",
    kambing: "羊",
    monyet: "猴",
    ayam: "雞",
    anjing: "狗",
    babi: "豬",
  };
  const SHIO_NAMES = {
    tikus: "Tikus",
    kerbau: "Kerbau",
    macan: "Macan",
    kelinci: "Kelinci",
    naga: "Naga",
    ular: "Ular",
    kuda: "Kuda",
    kambing: "Kambing",
    monyet: "Monyet",
    ayam: "Ayam",
    anjing: "Anjing",
    babi: "Babi",
  };
  const views = {
    shioList: document.getElementById("view-shio-list"),
    cookie: document.getElementById("view-cookie"),
  };
  const cookieEl = document.getElementById("cookie");
  const hintEl = document.getElementById("cookie-hint");
  const slipEl = document.getElementById("cookie-slip");
  let pendingCookie = null;
  let isCracked = false;
  let burstCrumbs = () => {};
  function switchView(viewName) {
    Object.values(views).forEach((v) => {
      if (v) {
        v.classList.remove("active");
        v.classList.add("hidden");
      }
    });
    if (views[viewName]) {
      views[viewName].classList.remove("hidden");
      setTimeout(() => views[viewName].classList.add("active"), 10);
    }
  }
  function resetCookie() {
    pendingCookie = null;
    isCracked = false;
    cookieEl.classList.remove("cracked", "shaking");
    hintEl.classList.remove("faded");
    slipEl.classList.add("hidden");
  }
  document.querySelectorAll(".shio-item").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      document
        .querySelectorAll(".shio-item")
        .forEach((b) => b.classList.remove("selected"));
      e.currentTarget.classList.add("selected");
      openCookie(e.currentTarget.dataset.shio);
    });
  });
  document.getElementById("back-to-start").addEventListener("click", () => {
    resetCookie();
    switchView("shioList");
    setTimeout(() => {
      const container = document.querySelector(".shio-content-wrapper");
      if (container)
        container.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 100);
  });
  function openCookie(shioKey) {
    resetCookie();
    document.getElementById("c-hanzi").textContent = SHIO_HANZI[shioKey] || "";
    document.getElementById("c-shio-name").textContent =
      SHIO_NAMES[shioKey] || "";
    switchView("cookie");
    setTimeout(() => {
      const stage = document.getElementById("cookie-stage");
      if (stage) stage.scrollIntoView({ behavior: "smooth", block: "center" });
    }, 100);
    fetch("/api/shio/fortune-cookie", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ shio: shioKey }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
          switchView("shioList");
          return;
        }
        pendingCookie = data;
      })
      .catch((err) => {
        console.error("Gagal mengambil kue keberuntungan:", err);
        alert("Terjadi gangguan energi kosmik. Silakan coba lagi.");
        switchView("shioList");
      });
  }
  cookieEl.addEventListener("click", () => {
    if (isCracked) return;
    if (!pendingCookie) {
      cookieEl.classList.add("shaking");
      setTimeout(() => cookieEl.classList.remove("shaking"), 450);
      return;
    }
    isCracked = true;
    cookieEl.classList.add("shaking");
    setTimeout(() => {
      cookieEl.classList.remove("shaking");
      cookieEl.classList.add("cracked");
      hintEl.classList.add("faded");
      const rect = cookieEl.getBoundingClientRect();
      burstCrumbs(rect.left + rect.width / 2, rect.top + rect.height / 2);
    }, 450);
    setTimeout(() => {
      document.getElementById("c-message").textContent =
        pendingCookie.message || "";
      document.getElementById("c-lucky-item").textContent =
        pendingCookie.lucky_item || "-";
      slipEl.classList.remove("hidden");
      setTimeout(() => slipEl.scrollIntoView({ behavior: "smooth", block: "center" }), 150);
    }, 950);
  });
  const canvas = document.getElementById("particle-canvas");
  if (canvas) {
    const ctx = canvas.getContext("2d");
    let particles = [];
    function resizeCanvas() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();
    class Crumb {
      constructor(x, y) {
        this.x = x;
        this.y = y;
        this.size = Math.random() * 4 + 1.5;
        this.speedX = Math.random() * 8 - 4;
        this.speedY = Math.random() * -5 - 1;
        this.color = Math.random() > 0.45 ? "#ffd700" : "#d9a441";
        this.life = 1.0;
        this.decay = Math.random() * 0.015 + 0.01;
      }
      update() {
        this.x += this.speedX;
        this.y += this.speedY;
        this.speedY += 0.18;
        this.speedX *= 0.99;
        this.life -= this.decay;
      }
      draw() {
        ctx.globalAlpha = Math.max(this.life, 0);
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1.0;
      }
    }
    burstCrumbs = (x, y) => {
      for (let i = 0; i < 45; i++) {
        particles.push(new Crumb(x, y));
      }
    };
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (let i = 0; i < particles.length; i++) {
        particles[i].update();
        particles[i].draw();
        if (particles[i].life <= 0 || particles[i].y > canvas.height + 50) {
          particles.splice(i, 1);
          i--;
        }
      }
      requestAnimationFrame(animate);
    }
    animate();
  }
});
