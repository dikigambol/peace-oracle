document.addEventListener("DOMContentLoaded", () => {
  flatpickr("#daily-date-input", {
    dateFormat: "Y-m-d",
    altInput: true,
    altFormat: "d F Y",
    theme: "dark",
    defaultDate: new Date(),
    onChange: function (selectedDates, dateStr, instance) {
      if (dateStr) fetchDailyAlmanak(dateStr);
    },
  });
  const currentYear = new Date().getFullYear();
  document.getElementById("yearly-subtitle").textContent =
    `Proyeksi Kosmik ${currentYear}`;
  const views = {
    selection: document.getElementById("view-selection"),
    daily: document.getElementById("view-daily"),
  };
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
  const btnDaily = document.getElementById("btn-daily");
  if (btnDaily) {
    btnDaily.addEventListener("click", () => {
      switchView("daily");
      fetchDailyAlmanak();
    });
  }
  document
    .getElementById("back-to-start-from-daily")
    .addEventListener("click", () => switchView("selection"));
  const btnTodayReset = document.getElementById("btn-today-reset");
  if (btnTodayReset) {
    btnTodayReset.addEventListener("click", () => {
      const fp = document.getElementById("daily-date-input")._flatpickr;
      if (fp) {
        fp.setDate(new Date());
      }
      fetchDailyAlmanak();
    });
  }
  const dateWrapper = document.getElementById("daily-date-wrapper");
  if (dateWrapper) {
    dateWrapper.addEventListener("click", () => {
      const fp = document.getElementById("daily-date-input")._flatpickr;
      if (fp) {
        fp.open();
      }
    });
  }
  function fetchDailyAlmanak(dateStr = null) {
    const grid = document.getElementById("daily-grid");
    grid.innerHTML =
      '<div class="loading-cosmic"><i class="fa-solid fa-compass fa-spin-pulse fa-3x"></i><p style="margin-top: 20px; font-family: \'Cinzel\', serif; font-size: 1.2rem; letter-spacing: 2px;">Menyelaraskan Garis Waktu...</p></div>';
    if (!dateStr) {
      const now = new Date();
      dateStr = `${now.getFullYear()}-${(now.getMonth() + 1).toString().padStart(2, "0")}-${now.getDate().toString().padStart(2, "0")}`;
    }
    fetch(`/api/shio/daily?date=${dateStr}`)
      .then((res) => res.json())
      .then((data) => {
        setTimeout(() => {
          document.getElementById("daily-master-name").textContent =
            data.today_shio_name;
          document.getElementById("daily-master-icon").innerHTML =
            `<span class="icon-hanzi">${data.today_shio_hanzi}</span>`;
          document.getElementById("daily-date-str").textContent = data.date_str;
          grid.innerHTML = "";
          data.fortunes.forEach((item, index) => {
            const card = document.createElement("div");
            card.className = `daily-card status-${item.status_code} animate-in`;
            card.style.animationDelay = `${index * 0.08}s`;
            card.innerHTML = `
                            <div class="daily-card-header">
                                <span class="daily-card-icon icon-hanzi">${item.hanzi}</span>
                                <h3 class="daily-card-name">${item.name}</h3>
                            </div>
                            <div class="daily-card-status">${item.status}</div>
                            <p class="daily-card-message">${item.message}</p>
                            ${item.daily_tip ? `<div class="daily-card-tip"><i class="fa-solid fa-lightbulb"></i> <span>${item.daily_tip}</span></div>` : ""}
                        `;
            grid.appendChild(card);
          });
        }, 500);
      })
      .catch((err) => {
        grid.innerHTML =
          '<p style="color:red; text-align:center;">Gagal memuat ramalan harian.</p>';
      });
  }
  const canvas = document.getElementById("particle-canvas");
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
});
