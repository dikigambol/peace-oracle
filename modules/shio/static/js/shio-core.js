(function () {
  const MOBILE_QUERY = "(max-width: 768px)";
  const renderers = {};
  const listeners = new Set();
  const bootHooks = [];
  let state = { form: {}, ui: {}, result: null, loading: false, error: "" };
  let activeLayout = null;
  let app = null;

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

  function updateUi(patch) {
    setState({ ui: Object.assign({}, state.ui, patch) });
  }

  function patchResult(patch) {
    if (!state.result) return;
    setState({ result: Object.assign({}, state.result, patch) });
  }

  function registerRenderer(name, renderer) {
    renderers[name] = renderer;
  }

  function onChange(listener) {
    listeners.add(listener);
  }

  function onBoot(hook) {
    bootHooks.push(hook);
  }

  async function run(task) {
    if (state.loading) return null;
    setState({ loading: true, error: "" });
    try {
      const value = await task();
      setState({ loading: false });
      return value;
    } catch (error) {
      setState({ loading: false, error: error.message });
      window.showErrorToast(error.message);
      return null;
    }
  }

  function postJson(url, body, headers) {
    return window.fetchJson(url, {
      method: "POST",
      headers: Object.assign({ "Content-Type": "application/json" }, headers || {}),
      body: JSON.stringify(body || {}),
    });
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
    while (node && node.firstChild) node.removeChild(node.firstChild);
    return node;
  }

  function part(root, name) {
    return root.querySelector('[data-part="' + name + '"]');
  }

  function parts(root, name) {
    return Array.from(root.querySelectorAll('[data-part="' + name + '"]'));
  }

  function staticUrl(path) {
    return (app ? app.dataset.static : "/shio-static/") + path;
  }

  function page() {
    return app ? app.dataset.page : "";
  }

  function api() {
    return app ? app.dataset.api : "";
  }

  function isoToday() {
    const now = new Date();
    return now.getFullYear() + "-" + String(now.getMonth() + 1).padStart(2, "0") + "-" +
      String(now.getDate()).padStart(2, "0");
  }

  function desktopDate(input, options) {
    const settings = Object.assign({
      dateFormat: "Y-m-d",
      altInput: true,
      altFormat: "j F Y",
      locale: "id",
      minDate: "1900-01-01",
      maxDate: "today",
      disableMobile: true,
    }, options || {});
    window.initDatePicker("#" + input.id, settings);
    return input._flatpickr || null;
  }

  function setDesktopDate(picker, input, value) {
    if (picker) {
      if (value) picker.setDate(value, false);
      else picker.clear(false);
    } else if (input) {
      input.value = value || "";
    }
  }

  function mobileDate(input, onPick) {
    if (!input.max && input.dataset.noMax === undefined) input.max = isoToday();
    if (!input.min) input.min = "1900-01-01";
    const handler = () => onPick(input.value || "");
    input.addEventListener("input", handler);
    input.addEventListener("change", handler);
  }

  function markChoice(root, attribute, value) {
    root.querySelectorAll("[data-" + attribute + "]").forEach((button) => {
      const on = button.dataset[attribute] === value;
      button.classList.toggle("selected", on);
      button.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  function loadingBox(text) {
    const box = el("div", "sh-loading");
    box.setAttribute("role", "status");
    box.appendChild(icon("fa-spinner fa-spin"));
    box.appendChild(document.createTextNode(text));
    return box;
  }

  function scrollIntoView(node) {
    if (!node || !node.scrollIntoView) return;
    node.scrollIntoView({ behavior: window.prefersReducedMotion() ? "auto" : "smooth", block: "start" });
  }

  function replay(node, className) {
    if (!node) return;
    node.classList.remove(className);
    void node.offsetWidth;
    node.classList.add(className);
  }

  async function share(payload) {
    const url = payload.url || window.location.href;
    if (navigator.share) {
      try {
        await navigator.share({ title: payload.title, text: payload.text, url: url });
      } catch (error) {}
      return;
    }
    try {
      await navigator.clipboard.writeText(payload.text + " " + url);
      window.showToast("Teks sudah disalin. Tinggal tempel di chat.", "info");
    } catch (error) {
      window.showErrorToast("Browser ini belum bisa menyalin otomatis.");
    }
  }

  function readJson(id) {
    const node = document.getElementById(id);
    if (!node) return null;
    try {
      return JSON.parse(node.textContent);
    } catch (error) {
      return null;
    }
  }

  function setupMoreSheet(root) {
    const sheet = root.querySelector("[data-sheet]");
    if (!sheet) return;
    const openers = Array.from(root.querySelectorAll("[data-sheet-open]"));
    const close = () => {
      sheet.hidden = true;
      openers.forEach((button) => button.setAttribute("aria-expanded", "false"));
    };
    openers.forEach((button) => {
      button.addEventListener("click", () => {
        const opening = sheet.hidden;
        sheet.hidden = !opening;
        button.setAttribute("aria-expanded", opening ? "true" : "false");
        if (opening) {
          const first = sheet.querySelector("a");
          if (first) first.focus();
        }
      });
    });
    sheet.querySelectorAll("[data-sheet-close]").forEach((node) => node.addEventListener("click", close));
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && !sheet.hidden) close();
    });
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
    app = document.getElementById("sh-app");
    if (!app) return;
    const mobileRoot = app.querySelector('[data-layout="mobile"]');
    if (mobileRoot) setupMoreSheet(mobileRoot);
    bootHooks.forEach((hook) => hook(app));
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

  window.Shio = {
    getState: getState,
    setState: setState,
    updateForm: updateForm,
    updateUi: updateUi,
    patchResult: patchResult,
    registerRenderer: registerRenderer,
    onChange: onChange,
    onBoot: onBoot,
    run: run,
    postJson: postJson,
    el: el,
    icon: icon,
    clear: clear,
    part: part,
    parts: parts,
    staticUrl: staticUrl,
    page: page,
    api: api,
    isoToday: isoToday,
    desktopDate: desktopDate,
    setDesktopDate: setDesktopDate,
    mobileDate: mobileDate,
    scrollIntoView: scrollIntoView,
    loadingBox: loadingBox,
    markChoice: markChoice,
    replay: replay,
    share: share,
    readJson: readJson,
    activeLayout: () => activeLayout,
  };

  document.addEventListener("DOMContentLoaded", boot);
})();

(function (Shio) {
  const BOARD_TAPS_NEEDED = 5;
  const BOARD_AUTO_CLOSE_MS = 5000;
  const BOARD_EXIT_MS = 480;
  const MEDALS = ["🥇", "🥈", "🥉"];
  let requestId = 0;
  let boardTaps = 0;
  let boardUnlocked = false;
  let closeTimer = null;
  let exitTimer = null;
  let overlay = null;

  async function load(date) {
    const target = date || Shio.isoToday();
    const id = ++requestId;
    Shio.updateForm({ date: target });
    Shio.setState({ loading: true, error: "" });
    try {
      const data = await window.fetchJson(Shio.api() + "?date=" + encodeURIComponent(target));
      if (id !== requestId) return;
      closeBoard();
      Shio.setState({ loading: false, result: data });
    } catch (error) {
      if (id !== requestId) return;
      Shio.setState({ loading: false, error: "Gagal memuat ramalan harian." });
    }
  }

  function pillarBox(label, hanzi, value, extraClass) {
    const box = Shio.el("div", "pillar-box" + (extraClass ? " " + extraClass : ""));
    box.appendChild(Shio.el("span", "pillar-label", label));
    box.appendChild(Shio.el("span", "pillar-hanzi", hanzi));
    box.appendChild(Shio.el("span", "pillar-value", value));
    return box;
  }

  function yijiColumn(className, iconName, title, items) {
    const col = Shio.el("div", "yiji-col " + className);
    const head = Shio.el("h4");
    head.appendChild(Shio.icon(iconName));
    head.appendChild(document.createTextNode(" " + title));
    col.appendChild(head);
    const list = Shio.el("ul");
    (items || []).forEach((item) => list.appendChild(Shio.el("li", null, item)));
    col.appendChild(list);
    return col;
  }

  function buildPillar(data) {
    const fragment = document.createDocumentFragment();
    const row = Shio.el("div", "pillar-row");
    row.appendChild(pillarBox("Pilar Hari", data.day_pillar_hanzi, data.day_pillar));
    row.appendChild(pillarBox("Elemen Hari", data.day_element_hanzi, data.day_element));
    row.appendChild(pillarBox("Dewa Harian", data.officer_hanzi, data.officer_name, "officer-" + data.officer_code));
    row.appendChild(pillarBox("Bulan Imlek", data.month_branch_hanzi, data.month_branch));
    fragment.appendChild(row);
    fragment.appendChild(Shio.el("p", "pillar-meaning", data.officer_meaning));
    const yiji = Shio.el("div", "yiji-row");
    yiji.appendChild(yijiColumn("yiji-yi", "fa-circle-check", "Cocok Untuk", data.officer_yi));
    yiji.appendChild(yijiColumn("yiji-ji", "fa-circle-xmark", "Sebaiknya Hindari", data.officer_ji));
    fragment.appendChild(yiji);
    return fragment;
  }

  function buildDailyCard(item, index) {
    const card = Shio.el("div", "daily-card status-" + item.status_code + " animate-in");
    card.style.animationDelay = 0.12 + index * 0.05 + "s";
    const header = Shio.el("div", "daily-card-header");
    header.appendChild(Shio.el("span", "daily-card-icon icon-hanzi", item.hanzi));
    header.appendChild(Shio.el("h3", "daily-card-name", item.name));
    card.appendChild(header);
    card.appendChild(Shio.el("div", "daily-card-status", item.status));
    const element = Shio.el("div", "daily-card-element element-" + item.element_relation_code);
    element.title = item.element_desc || "";
    element.appendChild(Shio.el("span", "element-badge", item.element_hanzi + " " + item.element));
    element.appendChild(Shio.el("span", "element-arrow", item.element_symbol));
    element.appendChild(Shio.el("span", "element-rel", item.element_relation));
    card.appendChild(element);
    card.appendChild(Shio.el("p", "daily-card-message", item.message));
    if (item.daily_tip) {
      const tip = Shio.el("div", "daily-card-tip");
      tip.appendChild(Shio.icon("fa-lightbulb"));
      tip.appendChild(Shio.el("span", null, " " + item.daily_tip));
      card.appendChild(tip);
    }
    return card;
  }

  function renderDaily(list, pillar, data) {
    Shio.clear(list);
    (data.fortunes || []).forEach((item, index) => list.appendChild(buildDailyCard(item, index)));
    Shio.clear(pillar);
    pillar.appendChild(buildPillar(data));
    pillar.hidden = false;
    Shio.replay(pillar, "animate-in");
  }

  function renderLoading(list, message) {
    Shio.clear(list);
    const box = Shio.el("div", "sh-loading");
    box.appendChild(Shio.icon("fa-compass fa-spin-pulse"));
    box.appendChild(Shio.el("p", null, message));
    list.appendChild(box);
  }

  function renderError(list, message) {
    Shio.clear(list);
    list.appendChild(Shio.el("p", "daily-error", message));
  }

  function renderLeaderboard(box, board, note) {
    Shio.clear(box);
    box.appendChild(Shio.el("h3", "board-title", "Papan Peringkat Shio Hari Ini"));
    const podium = Shio.el("div", "board-podium");
    board.slice(0, 3).forEach((item) => {
      const card = Shio.el("div", "podium-card place-" + item.rank);
      card.appendChild(Shio.el("span", "podium-medal", MEDALS[item.rank - 1]));
      card.appendChild(Shio.el("span", "podium-hanzi", item.hanzi));
      card.appendChild(Shio.el("span", "podium-name", item.name));
      card.appendChild(Shio.el("span", "podium-status", item.status));
      podium.appendChild(card);
    });
    box.appendChild(podium);
    const list = Shio.el("ol", "board-list");
    board.slice(3).forEach((item, index) => {
      const row = Shio.el("li", "board-row tier-" + item.tier);
      row.style.setProperty("--row-index", index);
      row.title = item.status;
      row.appendChild(Shio.el("span", "board-rank", String(item.rank)));
      row.appendChild(Shio.el("span", "board-hanzi", item.hanzi));
      const info = Shio.el("span", "board-info");
      info.appendChild(Shio.el("span", "board-name", item.name));
      info.appendChild(Shio.el("span", "board-status", item.status));
      row.appendChild(info);
      list.appendChild(row);
    });
    box.appendChild(list);
    if (note) box.appendChild(Shio.el("p", "board-note", note));
  }

  function hideBoardNow() {
    overlay.hidden = true;
    overlay.classList.remove("board-open", "board-closing");
    document.body.classList.remove("board-locked");
  }

  function closeBoard() {
    if (!overlay || overlay.hidden || overlay.classList.contains("board-closing")) return;
    if (closeTimer) {
      clearTimeout(closeTimer);
      closeTimer = null;
    }
    overlay.classList.remove("board-open");
    overlay.classList.add("board-closing");
    exitTimer = setTimeout(() => {
      exitTimer = null;
      hideBoardNow();
    }, BOARD_EXIT_MS);
  }

  function openBoard() {
    const data = Shio.getState().result;
    if (!overlay || !data || !data.leaderboard || !data.leaderboard.length) return;
    if (exitTimer) {
      clearTimeout(exitTimer);
      exitTimer = null;
    }
    overlay.classList.remove("board-closing");
    renderLeaderboard(document.getElementById("sh-board"), data.leaderboard, data.leaderboard_note);
    const bar = document.getElementById("sh-board-countdown");
    bar.style.animationDuration = BOARD_AUTO_CLOSE_MS + "ms";
    Shio.replay(bar, "counting");
    overlay.hidden = false;
    void overlay.offsetWidth;
    overlay.classList.add("board-open");
    document.body.classList.add("board-locked");
    if (closeTimer) clearTimeout(closeTimer);
    closeTimer = setTimeout(closeBoard, BOARD_AUTO_CLOSE_MS);
  }

  function tap(trigger) {
    Shio.replay(trigger, "tap-pulse");
    if (boardUnlocked) {
      openBoard();
      return;
    }
    boardTaps += 1;
    if (boardTaps >= BOARD_TAPS_NEEDED) {
      boardUnlocked = true;
      openBoard();
    }
  }

  Shio.onBoot((app) => {
    overlay = document.getElementById("sh-board-overlay");
    if (!overlay) return;
    app.querySelectorAll("[data-board-trigger]").forEach((trigger) => {
      trigger.addEventListener("click", () => tap(trigger));
    });
    document.getElementById("sh-board-close").addEventListener("click", closeBoard);
    overlay.addEventListener("click", (event) => {
      if (event.target === overlay) closeBoard();
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeBoard();
    });
  });

  Shio.almanac = {
    load: load,
    renderDaily: renderDaily,
    renderLoading: renderLoading,
    renderError: renderError,
    closeBoard: closeBoard,
  };
})(window.Shio);

(function (Shio) {
  function byId(id) {
    return document.getElementById(id);
  }

  function openAlmanac(scrollTop) {
    Shio.updateUi({ view: "almanac" });
    if (scrollTop) window.scrollTo(0, 0);
    const state = Shio.getState();
    if (!state.result && !state.loading) Shio.almanac.load(state.form.date || Shio.isoToday());
  }

  function bindViews(root, scrollTop) {
    root.querySelectorAll('[data-action="almanac"]').forEach((button) => {
      button.addEventListener("click", () => openAlmanac(scrollTop));
    });
    root.querySelectorAll('[data-action="menu"]').forEach((button) => {
      button.addEventListener("click", () => Shio.updateUi({ view: "menu" }));
    });
  }

  function makeRenderer(layout) {
    let els = null;
    let picker = null;
    let renderedResult = null;

    function renderAlmanac(state) {
      if (els.native) els.date.value = state.form.date || Shio.isoToday();
      if (state.loading) {
        Shio.almanac.renderLoading(els.list, "Menyelaraskan garis waktu...");
        renderedResult = null;
        return;
      }
      if (state.error && !state.result) {
        Shio.almanac.renderError(els.list, state.error);
        return;
      }
      if (!state.result || state.result === renderedResult) return;
      const data = state.result;
      els.name.textContent = data.today_shio_name;
      els.icon.textContent = data.today_shio_hanzi;
      Shio.almanac.renderDaily(els.list, els.pillar, data);
      renderedResult = data;
    }

    function render(state) {
      const almanac = state.ui.view === "almanac";
      els.menu.hidden = almanac;
      els.almanac.hidden = !almanac;
      if (els.back) els.back.hidden = !almanac;
      if (els.title) els.title.textContent = almanac ? "Almanak Harian" : "Shio Oracle";
      if (almanac) renderAlmanac(state);
    }

    function initDesktop(root) {
      picker = Shio.desktopDate(els.date, {
        minDate: null,
        maxDate: null,
        defaultDate: Shio.isoToday(),
        onChange: (dates, value) => {
          if (value && value !== Shio.getState().form.date) Shio.almanac.load(value);
        },
      });
      bindViews(root, false);
      els.today.addEventListener("click", () => {
        const today = Shio.isoToday();
        Shio.setDesktopDate(picker, els.date, today);
        Shio.almanac.load(today);
      });
    }

    function initMobile(root) {
      Shio.mobileDate(els.date, (value) => {
        if (value && value !== Shio.getState().form.date) Shio.almanac.load(value);
      });
      bindViews(root, true);
      els.today.addEventListener("click", () => Shio.almanac.load(Shio.isoToday()));
    }

    function init(root) {
      const prefix = layout === "desktop" ? "d-" : "m-";
      els = {
        native: layout === "mobile",
        menu: root.querySelector('[data-view="menu"]'),
        almanac: root.querySelector('[data-view="almanac"]'),
        back: layout === "mobile" ? byId("m-almanac-back") : null,
        title: layout === "mobile" ? byId("m-hub-title") : null,
        name: byId(prefix + "daily-name"),
        icon: Shio.part(byId(prefix + "daily-icon"), "icon"),
        date: byId(prefix + "daily-date"),
        today: byId(prefix + "daily-today"),
        pillar: byId(prefix + "daily-pillar"),
        list: byId(layout === "desktop" ? "d-daily-grid" : "m-daily-list"),
      };
      if (layout === "desktop") initDesktop(root);
      else initMobile(root);
    }

    function activate(state) {
      if (picker) Shio.setDesktopDate(picker, els.date, state.form.date || Shio.isoToday());
      renderedResult = null;
      render(state);
    }

    return { init: init, render: render, activate: activate };
  }

  Shio.onBoot((app) => {
    if (app.dataset.page !== "shio") return;
    Shio.registerRenderer("desktop", makeRenderer("desktop"));
    Shio.registerRenderer("mobile", makeRenderer("mobile"));
  });
})(window.Shio);

(function (Shio) {
  const SHIO_LIST = [
    ["tikus", "鼠", "Tikus"], ["kerbau", "牛", "Kerbau"], ["macan", "虎", "Macan"], ["kelinci", "兔", "Kelinci"],
    ["naga", "龍", "Naga"], ["ular", "蛇", "Ular"], ["kuda", "馬", "Kuda"], ["kambing", "羊", "Kambing"],
    ["monyet", "猴", "Monyet"], ["ayam", "雞", "Ayam"], ["anjing", "狗", "Anjing"], ["babi", "豬", "Babi"],
  ].map((row) => ({ key: row[0], hanzi: row[1], name: row[2] }));
  const BY_KEY = {};
  SHIO_LIST.forEach((item) => {
    BY_KEY[item.key] = item;
  });

  function markPicked(root, key) {
    root.querySelectorAll("[data-shio]").forEach((button) => {
      const on = button.dataset.shio === key;
      button.classList.toggle("selected", on);
      button.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  Shio.shio = { list: SHIO_LIST, byKey: BY_KEY, markPicked: markPicked };
})(window.Shio);

(function (Shio) {
  const CATEGORIES = [
    ["karir", "Karir", "fa-briefcase"],
    ["keuangan", "Keuangan", "fa-coins"],
    ["asmara", "Asmara", "fa-heart"],
    ["kesehatan", "Kesehatan", "fa-heart-pulse"],
  ];

  function yearShio(year) {
    return Shio.shio.list[((year - 4) % 12 + 12) % 12];
  }

  function describeYear(year) {
    const item = yearShio(year);
    return "Tahun " + item.name + " " + item.hanzi;
  }

  async function submit() {
    const form = Shio.getState().form;
    if (!form.shio) return null;
    const data = await Shio.run(() => Shio.postJson(Shio.api(), { shio: form.shio, year: form.year }));
    if (!data) return null;
    if (data.error && !data.user_shio) {
      window.showErrorToast(data.error);
      return null;
    }
    Shio.setState({ result: data });
    return data;
  }

  function shioBox(hanzi, name, extra, extraClass) {
    const box = Shio.el("div", "yearly-shio-box" + (extraClass ? " " + extraClass : ""));
    box.appendChild(Shio.el("span", "yearly-hanzi", hanzi));
    box.appendChild(Shio.el("span", "yearly-shio-name", name));
    if (extra) box.appendChild(Shio.el("span", "yearly-year-num", extra));
    return box;
  }

  function buildSummary(data) {
    const wrap = Shio.el("div", "yearly-card");
    const user = data.user_shio || {};
    const year = data.year_shio || {};
    const header = Shio.el("div", "yearly-header");
    const pair = Shio.el("div", "yearly-pair");
    pair.appendChild(shioBox(user.hanzi || "", user.name || ""));
    pair.appendChild(Shio.el("div", "yearly-arrow", "di"));
    pair.appendChild(shioBox(year.hanzi || "", "Tahun " + (year.name || ""), String(data.year || ""), "year-box"));
    header.appendChild(pair);
    wrap.appendChild(header);

    const relation = data.relation || {};
    const rel = Shio.el("div", "yearly-relation");
    const label = relation.name_id || relation.label || "";
    rel.appendChild(Shio.el("span", "yearly-badge code-" + (relation.code || "neutral"),
      relation.hanzi ? relation.hanzi + " · " + label : label));
    if (relation.tai_sui) rel.appendChild(Shio.el("span", "yearly-taisui", relation.tai_sui));
    rel.appendChild(Shio.el("p", "yearly-relation-note", relation.note || ""));
    wrap.appendChild(rel);

    const stem = data.stem_layer || {};
    const stemBox = Shio.el("div", "yearly-stem role-" + (stem.role || "setara"));
    const title = Shio.el("h4", "yearly-stem-title");
    title.appendChild(Shio.icon("fa-palette"));
    title.appendChild(document.createTextNode(" Warna Energi Tahun Ini "));
    title.appendChild(Shio.el("span", "yearly-stem-pillar", stem.year_pillar || ""));
    stemBox.appendChild(title);
    stemBox.appendChild(Shio.el("p", "yearly-stem-summary", stem.summary || ""));
    stemBox.appendChild(Shio.el("p", "yearly-stem-advice", stem.advice || ""));
    wrap.appendChild(stemBox);

    if (data.saran_utama) {
      const advice = Shio.el("div", "yearly-advice");
      const iconBox = Shio.el("div", "advice-icon");
      iconBox.appendChild(Shio.icon("fa-scroll"));
      advice.appendChild(iconBox);
      advice.appendChild(Shio.el("p", null, data.saran_utama));
      wrap.appendChild(advice);
    }
    return wrap;
  }

  function categories(data) {
    return CATEGORIES.map((row) => ({ key: row[0], label: row[1], icon: row[2], text: data[row[0]] || "-" }));
  }

  function buildCategory(item) {
    const card = Shio.el("div", "yearly-cat");
    const iconBox = Shio.el("div", "cat-icon");
    iconBox.appendChild(Shio.icon(item.icon));
    card.appendChild(iconBox);
    card.appendChild(Shio.el("h3", null, item.label));
    card.appendChild(Shio.el("p", null, item.text));
    return card;
  }

  function buildCategories(data) {
    const grid = Shio.el("div", "yearly-categories");
    categories(data).forEach((item) => grid.appendChild(buildCategory(item)));
    return grid;
  }

  Shio.onBoot((app) => {
    if (app.dataset.page !== "liunian") return;
    const seeded = parseInt(app.dataset.currentYear, 10);
    Shio.updateForm({ year: Number.isFinite(seeded) ? seeded : new Date().getFullYear() });
  });

  Shio.yearly = {
    yearShio: yearShio,
    describeYear: describeYear,
    submit: submit,
    buildSummary: buildSummary,
    categories: categories,
    buildCategory: buildCategory,
    buildCategories: buildCategories,
  };
})(window.Shio);

(function (Shio) {
  async function submit(key) {
    if (!key || Shio.getState().loading) return null;
    Shio.updateForm({ shio: key });
    Shio.setState({ result: null });
    const data = await Shio.run(() => Shio.postJson(Shio.api(), { shio: key }));
    if (!data) return null;
    if (!data.guardian_name) {
      window.showErrorToast(data.error || "Data penjaga tidak ditemukan.");
      return null;
    }
    Shio.setState({ result: data });
    return data;
  }

  function highlight(iconName, label, value) {
    const row = Shio.el("p", "highlight-item");
    const strong = Shio.el("strong");
    strong.appendChild(Shio.icon(iconName));
    strong.appendChild(document.createTextNode(" " + label + ":"));
    row.appendChild(strong);
    row.appendChild(document.createTextNode(" "));
    row.appendChild(Shio.el("span", null, value || "-"));
    return row;
  }

  function buildHero(data) {
    const hero = Shio.el("div", "guardian-hero");
    const frame = Shio.el("div", "guardian-image-container");
    const image = Shio.el("img", "guardian-icon-img");
    image.src = Shio.staticUrl(data.guardian_icon || "");
    image.alt = data.guardian_name || "";
    image.width = 150;
    image.height = 150;
    frame.appendChild(image);
    hero.appendChild(frame);
    hero.appendChild(Shio.el("h2", "res-title", data.guardian_name || ""));
    hero.appendChild(Shio.el("p", "res-fortune", data.guardian_desc || ""));
    if (data.tradition) hero.appendChild(Shio.el("p", "guardian-tradition", data.tradition));
    return hero;
  }

  function buildHighlights(data) {
    const box = Shio.el("div", "fortune-highlights");
    box.appendChild(highlight("fa-om", "Mantra", data.mantra));
    box.appendChild(highlight("fa-book-open", "Makna Mantra", data.mantra_meaning));
    box.appendChild(highlight("fa-leaf", "Elemen Shio",
      [data.shio_element, data.shio_element_hanzi].filter(Boolean).join(" ")));
    return box;
  }

  function buildFengShui(data) {
    const wrap = document.createDocumentFragment();
    if (data.feng_shui_note) wrap.appendChild(Shio.el("p", "guardian-side-note", data.feng_shui_note));
    const list = Shio.el("ul", "guardian-feng-shui-list");
    (Array.isArray(data.feng_shui_tips) ? data.feng_shui_tips : []).forEach((tip) => {
      list.appendChild(Shio.el("li", null, tip));
    });
    wrap.appendChild(list);
    return wrap;
  }

  function metaBox(iconName, label, value, note) {
    const box = Shio.el("div", "meta-box");
    box.appendChild(Shio.icon(iconName));
    box.appendChild(document.createTextNode(" " + label + ": "));
    box.appendChild(Shio.el("span", null, value || "-"));
    if (note) box.appendChild(Shio.el("small", "guardian-meta-note", note));
    return box;
  }

  function buildMeta(data) {
    const meta = Shio.el("div", "res-meta");
    meta.appendChild(metaBox("fa-clock", "Selaras dengan jam shio-mu", data.best_pray_time, data.pray_time_note));
    meta.appendChild(metaBox("fa-compass", "Arah Sakral", data.sacred_direction, data.direction_note));
    return meta;
  }

  function sections(data) {
    return [
      { key: "protection", title: "Nasihat Perlindungan", icon: "fa-shield-halved", full: true,
        build: () => Shio.el("p", null, data.protection_advice || "-") },
      { key: "offering", title: "Saran Persembahan", icon: "fa-gift",
        build: () => Shio.el("p", null, data.offering_suggestion || "-") },
      { key: "fengshui", title: "Tips Feng Shui", icon: "fa-yin-yang", build: () => buildFengShui(data) },
    ];
  }

  function buildCategories(data) {
    const grid = Shio.el("div", "fortune-categories");
    sections(data).forEach((section) => {
      const box = Shio.el("div", "category-box" + (section.full ? " guardian-category-full" : ""));
      const title = Shio.el("h3");
      title.appendChild(Shio.icon(section.icon));
      title.appendChild(document.createTextNode(" " + section.title));
      box.appendChild(title);
      box.appendChild(section.build());
      grid.appendChild(box);
    });
    return grid;
  }

  Shio.guardian = {
    submit: submit,
    buildHero: buildHero,
    buildHighlights: buildHighlights,
    buildMeta: buildMeta,
    sections: sections,
    buildCategories: buildCategories,
  };
})(window.Shio);

(function (Shio) {
  const CRUMB_TONES = ["#e8c47a", "#d9a441", "#c2883a", "#a86f28", "#8d5a20"];
  const EMBER_RAMP = [
    [1.0, "255, 248, 214"],
    [0.82, "255, 226, 130"],
    [0.6, "255, 164, 46"],
    [0.34, "232, 88, 18"],
    [0.0, "148, 28, 8"],
  ];

  let sparkTones = null;

  function readSparkTones() {
    const styles = getComputedStyle(document.documentElement);
    return [
      styles.getPropertyValue("--gold").trim() || "#ffd700",
      styles.getPropertyValue("--flame").trim() || "#ff4500",
    ];
  }

  const KINDS = {
    sparks: {
      burst: 30,
      trail: 5,
      composite: "source-over",
      spawn(x, y) {
        if (!sparkTones) sparkTones = readSparkTones();
        return {
          x: x,
          y: y,
          size: Math.random() * 5 + 2,
          speedX: Math.random() * 6 - 3,
          speedY: Math.random() * 6 - 3,
          color: sparkTones[Math.random() > 0.5 ? 0 : 1],
          life: 1.0,
          decay: Math.random() * 0.02 + 0.02,
        };
      },
      step(p) {
        p.x += p.speedX;
        p.y += p.speedY;
        p.life -= p.decay;
      },
      draw(ctx, p) {
        ctx.globalAlpha = Math.max(p.life, 0);
        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
      },
      dead(p) {
        return p.life <= 0;
      },
    },
    crumbs: {
      burst: 18,
      trail: 3,
      composite: "source-over",
      spawn(x, y) {
        const sides = 5 + Math.floor(Math.random() * 3);
        const notches = [];
        for (let i = 0; i < sides; i++) notches.push(0.55 + Math.random() * 0.7);
        return {
          x: x,
          y: y,
          size: Math.random() * 3.5 + 1.8,
          speedX: Math.random() * 7 - 3.5,
          speedY: -(Math.random() * 4.5 + 1),
          color: CRUMB_TONES[Math.floor(Math.random() * CRUMB_TONES.length)],
          life: 1.0,
          decay: Math.random() * 0.012 + 0.008,
          rot: Math.random() * Math.PI * 2,
          spin: (Math.random() - 0.5) * 0.22,
          sides: sides,
          notches: notches,
        };
      },
      step(p) {
        p.x += p.speedX;
        p.y += p.speedY;
        p.speedY += 0.2;
        p.speedX *= 0.985;
        p.rot += p.spin;
        p.spin *= 0.995;
        p.life -= p.decay;
      },
      draw(ctx, p) {
        ctx.save();
        ctx.globalAlpha = Math.max(p.life, 0);
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rot);
        ctx.fillStyle = p.color;
        ctx.beginPath();
        for (let i = 0; i < p.sides; i++) {
          const angle = (i / p.sides) * Math.PI * 2;
          const radius = p.size * p.notches[i];
          const px = Math.cos(angle) * radius;
          const py = Math.sin(angle) * radius * 0.78;
          if (i === 0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        }
        ctx.closePath();
        ctx.fill();
        ctx.restore();
      },
      dead(p, height) {
        return p.life <= 0 || p.y > height + 50;
      },
    },
    embers: {
      burst: 25,
      trail: 4,
      composite: "lighter",
      spawn(x, y) {
        return {
          x: x,
          y: y,
          size: Math.random() * 3.5 + 2,
          speedX: Math.random() * 1.6 - 0.8,
          speedY: -(Math.random() * 2.4 + 1.1),
          life: 1.0,
          decay: Math.random() * 0.014 + 0.011,
          wobble: Math.random() * Math.PI * 2,
          wobbleRate: Math.random() * 0.12 + 0.08,
          flicker: Math.random() * 0.35 + 0.65,
        };
      },
      step(p) {
        p.wobble += p.wobbleRate;
        p.x += p.speedX + Math.sin(p.wobble) * 0.55;
        p.y += p.speedY;
        p.speedY += 0.016;
        p.speedX *= 0.985;
        p.life -= p.decay;
        p.flicker = 0.65 + Math.abs(Math.sin(p.wobble * 1.7)) * 0.35;
      },
      draw(ctx, p) {
        const life = Math.max(p.life, 0);
        let rgb = EMBER_RAMP[EMBER_RAMP.length - 1][1];
        for (let i = 0; i < EMBER_RAMP.length; i++) {
          if (life >= EMBER_RAMP[i][0]) {
            rgb = EMBER_RAMP[i][1];
            break;
          }
        }
        const core = p.size * (0.35 + life * 0.65) * p.flicker;
        [[3.2, 0.22], [1.8, 0.45], [1, 1]].forEach((ring) => {
          ctx.fillStyle = "rgba(" + rgb + ", " + life * ring[1] + ")";
          ctx.beginPath();
          ctx.arc(p.x, p.y, core * ring[0], 0, Math.PI * 2);
          ctx.fill();
        });
      },
      dead(p) {
        return p.life <= 0;
      },
    },
  };

  let emitter = () => {};

  function start(kind) {
    const canvas = document.getElementById("particle-canvas");
    const surface = document.getElementById("shio-bg");
    if (!canvas || !canvas.getContext) return;
    const ctx = canvas.getContext("2d");
    const particles = [];
    let running = false;
    let dragging = false;

    function resize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }

    function frame() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.globalCompositeOperation = kind.composite;
      let alive = 0;
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        kind.step(p);
        if (kind.dead(p, canvas.height)) continue;
        kind.draw(ctx, p);
        particles[alive++] = p;
      }
      particles.length = alive;
      ctx.globalCompositeOperation = "source-over";
      ctx.globalAlpha = 1;
      if (alive) requestAnimationFrame(frame);
      else running = false;
    }

    emitter = (x, y, count) => {
      if (window.prefersReducedMotion()) return;
      for (let i = 0; i < count; i++) particles.push(kind.spawn(x, y));
      if (!running) {
        running = true;
        requestAnimationFrame(frame);
      }
    };

    window.addEventListener("resize", resize);
    resize();
    if (!surface) return;
    surface.addEventListener("mousedown", (e) => {
      dragging = true;
      emitter(e.clientX, e.clientY, kind.burst);
    });
    surface.addEventListener("mousemove", (e) => {
      if (dragging) emitter(e.clientX, e.clientY, kind.trail);
    });
    window.addEventListener("mouseup", () => {
      dragging = false;
    });
    surface.addEventListener("touchstart", (e) => {
      dragging = true;
      emitter(e.touches[0].clientX, e.touches[0].clientY, kind.burst);
    }, { passive: true });
    surface.addEventListener("touchmove", (e) => {
      if (dragging) emitter(e.touches[0].clientX, e.touches[0].clientY, kind.trail);
    }, { passive: true });
    window.addEventListener("touchend", () => {
      dragging = false;
    });
  }

  function emitFrom(node, count) {
    if (!node) return;
    const rect = node.getBoundingClientRect();
    emitter(rect.left + rect.width / 2, rect.top + rect.height / 2, count);
  }

  Shio.onBoot((app) => {
    const kind = KINDS[app.dataset.particles || "sparks"];
    if (kind) start(kind);
  });

  Shio.particles = { emit: (x, y, count) => emitter(x, y, count), emitFrom: emitFrom };
})(window.Shio);

(function (Shio) {
  const SHAKE_MS = 450;
  const SLIP_MS = 950;
  const TONE_NOTE = {
    good: "Pesanmu hari ini diambil dari kumpulan untuk hari yang mendukung.",
    bad: "Pesanmu hari ini diambil dari kumpulan untuk hari yang menekan.",
    neutral: "Pesanmu hari ini diambil dari kumpulan untuk hari yang netral.",
  };
  const renderedSlips = new WeakMap();
  let crackToken = 0;
  let crackingNode = null;

  async function pick(key) {
    if (!key || Shio.getState().loading) return null;
    crackToken += 1;
    crackingNode = null;
    Shio.updateForm({ shio: key });
    Shio.setState({ result: null, ui: Object.assign({}, Shio.getState().ui, { view: "cookie", cracked: false }) });
    const data = await Shio.run(() => Shio.postJson(Shio.api(), { shio: key }));
    if (!data || data.error) {
      if (data && data.error) window.showErrorToast(data.error);
      Shio.updateUi({ view: "pick" });
      return null;
    }
    Shio.setState({ result: data });
    return data;
  }

  function back() {
    crackToken += 1;
    crackingNode = null;
    Shio.setState({ result: null, ui: Object.assign({}, Shio.getState().ui, { view: "pick", cracked: false }) });
  }

  function shake(cookie) {
    Shio.replay(cookie, "shaking");
    setTimeout(() => cookie.classList.remove("shaking"), SHAKE_MS);
  }

  function crack(cookie, hint) {
    const state = Shio.getState();
    if (state.ui.cracked || crackingNode) return;
    if (!state.result) {
      shake(cookie);
      return;
    }
    const token = crackToken;
    crackingNode = cookie;
    cookie.classList.add("shaking");
    setTimeout(() => {
      if (token !== crackToken) return;
      cookie.classList.remove("shaking");
      cookie.classList.add("cracked");
      if (hint) hint.classList.add("faded");
      Shio.particles.emitFrom(cookie, 45);
    }, SHAKE_MS);
    setTimeout(() => {
      if (token !== crackToken) return;
      crackingNode = null;
      Shio.updateUi({ cracked: true });
    }, SLIP_MS);
  }

  function hokiRow(label, value) {
    const row = Shio.el("li");
    row.appendChild(Shio.el("strong", null, label));
    row.appendChild(Shio.el("span", null, value || "-"));
    return row;
  }

  function buildEnergy(energy, tone) {
    const box = Shio.el("div", "slip-energy");
    const head = Shio.el("p", "slip-energy-head");
    head.appendChild(Shio.el("span", "slip-energy-pillar", energy.pillar_hanzi || ""));
    const branch = energy.branch || {};
    head.appendChild(Shio.el("span", "slip-energy-badge code-" + (branch.code || "neutral"), branch.label || ""));
    const element = energy.element || {};
    head.appendChild(Shio.el("span", "slip-energy-badge code-" + (element.code || "neutral"),
      [element.symbol, element.name].filter(Boolean).join(" ")));
    box.appendChild(head);
    if (element.desc) box.appendChild(Shio.el("p", "slip-energy-desc", element.desc));
    if (TONE_NOTE[tone]) box.appendChild(Shio.el("p", "slip-energy-pick", TONE_NOTE[tone]));
    const lucky = energy.lucky;
    if (lucky) {
      const hoki = Shio.el("div", "slip-hoki");
      const label = Shio.el("span", "slip-lucky-label");
      label.appendChild(Shio.icon("fa-compass"));
      label.appendChild(document.createTextNode(" Hoki Hari Ini"));
      hoki.appendChild(label);
      hoki.appendChild(Shio.el("p", "slip-hoki-reason", lucky.reason || ""));
      const list = Shio.el("ul", "slip-hoki-list");
      list.appendChild(hokiRow("Elemen", lucky.element));
      list.appendChild(hokiRow("Warna", (lucky.colors || []).join(", ")));
      list.appendChild(hokiRow("Arah", (lucky.directions || []).join(", ")));
      list.appendChild(hokiRow("Angka", (lucky.numbers || []).join(", ")));
      hoki.appendChild(list);
      box.appendChild(hoki);
    }
    return box;
  }

  function buildSlip(data) {
    const slip = Shio.el("div", "cookie-slip");
    slip.appendChild(Shio.el("div", "slip-tear"));
    const body = Shio.el("div", "slip-body");
    const seal = Shio.el("div", "slip-seal");
    seal.appendChild(Shio.icon("fa-cookie-bite"));
    body.appendChild(seal);
    body.appendChild(Shio.el("p", "slip-message", data.message || ""));
    const lucky = Shio.el("div", "slip-lucky");
    const label = Shio.el("span", "slip-lucky-label");
    label.appendChild(Shio.icon("fa-clover"));
    label.appendChild(document.createTextNode(" Jimat Absurd Hari Ini"));
    lucky.appendChild(label);
    lucky.appendChild(Shio.el("p", "slip-lucky-text", data.lucky_item || "-"));
    body.appendChild(lucky);
    if (data.day_energy) body.appendChild(buildEnergy(data.day_energy, data.tone));
    const note = Shio.el("p", "slip-note");
    const clock = Shio.el("i", "fa-regular fa-clock");
    clock.setAttribute("aria-hidden", "true");
    note.appendChild(clock);
    note.appendChild(document.createTextNode(" Kue ini berlaku untuk hari ini. Balik lagi besok buat pesan baru."));
    body.appendChild(note);
    slip.appendChild(body);
    return slip;
  }

  function renderStage(nodes, state, instant) {
    const item = Shio.shio.byKey[state.form.shio];
    nodes.hanzi.textContent = item ? item.hanzi : "";
    nodes.name.textContent = item ? item.name : "";
    const cracked = Boolean(state.ui.cracked && state.result);
    const busy = crackingNode === nodes.cookie;
    nodes.cookie.classList.toggle("sh-instant", Boolean(instant && cracked));
    if (cracked) nodes.cookie.classList.add("cracked");
    else if (!busy) nodes.cookie.classList.remove("cracked", "shaking");
    nodes.cookie.disabled = cracked;
    nodes.hint.classList.toggle("faded", cracked || (busy && nodes.cookie.classList.contains("cracked")));
    nodes.hint.textContent = "";
    nodes.hint.appendChild(Shio.icon(state.loading ? "fa-spinner fa-spin" : "fa-hand-pointer"));
    nodes.hint.appendChild(document.createTextNode(state.loading ? " Kue sedang dipanggang..." : " Ketuk kuenya untuk membelah"));
    if (!cracked) {
      Shio.clear(nodes.slipBox);
      nodes.slipBox.hidden = true;
      renderedSlips.delete(nodes.slipBox);
      return;
    }
    nodes.slipBox.hidden = false;
    if (!instant && renderedSlips.get(nodes.slipBox) === state.result) return;
    Shio.clear(nodes.slipBox);
    const slip = buildSlip(state.result);
    if (instant) slip.classList.add("sh-instant");
    nodes.slipBox.appendChild(slip);
    renderedSlips.set(nodes.slipBox, state.result);
    if (!instant) {
      setTimeout(() => slip.scrollIntoView({ behavior: window.prefersReducedMotion() ? "auto" : "smooth", block: "center" }), 150);
    }
  }

  Shio.cookie = { pick: pick, back: back, crack: crack, renderStage: renderStage, buildSlip: buildSlip };
})(window.Shio);

(function (Shio) {
  const el = Shio.el;
  const scoreTimers = new WeakMap();

  function show(node, visible) {
    if (node) node.hidden = !visible;
  }

  function buildYearCard(card, side) {
    Shio.clear(card);
    const head = el("div", "year-head");
    head.appendChild(el("span", "year-pillar", side.pillar_hanzi));
    const meta = el("div");
    meta.appendChild(el("span", "dyn-name", side.shio_name));
    const nayin = side.nayin || {};
    meta.appendChild(el("span", "dyn-element", [nayin.hanzi, nayin.name].filter(Boolean).join(" · ")));
    head.appendChild(meta);
    card.appendChild(head);
    card.appendChild(el("p", "dyn-summary", (side.nayin_relation || {}).text || ""));
  }

  function renderYearLayer(root, layer) {
    const box = Shio.part(root, "year");
    show(box, Boolean(layer));
    if (!layer) return;
    Shio.part(root, "year-lichun").textContent = layer.lichun_note || "";
    const stem = Shio.part(root, "year-stem");
    const relation = layer.stem_relation || {};
    Shio.clear(stem);
    stem.className = "compat-year-stem kind-" + (relation.kind || "netral");
    stem.appendChild(el("span", "dyn-badge", [relation.hanzi, relation.label].filter(Boolean).join(" · ")));
    stem.appendChild(el("p", "dyn-summary", relation.text || ""));
    buildYearCard(Shio.part(root, "year-1"), layer.shio1);
    buildYearCard(Shio.part(root, "year-2"), layer.shio2);
  }

  function buildDynamicCard(card, side) {
    Shio.clear(card);
    card.className = "compat-dynamic-card role-" + side.role;
    const head = el("div", "dyn-head");
    head.appendChild(el("span", "dyn-icon", side.icon));
    const meta = el("div");
    const name = side.shio + " " + side.hanzi;
    meta.appendChild(el("span", "dyn-name", side.person ? side.person + " · " + name : name));
    meta.appendChild(el("span", "dyn-element", side.element + " " + side.element_hanzi));
    head.appendChild(meta);
    card.appendChild(head);
    card.appendChild(el("span", "dyn-badge", side.label));
    card.appendChild(el("p", "dyn-summary", side.summary));
    card.appendChild(el("p", "dyn-advice", side.advice));
  }

  function renderElementDynamic(root, dynamic) {
    show(Shio.part(root, "dynamic"), Boolean(dynamic));
    if (!dynamic) return;
    buildDynamicCard(Shio.part(root, "dyn-1"), dynamic.for_shio1);
    buildDynamicCard(Shio.part(root, "dyn-2"), dynamic.for_shio2);
    const arrow = Shio.part(root, "dyn-arrow");
    arrow.textContent = dynamic.for_shio1.arrow;
    arrow.classList.toggle("symmetric", Boolean(dynamic.symmetric));
  }

  function renderRelationBadge(root, relation, fallbackLabel) {
    const box = Shio.part(root, "relation-badge");
    const plain = Shio.part(root, "relationship");
    show(box, Boolean(relation));
    show(plain, !relation);
    if (!relation) {
      plain.textContent = fallbackLabel || "Data belum tersedia";
      return;
    }
    plain.textContent = "";
    box.className = "compat-relation-badge code-" + relation.code;
    Shio.part(root, "relation-hanzi").textContent = relation.hanzi;
    Shio.part(root, "relation-title").textContent = relation.label + " · " + relation.title;
    Shio.part(root, "relation-note").textContent = relation.note;
  }

  function renderDayPillar(root, pillar) {
    const box = Shio.part(root, "day-pillar");
    Shio.clear(box);
    box.className = "compat-day-pillar code-" + pillar.code;
    const head = el("div", "bazi-head");
    head.appendChild(el("span", "bazi-pillar", pillar.pillar1));
    head.appendChild(el("span", "bazi-link", pillar.hanzi));
    head.appendChild(el("span", "bazi-pillar", pillar.pillar2));
    box.appendChild(head);
    box.appendChild(el("span", "dyn-badge", pillar.label + " · " + pillar.title));
    box.appendChild(el("p", "dyn-summary", pillar.text));
    box.appendChild(el("p", "bazi-stem kind-" + pillar.stem_kind, pillar.stem_text));
  }

  function buildUsefulSide(side, layer) {
    const card = el("div", "useful-side");
    card.appendChild(el("span", "useful-side-name", side.label + " · " + side.pillar));
    card.appendChild(el("span", "useful-side-element", "Elemen diri " + side.element + " " + side.element_hanzi));
    card.appendChild(el("span", "useful-side-needs", "Butuh " + (side.needs || []).join(" & ")));
    if (side.supplies) card.appendChild(el("span", "useful-flag give", layer.supply_label));
    else if (side.burdens) card.appendChild(el("span", "useful-flag drain", layer.burden_label));
    else card.appendChild(el("span", "useful-flag flat", "Tidak menambah, tidak mengurangi"));
    return card;
  }

  function renderUsefulGod(root, match, layer) {
    const box = Shio.part(root, "useful");
    Shio.clear(box);
    box.className = "compat-useful code-" + match.code;
    const head = el("div", "useful-head");
    head.appendChild(el("span", "useful-glyph", "用神"));
    head.appendChild(el("span", "useful-title", match.title));
    box.appendChild(head);
    box.appendChild(el("p", "dyn-summary", match.note));
    const grid = el("div", "useful-grid");
    grid.appendChild(buildUsefulSide(match.side1, layer));
    grid.appendChild(buildUsefulSide(match.side2, layer));
    box.appendChild(grid);
    box.appendChild(el("p", "dyn-advice", match.advice));
  }

  function renderCoupleStars(root, stars) {
    const box = Shio.part(root, "stars");
    Shio.clear(box);
    show(box, Boolean(stars && stars.length));
    (stars || []).forEach((star) => {
      const card = el("div", "star-card code-" + star.code);
      const head = el("div", "star-head");
      head.appendChild(el("span", "star-icon", star.icon));
      head.appendChild(el("span", "star-title", star.title));
      head.appendChild(el("span", "star-who", star.who));
      card.appendChild(head);
      card.appendChild(el("p", "dyn-summary", star.note));
      box.appendChild(card);
    });
  }

  function renderBaziLayer(root, layer) {
    show(Shio.part(root, "bazi"), Boolean(layer));
    if (!layer) return;
    Shio.part(root, "bazi-title").textContent = layer.title;
    Shio.part(root, "bazi-note").textContent = layer.note;
    renderDayPillar(root, layer.day_pillar);
    renderUsefulGod(root, layer.useful_god, layer);
    renderCoupleStars(root, layer.couple_stars);
  }

  function renderPair(root, data) {
    const pair = Shio.part(root, "pair");
    Shio.clear(pair);
    const one = data.shio1 || {};
    const two = data.shio2 || {};
    const wrap = el("span", "compat-pair");
    wrap.appendChild(el("span", "compat-pair-hanzi", one.hanzi || ""));
    wrap.appendChild(el("span", "compat-pair-names", (one.name || "") + " × " + (two.name || "")));
    wrap.appendChild(el("span", "compat-pair-hanzi", two.hanzi || ""));
    pair.appendChild(wrap);
  }

  function renderNarrative(root, data) {
    const narrative = data.narrative || {};
    const title = Shio.part(root, "narrative-title");
    Shio.clear(title);
    if (narrative.icon) title.appendChild(Shio.icon(narrative.icon));
    title.appendChild(document.createTextNode(" " + (narrative.title || "")));
    Shio.part(root, "narrative").textContent = narrative.text || "-";
    Shio.part(root, "drama").textContent = data.drama || "-";
    Shio.part(root, "tips").textContent = data.tips || "-";
  }

  function renderCompatLayers(root, data) {
    renderPair(root, data);
    renderRelationBadge(root, data.pair_relation, data.relationship);
    renderElementDynamic(root, data.element_dynamic);
    renderYearLayer(root, data.year_layer);
    renderBaziLayer(root, data.bazi_layer);
    renderNarrative(root, data);
  }

  function scoreOf(data) {
    const score = Number(data && data.score);
    return Number.isFinite(score) ? Math.max(0, Math.min(100, Math.round(score))) : 0;
  }

  function renderScore(root, score, animate) {
    const text = Shio.part(root, "score-text");
    const circle = Shio.part(root, "score-circle");
    if (!text || !circle) return;
    const running = scoreTimers.get(root);
    if (running) clearInterval(running);
    scoreTimers.delete(root);
    circle.classList.remove("high", "mid", "low");
    circle.classList.add(score >= 70 ? "high" : score >= 45 ? "mid" : "low");
    if (!animate || window.prefersReducedMotion() || score <= 0) {
      circle.style.transition = animate ? "" : "none";
      circle.setAttribute("stroke-dasharray", score + ", 100");
      text.textContent = score + "%";
      if (!animate) {
        void circle.getBoundingClientRect();
        circle.style.transition = "";
      }
      return;
    }
    text.textContent = "0%";
    circle.style.transition = "none";
    circle.setAttribute("stroke-dasharray", "0, 100");
    void circle.getBoundingClientRect();
    circle.style.transition = "";
    let current = 0;
    const timer = setInterval(() => {
      current += 1;
      text.textContent = current + "%";
      if (current >= score) {
        clearInterval(timer);
        scoreTimers.delete(root);
        text.textContent = score + "%";
      }
    }, Math.max(10, Math.floor(1500 / score)));
    scoreTimers.set(root, timer);
    requestAnimationFrame(() => circle.setAttribute("stroke-dasharray", score + ", 100"));
  }

  async function submit() {
    const form = Shio.getState().form;
    if (!form.date1 || !form.date2) return null;
    const data = await Shio.run(() => Shio.postJson(Shio.api(), {
      tanggal1: form.date1,
      tanggal2: form.date2,
      lens: form.lens || "asmara",
    }));
    if (!data) return null;
    if (data.error && !data.shio1) {
      window.showErrorToast(data.error);
      return null;
    }
    Shio.setState({ result: data });
    return data;
  }

  function markLens(root, lens) {
    root.querySelectorAll("[data-lens]").forEach((chip) => {
      const on = chip.dataset.lens === lens;
      chip.classList.toggle("active", on);
      chip.setAttribute("aria-checked", on ? "true" : "false");
    });
  }

  Shio.onBoot((app) => {
    if (app.dataset.page === "peidui") Shio.updateForm({ lens: "asmara" });
  });

  Shio.renderCompatLayers = renderCompatLayers;
  Shio.compat = { submit: submit, scoreOf: scoreOf, renderScore: renderScore, markLens: markLens };
})(window.Shio);

(function (Shio) {
  const el = Shio.el;
  const history = {};
  const renderedPairs = new WeakMap();

  function historyLimit(size) {
    return Math.max(1, Math.min(size - 1, Math.floor(size / 2)));
  }

  function pickFrom(key, pool) {
    if (!Array.isArray(pool) || !pool.length) return "-";
    if (pool.length === 1) return pool[0];
    const seen = history[key] || (history[key] = []);
    const available = [];
    for (let i = 0; i < pool.length; i++) {
      if (seen.indexOf(i) === -1) available.push(i);
    }
    const source = available.length ? available : pool.map((item, i) => i);
    const index = source[Math.floor(Math.random() * source.length)];
    seen.push(index);
    while (seen.length > historyLimit(pool.length)) seen.shift();
    return pool[index];
  }

  function drawTraits(pool, count) {
    const copy = pool.slice();
    for (let i = copy.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const swap = copy[i];
      copy[i] = copy[j];
      copy[j] = swap;
    }
    return copy.slice(0, Math.min(count, copy.length));
  }

  function makeDraw(data, count) {
    return {
      count: count,
      headline: pickFrom("headline", data.headlines),
      traits: drawTraits(Array.isArray(data.toxic_traits) ? data.toxic_traits : [], data.traits_per_draw || 8),
      sin: pickFrom("sin", data.financial_sins),
      flag: pickFrom("flag", data.love_red_flags),
      catchphrase: pickFrom("catchphrase", data.catchphrases),
      weakness: pickFrom("weak", data.secret_weaknesses),
      tip: pickFrom("tip", data.survival_tips),
    };
  }

  async function submit() {
    const form = Shio.getState().form;
    if (!form.date) return null;
    const data = await Shio.run(() => Shio.postJson(Shio.api(), { tanggal: form.date, gender: form.gender || null }));
    if (!data) return null;
    if (data.error || !data.chart_roast) {
      window.showErrorToast(data.error || "Data roasting tidak ditemukan.");
      return null;
    }
    Object.keys(history).forEach((key) => delete history[key]);
    Shio.updateForm({ partner: null });
    Shio.setState({
      result: data,
      draw: makeDraw(data, 1),
      pair: null,
      ui: Object.assign({}, Shio.getState().ui, { pairOpen: false }),
    });
    return data;
  }

  function reroll() {
    const state = Shio.getState();
    if (!state.result) return;
    Shio.setState({ draw: makeDraw(state.result, (state.draw ? state.draw.count : 0) + 1) });
  }

  let pairRequest = 0;

  async function pair(partner) {
    const state = Shio.getState();
    if (!state.result || !partner) return;
    const requestId = ++pairRequest;
    Shio.updateForm({ partner: partner });
    Shio.setState({ pair: null, pairLoading: true });
    try {
      const data = await Shio.postJson(Shio.api(), { shio: state.result.chart_roast.shio_key, pasangan: partner });
      if (requestId !== pairRequest) return;
      Shio.setState({ pair: data.pair_roast || null, pairLoading: false });
    } catch (error) {
      if (requestId !== pairRequest) return;
      Shio.setState({ pairLoading: false });
      window.showErrorToast(error.message);
    }
  }

  function togglePair() {
    Shio.updateUi({ pairOpen: !Shio.getState().ui.pairOpen });
  }

  function comboLabel(data, draw) {
    const combinations = data.combination_count || 0;
    if (combinations < 2 || !draw) return "";
    return "racikan ke-" + draw.count + " dari " + combinations.toLocaleString("id-ID");
  }

  function canReroll(data) {
    return (data.combination_count || 0) >= 2;
  }

  function buildHeader(data) {
    const head = el("div", "roast-header");
    head.appendChild(el("div", "roast-hanzi", data.chart_roast.shio_hanzi || ""));
    head.appendChild(el("h2", "roast-shio-name", data.shio_name || ""));
    const stamp = el("span", "roast-stamp");
    stamp.appendChild(Shio.icon("fa-fire"));
    stamp.appendChild(document.createTextNode(" DIBAKAR HABIS"));
    head.appendChild(stamp);
    return head;
  }

  function buildHeadline(draw) {
    const box = el("div", "roast-headline");
    const mark = el("div", "roast-quote-mark");
    mark.appendChild(Shio.icon("fa-skull"));
    box.appendChild(mark);
    box.appendChild(el("p", null, draw.headline));
    return box;
  }

  function dmCard(hanzi, label, title, entry) {
    const card = el("div", "roast-dm-card");
    const head = el("div", "roast-dm-head");
    head.appendChild(el("span", "dm-hanzi", hanzi));
    const meta = el("div");
    meta.appendChild(el("span", "dm-label", label));
    meta.appendChild(el("span", "dm-title", title));
    head.appendChild(meta);
    card.appendChild(head);
    card.appendChild(el("p", "dm-headline", entry.headline));
    card.appendChild(el("p", "dm-roast", entry.roast));
    card.appendChild(el("p", "dm-tip", entry.tip));
    return card;
  }

  function buildChart(chart) {
    const box = el("div", "roast-chart");
    const summary = el("div", "chart-summary");
    [
      [chart.year_pillar, "Pilar tahun"],
      [chart.shio_hanzi + " " + chart.shio_name, "Shio dari tanggal"],
      [chart.year_element + " " + chart.year_polarity, "Elemen tahun"],
    ].forEach((row) => {
      const cell = el("div", "chart-cell");
      cell.appendChild(el("span", "chart-value", row[0]));
      cell.appendChild(el("span", "chart-label", row[1]));
      summary.appendChild(cell);
    });
    box.appendChild(summary);
    const dm = chart.day_master;
    if (dm) box.appendChild(dmCard(dm.stem_hanzi, "Pilar harimu sendiri (日主)", dm.pillar_hanzi + " · " + dm.title, dm));
    const dir = chart.direction;
    if (dir) {
      box.appendChild(dmCard(dir.direction_hanzi, "Arah periode besar (大運)",
        dir.direction_label + " · batang tahun " + dir.polarity + " + " + dir.gender, dir));
    }
    return box;
  }

  function buildTraits(draw) {
    const box = el("div", "roast-section");
    const title = el("h3", "roast-section-title");
    title.appendChild(Shio.icon("fa-biohazard"));
    title.appendChild(document.createTextNode(" Toxic Traits"));
    box.appendChild(title);
    const list = el("ul", "roast-traits");
    draw.traits.forEach((trait) => list.appendChild(el("li", null, trait)));
    box.appendChild(list);
    return box;
  }

  function sinBox(kind, iconName, title, text) {
    const box = el("div", "roast-sin-box " + kind);
    const iconBox = el("div", "sin-icon");
    iconBox.appendChild(Shio.icon(iconName));
    box.appendChild(iconBox);
    box.appendChild(el("h3", null, title));
    box.appendChild(el("p", null, text));
    return box;
  }

  function buildSins(draw) {
    const box = el("div", "roast-sins");
    box.appendChild(sinBox("sin-money", "fa-sack-xmark", "Dosa Finansial", draw.sin));
    box.appendChild(sinBox("sin-love", "fa-heart-crack", "Red Flag Asmara", draw.flag));
    return box;
  }

  function buildCatchphrase(draw) {
    const box = el("div", "roast-catchphrase");
    box.appendChild(Shio.icon("fa-quote-left"));
    box.appendChild(el("p", null, draw.catchphrase));
    return box;
  }

  function sideNote(kind, iconName, title, text) {
    const box = el("div", "roast-" + kind);
    const iconBox = el("div", kind + "-icon");
    iconBox.appendChild(Shio.icon(iconName));
    box.appendChild(iconBox);
    const body = el("div", kind + "-body");
    body.appendChild(el("h3", null, title));
    body.appendChild(el("p", null, text));
    box.appendChild(body);
    return box;
  }

  function sections(data, draw) {
    return [
      { key: "headline", title: "Headline", node: buildHeadline(draw) },
      { key: "chart", title: "Kartu Ba Zi", node: buildChart(data.chart_roast) },
      { key: "traits", title: "Toxic Traits", node: buildTraits(draw) },
      { key: "sins", title: "Dosa & Red Flag", node: buildSins(draw) },
      { key: "catchphrase", title: "Kalimat Andalan", node: buildCatchphrase(draw) },
      { key: "weakness", title: "Kelemahan Rahasia", node: sideNote("weakness", "fa-user-secret", "Kelemahan Rahasia", draw.weakness) },
      { key: "tip", title: "Survival Tip", node: sideNote("tip", "fa-hand-holding-heart", "Survival Tip", draw.tip) },
    ];
  }

  function renderPairCard(card, data) {
    Shio.clear(card);
    card.hidden = !data;
    if (!data) return;
    card.className = "roast-pair-card code-" + data.code;
    const head = el("div", "roast-pair-head");
    head.appendChild(el("span", "pair-hanzi", data.shio1.hanzi));
    head.appendChild(el("span", "pair-rel", data.relation_hanzi + " " + data.relation_label));
    head.appendChild(el("span", "pair-hanzi", data.shio2.hanzi));
    card.appendChild(head);
    card.appendChild(el("p", "pair-verdict", data.verdict));
    card.appendChild(el("p", "pair-roast", data.roast));
    card.appendChild(el("p", "pair-tip", data.tip));
    Shio.replay(card, "roast-flash");
  }

  function renderPairPanel(nodes, state) {
    const open = Boolean(state.ui.pairOpen);
    nodes.toggle.classList.toggle("open", open);
    nodes.toggle.setAttribute("aria-expanded", open ? "true" : "false");
    nodes.body.hidden = !open;
    Shio.markChoice(nodes.body, "shio", state.form.partner);
    nodes.loading.hidden = !state.pairLoading;
    if (renderedPairs.get(nodes.card) !== state.pair) {
      renderPairCard(nodes.card, state.pair);
      renderedPairs.set(nodes.card, state.pair);
    }
  }

  function bindPairPanel(nodes) {
    nodes.toggle.addEventListener("click", togglePair);
    nodes.body.querySelectorAll("[data-shio]").forEach((button) => {
      button.addEventListener("click", () => pair(button.dataset.shio));
    });
  }

  function bindGender(root, onChange) {
    root.querySelectorAll("[data-gender]").forEach((button) => {
      button.addEventListener("click", () => {
        const current = Shio.getState().form.gender;
        Shio.updateForm({ gender: current === button.dataset.gender ? null : button.dataset.gender });
        onChange();
      });
    });
  }

  Shio.roast = {
    submit: submit,
    reroll: reroll,
    comboLabel: comboLabel,
    canReroll: canReroll,
    buildHeader: buildHeader,
    sections: sections,
    renderPairPanel: renderPairPanel,
    bindPairPanel: bindPairPanel,
    bindGender: bindGender,
  };
})(window.Shio);

(function (Shio) {
  const el = Shio.el;

  function paragraph(parent, text, className) {
    if (!text) return;
    parent.appendChild(el("p", className || "destiny-text", text));
  }

  function bulletList(parent, items, className) {
    if (!items || !items.length) return;
    const list = el("ul", className || "destiny-list");
    items.forEach((item) => list.appendChild(el("li", null, item)));
    parent.appendChild(list);
  }

  function card(className) {
    return el("div", "destiny-card" + (className ? " " + className : ""));
  }

  function labelled(parent, label, value) {
    if (!value) return;
    const row = el("p", "destiny-kv");
    row.appendChild(el("span", "destiny-kv-label", label));
    row.appendChild(el("span", "destiny-kv-value", value));
    parent.appendChild(row);
  }

  function twoLists(leftTitle, leftItems, rightTitle, rightItems) {
    const columns = el("div", "destiny-two-col");
    const left = el("div");
    left.appendChild(el("h4", null, leftTitle));
    bulletList(left, leftItems, "destiny-list destiny-list-ok");
    const right = el("div");
    right.appendChild(el("h4", null, rightTitle));
    bulletList(right, rightItems, "destiny-list destiny-list-off");
    columns.appendChild(left);
    columns.appendChild(right);
    return columns;
  }

  function headBlock(className, hanzi, hanziClass, title, sub) {
    const head = el("div", className);
    head.appendChild(el("span", hanziClass, hanzi));
    const meta = el("div");
    meta.appendChild(el("h4", "destiny-dm-title", title));
    meta.appendChild(el("span", "destiny-dm-sub", sub));
    head.appendChild(meta);
    return head;
  }

  function notice(icon, title, warn, fill) {
    const box = el("div", "destiny-notice" + (warn ? " destiny-notice-warn" : ""));
    box.appendChild(el("span", "destiny-notice-icon", icon));
    const body = el("div");
    body.appendChild(el("strong", null, title));
    fill(body);
    box.appendChild(body);
    return box;
  }

  function buildNotices(meta, noBirthTime) {
    const box = el("div", "destiny-notices");
    box.appendChild(notice("☯", "Aliran " + meta.school, false, (body) => {
      paragraph(body, "Perhitungan memakai batas awal musim semi (立春) untuk pilar tahun dan batas 23:00 untuk pilar hari (子時換日).", "destiny-notice-text");
    }));
    if (meta.late_zi_alternative_day) {
      box.appendChild(notice("🌗", "Kamu lahir di jam 23:00–23:59", true, (body) => {
        paragraph(body, "Aliran yang dipakai di sini menganggap harimu sudah berganti sejak pukul 23:00. Sebagian praktisi Zi Ping memakai aliran lain (子正換日) yang baru mengganti hari pukul 00:00.", "destiny-notice-text");
        paragraph(body, "Menurut aliran itu, pilar harimu adalah " + meta.late_zi_alternative_day + ", bukan pilar hari di tabel bawah, dan pilar jammu ikut berubah. Dua-duanya sah — bedanya ada di aturan, bukan di hitungan.", "destiny-notice-text");
      }));
    }
    if (meta.city_unrecognized) {
      box.appendChild(notice("📍", "Kota lahir tidak dikenali", true, (body) => {
        paragraph(body, "Nama kota yang kamu ketik tidak ada di daftar, jadi zona WIB dipakai sebagai asumsi. Hasilnya bisa berbeda kalau kamu lahir di WITA atau WIT tepat di hari pergantian musim. Ketik ulang lalu pilih dari daftar supaya tepat.", "destiny-notice-text");
      }));
    }
    if (meta.city_zone_only) {
      box.appendChild(notice("📍", "Kota dipakai untuk zona waktu", false, (body) => {
        paragraph(body, "Tanpa jam lahir, " + meta.city.name + " dipakai untuk menentukan zona " + meta.city.zone + " di batas pergantian musim. Koreksi waktu matahari sejati butuh jam lahir, jadi belum diterapkan.", "destiny-notice-text");
      }));
    }
    if (meta.city && meta.true_solar_offset_minutes !== null && meta.true_solar_offset_minutes !== undefined) {
      box.appendChild(notice("🕰", "Koreksi waktu matahari sejati", false, (body) => {
        const offset = meta.true_solar_offset_minutes;
        paragraph(body, "Jam lahirmu dibaca sebagai waktu " + meta.city.zone + " lalu digeser " + (offset >= 0 ? "+" : "") +
          offset.toFixed(1) + " menit menurut bujur " + meta.city.name + " (" + meta.city.longitude + "°BT) terhadap meridian " +
          meta.city.zone_meridian + "°BT.", "destiny-notice-text");
        if (meta.city.assumed) {
          paragraph(body, "Kota lahir tidak dipilih atau tidak dikenali, jadi dipakai " + meta.city.name + " sebagai asumsi. Ketik ulang lalu pilih dari daftar supaya tepat.", "destiny-notice-text");
        }
      }));
    }
    if (noBirthTime) {
      box.appendChild(notice("🕯", "Bacaan tiga pilar", true, (body) => {
        paragraph(body, noBirthTime.notice, "destiny-notice-text");
        const columns = twoLists("Tetap sah dibaca", noBirthTime.still_valid, "Tidak ditampilkan", noBirthTime.not_available);
        columns.className = "destiny-notice-columns";
        body.appendChild(columns);
        paragraph(body, noBirthTime.invitation, "destiny-notice-text");
      }));
    }
    return box;
  }

  function updateChartHint(frame) {
    const scroll = frame.querySelector(".destiny-chart-scroll");
    if (!scroll) return;
    const maxScroll = scroll.scrollWidth - scroll.clientWidth;
    frame.classList.toggle("more-left", scroll.scrollLeft > 4);
    frame.classList.toggle("more-right", scroll.scrollLeft < maxScroll - 4);
  }

  function rowHead(hanzi, label) {
    const cell = el("th", "destiny-chart-rowhead");
    cell.appendChild(el("span", "destiny-chart-rowhead-hanzi", hanzi));
    cell.appendChild(el("span", "destiny-chart-rowhead-label", label));
    return cell;
  }

  function buildTable(pillars) {
    const table = el("table", "destiny-chart");
    const available = pillars.filter((p) => p.available);
    const headRow = el("tr");
    headRow.appendChild(el("th", "destiny-chart-corner", ""));
    available.forEach((p) => {
      const cell = el("th");
      cell.appendChild(el("span", "destiny-chart-hanzi-small", p.hanzi));
      cell.appendChild(el("span", "destiny-chart-label", p.label));
      headRow.appendChild(cell);
    });
    const head = el("thead");
    head.appendChild(headRow);
    table.appendChild(head);
    const body = el("tbody");
    const stemRow = el("tr");
    stemRow.appendChild(rowHead("天干", "Batang Langit"));
    available.forEach((p) => {
      const cell = el("td");
      cell.appendChild(el("span", "destiny-chart-hanzi", p.stem_hanzi));
      cell.appendChild(el("span", "destiny-chart-sub", p.stem + " · " + p.stem_element));
      cell.appendChild(el("span", "destiny-chart-god", p.stem_god.hanzi + " " + p.stem_god.meaning));
      stemRow.appendChild(cell);
    });
    body.appendChild(stemRow);
    const branchRow = el("tr");
    branchRow.appendChild(rowHead("地支", "Cabang Bumi"));
    available.forEach((p) => {
      const cell = el("td");
      cell.appendChild(el("span", "destiny-chart-hanzi", p.branch_hanzi));
      cell.appendChild(el("span", "destiny-chart-sub", p.branch + " · " + p.branch_element));
      branchRow.appendChild(cell);
    });
    body.appendChild(branchRow);
    const hiddenRow = el("tr");
    hiddenRow.appendChild(rowHead("藏干", "Batang Tersembunyi"));
    available.forEach((p) => {
      const cell = el("td");
      p.hidden_stems.forEach((h) => {
        const item = el("span", "destiny-hidden");
        item.appendChild(el("span", "destiny-hidden-hanzi", h.hanzi));
        item.appendChild(el("span", "destiny-hidden-god", h.god.hanzi + " " + h.god.meaning));
        cell.appendChild(item);
      });
      hiddenRow.appendChild(cell);
    });
    body.appendChild(hiddenRow);
    table.appendChild(body);
    return table;
  }

  function buildChart(pillars) {
    const wrap = el("div");
    wrap.appendChild(el("p", "destiny-note", "Ini chart mentahmu, bukan ringkasan. Kamu bisa mencocokkannya dengan kalkulator Ba Zi mana pun."));
    const frame = el("div", "destiny-chart-frame");
    const hint = el("p", "destiny-scroll-hint", "Geser tabel ke samping ");
    hint.setAttribute("aria-hidden", "true");
    hint.appendChild(Shio.icon("fa-arrow-right-long"));
    frame.appendChild(hint);
    const viewport = el("div", "destiny-chart-viewport");
    const scroll = el("div", "destiny-chart-scroll");
    scroll.appendChild(buildTable(pillars));
    scroll.addEventListener("scroll", () => updateChartHint(frame), { passive: true });
    viewport.appendChild(scroll);
    frame.appendChild(viewport);
    wrap.appendChild(frame);
    const positions = el("div", "destiny-positions");
    pillars.forEach((p) => {
      const item = card("destiny-position" + (p.available ? "" : " destiny-position-off"));
      const title = el("h4", "destiny-position-title");
      title.appendChild(el("span", "destiny-position-hanzi", p.hanzi));
      title.appendChild(el("span", null, p.label));
      title.appendChild(el("span", "destiny-position-age", p.age_range));
      item.appendChild(title);
      paragraph(item, p.domain, "destiny-text destiny-text-small");
      paragraph(item, p.available ? p.reading_note : "Tidak tersedia tanpa jam lahir.", "destiny-text destiny-text-small");
      positions.appendChild(item);
    });
    wrap.appendChild(positions);
    return wrap;
  }

  function buildDayMaster(dm) {
    const item = card();
    item.appendChild(headBlock("destiny-dm-head", dm.hanzi, "destiny-dm-hanzi", dm.title, dm.name + " · " + dm.element + " " + dm.polarity));
    paragraph(item, dm.personality);
    paragraph(item, dm.variant, "destiny-text destiny-text-accent");
    item.appendChild(twoLists("Kekuatan", dm.strengths, "Kelemahan", dm.weaknesses));
    return item;
  }

  function buildStrength(strength, useful) {
    const item = card();
    item.appendChild(headBlock("destiny-strength-head", strength.hanzi, "destiny-strength-hanzi", strength.title, strength.label));
    paragraph(item, strength.summary);
    paragraph(item, strength.advice);
    paragraph(item, strength.caution, "destiny-text destiny-text-warn");
    labelled(item, "Rasio dukungan", (strength.support_ratio * 100).toFixed(1) + "%");
    labelled(item, "Elemen menguntungkan", useful.favourable.join(", "));
    labelled(item, "Elemen merugikan", useful.unfavourable.join(", "));
    return item;
  }

  function buildRelations(relations) {
    const box = el("div");
    box.appendChild(el("p", "destiny-note", "Bagaimana pilar-pilarmu sendiri saling tarik, saling kunci, atau saling bentrok."));
    const items = (relations && relations.items) || [];
    if (!items.length) {
      paragraph(box, "Pilar-pilarmu tidak saling mengunci atau bentrok. Energinya berdiri sendiri-sendiri, jadi bacaanmu lebih banyak ditentukan oleh elemen dan dewanya.");
      return box;
    }
    const grid = el("div", "destiny-relation-grid");
    items.forEach((item) => {
      const entry = card("destiny-relation destiny-relation-" + item.code);
      const head = el("div", "destiny-relation-head");
      head.appendChild(el("span", "destiny-relation-hanzi", item.hanzi));
      const meta = el("div");
      meta.appendChild(el("h4", "destiny-relation-title", item.title));
      meta.appendChild(el("span", "destiny-dm-sub", item.slots.join(" · ") + " · " + item.branches));
      head.appendChild(meta);
      entry.appendChild(head);
      if (item.element) {
        entry.appendChild(el("span", "destiny-relation-tag", "Elemen " + item.element + " " + item.element_hanzi));
      } else if (item.reach_label) {
        const tag = el("span", "destiny-relation-tag destiny-relation-" + item.reach, item.reach_label);
        tag.title = item.reach_note;
        entry.appendChild(tag);
      }
      paragraph(entry, item.note, "destiny-text destiny-text-small");
      paragraph(entry, item.advice, "destiny-text destiny-text-small destiny-text-muted");
      grid.appendChild(entry);
    });
    box.appendChild(grid);
    if (relations.clash_note) paragraph(box, relations.clash_note, "destiny-note");
    return box;
  }

  function buildElements(elements) {
    const box = el("div");
    const max = elements.reduce((acc, e) => Math.max(acc, e.score), 0) || 1;
    elements.forEach((e) => {
      const item = card("destiny-element destiny-role-" + e.role);
      const head = el("div", "destiny-element-head");
      head.appendChild(el("span", "destiny-element-name", e.label + " " + e.hanzi));
      head.appendChild(el("span", "destiny-element-score", e.score.toFixed(2)));
      item.appendChild(head);
      const bar = el("div", "destiny-bar");
      const fill = el("div", "destiny-bar-fill");
      fill.style.width = Math.round((e.score / max) * 100) + "%";
      bar.appendChild(fill);
      item.appendChild(bar);
      const tags = el("div", "destiny-tags");
      tags.appendChild(el("span", "destiny-tag destiny-tag-" + e.status, e.status));
      tags.appendChild(el("span", "destiny-tag destiny-tag-role-" + e.role, e.role));
      item.appendChild(tags);
      paragraph(item, e.status_label, "destiny-text destiny-text-small destiny-text-accent");
      paragraph(item, e.impact, "destiny-text destiny-text-small");
      paragraph(item, e.verdict, "destiny-text destiny-text-small destiny-text-accent");
      paragraph(item, e.action, "destiny-text destiny-text-small");
      paragraph(item, e.remedy, "destiny-text destiny-text-small");
      box.appendChild(item);
    });
    return box;
  }

  function buildGod(god) {
    const item = card();
    item.appendChild(headBlock("destiny-dm-head", god.name_cn, "destiny-dm-hanzi", god.name_id, "Menguasai " + Math.round(god.share * 100) + "% bobot chart"));
    if (!god.decisive) {
      paragraph(item, "Selisihnya tipis dengan dewa di bawahnya, jadi bacaan ini condong, bukan mutlak.", "destiny-text destiny-text-warn destiny-text-small");
    }
    paragraph(item, god.essence);
    paragraph(item, god.variant, "destiny-text destiny-text-accent");
    return item;
  }

  function destinyCard(title, lines) {
    const item = card("destiny-destiny-card");
    item.appendChild(el("h4", "destiny-destiny-title", title));
    lines.forEach((line) => {
      if (typeof line === "function") line(item);
      else paragraph(item, line[0], "destiny-text destiny-text-small" + (line[1] ? " " + line[1] : ""));
    });
    return item;
  }

  function buildDestiny(destiny, nuance, disclaimer) {
    const grid = el("div", "destiny-destiny-grid");
    grid.appendChild(destinyCard("Karir — " + destiny.career.archetype, [
      [destiny.career.work_style],
      (item) => bulletList(item, destiny.career.ideal_fields, "destiny-list destiny-list-plain"),
      [destiny.career.warning, "destiny-text-warn"],
      [nuance.karir, "destiny-text-accent"],
    ]));
    grid.appendChild(destinyCard("Rezeki — " + destiny.wealth.wealth_type, [
      [destiny.wealth.investment_advice],
      [destiny.wealth.financial_trap, "destiny-text-warn"],
      [destiny.wealth.lucky_period],
      [nuance.rezeki, "destiny-text-accent"],
    ]));
    grid.appendChild(destinyCard("Asmara — " + destiny.love.love_type, [
      [destiny.love.ideal_partner_desc],
      [destiny.love.red_flag, "destiny-text-warn"],
      [destiny.love.peach_blossom_note],
      [nuance.asmara, "destiny-text-accent"],
    ]));
    grid.appendChild(destinyCard("Kesehatan — " + destiny.health.energy_type, [
      [destiny.health.exercise_advice],
      [destiny.health.taboo, "destiny-text-warn"],
      (item) => destiny.health.organs.forEach((organ) => {
        const row = el("div", "destiny-organ");
        row.appendChild(el("strong", null, organ.element + " tipis — " + organ.vulnerable_organ));
        paragraph(row, organ.symptoms, "destiny-text destiny-text-small");
        paragraph(row, organ.prevention, "destiny-text destiny-text-small");
        item.appendChild(row);
      }),
      [disclaimer, "destiny-text-muted"],
    ]));
    return grid;
  }

  function buildShenSha(stars) {
    if (!stars.length) {
      return el("p", "destiny-text", "Tidak ada bintang nasib menonjol di chart-mu. Itu bukan kekurangan — bacaanmu ditentukan sepenuhnya oleh pilar dan dewanya.");
    }
    const grid = el("div", "destiny-star-grid");
    stars.forEach((star) => {
      const item = card("destiny-star destiny-star-" + star.category);
      const head = el("div", "destiny-star-head");
      head.appendChild(el("span", "destiny-star-icon", star.icon));
      const meta = el("div");
      meta.appendChild(el("h4", "destiny-star-title", star.name_id));
      meta.appendChild(el("span", "destiny-dm-sub", star.name_cn + " · " + star.slots.join(", ")));
      head.appendChild(meta);
      item.appendChild(head);
      paragraph(item, star.description, "destiny-text destiny-text-small");
      paragraph(item, star.life_impact, "destiny-text destiny-text-small");
      grid.appendChild(item);
    });
    return grid;
  }

  function buildLuck(luck) {
    const box = el("div");
    box.appendChild(el("p", "destiny-note", "Arah " + luck.direction + ", mulai berlaku sekitar usia " +
      luck.start_age_years + " tahun " + luck.start_age_months + " bulan."));
    luck.pillars.forEach((p) => {
      const item = card("destiny-luck-item");
      const head = el("div", "destiny-luck-head");
      head.appendChild(el("span", "destiny-luck-hanzi", p.pillar_hanzi));
      const meta = el("div");
      meta.appendChild(el("h4", "destiny-luck-title", p.phase_name));
      meta.appendChild(el("span", "destiny-dm-sub", "Usia " + p.age_from + "–" + p.age_to + " · " + p.year_from + "–" +
        p.year_to + " · " + p.dominant_god.hanzi + " " + p.dominant_god.meaning));
      head.appendChild(meta);
      item.appendChild(head);
      paragraph(item, p.description, "destiny-text destiny-text-small");
      paragraph(item, p.advice, "destiny-text destiny-text-small destiny-text-accent");
      box.appendChild(item);
    });
    return box;
  }

  function buildHeritage(heritage) {
    const box = el("div");
    box.appendChild(el("p", "destiny-note", "Lapisan cabang tahun: latar keluarga, masa kecil, dan wajah sosialmu — bukan diri sejatimu, karena itu sudah dibahas di bagian Day Master."));
    const item = card();
    item.appendChild(headBlock("destiny-dm-head", heritage.icon, "destiny-dm-hanzi", heritage.shio_name + " " + heritage.shio_hanzi,
      "Cabang tahun " + heritage.branch_hanzi + " · " + heritage.branch_element));
    heritage.persona.split("\n\n").forEach((part) => paragraph(item, part));
    paragraph(item, heritage.relation_text, "destiny-text destiny-text-accent");
    const alter = el("div", "destiny-alter");
    alter.appendChild(el("h4", null, heritage.alter_ego.title));
    paragraph(alter, heritage.alter_ego.description, "destiny-text destiny-text-small");
    item.appendChild(alter);
    item.appendChild(twoLists("Yang orang lihat", heritage.traits_positive, "Yang bikin repot", heritage.traits_negative));
    item.appendChild(twoLists("Green flag", heritage.green_flags, "Red flag", heritage.red_flags));
    const facts = el("div", "destiny-facts");
    labelled(facts, "Bunga keberuntungan", heritage.lucky_flowers.join(", "));
    labelled(facts, "Warna yang menekan", heritage.unlucky_colors.join(", "));
    labelled(facts, "Angka yang menekan", heritage.unlucky_numbers.join(", "));
    labelled(facts, "Bulan mendukung", heritage.best_months.join(", "));
    labelled(facts, "Bulan menggesek", heritage.worst_months.join(", "));
    labelled(facts, "Tokoh seangkatan shio", heritage.famous_people.join(", "));
    item.appendChild(facts);
    paragraph(item, heritage.spirit_advice, "destiny-text destiny-text-accent");
    box.appendChild(item);
    return box;
  }

  function buildRemedy(remedies) {
    const box = el("div");
    box.appendChild(el("p", "destiny-note", "Hanya untuk elemen yang menguntungkanmu."));
    const grid = el("div", "destiny-remedy-grid");
    remedies.forEach((r) => {
      const item = card("destiny-remedy-card");
      item.appendChild(el("h4", "destiny-destiny-title", r.element));
      labelled(item, "Warna", r.colors.join(", "));
      labelled(item, "Arah", r.directions.join(", "));
      labelled(item, "Angka", r.numbers.join(", "));
      labelled(item, "Kristal", r.crystals.join(", "));
      labelled(item, "Makanan", r.food_elements.join(", "));
      paragraph(item, r.ritual_advice, "destiny-text destiny-text-small");
      grid.appendChild(item);
    });
    box.appendChild(grid);
    return box;
  }

  function sections(data) {
    const list = [
      { key: "chart", title: "Empat Pilar", icon: "fa-table-columns", build: () => buildChart(data.pillars) },
      { key: "daymaster", title: "Day Master", icon: "fa-user-astronaut", build: () => buildDayMaster(data.day_master) },
      { key: "strength", title: "Kekuatan Diri", icon: "fa-scale-balanced", build: () => buildStrength(data.strength, data.useful_gods) },
      { key: "relations", title: "Relasi di Dalam Chart", icon: "fa-diagram-project", build: () => buildRelations(data.relations) },
      { key: "elements", title: "Lima Elemen", icon: "fa-chart-simple", build: () => buildElements(data.elements) },
      { key: "god", title: "Dewa Dominan", icon: "fa-hand-sparkles", build: () => buildGod(data.dominant_god) },
      { key: "destiny", title: "Peta Takdir", icon: "fa-compass",
        build: () => buildDestiny(data.destiny, data.day_master.nuance, data.meta.disclaimer) },
      { key: "shensha", title: "Bintang Nasib", icon: "fa-star", build: () => buildShenSha(data.shen_sha || []) },
    ];
    if (data.luck) list.push({ key: "luck", title: "Periode Besar", icon: "fa-hourglass-half", build: () => buildLuck(data.luck) });
    list.push({ key: "heritage", title: "Wajah Luar & Warisan Leluhur", icon: "fa-house-chimney", build: () => buildHeritage(data.heritage) });
    list.push({ key: "remedy", title: "Penyeimbang", icon: "fa-gem", build: () => buildRemedy(data.remedy || []) });
    return list;
  }

  function summary(data) {
    const dm = data.day_master || {};
    const available = (data.pillars || []).filter((p) => p.available).map((p) => p.hanzi);
    return [dm.hanzi, dm.title].filter(Boolean).join(" ") + " · " + available.length + " pilar";
  }

  function refreshChartHints(root) {
    requestAnimationFrame(() => root.querySelectorAll(".destiny-chart-frame").forEach(updateChartHint));
  }

  async function submit() {
    const form = Shio.getState().form;
    if (!form.date || !form.gender) return null;
    const hasHour = form.hour !== "" && form.hour !== undefined && form.hour !== null;
    const data = await Shio.run(() => Shio.postJson(Shio.api(), {
      tanggal: form.date,
      jam: hasHour ? form.hour : null,
      menit: hasHour ? form.minute || "0" : null,
      kota: form.city || null,
      gender: form.gender,
    }));
    if (!data) return null;
    Shio.setState({ result: data });
    return data;
  }

  function bindTimeFields(hour, minute, onChange) {
    hour.addEventListener("change", () => {
      const patch = { hour: hour.value };
      if (hour.value === "") patch.minute = "";
      else if (!Shio.getState().form.minute) patch.minute = "0";
      Shio.updateForm(patch);
      onChange();
    });
    minute.addEventListener("change", () => {
      Shio.updateForm({ minute: minute.value });
      onChange();
    });
  }

  function syncTimeFields(hour, minute, form) {
    hour.value = form.hour || "";
    minute.disabled = !form.hour;
    minute.value = form.hour ? form.minute || "0" : "";
  }

  Shio.destiny = {
    submit: submit,
    buildNotices: buildNotices,
    sections: sections,
    summary: summary,
    refreshChartHints: refreshChartHints,
    bindTimeFields: bindTimeFields,
    syncTimeFields: syncTimeFields,
  };
})(window.Shio);

(function (Shio) {
  const el = Shio.el;
  const CODE_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ";
  const CODE_LENGTH = 6;
  const SEAT_PREFIX = "shio_quiz_seat_";
  const ROOMS_API = "/api/shio/quiz/rooms";

  function normaliseCode(value) {
    const code = String(value || "").replace(/[\s-]/g, "").toUpperCase().replace(/O/g, "0").replace(/[IL]/g, "1");
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
    } catch (error) {
      return null;
    }
  }

  function saveSeat(code, seat) {
    try {
      localStorage.setItem(SEAT_PREFIX + code, JSON.stringify(seat));
    } catch (error) {}
  }

  function clearSeat(code) {
    try {
      localStorage.removeItem(SEAT_PREFIX + code);
    } catch (error) {}
  }

  async function request(path, options) {
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
    } catch (error) {
      payload = null;
    }
    if (!res.ok) {
      const error = new Error((payload && payload.error) || "Server menolak permintaan (status " + res.status + ").");
      error.status = res.status;
      throw error;
    }
    return payload;
  }

  function roomPage(roomCode) {
    return "/shio/quiz/" + roomCode;
  }

  function joinByCode() {
    const code = normaliseCode(Shio.getState().form.code);
    if (!code) {
      window.showErrorToast("Kode room terdiri dari 6 huruf atau angka.");
      return false;
    }
    window.location.href = roomPage(code);
    return true;
  }

  async function createRoom() {
    const form = Shio.getState().form;
    const name = (form.name || "").trim();
    if (!form.mode) return window.showErrorToast("Pilih mode quiz dulu.");
    if (!name) return window.showErrorToast("Isi nama panggilanmu dulu.");
    if (!form.birth) return window.showErrorToast("Pilih tanggal lahirmu dulu.");
    if (form.mode === "pasangan" && !form.relation) return window.showErrorToast("Pilih jenis hubungan kalian dulu.");
    const body = { mode: form.mode, name: name, birth_date: form.birth };
    if (form.mode === "pasangan") body.relation_type = form.relation;
    if (form.mode === "tebak") body.flavor = form.flavor || "manis";
    const data = await Shio.run(() => request(ROOMS_API, { method: "POST", body: body }));
    if (!data) return null;
    saveSeat(data.room_code, { token: data.token, slot: data.slot });
    Shio.setState({ loading: true });
    window.location.href = roomPage(data.room_code);
    return data;
  }

  function markRadio(root, attribute, value) {
    root.querySelectorAll("[data-" + attribute + "]").forEach((button) => {
      const on = button.dataset[attribute] === value;
      button.classList.toggle("active", on);
      button.setAttribute("aria-checked", on ? "true" : "false");
    });
  }

  function renderOptions(root, form) {
    markRadio(root, "mode", form.mode);
    markRadio(root, "relation", form.relation);
    markRadio(root, "flavor", form.flavor);
    root.querySelectorAll("[data-quiz-group]").forEach((group) => {
      group.hidden = group.dataset.quizGroup !== (form.mode === "pasangan" ? "relation" : form.mode === "tebak" ? "flavor" : "");
    });
    const chip = root.querySelector('[data-flavor="' + form.flavor + '"]');
    const note = root.querySelector("[data-quiz-flavor-note]");
    if (note) note.textContent = chip ? chip.dataset.note : "";
  }

  function modeTitle(root, mode) {
    const button = root.querySelector('[data-mode="' + mode + '"] .quiz-mode-title');
    return button ? button.textContent : "";
  }

  function bindOptions(root, onChange) {
    ["mode", "relation", "flavor"].forEach((attribute) => {
      root.querySelectorAll("[data-" + attribute + "]").forEach((button) => {
        button.addEventListener("click", () => {
          Shio.updateForm({ [attribute]: button.dataset[attribute] });
          renderOptions(root, Shio.getState().form);
          onChange(attribute);
        });
      });
    });
  }

  Shio.onBoot((app) => {
    if (app.dataset.page === "juhui") Shio.updateForm({ flavor: "manis" });
  });

  Shio.quizLobby = {
    normaliseCode: normaliseCode,
    joinByCode: joinByCode,
    createRoom: createRoom,
    renderOptions: renderOptions,
    bindOptions: bindOptions,
    modeTitle: modeTitle,
  };

  const POLL_STEPS = [2000, 2000, 3000, 5000, 5000, 10000];
  const POLL_IDLE_LIMIT = 15 * 60 * 1000;
  const FINISH_CONFIRM_MS = 4000;
  let code = "";
  let seat = null;
  let lastSignature = "";
  let pollTimer = null;
  let pollStep = 0;
  let lastChangeAt = Date.now();
  let inFlight = false;
  let finishArmedUntil = 0;

  function setNotice(text, withRefresh) {
    Shio.setState({ notice: text ? { text: text, refresh: Boolean(withRefresh) } : null });
  }

  function schedulePoll() {
    clearTimeout(pollTimer);
    pollTimer = null;
    const view = Shio.getState().room;
    if (!view || view.status === "done" || document.hidden) return;
    if (Date.now() - lastChangeAt > POLL_IDLE_LIMIT) {
      setNotice("Room ini sudah lama tidak berubah, jadi pembaruan otomatis dijeda.", true);
      return;
    }
    pollTimer = setTimeout(refresh, POLL_STEPS[Math.min(pollStep, POLL_STEPS.length - 1)]);
  }

  async function refresh() {
    if (inFlight) return;
    inFlight = true;
    clearTimeout(pollTimer);
    try {
      const view = await request(ROOMS_API + "/" + code, { token: seat && seat.token });
      const signature = JSON.stringify(view);
      if (signature !== lastSignature) {
        lastSignature = signature;
        lastChangeAt = Date.now();
        pollStep = 0;
        if (seat && !view.me) {
          clearSeat(code);
          seat = null;
        }
        const notice = Shio.getState().notice;
        Shio.setState({ room: view, missing: false, notice: notice && notice.refresh ? null : notice });
      } else {
        pollStep += 1;
        const notice = Shio.getState().notice;
        if (notice && notice.refresh) setNotice(null);
      }
    } catch (error) {
      if (error.status === 404) {
        inFlight = false;
        Shio.setState({ room: null, missing: true, notice: { text: error.message, refresh: false } });
        return;
      }
      pollStep += 1;
      setNotice(error.message, true);
    } finally {
      inFlight = false;
    }
    schedulePoll();
  }

  function manualRefresh() {
    lastChangeAt = Date.now();
    pollStep = 0;
    setNotice(null);
    refresh();
  }

  function post(path, body) {
    return request(ROOMS_API + "/" + code + path, { method: "POST", token: seat && seat.token, body: body || {} });
  }

  async function act(busy, task) {
    if (Shio.getState().busy) return null;
    Shio.setState({ busy: busy });
    try {
      return await task();
    } catch (error) {
      window.showErrorToast(error.message);
      return null;
    } finally {
      Shio.setState({ busy: null });
    }
  }

  function join() {
    const form = Shio.getState().form;
    const name = (form.name || "").trim();
    if (!name || !form.birth) {
      window.showErrorToast("Isi nama dan tanggal lahirmu dulu.");
      return null;
    }
    return act("join", async () => {
      const data = await request(ROOMS_API + "/" + code + "/join", { method: "POST", body: { name: name, birth_date: form.birth } });
      seat = { token: data.token, slot: data.slot };
      saveSeat(code, seat);
      await refresh();
      return data;
    });
  }

  function pickAnswer(index, option) {
    const answers = (Shio.getState().form.answers || []).slice();
    answers[index] = option;
    Shio.updateForm({ answers: answers });
  }

  function missingAnswer(view) {
    const answers = Shio.getState().form.answers || [];
    for (let index = 0; index < view.questions.length; index += 1) {
      if (typeof answers[index] !== "number") return index;
    }
    return -1;
  }

  function submitAnswers() {
    const view = Shio.getState().room;
    if (!view || !view.questions) return null;
    const missing = missingAnswer(view);
    if (missing !== -1) {
      window.showErrorToast("Soal nomor " + (missing + 1) + " belum dijawab.");
      return null;
    }
    const answers = Shio.getState().form.answers.slice(0, view.questions.length);
    return act("answers", async () => {
      await post("/answers", { answers: answers });
      await refresh();
      return true;
    });
  }

  function start() {
    return act("start", async () => {
      await post("/start");
      await refresh();
      return true;
    });
  }

  function finish() {
    if (Date.now() > finishArmedUntil) {
      finishArmedUntil = Date.now() + FINISH_CONFIRM_MS;
      window.showToast("Klik sekali lagi untuk mengakhiri. Ronde yang belum terjawab dihitung 0 poin.", "info");
      return null;
    }
    finishArmedUntil = 0;
    return act("finish", async () => {
      await post("/finish");
      await refresh();
      return true;
    });
  }

  function guess(round, slot) {
    return act("guess", async () => {
      try {
        const outcome = await post("/guess", { round: round, slot: slot });
        if (outcome.correct) window.showToast("Benar! +" + outcome.points + " poin.", "info");
        else window.showToast("Bukan dia. Satu petunjuk baru terbuka.", "error");
      } finally {
        await refresh();
      }
      return true;
    });
  }

  function roomUrl() {
    return window.location.origin + "/shio/quiz/" + code;
  }

  function copyLink() {
    const url = roomUrl();
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url)
        .then(() => window.showToast("Tautan room tersalin.", "info"))
        .catch(() => window.showToast(url, "info"));
    } else {
      window.showToast(url, "info");
    }
  }

  function shareLink() {
    const text = "Gabung ke room Quiz Shio-ku, kodenya " + code + ": " + roomUrl();
    if (navigator.share) {
      navigator.share({ title: "Quiz Shio Bareng", text: text, url: roomUrl() }).catch(() => {});
      return;
    }
    window.open("https://wa.me/?text=" + encodeURIComponent(text), "_blank", "noopener");
  }

  function describeRoom(view) {
    const parts = [view.mode_title];
    if (view.relation_label) parts.push(view.relation_label);
    if (view.flavor_label) parts.push("Rasa " + view.flavor_label);
    return parts.join(" · ");
  }

  function describeMeta(view) {
    const expires = new Date(view.expires_at);
    const expiry = isNaN(expires.getTime()) ? "" :
      "Berlaku sampai " + expires.toLocaleString("id-ID", { weekday: "long", hour: "2-digit", minute: "2-digit" });
    return view.participant_count + " dari " + view.max_participants + " orang" + (expiry ? " · " + expiry : "");
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
    if (view.turn) return view.turn.finished_players + " dari " + count + " pemain sudah selesai menebak.";
    return "Permainan sedang berjalan.";
  }

  function outsiderNotice(view) {
    if (view.me) return "";
    const canJoin = view.status === "lobby" && view.participant_count < view.max_participants;
    if (canJoin) return "";
    if (view.status !== "done") return "Room ini sudah mulai atau sudah penuh, jadi kamu hanya bisa melihat daftar pesertanya.";
    return "Room ini sudah selesai. Hasilnya hanya bisa dibuka oleh pesertanya.";
  }

  function roomFlags(view) {
    const isHost = Boolean(view.me && view.me.is_host);
    return {
      canJoin: !view.me && view.status === "lobby" && view.participant_count < view.max_participants,
      showLobby: view.status !== "done",
      showStart: isHost && view.mode !== "pasangan" && view.status === "lobby",
      startDisabled: view.participant_count < view.min_participants,
      showFinish: isHost && view.mode === "tebak" && view.status === "playing",
      showQuestions: Boolean(view.me && view.questions),
      showTurn: Boolean(view.turn),
      showResult: view.status === "done" && Boolean(view.result),
    };
  }

  function buildPeople(view) {
    const list = el("ul", "quiz-people");
    view.participants.forEach((person) => {
      const item = el("li", "quiz-person" + (person.is_me ? " is-me" : ""));
      item.appendChild(el("span", "quiz-person-hanzi", person.hanzi || "?"));
      const body = el("div", "quiz-person-body");
      body.appendChild(el("span", "quiz-person-name", person.name));
      const tags = [];
      if (person.shio) tags.push(person.shio);
      if (person.is_host) tags.push("pembuat room");
      if (person.is_me) tags.push("kamu");
      body.appendChild(el("span", "quiz-person-tags", tags.join(" · ")));
      item.appendChild(body);
      if (view.mode === "pasangan") {
        item.appendChild(el("span", "quiz-person-state" + (person.answered ? " done" : ""), person.answered ? "Sudah jawab" : "Belum jawab"));
      }
      list.appendChild(item);
    });
    return list;
  }

  function buildQuestion(question, index, onPick) {
    const fieldset = el("fieldset", "quiz-question-set");
    fieldset.appendChild(el("legend", "quiz-question-text", question.question));
    const picked = (Shio.getState().form.answers || [])[index];
    question.options.forEach((option, optionIndex) => {
      const label = el("label", "quiz-answer");
      const input = document.createElement("input");
      input.type = "radio";
      input.name = "sh-q-" + Shio.activeLayout() + "-" + index;
      input.value = String(optionIndex);
      input.checked = picked === optionIndex;
      input.addEventListener("change", () => {
        pickAnswer(index, optionIndex);
        if (onPick) onPick(index, optionIndex);
      });
      label.appendChild(input);
      label.appendChild(el("span", "quiz-answer-text", option));
      fieldset.appendChild(label);
    });
    return fieldset;
  }

  function buildTurn(view) {
    const turn = view.turn;
    const current = turn.current;
    const box = el("div", "sh-quiz-turn");
    const head = el("div", "quiz-turn-head");
    head.appendChild(el("h2", "quiz-card-title", current ? "Ronde " + current.number + " dari " + turn.total_rounds : "Semua ronde selesai"));
    head.appendChild(el("span", "quiz-points", turn.points + " poin"));
    box.appendChild(head);
    if (!current) {
      box.appendChild(el("p", "quiz-hint", "Kamu menebak benar " + turn.solved_rounds + " dari " + turn.total_rounds +
        " ronde. Hasil keluar begitu semua pemain selesai."));
      return box;
    }
    box.appendChild(el("p", "quiz-hint", "Sifat-sifat ini milik salah satu teman di room. Siapa?"));
    const hints = el("ol", "quiz-hints");
    current.hints.forEach((hint) => hints.appendChild(el("li", "quiz-hint-item", hint)));
    box.appendChild(hints);
    box.appendChild(el("p", "quiz-hint", "Petunjuk " + current.hints.length + " dari " + current.hints_total +
      ". Tiap tebakan salah membuka satu petunjuk lagi dan mengurangi poin."));
    const options = el("div", "quiz-options");
    const busy = Boolean(Shio.getState().busy);
    current.options.forEach((option) => {
      const wrong = current.wrong_slots.indexOf(option.slot) !== -1;
      const button = el("button", "quiz-option" + (wrong ? " wrong" : ""), option.name);
      button.type = "button";
      button.disabled = wrong || busy;
      if (wrong) button.setAttribute("aria-label", option.name + ", tebakan salah");
      button.addEventListener("click", () => guess(current.round, option.slot));
      options.appendChild(button);
    });
    box.appendChild(options);
    return box;
  }

  function participantName(view, slot) {
    const found = view.participants.find((person) => person.slot === slot);
    return found ? found.name : "?";
  }

  function buildVerdict(kicker, verdict, scoreText, lines) {
    const card = el("div", "quiz-card quiz-verdict verdict-" + verdict.key);
    card.appendChild(el("p", "quiz-verdict-kicker", kicker));
    if (scoreText) card.appendChild(el("div", "quiz-score", scoreText));
    card.appendChild(el("h2", "quiz-verdict-title", verdict.title));
    if (verdict.note) card.appendChild(el("p", "quiz-verdict-note", verdict.note));
    if (lines.length) {
      const box = el("div", "quiz-breakdown");
      lines.forEach((line) => {
        const row = el("div", "quiz-breakdown-row");
        row.appendChild(el("span", "quiz-breakdown-label", line[0]));
        row.appendChild(el("span", "quiz-breakdown-value", line[1]));
        box.appendChild(row);
      });
      card.appendChild(box);
    }
    return card;
  }

  function pairItem(pair) {
    const item = el("li", "quiz-pair code-" + pair.code);
    const head = el("div", "quiz-pair-head");
    head.appendChild(el("span", "quiz-pair-names", pair.names.join(" × ")));
    head.appendChild(el("span", "quiz-pair-hanzi", pair.hanzi));
    item.appendChild(head);
    item.appendChild(el("span", "quiz-pair-label", pair.label + " · " + pair.title));
    item.appendChild(el("p", "quiz-pair-note", pair.note));
    return item;
  }

  function pairList(pairs, emptyText) {
    const list = el("ul", "quiz-pairs");
    if (!pairs.length && emptyText) list.appendChild(el("li", "quiz-empty", emptyText));
    pairs.forEach((pair) => list.appendChild(pairItem(pair)));
    return list;
  }

  function personHead(hanzi, name, tags, badge) {
    const head = el("div", "quiz-role-head");
    head.appendChild(el("span", "quiz-person-hanzi", hanzi));
    const body = el("div", "quiz-person-body");
    body.appendChild(el("span", "quiz-person-name", name));
    body.appendChild(el("span", "quiz-person-tags", tags));
    head.appendChild(body);
    head.appendChild(el("span", "quiz-role-title", badge));
    return head;
  }

  function pairResult(view) {
    const result = view.result;
    const name1 = participantName(view, 1);
    const name2 = participantName(view, 2);
    const compare = el("ul", "quiz-compare");
    result.comparisons.forEach((row) => {
      const item = el("li", "quiz-compare-item distance-" + row.distance);
      item.appendChild(el("p", "quiz-compare-question", row.question));
      const answers = el("div", "quiz-compare-answers");
      [[name1, row.answer1], [name2, row.answer2]].forEach((pair) => {
        const line = el("p", "quiz-compare-answer");
        line.appendChild(el("strong", null, pair[0] + ": "));
        line.appendChild(document.createTextNode(pair[1]));
        answers.appendChild(line);
      });
      item.appendChild(answers);
      item.appendChild(el("span", "quiz-compare-badge", row.label));
      compare.appendChild(item);
    });
    return {
      verdict: buildVerdict("Ramalan Pasangan · " + (view.relation_label || "") + " · " + name1 + " & " + name2, result.verdict,
        result.score + "%", [
          ["Relasi shio (" + Math.round(result.weights.shio * 100) + "%)", result.shio_score + "%"],
          ["Kecocokan jawaban (" + Math.round(result.weights.answers * 100) + "%)", result.answer_score + "%"],
        ]),
      sections: [{ key: "compare", title: "Jawaban Kalian", icon: "fa-scale-balanced", node: compare }],
      compat: result.compatibility,
    };
  }

  function groupResult(view) {
    const result = view.result;
    const counts = result.counts;
    const roles = el("ul", "quiz-roles");
    result.members.forEach((member) => {
      const item = el("li", "quiz-role role-" + member.role_key);
      item.appendChild(personHead(member.hanzi, member.name, member.shio, member.role_title));
      item.appendChild(el("p", "quiz-role-note", member.role_note));
      item.appendChild(el("p", "quiz-role-tally", member.good + " harmonis · " + member.bad + " gesekan · " + member.neutral + " netral"));
      roles.appendChild(item);
    });
    const sections = [{ key: "roles", title: "Peran di Geng", icon: "fa-masks-theater", node: roles }];
    if (result.triads.length) {
      const triads = el("ul", "quiz-pairs");
      result.triads.forEach((triad) => {
        const item = el("li", "quiz-pair code-good");
        item.appendChild(el("span", "quiz-pair-names", triad.names.join(", ")));
        item.appendChild(el("p", "quiz-pair-note", "Satu segitiga tiga harmoni berelemen " + triad.element + " (" +
          triad.element_hanzi + "). Kalau mereka bertiga satu tim, arahnya gampang kompak."));
        triads.appendChild(item);
      });
      sections.push({ key: "triads", title: "Tiga Serangkai (三合)", icon: "fa-circle-nodes", node: triads });
    }
    sections.push({ key: "best", title: "Paling Klop", icon: "fa-link", node: pairList(result.best_pairs, "Tidak ada pasangan 六合 atau 三合 di kelompok ini.") });
    sections.push({ key: "tense", title: "Paling Rawan Gesekan", icon: "fa-bolt", node: pairList(result.tense_pairs, "Tidak ada benturan cabang di kelompok ini.") });
    sections.push({ key: "all", title: "Semua " + result.pairs.length + " pasangan", icon: "fa-list", node: pairList(result.pairs, ""), collapsed: true });
    return {
      verdict: buildVerdict("Ramalan Kelompok · " + result.members.length + " orang", result.verdict, "", [
        ["Ikatan harmonis", counts.good + " pasangan"],
        ["Rawan gesekan", counts.bad + " pasangan"],
        ["Netral", counts.neutral + " pasangan"],
      ]),
      sections: sections,
      note: result.note,
      compat: null,
    };
  }

  function guessResult(view) {
    const result = view.result;
    const mine = view.me ? result.targets.find((target) => target.slot === view.me.slot) : null;
    const leader = result.leaderboard[0];
    const verdict = mine
      ? buildVerdict("Tebak Shio Teman · tentang kamu", mine.verdict, mine.readability + "%", [["Skor maksimal per pemain", result.max_points + " poin"]])
      : buildVerdict("Tebak Shio Teman", { key: "terbaca", title: "Juara: " + leader.name, note: "" }, "", [["Skor maksimal per pemain", result.max_points + " poin"]]);
    const board = el("ol", "quiz-leaderboard");
    result.leaderboard.forEach((row) => {
      const item = el("li", "quiz-leader");
      item.appendChild(el("span", "quiz-leader-name", row.name));
      item.appendChild(el("span", "quiz-leader-points", row.points + " poin · " + row.solved + " benar"));
      board.appendChild(item);
    });
    const targets = el("ul", "quiz-targets");
    result.targets.slice().sort((a, b) => b.readability - a.readability).forEach((target) => {
      const item = el("li", "quiz-target verdict-" + target.verdict.key);
      item.appendChild(personHead(target.hanzi, target.name, "Shio " + target.shio, target.readability + "%"));
      item.appendChild(el("p", "quiz-role-note", target.verdict.title + " — " + target.verdict.note));
      const details = el("details", "quiz-target-hints");
      details.appendChild(el("summary", null, "Petunjuk yang dipakai"));
      const hints = el("ol", "quiz-hints");
      target.hints.forEach((hint) => hints.appendChild(el("li", "quiz-hint-item", hint)));
      details.appendChild(hints);
      item.appendChild(details);
      targets.appendChild(item);
    });
    return {
      verdict: verdict,
      sections: [
        { key: "leaderboard", title: "Papan Skor Penebak", icon: "fa-ranking-star", node: board },
        { key: "targets", title: "Siapa Paling Gampang Ditebak", icon: "fa-user-secret", node: targets },
      ],
      compat: null,
    };
  }

  function buildResult(view) {
    if (view.mode === "pasangan") return pairResult(view);
    if (view.mode === "kelompok") return groupResult(view);
    return guessResult(view);
  }

  Shio.onBoot((app) => {
    if (app.dataset.page !== "juhui-fangjian") return;
    code = app.dataset.roomCode;
    seat = loadSeat(code);
    Shio.setState({ room: null, notice: null, busy: null, missing: false });
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) {
        clearTimeout(pollTimer);
        pollTimer = null;
        return;
      }
      const view = Shio.getState().room;
      if (view && view.status !== "done") {
        pollStep = 0;
        refresh();
      }
    });
    refresh();
  });

  Shio.quizRoom = {
    join: join,
    pickAnswer: pickAnswer,
    missingAnswer: missingAnswer,
    submitAnswers: submitAnswers,
    start: start,
    finish: finish,
    copyLink: copyLink,
    shareLink: shareLink,
    manualRefresh: manualRefresh,
    describeRoom: describeRoom,
    describeMeta: describeMeta,
    describeLobby: describeLobby,
    outsiderNotice: outsiderNotice,
    roomFlags: roomFlags,
    buildPeople: buildPeople,
    buildQuestion: buildQuestion,
    buildTurn: buildTurn,
    buildResult: buildResult,
  };
})(window.Shio);
