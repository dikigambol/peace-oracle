document.addEventListener("DOMContentLoaded", () => {
  let shio1 = null;
  let shio2 = null;
  const btnCheck = document.getElementById("btn-check");
  const resultEl = document.getElementById("compat-result");
  function setupPicker(pickerId, callback) {
    const picker = document.getElementById(pickerId);
    picker.querySelectorAll(".shio-pick").forEach((el) => {
      el.addEventListener("click", () => {
        picker
          .querySelectorAll(".shio-pick")
          .forEach((p) => p.classList.remove("selected"));
        el.classList.add("selected");
        callback(el.dataset.shio);
        updateButton();
      });
    });
  }
  setupPicker("picker-1", (key) => {
    shio1 = key;
  });
  setupPicker("picker-2", (key) => {
    shio2 = key;
  });
  function updateButton() {
    btnCheck.disabled = !(shio1 && shio2);
  }
  btnCheck.addEventListener("click", () => {
    if (!shio1 || !shio2) return;
    fetchCompatibility(shio1, shio2);
  });
  function fetchCompatibility(s1, s2) {
    fetch("/api/shio/compatibility", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ shio1: s1, shio2: s2 }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.error && !data.shio1) {
          alert(data.error);
          return;
        }
        resultEl.classList.remove("hidden");
        const hanzi1 = data.shio1 ? data.shio1.hanzi : "";
        const hanzi2 = data.shio2 ? data.shio2.hanzi : "";
        const name1 = data.shio1 ? data.shio1.name : "";
        const name2 = data.shio2 ? data.shio2.name : "";
        document.getElementById("c-pair").innerHTML = `
                <span style="display:inline-flex; align-items:center; gap:12px; font-family:'Cinzel', serif; font-size:1.8rem; font-weight:bold;">
                    <span style="display:inline-flex; align-items:center; justify-content:center; width:40px; height:40px; border:2px solid #ffd700; border-radius:50%; font-size:1.6rem; color:#ffd700; box-shadow:0 0 10px rgba(255,215,0,0.5), inset 0 0 8px rgba(255,215,0,0.3); font-family: 'Noto Serif TC', serif; background: rgba(0,0,0,0.3); text-shadow: 0 0 5px rgba(255,215,0,0.8);">${hanzi1}</span>
                    <span style="color:#fff; text-shadow: 0 0 10px rgba(255,255,255,0.3);">${name1} &times; ${name2}</span>
                    <span style="display:inline-flex; align-items:center; justify-content:center; width:40px; height:40px; border:2px solid #ffd700; border-radius:50%; font-size:1.6rem; color:#ffd700; box-shadow:0 0 10px rgba(255,215,0,0.5), inset 0 0 8px rgba(255,215,0,0.3); font-family: 'Noto Serif TC', serif; background: rgba(0,0,0,0.3); text-shadow: 0 0 5px rgba(255,215,0,0.8);">${hanzi2}</span>
                </span>
            `;
        document.getElementById("c-relationship").textContent =
          data.relationship || "Data belum tersedia";
        const score = data.score || 50;
        const scoreText = document.getElementById("c-score-text");
        const scoreFill = document.getElementById("c-score-fill");
        scoreText.textContent = `${score}/100`;
        scoreFill.style.width = "0%";
        scoreFill.className = "score-fill";
        if (score >= 70) scoreFill.classList.add("high");
        else if (score >= 45) scoreFill.classList.add("mid");
        else scoreFill.classList.add("low");
        setTimeout(() => {
          scoreFill.style.width = `${score}%`;
          scoreFill.textContent = `${score}%`;
        }, 100);
        document.getElementById("c-asmara").textContent = data.asmara || "-";
        document.getElementById("c-bisnis").textContent = data.bisnis || "-";
        document.getElementById("c-drama").textContent = data.drama || "-";
        document.getElementById("c-tips").textContent = data.tips || "-";
        setTimeout(() => {
          resultEl.scrollIntoView({ behavior: "smooth", block: "start" });
        }, 200);
      })
      .catch((err) => {
        console.error("Gagal memuat kompatibilitas:", err);
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
