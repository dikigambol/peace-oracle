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
    // Pengambilan data karakter zodiak via API
    // ----------------------------------------------------
    const instructionPanel = document.getElementById('char-instruction');
    const loaderPanel = document.getElementById('char-loader');
    const contentPanel = document.getElementById('char-content');

    cards.forEach(card => {
        card.addEventListener('click', async () => {
            // Kelola kelas aktif
            cards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');

            // Tampilkan loader, sembunyikan instruksi & konten lama
            instructionPanel.classList.add('hidden');
            contentPanel.classList.add('hidden');
            loaderPanel.classList.remove('hidden');

            // Scroll otomatis ke panel detail karakter di layar mobile/tablet (<= 968px)
            if (window.innerWidth <= 968) {
                const detailsContainer = document.querySelector('.details-panel-container');
                if (detailsContainer) {
                    detailsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }

            const sign = card.getAttribute('data-sign');

            try {
                // Ambil data karakter zodiak dari server Flask
                const response = await fetch(`/api/zodiak/karakter/${sign}`);
                if (!response.ok) throw new Error('Gagal mengambil data karakter');

                const data = await response.json();

                // Berikan penundaan transisi halus agar animasi loader terlihat elegan
                setTimeout(() => {
                    loaderPanel.classList.add('hidden');
                    displayCharacterDetails(data);
                }, 300);
            } catch (err) {
                console.error(err);
                loaderPanel.classList.add('hidden');
                alert('Gagal mengambil data karakter dari server. Silakan coba lagi.');
            }
        });
    });

    function displayCharacterDetails(data) {
        // Tampilkan panel detail
        contentPanel.classList.remove('hidden');

        // Perbarui info dasar
        document.getElementById('char-name').innerText = data.name;
        document.getElementById('char-dates').innerText = data.date_range;

        // Perbarui Simbol Zodiak
        const symbols = {
            aries: '♈', taurus: '♉', gemini: '♊', cancer: '♋',
            leo: '♌', virgo: '♍', libra: '♎', scorpio: '♏',
            sagittarius: '♐', capricorn: '♑', aquarius: '♒', pisces: '♓'
        };
        const signKey = data.name.toLowerCase();
        document.getElementById('char-symbol').innerText = symbols[signKey] || '✨';

        // Petakan nama elemen Indonesia ke kelas CSS
        const elementClasses = {
            api: 'fire',
            tanah: 'earth',
            udara: 'air',
            air: 'water'
        };
        const elemKey = data.element.toLowerCase();
        const cssClass = elementClasses[elemKey] || 'fire';

        // Perbarui Badge Elemen
        const elementBadge = document.getElementById('char-element-badge');
        elementBadge.className = `details-element-badge element-badge ${cssClass}`;
        elementBadge.innerText = data.element;

        // 1. Render Ciri Fisik Dominan
        const physicalContainer = document.getElementById('char-physical-tags');
        physicalContainer.innerHTML = '';
        data.physical_traits.forEach(trait => {
            const item = document.createElement('div');
            item.className = 'physical-trait-item';
            item.innerHTML = `<i class="fa-solid fa-check-circle"></i> <span>${trait}</span>`;
            physicalContainer.appendChild(item);
        });

        // 2. Render Sifat & Karakter Utama
        document.getElementById('char-personality-text').innerText = data.personality;

        // 3. Render Kebiasaan Unik Sehari-hari
        const habitsContainer = document.getElementById('char-habits-list');
        habitsContainer.innerHTML = '';
        data.habits.forEach(habit => {
            const li = document.createElement('li');
            li.innerText = habit;
            habitsContainer.appendChild(li);
        });

        // 4. Render Fun Fact
        document.getElementById('char-fun-fact-text').innerText = data.fun_fact;
    }

    // Tombol kembali ke grid zodiak di layar mobile
    const btnBackChar = document.getElementById('btn-back-grid-char');
    if (btnBackChar) {
        btnBackChar.addEventListener('click', () => {
            const zodiacGrid = document.getElementById('zodiac-grid');
            if (zodiacGrid) {
                zodiacGrid.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    }
});
