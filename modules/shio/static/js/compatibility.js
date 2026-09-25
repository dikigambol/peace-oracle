document.addEventListener("DOMContentLoaded", () => {
  const btnCheck = document.getElementById("btn-check");
  const resultEl = document.getElementById("compat-result");
  const lensChips = document.querySelectorAll("#lens-chips .choice-chip");
  let birth1 = null;
  let birth2 = null;
  let lens = "asmara";
  let scoreTimer = null;

  function setupBirthInput(id, onPick) {
    window.initDatePicker("#" + id, {
      dateFormat: "Y-m-d",
      altInput: true,
      altFormat: "j F Y",
      locale: "id",
      maxDate: "today",
      minDate: "1900-01-01",
      onChange: (dates, str) => onPick(str || null),
    });
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
  lensChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      lens = chip.dataset.lens;
      lensChips.forEach((other) => {
        const active = other === chip;
        other.classList.toggle("active", active);
        other.setAttribute("aria-checked", active ? "true" : "false");
      });
      if (birth1 && birth2 && !resultEl.classList.contains("hidden")) {
        fetchCompatibility();
      }
    });
  });
  btnCheck.addEventListener("click", () => {
    if (!birth1 || !birth2) return;
    fetchCompatibility();
  });

  function animateScore(score) {
    const scoreText = document.getElementById("c-score-text");
    const scoreCircle = document.getElementById("c-score-circle");
    scoreText.textContent = "0%";
    scoreCircle.setAttribute("stroke-dasharray", "0, 100");
    scoreCircle.className.baseVal = "circle";
    if (score >= 70) scoreCircle.classList.add("high");
    else if (score >= 45) scoreCircle.classList.add("mid");
    else scoreCircle.classList.add("low");
    if (scoreTimer) {
      clearInterval(scoreTimer);
      scoreTimer = null;
    }
    if (window.prefersReducedMotion() || score <= 0) {
      scoreText.textContent = score + "%";
    } else {
      let currentScore = 0;
      const stepTime = Math.max(10, Math.floor(1500 / score));
      scoreTimer = setInterval(() => {
        currentScore += 1;
        scoreText.textContent = currentScore + "%";
        if (currentScore >= score) {
          clearInterval(scoreTimer);
          scoreTimer = null;
          scoreText.textContent = score + "%";
        }
      }, stepTime);
    }
    setTimeout(() => {
      scoreCircle.setAttribute("stroke-dasharray", score + ", 100");
    }, 50);
  }

  function fetchCompatibility() {
    window.setButtonLoading(btnCheck, true, "Menimbang energi...");
    window
      .fetchJson("/api/shio/compatibility", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tanggal1: birth1, tanggal2: birth2, lens: lens }),
      })
      .then((data) => {
        if (data.error && !data.shio1) {
          window.showErrorToast(data.error);
          return;
        }
        resultEl.classList.remove("hidden");
        resultEl.classList.remove("animate-in");
        void resultEl.offsetWidth;
        resultEl.classList.add("animate-in");
        animateScore(data.score || 50);
        window.renderCompatLayers(data);
        setTimeout(() => {
          resultEl.scrollIntoView({ behavior: "smooth", block: "start" });
        }, 200);
      })
      .catch((err) => {
        console.error("Gagal memuat kompatibilitas:", err);
        window.showErrorToast(err && err.message);
      })
      .finally(() => {
        window.setButtonLoading(btnCheck, false, null, !(birth1 && birth2));
      });
  }
  window.initBurstParticles();
});
