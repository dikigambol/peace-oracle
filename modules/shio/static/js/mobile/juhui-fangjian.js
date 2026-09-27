(function () {
  const Shio = window.Shio;
  const Room = Shio.quizRoom;
  let els = null;
  let renderedView = null;
  let renderedBusy = null;
  let renderedQuestion = -1;
  let resultBuilt = false;
  let questionIndex = 0;

  function byId(id) {
    return document.getElementById(id);
  }

  function renderNotice(state) {
    const view = state.room;
    const notice = state.notice || (view && Room.outsiderNotice(view) ? { text: Room.outsiderNotice(view), refresh: false } : null);
    els.notice.hidden = !notice;
    els.noticeText.textContent = notice ? notice.text : "";
    els.refresh.hidden = !(notice && notice.refresh);
  }

  function renderQuestion(view, busy) {
    const total = view.questions.length;
    questionIndex = Math.min(questionIndex, total - 1);
    els.questionProgress.textContent = "Soal " + (questionIndex + 1) + " dari " + total;
    els.questionFill.style.width = ((questionIndex + 1) / total) * 100 + "%";
    els.questionBack.hidden = questionIndex === 0;
    if (busy === "answers") window.setButtonLoading(els.questionNext, true, "Mengirim...");
    else {
      window.setButtonLoading(els.questionNext, false);
      els.questionNext.textContent = questionIndex === total - 1 ? "Kirim jawaban" : "Lanjut";
    }
    if (renderedQuestion === questionIndex) return;
    renderedQuestion = questionIndex;
    Shio.clear(els.question);
    els.question.appendChild(Room.buildQuestion(view.questions[questionIndex], questionIndex));
  }

  function renderSection(section) {
    const details = Shio.el("details", "sh-m-details");
    details.open = !section.collapsed;
    const summary = Shio.el("summary");
    const label = Shio.el("span");
    label.appendChild(Shio.icon(section.icon));
    label.appendChild(document.createTextNode(" " + section.title));
    summary.appendChild(label);
    details.appendChild(summary);
    const body = Shio.el("div", "sh-m-details-body");
    body.appendChild(section.node);
    details.appendChild(body);
    return details;
  }

  function renderResult(view) {
    if (resultBuilt) return;
    resultBuilt = true;
    const result = Room.buildResult(view);
    Shio.clear(els.verdict);
    els.verdict.appendChild(result.verdict);
    Shio.clear(els.sections);
    result.sections.forEach((section) => els.sections.appendChild(renderSection(section)));
    els.compat.hidden = !result.compat;
    if (result.compat) Shio.renderCompatLayers(els.compat, result.compat);
    els.note.hidden = !result.note;
    els.note.textContent = result.note || "";
  }

  function render(state) {
    const view = state.room;
    renderNotice(state);
    els.mode.textContent = view ? Room.describeRoom(view) : state.missing ? "Room tidak ditemukan" : "Memuat room...";
    els.meta.textContent = view ? Room.describeMeta(view) : "";
    const flags = view ? Room.roomFlags(view) : {};
    els.join.hidden = !flags.canJoin;
    els.lobby.hidden = !flags.showLobby;
    els.action.hidden = !(flags.showLobby && view.me);
    els.questions.hidden = !flags.showQuestions;
    els.turn.hidden = !flags.showTurn;
    els.result.hidden = !flags.showResult;
    window.setButtonLoading(els.joinSubmit, state.busy === "join", "Bergabung...");
    if (!view) return;
    if (flags.canJoin) {
      els.joinInfo.textContent = Room.describeRoom(view) + ". Sudah ada " + view.participant_count + " dari " + view.max_participants + " orang.";
    }
    if (flags.showQuestions) renderQuestion(view, state.busy);
    if (flags.showResult) renderResult(view);
    if (view === renderedView && state.busy === renderedBusy) return;
    renderedView = view;
    renderedBusy = state.busy;
    if (flags.showLobby) {
      Shio.clear(els.people);
      els.people.appendChild(Room.buildPeople(view));
      els.count.textContent = view.participant_count + "/" + view.max_participants;
      els.status.textContent = Room.describeLobby(view);
      els.start.hidden = !flags.showStart;
      window.setButtonLoading(els.start, state.busy === "start", "Memulai...", flags.startDisabled);
      els.finish.hidden = !flags.showFinish;
    }
    if (flags.showTurn) {
      Shio.clear(els.turn);
      els.turn.appendChild(Room.buildTurn(view));
    }
  }

  function nextQuestion() {
    const view = Shio.getState().room;
    if (!view || !view.questions) return;
    const answers = Shio.getState().form.answers || [];
    if (typeof answers[questionIndex] !== "number") {
      window.showErrorToast("Soal nomor " + (questionIndex + 1) + " belum dijawab.");
      return;
    }
    if (questionIndex < view.questions.length - 1) {
      questionIndex += 1;
      render(Shio.getState());
      return;
    }
    Room.submitAnswers();
  }

  function init(root) {
    els = {
      root: root,
      mode: byId("m-room-mode"),
      meta: byId("m-room-meta"),
      notice: byId("m-room-notice"),
      noticeText: byId("m-room-notice-text"),
      refresh: byId("m-room-refresh"),
      join: byId("m-room-join"),
      joinInfo: byId("m-room-join-info"),
      joinSubmit: byId("m-room-join-submit"),
      name: byId("m-room-name"),
      birth: byId("m-room-birth"),
      action: byId("m-room-action"),
      status: byId("m-room-status"),
      start: byId("m-room-start"),
      finish: byId("m-room-finish"),
      questions: byId("m-room-questions"),
      questionProgress: byId("m-room-question-progress"),
      questionFill: byId("m-room-question-fill"),
      question: byId("m-room-question"),
      questionBack: byId("m-room-question-back"),
      questionNext: byId("m-room-question-next"),
      turn: byId("m-room-turn"),
      result: byId("m-room-result"),
      verdict: byId("m-room-verdict"),
      sections: byId("m-room-sections"),
      compat: byId("m-room-compat"),
      note: byId("m-room-note"),
      lobby: byId("m-room-lobby"),
      count: byId("m-room-count"),
      people: byId("m-room-people"),
    };
    els.name.addEventListener("input", () => Shio.updateForm({ name: els.name.value }));
    Shio.mobileDate(els.birth, (value) => Shio.updateForm({ birth: value }));
    els.join.addEventListener("submit", (event) => {
      event.preventDefault();
      Room.join();
    });
    els.questionNext.addEventListener("click", nextQuestion);
    els.questionBack.addEventListener("click", () => {
      questionIndex = Math.max(0, questionIndex - 1);
      render(Shio.getState());
    });
    els.start.addEventListener("click", Room.start);
    els.finish.addEventListener("click", Room.finish);
    els.refresh.addEventListener("click", Room.manualRefresh);
    byId("m-room-copy").addEventListener("click", Room.copyLink);
    byId("m-room-share").addEventListener("click", Room.shareLink);
  }

  function activate(state) {
    els.name.value = state.form.name || "";
    els.birth.value = state.form.birth || "";
    const view = state.room;
    const missing = view && view.questions ? Room.missingAnswer(view) : 0;
    questionIndex = missing === -1 ? (view ? view.questions.length - 1 : 0) : missing;
    renderedView = null;
    renderedQuestion = -1;
    resultBuilt = false;
    render(state);
  }

  Shio.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
