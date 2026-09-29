(function () {
  const MOBILE_QUERY = "(max-width: 768px)";
  const MONTHS = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
  ];
  const renderers = {};
  const listeners = new Set();
  let state = {
    form: {},
    result: null,
    loading: false,
    error: "",
  };
  let activeLayout = null;
  let glossary = {};

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

  function initDate(input, onPick) {
    window.initDatePicker("#" + input.id, {
      dateFormat: "Y-m-d",
      altInput: true,
      altFormat: "j F Y",
      locale: "id",
      minDate: input.dataset.min,
      maxDate: input.dataset.max,
      disableMobile: true,
      onChange: (dates, str) => onPick(str),
    });
    return input._flatpickr || null;
  }

  function syncPicker(picker, input, value) {
    if (!picker) {
      input.value = value || "";
      return;
    }
    if (value) picker.setDate(value, false);
    else picker.clear(false);
  }

  function bindInputs(fields) {
    Object.entries(fields).forEach(([key, node]) => {
      node.addEventListener("input", () => updateForm({ [key]: node.value }));
    });
  }

  function syncInputs(fields, form) {
    Object.entries(fields).forEach(([key, node]) => {
      node.value = form[key] || "";
      refreshTimeClear(node);
    });
  }

  const timeClearRefreshers = new WeakMap();

  function refreshTimeClear(input) {
    const refresh = timeClearRefreshers.get(input);
    if (refresh) refresh();
  }

  function setupTimeClear(root) {
    root.querySelectorAll('input[type="time"]').forEach((input) => {
      const wrap = el("span", "wt-time");
      input.parentNode.insertBefore(wrap, input);
      wrap.appendChild(input);
      const button = el("button", "wt-time-clear");
      button.type = "button";
      button.setAttribute("aria-label", "Hapus jam lahir");
      const mark = el("i", "fa-solid fa-xmark");
      mark.setAttribute("aria-hidden", "true");
      button.appendChild(mark);
      wrap.appendChild(button);
      const refresh = () => {
        button.hidden = !input.value;
      };
      input.addEventListener("input", refresh);
      input.addEventListener("change", refresh);
      button.addEventListener("click", () => {
        input.value = "";
        input.dispatchEvent(new Event("input", { bubbles: true }));
        input.focus();
      });
      timeClearRefreshers.set(input, refresh);
      refresh();
    });
  }

  function renderStepper(nodes, step, total) {
    nodes.steps.forEach((node) => {
      node.hidden = Number(node.dataset.step) !== step;
    });
    nodes.progressText.textContent = "Langkah " + step + " dari " + total;
    nodes.progressFill.style.width = (step / total) * 100 + "%";
    nodes.back.hidden = step === 1;
  }

  function cardHeader(iconName, label) {
    const header = el("header", "wt-result-head");
    const icon = el("i", "fa-solid " + iconName + " wt-result-icon");
    icon.setAttribute("aria-hidden", "true");
    header.appendChild(icon);
    header.appendChild(label);
    return header;
  }

  function adviceBlock(title, inti, saran) {
    const block = el("div", "wt-watak");
    if (title) block.appendChild(el("h4", "wt-watak-title", title));
    block.appendChild(el("p", "wt-watak-inti", inti));
    const advice = el("p", "wt-watak-saran");
    advice.appendChild(el("strong", null, "Saran: "));
    advice.appendChild(document.createTextNode(saran));
    block.appendChild(advice);
    return block;
  }

  function factsList(rows) {
    const list = el("dl", "wt-facts");
    rows.forEach((fact) => {
      const row = el("div", "wt-fact");
      row.appendChild(el("dt", null, fact[0]));
      row.appendChild(el("dd", null, fact[1]));
      list.appendChild(row);
    });
    return list;
  }

  function neptuFormula(weton) {
    return "Neptu " + weton.neptu + " = " + weton.hari + " " + weton.neptu_hari + " + " +
      weton.pasaran + " " + weton.neptu_pasaran;
  }

  function roastError(form) {
    if (!form.a_tanggal) return "Isi tanggal lahirmu dulu.";
    if (form.duo && !form.b_tanggal) return "Isi tanggal lahir orang kedua dulu, atau matikan opsi orang kedua.";
    return "";
  }

  function formatShortDate(iso) {
    const [year, month, day] = iso.split("-").map(Number);
    return day + " " + MONTHS[month - 1].slice(0, 3) + " " + year;
  }

  async function submit() {
    if (state.loading) return false;
    const app = document.getElementById("wt-app");
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
    setState({ result: null, error: "" });
  }

  function freshForm(form) {
    const app = byId("wt-app");
    const next = {};
    if (form.lens) next.lens = form.lens;
    if (form.hajat) {
      next.hajat = form.hajat;
      next.dari = app.dataset.defaultStart;
      next.sampai = app.dataset.defaultEnd;
    }
    return next;
  }

  function focusResult(node) {
    if (!node) return;
    if (!node.hasAttribute("tabindex")) node.setAttribute("tabindex", "-1");
    node.classList.add("wt-result-target");
    const behavior = window.prefersReducedMotion() ? "auto" : "smooth";
    if (activeLayout === "mobile") window.scrollTo({ top: 0, behavior: behavior });
    else node.scrollIntoView({ behavior: behavior, block: "start" });
    node.focus({ preventScroll: true });
  }

  function showResult(node) {
    state = Object.assign({}, state, { submitted: state.form, form: freshForm(state.form) });
    if (activeLayout && renderers[activeLayout]) renderers[activeLayout].activate(state);
    focusResult(node);
  }

  function patchResult(patch) {
    if (!state.result) return;
    setState({ result: Object.assign({}, state.result, patch) });
  }

  function calendarGo(target) {
    updateForm({ bulan: target.bulan || "", tanggal: target.tanggal || "" });
    return submit();
  }

  function buildLahirCards(result) {
    const weton = result.weton;
    const jawa = result.jawa;
    const wuku = result.wuku;
    const mangsa = result.mangsa;
    const watak = result.watak;
    return [
      {
        key: "weton",
        icon: "fa-seedling",
        title: "Weton & Neptu",
        term: "neptu",
        headline: weton.label,
        sub: neptuFormula(weton),
        facts: [
          ["Hari Jawa", weton.hari_jawa],
          ["Paarasan", result.paarasan],
        ],
        items: [],
      },
      {
        key: "wuku",
        icon: "fa-circle-nodes",
        title: "Wuku",
        term: "wuku",
        headline: wuku.name,
        sub: "Wuku ke-" + wuku.number + " dari 30 · hari ke-" + wuku.day_in_wuku,
        facts: [["Dewa pelindung", wuku.dewa], ["Pohon lambang", wuku.kayu], ["Burung lambang", wuku.burung || "Tidak ada"]]
          .filter((fact) => fact[1]),
        items: [watak.wuku],
      },
      {
        key: "jawa",
        icon: "fa-moon",
        title: "Tanggal Jawa",
        term: "kurup",
        headline: jawa.tanggal + " " + jawa.sasi + " " + jawa.tahun,
        sub: "Tahun " + jawa.taun + " · Windu " + jawa.windu,
        facts: [
          ["Kurup", jawa.kurup + " (" + jawa.kurup_long + ")"],
          ["Panjang tahun", jawa.year_length + " hari"],
        ],
        items: [],
      },
      {
        key: "mangsa",
        icon: "fa-cloud-sun-rain",
        title: "Pranata Mangsa",
        term: "mangsa",
        headline: "Mangsa " + mangsa.name,
        sub: mangsa.sanskrit + " · " + formatShortDate(mangsa.start) + " – " + formatShortDate(mangsa.end),
        facts: [
          ["Candra", mangsa.candra],
          ["Artinya", mangsa.arti],
          ["Tanda alam", mangsa.tanda],
          ["Kegiatan tani", mangsa.tani],
        ].filter((fact) => fact[1]),
        items: [],
      },
      {
        key: "watak",
        icon: "fa-user-astronaut",
        title: "Watak",
        term: "weton",
        headline: "Watak " + weton.label,
        sub: "Gabungan watak hari, pasaran, dan jumlah neptu",
        facts: [],
        items: [watak.hari, watak.pasaran, watak.neptu],
      },
      {
        key: "laku",
        icon: "fa-person-walking",
        title: "Laku",
        term: "paarasan",
        headline: result.paarasan,
        sub: "Menurut jumlah neptu " + weton.neptu,
        facts: [],
        items: [watak.paarasan],
      },
      {
        key: "karier",
        icon: "fa-briefcase",
        title: "Karier",
        term: "neptu",
        headline: "Gaya kerja " + weton.label,
        sub: result.karier.note,
        facts: [],
        items: [result.karier.hari, result.karier.pasaran, result.karier.neptu],
      },
    ];
  }

  function renderCard(card, variant) {
    const article = el("article", "wt-card wt-result-card wt-card-" + card.key);
    const label = el("p", "wt-result-label");
    if (variant === "desktop" && glossary[card.term]) {
      const term = el("span", "wt-term", card.title);
      term.tabIndex = 0;
      term.dataset.tip = glossary[card.term];
      label.appendChild(term);
    } else {
      label.textContent = card.title;
    }
    article.appendChild(cardHeader(card.icon, label));
    article.appendChild(el("h3", "wt-result-headline", card.headline));
    if (card.sub) article.appendChild(el("p", "wt-result-sub", card.sub));
    if (card.facts.length) article.appendChild(factsList(card.facts));
    card.items.forEach((item) => article.appendChild(adviceBlock(item.title, item.inti, item.saran)));
    if (variant === "mobile" && glossary[card.term]) {
      const details = el("details", "wt-glossary");
      details.appendChild(el("summary", null, "Apa itu " + card.term + "?"));
      details.appendChild(el("p", null, glossary[card.term]));
      article.appendChild(details);
    }
    return article;
  }

  function describeSources(result) {
    const sources = result.sources || {};
    return "Sumber hitungan dan tafsir: " + Object.values(sources).join("; ") + ".";
  }

  const PAYLOAD_BUILDERS = {
    kecocokan: (form) => ({
      lens: form.lens,
      a: { nama: form.a_nama, tanggal: form.a_tanggal, jam: form.a_jam, kota: form.a_kota },
      b: { nama: form.b_nama, tanggal: form.b_tanggal, jam: form.b_jam, kota: form.b_kota },
    }),
    kalender: (form) => {
      const payload = {};
      if (form.tanggal) payload.tanggal = form.tanggal;
      else if (form.bulan) payload.bulan = form.bulan;
      if (form.lahir_tanggal) {
        payload.lahir = { tanggal: form.lahir_tanggal, jam: form.lahir_jam, kota: form.lahir_kota };
      }
      return payload;
    },
    roasting: (form) => {
      const payload = {
        a: { nama: form.a_nama, tanggal: form.a_tanggal, jam: form.a_jam, kota: form.a_kota },
      };
      if (form.duo && form.b_tanggal) {
        payload.b = { nama: form.b_nama, tanggal: form.b_tanggal, jam: form.b_jam, kota: form.b_kota };
      }
      return payload;
    },
    dinabecik: (form) => {
      const payload = { hajat: form.hajat, dari: form.dari, sampai: form.sampai };
      if (form.a_tanggal) payload.a = { tanggal: form.a_tanggal, jam: form.a_jam, kota: form.a_kota };
      return payload;
    },
  };

  function findDay(result, iso) {
    return result.days.find((day) => day.date === iso) || result.days[0];
  }

  function dayMarks(day) {
    const marks = [];
    if (day.istimewa.length) marks.push("istimewa");
    if (day.pantangan.length) marks.push("pantangan");
    if (day.wetonan) marks.push("wetonan");
    return marks;
  }

  function renderMarks(day) {
    const wrap = el("span", "wt-cal-marks");
    wrap.setAttribute("aria-hidden", "true");
    dayMarks(day).forEach((mark) => wrap.appendChild(el("span", "wt-mark wt-mark-" + mark)));
    return wrap;
  }

  function describeDayForLabel(result, day) {
    const parts = [day.label, day.weton.label, day.jawa.tanggal + " " + day.jawa.sasi];
    day.istimewa.forEach((key) => parts.push(result.istimewa_info[key].name));
    day.pantangan.forEach((item) => parts.push(result.pantangan_info[item.key].name));
    if (day.wetonan) parts.push("wetonanmu");
    if (day.today) parts.push("hari ini");
    return parts.join(", ");
  }

  function renderNoteBlock(title, inti, saran, extra) {
    const block = adviceBlock(title, inti, saran);
    if (extra) block.appendChild(el("p", "wt-cal-source", extra));
    return block;
  }

  function renderDayDetail(result, iso) {
    const day = findDay(result, iso);
    const weton = day.weton;
    const jawa = day.jawa;
    const wuku = day.wuku;
    const mangsa = result.mangsa[day.mangsa];
    const keblat = result.keblat[weton.pasaran_key];
    const article = el("article", "wt-card wt-result-card wt-cal-detail");
    article.appendChild(cardHeader("fa-calendar-day", el("p", "wt-result-label", day.label + (day.today ? " · hari ini" : ""))));
    article.appendChild(el("h3", "wt-result-headline", weton.label));
    article.appendChild(el("p", "wt-result-sub", neptuFormula(weton)));
    const badges = el("div", "wt-cal-badges");
    day.istimewa.forEach((key) => badges.appendChild(el("span", "wt-badge wt-badge-istimewa", result.istimewa_info[key].name)));
    day.pantangan.forEach((item) => badges.appendChild(el("span", "wt-badge wt-badge-pantangan", result.pantangan_info[item.key].name)));
    if (day.wetonan) badges.appendChild(el("span", "wt-badge wt-badge-wetonan", "Wetonanmu"));
    if (badges.children.length) article.appendChild(badges);
    const lambang = [wuku.kayu && "kayu " + wuku.kayu, "burung " + (wuku.burung || "tidak ada")].filter(Boolean).join(" · ");
    article.appendChild(factsList([
      ["Tanggal Jawa", jawa.tanggal + " " + jawa.sasi + " " + jawa.tahun + " · tahun " + jawa.taun + ", windu " + jawa.windu],
      ["Wuku", wuku.name + " (ke-" + wuku.number + ") · dewa " + wuku.dewa],
      ["Lambang wuku", lambang],
      ["Hari Jawa", weton.hari_jawa],
      ["Arah pasaran", keblat.arah + " · warna " + keblat.warna],
      ["Pranata mangsa", "Mangsa " + mangsa.name + " (" + mangsa.sanskrit + ")"],
      ["Artinya", mangsa.arti],
      ["Tanda alam", mangsa.tanda],
    ].filter((fact) => fact[1])));
    day.istimewa.forEach((key) => {
      const info = result.istimewa_info[key];
      article.appendChild(renderNoteBlock(info.name, info.inti, info.saran, "Sumber: " + info.source));
    });
    day.pantangan.forEach((item) => {
      const info = result.pantangan_info[item.key];
      article.appendChild(renderNoteBlock(
        info.name + " (" + info.arti + ")", info.inti, info.saran, "Tercatat " + item.basis_label + ".",
      ));
    });
    if (!day.istimewa.length && !day.pantangan.length) {
      article.appendChild(el("p", "wt-cal-plain",
        "Hari biasa: tidak ada catatan hari istimewa atau pantangan di tabel primbon yang kami pakai."));
    }
    return article;
  }

  function renderWetonanSummary(wetonan) {
    const wrap = el("div", "wt-wetonan-summary");
    wrap.appendChild(el("p", "wt-wetonan-headline", "Wetonmu " + wetonan.weton.label + " (neptu " + wetonan.weton.neptu + ")"));
    if (wetonan.next) {
      const when = wetonan.next.days === 0 ? "hari ini" : wetonan.next.label + " (" + wetonan.next.days + " hari lagi)";
      wrap.appendChild(el("p", "wt-result-sub", "Wetonan berikutnya: " + when + "."));
    }
    const note = el("p", "wt-duo-note", wetonan.maghrib.text);
    note.dataset.kind = wetonan.maghrib.kind;
    wrap.appendChild(note);
    wrap.appendChild(el("p", "wt-hint", wetonan.note));
    return wrap;
  }

  function renderDuo(result) {
    const wrap = el("div", "wt-duo");
    result.people.forEach((person, index) => {
      if (index === 1) {
        const total = el("div", "wt-duo-total");
        total.appendChild(el("span", "wt-duo-total-label", "Total neptu"));
        total.appendChild(el("strong", "wt-duo-total-value", String(result.total_neptu)));
        total.appendChild(el("span", "wt-duo-total-formula", result.total_formula));
        wrap.appendChild(total);
      }
      const card = el("article", "wt-card wt-duo-person");
      card.appendChild(el("p", "wt-result-label", person.nama));
      card.appendChild(el("h3", "wt-result-headline", person.weton.label));
      card.appendChild(el("p", "wt-result-sub", "Neptu " + person.weton.neptu + " · lahir " + person.input.tanggal_label));
      const note = el("p", "wt-duo-note", person.maghrib.text);
      note.dataset.kind = person.maghrib.kind;
      card.appendChild(note);
      wrap.appendChild(card);
    });
    return wrap;
  }

  function renderPetungCard(item) {
    const result = item.result;
    const article = el("article", "wt-card wt-result-card wt-petung-card");
    article.appendChild(cardHeader("fa-scale-balanced", el("p", "wt-result-label", item.name)));
    const title = el("div", "wt-petung-title");
    title.appendChild(el("h3", "wt-result-headline", result.name));
    title.appendChild(el("span", "wt-tone wt-tone-" + result.tone, result.tone_label));
    article.appendChild(title);
    article.appendChild(el("p", "wt-result-sub", item.formula + " → " + result.name));
    article.appendChild(adviceBlock(null, result.inti, result.saran));
    article.appendChild(factsList([["Makna klasik", result.meaning], ["Sumber", item.source]]));
    return article;
  }

  const calendar = {
    renderHeader(els, state) {
      const result = state.result;
      showError(els.error, state.error);
      window.setButtonLoading(els.submit, state.loading && Boolean(state.form.lahir_tanggal), "Menandai...");
      if (!result) return false;
      els.month.textContent = result.month.label;
      els.jawa.textContent = result.month.jawa_label;
      els.prev.disabled = !result.month.prev;
      els.next.disabled = !result.month.next;
      return true;
    },
    renderFooter(els, result) {
      const wetonan = result.wetonan;
      els.summary.hidden = !wetonan;
      els.clear.hidden = !wetonan;
      clear(els.summary);
      if (wetonan) els.summary.appendChild(renderWetonanSummary(wetonan));
      els.note.textContent = result.note;
      els.disclaimer.textContent = result.disclaimer + " Sumber: " + Object.values(result.sources).join("; ") + ".";
    },
    bindNav(els, selectDay) {
      [[els.prev, "prev"], [els.next, "next"]].forEach(([button, key]) => {
        button.addEventListener("click", () => {
          if (state.result && state.result.month[key]) calendarGo({ bulan: state.result.month[key] });
        });
      });
      els.today.addEventListener("click", () => {
        const result = state.result;
        if (result && result.days.some((day) => day.date === result.today)) {
          selectDay(result.today);
          return;
        }
        calendarGo({ tanggal: result ? result.today : "" });
      });
    },
    submitWetonan(els) {
      if (!state.form.lahir_tanggal) {
        showError(els.error, "Isi tanggal lahir dulu.");
        return;
      }
      calendarGo({ tanggal: state.result ? state.result.selected : "" });
    },
    clearWetonan(afterReset) {
      updateForm({ lahir_tanggal: "", lahir_jam: "", lahir_kota: "" });
      afterReset(state.form);
      calendarGo({ tanggal: state.result ? state.result.selected : "" });
    },
  };

  function applyLayout(app, media) {
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

  function readJsonScript(id) {
    const node = document.getElementById(id);
    if (!node) return null;
    try {
      return JSON.parse(node.textContent);
    } catch (error) {
      return null;
    }
  }

  function duoLabel(result) {
    return "Kamu × " + result.duo.partner.nama + " · " + result.duo.petung.result_name;
  }

  function roastSlides(result) {
    const slides = result.roasts.map((text) => ({ group: "solo", label: "Roast " + result.person.weton.label, text: text }));
    if (result.duo) {
      result.duo.roasts.forEach((text) => slides.push({ group: "duo", label: duoLabel(result), text: text }));
    }
    return slides;
  }

  function dinaDefaults(app) {
    if (state.form.hajat) return;
    updateForm({
      hajat: app.dataset.defaultHajat,
      dari: app.dataset.defaultStart,
      sampai: app.dataset.defaultEnd,
    });
  }

  function dinaError(form) {
    if (!form.dari || !form.sampai) return "Pilih tanggal awal dan akhir dulu.";
    if (form.sampai < form.dari) return "Tanggal akhir harus sama dengan atau sesudah tanggal awal.";
    return "";
  }

  function buildDinaItem(day) {
    const article = el("article", "wt-card wt-result-card wt-dina-item wt-dina-item-" + day.status);
    const icon = day.status === "hindari" ? "fa-ban" : "fa-calendar-check";
    article.appendChild(cardHeader(icon, el("p", "wt-result-label", day.label + (day.today ? " · hari ini" : ""))));
    article.appendChild(el("h3", "wt-result-headline", day.weton.label));
    article.appendChild(el("p", "wt-result-sub",
      day.jawa.tanggal + " " + day.jawa.sasi + " " + day.jawa.tahun + " · wuku " + day.wuku + " · neptu " + day.weton.neptu));
    const chips = el("div", "wt-cal-badges");
    chips.appendChild(el("span", "wt-tone wt-tone-" + day.tone, day.tone_label));
    day.reasons.forEach((reason) => {
      if (reason.kind !== "bebas" || day.tone !== "aman") {
        chips.appendChild(el("span", "wt-tone wt-tone-" + reason.tone, reason.label));
      }
    });
    article.appendChild(chips);
    const details = day.reasons.filter((reason) => reason.text).map((reason) => [reason.label, reason.text]);
    if (details.length) article.appendChild(factsList(details));
    const link = el("a", "wt-dina-link", "Lihat di kalender ");
    link.href = document.getElementById("wt-app").dataset.calendarUrl + "?tanggal=" + day.date;
    const arrow = el("i", "fa-solid fa-arrow-right");
    arrow.setAttribute("aria-hidden", "true");
    link.appendChild(arrow);
    article.appendChild(link);
    return article;
  }

  function dinaTitle(result) {
    const count = result.recommended.length;
    if (!count) return "Belum ada hari yang pas";
    return count + " hari paling pas buat " + result.hajat.label.toLowerCase();
  }

  function renderDina(els, result) {
    els.basis.textContent = result.hajat.inti + " " + result.hajat.saran;
    const person = result.people[0];
    els.maghrib.hidden = !person;
    if (person) {
      els.maghrib.textContent = "Wetonmu " + person.weton.label + " (neptu " + person.weton.neptu + "). " + person.maghrib.text;
      els.maghrib.dataset.kind = person.maghrib.kind;
    }
    clear(els.sasi);
    result.sasi_notes.forEach((note) => {
      const line = el("p", "wt-note", "Sasi " + note.sasi + " (" + note.days + " hari di rentang ini): " + note.text);
      line.dataset.kind = note.tone;
      els.sasi.appendChild(line);
    });
    if (result.petung_hint) {
      const hint = el("p", "wt-note", result.petung_hint);
      hint.dataset.kind = "after";
      els.sasi.appendChild(hint);
    }
    els.none.hidden = result.recommended.length > 0;
    els.none.textContent = "Tidak ada hari yang lolos di rentang " + result.range.label +
      ". Coba geser atau lebarkan rentang tanggalnya.";
    clear(els.recommended);
    result.recommended.forEach((day) => els.recommended.appendChild(buildDinaItem(day)));
    els.avoidWrap.hidden = !result.avoid.length;
    els.avoidTitle.textContent = "Sebaiknya dihindari (" + result.avoid.length + " hari)";
    clear(els.avoid);
    result.avoid.forEach((day) => els.avoid.appendChild(buildDinaItem(day)));
    els.note.textContent = result.note;
    els.disclaimer.textContent = result.disclaimer + " Sumber: " + Object.values(result.sources).join("; ") + ".";
  }

  function boot() {
    const app = document.getElementById("wt-app");
    if (!app) return;
    glossary = readJsonScript("wt-glossary") || {};
    const initial = readJsonScript("wt-initial");
    if (initial) state = Object.assign({}, state, { result: initial });
    setupTimeClear(app);
    Object.keys(renderers).forEach((name) => {
      const root = app.querySelector('[data-layout="' + name + '"]');
      if (root) renderers[name].init(root);
    });
    listeners.add((next) => {
      if (activeLayout && renderers[activeLayout]) renderers[activeLayout].render(next);
    });
    const media = window.matchMedia(MOBILE_QUERY);
    media.addEventListener("change", () => applyLayout(app, media));
    applyLayout(app, media);
  }

  window.Weton = {
    getState: getState,
    updateForm: updateForm,
    submit: submit,
    reset: reset,
    showResult: showResult,
    patchResult: patchResult,
    calendarGo: calendarGo,
    renderMarks: renderMarks,
    describeDayForLabel: describeDayForLabel,
    renderDayDetail: renderDayDetail,
    renderWetonanSummary: renderWetonanSummary,
    duoLabel: duoLabel,
    roastSlides: roastSlides,
    registerRenderer: registerRenderer,
    buildLahirCards: buildLahirCards,
    renderCard: renderCard,
    describeSources: describeSources,
    renderDuo: renderDuo,
    renderPetungCard: renderPetungCard,
    el: el,
    clear: clear,
    byId: byId,
    showError: showError,
    initDate: initDate,
    syncPicker: syncPicker,
    bindInputs: bindInputs,
    syncInputs: syncInputs,
    renderStepper: renderStepper,
    roastError: roastError,
    calendar: calendar,
    dinaDefaults: dinaDefaults,
    dinaError: dinaError,
    dinaTitle: dinaTitle,
    buildDinaItem: buildDinaItem,
    renderDina: renderDina,
  };

  document.addEventListener("DOMContentLoaded", boot);
})();
