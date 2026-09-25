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
    window
      .fetchJson("/api/shio/guardian", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
      .then((data) => {
        const resTitle = document.getElementById("res-title");
        if (resTitle) {
          resTitle.textContent = data.guardian_name;
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
          data.shio_element + " " + data.shio_element_hanzi;
        document.getElementById("res-tradition").textContent = data.tradition;
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
        document.getElementById("res-dir-note").textContent = data.direction_note;
        document.getElementById("res-pray-time-note").textContent =
          data.pray_time_note;
        document.getElementById("res-feng-shui-note").textContent =
          data.feng_shui_note;
        const resultCard = document.getElementById("main-fortune-card");
        resultCard.classList.remove("hidden");
        setTimeout(() => resultCard.scrollIntoView({ behavior: "smooth", block: "start" }), 100);
      })
      .catch((err) => {
        console.error("Gagal mendapatkan data penjaga:", err);
        window.showErrorToast(err && err.message);
      });
  }
  window.initBurstParticles();
});
