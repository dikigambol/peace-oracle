(function () {
  const Shio = window.Shio;
  const byId = Shio.byId;

  function lobbyRenderer() {
    let els = null;
    let picker = null;

    function render(state) {
      const form = state.form;
      Shio.quizLobby.renderOptions(els.root, form);
      els.create.hidden = !form.mode;
      els.title.textContent = Shio.quizLobby.modeTitle(els.root, form.mode);
      window.setButtonLoading(els.submit, state.loading, "Menyiapkan room...");
    }

    function init(root) {
      els = {
        root: root,
        code: byId("d-quiz-code"),
        name: byId("d-quiz-name"),
        birth: byId("d-quiz-birth"),
        create: byId("d-quiz-create"),
        title: byId("d-quiz-create-title"),
        submit: byId("d-quiz-create-submit"),
      };
      picker = Shio.desktopDate(els.birth, {
        onChange: (dates, value) => Shio.updateForm({ birth: value || "" }),
      });
      Shio.quizLobby.bindJoin(els, byId("d-quiz-join"));
      Shio.quizLobby.bindOptions(root, (attribute) => {
        render(Shio.getState());
        if (attribute === "mode") Shio.scrollIntoView(els.create);
      });
      els.create.addEventListener("submit", (event) => {
        event.preventDefault();
        Shio.quizLobby.createRoom();
      });
    }

    function activate(state) {
      els.code.value = state.form.code || "";
      els.name.value = state.form.name || "";
      Shio.setDesktopDate(picker, els.birth, state.form.birth);
      render(state);
    }

    return { init: init, render: render, activate: activate };
  }

  function roomRenderer() {
    const Room = Shio.quizRoom;
    let els = null;
    let picker = null;
    let renderedView = null;
    let renderedBusy = null;
    let questionsBuilt = false;
    let resultBuilt = false;

    function renderQuestions(view) {
      if (questionsBuilt) return;
      questionsBuilt = true;
      Shio.clear(els.questionList);
      view.questions.forEach((question, index) => {
        const item = Shio.el("li", "quiz-question");
        item.appendChild(Room.buildQuestion(question, index));
        els.questionList.appendChild(item);
      });
    }

    function renderSection(section) {
      const card = Shio.el(section.collapsed ? "details" : "div", "quiz-card" + (section.collapsed ? " quiz-details" : ""));
      const title = Shio.el(section.collapsed ? "summary" : "h3", section.collapsed ? null : "quiz-section-title");
      if (!section.collapsed) title.appendChild(Shio.icon(section.icon));
      title.appendChild(document.createTextNode((section.collapsed ? "Lihat " : " ") + section.title));
      card.appendChild(title);
      card.appendChild(section.node);
      return card;
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
      els.questions.hidden = !flags.showQuestions;
      els.turn.hidden = !flags.showTurn;
      els.result.hidden = !flags.showResult;
      els.idle.hidden = Boolean(flags.showQuestions || flags.showTurn || flags.showResult);
      els.body.classList.toggle("sh-d-body-single", Boolean(flags.showResult && !flags.canJoin && !flags.showLobby));
      window.setButtonLoading(els.joinSubmit, state.busy === "join", "Bergabung...");
      window.setButtonLoading(els.answersSubmit, state.busy === "answers", "Mengirim...");
      if (!view) {
        els.idleText.textContent = state.missing ? "Room ini tidak ada atau sudah kedaluwarsa." : "Memuat room...";
        return;
      }
      els.idleText.textContent = view.me ? Room.describeLobby(view) : flags.canJoin ? "Isi nama dan tanggal lahir di atas untuk ikut main." : Room.describeLobby(view);
      if (flags.canJoin) {
        els.joinInfo.textContent = Room.describeJoin(view);
      }
      if (flags.showQuestions) renderQuestions(view);
      if (flags.showResult) renderResult(view);
      if (view === renderedView && state.busy === renderedBusy) return;
      renderedView = view;
      renderedBusy = state.busy;
      Room.renderLobby(els, view, state, flags);
    }

    function init(root) {
      els = {
        root: root,
        body: root.querySelector(".sh-d-body"),
        mode: byId("d-room-mode"),
        meta: byId("d-room-meta"),
        notice: byId("d-room-notice"),
        noticeText: byId("d-room-notice-text"),
        refresh: byId("d-room-refresh"),
        join: byId("d-room-join"),
        joinInfo: byId("d-room-join-info"),
        joinSubmit: byId("d-room-join-submit"),
        name: byId("d-room-name"),
        birth: byId("d-room-birth"),
        lobby: byId("d-room-lobby"),
        count: byId("d-room-count"),
        people: byId("d-room-people"),
        status: byId("d-room-status"),
        start: byId("d-room-start"),
        finish: byId("d-room-finish"),
        idle: byId("d-room-idle"),
        idleText: byId("d-room-idle-text"),
        questions: byId("d-room-questions"),
        questionList: byId("d-room-question-list"),
        answersSubmit: byId("d-room-answers-submit"),
        turn: byId("d-room-turn"),
        result: byId("d-room-result"),
        verdict: byId("d-room-verdict"),
        sections: byId("d-room-sections"),
        compat: byId("d-room-compat"),
        note: byId("d-room-note"),
      };
      picker = Shio.desktopDate(els.birth, {
        onChange: (dates, value) => Shio.updateForm({ birth: value || "" }),
      });
      els.questions.addEventListener("submit", (event) => {
        event.preventDefault();
        Room.submitAnswers();
      });
      Room.bindActions(els, "d");
    }

    function activate(state) {
      els.name.value = state.form.name || "";
      Shio.setDesktopDate(picker, els.birth, state.form.birth);
      renderedView = null;
      questionsBuilt = false;
      resultBuilt = false;
      render(state);
    }

    return { init: init, render: render, activate: activate };
  }

  Shio.onBoot((app) => {
    Shio.registerRenderer("desktop", app.dataset.roomCode ? roomRenderer() : lobbyRenderer());
  });
})();
