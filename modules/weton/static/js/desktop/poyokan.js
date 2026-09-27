(function () {
  const Weton = window.Weton;
  const SIDES = ["a", "b"];
  const TEXT_FIELDS = { a: ["jam", "kota"], b: ["nama", "jam", "kota"] };
  const SOLO_CARDS = 4;
  const DUO_CARDS = 2;
  let els = null;
  const pickers = {};
  let renderedResult = null;
  let shown = { solo: [], duo: [] };

  function byId(id) {
    return document.getElementById(id);
  }

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
    shown.solo.forEach((index, slot) => {
      els.cards.appendChild(buildCard("solo", result.roasts, slot, "Roast " + (slot + 1)));
    });
    Weton.clear(els.duoCards);
    if (result.duo) {
      shown.duo.forEach((index, slot) => {
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
    els.error.hidden = !state.error;
    els.error.textContent = state.error;
    renderResult(state.result);
  }

  function syncInputs(form) {
    SIDES.forEach((side) => {
      const value = form[side + "_tanggal"] || "";
      if (pickers[side]) {
        if (value) pickers[side].setDate(value, false);
        else pickers[side].clear(false);
      } else {
        byId("d-" + side + "-tanggal").value = value;
      }
      TEXT_FIELDS[side].forEach((field) => {
        byId("d-" + side + "-" + field).value = form[side + "_" + field] || "";
      });
    });
    els.duoToggle.checked = Boolean(form.duo);
    els.duoFields.hidden = !form.duo;
  }

  function init(root) {
    els = {
      root: root,
      form: byId("d-roast-form"),
      submit: byId("d-roast-submit"),
      error: byId("d-roast-error"),
      empty: byId("d-roast-empty"),
      result: byId("d-roast-result"),
      meta: byId("d-roast-meta"),
      title: byId("d-roast-title"),
      share: byId("d-roast-share"),
      maghrib: byId("d-roast-maghrib"),
      cards: byId("d-roast-cards"),
      duo: byId("d-roast-duo"),
      duoTitle: byId("d-roast-duo-title"),
      duoSub: byId("d-roast-duo-sub"),
      duoCards: byId("d-roast-duo-cards"),
      disclaimer: byId("d-roast-disclaimer"),
      duoToggle: byId("d-duo"),
      duoFields: byId("d-duo-fields"),
    };
    SIDES.forEach((side) => {
      const input = byId("d-" + side + "-tanggal");
      window.initDatePicker("#d-" + side + "-tanggal", {
        dateFormat: "Y-m-d",
        altInput: true,
        altFormat: "j F Y",
        locale: "id",
        minDate: input.dataset.min,
        maxDate: input.dataset.max,
        disableMobile: true,
        onChange: (dates, str) => Weton.updateForm({ [side + "_tanggal"]: str }),
      });
      pickers[side] = input._flatpickr || null;
      TEXT_FIELDS[side].forEach((field) => {
        const node = byId("d-" + side + "-" + field);
        node.addEventListener("input", () => Weton.updateForm({ [side + "_" + field]: node.value }));
      });
    });
    els.duoToggle.addEventListener("change", () => {
      Weton.updateForm({ duo: els.duoToggle.checked });
      els.duoFields.hidden = !els.duoToggle.checked;
    });
    els.form.addEventListener("submit", (event) => {
      event.preventDefault();
      const form = Weton.getState().form;
      let message = "";
      if (!form.a_tanggal) message = "Isi tanggal lahirmu dulu.";
      else if (form.duo && !form.b_tanggal) message = "Isi tanggal lahir orang kedua dulu, atau matikan roasting berdua.";
      if (message) {
        els.error.hidden = false;
        els.error.textContent = message;
        return;
      }
      Weton.submit();
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
    els.share.addEventListener("click", () => {
      const result = Weton.getState().result;
      if (result) Weton.share(Weton.roastShare(result, result.roasts[shown.solo[0]]));
    });
  }

  function activate(state) {
    syncInputs(state.form);
    render(state);
  }

  Weton.registerRenderer("desktop", { init: init, render: render, activate: activate });
})();
