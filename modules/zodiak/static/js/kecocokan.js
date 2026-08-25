document.addEventListener("DOMContentLoaded", () => {
  const btnCalc = document.getElementById("btn-calculate-compatibility-large");
  const quickViz = document.getElementById("quick-viz");
  const resultCircle = document.getElementById("result-svg-circle-large");
  const resultStatus = document.getElementById("result-status-large");
  const instructionPanel = document.getElementById("comp-details-instruction");
  const contentPanel = document.getElementById("comp-details-content");
  const badgeOne = document.getElementById("comp-badge-one");
  const badgeTwo = document.getElementById("comp-badge-two");
  const narrativeText = document.getElementById("comp-narrative");
  const loveBar = document.getElementById("param-love-bar");
  const commBar = document.getElementById("param-comm-bar");
  const trustBar = document.getElementById("param-trust-bar");
  const futureBar = document.getElementById("param-future-bar");
  const lovePercent = document.getElementById("param-love-percent");
  const commPercent = document.getElementById("param-comm-percent");
  const trustPercent = document.getElementById("param-trust-percent");
  const futurePercent = document.getElementById("param-future-percent");
  const strengthsList = document.getElementById("comp-strengths-list");
  const challengesList = document.getElementById("comp-challenges-list");
  const modePills = document.querySelectorAll(".relation-pill");
  let currentMode = "romance";
  let lastFetchedData = null;
  const elemClassMap = {
    api: "fire",
    tanah: "earth",
    udara: "air",
    air: "water",
  };
  modePills.forEach((pill) => {
    pill.addEventListener("click", () => {
      modePills.forEach((p) => p.classList.remove("active"));
      pill.classList.add("active");
      currentMode = pill.getAttribute("data-mode") || "romance";
      if (lastFetchedData) {
        renderSelectedMode(lastFetchedData, currentMode);
      }
    });
  });
  if (btnCalc) {
    btnCalc.addEventListener("click", async () => {
      const signOne = document.getElementById("sign-one-select-large").value;
      const signTwo = document.getElementById("sign-two-select-large").value;
      if (!signOne || !signTwo) {
        alert("Harap pilih kedua zodiak terlebih dahulu.");
        return;
      }
      const loaderPanel = document.getElementById("comp-details-loader");
      const origBtnText = btnCalc.innerHTML;
      if (instructionPanel) instructionPanel.classList.add("hidden");
      if (contentPanel) contentPanel.classList.add("hidden");
      if (quickViz) quickViz.classList.add("hidden");
      if (loaderPanel) loaderPanel.classList.remove("hidden");
      btnCalc.disabled = true;
      btnCalc.innerHTML = '<i class="fa-solid fa-atom fa-spin"></i> Menghitung';
      if (window.innerWidth <= 968) {
        const detailsContainer = document.querySelector(
          ".details-panel-container",
        );
        if (detailsContainer) {
          detailsContainer.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      }
      try {
        const response = await fetch(
          `/api/zodiak/compatibility/${signOne}/${signTwo}`,
        );
        if (!response.ok) throw new Error("Gagal memproses kecocokan zodiak");
        const data = await response.json();
        lastFetchedData = data;
        setTimeout(() => {
          if (loaderPanel) loaderPanel.classList.add("hidden");
          displayCompatibilityDetails(data);
          if (
            data.modes &&
            data.modes.ai_notice &&
            typeof window.showAiQuotaToast === "function"
          ) {
            window.showAiQuotaToast(data.modes.ai_notice);
          }
          btnCalc.disabled = false;
          btnCalc.innerHTML = origBtnText;
        }, 300);
      } catch (err) {
        console.error(err);
        if (loaderPanel) loaderPanel.classList.add("hidden");
        if (instructionPanel) instructionPanel.classList.remove("hidden");
        btnCalc.disabled = false;
        btnCalc.innerHTML = origBtnText;
        alert("Gagal memuat analisis kecocokan. Silakan coba lagi.");
      }
    });
  }
  function displayCompatibilityDetails(data) {
    if (quickViz) quickViz.classList.remove("hidden");
    if (instructionPanel) instructionPanel.classList.add("hidden");
    if (contentPanel) contentPanel.classList.remove("hidden");
    const clsOne = elemClassMap[data.element_one.toLowerCase()] || "fire";
    const clsTwo = elemClassMap[data.element_two.toLowerCase()] || "water";
    if (badgeOne) {
      badgeOne.className = `element-badge ${clsOne}`;
      badgeOne.innerText = data.element_one;
    }
    if (badgeTwo) {
      badgeTwo.className = `element-badge ${clsTwo}`;
      badgeTwo.innerText = data.element_two;
    }
    renderSelectedMode(data, currentMode);
  }
  function renderSelectedMode(data, mode) {
    const modeInfo =
      data.modes && data.modes[mode]
        ? data.modes[mode]
        : {
            score: data.score || 75,
            status: data.status || "Harmonis",
            summary: data.narrative || "",
            strengths: data.strengths || [],
            challenges: data.challenges || [],
            metrics: {
              love: data.love || 80,
              comm: data.communication || 80,
              trust: data.trust || 80,
              future: data.future || 80,
            },
          };
    const score = modeInfo.score;
    if (resultCircle) {
      const circumference = 251.2;
      resultCircle.style.strokeDasharray = circumference;
      resultCircle.style.strokeDashoffset = circumference;
      setTimeout(() => {
        const offsetValue = circumference - (circumference * score) / 100;
        resultCircle.style.strokeDashoffset = offsetValue;
        if (score >= 85) {
          resultCircle.style.stroke = "#10b981";
        } else if (score >= 70) {
          resultCircle.style.stroke = "#3b82f6";
        } else if (score >= 55) {
          resultCircle.style.stroke = "#f59e0b";
        } else {
          resultCircle.style.stroke = "#ef4444";
        }
      }, 50);
    }
    animateCount("result-percentage-large", score);
    if (resultStatus) resultStatus.innerText = modeInfo.status;
    if (narrativeText) narrativeText.innerText = modeInfo.summary;
    const metrics = modeInfo.metrics || {
      love: 80,
      comm: 80,
      trust: 80,
      future: 80,
    };
    if (lovePercent) lovePercent.innerText = `${metrics.love}%`;
    if (commPercent) commPercent.innerText = `${metrics.comm}%`;
    if (trustPercent) trustPercent.innerText = `${metrics.trust}%`;
    if (futurePercent) futurePercent.innerText = `${metrics.future}%`;
    setTimeout(() => {
      if (loveBar) loveBar.style.width = `${metrics.love}%`;
      if (commBar) commBar.style.width = `${metrics.comm}%`;
      if (trustBar) trustBar.style.width = `${metrics.trust}%`;
      if (futureBar) futureBar.style.width = `${metrics.future}%`;
    }, 150);
    if (strengthsList) {
      strengthsList.innerHTML = "";
      (modeInfo.strengths || []).forEach((str) => {
        const li = document.createElement("li");
        li.innerText = str;
        strengthsList.appendChild(li);
      });
    }
    if (challengesList) {
      challengesList.innerHTML = "";
      (modeInfo.challenges || []).forEach((ch) => {
        const li = document.createElement("li");
        li.innerText = ch;
        challengesList.appendChild(li);
      });
    }
  }
  function animateCount(elementId, targetValue) {
    const element = document.getElementById(elementId);
    if (!element) return;
    let current = 0;
    const duration = 1000;
    const stepTime = Math.abs(Math.floor(duration / Math.max(1, targetValue)));
    const timer = setInterval(() => {
      current += 1;
      element.innerText = `${current}%`;
      if (current >= targetValue) {
        clearInterval(timer);
        element.innerText = `${targetValue}%`;
      }
    }, stepTime);
  }
  const tabBtnStandard = document.getElementById("tab-btn-standard");
  const tabBtnQuiz = document.getElementById("tab-btn-quiz");
  const standardSection = document.getElementById(
    "standard-compatibility-section",
  );
  const quizSection = document.getElementById("quiz-room-section");
  if (tabBtnStandard && tabBtnQuiz) {
    tabBtnStandard.addEventListener("click", () => {
      tabBtnStandard.classList.add("active");
      tabBtnQuiz.classList.remove("active");
      if (standardSection) standardSection.classList.remove("hidden");
      if (quizSection) quizSection.classList.add("hidden");
    });
    tabBtnQuiz.addEventListener("click", () => {
      tabBtnQuiz.classList.add("active");
      tabBtnStandard.classList.remove("active");
      if (quizSection) quizSection.classList.remove("hidden");
      if (standardSection) standardSection.classList.add("hidden");
    });
  }
  let quizQuestions = [];
  let currentQuizIndex = 0;
  let quizUserAnswers = [];
  let isJoinMode = false;
  let currentRole = "host";
  let currentRoomCode = "";
  let currentShareUrl = "";
  let pollingInterval = null;
  const btnModeCreate = document.getElementById("btn-mode-create");
  const btnModeJoin = document.getElementById("btn-mode-join");
  const fieldRoomCode = document.getElementById("field-room-code");
  const inputRoomCode = document.getElementById("quiz-input-room-code");
  const inputName = document.getElementById("quiz-input-name");
  const selectSign = document.getElementById("quiz-select-sign");
  const btnStartQuiz = document.getElementById("btn-start-quiz");
  const stepInit = document.getElementById("quiz-step-init");
  const stepQuestions = document.getElementById("quiz-step-questions");
  const stepLoader = document.getElementById("quiz-step-loader");
  const stepWaiting = document.getElementById("quiz-step-waiting");
  const stepResult = document.getElementById("quiz-step-result");
  function showQuizStep(targetStep) {
    [stepInit, stepQuestions, stepLoader, stepWaiting, stepResult].forEach(
      (s) => {
        if (s) s.classList.add("hidden");
      },
    );
    if (targetStep) targetStep.classList.remove("hidden");
  }
  if (btnModeCreate && btnModeJoin) {
    btnModeCreate.addEventListener("click", () => {
      isJoinMode = false;
      btnModeCreate.classList.add("active");
      btnModeJoin.classList.remove("active");
      if (fieldRoomCode) fieldRoomCode.classList.add("hidden");
    });
    btnModeJoin.addEventListener("click", () => {
      isJoinMode = true;
      btnModeJoin.classList.add("active");
      btnModeCreate.classList.remove("active");
      if (fieldRoomCode) fieldRoomCode.classList.remove("hidden");
    });
  }
  async function loadQuizQuestions() {
    try {
      const res = await fetch("/api/zodiak/quiz/questions");
      if (res.ok) {
        const data = await res.json();
        quizQuestions = data.questions || [];
      }
    } catch (e) {
      console.error("Gagal mengambil pertanyaan quiz:", e);
    }
  }
  loadQuizQuestions();
  if (btnStartQuiz) {
    btnStartQuiz.addEventListener("click", async () => {
      const name = inputName ? inputName.value.trim() : "";
      const sign = selectSign ? selectSign.value : "";
      if (!name || !sign) {
        alert("Harap isi Nama dan Zodiak Anda terlebih dahulu.");
        return;
      }
      const origText = btnStartQuiz.innerHTML;
      btnStartQuiz.disabled = true;
      btnStartQuiz.innerHTML =
        '<i class="fa-solid fa-atom fa-spin"></i> Memproses...';
      if (!isJoinMode) {
        try {
          const res = await fetch("/api/zodiak/quiz/create_room", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ host_name: name, host_sign: sign }),
          });
          if (!res.ok) throw new Error("Gagal membuat room.");
          const data = await res.json();
          currentRoomCode = data.room_code;
          currentShareUrl = data.share_url;
          currentRole = "host";
          setupShareButtons(currentShareUrl, name, sign);
          const displayCode = document.getElementById("display-room-code");
          if (displayCode) displayCode.innerText = currentRoomCode;
        } catch (err) {
          alert("Gagal membuat room. Silakan coba lagi.");
          btnStartQuiz.disabled = false;
          btnStartQuiz.innerHTML = origText;
          return;
        }
      } else {
        const code = inputRoomCode
          ? inputRoomCode.value.trim().toUpperCase()
          : "";
        if (!code || code.length < 5) {
          alert(
            "Harap masukkan Kode Room pasangan yang valid (Contoh: RO-8X92K).",
          );
          btnStartQuiz.disabled = false;
          btnStartQuiz.innerHTML = origText;
          return;
        }
        currentRoomCode = code;
        currentRole = "partner";
        try {
          const res = await fetch("/api/zodiak/quiz/join_room", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              room_code: currentRoomCode,
              partner_name: name,
              partner_sign: sign,
            }),
          });
          if (!res.ok) throw new Error("Kode Room tidak valid.");
          const resData = await res.json();
          if (resData.status === "completed") {
            showQuizStep(stepLoader);
            const loaderDesc = document.getElementById("quiz-loader-desc");
            if (loaderDesc) {
              loaderDesc.innerHTML =
                "✨ Kode Room ini telah selesai! Memuat hasil analisis kecocokan kalian...";
            }
            setTimeout(() => {
              renderQuizResult(resData);
              btnStartQuiz.disabled = false;
              btnStartQuiz.innerHTML = origText;
            }, 600);
            return;
          }
        } catch (err) {
          alert(
            "Kode Room tidak ditemukan. Pastikan kode room pasangan benar.",
          );
          btnStartQuiz.disabled = false;
          btnStartQuiz.innerHTML = origText;
          return;
        }
      }
      btnStartQuiz.disabled = false;
      btnStartQuiz.innerHTML = origText;
      currentQuizIndex = 0;
      quizUserAnswers = new Array(quizQuestions.length).fill(null);
      showQuizStep(stepQuestions);
      renderQuestion(currentQuizIndex);
    });
  }
  function renderQuestion(index) {
    if (!quizQuestions || quizQuestions.length === 0) return;
    const q = quizQuestions[index];
    const catBadge = document.getElementById("quiz-cat-badge");
    const qNum = document.getElementById("quiz-q-num");
    const qFill = document.getElementById("quiz-progress-fill");
    const qText = document.getElementById("quiz-q-text");
    const optionsContainer = document.getElementById("quiz-options-container");
    const btnPrev = document.getElementById("btn-quiz-prev");
    const btnNext = document.getElementById("btn-quiz-next");
    if (catBadge) catBadge.innerText = q.category;
    if (qNum) qNum.innerText = index + 1;
    if (qFill)
      qFill.style.width = `${((index + 1) / quizQuestions.length) * 100}%`;
    if (qText) qText.innerText = q.question;
    if (optionsContainer) {
      optionsContainer.innerHTML = "";
      q.options.forEach((optText, optIdx) => {
        const btnOpt = document.createElement("button");
        btnOpt.type = "button";
        btnOpt.className = "quiz-option-btn";
        if (quizUserAnswers[index] === optIdx) {
          btnOpt.classList.add("selected");
        }
        btnOpt.innerHTML = `
                    <span class="quiz-option-letter">${String.fromCharCode(65 + optIdx)}</span>
                    <span class="quiz-option-text">${optText}</span>
                `;
        btnOpt.addEventListener("click", () => {
          document
            .querySelectorAll(".quiz-option-btn")
            .forEach((b) => b.classList.remove("selected"));
          btnOpt.classList.add("selected");
          quizUserAnswers[index] = optIdx;
          if (btnNext) btnNext.disabled = false;
        });
        optionsContainer.appendChild(btnOpt);
      });
    }
    if (btnPrev) {
      if (index > 0) btnPrev.classList.remove("hidden");
      else btnPrev.classList.add("hidden");
    }
    if (btnNext) {
      btnNext.disabled = quizUserAnswers[index] === null;
      if (index === quizQuestions.length - 1) {
        btnNext.innerHTML = 'Simpan <i class="fa-solid fa-check-circle"></i>';
      } else {
        btnNext.innerHTML = 'Lanjut <i class="fa-solid fa-arrow-right"></i>';
      }
    }
  }
  const btnNext = document.getElementById("btn-quiz-next");
  const btnPrev = document.getElementById("btn-quiz-prev");
  if (btnNext) {
    btnNext.addEventListener("click", async () => {
      if (currentQuizIndex < quizQuestions.length - 1) {
        currentQuizIndex++;
        renderQuestion(currentQuizIndex);
      } else {
        await submitQuizForm();
      }
    });
  }
  if (btnPrev) {
    btnPrev.addEventListener("click", () => {
      if (currentQuizIndex > 0) {
        currentQuizIndex--;
        renderQuestion(currentQuizIndex);
      }
    });
  }
  async function submitQuizForm() {
    showQuizStep(stepLoader);
    const loaderDesc = document.getElementById("quiz-loader-desc");
    if (loaderDesc) {
      loaderDesc.innerHTML =
        "Mohon tunggu sebentar, 10 jawabanmu sedang disimpan &amp; disinkronkan ke room pasangan... ✨";
    }
    try {
      const res = await fetch("/api/zodiak/quiz/submit_answers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          room_code: currentRoomCode,
          role: currentRole,
          answers: quizUserAnswers,
        }),
      });
      if (!res.ok) throw new Error("Gagal mengirimkan jawaban.");
      const data = await res.json();
      if (data.status === "completed") {
        if (loaderDesc) {
          loaderDesc.innerHTML =
            "✨ Kedua pasangan telah selesai! AI sedang menyusun analisis chemistry kecocokan kalian...";
        }
        setTimeout(() => {
          renderQuizResult(data);
        }, 800);
      } else {
        setTimeout(() => {
          showQuizStep(stepWaiting);
          const displayCode = document.getElementById("display-room-code");
          if (displayCode) displayCode.innerText = currentRoomCode;
          const pollingText = document.getElementById("polling-text");
          if (pollingText)
            pollingText.innerText =
              "Jawaban 10 pertanyaanmu telah tersimpan! Menunggu pasanganmu selesai...";
          startPollingForPartner();
        }, 600);
      }
    } catch (err) {
      showQuizStep(stepQuestions);
      alert("Gagal menyimpan jawaban. Silakan coba lagi.");
    }
  }
  function startPollingForPartner() {
    if (pollingInterval) clearInterval(pollingInterval);
    pollingInterval = setInterval(async () => {
      try {
        const res = await fetch(`/api/zodiak/quiz/room/${currentRoomCode}`);
        if (res.ok) {
          const data = await res.json();
          if (data.status === "completed") {
            clearInterval(pollingInterval);
            showQuizStep(stepLoader);
            const loaderDesc = document.getElementById("quiz-loader-desc");
            if (loaderDesc) {
              loaderDesc.innerHTML =
                "✨ Pasanganmu baru saja selesai menjawab! Memuat hasil kecocokan kalian...";
            }
            setTimeout(() => {
              renderQuizResult(data);
            }, 700);
          }
        }
      } catch (e) {}
    }, 2000);
  }
  function setupShareButtons(shareUrl, hostName, hostSign) {
    const btnWa = document.getElementById("btn-copy-wa-link");
    const btnCopy = document.getElementById("btn-copy-link-only");
    const waText = encodeURIComponent(
      `✨ *Tantangan Quiz Kecocokan Partner Zodiak* ✨\n\nHalo! ${hostName} (${hostSign.toUpperCase()}) mengundangmu main 10 Pertanyaan Partner nih!\n\nYuk ikutan jawab 10 pertanyaan kecocokan hubungan kalian & liat hasil analisisnya di sini:\n${shareUrl}`,
    );
    if (btnWa) {
      btnWa.onclick = () => {
        window.open(`https://api.whatsapp.com/send?text=${waText}`, "_blank");
      };
    }
    if (btnCopy) {
      btnCopy.onclick = () => {
        navigator.clipboard.writeText(shareUrl);
        alert("Link Room berhasil disalin! Silakan bagikan ke pasangan Anda.");
      };
    }
  }
  function renderQuizResult(data) {
    showQuizStep(stepResult);
    const coupleNames = document.getElementById("res-couple-names");
    const headline = document.getElementById("res-ai-headline");
    const verdict = document.getElementById("res-ai-verdict");
    const strengths = document.getElementById("res-ai-strengths");
    const challenge = document.getElementById("res-ai-challenge");
    const tip = document.getElementById("res-ai-tip");
    const quizScoreCircle = document.getElementById("circle-quiz-score");
    const zodiacScoreCircle = document.getElementById("circle-zodiac-score");
    const breakdownList = document.getElementById("res-breakdown-list");
    const hSignName = (data.host_sign || "Aries").toUpperCase();
    const pSignName = (data.partner_sign || "Taurus").toUpperCase();
    if (coupleNames)
      coupleNames.innerText = `${data.host_name} (${hSignName}) & ${data.partner_name} (${pSignName})`;
    const ai = data.ai_result || {};
    if (headline)
      headline.innerText =
        ai.vibe_headline || "Dinamika Pasangan Kosmik Yang Seru!";
    if (verdict)
      verdict.innerText =
        ai.verdict || "Kalian punya keselarasan karakter yang unik.";
    if (strengths)
      strengths.innerText =
        ai.strengths || "Kalian saling melengkapi satu sama lain.";
    if (challenge)
      challenge.innerText =
        ai.challenge || "Perbedaan sudut pandang bisa jadi bumbu hubungan.";
    if (tip)
      tip.innerText =
        ai.couple_tip || "Terus pertahankan komunikasi yang hangat!";
    const maxDash = 251.2;
    const qScore = data.match_score || 75;
    const zScore = data.zodiac_score || 80;
    if (quizScoreCircle)
      quizScoreCircle.style.strokeDashoffset =
        maxDash - (maxDash * qScore) / 100;
    if (zodiacScoreCircle)
      zodiacScoreCircle.style.strokeDashoffset =
        maxDash - (maxDash * zScore) / 100;
    animateCount("res-quiz-percent", qScore);
    animateCount("res-zodiac-percent", zScore);
    if (breakdownList && data.breakdown) {
      breakdownList.innerHTML = "";
      data.breakdown.forEach((item, idx) => {
        const row = document.createElement("div");
        row.className = `breakdown-item ${item.is_match ? "match" : "unique"}`;
        row.innerHTML = `
                    <div class="breakdown-item-header">
                        <span class="breakdown-q-num">Pertanyaan #${idx + 1} (${item.category})</span>
                        <span class="breakdown-status-badge ${item.is_match ? "match" : "unique"}">
                            ${item.is_match ? "✨ Match!" : "💡 Unik"}
                        </span>
                    </div>
                    <p class="breakdown-q-title">${item.question}</p>
                    <div class="breakdown-answers-grid">
                        <div class="ans-box host">
                            <span class="ans-user">${data.host_name}:</span>
                            <span class="ans-text">${item.host_answer}</span>
                        </div>
                        <div class="ans-box partner">
                            <span class="ans-user">${data.partner_name}:</span>
                            <span class="ans-text">${item.partner_answer}</span>
                        </div>
                    </div>
                `;
        breakdownList.appendChild(row);
      });
    }
    const btnShareWa = document.getElementById("btn-share-result-wa");
    const btnReset = document.getElementById("btn-reset-quiz");
    if (btnShareWa) {
      const currentUrl = `${window.location.origin}/zodiak/kecocokan?room=${data.room_code}`;
      const resWaText = encodeURIComponent(
        `💖 *Hasil Quiz Kecocokan Partner Zodiak* 💖\n\n*${data.host_name}* (${hSignName}) & *${data.partner_name}* (${pSignName})\n\n🎯 Skor Kembaran Quiz: *${qScore}%*\n✨ Skor Zodiak: *${zScore}%*\n\n"${ai.vibe_headline || "Chemistry Kosmik Yang Manis!"}"\n\nLihat detail analisis kecocokan lengkap kami di sini:\n${currentUrl}`,
      );
      btnShareWa.onclick = () => {
        window.open(
          `https://api.whatsapp.com/send?text=${resWaText}`,
          "_blank",
        );
      };
    }
    if (btnReset) {
      btnReset.onclick = () => {
        if (pollingInterval) clearInterval(pollingInterval);
        window.location.href = "/zodiak/kecocokan";
      };
    }
  }
  const urlParams = new URLSearchParams(window.location.search);
  const roomParam = urlParams.get("room");
  if (roomParam) {
    if (tabBtnQuiz) tabBtnQuiz.click();
    if (btnModeJoin) btnModeJoin.click();
    if (inputRoomCode) inputRoomCode.value = roomParam.trim().toUpperCase();
    showQuizStep(stepLoader);
    const loaderDesc = document.getElementById("quiz-loader-desc");
    if (loaderDesc) {
      loaderDesc.innerHTML =
        "✨ Memeriksa status room &amp; memuat hasil kecocokan partner...";
    }
    fetch(`/api/zodiak/quiz/room/${roomParam.trim().toUpperCase()}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "completed") {
          setTimeout(() => {
            renderQuizResult(data);
          }, 500);
        } else {
          showQuizStep(stepInit);
        }
      })
      .catch(() => {
        showQuizStep(stepInit);
      });
  }
});
