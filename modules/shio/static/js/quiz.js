(function () {
  const CODE_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ";
  const CODE_LENGTH = 6;
  const SEAT_PREFIX = "shio_quiz_seat_";

  function normaliseCode(value) {
    const code = String(value || "")
      .replace(/[\s-]/g, "")
      .toUpperCase()
      .replace(/O/g, "0")
      .replace(/[IL]/g, "1");
    if (code.length !== CODE_LENGTH) return null;
    for (const char of code) {
      if (CODE_ALPHABET.indexOf(char) === -1) return null;
    }
    return code;
  }

  function loadSeat(code) {
    try {
      const raw = localStorage.getItem(SEAT_PREFIX + code);
      const seat = raw ? JSON.parse(raw) : null;
      return seat && typeof seat.token === "string" ? seat : null;
    } catch (e) {
      return null;
    }
  }

  function saveSeat(code, seat) {
    try {
      localStorage.setItem(SEAT_PREFIX + code, JSON.stringify(seat));
    } catch (e) {}
  }

  function clearSeat(code) {
    try {
      localStorage.removeItem(SEAT_PREFIX + code);
    } catch (e) {}
  }

  async function api(path, options) {
    const settings = options || {};
    const headers = { "Content-Type": "application/json" };
    if (settings.token) headers["X-Quiz-Token"] = settings.token;
    const res = await fetch(path, {
      method: settings.method || "GET",
      headers: headers,
      body: settings.body ? JSON.stringify(settings.body) : undefined,
    });
    let payload = null;
    try {
      payload = await res.json();
    } catch (e) {
      payload = null;
    }
    if (!res.ok) {
      const error = new Error(
        (payload && payload.error) || "Server menolak permintaan (status " + res.status + ")."
      );
      error.status = res.status;
      throw error;
    }
    return payload;
  }

  function makeEl(tag, className, text) {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (text !== undefined && text !== null) el.textContent = text;
    return el;
  }

  function clearNode(node) {
    while (node.firstChild) node.removeChild(node.firstChild);
  }

  function readBirthInput(selector) {
    const input = document.querySelector(selector);
    return input ? input.value.trim() : "";
  }

  function byId(id) {
    return document.getElementById(id);
  }

  function setVerdict(kicker, verdict, scoreText) {
    byId("verdict-kicker").textContent = kicker;
    byId("verdict-title").textContent = verdict.title;
    byId("verdict-note").textContent = verdict.note;
    const score = byId("verdict-score");
    score.textContent = scoreText || "";
    score.classList.toggle("hidden", !scoreText);
    byId("result-verdict").className = "quiz-card quiz-verdict verdict-" + verdict.key;
  }

  function setBreakdown(lines) {
    const box = byId("verdict-breakdown");
    clearNode(box);
    lines.forEach((line) => {
      const row = makeEl("div", "quiz-breakdown-row");
      row.appendChild(makeEl("span", "quiz-breakdown-label", line[0]));
      row.appendChild(makeEl("span", "quiz-breakdown-value", line[1]));
      box.appendChild(row);
    });
    box.classList.toggle("hidden", !lines.length);
  }

  function participantName(view, slot) {
    const found = view.participants.find((person) => person.slot === slot);
    return found ? found.name : "?";
  }

  function renderPairResult(view) {
    const result = view.result;
    const name1 = participantName(view, 1);
    const name2 = participantName(view, 2);
    setVerdict(
      "Ramalan Pasangan · " + (view.relation_label || "") + " · " + name1 + " & " + name2,
      result.verdict,
      result.score + "%"
    );
    setBreakdown([
      ["Relasi shio (" + Math.round(result.weights.shio * 100) + "%)", result.shio_score + "%"],
      ["Kecocokan jawaban (" + Math.round(result.weights.answers * 100) + "%)", result.answer_score + "%"],
    ]);
    const list = byId("pair-compare");
    clearNode(list);
    result.comparisons.forEach((row) => {
      const item = makeEl("li", "quiz-compare-item distance-" + row.distance);
      item.appendChild(makeEl("p", "quiz-compare-question", row.question));
      const answers = makeEl("div", "quiz-compare-answers");
      const first = makeEl("p", "quiz-compare-answer");
      first.appendChild(makeEl("strong", null, name1 + ": "));
      first.appendChild(document.createTextNode(row.answer1));
      const second = makeEl("p", "quiz-compare-answer");
      second.appendChild(makeEl("strong", null, name2 + ": "));
      second.appendChild(document.createTextNode(row.answer2));
      answers.appendChild(first);
      answers.appendChild(second);
      item.appendChild(answers);
      item.appendChild(makeEl("span", "quiz-compare-badge", row.label));
      list.appendChild(item);
    });
    window.renderCompatLayers(result.compatibility);
    byId("result-pair").classList.remove("hidden");
  }

  function buildPairItem(pair) {
    const item = makeEl("li", "quiz-pair code-" + pair.code);
    const head = makeEl("div", "quiz-pair-head");
    head.appendChild(makeEl("span", "quiz-pair-names", pair.names.join(" × ")));
    head.appendChild(makeEl("span", "quiz-pair-hanzi", pair.hanzi));
    item.appendChild(head);
    item.appendChild(makeEl("span", "quiz-pair-label", pair.label + " · " + pair.title));
    item.appendChild(makeEl("p", "quiz-pair-note", pair.note));
    return item;
  }

  function fillPairs(listId, pairs, emptyText) {
    const list = byId(listId);
    clearNode(list);
    if (!pairs.length) {
      list.appendChild(makeEl("li", "quiz-empty", emptyText));
      return;
    }
    pairs.forEach((pair) => list.appendChild(buildPairItem(pair)));
  }

  function renderGroupResult(view) {
    const result = view.result;
    const counts = result.counts;
    setVerdict("Ramalan Kelompok · " + result.members.length + " orang", result.verdict, "");
    setBreakdown([
      ["Ikatan harmonis", counts.good + " pasangan"],
      ["Rawan gesekan", counts.bad + " pasangan"],
      ["Netral", counts.neutral + " pasangan"],
    ]);
    const roles = byId("group-roles");
    clearNode(roles);
    result.members.forEach((member) => {
      const item = makeEl("li", "quiz-role role-" + member.role_key);
      const head = makeEl("div", "quiz-role-head");
      head.appendChild(makeEl("span", "quiz-person-hanzi", member.hanzi));
      const body = makeEl("div", "quiz-person-body");
      body.appendChild(makeEl("span", "quiz-person-name", member.name));
      body.appendChild(makeEl("span", "quiz-person-tags", member.shio));
      head.appendChild(body);
      head.appendChild(makeEl("span", "quiz-role-title", member.role_title));
      item.appendChild(head);
      item.appendChild(makeEl("p", "quiz-role-note", member.role_note));
      item.appendChild(
        makeEl(
          "p",
          "quiz-role-tally",
          member.good + " harmonis · " + member.bad + " gesekan · " + member.neutral + " netral"
        )
      );
      roles.appendChild(item);
    });
    const triads = byId("group-triads");
    clearNode(triads);
    result.triads.forEach((triad) => {
      const item = makeEl("li", "quiz-pair code-good");
      item.appendChild(makeEl("span", "quiz-pair-names", triad.names.join(", ")));
      item.appendChild(
        makeEl(
          "p",
          "quiz-pair-note",
          "Satu segitiga tiga harmoni berelemen " + triad.element + " (" + triad.element_hanzi +
            "). Kalau mereka bertiga satu tim, arahnya gampang kompak."
        )
      );
      triads.appendChild(item);
    });
    byId("group-triads-card").classList.toggle("hidden", !result.triads.length);
    fillPairs("group-best", result.best_pairs, "Tidak ada pasangan 六合 atau 三合 di kelompok ini.");
    fillPairs("group-tense", result.tense_pairs, "Tidak ada benturan cabang di kelompok ini.");
    byId("group-all-summary").textContent = "Lihat semua " + result.pairs.length + " pasangan";
    fillPairs("group-all", result.pairs, "");
    byId("group-note").textContent = result.note;
    byId("result-group").classList.remove("hidden");
  }

  function renderGuessResult(view) {
    const result = view.result;
    const mine = view.me ? result.targets.find((target) => target.slot === view.me.slot) : null;
    const leader = result.leaderboard[0];
    if (mine) {
      setVerdict("Tebak Shio Teman · tentang kamu", mine.verdict, mine.readability + "%");
    } else {
      setVerdict("Tebak Shio Teman", { key: "terbaca", title: "Juara: " + leader.name, note: "" }, "");
    }
    setBreakdown([["Skor maksimal per pemain", result.max_points + " poin"]]);
    const board = byId("guess-leaderboard");
    clearNode(board);
    result.leaderboard.forEach((row) => {
      const item = makeEl("li", "quiz-leader");
      item.appendChild(makeEl("span", "quiz-leader-name", row.name));
      item.appendChild(makeEl("span", "quiz-leader-points", row.points + " poin · " + row.solved + " benar"));
      board.appendChild(item);
    });
    const targets = byId("guess-targets");
    clearNode(targets);
    result.targets
      .slice()
      .sort((a, b) => b.readability - a.readability)
      .forEach((target) => {
        const item = makeEl("li", "quiz-target verdict-" + target.verdict.key);
        const head = makeEl("div", "quiz-role-head");
        head.appendChild(makeEl("span", "quiz-person-hanzi", target.hanzi));
        const body = makeEl("div", "quiz-person-body");
        body.appendChild(makeEl("span", "quiz-person-name", target.name));
        body.appendChild(makeEl("span", "quiz-person-tags", "Shio " + target.shio));
        head.appendChild(body);
        head.appendChild(makeEl("span", "quiz-role-title", target.readability + "%"));
        item.appendChild(head);
        item.appendChild(makeEl("p", "quiz-role-note", target.verdict.title + " — " + target.verdict.note));
        const details = makeEl("details", "quiz-target-hints");
        details.appendChild(makeEl("summary", null, "Petunjuk yang dipakai"));
        const hints = makeEl("ol", "quiz-hints");
        target.hints.forEach((hint) => hints.appendChild(makeEl("li", "quiz-hint-item", hint)));
        details.appendChild(hints);
        item.appendChild(details);
        targets.appendChild(item);
      });
    byId("result-guess").classList.remove("hidden");
  }

  function renderQuizResult(view) {
    if (view.mode === "pasangan") renderPairResult(view);
    else if (view.mode === "kelompok") renderGroupResult(view);
    else renderGuessResult(view);
  }

  function initHub() {
    const joinForm = byId("quiz-join-form");
    const joinInput = byId("join-code");
    const createForm = byId("quiz-create-form");
    const createTitle = byId("create-title");
    const createSubmit = byId("create-submit");
    const relationGroup = byId("relation-group");
    const flavorGroup = byId("flavor-group");
    const flavorNote = byId("flavor-note");
    const modeButtons = document.querySelectorAll(".quiz-mode");
    const relationChips = document.querySelectorAll("[data-relation]");
    const flavorChips = document.querySelectorAll("[data-flavor]");

    let mode = null;
    let relationType = null;
    let flavor = "manis";

    window.initDatePicker("#create-birth", {
      dateFormat: "Y-m-d",
      altInput: true,
      altFormat: "j F Y",
      locale: "id",
      maxDate: "today",
      minDate: "1900-01-01",
    });

    function selectInGroup(buttons, chosen) {
      buttons.forEach((button) => {
        const active = button === chosen;
        button.classList.toggle("active", active);
        button.setAttribute("aria-checked", active ? "true" : "false");
      });
    }

    modeButtons.forEach((button) => {
      button.addEventListener("click", () => {
        mode = button.dataset.mode;
        selectInGroup(modeButtons, button);
        createTitle.textContent = button.querySelector(".quiz-mode-title").textContent;
        relationGroup.classList.toggle("hidden", mode !== "pasangan");
        flavorGroup.classList.toggle("hidden", mode !== "tebak");
        createForm.classList.remove("hidden");
        createForm.scrollIntoView({ behavior: window.prefersReducedMotion() ? "auto" : "smooth", block: "start" });
      });
    });

    relationChips.forEach((chip) => {
      chip.addEventListener("click", () => {
        relationType = chip.dataset.relation;
        selectInGroup(relationChips, chip);
      });
    });

    flavorChips.forEach((chip) => {
      chip.addEventListener("click", () => {
        flavor = chip.dataset.flavor;
        selectInGroup(flavorChips, chip);
        flavorNote.textContent = chip.dataset.note;
      });
    });

    joinForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const code = normaliseCode(joinInput.value);
      if (!code) {
        window.showErrorToast("Kode room terdiri dari 6 huruf atau angka.");
        joinInput.focus();
        return;
      }
      window.location.href = "/shio/quiz/" + code;
    });

    createForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const name = byId("create-name").value.trim();
      const birthDate = readBirthInput("#create-birth");
      if (!name) {
        window.showErrorToast("Isi nama panggilanmu dulu.");
        return;
      }
      if (!birthDate) {
        window.showErrorToast("Pilih tanggal lahirmu dulu.");
        return;
      }
      if (mode === "pasangan" && !relationType) {
        window.showErrorToast("Pilih jenis hubungan kalian dulu.");
        return;
      }
      const body = { mode: mode, name: name, birth_date: birthDate };
      if (mode === "pasangan") body.relation_type = relationType;
      if (mode === "tebak") body.flavor = flavor;
      window.setButtonLoading(createSubmit, true, "Menyiapkan room...");
      api("/api/shio/quiz/rooms", { method: "POST", body: body })
        .then((data) => {
          saveSeat(data.room_code, { token: data.token, slot: data.slot });
          window.location.href = "/shio/quiz/" + data.room_code;
        })
        .catch((error) => {
          window.showErrorToast(error.message);
          window.setButtonLoading(createSubmit, false);
        });
    });
  }

  function initRoom() {
    const code = byId("quiz-room").dataset.roomCode;
    const POLL_STEPS = [2000, 2000, 3000, 5000, 5000, 10000];
    const POLL_IDLE_LIMIT = 15 * 60 * 1000;
    const FINISH_CONFIRM_MS = 4000;

    let seat = loadSeat(code);
    let state = null;
    let lastSignature = "";
    let pollTimer = null;
    let pollStep = 0;
    let lastChangeAt = Date.now();
    let inFlight = false;
    let questionsRendered = false;
    let resultRendered = false;
    let finishArmedUntil = 0;

    const els = {
      mode: byId("room-mode"),
      meta: byId("room-meta"),
      notice: byId("room-notice"),
      noticeText: byId("room-notice-text"),
      refresh: byId("btn-refresh"),
      join: byId("room-join"),
      joinInfo: byId("join-info"),
      joinSubmit: byId("join-submit"),
      lobby: byId("room-lobby"),
      lobbyCount: byId("lobby-count"),
      lobbyPeople: byId("lobby-people"),
      lobbyStatus: byId("lobby-status"),
      start: byId("btn-start"),
      finish: byId("btn-finish"),
      questions: byId("room-questions"),
      questionList: byId("question-list"),
      answersSubmit: byId("answers-submit"),
      turn: byId("room-turn"),
      result: byId("room-result"),
    };

    window.initDatePicker("#join-birth", {
      dateFormat: "Y-m-d",
      altInput: true,
      altFormat: "j F Y",
      locale: "id",
      maxDate: "today",
      minDate: "1900-01-01",
    });

    function toggle(el, visible) {
      el.classList.toggle("hidden", !visible);
    }

    function roomUrl() {
      return window.location.origin + "/shio/quiz/" + code;
    }

    function showNotice(message, withRefresh) {
      els.noticeText.textContent = message;
      toggle(els.refresh, Boolean(withRefresh));
      toggle(els.notice, true);
    }

    function hideNotice() {
      toggle(els.notice, false);
    }

    function schedulePoll() {
      clearTimeout(pollTimer);
      pollTimer = null;
      if (!state || state.status === "done" || document.hidden) return;
      if (Date.now() - lastChangeAt > POLL_IDLE_LIMIT) {
        showNotice("Room ini sudah lama tidak berubah, jadi pembaruan otomatis dijeda.", true);
        return;
      }
      const delay = POLL_STEPS[Math.min(pollStep, POLL_STEPS.length - 1)];
      pollTimer = setTimeout(refresh, delay);
    }

    async function refresh() {
      if (inFlight) return;
      inFlight = true;
      clearTimeout(pollTimer);
      try {
        const view = await api("/api/shio/quiz/rooms/" + code, { token: seat && seat.token });
        const signature = JSON.stringify(view);
        if (signature !== lastSignature) {
          lastSignature = signature;
          lastChangeAt = Date.now();
          pollStep = 0;
          render(view);
        } else {
          pollStep += 1;
        }
        if (!els.refresh.classList.contains("hidden")) hideNotice();
      } catch (error) {
        if (error.status === 404) {
          state = null;
          els.mode.textContent = "Room tidak ditemukan";
          showNotice(error.message, false);
          [els.join, els.lobby, els.questions, els.turn, els.result].forEach((el) => toggle(el, false));
          return;
        }
        pollStep += 1;
        showNotice(error.message, true);
      } finally {
        inFlight = false;
      }
      schedulePoll();
    }

    function describeRoom(view) {
      const parts = [view.mode_title];
      if (view.relation_label) parts.push(view.relation_label);
      if (view.flavor_label) parts.push("Rasa " + view.flavor_label);
      return parts.join(" · ");
    }

    function describeExpiry(view) {
      const expires = new Date(view.expires_at);
      if (isNaN(expires.getTime())) return "";
      return (
        "Berlaku sampai " +
        expires.toLocaleString("id-ID", { weekday: "long", hour: "2-digit", minute: "2-digit" })
      );
    }

    function renderPeople(view) {
      clearNode(els.lobbyPeople);
      view.participants.forEach((person) => {
        const item = makeEl("li", "quiz-person" + (person.is_me ? " is-me" : ""));
        item.appendChild(makeEl("span", "quiz-person-hanzi", person.hanzi || "?"));
        const body = makeEl("div", "quiz-person-body");
        body.appendChild(makeEl("span", "quiz-person-name", person.name));
        const tags = [];
        if (person.shio) tags.push(person.shio);
        if (person.is_host) tags.push("pembuat room");
        if (person.is_me) tags.push("kamu");
        body.appendChild(makeEl("span", "quiz-person-tags", tags.join(" · ")));
        item.appendChild(body);
        if (view.mode === "pasangan") {
          const done = person.answered;
          const badge = makeEl("span", "quiz-person-state" + (done ? " done" : ""), done ? "Sudah jawab" : "Belum jawab");
          item.appendChild(badge);
        }
        els.lobbyPeople.appendChild(item);
      });
      els.lobbyCount.textContent = view.participant_count + "/" + view.max_participants;
    }

    function describeLobby(view) {
      const me = view.me;
      const count = view.participant_count;
      if (view.mode === "pasangan") {
        if (count < 2) return "Bagikan kode room ke orangnya. Soal bisa kamu jawab sambil menunggu.";
        if (me && me.answered) return "Jawabanmu tersimpan. Menunggu jawaban satunya lagi.";
        return "Kalian sudah berdua. Tinggal jawab soalnya.";
      }
      if (view.status === "lobby") {
        const missing = view.min_participants - count;
        if (missing > 0) return "Butuh " + missing + " orang lagi sebelum bisa mulai.";
        if (me && me.is_host) return "Sudah cukup. Mulai sekarang, atau tunggu sampai " + view.max_participants + " orang.";
        return "Menunggu pembuat room menekan Mulai.";
      }
      if (view.turn) {
        return view.turn.finished_players + " dari " + count + " pemain sudah selesai menebak.";
      }
      return "Permainan sedang berjalan.";
    }

    function renderLobby(view) {
      const visible = view.status !== "done";
      toggle(els.lobby, visible);
      if (!visible) return;
      renderPeople(view);
      els.lobbyStatus.textContent = describeLobby(view);
      const isHost = Boolean(view.me && view.me.is_host);
      const canStart = isHost && view.mode !== "pasangan" && view.status === "lobby";
      toggle(els.start, canStart);
      els.start.disabled = view.participant_count < view.min_participants;
      toggle(els.finish, isHost && view.mode === "tebak" && view.status === "playing");
    }

    function renderJoin(view) {
      const canJoin = !view.me && view.status === "lobby" && view.participant_count < view.max_participants;
      toggle(els.join, canJoin);
      if (canJoin) {
        els.joinInfo.textContent =
          describeRoom(view) + ". Sudah ada " + view.participant_count + " dari " + view.max_participants + " orang.";
      } else if (!view.me && view.status !== "done") {
        showNotice("Room ini sudah mulai atau sudah penuh, jadi kamu hanya bisa melihat daftar pesertanya.", false);
      } else if (!view.me) {
        showNotice("Room ini sudah selesai. Hasilnya hanya bisa dibuka oleh pesertanya.", false);
      }
    }

    function renderQuestions(view) {
      const visible = Boolean(view.me && view.questions);
      toggle(els.questions, visible);
      if (!visible || questionsRendered) return;
      questionsRendered = true;
      clearNode(els.questionList);
      view.questions.forEach((question, index) => {
        const item = makeEl("li", "quiz-question");
        const fieldset = makeEl("fieldset", "quiz-question-set");
        fieldset.appendChild(makeEl("legend", "quiz-question-text", question.question));
        question.options.forEach((option, optionIndex) => {
          const label = makeEl("label", "quiz-answer");
          const input = document.createElement("input");
          input.type = "radio";
          input.name = "q-" + index;
          input.value = String(optionIndex);
          label.appendChild(input);
          label.appendChild(makeEl("span", "quiz-answer-text", option));
          fieldset.appendChild(label);
        });
        item.appendChild(fieldset);
        els.questionList.appendChild(item);
      });
    }

    function renderTurn(view) {
      const turn = view.turn;
      toggle(els.turn, Boolean(turn));
      if (!turn) return;
      const current = turn.current;
      byId("turn-points").textContent = turn.points + " poin";
      const title = byId("turn-title");
      const hints = byId("turn-hints");
      const options = byId("turn-options");
      const hintCount = byId("turn-hint-count");
      const wait = byId("turn-wait");
      clearNode(hints);
      clearNode(options);
      if (!current) {
        title.textContent = "Semua ronde selesai";
        hintCount.textContent = "";
        wait.textContent =
          "Kamu menebak benar " + turn.solved_rounds + " dari " + turn.total_rounds +
          " ronde. Hasil keluar begitu semua pemain selesai.";
        return;
      }
      title.textContent = "Ronde " + current.number + " dari " + turn.total_rounds;
      current.hints.forEach((hint) => hints.appendChild(makeEl("li", "quiz-hint-item", hint)));
      hintCount.textContent =
        "Petunjuk " + current.hints.length + " dari " + current.hints_total +
        ". Tiap tebakan salah membuka satu petunjuk lagi dan mengurangi poin.";
      wait.textContent = "";
      current.options.forEach((option) => {
        const wrong = current.wrong_slots.indexOf(option.slot) !== -1;
        const button = makeEl("button", "quiz-option" + (wrong ? " wrong" : ""), option.name);
        button.type = "button";
        button.disabled = wrong;
        if (wrong) button.setAttribute("aria-label", option.name + ", tebakan salah");
        button.addEventListener("click", () => submitGuess(current.round, option.slot, button));
        options.appendChild(button);
      });
    }

    function renderResult(view) {
      const done = view.status === "done" && Boolean(view.result);
      toggle(els.result, done);
      if (!done || resultRendered) return;
      resultRendered = true;
      renderQuizResult(view);
    }

    function render(view) {
      state = view;
      if (seat && !view.me) {
        clearSeat(code);
        seat = null;
      }
      els.mode.textContent = describeRoom(view);
      els.meta.textContent = view.participant_count + " dari " + view.max_participants + " orang · " + describeExpiry(view);
      renderJoin(view);
      renderLobby(view);
      renderQuestions(view);
      renderTurn(view);
      renderResult(view);
    }

    function post(path, body) {
      return api("/api/shio/quiz/rooms/" + code + path, {
        method: "POST",
        token: seat && seat.token,
        body: body || {},
      });
    }

    els.join.addEventListener("submit", (event) => {
      event.preventDefault();
      const name = byId("join-name").value.trim();
      const birthDate = readBirthInput("#join-birth");
      if (!name || !birthDate) {
        window.showErrorToast("Isi nama dan tanggal lahirmu dulu.");
        return;
      }
      window.setButtonLoading(els.joinSubmit, true, "Bergabung...");
      api("/api/shio/quiz/rooms/" + code + "/join", {
        method: "POST",
        body: { name: name, birth_date: birthDate },
      })
        .then((data) => {
          seat = { token: data.token, slot: data.slot };
          saveSeat(code, seat);
          return refresh();
        })
        .catch((error) => window.showErrorToast(error.message))
        .finally(() => window.setButtonLoading(els.joinSubmit, false));
    });

    els.questions.addEventListener("submit", (event) => {
      event.preventDefault();
      const answers = [];
      const total = els.questionList.children.length;
      for (let index = 0; index < total; index += 1) {
        const picked = els.questions.querySelector('input[name="q-' + index + '"]:checked');
        if (!picked) {
          window.showErrorToast("Soal nomor " + (index + 1) + " belum dijawab.");
          return;
        }
        answers.push(Number(picked.value));
      }
      window.setButtonLoading(els.answersSubmit, true, "Mengirim...");
      post("/answers", { answers: answers })
        .then(() => refresh())
        .catch((error) => window.showErrorToast(error.message))
        .finally(() => window.setButtonLoading(els.answersSubmit, false));
    });

    els.start.addEventListener("click", () => {
      window.setButtonLoading(els.start, true, "Memulai...");
      post("/start")
        .then(() => refresh())
        .catch((error) => window.showErrorToast(error.message))
        .finally(() =>
          window.setButtonLoading(
            els.start,
            false,
            null,
            !state || state.participant_count < state.min_participants
          )
        );
    });

    els.finish.addEventListener("click", () => {
      if (Date.now() > finishArmedUntil) {
        finishArmedUntil = Date.now() + FINISH_CONFIRM_MS;
        window.showToast("Klik sekali lagi untuk mengakhiri. Ronde yang belum terjawab dihitung 0 poin.", "info");
        return;
      }
      finishArmedUntil = 0;
      post("/finish")
        .then(() => refresh())
        .catch((error) => window.showErrorToast(error.message));
    });

    function submitGuess(round, slot, button) {
      document.querySelectorAll("#turn-options .quiz-option").forEach((option) => {
        option.disabled = true;
      });
      post("/guess", { round: round, slot: slot })
        .then((outcome) => {
          if (outcome.correct) {
            window.showToast("Benar! +" + outcome.points + " poin.", "info");
          } else {
            button.classList.add("wrong");
            window.showToast("Bukan dia. Satu petunjuk baru terbuka.", "error");
          }
          return refresh();
        })
        .catch((error) => {
          window.showErrorToast(error.message);
          return refresh();
        });
    }

    byId("btn-copy").addEventListener("click", () => {
      const url = roomUrl();
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard
          .writeText(url)
          .then(() => window.showToast("Tautan room tersalin.", "info"))
          .catch(() => window.showToast(url, "info"));
      } else {
        window.showToast(url, "info");
      }
    });

    byId("btn-share").addEventListener("click", () => {
      const text = "Gabung ke room Quiz Shio-ku, kodenya " + code + ": " + roomUrl();
      if (navigator.share) {
        navigator.share({ title: "Quiz Shio Bareng", text: text, url: roomUrl() }).catch(() => {});
        return;
      }
      window.open("https://wa.me/?text=" + encodeURIComponent(text), "_blank", "noopener");
    });

    els.refresh.addEventListener("click", () => {
      lastChangeAt = Date.now();
      pollStep = 0;
      hideNotice();
      refresh();
    });

    document.addEventListener("visibilitychange", () => {
      if (document.hidden) {
        clearTimeout(pollTimer);
        pollTimer = null;
        return;
      }
      if (state && state.status !== "done") {
        pollStep = 0;
        refresh();
      }
    });

    refresh();
  }

  document.addEventListener("DOMContentLoaded", () => {
    if (byId("quiz-room")) initRoom();
    else if (byId("quiz-join-form")) initHub();
    window.initBurstParticles();
  });
})();
