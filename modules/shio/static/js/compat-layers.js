(function () {
  function clearNode(node) {
    while (node.firstChild) node.removeChild(node.firstChild);
  }

  function makeEl(tag, className, text) {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (text !== undefined && text !== null) el.textContent = text;
    return el;
  }

  function buildYearCard(card, side) {
    clearNode(card);
    const head = makeEl("div", "year-head");
    head.appendChild(makeEl("span", "year-pillar", side.pillar_hanzi));
    const meta = document.createElement("div");
    meta.appendChild(makeEl("span", "dyn-name", side.shio_name));
    meta.appendChild(
      makeEl("span", "dyn-element", side.nayin.hanzi + " · " + side.nayin.name)
    );
    head.appendChild(meta);
    card.appendChild(head);
    card.appendChild(makeEl("p", "dyn-summary", side.nayin_relation.text));
  }

  function renderYearLayer(layer) {
    const box = document.getElementById("c-year");
    if (!layer) {
      box.classList.add("hidden");
      return;
    }
    document.getElementById("c-year-lichun").textContent = layer.lichun_note;
    const stem = document.getElementById("c-year-stem");
    clearNode(stem);
    stem.className = "compat-year-stem kind-" + layer.stem_relation.kind;
    stem.appendChild(
      makeEl("span", "dyn-badge", layer.stem_relation.hanzi + " · " + layer.stem_relation.label)
    );
    stem.appendChild(makeEl("p", "dyn-summary", layer.stem_relation.text));
    buildYearCard(document.getElementById("c-year-1"), layer.shio1);
    buildYearCard(document.getElementById("c-year-2"), layer.shio2);
    box.classList.remove("hidden");
  }

  function buildDynamicCard(card, side) {
    clearNode(card);
    card.className = "compat-dynamic-card role-" + side.role;
    const head = makeEl("div", "dyn-head");
    head.appendChild(makeEl("span", "dyn-icon", side.icon));
    const meta = document.createElement("div");
    const title = side.person
      ? side.person + " · " + side.shio + " " + side.hanzi
      : side.shio + " " + side.hanzi;
    meta.appendChild(makeEl("span", "dyn-name", title));
    meta.appendChild(makeEl("span", "dyn-element", side.element + " " + side.element_hanzi));
    head.appendChild(meta);
    card.appendChild(head);
    card.appendChild(makeEl("span", "dyn-badge", side.label));
    card.appendChild(makeEl("p", "dyn-summary", side.summary));
    card.appendChild(makeEl("p", "dyn-advice", side.advice));
  }

  function renderElementDynamic(dynamic) {
    const box = document.getElementById("c-dynamic");
    if (!dynamic) {
      box.classList.add("hidden");
      return;
    }
    const arrow = document.getElementById("c-dyn-arrow");
    buildDynamicCard(document.getElementById("c-dyn-1"), dynamic.for_shio1);
    buildDynamicCard(document.getElementById("c-dyn-2"), dynamic.for_shio2);
    arrow.textContent = dynamic.for_shio1.arrow;
    arrow.classList.toggle("symmetric", dynamic.symmetric);
    box.classList.remove("hidden");
  }

  function renderRelationBadge(relation, fallbackLabel) {
    const box = document.getElementById("c-relation-badge");
    const plain = document.getElementById("c-relationship");
    if (!relation) {
      box.classList.add("hidden");
      plain.textContent = fallbackLabel || "Data belum tersedia";
      plain.classList.remove("hidden");
      return;
    }
    plain.textContent = "";
    plain.classList.add("hidden");
    box.className = "compat-relation-badge code-" + relation.code;
    document.getElementById("c-relation-hanzi").textContent = relation.hanzi;
    document.getElementById("c-relation-title").textContent =
      relation.label + " · " + relation.title;
    document.getElementById("c-relation-note").textContent = relation.note;
  }

  function renderDayPillar(pillar) {
    const box = document.getElementById("c-day-pillar");
    clearNode(box);
    box.className = "compat-day-pillar code-" + pillar.code;
    const head = makeEl("div", "bazi-head");
    head.appendChild(makeEl("span", "bazi-pillar", pillar.pillar1));
    head.appendChild(makeEl("span", "bazi-link", pillar.hanzi));
    head.appendChild(makeEl("span", "bazi-pillar", pillar.pillar2));
    box.appendChild(head);
    box.appendChild(makeEl("span", "dyn-badge", pillar.label + " · " + pillar.title));
    box.appendChild(makeEl("p", "dyn-summary", pillar.text));
    box.appendChild(makeEl("p", "bazi-stem kind-" + pillar.stem_kind, pillar.stem_text));
  }

  function buildUsefulSide(side, layer) {
    const card = makeEl("div", "useful-side");
    card.appendChild(makeEl("span", "useful-side-name", side.label + " · " + side.pillar));
    card.appendChild(
      makeEl("span", "useful-side-element", "Elemen diri " + side.element + " " + side.element_hanzi)
    );
    card.appendChild(makeEl("span", "useful-side-needs", "Butuh " + side.needs.join(" & ")));
    let flag;
    if (side.supplies) {
      flag = makeEl("span", "useful-flag give", layer.supply_label);
    } else if (side.burdens) {
      flag = makeEl("span", "useful-flag drain", layer.burden_label);
    } else {
      flag = makeEl("span", "useful-flag flat", "Tidak menambah, tidak mengurangi");
    }
    card.appendChild(flag);
    return card;
  }

  function renderUsefulGod(match, layer) {
    const box = document.getElementById("c-useful");
    clearNode(box);
    box.className = "compat-useful code-" + match.code;
    const head = makeEl("div", "useful-head");
    head.appendChild(makeEl("span", "useful-glyph", "用神"));
    head.appendChild(makeEl("span", "useful-title", match.title));
    box.appendChild(head);
    box.appendChild(makeEl("p", "dyn-summary", match.note));
    const grid = makeEl("div", "useful-grid");
    grid.appendChild(buildUsefulSide(match.side1, layer));
    grid.appendChild(buildUsefulSide(match.side2, layer));
    box.appendChild(grid);
    box.appendChild(makeEl("p", "dyn-advice", match.advice));
  }

  function renderCoupleStars(stars) {
    const box = document.getElementById("c-stars");
    clearNode(box);
    if (!stars || !stars.length) {
      box.classList.add("hidden");
      return;
    }
    stars.forEach((star) => {
      const card = makeEl("div", "star-card code-" + star.code);
      const head = makeEl("div", "star-head");
      head.appendChild(makeEl("span", "star-icon", star.icon));
      head.appendChild(makeEl("span", "star-title", star.title));
      head.appendChild(makeEl("span", "star-who", star.who));
      card.appendChild(head);
      card.appendChild(makeEl("p", "dyn-summary", star.note));
      box.appendChild(card);
    });
    box.classList.remove("hidden");
  }

  function renderBaziLayer(layer) {
    const box = document.getElementById("c-bazi");
    if (!layer) {
      box.classList.add("hidden");
      return;
    }
    document.getElementById("c-bazi-title").textContent = layer.title;
    document.getElementById("c-bazi-note").textContent = layer.note;
    renderDayPillar(layer.day_pillar);
    renderUsefulGod(layer.useful_god, layer);
    renderCoupleStars(layer.couple_stars);
    box.classList.remove("hidden");
  }

  function renderPair(data) {
    const pair = document.getElementById("c-pair");
    clearNode(pair);
    const wrap = makeEl("span", "compat-pair");
    wrap.appendChild(makeEl("span", "compat-pair-hanzi", data.shio1 ? data.shio1.hanzi : ""));
    const names = [data.shio1 ? data.shio1.name : "", data.shio2 ? data.shio2.name : ""];
    wrap.appendChild(makeEl("span", "compat-pair-names", names.join(" × ")));
    wrap.appendChild(makeEl("span", "compat-pair-hanzi", data.shio2 ? data.shio2.hanzi : ""));
    pair.appendChild(wrap);
  }

  function renderNarrative(data) {
    const narrative = data.narrative;
    const title = document.getElementById("c-narrative-title");
    clearNode(title);
    title.appendChild(makeEl("i", "fa-solid " + narrative.icon));
    title.appendChild(document.createTextNode(" " + narrative.title));
    document.getElementById("c-narrative").textContent = narrative.text || "-";
    document.getElementById("c-drama").textContent = data.drama || "-";
    document.getElementById("c-tips").textContent = data.tips || "-";
  }

  window.renderCompatLayers = function (data) {
    renderPair(data);
    renderRelationBadge(data.pair_relation, data.relationship);
    renderElementDynamic(data.element_dynamic);
    renderYearLayer(data.year_layer);
    renderBaziLayer(data.bazi_layer);
    renderNarrative(data);
  };
})();
