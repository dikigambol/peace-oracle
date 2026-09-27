(function () {
  const Shio = window.Shio;
  let els = null;
  let step = 1;

  function byId(id) {
    return document.getElementById(id);
  }

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
    els.steps.forEach((node) => {
      node.hidden = Number(node.dataset.step) !== step;
    });
    els.progressText.textContent = "Langkah " + step + " dari 2";
    els.progressFill.style.width = step * 50 + "%";
    els.back.hidden = step === 1;
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
    els.code.addEventListener("input", () => Shio.updateForm({ code: els.code.value }));
    els.name.addEventListener("input", () => Shio.updateForm({ name: els.name.value }));
    Shio.mobileDate(els.birth, (value) => Shio.updateForm({ birth: value }));
    Shio.quizLobby.bindOptions(root, () => render(Shio.getState()));
    els.join.addEventListener("submit", (event) => {
      event.preventDefault();
      if (!Shio.quizLobby.joinByCode()) els.code.focus();
    });
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

  Shio.registerRenderer("mobile", { init: init, render: render, activate: activate });
})();
