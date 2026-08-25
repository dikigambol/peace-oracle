document.addEventListener("DOMContentLoaded", () => {
  const views = {
    shioList: document.getElementById("view-shio-list"),
    result: document.getElementById("view-result"),
  };
  let selectedShio = null;
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
      selectedShio = e.currentTarget.dataset.shio;
      fetchFortune(selectedShio);
      const resultCard = document.getElementById("main-fortune-card");
      resultCard.classList.remove("hidden");
      switchView("result");
      setTimeout(() => {
        const container = document.querySelector(".shio-content-wrapper");
        if (container)
          container.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 100);
    });
  });
  document.getElementById("back-to-start").addEventListener("click", () => {
    selectedShio = null;
    switchView("shioList");
  });
  function fetchFortune(shioKey) {
    const payload = { shio: shioKey };
    fetch("/api/shio/guardian", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then((res) => res.json())
      .then((data) => {
        const resTitle = document.getElementById("res-title");
        if (resTitle) {
          resTitle.textContent = data.guardian_name;
          resTitle.style.color = "#ffd700";
        }
        const staticBaseUrl = document
          .querySelector('link[href*="shio.css"]')
          .href.split("css/")[0];
        document.getElementById("res-guardian-icon").src =
          staticBaseUrl + data.guardian_icon;
        document.getElementById("res-guardian-desc").textContent =
          data.guardian_desc;
        document.getElementById("res-mantra").textContent = data.mantra;
        document.getElementById("res-mantra-meaning").textContent =
          data.mantra_meaning;
        document.getElementById("res-guardian-element").textContent =
          data.guardian_element;
        document.getElementById("res-protection").textContent =
          data.protection_advice;
        document.getElementById("res-offering").textContent =
          data.offering_suggestion;
        const fengShuiList = document.getElementById("res-feng-shui");
        fengShuiList.innerHTML = "";
        if (data.feng_shui_tips && Array.isArray(data.feng_shui_tips)) {
          data.feng_shui_tips.forEach((tip) => {
            const li = document.createElement("li");
            li.textContent = tip;
            fengShuiList.appendChild(li);
          });
        }
        document.getElementById("res-pray-time").textContent =
          data.best_pray_time;
        document.getElementById("res-sacred-dir").textContent =
          data.sacred_direction;
        const resultCard = document.getElementById("main-fortune-card");
        resultCard.classList.remove("hidden");
        setTimeout(
          () =>
            resultCard.scrollIntoView({ behavior: "smooth", block: "start" }),
          100,
        );
      })
      .catch((err) => {
        console.error("Gagal mendapatkan data penjaga:", err);
        alert("Terjadi gangguan energi kosmik. Silakan coba lagi.");
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
    class Particle {
      constructor(x, y) {
        this.x = x;
        this.y = y;
        this.size = Math.random() * 5 + 2;
        this.speedX = Math.random() * 6 - 3;
        this.speedY = Math.random() * 6 - 3;
        this.color = Math.random() > 0.5 ? "#ffd700" : "#ff4500";
        this.life = 1.0;
        this.decay = Math.random() * 0.02 + 0.02;
      }
      update() {
        this.x += this.speedX;
        this.y += this.speedY;
        this.life -= this.decay;
      }
      draw() {
        ctx.globalAlpha = this.life;
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1.0;
      }
    }
    function createParticles(x, y) {
      for (let i = 0; i < 30; i++) {
        particles.push(new Particle(x, y));
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
        createParticles(e.clientX, e.clientY);
      });
      shioBg.addEventListener("mousemove", (e) => {
        if (isDragging) {
          for (let i = 0; i < 5; i++) {
            particles.push(new Particle(e.clientX, e.clientY));
          }
        }
      });
      window.addEventListener("mouseup", () => {
        isDragging = false;
      });
      shioBg.addEventListener("touchstart", (e) => {
        isDragging = true;
        const touch = e.touches[0];
        createParticles(touch.clientX, touch.clientY);
      });
      shioBg.addEventListener("touchmove", (e) => {
        if (isDragging) {
          const touch = e.touches[0];
          for (let i = 0; i < 5; i++) {
            particles.push(new Particle(touch.clientX, touch.clientY));
          }
        }
      });
      window.addEventListener("touchend", () => {
        isDragging = false;
      });
    }
  }
});
