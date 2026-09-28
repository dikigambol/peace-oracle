(function () {
  const Shio = window.Shio;
  const byId = Shio.byId;
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

  Shio.registerRenderer("desktop", { init: init, render: render, activate: activate });
})();
