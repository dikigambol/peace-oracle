document.addEventListener('DOMContentLoaded', () => {
    const viewForm = document.getElementById('view-form');
    const viewResult = document.getElementById('view-result');
    const dateInput = document.getElementById('destiny-date');
    const hourSelect = document.getElementById('destiny-hour');
    const minuteSelect = document.getElementById('destiny-minute');
    const cityInput = document.getElementById('destiny-city');
    const submitBtn = document.getElementById('destiny-submit');
    const errorBox = document.getElementById('destiny-error');
    const backBtn = document.getElementById('destiny-back');

    let selectedGender = null;
    let selectedDate = null;
    let loading = false;
    let datePicker = null;

    function el(tag, className, text) {
        const node = document.createElement(tag);
        if (className) node.className = className;
        if (text !== undefined && text !== null) node.textContent = text;
        return node;
    }

    function clear(node) {
        while (node.firstChild) node.removeChild(node.firstChild);
        return node;
    }

    function paragraph(parent, text, className) {
        if (!text) return;
        parent.appendChild(el('p', className || 'destiny-text', text));
    }

    function bulletList(parent, items, className) {
        if (!items || !items.length) return;
        const list = el('ul', className || 'destiny-list');
        items.forEach(item => list.appendChild(el('li', null, item)));
        parent.appendChild(list);
    }

    function card(className) {
        return el('div', 'destiny-card' + (className ? ' ' + className : ''));
    }

    function labelled(parent, label, value) {
        if (!value) return;
        const row = el('p', 'destiny-kv');
        row.appendChild(el('span', 'destiny-kv-label', label));
        row.appendChild(el('span', 'destiny-kv-value', value));
        parent.appendChild(row);
    }

    function updateSubmitState() {
        submitBtn.disabled = loading || !selectedDate || !selectedGender;
    }

    if (window.flatpickr) {
        datePicker = flatpickr(dateInput, {
            dateFormat: 'Y-m-d',
            altInput: true,
            altFormat: 'j F Y',
            locale: 'id',
            maxDate: 'today',
            minDate: '1900-01-01',
            defaultDate: null,
            onChange: (dates, str) => {
                selectedDate = str || null;
                updateSubmitState();
            }
        });
    } else {
        dateInput.removeAttribute('readonly');
        dateInput.addEventListener('change', () => {
            selectedDate = dateInput.value || null;
            updateSubmitState();
        });
    }

    document.querySelectorAll('.destiny-gender-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.destiny-gender-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            selectedGender = btn.dataset.gender;
            updateSubmitState();
        });
    });

    hourSelect.addEventListener('change', () => {
        minuteSelect.disabled = hourSelect.value === '';
        if (minuteSelect.disabled) {
            minuteSelect.value = '';
        } else if (minuteSelect.value === '') {
            minuteSelect.value = '0';
        }
    });

    function resetForm() {
        selectedDate = null;
        selectedGender = null;
        if (datePicker) {
            datePicker.clear();
        } else {
            dateInput.value = '';
        }
        document.querySelectorAll('.destiny-gender-btn').forEach(b => b.classList.remove('selected'));
        hourSelect.value = '';
        minuteSelect.value = '';
        minuteSelect.disabled = true;
        cityInput.value = '';
        errorBox.classList.add('hidden');
        updateSubmitState();
    }

    backBtn.addEventListener('click', () => {
        viewResult.classList.add('hidden');
        viewResult.classList.remove('active');
        viewForm.classList.remove('hidden');
        viewForm.classList.add('active');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    submitBtn.addEventListener('click', () => {
        if (!selectedDate || !selectedGender) return;
        requestChart();
    });

    function showError(message) {
        errorBox.textContent = message;
        errorBox.classList.remove('hidden');
    }

    function requestChart() {
        loading = true;
        updateSubmitState();
        errorBox.classList.add('hidden');
        submitBtn.classList.add('loading');

        fetch('/api/shio/destiny', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                tanggal: selectedDate,
                jam: hourSelect.value === '' ? null : hourSelect.value,
                menit: hourSelect.value === '' ? null : minuteSelect.value || '0',
                kota: cityInput.value || null,
                gender: selectedGender
            })
        })
            .then(res => res.json().then(data => ({ ok: res.ok, data })))
            .then(({ ok, data }) => {
                if (!ok || data.error) {
                    showError(data.error || 'Gulungan gagal dibuka. Coba lagi.');
                    return;
                }
                render(data);
                viewForm.classList.add('hidden');
                viewForm.classList.remove('active');
                viewResult.classList.remove('hidden');
                viewResult.classList.add('active');
                window.scrollTo({ top: 0, behavior: 'smooth' });
                resetForm();
            })
            .catch(err => {
                console.error('Gagal memuat gulungan:', err);
                showError('Terjadi gangguan energi kosmik. Silakan coba lagi.');
            })
            .finally(() => {
                loading = false;
                submitBtn.classList.remove('loading');
                updateSubmitState();
            });
    }

    function renderNotices(meta, noBirthTime) {
        const box = clear(document.getElementById('destiny-notices'));

        const school = el('div', 'destiny-notice');
        school.appendChild(el('span', 'destiny-notice-icon', '☯'));
        const schoolBody = el('div');
        schoolBody.appendChild(el('strong', null, 'Aliran ' + meta.school));
        paragraph(schoolBody, 'Perhitungan memakai batas awal musim semi (立春) untuk pilar tahun dan batas 23:00 untuk pilar hari (子時換日).', 'destiny-notice-text');
        school.appendChild(schoolBody);
        box.appendChild(school);

        if (meta.late_zi_alternative_day) {
            const lateZi = el('div', 'destiny-notice destiny-notice-warn');
            lateZi.appendChild(el('span', 'destiny-notice-icon', '🌗'));
            const body = el('div');
            body.appendChild(el('strong', null, 'Kamu lahir di jam 23:00–23:59'));
            paragraph(body, 'Aliran yang dipakai di sini menganggap harimu sudah berganti sejak pukul 23:00. Sebagian praktisi Zi Ping memakai aliran lain (子正換日) yang baru mengganti hari pukul 00:00.', 'destiny-notice-text');
            paragraph(body, 'Menurut aliran itu, pilar harimu adalah ' + meta.late_zi_alternative_day + ', bukan pilar hari di tabel bawah, dan pilar jammu ikut berubah. Dua-duanya sah — bedanya ada di aturan, bukan di hitungan.', 'destiny-notice-text');
            lateZi.appendChild(body);
            box.appendChild(lateZi);
        }

        if (meta.city_unrecognized) {
            const unknown = el('div', 'destiny-notice destiny-notice-warn');
            unknown.appendChild(el('span', 'destiny-notice-icon', '📍'));
            const body = el('div');
            body.appendChild(el('strong', null, 'Kota lahir tidak dikenali'));
            paragraph(body, 'Nama kota yang kamu ketik tidak ada di daftar, jadi zona WIB dipakai sebagai asumsi. Hasilnya bisa berbeda kalau kamu lahir di WITA atau WIT tepat di hari pergantian musim. Ketik ulang lalu pilih dari daftar supaya tepat.', 'destiny-notice-text');
            unknown.appendChild(body);
            box.appendChild(unknown);
        }

        if (meta.city_zone_only) {
            const zoneOnly = el('div', 'destiny-notice');
            zoneOnly.appendChild(el('span', 'destiny-notice-icon', '📍'));
            const body = el('div');
            body.appendChild(el('strong', null, 'Kota dipakai untuk zona waktu'));
            paragraph(body, 'Tanpa jam lahir, ' + meta.city.name + ' dipakai untuk menentukan zona ' + meta.city.zone + ' di batas pergantian musim. Koreksi waktu matahari sejati butuh jam lahir, jadi belum diterapkan.', 'destiny-notice-text');
            zoneOnly.appendChild(body);
            box.appendChild(zoneOnly);
        }

        if (meta.city && meta.true_solar_offset_minutes !== null) {
            const solar = el('div', 'destiny-notice');
            solar.appendChild(el('span', 'destiny-notice-icon', '🕰'));
            const body = el('div');
            body.appendChild(el('strong', null, 'Koreksi waktu matahari sejati'));
            const offset = meta.true_solar_offset_minutes;
            const sign = offset >= 0 ? '+' : '';
            paragraph(body, 'Jam lahirmu dibaca sebagai waktu ' + meta.city.zone +
                ' lalu digeser ' + sign + offset.toFixed(1) + ' menit menurut bujur ' +
                meta.city.name + ' (' + meta.city.longitude + '°BT) terhadap meridian ' +
                meta.city.zone_meridian + '°BT.',
                'destiny-notice-text');
            if (meta.city.assumed) {
                paragraph(body, 'Kota lahir tidak dipilih atau tidak dikenali, jadi dipakai ' + meta.city.name + ' sebagai asumsi. Ketik ulang lalu pilih dari daftar supaya tepat.', 'destiny-notice-text');
            }
            solar.appendChild(body);
            box.appendChild(solar);
        }

        if (noBirthTime) {
            const notice = el('div', 'destiny-notice destiny-notice-warn');
            notice.appendChild(el('span', 'destiny-notice-icon', '🕯'));
            const body = el('div');
            body.appendChild(el('strong', null, 'Bacaan tiga pilar'));
            paragraph(body, noBirthTime.notice, 'destiny-notice-text');

            const columns = el('div', 'destiny-notice-columns');
            const valid = el('div');
            valid.appendChild(el('h4', null, 'Tetap sah dibaca'));
            bulletList(valid, noBirthTime.still_valid, 'destiny-list destiny-list-ok');
            const missing = el('div');
            missing.appendChild(el('h4', null, 'Tidak ditampilkan'));
            bulletList(missing, noBirthTime.not_available, 'destiny-list destiny-list-off');
            columns.appendChild(valid);
            columns.appendChild(missing);
            body.appendChild(columns);
            paragraph(body, noBirthTime.invitation, 'destiny-notice-text');
            notice.appendChild(body);
            box.appendChild(notice);
        }
    }

    const chartFrame = document.getElementById('destiny-chart-frame');
    const chartScroll = document.getElementById('destiny-chart-scroll');

    function updateChartScrollHint() {
        if (!chartFrame || !chartScroll) return;
        const maxScroll = chartScroll.scrollWidth - chartScroll.clientWidth;
        chartFrame.classList.toggle('more-left', chartScroll.scrollLeft > 4);
        chartFrame.classList.toggle('more-right', chartScroll.scrollLeft < maxScroll - 4);
    }

    if (chartScroll) {
        chartScroll.addEventListener('scroll', updateChartScrollHint, { passive: true });
        window.addEventListener('resize', updateChartScrollHint);
    }

    function renderChart(pillars) {
        const table = clear(document.getElementById('destiny-chart'));
        const available = pillars.filter(p => p.available);

        const headRow = el('tr');
        headRow.appendChild(el('th', 'destiny-chart-corner', ''));
        available.forEach(p => {
            const cell = el('th');
            cell.appendChild(el('span', 'destiny-chart-hanzi-small', p.hanzi));
            cell.appendChild(el('span', 'destiny-chart-label', p.label));
            headRow.appendChild(cell);
        });
        const head = el('thead');
        head.appendChild(headRow);
        table.appendChild(head);

        const body = el('tbody');

        const rowHead = (hanzi, label) => {
            const cell = el('th', 'destiny-chart-rowhead');
            cell.appendChild(el('span', 'destiny-chart-rowhead-hanzi', hanzi));
            cell.appendChild(el('span', 'destiny-chart-rowhead-label', label));
            return cell;
        };

        const stemRow = el('tr');
        stemRow.appendChild(rowHead('天干', 'Batang Langit'));
        available.forEach(p => {
            const cell = el('td');
            cell.appendChild(el('span', 'destiny-chart-hanzi', p.stem_hanzi));
            cell.appendChild(el('span', 'destiny-chart-sub', p.stem + ' · ' + p.stem_element));
            cell.appendChild(el('span', 'destiny-chart-god', p.stem_god.hanzi + ' ' + p.stem_god.meaning));
            stemRow.appendChild(cell);
        });
        body.appendChild(stemRow);

        const branchRow = el('tr');
        branchRow.appendChild(rowHead('地支', 'Cabang Bumi'));
        available.forEach(p => {
            const cell = el('td');
            cell.appendChild(el('span', 'destiny-chart-hanzi', p.branch_hanzi));
            cell.appendChild(el('span', 'destiny-chart-sub', p.branch + ' · ' + p.branch_element));
            branchRow.appendChild(cell);
        });
        body.appendChild(branchRow);

        const hiddenRow = el('tr');
        hiddenRow.appendChild(rowHead('藏干', 'Batang Tersembunyi'));
        available.forEach(p => {
            const cell = el('td');
            p.hidden_stems.forEach(h => {
                const item = el('span', 'destiny-hidden');
                item.appendChild(el('span', 'destiny-hidden-hanzi', h.hanzi));
                item.appendChild(el('span', 'destiny-hidden-god', h.god.hanzi + ' ' + h.god.meaning));
                cell.appendChild(item);
            });
            hiddenRow.appendChild(cell);
        });
        body.appendChild(hiddenRow);

        table.appendChild(body);

        const positions = clear(document.getElementById('destiny-positions'));
        pillars.forEach(p => {
            const item = card('destiny-position' + (p.available ? '' : ' destiny-position-off'));
            const title = el('h4', 'destiny-position-title');
            title.appendChild(el('span', 'destiny-position-hanzi', p.hanzi));
            title.appendChild(el('span', null, p.label));
            title.appendChild(el('span', 'destiny-position-age', p.age_range));
            item.appendChild(title);
            paragraph(item, p.domain, 'destiny-text destiny-text-small');
            paragraph(item, p.available ? p.reading_note : 'Tidak tersedia tanpa jam lahir.', 'destiny-text destiny-text-small');
            positions.appendChild(item);
        });
    }

    function renderDayMaster(dm) {
        const box = clear(document.getElementById('destiny-daymaster'));
        const item = card();

        const head = el('div', 'destiny-dm-head');
        head.appendChild(el('span', 'destiny-dm-hanzi', dm.hanzi));
        const meta = el('div');
        meta.appendChild(el('h4', 'destiny-dm-title', dm.title));
        meta.appendChild(el('span', 'destiny-dm-sub', dm.name + ' · ' + dm.element + ' ' + dm.polarity));
        head.appendChild(meta);
        item.appendChild(head);

        paragraph(item, dm.personality);
        paragraph(item, dm.variant, 'destiny-text destiny-text-accent');

        const columns = el('div', 'destiny-two-col');
        const good = el('div');
        good.appendChild(el('h4', null, 'Kekuatan'));
        bulletList(good, dm.strengths, 'destiny-list destiny-list-ok');
        const bad = el('div');
        bad.appendChild(el('h4', null, 'Kelemahan'));
        bulletList(bad, dm.weaknesses, 'destiny-list destiny-list-off');
        columns.appendChild(good);
        columns.appendChild(bad);
        item.appendChild(columns);

        box.appendChild(item);
    }

    function renderStrength(strength, useful) {
        const box = clear(document.getElementById('destiny-strength'));
        const item = card();

        const head = el('div', 'destiny-strength-head');
        head.appendChild(el('span', 'destiny-strength-hanzi', strength.hanzi));
        const meta = el('div');
        meta.appendChild(el('h4', 'destiny-dm-title', strength.title));
        meta.appendChild(el('span', 'destiny-dm-sub', strength.label));
        head.appendChild(meta);
        item.appendChild(head);

        paragraph(item, strength.summary);
        paragraph(item, strength.advice);
        paragraph(item, strength.caution, 'destiny-text destiny-text-warn');

        labelled(item, 'Rasio dukungan', (strength.support_ratio * 100).toFixed(1) + '%');
        labelled(item, 'Elemen menguntungkan', useful.favourable.join(', '));
        labelled(item, 'Elemen merugikan', useful.unfavourable.join(', '));

        box.appendChild(item);
    }

    function renderElements(elements) {
        const box = clear(document.getElementById('destiny-elements'));
        const max = elements.reduce((acc, e) => Math.max(acc, e.score), 0) || 1;

        elements.forEach(e => {
            const item = card('destiny-element destiny-role-' + e.role);

            const head = el('div', 'destiny-element-head');
            head.appendChild(el('span', 'destiny-element-name', e.label + ' ' + e.hanzi));
            head.appendChild(el('span', 'destiny-element-score', e.score.toFixed(2)));
            item.appendChild(head);

            const bar = el('div', 'destiny-bar');
            const fill = el('div', 'destiny-bar-fill');
            fill.style.width = Math.round((e.score / max) * 100) + '%';
            bar.appendChild(fill);
            item.appendChild(bar);

            const tags = el('div', 'destiny-tags');
            tags.appendChild(el('span', 'destiny-tag destiny-tag-' + e.status, e.status));
            tags.appendChild(el('span', 'destiny-tag destiny-tag-role-' + e.role, e.role));
            item.appendChild(tags);

            paragraph(item, e.status_label, 'destiny-text destiny-text-small destiny-text-accent');
            paragraph(item, e.impact, 'destiny-text destiny-text-small');
            paragraph(item, e.verdict, 'destiny-text destiny-text-small destiny-text-accent');
            paragraph(item, e.action, 'destiny-text destiny-text-small');
            paragraph(item, e.remedy, 'destiny-text destiny-text-small');

            box.appendChild(item);
        });
    }

    function renderGod(god) {
        const box = clear(document.getElementById('destiny-god'));
        const item = card();

        const head = el('div', 'destiny-dm-head');
        head.appendChild(el('span', 'destiny-dm-hanzi', god.name_cn));
        const meta = el('div');
        meta.appendChild(el('h4', 'destiny-dm-title', god.name_id));
        meta.appendChild(el('span', 'destiny-dm-sub',
            'Menguasai ' + Math.round(god.share * 100) + '% bobot chart'));
        head.appendChild(meta);
        item.appendChild(head);

        if (!god.decisive) {
            paragraph(item,
                'Selisihnya tipis dengan dewa di bawahnya, jadi bacaan ini condong, bukan mutlak.',
                'destiny-text destiny-text-warn destiny-text-small');
        }

        paragraph(item, god.essence);
        paragraph(item, god.variant, 'destiny-text destiny-text-accent');

        box.appendChild(item);
    }

    function renderDestiny(destiny, nuance, disclaimer) {
        const box = clear(document.getElementById('destiny-destiny'));
        const grid = el('div', 'destiny-destiny-grid');

        const career = card('destiny-destiny-card');
        career.appendChild(el('h4', 'destiny-destiny-title', 'Karir — ' + destiny.career.archetype));
        paragraph(career, destiny.career.work_style, 'destiny-text destiny-text-small');
        bulletList(career, destiny.career.ideal_fields, 'destiny-list destiny-list-plain');
        paragraph(career, destiny.career.warning, 'destiny-text destiny-text-small destiny-text-warn');
        paragraph(career, nuance.karir, 'destiny-text destiny-text-small destiny-text-accent');
        grid.appendChild(career);

        const wealth = card('destiny-destiny-card');
        wealth.appendChild(el('h4', 'destiny-destiny-title', 'Rezeki — ' + destiny.wealth.wealth_type));
        paragraph(wealth, destiny.wealth.investment_advice, 'destiny-text destiny-text-small');
        paragraph(wealth, destiny.wealth.financial_trap, 'destiny-text destiny-text-small destiny-text-warn');
        paragraph(wealth, destiny.wealth.lucky_period, 'destiny-text destiny-text-small');
        paragraph(wealth, nuance.rezeki, 'destiny-text destiny-text-small destiny-text-accent');
        grid.appendChild(wealth);

        const love = card('destiny-destiny-card');
        love.appendChild(el('h4', 'destiny-destiny-title', 'Asmara — ' + destiny.love.love_type));
        paragraph(love, destiny.love.ideal_partner_desc, 'destiny-text destiny-text-small');
        paragraph(love, destiny.love.red_flag, 'destiny-text destiny-text-small destiny-text-warn');
        paragraph(love, destiny.love.peach_blossom_note, 'destiny-text destiny-text-small');
        paragraph(love, nuance.asmara, 'destiny-text destiny-text-small destiny-text-accent');
        grid.appendChild(love);

        const health = card('destiny-destiny-card');
        health.appendChild(el('h4', 'destiny-destiny-title', 'Kesehatan — ' + destiny.health.energy_type));
        paragraph(health, destiny.health.exercise_advice, 'destiny-text destiny-text-small');
        paragraph(health, destiny.health.taboo, 'destiny-text destiny-text-small destiny-text-warn');
        destiny.health.organs.forEach(organ => {
            const row = el('div', 'destiny-organ');
            row.appendChild(el('strong', null, organ.element + ' tipis — ' + organ.vulnerable_organ));
            paragraph(row, organ.symptoms, 'destiny-text destiny-text-small');
            paragraph(row, organ.prevention, 'destiny-text destiny-text-small');
            health.appendChild(row);
        });
        paragraph(health, disclaimer, 'destiny-text destiny-text-small destiny-text-muted');
        grid.appendChild(health);

        box.appendChild(grid);
    }

    function renderRelations(relations) {
        const box = clear(document.getElementById('destiny-relations'));
        const items = (relations && relations.items) || [];
        if (!items.length) {
            paragraph(box, 'Pilar-pilarmu tidak saling mengunci atau bentrok. Energinya berdiri sendiri-sendiri, jadi bacaanmu lebih banyak ditentukan oleh elemen dan dewanya.', 'destiny-text');
            return;
        }
        const grid = el('div', 'destiny-relation-grid');
        items.forEach(item => {
            const entry = card('destiny-relation destiny-relation-' + item.code);
            const head = el('div', 'destiny-relation-head');
            head.appendChild(el('span', 'destiny-relation-hanzi', item.hanzi));
            const meta = el('div');
            meta.appendChild(el('h4', 'destiny-relation-title', item.title));
            const where = item.slots.join(' · ') + ' · ' + item.branches;
            meta.appendChild(el('span', 'destiny-dm-sub', where));
            head.appendChild(meta);
            entry.appendChild(head);
            if (item.element) {
                entry.appendChild(el('span', 'destiny-relation-tag',
                    'Elemen ' + item.element + ' ' + item.element_hanzi));
            } else if (item.reach_label) {
                const tag = el('span', 'destiny-relation-tag destiny-relation-' + item.reach,
                    item.reach_label);
                tag.title = item.reach_note;
                entry.appendChild(tag);
            }
            paragraph(entry, item.note, 'destiny-text destiny-text-small');
            paragraph(entry, item.advice, 'destiny-text destiny-text-small destiny-text-muted');
            grid.appendChild(entry);
        });
        box.appendChild(grid);
        if (relations.clash_note) {
            paragraph(box, relations.clash_note, 'destiny-note');
        }
    }

    function renderShenSha(stars) {
        const box = clear(document.getElementById('destiny-shensha'));
        if (!stars.length) {
            paragraph(box, 'Tidak ada bintang nasib menonjol di chart-mu. Itu bukan kekurangan — bacaanmu ditentukan sepenuhnya oleh pilar dan dewanya.', 'destiny-text');
            return;
        }
        const grid = el('div', 'destiny-star-grid');
        stars.forEach(star => {
            const item = card('destiny-star destiny-star-' + star.category);
            const head = el('div', 'destiny-star-head');
            head.appendChild(el('span', 'destiny-star-icon', star.icon));
            const meta = el('div');
            meta.appendChild(el('h4', 'destiny-star-title', star.name_id));
            meta.appendChild(el('span', 'destiny-dm-sub', star.name_cn + ' · ' + star.slots.join(', ')));
            head.appendChild(meta);
            item.appendChild(head);
            paragraph(item, star.description, 'destiny-text destiny-text-small');
            paragraph(item, star.life_impact, 'destiny-text destiny-text-small');
            grid.appendChild(item);
        });
        box.appendChild(grid);
    }

    function renderLuck(luck) {
        const block = document.getElementById('destiny-luck-block');
        const box = clear(document.getElementById('destiny-luck'));
        if (!luck) {
            block.classList.add('hidden');
            return;
        }
        block.classList.remove('hidden');
        document.getElementById('destiny-luck-note').textContent =
            'Arah ' + luck.direction + ', mulai berlaku sekitar usia ' +
            luck.start_age_years + ' tahun ' + luck.start_age_months + ' bulan.';

        luck.pillars.forEach(p => {
            const item = card('destiny-luck-item');
            const head = el('div', 'destiny-luck-head');
            head.appendChild(el('span', 'destiny-luck-hanzi', p.pillar_hanzi));
            const meta = el('div');
            meta.appendChild(el('h4', 'destiny-luck-title', p.phase_name));
            meta.appendChild(el('span', 'destiny-dm-sub',
                'Usia ' + p.age_from + '–' + p.age_to + ' · ' + p.year_from + '–' + p.year_to +
                ' · ' + p.dominant_god.hanzi + ' ' + p.dominant_god.meaning));
            head.appendChild(meta);
            item.appendChild(head);
            paragraph(item, p.description, 'destiny-text destiny-text-small');
            paragraph(item, p.advice, 'destiny-text destiny-text-small destiny-text-accent');
            box.appendChild(item);
        });
    }

    function renderHeritage(heritage) {
        const box = clear(document.getElementById('destiny-heritage'));
        const item = card();

        const head = el('div', 'destiny-dm-head');
        head.appendChild(el('span', 'destiny-dm-hanzi', heritage.icon));
        const meta = el('div');
        meta.appendChild(el('h4', 'destiny-dm-title',
            heritage.shio_name + ' ' + heritage.shio_hanzi));
        meta.appendChild(el('span', 'destiny-dm-sub',
            'Cabang tahun ' + heritage.branch_hanzi + ' · ' + heritage.branch_element));
        head.appendChild(meta);
        item.appendChild(head);

        heritage.persona.split('\n\n').forEach(part => paragraph(item, part));
        paragraph(item, heritage.relation_text, 'destiny-text destiny-text-accent');

        const alter = el('div', 'destiny-alter');
        alter.appendChild(el('h4', null, heritage.alter_ego.title));
        paragraph(alter, heritage.alter_ego.description, 'destiny-text destiny-text-small');
        item.appendChild(alter);

        const columns = el('div', 'destiny-two-col');
        const good = el('div');
        good.appendChild(el('h4', null, 'Yang orang lihat'));
        bulletList(good, heritage.traits_positive, 'destiny-list destiny-list-ok');
        const bad = el('div');
        bad.appendChild(el('h4', null, 'Yang bikin repot'));
        bulletList(bad, heritage.traits_negative, 'destiny-list destiny-list-off');
        columns.appendChild(good);
        columns.appendChild(bad);
        item.appendChild(columns);

        const flags = el('div', 'destiny-two-col');
        const green = el('div');
        green.appendChild(el('h4', null, 'Green flag'));
        bulletList(green, heritage.green_flags, 'destiny-list destiny-list-ok');
        const red = el('div');
        red.appendChild(el('h4', null, 'Red flag'));
        bulletList(red, heritage.red_flags, 'destiny-list destiny-list-off');
        flags.appendChild(green);
        flags.appendChild(red);
        item.appendChild(flags);

        const facts = el('div', 'destiny-facts');
        labelled(facts, 'Bunga keberuntungan', heritage.lucky_flowers.join(', '));
        labelled(facts, 'Warna yang menekan', heritage.unlucky_colors.join(', '));
        labelled(facts, 'Angka yang menekan', heritage.unlucky_numbers.join(', '));
        labelled(facts, 'Bulan mendukung', heritage.best_months.join(', '));
        labelled(facts, 'Bulan menggesek', heritage.worst_months.join(', '));
        labelled(facts, 'Tokoh seangkatan shio', heritage.famous_people.join(', '));
        item.appendChild(facts);

        paragraph(item, heritage.spirit_advice, 'destiny-text destiny-text-accent');

        box.appendChild(item);
    }

    function renderRemedy(remedies) {
        const box = clear(document.getElementById('destiny-remedy'));
        const grid = el('div', 'destiny-remedy-grid');
        remedies.forEach(r => {
            const item = card('destiny-remedy-card');
            item.appendChild(el('h4', 'destiny-destiny-title', r.element));
            labelled(item, 'Warna', r.colors.join(', '));
            labelled(item, 'Arah', r.directions.join(', '));
            labelled(item, 'Angka', r.numbers.join(', '));
            labelled(item, 'Kristal', r.crystals.join(', '));
            labelled(item, 'Makanan', r.food_elements.join(', '));
            paragraph(item, r.ritual_advice, 'destiny-text destiny-text-small');
            grid.appendChild(item);
        });
        box.appendChild(grid);
    }

    function render(data) {
        renderNotices(data.meta, data.no_birth_time);
        renderChart(data.pillars);
        requestAnimationFrame(updateChartScrollHint);
        renderDayMaster(data.day_master);
        renderStrength(data.strength, data.useful_gods);
        renderElements(data.elements);
        renderGod(data.dominant_god);
        renderDestiny(data.destiny, data.day_master.nuance, data.meta.disclaimer);
        renderRelations(data.relations);
        renderShenSha(data.shen_sha);
        renderLuck(data.luck);
        renderHeritage(data.heritage);
        renderRemedy(data.remedy);
        document.getElementById('destiny-disclaimer').textContent = data.meta.disclaimer;
    }
  window.initBurstParticles();
});
