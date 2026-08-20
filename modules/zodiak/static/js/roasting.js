document.addEventListener('DOMContentLoaded', () => {
    // ----------------------------------------------------
    // Efek glow gerakan mouse pada kartu zodiak (Optimized 60fps)
    // ----------------------------------------------------
    const cards = document.querySelectorAll('.zodiac-card');
    cards.forEach(card => {
        let rect = null;
        let ticking = false;

        card.addEventListener('mouseenter', () => {
            rect = card.getBoundingClientRect();
        });

        card.addEventListener('mousemove', e => {
            if (!rect) rect = card.getBoundingClientRect();
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    if (rect) {
                        const x = e.clientX - rect.left;
                        const y = e.clientY - rect.top;
                        card.style.setProperty('--x', `${x}px`);
                        card.style.setProperty('--y', `${y}px`);
                    }
                    ticking = false;
                });
                ticking = true;
            }
        });

        card.addEventListener('mouseleave', () => {
            rect = null;
        });
    });

    // ----------------------------------------------------
    // Pengambilan data Roast My Sign zodiak via API
    // ----------------------------------------------------
    const instructionPanel = document.getElementById('roast-instruction');
    const loaderPanel = document.getElementById('roast-loader');
    const contentPanel = document.getElementById('roast-content');
    const btnBackGrid = document.getElementById('btn-back-grid-roast');

    const symbolEl = document.getElementById('roast-symbol');
    const nameEl = document.getElementById('roast-name');
    const datesEl = document.getElementById('roast-dates');
    const elementBadgeEl = document.getElementById('roast-element-badge');
    
    const headlineTextEl = document.getElementById('roast-headline-text');
    const toxicListEl = document.getElementById('roast-toxic-list');
    const financialTextEl = document.getElementById('roast-financial-text');
    const loveTextEl = document.getElementById('roast-love-text');
    const quoteTextEl = document.getElementById('roast-quote-text');
    const tipTextEl = document.getElementById('roast-tip-text');

    // Elemen Roasting Hubungan (Zodiak A & B)
    const pairSignANameEl = document.getElementById('pair-sign-a-name');
    const pairSignSelectEl = document.getElementById('pair-sign-select');
    const pairRoastResultEl = document.getElementById('pair-roast-result');
    const pairRoastBadgeEl = document.getElementById('pair-roast-badge');
    const pairRoastHeadlineEl = document.getElementById('pair-roast-headline');
    const pairRoastDescEl = document.getElementById('pair-roast-desc');
    const pairRoastVerdictEl = document.getElementById('pair-roast-verdict');

    const elementClasses = {
        api: 'fire',
        tanah: 'earth',
        udara: 'air',
        air: 'water'
    };

    const symbols = {
        aries: '♈', taurus: '♉', gemini: '♊', cancer: '♋',
        leo: '♌', virgo: '♍', libra: '♎', scorpio: '♏',
        sagittarius: '♐', capricorn: '♑', aquarius: '♒', pisces: '♓'
    };

    let activeSignA = null;

    cards.forEach(card => {
        card.addEventListener('click', async () => {
            // Kelola kelas aktif
            cards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');

            // Tampilkan loader, sembunyikan instruksi & konten lama
            instructionPanel.classList.add('hidden');
            contentPanel.classList.add('hidden');
            loaderPanel.classList.remove('hidden');

            // Scroll otomatis ke panel detail di layar mobile/tablet (<= 968px)
            if (window.innerWidth <= 968) {
                const detailsContainer = document.querySelector('.details-panel-container');
                if (detailsContainer) {
                    detailsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }

            const signKey = card.getAttribute('data-sign');
            activeSignA = signKey;

            // Reset dropdown & hasil pasangan
            if (pairSignSelectEl) pairSignSelectEl.value = '';
            if (pairRoastResultEl) pairRoastResultEl.classList.add('hidden');

            try {
                // Ambil data Roast My Sign dari server Flask
                const response = await fetch(`/zodiak/api/roast?sign=${signKey}`);
                if (!response.ok) throw new Error('Gagal mengambil data roasting zodiak');

                const data = await response.json();
                
                // Transisi halus loader
                setTimeout(() => {
                    loaderPanel.classList.add('hidden');
                    displayRoastingDetails(data, signKey);
                }, 300);
            } catch (err) {
                console.error(err);
                loaderPanel.classList.add('hidden');
                alert('Gagal mengambil data roasting. Silakan coba lagi.');
            }
        });
    });

    // Tombol Kembali di Mobile
    if (btnBackGrid) {
        btnBackGrid.addEventListener('click', () => {
            const selectorContainer = document.querySelector('.zodiac-selector-container');
            if (selectorContainer) {
                selectorContainer.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    function displayRoastingDetails(data, signKey) {
        contentPanel.classList.remove('hidden');

        const roast = data.roast;

        // Perbarui info dasar
        if (symbolEl) symbolEl.innerText = symbols[signKey] || '✨';
        if (nameEl) nameEl.innerText = data.name;
        if (datesEl) datesEl.innerText = data.date_range;
        if (pairSignANameEl) pairSignANameEl.innerText = data.name;

        // Perbarui Badge Elemen
        const elemKey = (data.element || 'Api').toLowerCase();
        const cssClass = elementClasses[elemKey] || 'fire';
        if (elementBadgeEl) {
            elementBadgeEl.className = `details-element-badge element-badge ${cssClass}`;
            elementBadgeEl.innerText = data.element;
        }

        if (headlineTextEl) headlineTextEl.innerText = roast.headline;

        // Render Red Flags List
        if (toxicListEl) {
            toxicListEl.innerHTML = '';
            roast.toxic_traits.forEach(trait => {
                const li = document.createElement('li');
                li.innerText = trait;
                toxicListEl.appendChild(li);
            });
        }

        if (financialTextEl) financialTextEl.innerText = roast.financial_sin;
        if (loveTextEl) loveTextEl.innerText = roast.love_red_flag;
        if (quoteTextEl) quoteTextEl.innerText = `"${roast.catchphrase}"`;
        if (tipTextEl) tipTextEl.innerText = roast.survival_tip;
    }

    // Event Listener Pemilihan Zodiak B untuk Roasting Hubungan
    if (pairSignSelectEl) {
        pairSignSelectEl.addEventListener('change', async () => {
            const signB = pairSignSelectEl.value;
            if (!activeSignA || !signB) {
                if (pairRoastResultEl) pairRoastResultEl.classList.add('hidden');
                return;
            }

            try {
                const response = await fetch(`/zodiak/api/roast?sign=${activeSignA}&sign_b=${signB}`);
                if (!response.ok) throw new Error('Gagal mengambil data roasting pasangan');

                const data = await response.json();
                const rel = data.relationship_roast;

                if (rel && pairRoastResultEl) {
                    pairRoastBadgeEl.innerText = rel.badge;
                    pairRoastHeadlineEl.innerText = rel.headline;
                    pairRoastDescEl.innerText = rel.desc;
                    pairRoastVerdictEl.innerText = rel.verdict;

                    pairRoastResultEl.classList.remove('hidden');
                }
            } catch (err) {
                console.error(err);
                alert('Gagal mengambil roasting hubungan.');
            }
        });
    }
});
