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
  const rerollBtn = document.getElementById("roast-reroll");
  const rerollCount = document.getElementById("roast-reroll-count");
  let current = null;
  let lastVariant = -1;

  function pickVariant(total) {
    if (total < 2) return 0;
    let index = lastVariant;
    while (index === lastVariant) {
      index = Math.floor(Math.random() * total);
    }
    lastVariant = index;
    return index;
  }

  const lastPick = {};

  function pickFrom(key, pool) {
    if (!Array.isArray(pool) || !pool.length) return "-";
    if (pool.length === 1) return pool[0];
    let index = lastPick[key];
    const sebelumnya = index;
    while (index === sebelumnya) {
      index = Math.floor(Math.random() * pool.length);
    }
    lastPick[key] = index;
    return pool[index];
  }

  function drawTraits(pool, count) {
    const copy = pool.slice();
    for (let i = copy.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy.slice(0, Math.min(count, copy.length));
  }

  function renderRoast(shioKey) {
    const data = current;
    const variants = data.variants || [];
    const variant = variants[pickVariant(variants.length)] || {};
    const pool = Array.isArray(data.toxic_traits) ? data.toxic_traits : [];
    const traits = drawTraits(pool, data.traits_per_draw || 8);

    document.getElementById("r-hanzi").textContent = SHIO_HANZI[shioKey] || "";
    document.getElementById("r-shio-name").textContent = data.shio_name || "";
    document.getElementById("r-headline").textContent = variant.headline || "";

    const traitsList = document.getElementById("r-toxic-traits");
    while (traitsList.firstChild) traitsList.removeChild(traitsList.firstChild);
    traits.forEach((trait) => {
      const li = document.createElement("li");
      li.textContent = trait;
      traitsList.appendChild(li);
    });

    document.getElementById("r-financial-sin").textContent = pickFrom(
      "sin",
      data.financial_sins
    );
    document.getElementById("r-love-red-flag").textContent = pickFrom(
      "flag",
      data.love_red_flags
    );
    document.getElementById("r-catchphrase").textContent =
      variant.catchphrase || "";
    document.getElementById("r-secret-weakness").textContent = pickFrom(
      "weak",
      data.secret_weaknesses
    );
    document.getElementById("r-survival-tip").textContent =
      variant.survival_tip || "-";

    rerollCount.textContent = variants.length
      ? "versi " + (lastVariant + 1) + " dari " + variants.length
      : "";
    rerollBtn.classList.toggle(
      "hidden",
      variants.length < 2 && pool.length <= (data.traits_per_draw || 8)
    );
  }

  if (rerollBtn) {
    rerollBtn.addEventListener("click", () => {
      if (!current || !current.shioKey) return;
      renderRoast(current.shioKey);
      roastCard.classList.remove("roast-flash");
      void roastCard.offsetWidth;
      roastCard.classList.add("roast-flash");
    });
  }
  const pairBody = document.getElementById("pair-body");
  const pairToggle = document.getElementById("pair-toggle");
  const pairPicker = document.getElementById("pair-picker");
  const pairCard = document.getElementById("pair-card");

  function buildPairPicker() {
    while (pairPicker.firstChild) pairPicker.removeChild(pairPicker.firstChild);
    Object.keys(SHIO_HANZI).forEach((key) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "pair-pick";
      btn.dataset.shio = key;
      const glyph = document.createElement("span");
      glyph.className = "pair-pick-hanzi";
      glyph.textContent = SHIO_HANZI[key];
      const label = document.createElement("span");
      label.className = "pair-pick-name";
      label.textContent = key.charAt(0).toUpperCase() + key.slice(1);
      btn.appendChild(glyph);
      btn.appendChild(label);
      btn.addEventListener("click", () => {
        pairPicker
          .querySelectorAll(".pair-pick")
          .forEach((b) => b.classList.remove("selected"));
        btn.classList.add("selected");
        fetchPairRoast(key);
      });
      pairPicker.appendChild(btn);
    });
  }

  function renderPairRoast(pair) {
    if (!pair) {
      pairCard.classList.add("hidden");
      return;
    }
    document.getElementById("p-hanzi-1").textContent = pair.shio1.hanzi;
    document.getElementById("p-hanzi-2").textContent = pair.shio2.hanzi;
    document.getElementById("p-rel").textContent =
      pair.relation_hanzi + " " + pair.relation_label;
    document.getElementById("p-verdict").textContent = pair.verdict;
    document.getElementById("p-roast").textContent = pair.roast;
    document.getElementById("p-tip").textContent = pair.tip;
    pairCard.className = "roast-pair-card code-" + pair.code;
    pairCard.classList.remove("roast-flash");
    void pairCard.offsetWidth;
    pairCard.classList.add("roast-flash");
  }

  function fetchPairRoast(partnerKey) {
    if (!current || !current.shioKey) return;
    fetch("/api/shio/roasting", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ shio: current.shioKey, pasangan: partnerKey }),
    })
      .then((res) => res.json())
      .then((data) => renderPairRoast(data.pair_roast))
      .catch(() => {
        alert("Gagal memuat roasting pasangan. Coba lagi.");
      });
  }

  if (pairToggle) {
    pairToggle.addEventListener("click", () => {
      pairBody.classList.toggle("hidden");
      pairToggle.classList.toggle("open", !pairBody.classList.contains("hidden"));
    });
  }

  function resetPairRoast() {
    pairBody.classList.add("hidden");
    pairToggle.classList.remove("open");
    pairCard.classList.add("hidden");
    pairPicker
      .querySelectorAll(".pair-pick")
      .forEach((b) => b.classList.remove("selected"));
  }

  const dmDate = document.getElementById("dm-date");
  const chartBox = document.getElementById("chart-roast");
  const dirCard = document.getElementById("dir-card");
  let dmValue = null;
  let genderValue = null;

  document.querySelectorAll(".roast-gender-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const sudah = btn.classList.contains("selected");
      document
        .querySelectorAll(".roast-gender-btn")
        .forEach((b) => b.classList.remove("selected"));
      if (sudah) {
        genderValue = null;
      } else {
        btn.classList.add("selected");
        genderValue = btn.dataset.gender;
      }
    });
  });

  function renderChartRoast(chart) {
    if (!chart) {
      chartBox.classList.add("hidden");
      return;
    }

    const ringkas = document.getElementById("chart-summary");
    while (ringkas.firstChild) ringkas.removeChild(ringkas.firstChild);
    [
      [chart.year_pillar, "Pilar tahun"],
      [chart.shio_hanzi + " " + chart.shio_name, "Shio dari tanggal"],
      [chart.year_element + " " + chart.year_polarity, "Elemen tahun"],
    ].forEach(([nilai, label]) => {
      const sel = document.createElement("div");
      sel.className = "chart-cell";
      const v = document.createElement("span");
      v.className = "chart-value";
      v.textContent = nilai;
      const l = document.createElement("span");
      l.className = "chart-label";
      l.textContent = label;
      sel.appendChild(v);
      sel.appendChild(l);
      ringkas.appendChild(sel);
    });

    const koreksi = document.getElementById("chart-correction");
    while (koreksi.firstChild) koreksi.removeChild(koreksi.firstChild);
    if (chart.correction) {
      const p = document.createElement("p");
      p.textContent =
        "Tanggal itu jatuh di pilar " + chart.correction.pillar + ", jadi shiomu " +
        chart.correction.actual + ", bukan " + chart.correction.picked +
        ". Batas awal musim semi (立春) sering bikin kelahiran Januari salah shio.";
      koreksi.appendChild(p);
      koreksi.classList.remove("hidden");
    } else {
      koreksi.classList.add("hidden");
    }

    const dm = chart.day_master;
    document.getElementById("dm-hanzi").textContent = dm.stem_hanzi;
    document.getElementById("dm-title").textContent =
      dm.pillar_hanzi + " \u00b7 " + dm.title;
    document.getElementById("dm-headline").textContent = dm.headline;
    document.getElementById("dm-roast").textContent = dm.roast;
    document.getElementById("dm-tip").textContent = dm.tip;

    if (chart.direction) {
      const a = chart.direction;
      document.getElementById("dir-hanzi").textContent = a.direction_hanzi;
      document.getElementById("dir-title").textContent =
        a.direction_label + " \u00b7 batang tahun " + a.polarity + " + " + a.gender;
      document.getElementById("dir-headline").textContent = a.headline;
      document.getElementById("dir-roast").textContent = a.roast;
      document.getElementById("dir-tip").textContent = a.tip;
      dirCard.classList.remove("hidden");
    } else {
      dirCard.classList.add("hidden");
    }

    chartBox.classList.remove("hidden");
    chartBox.classList.remove("roast-flash");
    void chartBox.offsetWidth;
    chartBox.classList.add("roast-flash");
  }

  if (window.flatpickr && dmDate) {
    flatpickr(dmDate, {
      dateFormat: "Y-m-d",
      altInput: true,
      altFormat: "j F Y",
      locale: "id",
      maxDate: "today",
      minDate: "1900-01-01",
      onChange: (dates, str) => {
        dmValue = str || null;
        updateSubmitState();
      },
    });
  } else if (dmDate) {
    dmDate.removeAttribute("readonly");
    dmDate.addEventListener("change", () => {
      dmValue = dmDate.value || null;
      updateSubmitState();
    });
  }

  function resetDayMasterRoast() {
    chartBox.classList.add("hidden");
    dirCard.classList.add("hidden");
  }

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
  const submitBtn = document.getElementById("roast-submit");

  function updateSubmitState() {
    submitBtn.disabled = !dmValue;
  }

  if (submitBtn) {
    submitBtn.addEventListener("click", () => {
      if (dmValue) fetchRoasting();
    });
  }
  document.getElementById("back-to-start").addEventListener("click", () => {
    roastCard.classList.add("hidden");
    resetPairRoast();
    resetDayMasterRoast();
    switchView("shioList");
    setTimeout(() => {
      const container = document.querySelector(".shio-content-wrapper");
      if (container)
        container.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 100);
  });
  function fetchRoasting() {
    roastCard.classList.add("hidden");
    rerollBtn.classList.add("hidden");
    switchView("result");
    fetch("/api/shio/roasting", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tanggal: dmValue, gender: genderValue }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
          switchView("shioList");
          return;
        }
        current = data;
        current.shioKey = data.chart_roast.shio_key;
        lastVariant = -1;
        renderRoast(current.shioKey);
        renderChartRoast(data.chart_roast);
        roastCard.classList.remove("hidden");
        resetPairRoast();
        resetDayMasterRoast();
        setTimeout(() => roastCard.scrollIntoView({ behavior: "smooth", block: "start" }), 100);
      })
      .catch((err) => {
        console.error("Gagal mendapatkan data roasting:", err);
        alert("Terjadi gangguan energi kosmik. Silakan coba lagi.");
        switchView("shioList");
      });
  }
  buildPairPicker();
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
    const EMBER_RAMP = [
      [1.0, "255, 248, 214"],
      [0.82, "255, 226, 130"],
      [0.6, "255, 164, 46"],
      [0.34, "232, 88, 18"],
      [0.0, "148, 28, 8"],
    ];
    class Ember {
      constructor(x, y) {
        this.x = x;
        this.y = y;
        this.size = Math.random() * 3.5 + 2;
        this.speedX = Math.random() * 1.6 - 0.8;
        this.speedY = -(Math.random() * 2.4 + 1.1);
        this.life = 1.0;
        this.decay = Math.random() * 0.014 + 0.011;
        this.wobble = Math.random() * Math.PI * 2;
        this.wobbleRate = Math.random() * 0.12 + 0.08;
        this.flicker = Math.random() * 0.35 + 0.65;
      }
      update() {
        this.wobble += this.wobbleRate;
        this.x += this.speedX + Math.sin(this.wobble) * 0.55;
        this.y += this.speedY;
        this.speedY += 0.016;
        this.speedX *= 0.985;
        this.life -= this.decay;
        this.flicker = 0.65 + Math.abs(Math.sin(this.wobble * 1.7)) * 0.35;
      }
      warna() {
        for (let i = 0; i < EMBER_RAMP.length; i++) {
          if (this.life >= EMBER_RAMP[i][0]) return EMBER_RAMP[i][1];
        }
        return EMBER_RAMP[EMBER_RAMP.length - 1][1];
      }
      draw() {
        const hidup = Math.max(this.life, 0);
        const rgb = this.warna();
        const inti = this.size * (0.35 + hidup * 0.65) * this.flicker;
        ctx.fillStyle = `rgba(${rgb}, ${hidup * 0.22})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, inti * 3.2, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = `rgba(${rgb}, ${hidup * 0.45})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, inti * 1.8, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = `rgba(${rgb}, ${hidup})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, inti, 0, Math.PI * 2);
        ctx.fill();
      }
    }
    function createEmbers(x, y, count) {
      for (let i = 0; i < count; i++) {
        particles.push(new Ember(x, y));
      }
    }
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.globalCompositeOperation = "lighter";
      for (let i = 0; i < particles.length; i++) {
        particles[i].update();
        particles[i].draw();
        if (particles[i].life <= 0) {
          particles.splice(i, 1);
          i--;
        }
      }
      ctx.globalCompositeOperation = "source-over";
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
    if (submitBtn) {
      submitBtn.addEventListener("click", (e) => {
        const rect = e.currentTarget.getBoundingClientRect();
        createEmbers(rect.left + rect.width / 2, rect.top + rect.height / 2, 34);
      });
    }
  }
});
