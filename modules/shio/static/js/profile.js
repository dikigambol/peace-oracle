document.addEventListener("DOMContentLoaded", () => {
  const views = {
    shioList: document.getElementById("view-shio-list"),
    profile: document.getElementById("view-profile"),
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
  document.querySelectorAll(".shio-item").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const shioKey = e.currentTarget.dataset.shio;
      fetchProfile(shioKey);
      switchView("profile");
    });
  });
  document
    .getElementById("back-to-select")
    .addEventListener("click", () => switchView("shioList"));
  const elementNames = {
    kayu: "Kayu 🌳",
    api: "Api 🔥",
    tanah: "Tanah ⛰️",
    logam: "Logam ⚙️",
    air: "Air 💧",
  };
  function fetchProfile(shioKey) {
    fetch("/api/shio/profile", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ shio: shioKey }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
          return;
        }
        const card = document.getElementById("profile-card");
        card.classList.remove("hidden");
        document.getElementById("p-icon").textContent = data.icon || "";
        document.getElementById("p-hanzi").textContent = data.hanzi || "";
        document.getElementById("p-name").textContent = data.name || "";
        document.getElementById("p-branch").textContent =
          data.earthly_branch || "";
        document.getElementById("p-yinyang").textContent = data.yin_yang || "";
        document.getElementById("p-element").textContent =
          `Elemen: ${data.fixed_element || ""}`;
        const traitsPosEl = document.getElementById("p-traits-pos");
        const traitsNegEl = document.getElementById("p-traits-neg");
        traitsPosEl.innerHTML = "";
        traitsNegEl.innerHTML = "";
        (data.traits_positive || []).forEach((t) => {
          traitsPosEl.innerHTML += `<span class="trait-tag trait-positive">${t}</span>`;
        });
        (data.traits_negative || []).forEach((t) => {
          traitsNegEl.innerHTML += `<span class="trait-tag trait-negative">${t}</span>`;
        });
        const persEl = document.getElementById("p-personality");
        persEl.innerHTML = "";
        if (data.personality_long) {
          data.personality_long.split("\n").forEach((p) => {
            if (p.trim()) persEl.innerHTML += `<p>${p.trim()}</p>`;
          });
        }
        const greenEl = document.getElementById("p-green-flags");
        greenEl.innerHTML = "";
        (data.green_flags || []).forEach((f) => {
          greenEl.innerHTML += `<li>${f}</li>`;
        });
        const redEl = document.getElementById("p-red-flags");
        redEl.innerHTML = "";
        (data.red_flags || []).forEach((f) => {
          redEl.innerHTML += `<li>${f}</li>`;
        });
        const luckyGrid = document.getElementById("p-lucky-grid");
        luckyGrid.innerHTML = "";
        const luckyItems = [
          { label: "Warna Hoki", value: (data.lucky_colors || []).join(", ") },
          {
            label: "Warna Sial",
            value: (data.unlucky_colors || []).join(", "),
          },
          { label: "Angka Hoki", value: (data.lucky_numbers || []).join(", ") },
          {
            label: "Angka Sial",
            value: (data.unlucky_numbers || []).join(", "),
          },
          { label: "Bunga Hoki", value: (data.lucky_flowers || []).join(", ") },
          {
            label: "Bulan Terbaik",
            value: (data.best_months || []).join(", "),
          },
          {
            label: "Bulan Terburuk",
            value: (data.worst_months || []).join(", "),
          },
        ];
        luckyItems.forEach((item) => {
          if (item.value) {
            luckyGrid.innerHTML += `
                        <div class="lucky-item">
                            <div class="lucky-label">${item.label}</div>
                            <div class="lucky-value">${item.value}</div>
                        </div>`;
          }
        });
        const careerEl = document.getElementById("p-career");
        careerEl.innerHTML = "";
        (data.ideal_career || []).forEach((c) => {
          careerEl.innerHTML += `<span class="trait-tag trait-positive">${c}</span>`;
        });
        document.getElementById("p-health").textContent =
          data.health_warning || "";
        document.getElementById("p-spirit").textContent =
          data.spirit_advice || "";
        const alterEl = document.getElementById("p-alter-ego");
        alterEl.innerHTML = "";
        const alterData = data.alter_ego || {};
        Object.keys(alterData).forEach((elem) => {
          const ego = alterData[elem];
          if (ego && ego.title) {
            alterEl.innerHTML += `
                        <div class="alter-ego-card">
                            <div class="ego-element">${elementNames[elem] || elem}</div>
                            <div class="ego-title">${ego.title}</div>
                            <div class="ego-desc">${ego.desc || ""}</div>
                        </div>`;
          }
        });
        const famousEl = document.getElementById("p-famous");
        famousEl.innerHTML = "";
        (data.famous_people || []).forEach((p) => {
          famousEl.innerHTML += `<span class="famous-tag">${p}</span>`;
        });
        setTimeout(() => {
          const wrapper = document.querySelector(".shio-content-wrapper");
          if (wrapper)
            wrapper.scrollIntoView({ behavior: "smooth", block: "start" });
        }, 100);
      })
      .catch((err) => {
        console.error("Gagal memuat profil:", err);
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
