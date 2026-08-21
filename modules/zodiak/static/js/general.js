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
    // Pengambilan data General zodiak via API
    // ----------------------------------------------------
    const instructionPanel = document.getElementById('gen-instruction');
    const loaderPanel = document.getElementById('gen-loader');
    const contentPanel = document.getElementById('gen-content');

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

            const sign = card.getAttribute('data-sign');

            try {
                // Ambil data General zodiak dari server Flask
                const response = await fetch(`/api/zodiak/general/${sign}`);
                if (!response.ok) throw new Error('Gagal mengambil data general');

                const data = await response.json();

                // Berikan penundaan transisi halus agar animasi loader terlihat elegan
                setTimeout(() => {
                    loaderPanel.classList.add('hidden');
                    displayGeneralDetails(data);
                }, 300);
            } catch (err) {
                console.error(err);
                loaderPanel.classList.add('hidden');
                alert('Gagal mengambil data dari server. Silakan coba lagi.');
            }
        });
    });

    function displayGeneralDetails(data) {
        // Tampilkan panel detail
        contentPanel.classList.remove('hidden');

        // Perbarui info dasar
        document.getElementById('gen-name').innerText = data.name;
        document.getElementById('gen-dates').innerText = data.date_range;

        // Perbarui Simbol Zodiak
        const symbols = {
            aries: '♈', taurus: '♉', gemini: '♊', cancer: '♋',
            leo: '♌', virgo: '♍', libra: '♎', scorpio: '♏',
            sagittarius: '♐', capricorn: '♑', aquarius: '♒', pisces: '♓'
        };
        const signKey = data.name.toLowerCase();
        document.getElementById('gen-symbol').innerText = symbols[signKey] || '✨';

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
        const elementBadge = document.getElementById('gen-element-badge');
        elementBadge.className = `details-element-badge element-badge ${cssClass}`;
        elementBadge.innerText = data.element;

        // 1. Render Ciri Fisik Dominan
        const physicalContainer = document.getElementById('gen-physical-tags');
        physicalContainer.innerHTML = '';
        data.physical_traits.forEach(trait => {
            const item = document.createElement('div');
            item.className = 'physical-trait-item';
            item.innerHTML = `<i class="fa-solid fa-check-circle"></i> <span>${trait}</span>`;
            physicalContainer.appendChild(item);
        });

        // 2. Render Sifat & Karakter Utama
        document.getElementById('gen-personality-text').innerText = data.personality;

        // 3. Render Kebiasaan Unik Sehari-hari
        const habitsContainer = document.getElementById('gen-habits-list');
        habitsContainer.innerHTML = '';
        data.habits.forEach(habit => {
            const li = document.createElement('li');
            li.innerText = habit;
            habitsContainer.appendChild(li);
        });

        // 4. Render Animal Soulmate
        if (data.animal_soulmate) {
            document.getElementById('gen-animal-name').innerText = data.animal_soulmate.name;
            document.getElementById('gen-animal-desc').innerText = data.animal_soulmate.description;
        }

        // 5. Render Selera Lidah / Cosmic Pantry
        if (data.cosmic_pantry) {
            document.getElementById('gen-pantry-profile').innerText = data.cosmic_pantry.taste_profile;
            document.getElementById('gen-pantry-food').innerText = data.cosmic_pantry.favorite_food;
            document.getElementById('gen-pantry-habit').innerText = data.cosmic_pantry.food_habit;
        }

        // 6. Render Astro Decor / Tata Letak Ruang
        if (data.astro_decor) {
            document.getElementById('gen-decor-style').innerText = data.astro_decor.style;
            document.getElementById('gen-decor-elements').innerText = data.astro_decor.key_elements;
            document.getElementById('gen-decor-vibe').innerText = data.astro_decor.vibe;
        }

        // 7. Render Fun Fact
        document.getElementById('gen-fun-fact-text').innerText = data.fun_fact;
    }

    // Tombol kembali ke grid zodiak di layar mobile
    const btnBackGen = document.getElementById('btn-back-grid-gen');
    if (btnBackGen) {
        btnBackGen.addEventListener('click', () => {
            const zodiacGrid = document.getElementById('zodiac-grid');
            if (zodiacGrid) {
                zodiacGrid.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    }
});
