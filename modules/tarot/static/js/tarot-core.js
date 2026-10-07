(function () {
  const MOBILE_QUERY = "(max-width: 768px)";
  const DECK_STORAGE_PREFIX = "tarot-deck:";
  const LEGACY_DECK_KEY = "tarot-deck";
  const DECKS = {
    rider: { label: "Rider-Waite 1909", ext: ".webp" },
    oracolo: { label: "Oracolo", ext: ".svg" },
  };
  const BOARD_LAYOUTS = {
    satu: "satu",
    tiga_waktu: "tiga",
    tiga_langkah: "tiga",
    celtic: "celtic",
    hubungan: "hubungan",
  };
  const renderers = {};
  const listeners = new Set();
  let state = {
    form: {},
    result: null,
    loading: false,
    error: "",
  };
  let activeLayout = null;
  let app = null;
  let availableDecks = ["rider"];
  let defaultDeck = "rider";
  let currentDeck = "rider";

  function getState() {
    return state;
  }

  function setState(patch) {
    state = Object.assign({}, state, patch);
    listeners.forEach((listener) => listener(state));
  }

  function updateForm(patch) {
    state = Object.assign({}, state, { form: Object.assign({}, state.form, patch) });
  }

  function registerRenderer(name, renderer) {
    renderers[name] = renderer;
  }

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined && text !== null) node.textContent = text;
    return node;
  }

  function icon(name) {
    const node = el("i", "fa-solid " + name);
    node.setAttribute("aria-hidden", "true");
    return node;
  }

  function clear(node) {
    while (node.firstChild) node.removeChild(node.firstChild);
  }

  function byId(id) {
    return document.getElementById(id);
  }

  function showError(node, message) {
    node.hidden = !message;
    node.textContent = message || "";
  }

  function readDeckOptions() {
    const listed = (app.dataset.decks || "").split(" ").filter((deck) => DECKS[deck]);
    availableDecks = listed.length ? listed : ["rider"];
    defaultDeck = availableDecks.includes(app.dataset.deck) ? app.dataset.deck : availableDecks[0];
  }

  function deckStorageKey() {
    return DECK_STORAGE_PREFIX + app.dataset.deckDay;
  }

  function readStoredDeck() {
    try {
      window.localStorage.removeItem(LEGACY_DECK_KEY);
      const stored = window.localStorage.getItem(deckStorageKey());
      return availableDecks.includes(stored) ? stored : defaultDeck;
    } catch (error) {
      return defaultDeck;
    }
  }

  function storeDeck(deck) {
    try {
      window.localStorage.setItem(deckStorageKey(), deck);
    } catch (error) {
      return;
    }
  }

  function imageBase() {
    return app ? app.dataset.images : "";
  }

  function cardSrc(slug, deck) {
    const key = DECKS[deck] ? deck : currentDeck;
    return imageBase() + key + "/" + slug + DECKS[key].ext;
  }

  function backSrc() {
    return imageBase() + currentDeck + "/retro.svg";
  }

  function applyDeck(root) {
    root.querySelectorAll("img[data-card]:not([data-fixed-deck])").forEach((img) => {
      const src = cardSrc(img.dataset.card);
      if (img.getAttribute("src") !== src) img.setAttribute("src", src);
    });
    root.querySelectorAll("img[data-back]").forEach((img) => {
      const src = backSrc();
      if (img.getAttribute("src") !== src) img.setAttribute("src", src);
    });
  }

  function syncDeckControls() {
    document.querySelectorAll("[data-deck-choice]").forEach((button) => {
      const on = button.dataset.deckChoice === currentDeck;
      button.classList.toggle("is-active", on);
      button.setAttribute("aria-checked", on ? "true" : "false");
      button.tabIndex = on ? 0 : -1;
    });
    document.querySelectorAll("[data-deck-toggle]").forEach((button) => {
      button.setAttribute("aria-label", "Ganti dek kartu, sekarang " + DECKS[currentDeck].label);
      button.dataset.deck = currentDeck;
    });
  }

  function setDeck(deck, persist) {
    currentDeck = availableDecks.includes(deck) ? deck : defaultDeck;
    if (app) app.dataset.deck = currentDeck;
    if (persist) storeDeck(currentDeck);
    applyDeck(document);
    syncDeckControls();
  }

  function nextDeck(step) {
    const count = availableDecks.length;
    return availableDecks[(availableDecks.indexOf(currentDeck) + step + count) % count];
  }

  function bindDeckControls() {
    if (availableDecks.length < 2) return;
    document.querySelectorAll("[data-deck-choice]").forEach((button) => {
      button.addEventListener("click", () => setDeck(button.dataset.deckChoice, true));
      button.addEventListener("keydown", (event) => {
        const forward = event.key === "ArrowRight" || event.key === "ArrowDown";
        const backward = event.key === "ArrowLeft" || event.key === "ArrowUp";
        if (!forward && !backward) return;
        event.preventDefault();
        setDeck(nextDeck(forward ? 1 : -1), true);
        const group = button.closest("[role='radiogroup']");
        const active = group && group.querySelector("[data-deck-choice='" + currentDeck + "']");
        if (active) active.focus();
      });
    });
    document.querySelectorAll("[data-deck-toggle]").forEach((button) => {
      button.addEventListener("click", () => {
        setDeck(nextDeck(1), true);
        window.showToast("Dek kartu sekarang " + DECKS[currentDeck].label + ".", "info");
      });
    });
  }

  function setImageSize(img) {
    img.width = 360;
    img.height = 620;
    img.decoding = "async";
  }

  function cardImage(card, extraClass) {
    const img = el("img", "tr-card-img" + (extraClass ? " " + extraClass : ""));
    img.dataset.card = card.slug;
    img.src = cardSrc(card.slug);
    img.alt = card.name + (card.reversed ? ", posisi terbalik" : "");
    setImageSize(img);
    return img;
  }

  function backImage(extraClass) {
    const img = el("img", "tr-card-img tr-card-back" + (extraClass ? " " + extraClass : ""));
    img.dataset.back = "";
    img.src = backSrc();
    img.alt = "";
    setImageSize(img);
    return img;
  }

  function cardFace(card, extraClass) {
    const figure = el("figure", "tr-face" + (card.reversed ? " is-reversed" : "") + (extraClass ? " " + extraClass : ""));
    figure.appendChild(cardImage(card));
    return figure;
  }

  function flipCard(card, extraClass) {
    const wrap = el("div", "tr-flip" + (card.reversed ? " is-reversed" : "") + (extraClass ? " " + extraClass : ""));
    const inner = el("div", "tr-flip-inner");
    inner.appendChild(backImage("tr-flip-back"));
    inner.appendChild(cardImage(card, "tr-flip-front"));
    wrap.appendChild(inner);
    return wrap;
  }

  function reveal(nodes, step) {
    const list = Array.from(nodes);
    if (window.prefersReducedMotion()) {
      list.forEach((node) => node.classList.add("is-revealed"));
      return;
    }
    list.forEach((node, index) => {
      setTimeout(() => node.classList.add("is-revealed"), 150 + index * (step || 200));
    });
  }

  function createFan(nodes, options) {
    const size = Number(nodes.fan.dataset.size) || 78;
    const buttons = [];
    let target = Number(nodes.fan.dataset.count) || 1;

    function picks() {
      return (state.form.picks || []).slice();
    }

    function update() {
      const current = picks();
      const full = current.length >= target;
      buttons.forEach((button, index) => {
        const order = current.indexOf(index);
        const picked = order !== -1;
        button.classList.toggle("is-picked", picked);
        button.classList.toggle("is-muted", full && !picked);
        button.setAttribute("aria-pressed", picked ? "true" : "false");
        button.setAttribute("aria-label", "Kartu tertutup ke-" + (index + 1) + (picked ? ", pilihan ke-" + (order + 1) : ""));
        button.querySelector(".tr-fan-badge").textContent = picked ? String(order + 1) : "";
      });
      nodes.count.textContent = current.length + " dari " + target + " kartu dipilih";
      nodes.count.classList.toggle("is-full", full);
      if (options.onChange) options.onChange(current, target);
    }

    function toggle(index) {
      const current = picks();
      const position = current.indexOf(index);
      if (position !== -1) {
        current.splice(position, 1);
      } else if (current.length < target) {
        current.push(index);
      } else {
        nodes.count.classList.remove("is-nudge");
        void nodes.count.offsetWidth;
        nodes.count.classList.add("is-nudge");
        return;
      }
      updateForm({ picks: current });
      update();
    }

    function shuffle(animate) {
      updateForm({ picks: [] });
      update();
      if (!animate || window.prefersReducedMotion()) return;
      nodes.fan.classList.remove("is-shuffling");
      void nodes.fan.offsetWidth;
      nodes.fan.classList.add("is-shuffling");
      setTimeout(() => nodes.fan.classList.remove("is-shuffling"), 700);
    }

    function setTarget(count) {
      target = count;
      nodes.fan.dataset.count = String(count);
      const current = picks();
      if (current.length > count) updateForm({ picks: current.slice(0, count) });
      update();
    }

    for (let index = 0; index < size; index += 1) {
      const button = el("button", "tr-fan-card");
      button.type = "button";
      const outer = index < Math.ceil(size / 2);
      button.style.setProperty("--i", String(index));
      button.style.setProperty("--j", String(outer ? index : index - Math.ceil(size / 2)));
      button.classList.add(outer ? "is-outer" : "is-inner");
      const back = backImage();
      back.loading = "lazy";
      button.appendChild(back);
      button.appendChild(el("span", "tr-fan-badge"));
      button.addEventListener("click", () => toggle(index));
      nodes.fan.appendChild(button);
      buttons.push(button);
    }
    nodes.shuffle.addEventListener("click", () => shuffle(true));
    update();

    return { update: update, shuffle: shuffle, setTarget: setTarget, target: () => target };
  }

  function bindToggle(input, key) {
    input.addEventListener("change", () => updateForm({ [key]: input.checked }));
  }

  function bindInputs(fields) {
    Object.entries(fields).forEach(([key, node]) => {
      node.addEventListener("input", () => updateForm({ [key]: node.value }));
    });
  }

  function syncInputs(fields, form) {
    Object.entries(fields).forEach(([key, node]) => {
      node.value = form[key] || "";
    });
  }

  function bindRadios(root, name, key) {
    root.querySelectorAll("input[name='" + name + "']").forEach((input) => {
      input.addEventListener("change", () => {
        if (input.checked) updateForm({ [key]: input.value });
      });
    });
  }

  function syncRadios(root, name, value) {
    root.querySelectorAll("input[name='" + name + "']").forEach((input) => {
      input.checked = input.value === value;
    });
  }

  function renderStepper(nodes, step, total) {
    nodes.steps.forEach((node) => {
      node.hidden = Number(node.dataset.step) !== step;
    });
    nodes.progressText.textContent = "Langkah " + step + " dari " + total;
    Array.from(nodes.marks.children).forEach((mark, index) => {
      mark.classList.toggle("is-done", index + 1 < step);
      mark.classList.toggle("is-current", index + 1 === step);
    });
    nodes.back.hidden = step === 1;
  }

  function toneBadge(tone, label) {
    return el("span", "tr-tone tr-tone-" + tone, label);
  }

  function badges(card) {
    const row = el("div", "tr-badges");
    row.appendChild(el("span", "tr-badge" + (card.reversed ? " tr-badge-rev" : ""), card.orientation_label));
    if (card.tone) row.appendChild(toneBadge(card.tone, card.tone_label));
    return row;
  }

  function keywordList(words) {
    const list = el("ul", "tr-keywords");
    words.forEach((word) => list.appendChild(el("li", null, word)));
    return list;
  }

  function saranBlock(text) {
    const advice = el("p", "tr-saran");
    advice.appendChild(el("strong", null, "Saran: "));
    advice.appendChild(document.createTextNode(text));
    return advice;
  }

  function cardLink(card) {
    const link = el("a", "tr-more-link", "Pelajari kartu ini ");
    link.href = (app ? app.dataset.cards : "") + "/" + card.slug;
    link.appendChild(icon("fa-arrow-right"));
    return link;
  }

  function subtitle(card) {
    const parts = [card.name_id, card.arcana_label];
    if (card.suit_label) parts.push("suit " + card.suit_label);
    return parts.join(" · ");
  }

  function renderReadingCard(card, index, prefix) {
    const article = el("article", "tr-card tr-reading-card tr-tone-edge-" + card.tone);
    if (card.position) {
      article.id = prefix + "-pos-" + (index + 1);
      const head = el("header", "tr-reading-head");
      head.appendChild(el("span", "tr-pos-number", String(index + 1)));
      const text = el("div");
      text.appendChild(el("p", "tr-result-label", card.position.label));
      text.appendChild(el("p", "tr-position-prompt", card.position.prompt));
      head.appendChild(text);
      article.appendChild(head);
    }
    const body = el("div", "tr-reading-body");
    body.appendChild(cardFace(card, "tr-reading-face"));
    const info = el("div", "tr-reading-info");
    info.appendChild(el("h3", "tr-card-name", card.name));
    info.appendChild(el("p", "tr-card-sub", subtitle(card)));
    info.appendChild(badges(card));
    info.appendChild(keywordList(card.keywords));
    body.appendChild(info);
    article.appendChild(body);
    article.appendChild(el("p", "tr-meaning-text", card.meaning));
    article.appendChild(saranBlock(card.saran));
    article.appendChild(cardLink(card));
    return article;
  }

  function renderSummary(node, result, extra) {
    clear(node);
    node.appendChild(el("p", "tr-eyebrow", "Gambaran umum"));
    if (result.question) node.appendChild(el("blockquote", "tr-question", "“" + result.question + "”"));
    const meta = [result.spread.name, result.spread.short, "topik " + result.topic.label.toLowerCase()];
    if (extra) meta.unshift(extra);
    if (!result.reversed_allowed) meta.push("semua kartu dibaca tegak");
    node.appendChild(el("p", "tr-summary-meta", meta.join(" · ")));
    const tone = el("div", "tr-summary-tone");
    tone.appendChild(toneBadge(result.overall.tone, result.overall.label));
    node.appendChild(tone);
    node.appendChild(el("p", "tr-summary-text", result.overall.text));
  }

  function renderBoard(node, result, prefix) {
    clear(node);
    const layout = BOARD_LAYOUTS[result.spread.key] || "tiga";
    node.className = "tr-board tr-board-" + layout;
    const flips = [];
    result.cards.forEach((card, index) => {
      const slot = el("a", "tr-slot tr-slot-" + (index + 1));
      slot.href = "#" + prefix + "-pos-" + (index + 1);
      slot.style.gridArea = layout === "celtic" && index === 1 ? "p1" : "p" + (index + 1);
      slot.setAttribute("aria-label", (index + 1) + ". " + card.position.label + ": " + card.name + (card.reversed ? ", terbalik" : ""));
      const flip = flipCard(card, "tr-slot-card");
      slot.appendChild(flip);
      const label = el("span", "tr-slot-label");
      label.setAttribute("aria-hidden", "true");
      label.appendChild(el("b", null, String(index + 1)));
      label.appendChild(document.createTextNode(" " + card.position.label));
      slot.appendChild(label);
      slot.addEventListener("click", (event) => {
        const target = byId(prefix + "-pos-" + (index + 1));
        if (!target) return;
        event.preventDefault();
        target.scrollIntoView({ behavior: window.prefersReducedMotion() ? "auto" : "smooth", block: "start" });
      });
      node.appendChild(slot);
      flips.push(flip);
    });
    reveal(flips, result.cards.length > 7 ? 140 : 220);
  }

  function renderInsights(node, result) {
    clear(node);
    if (result.patterns.length) {
      const section = el("section", "tr-card tr-insight");
      section.appendChild(el("h3", "tr-insight-title", "Pola dalam kartu"));
      result.patterns.forEach((pattern) => section.appendChild(el("p", "tr-insight-text", pattern.text)));
      node.appendChild(section);
    }
    if (result.relations.length) {
      const section = el("section", "tr-card tr-insight");
      section.appendChild(el("h3", "tr-insight-title", "Hubungan antar posisi"));
      result.relations.forEach((relation) => {
        const block = el("div", "tr-relation");
        block.appendChild(el("h4", "tr-relation-title", relation.title));
        block.appendChild(el("p", "tr-insight-text", relation.text));
        section.appendChild(block);
      });
      node.appendChild(section);
    }
    node.hidden = !node.children.length;
  }

  function renderCardList(node, result, prefix) {
    clear(node);
    result.cards.forEach((card, index) => node.appendChild(renderReadingCard(card, index, prefix)));
  }

  function renderFooter(prefix, result) {
    const disclaimer = byId(prefix + "-disclaimer");
    const sources = byId(prefix + "-sources");
    if (disclaimer && result.disclaimer) disclaimer.textContent = result.disclaimer;
    if (sources) sources.textContent = "Sumber: " + Object.values(result.sources || {}).join("; ") + ".";
  }

  function renderDaily(node, result) {
    clear(node);
    const card = result.card;
    const article = el("article", "tr-card tr-daily-result tr-tone-edge-" + card.tone);
    article.appendChild(el("p", "tr-eyebrow", "Kartu hari ini · " + result.date_label));
    article.appendChild(el("h2", "tr-card-name tr-card-name-lg", card.name));
    article.appendChild(el("p", "tr-card-sub", subtitle(card)));
    article.appendChild(badges(card));
    article.appendChild(keywordList(card.keywords));
    article.appendChild(el("p", "tr-meaning-text", card.meaning));
    article.appendChild(saranBlock(card.saran));
    const topics = el("div", "tr-topic-list");
    result.topics.filter((topic) => topic.key !== "umum").forEach((topic) => {
      const block = el("div", "tr-meaning");
      const title = el("h3", "tr-meaning-title");
      title.appendChild(icon(topic.icon));
      title.appendChild(document.createTextNode(" " + topic.label));
      block.appendChild(title);
      block.appendChild(el("p", null, card.meanings[topic.key]));
      topics.appendChild(block);
    });
    article.appendChild(topics);
    article.appendChild(el("p", "tr-hint", result.note));
    article.appendChild(cardLink(card));
    node.appendChild(article);
  }

  function renderStage(node, card) {
    clear(node);
    const flip = flipCard(card, "tr-stage-flip");
    node.appendChild(flip);
    reveal([flip], 0);
  }

  function resetStage(node) {
    clear(node);
    node.appendChild(backImage());
  }

  function renderYesNo(node, result) {
    clear(node);
    const card = result.card;
    const hero = el("section", "tr-card tr-answer tr-answer-" + result.answer.key);
    const flipWrap = el("div", "tr-answer-art");
    const flip = flipCard(card, "tr-answer-flip");
    flipWrap.appendChild(flip);
    hero.appendChild(flipWrap);
    const text = el("div", "tr-answer-main");
    text.appendChild(el("p", "tr-eyebrow", "Jawaban kartu"));
    text.appendChild(el("blockquote", "tr-question", "“" + result.question + "”"));
    text.appendChild(el("p", "tr-answer-label", result.answer.label));
    text.appendChild(el("p", "tr-answer-text", result.answer.text));
    text.appendChild(el("h3", "tr-card-name", card.name));
    text.appendChild(el("p", "tr-card-sub", subtitle(card)));
    text.appendChild(badges(card));
    text.appendChild(el("p", "tr-meaning-text", card.meaning));
    text.appendChild(saranBlock(card.saran));
    text.appendChild(cardLink(card));
    hero.appendChild(text);
    node.appendChild(hero);
    reveal([flip], 0);
  }

  function formulaList(lines) {
    const list = el("ol", "tr-formula");
    lines.forEach((line) => list.appendChild(el("li", null, line)));
    return list;
  }

  function birthCard(item) {
    const article = el("article", "tr-card tr-birth-card tr-birth-" + item.role);
    article.appendChild(el("p", "tr-result-label", item.role_label));
    const body = el("div", "tr-reading-body");
    body.appendChild(cardFace(item.card, "tr-reading-face"));
    const info = el("div", "tr-reading-info");
    info.appendChild(el("h3", "tr-card-name", item.card.name));
    info.appendChild(el("p", "tr-card-sub", item.card.name_id + " · angka " + item.birth_number));
    info.appendChild(el("p", "tr-meaning-text", item.text));
    info.appendChild(cardLink(item.card));
    body.appendChild(info);
    article.appendChild(body);
    return article;
  }

  function renderBirth(node, result) {
    clear(node);
    const intro = el("section", "tr-card tr-birth-intro");
    intro.appendChild(el("p", "tr-eyebrow", "Lahir " + result.input.tanggal_label));
    intro.appendChild(el("h2", "tr-card-name tr-card-name-lg", result.cards.map((item) => item.card.name).join(" · ")));
    intro.appendChild(el("p", "tr-summary-text", result.family));
    intro.appendChild(el("h3", "tr-insight-title", "Cara menghitung"));
    intro.appendChild(formulaList(result.formula));
    node.appendChild(intro);
    const grid = el("div", "tr-birth-grid");
    result.cards.forEach((item) => grid.appendChild(birthCard(item)));
    node.appendChild(grid);
    const year = result.year;
    const yearCard = birthCard({
      role: "tahun",
      role_label: "Kartu tahun " + year.tahun,
      birth_number: year.birth_number,
      card: year.card,
      text: year.text,
    });
    yearCard.appendChild(formulaList(year.formula));
    node.appendChild(yearCard);
    node.appendChild(el("p", "tr-hint", result.note));
  }

  function focusResult(node) {
    if (!node) return;
    if (!node.hasAttribute("tabindex")) node.setAttribute("tabindex", "-1");
    node.classList.add("tr-result-target");
    const behavior = window.prefersReducedMotion() ? "auto" : "smooth";
    if (activeLayout === "mobile") window.scrollTo({ top: 0, behavior: behavior });
    else node.scrollIntoView({ behavior: behavior, block: "start" });
    node.focus({ preventScroll: true });
  }

  function freshForm(form) {
    const next = { picks: [] };
    ["topic", "spread", "reversed"].forEach((key) => {
      if (form[key] !== undefined) next[key] = form[key];
    });
    return next;
  }

  function showResult(node) {
    state = Object.assign({}, state, { submitted: state.form, form: freshForm(state.form) });
    if (activeLayout && renderers[activeLayout]) renderers[activeLayout].activate(state);
    focusResult(node);
  }

  const PAYLOAD_BUILDERS = {
    giorno: (form) => ({ reversed: form.reversed !== false }),
    lettura: (form) => ({
      question: form.question || "",
      topic: form.topic,
      spread: form.spread,
      picks: form.picks || [],
      reversed: form.reversed !== false,
    }),
    sino: (form) => ({ question: form.question || "", picks: form.picks || [], reversed: form.reversed !== false }),
    legame: (form) => ({
      nama_a: form.nama_a || "",
      nama_b: form.nama_b || "",
      picks: form.picks || [],
      reversed: form.reversed !== false,
    }),
    nascita: (form) => ({ tanggal: form.tanggal || "", tahun: form.tahun || "" }),
  };

  async function submit() {
    if (state.loading) return false;
    setState({ loading: true, error: "" });
    try {
      const builder = PAYLOAD_BUILDERS[app.dataset.page];
      const result = await window.fetchJson(app.dataset.api, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(builder ? builder(state.form) : state.form),
      });
      setState({ loading: false, result: result });
      return true;
    } catch (error) {
      setState({ loading: false, error: error.message });
      return false;
    }
  }

  function reset() {
    setState({ result: null, error: "", form: freshForm(state.form) });
  }

  function questionError(form, required) {
    if (required && !(form.question || "").trim()) return "Tulis pertanyaanmu dulu.";
    return "";
  }

  function picksError(form, count) {
    const picked = (form.picks || []).length;
    if (picked < count) return "Ambil " + (count - picked) + " kartu lagi dari dek.";
    return "";
  }

  const COUNT_WORDS = { 1: "satu", 3: "tiga", 7: "tujuh", 10: "sepuluh" };

  function mapIds(ids) {
    const nodes = {};
    Object.entries(ids || {}).forEach(([key, id]) => {
      nodes[key] = byId(id);
    });
    return nodes;
  }

  function picksReady(form, fan) {
    return !fan || (form.picks || []).length === fan.target();
  }

  function setupForm(root, prefix, config) {
    const els = {
      fields: mapIds(config.fields),
      reversed: byId(prefix + "-reversed"),
      fan: byId(prefix + "-fan"),
      count: byId(prefix + "-fan-count"),
      shuffle: byId(prefix + "-shuffle"),
      fanTitle: byId(prefix + "-fan-title"),
    };
    bindInputs(els.fields);
    Object.entries(config.radios || {}).forEach(([key, name]) => bindRadios(root, name, key));
    if (els.reversed) bindToggle(els.reversed, "reversed");
    return els;
  }

  function spreadTarget(root, config, fan) {
    if (!config.spreadRadios) return fan.target();
    const checked = root.querySelector("input[name='" + config.spreadRadios + "']:checked");
    return checked ? Number(checked.dataset.count) : fan.target();
  }

  function syncFanTitle(els, fan) {
    if (els.fanTitle) els.fanTitle.textContent = "Ambil " + (COUNT_WORDS[fan.target()] || fan.target()) + " kartu";
  }

  function bindSpreads(root, config, els, getFan) {
    if (!config.spreadRadios) return;
    root.querySelectorAll("input[name='" + config.spreadRadios + "']").forEach((input) => {
      input.addEventListener("change", () => {
        if (!input.checked) return;
        updateForm({ spread: input.value });
        getFan().setTarget(Number(input.dataset.count));
        syncFanTitle(els, getFan());
      });
    });
  }

  function syncForm(root, config, els, fan, form) {
    syncInputs(els.fields, form);
    Object.entries(config.radios || {}).forEach(([key, name]) => syncRadios(root, name, form[key]));
    if (config.spreadRadios) syncRadios(root, config.spreadRadios, form.spread);
    if (els.reversed) els.reversed.checked = form.reversed !== false;
    if (fan) {
      fan.setTarget(spreadTarget(root, config, fan));
      syncFanTitle(els, fan);
    }
  }

  function formError(config, form, step) {
    return config.validate ? config.validate(form, step) : "";
  }

  function drawForm(config) {
    const prefix = config.prefix || "d";
    let root = null;
    let els = null;
    let fan = null;
    let shown;

    function render(current) {
      window.setButtonLoading(els.submit, current.loading, config.loadingLabel, !picksReady(current.form, fan));
      showError(els.error, current.error);
      if (current.result === shown) return;
      shown = current.result;
      const hasResult = Boolean(current.result);
      if (!config.keepForm) els.form.hidden = hasResult;
      if (els.empty) els.empty.hidden = hasResult;
      if (els.footer) els.footer.hidden = !hasResult;
      els.result.hidden = !hasResult && !els.empty;
      if (hasResult) config.renderResult(current.result, prefix);
      else if (config.clearResult) config.clearResult(prefix);
    }

    function init(layoutRoot) {
      root = layoutRoot;
      els = Object.assign(setupForm(root, prefix, config), {
        form: byId(prefix + "-form"),
        submit: byId(prefix + "-submit"),
        error: byId(prefix + "-error"),
        result: byId(prefix + "-result"),
        empty: byId(prefix + "-empty"),
        footer: byId(prefix + "-footer"),
        reset: byId(prefix + "-reset"),
      });
      if (els.fan) {
        fan = createFan(els, {
          onChange: (picks, target) => {
            if (!state.loading) els.submit.disabled = picks.length !== target;
          },
        });
      }
      bindSpreads(root, config, els, () => fan);
      els.form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const message = formError(config, state.form) || (fan ? picksError(state.form, fan.target()) : "");
        if (message) {
          showError(els.error, message);
          return;
        }
        if (await submit()) showResult(els.result);
      });
      if (els.reset) {
        els.reset.addEventListener("click", () => {
          reset();
          if (fan) fan.shuffle(false);
          window.scrollTo({ top: 0, behavior: window.prefersReducedMotion() ? "auto" : "smooth" });
        });
      }
    }

    function activate(current) {
      syncForm(root, config, els, fan, current.form);
      shown = undefined;
      render(current);
    }

    return { init: init, render: render, activate: activate };
  }

  function drawSteps(config) {
    const prefix = "m";
    let root = null;
    let els = null;
    let fan = null;
    let shown;
    let step = 1;

    function onFanStep() {
      return Boolean(fan) && step === config.fanStep;
    }

    function renderSteps(current) {
      renderStepper(els, step, config.total);
      if (current.loading) {
        window.setButtonLoading(els.next, true, config.loadingLabel);
        return;
      }
      window.setButtonLoading(els.next, false, null, onFanStep() && !picksReady(current.form, fan));
      els.next.textContent = step === config.total ? config.submitLabel : "Lanjut";
    }

    function render(current) {
      const hasResult = Boolean(current.result);
      els.stepsSection.hidden = hasResult;
      els.resultSection.hidden = !hasResult;
      if (hasResult) {
        if (current.result !== shown) {
          shown = current.result;
          config.renderResult(current.result, prefix);
        }
        return;
      }
      shown = null;
      renderSteps(current);
      showError(els.error, current.error);
    }

    function focusStep() {
      const active = els.steps.find((node) => Number(node.dataset.step) === step);
      const target = active && active.querySelector("input:not([type='radio']):not([type='checkbox']), textarea, h2");
      if (target && target.tagName !== "H2") target.focus();
    }

    async function goNext() {
      const message = formError(config, state.form, step) || (onFanStep() ? picksError(state.form, fan.target()) : "");
      if (message) {
        showError(els.error, message);
        return;
      }
      showError(els.error, "");
      if (step < config.total) {
        step += 1;
        if (onFanStep()) {
          fan.setTarget(spreadTarget(root, config, fan));
          syncFanTitle(els, fan);
        }
        renderSteps(state);
        focusStep();
        return;
      }
      const ok = await submit();
      render(state);
      if (ok) showResult(els.resultSection);
    }

    function init(layoutRoot) {
      root = layoutRoot;
      els = Object.assign(setupForm(root, prefix, config), {
        stepsSection: byId(prefix + "-steps"),
        resultSection: byId(prefix + "-result"),
        steps: Array.from(root.querySelectorAll(".tr-m-step")),
        progressText: byId(prefix + "-progress-text"),
        marks: byId(prefix + "-step-marks"),
        error: byId(prefix + "-error"),
        back: byId(prefix + "-back"),
        next: byId(prefix + "-next"),
        reset: byId(prefix + "-reset"),
      });
      if (els.fan) {
        fan = createFan(els, {
          onChange: (picks, target) => {
            if (onFanStep() && !state.loading) els.next.disabled = picks.length !== target;
          },
        });
      }
      bindSpreads(root, config, els, () => fan);
      Object.values(els.fields).forEach((node) => {
        if (node.tagName !== "INPUT") return;
        node.addEventListener("keydown", (event) => {
          if (event.key === "Enter") {
            event.preventDefault();
            goNext();
          }
        });
      });
      els.next.addEventListener("click", goNext);
      els.back.addEventListener("click", () => {
        step = Math.max(1, step - 1);
        showError(els.error, "");
        renderSteps(state);
      });
      els.reset.addEventListener("click", () => {
        step = 1;
        reset();
        if (fan) fan.shuffle(false);
      });
    }

    function activate(current) {
      syncForm(root, config, els, fan, current.form);
      shown = undefined;
      render(current);
    }

    return { init: init, render: render, activate: activate };
  }

  function applyLayout(media) {
    const next = media.matches ? "mobile" : "desktop";
    app.querySelectorAll("[data-layout]").forEach((root) => {
      const on = root.dataset.layout === next;
      root.hidden = !on;
      root.inert = !on;
    });
    const mobileRoot = app.querySelector('[data-layout="mobile"]');
    const bottomNav = mobileRoot && mobileRoot.querySelector("[data-bottom-nav]");
    document.body.classList.toggle("has-bottom-nav", next === "mobile" && Boolean(bottomNav));
    app.dataset.activeLayout = next;
    activeLayout = next;
    if (renderers[next]) renderers[next].activate(state);
  }

  function boot() {
    app = byId("tr-app");
    if (!app) return;
    readDeckOptions();
    setDeck(readStoredDeck(), false);
    bindDeckControls();
    if (app.dataset.page && PAYLOAD_BUILDERS[app.dataset.page]) {
      state = Object.assign({}, state, {
        form: {
          picks: [],
          reversed: true,
          topic: app.dataset.defaultTopic,
          spread: app.dataset.defaultSpread,
        },
      });
    }
    Object.keys(renderers).forEach((name) => {
      const root = app.querySelector('[data-layout="' + name + '"]');
      if (root) renderers[name].init(root);
    });
    listeners.add((next) => {
      if (activeLayout && renderers[activeLayout]) renderers[activeLayout].render(next);
    });
    const media = window.matchMedia(MOBILE_QUERY);
    media.addEventListener("change", () => applyLayout(media));
    applyLayout(media);
  }

  window.Tarot = {
    getState: getState,
    setState: setState,
    updateForm: updateForm,
    registerRenderer: registerRenderer,
    submit: submit,
    reset: reset,
    showResult: showResult,
    el: el,
    clear: clear,
    byId: byId,
    showError: showError,
    createFan: createFan,
    bindToggle: bindToggle,
    bindInputs: bindInputs,
    syncInputs: syncInputs,
    bindRadios: bindRadios,
    syncRadios: syncRadios,
    renderStepper: renderStepper,
    renderSummary: renderSummary,
    renderBoard: renderBoard,
    renderInsights: renderInsights,
    renderCardList: renderCardList,
    renderFooter: renderFooter,
    renderDaily: renderDaily,
    renderStage: renderStage,
    resetStage: resetStage,
    renderYesNo: renderYesNo,
    renderBirth: renderBirth,
    questionError: questionError,
    picksError: picksError,
    drawForm: drawForm,
    drawSteps: drawSteps,
  };

  document.addEventListener("DOMContentLoaded", boot);
})();
