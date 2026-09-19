document.addEventListener("DOMContentLoaded", () => {
  const btnCheck = document.getElementById("btn-check");
  const resultEl = document.getElementById("compat-result");
  let birth1 = null;
  let birth2 = null;

  function setupBirthInput(id, onPick) {
    const input = document.getElementById(id);
    if (window.flatpickr) {
      flatpickr(input, {
        dateFormat: "Y-m-d",
        altInput: true,
        altFormat: "j F Y",
        locale: "id",
        maxDate: "today",
        minDate: "1900-01-01",
        onChange: (dates, str) => onPick(str || null),
      });
    } else {
      input.removeAttribute("readonly");
      input.addEventListener("change", () => onPick(input.value || null));
    }
  }
  setupBirthInput("birth-1", (value) => {
    birth1 = value;
    updateButton();
  });
  setupBirthInput("birth-2", (value) => {
    birth2 = value;
    updateButton();
  });
  function updateButton() {
    btnCheck.disabled = !(birth1 && birth2);
  }
  btnCheck.addEventListener("click", () => {
    if (!birth1 || !birth2) return;
    fetchCompatibility();
  });
  function buildYearCard(card, side) {
    while (card.firstChild) card.removeChild(card.firstChild);

    const head = document.createElement("div");
    head.className = "year-head";
    const pillar = document.createElement("span");
    pillar.className = "year-pillar";
    pillar.textContent = side.pillar_hanzi;
    const meta = document.createElement("div");
    const name = document.createElement("span");
    name.className = "dyn-name";
    name.textContent = side.shio_name;
    const nayin = document.createElement("span");
    nayin.className = "dyn-element";
    nayin.textContent = side.nayin.hanzi + " \u00b7 " + side.nayin.name;
    meta.appendChild(name);
    meta.appendChild(nayin);
    head.appendChild(pillar);
    head.appendChild(meta);
    card.appendChild(head);

    const text = document.createElement("p");
    text.className = "dyn-summary";
    text.textContent = side.nayin_relation.text;
    card.appendChild(text);
  }

  function renderYearLayer(layer) {
    const box = document.getElementById("c-year");
    if (!layer) {
      box.classList.add("hidden");
      return;
    }

    document.getElementById("c-year-lichun").textContent = layer.lichun_note;

    const stem = document.getElementById("c-year-stem");
    while (stem.firstChild) stem.removeChild(stem.firstChild);
    stem.className = "compat-year-stem kind-" + layer.stem_relation.kind;
    const badge = document.createElement("span");
    badge.className = "dyn-badge";
    badge.textContent = layer.stem_relation.hanzi + " \u00b7 " + layer.stem_relation.label;
    const stemText = document.createElement("p");
    stemText.className = "dyn-summary";
    stemText.textContent = layer.stem_relation.text;
    stem.appendChild(badge);
    stem.appendChild(stemText);

    buildYearCard(document.getElementById("c-year-1"), layer.shio1);
    buildYearCard(document.getElementById("c-year-2"), layer.shio2);
    box.classList.remove("hidden");
  }

  function buildDynamicCard(card, side) {
    while (card.firstChild) card.removeChild(card.firstChild);
    card.className = "compat-dynamic-card role-" + side.role;

    const head = document.createElement("div");
    head.className = "dyn-head";

    const icon = document.createElement("span");
    icon.className = "dyn-icon";
    icon.textContent = side.icon;
    head.appendChild(icon);

    const meta = document.createElement("div");
    const name = document.createElement("span");
    name.className = "dyn-name";
    name.textContent = side.shio + " " + side.hanzi;
    const element = document.createElement("span");
    element.className = "dyn-element";
    element.textContent = side.element + " " + side.element_hanzi;
    meta.appendChild(name);
    meta.appendChild(element);
    head.appendChild(meta);
    card.appendChild(head);

    const badge = document.createElement("span");
    badge.className = "dyn-badge";
    badge.textContent = side.label;
    card.appendChild(badge);

    const summary = document.createElement("p");
    summary.className = "dyn-summary";
    summary.textContent = side.summary;
    card.appendChild(summary);

    const advice = document.createElement("p");
    advice.className = "dyn-advice";
    advice.textContent = side.advice;
    card.appendChild(advice);
  }

  function renderElementDynamic(dynamic) {
    const box = document.getElementById("c-dynamic");
    if (!dynamic) {
      box.classList.add("hidden");
      return;
    }
    const arrow = document.getElementById("c-dyn-arrow");

    buildDynamicCard(document.getElementById("c-dyn-1"), dynamic.for_shio1);
    buildDynamicCard(document.getElementById("c-dyn-2"), dynamic.for_shio2);

    arrow.textContent = dynamic.for_shio1.arrow;
    arrow.classList.toggle("symmetric", dynamic.symmetric);
    box.classList.remove("hidden");
  }

  function clearNode(node) {
    while (node.firstChild) node.removeChild(node.firstChild);
  }

  function renderRelationBadge(relation, fallbackLabel) {
    const box = document.getElementById("c-relation-badge");
    const plain = document.getElementById("c-relationship");
    if (!relation) {
      box.classList.add("hidden");
      plain.textContent = fallbackLabel || "Data belum tersedia";
      plain.classList.remove("hidden");
      return;
    }
    plain.textContent = "";
    plain.classList.add("hidden");
    box.className = "compat-relation-badge code-" + relation.code;
    document.getElementById("c-relation-hanzi").textContent = relation.hanzi;
    document.getElementById("c-relation-title").textContent =
      relation.label + " \u00b7 " + relation.title;
    document.getElementById("c-relation-note").textContent = relation.note;
  }

  function renderDayPillar(pillar) {
    const box = document.getElementById("c-day-pillar");
    clearNode(box);
    box.className = "compat-day-pillar code-" + pillar.code;

    const head = document.createElement("div");
    head.className = "bazi-head";
    const left = document.createElement("span");
    left.className = "bazi-pillar";
    left.textContent = pillar.pillar1;
    const link = document.createElement("span");
    link.className = "bazi-link";
    link.textContent = pillar.hanzi;
    const right = document.createElement("span");
    right.className = "bazi-pillar";
    right.textContent = pillar.pillar2;
    head.appendChild(left);
    head.appendChild(link);
    head.appendChild(right);
    box.appendChild(head);

    const badge = document.createElement("span");
    badge.className = "dyn-badge";
    badge.textContent = pillar.label + " \u00b7 " + pillar.title;
    box.appendChild(badge);

    const text = document.createElement("p");
    text.className = "dyn-summary";
    text.textContent = pillar.text;
    box.appendChild(text);

    const stem = document.createElement("p");
    stem.className = "bazi-stem kind-" + pillar.stem_kind;
    stem.textContent = pillar.stem_text;
    box.appendChild(stem);
  }

  function buildUsefulSide(side) {
    const card = document.createElement("div");
    card.className = "useful-side";

    const name = document.createElement("span");
    name.className = "useful-side-name";
    name.textContent = side.label + " \u00b7 " + side.pillar;
    card.appendChild(name);

    const element = document.createElement("span");
    element.className = "useful-side-element";
    element.textContent =
      "Elemen diri " + side.element + " " + side.element_hanzi;
    card.appendChild(element);

    const needs = document.createElement("span");
    needs.className = "useful-side-needs";
    needs.textContent = "Butuh " + side.needs.join(" & ");
    card.appendChild(needs);

    const flag = document.createElement("span");
    if (side.supplies) {
      flag.className = "useful-flag give";
      flag.textContent = "Memasok pasangan";
    } else if (side.burdens) {
      flag.className = "useful-flag drain";
      flag.textContent = "Membebani pasangan";
    } else {
      flag.className = "useful-flag flat";
      flag.textContent = "Tidak menambah, tidak mengurangi";
    }
    card.appendChild(flag);

    return card;
  }

  function renderUsefulGod(match) {
    const box = document.getElementById("c-useful");
    clearNode(box);
    box.className = "compat-useful code-" + match.code;

    const head = document.createElement("div");
    head.className = "useful-head";
    const glyph = document.createElement("span");
    glyph.className = "useful-glyph";
    glyph.textContent = "\u7528\u795e";
    const title = document.createElement("span");
    title.className = "useful-title";
    title.textContent = match.title;
    head.appendChild(glyph);
    head.appendChild(title);
    box.appendChild(head);

    const note = document.createElement("p");
    note.className = "dyn-summary";
    note.textContent = match.note;
    box.appendChild(note);

    const grid = document.createElement("div");
    grid.className = "useful-grid";
    grid.appendChild(buildUsefulSide(match.side1));
    grid.appendChild(buildUsefulSide(match.side2));
    box.appendChild(grid);

    const advice = document.createElement("p");
    advice.className = "dyn-advice";
    advice.textContent = match.advice;
    box.appendChild(advice);
  }

  function renderCoupleStars(stars) {
    const box = document.getElementById("c-stars");
    clearNode(box);
    if (!stars || !stars.length) {
      box.classList.add("hidden");
      return;
    }
    stars.forEach((star) => {
      const card = document.createElement("div");
      card.className = "star-card code-" + star.code;

      const head = document.createElement("div");
      head.className = "star-head";
      const icon = document.createElement("span");
      icon.className = "star-icon";
      icon.textContent = star.icon;
      const title = document.createElement("span");
      title.className = "star-title";
      title.textContent = star.title;
      const who = document.createElement("span");
      who.className = "star-who";
      who.textContent = star.who;
      head.appendChild(icon);
      head.appendChild(title);
      head.appendChild(who);
      card.appendChild(head);

      const note = document.createElement("p");
      note.className = "dyn-summary";
      note.textContent = star.note;
      card.appendChild(note);

      box.appendChild(card);
    });
    box.classList.remove("hidden");
  }

  function renderBaziLayer(layer) {
    const box = document.getElementById("c-bazi");
    if (!layer) {
      box.classList.add("hidden");
      return;
    }
    document.getElementById("c-bazi-note").textContent = layer.note;
    renderDayPillar(layer.day_pillar);
    renderUsefulGod(layer.useful_god);
    renderCoupleStars(layer.couple_stars);
    box.classList.remove("hidden");
  }

  function fetchCompatibility() {
    fetch("/api/shio/compatibility", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tanggal1: birth1, tanggal2: birth2 }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.error && !data.shio1) {
          alert(data.error);
          return;
        }
        resultEl.classList.remove("hidden");
        resultEl.classList.remove("animate-in");
        void resultEl.offsetWidth;
        resultEl.classList.add("animate-in");
        const hanzi1 = data.shio1 ? data.shio1.hanzi : "";
        const hanzi2 = data.shio2 ? data.shio2.hanzi : "";
        const name1 = data.shio1 ? data.shio1.name : "";
        const name2 = data.shio2 ? data.shio2.name : "";
        document.getElementById("c-pair").innerHTML = `
                <span class="compat-pair">
                    <span class="compat-pair-hanzi">${hanzi1}</span>
                    <span class="compat-pair-names">${name1} &times; ${name2}</span>
                    <span class="compat-pair-hanzi">${hanzi2}</span>
                </span>
            `;
        const score = data.score || 50;
        const scoreText = document.getElementById("c-score-text");
        const scoreCircle = document.getElementById("c-score-circle");
        
        scoreText.textContent = `0%`;
        scoreCircle.setAttribute("stroke-dasharray", `0, 100`);
        scoreCircle.className.baseVal = "circle";

        if (score >= 70) scoreCircle.classList.add("high");
        else if (score >= 45) scoreCircle.classList.add("mid");
        else scoreCircle.classList.add("low");
        
        let currentScore = 0;
        const duration = 1500;
        const stepTime = Math.max(10, Math.floor(duration / (score || 1)));
        const timer = setInterval(() => {
            currentScore += 1;
            scoreText.textContent = `${currentScore}%`;
            if (currentScore >= score) {
                clearInterval(timer);
                scoreText.textContent = `${score}%`;
            }
        }, stepTime);

        setTimeout(() => {
          scoreCircle.setAttribute("stroke-dasharray", `${score}, 100`);
        }, 50);
        renderRelationBadge(data.pair_relation, data.relationship);
        renderElementDynamic(data.element_dynamic);
        renderYearLayer(data.year_layer);
        renderBaziLayer(data.bazi_layer);

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
