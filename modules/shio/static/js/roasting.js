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
  const views = {
    shioList: document.getElementById("view-shio-list"),
    result: document.getElementById("view-result"),
  };
  const roastCard = document.getElementById("roast-card");
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
  document.querySelectorAll(".shio-item").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      document
        .querySelectorAll(".shio-item")
        .forEach((b) => b.classList.remove("selected"));
      e.currentTarget.classList.add("selected");
      fetchRoasting(e.currentTarget.dataset.shio);
    });
  });
  document.getElementById("back-to-start").addEventListener("click", () => {
    roastCard.classList.add("hidden");
    switchView("shioList");
    setTimeout(() => {
      const container = document.querySelector(".shio-content-wrapper");
      if (container)
        container.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 100);
  });
  function fetchRoasting(shioKey) {
    roastCard.classList.add("hidden");
    switchView("result");
    fetch("/api/shio/roasting", {
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
        document.getElementById("r-hanzi").textContent =
          SHIO_HANZI[shioKey] || "";
        document.getElementById("r-shio-name").textContent =
          data.shio_name || "";
        document.getElementById("r-headline").textContent = data.headline || "";
        const traitsList = document.getElementById("r-toxic-traits");
        traitsList.innerHTML = "";
        if (Array.isArray(data.toxic_traits)) {
          data.toxic_traits.forEach((trait) => {
            const li = document.createElement("li");
            li.textContent = trait;
            traitsList.appendChild(li);
          });
        }
        document.getElementById("r-financial-sin").textContent =
          data.financial_sin || "-";
        document.getElementById("r-love-red-flag").textContent =
          data.love_red_flag || "-";
        document.getElementById("r-catchphrase").textContent =
          data.catchphrase || "";
        document.getElementById("r-secret-weakness").textContent =
          data.secret_weakness || "-";
        document.getElementById("r-survival-tip").textContent =
          data.survival_tip || "-";
        roastCard.classList.remove("hidden");
        setTimeout(() => roastCard.scrollIntoView({ behavior: "smooth", block: "start" }), 100);
      })
      .catch((err) => {
        console.error("Gagal mendapatkan data roasting:", err);
        alert("Terjadi gangguan energi kosmik. Silakan coba lagi.");
        switchView("shioList");
      });
  }
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
    class Ember {
      constructor(x, y) {
        this.x = x;
        this.y = y;
        this.size = Math.random() * 4 + 1.5;
        this.speedX = Math.random() * 3 - 1.5;
        this.speedY = -(Math.random() * 3 + 1);
        this.color = Math.random() > 0.4 ? "#ff4500" : "#ffd700";
        this.life = 1.0;
        this.decay = Math.random() * 0.02 + 0.015;
      }
      update() {
        this.x += this.speedX;
        this.y += this.speedY;
        this.speedY += 0.02;
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
    function createEmbers(x, y, count) {
      for (let i = 0; i < count; i++) {
        particles.push(new Ember(x, y));
      }
    }
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (let i = 0; i < particles.length; i++) {
        particles[i].update();
        particles[i].draw();
        if (particles[i].life <= 0) {
          particles.splice(i, 1);
          i--;
        }
      }
      requestAnimationFrame(animate);
    }
    animate();
    let isDragging = false;
    const shioBg = document.getElementById("shio-bg");
    if (shioBg) {
      shioBg.addEventListener("mousedown", (e) => {
        isDragging = true;
        createEmbers(e.clientX, e.clientY, 25);
      });
      shioBg.addEventListener("mousemove", (e) => {
        if (isDragging) createEmbers(e.clientX, e.clientY, 4);
      });
      window.addEventListener("mouseup", () => {
        isDragging = false;
      });
      shioBg.addEventListener("touchstart", (e) => {
        isDragging = true;
        const touch = e.touches[0];
        createEmbers(touch.clientX, touch.clientY, 25);
      });
      shioBg.addEventListener("touchmove", (e) => {
        if (isDragging) {
          const touch = e.touches[0];
          createEmbers(touch.clientX, touch.clientY, 4);
        }
      });
      window.addEventListener("touchend", () => {
        isDragging = false;
      });
    }
    document.querySelectorAll(".shio-item").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const rect = e.currentTarget.getBoundingClientRect();
        createEmbers(rect.left + rect.width / 2, rect.top + rect.height / 2, 30);
      });
    });
  }
});
