(function () {
  const Weton = window.Weton;
  const byId = Weton.byId;
  const SIDES = ["a", "b"];
  const TEXT_FIELDS = { a: ["jam", "kota"], b: ["nama", "jam", "kota"] };
  const SOLO_CARDS = 4;
  const DUO_CARDS = 2;
  let els = null;
  const pickers = {};
  let renderedResult = null;
  let shown = { solo: [], duo: [] };

  function nextIndex(pool, current) {
    if (pool.length <= current.length) return null;
    const last = Math.max.apply(null, current);
    for (let step = 1; step <= pool.length; step += 1) {
      const candidate = (last + step) % pool.length;
      if (current.indexOf(candidate) === -1) return candidate;
    }
    return null;
  }

  function buildCard(group, pool, slot, label) {
    const card = Weton.el("article", "wt-card wt-roast-card wt-roast-card-" + group);
    card.appendChild(Weton.el("p", "wt-result-label", label));
    card.appendChild(Weton.el("p", "wt-roast-text", pool[shown[group][slot]]));
    const actions = Weton.el("div", "wt-roast-actions");
    const reroll = Weton.el("button", "wt-btn wt-btn-ghost wt-roast-reroll");
    reroll.type = "button";
    reroll.dataset.group = group;
    reroll.dataset.slot = String(slot);
    const icon = Weton.el("i", "fa-solid fa-shuffle");
    icon.setAttribute("aria-hidden", "true");
    reroll.appendChild(icon);
    reroll.appendChild(document.createTextNode(" Acak ulang"));
    reroll.disabled = pool.length <= shown[group].length;
    actions.appendChild(reroll);
    card.appendChild(actions);
    return card;
  }

  function renderCards(result) {
    Weton.clear(els.cards);
    shown.solo.forEach((_, slot) => {
      els.cards.appendChild(buildCard("solo", result.roasts, slot, "Roast " + (slot + 1)));
    });
    Weton.clear(els.duoCards);
    if (result.duo) {
      shown.duo.forEach((_, slot) => {
        els.duoCards.appendChild(buildCard("duo", result.duo.roasts, slot, "Roast berdua " + (slot + 1)));
      });
    }
  }

  function renderResult(result) {
    els.empty.hidden = Boolean(result);
    els.result.hidden = !result;
    if (!result) {
      renderedResult = null;
      return;
    }
    if (result !== renderedResult) {
      shown = {
        solo: result.roasts.slice(0, SOLO_CARDS).map((text, index) => index),
        duo: result.duo ? result.duo.roasts.slice(0, DUO_CARDS).map((text, index) => index) : [],
      };
      renderedResult = result;
    }
    const weton = result.person.weton;
    els.meta.textContent = "Neptu " + weton.neptu + " · " + result.person.paarasan;
    els.title.textContent = "Roasting " + weton.label;
    els.maghrib.textContent = result.person.maghrib.text;
    els.maghrib.dataset.kind = result.person.maghrib.kind;
    els.duo.hidden = !result.duo;
    if (result.duo) {
      els.duoTitle.textContent = Weton.duoLabel(result);
      els.duoSub.textContent = result.duo.partner.weton.label + " · " + result.duo.petung.formula + " → " +
        result.duo.petung.result_name + " (" + result.duo.petung.tone_label.toLowerCase() + ")";
    }
    renderCards(result);
    els.disclaimer.textContent = result.disclaimer + " Sumber: " + result.source;
  }

  function render(state) {
    window.setButtonLoading(els.submit, state.loading, "Menyiapkan roasting...");
    Weton.showError(els.error, state.error);
    renderResult(state.result);
  }

  function syncInputs(form) {
    SIDES.forEach((side) => {
      Weton.syncPicker(pickers[side], byId("d-" + side + "-tanggal"), form[side + "_tanggal"]);
    });
    Weton.syncInputs(els.fields, form);
    els.duoToggle.checked = Boolean(form.duo);
    els.duoFields.hidden = !form.duo;
  }

  function init(root) {
    els = {
      form: byId("d-roast-form"),
      submit: byId("d-roast-submit"),
      error: byId("d-roast-error"),
      empty: byId("d-roast-empty"),
      result: byId("d-roast-result"),
      meta: byId("d-roast-meta"),
      title: byId("d-roast-title"),
      maghrib: byId("d-roast-maghrib"),
      cards: byId("d-roast-cards"),
      duo: byId("d-roast-duo"),
      duoTitle: byId("d-roast-duo-title"),
      duoSub: byId("d-roast-duo-sub"),
      duoCards: byId("d-roast-duo-cards"),
      disclaimer: byId("d-roast-disclaimer"),
      duoToggle: byId("d-duo"),
      duoFields: byId("d-duo-fields"),
      fields: {},
    };
    SIDES.forEach((side) => {
      pickers[side] = Weton.initDate(byId("d-" + side + "-tanggal"), (str) => Weton.updateForm({ [side + "_tanggal"]: str }));
      TEXT_FIELDS[side].forEach((field) => {
        els.fields[side + "_" + field] = byId("d-" + side + "-" + field);
      });
    });
    Weton.bindInputs(els.fields);
    els.duoToggle.addEventListener("change", () => {
      Weton.updateForm({ duo: els.duoToggle.checked });
      els.duoFields.hidden = !els.duoToggle.checked;
    });
    els.form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const message = Weton.roastError(Weton.getState().form);
      if (message) {
        Weton.showError(els.error, message);
        return;
      }
      if (await Weton.submit()) Weton.showResult(els.result);
    });
    root.addEventListener("click", (event) => {
      const button = event.target.closest(".wt-roast-reroll");
      if (!button) return;
      const result = Weton.getState().result;
      if (!result) return;
      const group = button.dataset.group;
      const pool = group === "duo" ? result.duo.roasts : result.roasts;
      const replacement = nextIndex(pool, shown[group]);
      if (replacement === null) return;
      shown[group][Number(button.dataset.slot)] = replacement;
      const card = button.closest(".wt-roast-card");
      card.querySelector(".wt-roast-text").textContent = pool[replacement];
    });
  }

  function activate(state) {
    syncInputs(state.form);
    render(state);
  }

  Weton.registerRenderer("desktop", { init: init, render: render, activate: activate });
})();
