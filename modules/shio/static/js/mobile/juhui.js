(function () {
  const Shio = window.Shio;
  const byId = Shio.byId;

  function lobbyRenderer() {
    let els = null;
    let step = 1;

    function render(state) {
      const form = state.form;
      const tab = state.ui.tab || "join";
      els.tabs.forEach((button) => {
        const on = button.dataset.quizTab === tab;
        button.classList.toggle("is-active", on);
        button.setAttribute("aria-selected", on ? "true" : "false");
      });
      els.join.hidden = tab !== "join";
      els.create.hidden = tab !== "create";
      if (!form.mode) step = 1;
      Shio.renderStepper(els, step, 2);
      Shio.quizLobby.renderOptions(els.root, form);
      els.title.textContent = Shio.quizLobby.modeTitle(els.root, form.mode);
      if (state.loading) {
        window.setButtonLoading(els.next, true, "Menyiapkan room...");
      } else {
        window.setButtonLoading(els.next, false);
        els.next.textContent = step === 2 ? "Buat room" : "Lanjut";
      }
    }

    function goNext() {
      const form = Shio.getState().form;
      if (step === 1) {
        if (!form.mode) {
          window.showErrorToast("Pilih mode quiz dulu.");
          return;
        }
        step = 2;
        render(Shio.getState());
        window.scrollTo(0, 0);
        return;
      }
      Shio.quizLobby.createRoom();
    }

    function init(root) {
      els = {
        root: root,
        tabs: Array.from(root.querySelectorAll("[data-quiz-tab]")),
        join: byId("m-quiz-join"),
        create: byId("m-quiz-create"),
        code: byId("m-quiz-code"),
        name: byId("m-quiz-name"),
        birth: byId("m-quiz-birth"),
        steps: Array.from(root.querySelectorAll(".sh-m-step")),
        progressText: byId("m-quiz-progress-text"),
        progressFill: byId("m-quiz-progress-fill"),
        title: byId("m-quiz-create-title"),
        back: byId("m-quiz-back"),
        next: byId("m-quiz-next"),
      };
      els.tabs.forEach((button) => {
        button.addEventListener("click", () => Shio.updateUi({ tab: button.dataset.quizTab }));
      });
      Shio.quizLobby.bindJoin(els, els.join);
      Shio.mobileDate(els.birth, (value) => Shio.updateForm({ birth: value }));
      Shio.quizLobby.bindOptions(root, () => render(Shio.getState()));
      els.next.addEventListener("click", goNext);
      els.back.addEventListener("click", () => {
        step = 1;
        render(Shio.getState());
      });
    }

    function activate(state) {
      els.code.value = state.form.code || "";
      els.name.value = state.form.name || "";
      els.birth.value = state.form.birth || "";
      if (state.form.mode && !state.ui.tab) Shio.updateUi({ tab: "create" });
      render(Shio.getState());
    }

    return { init: init, render: render, activate: activate };
  }

  function roomRenderer() {
    const Room = Shio.quizRoom;
    let els = null;
    let renderedView = null;
    let renderedBusy = null;
    let renderedQuestion = -1;
    let resultBuilt = false;
    let questionIndex = 0;

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
      return Shio.detailsBlock(section.title, section.icon, section.node, !section.collapsed);
    }

    function renderResult(view) {
      if (resultBuilt) return;
      resultBuilt = true;
      Room.renderResultInto(els, view, renderSection);
    }

    function render(state) {
      const view = state.room;
      Room.renderHeader(els, state);
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
        els.joinInfo.textContent = Room.describeJoin(view);
      }
      if (flags.showQuestions) renderQuestion(view, state.busy);
      if (flags.showResult) renderResult(view);
      if (view === renderedView && state.busy === renderedBusy) return;
      renderedView = view;
      renderedBusy = state.busy;
      Room.renderLobby(els, view, state, flags);
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
      Shio.mobileDate(els.birth, (value) => Shio.updateForm({ birth: value }));
      els.questionNext.addEventListener("click", nextQuestion);
      els.questionBack.addEventListener("click", () => {
        questionIndex = Math.max(0, questionIndex - 1);
        render(Shio.getState());
      });
      Room.bindActions(els, "m");
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

    return { init: init, render: render, activate: activate };
  }

  Shio.onBoot((app) => {
    Shio.registerRenderer("mobile", app.dataset.roomCode ? roomRenderer() : lobbyRenderer());
  });
})();
