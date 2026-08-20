document.addEventListener('DOMContentLoaded', () => {
    const btnCalc = document.getElementById('btn-calculate-compatibility-large');
    const quickViz = document.getElementById('quick-viz');
    const resultCircle = document.getElementById('result-svg-circle-large');
    const resultStatus = document.getElementById('result-status-large');

    const instructionPanel = document.getElementById('comp-details-instruction');
    const contentPanel = document.getElementById('comp-details-content');

    const badgeOne = document.getElementById('comp-badge-one');
    const badgeTwo = document.getElementById('comp-badge-two');
    const narrativeText = document.getElementById('comp-narrative');

    const loveBar = document.getElementById('param-love-bar');
    const commBar = document.getElementById('param-comm-bar');
    const trustBar = document.getElementById('param-trust-bar');
    const futureBar = document.getElementById('param-future-bar');

    const lovePercent = document.getElementById('param-love-percent');
    const commPercent = document.getElementById('param-comm-percent');
    const trustPercent = document.getElementById('param-trust-percent');
    const futurePercent = document.getElementById('param-future-percent');

    const strengthsList = document.getElementById('comp-strengths-list');
    const challengesList = document.getElementById('comp-challenges-list');

    // Pill Mode Hubungan
    const modePills = document.querySelectorAll('.relation-pill');
    let currentMode = 'romance';
    let lastFetchedData = null;

    const elemClassMap = {
        api: 'fire',
        tanah: 'earth',
        udara: 'air',
        air: 'water'
    };

    // Handler klik pill mode hubungan
    modePills.forEach(pill => {
        pill.addEventListener('click', () => {
            modePills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            currentMode = pill.getAttribute('data-mode') || 'romance';

            // Jika data sudah di-fetch, perbarui tampilan secara instan tanpa fetch ulang
            if (lastFetchedData) {
                renderSelectedMode(lastFetchedData, currentMode);
            }
        });
    });

    btnCalc.addEventListener('click', async () => {
        const signOne = document.getElementById('sign-one-select-large').value;
        const signTwo = document.getElementById('sign-two-select-large').value;

        if (!signOne || !signTwo) {
            alert('Harap pilih kedua zodiak terlebih dahulu.');
            return;
        }

        try {
            // Panggil API Backend Flask
            const response = await fetch(`/zodiak/api/compatibility/${signOne}/${signTwo}`);
            if (!response.ok) throw new Error('Gagal memproses kecocokan zodiak');

            const data = await response.json();
            lastFetchedData = data;
            displayCompatibilityDetails(data);
        } catch (err) {
            console.error(err);
            alert('Gagal memuat analisis kecocokan. Silakan coba lagi.');
        }
    });

    function displayCompatibilityDetails(data) {
        // Tampilkan panel detail hasil & visualisasi
        quickViz.classList.remove('hidden');
        instructionPanel.classList.add('hidden');
        contentPanel.classList.remove('hidden');

        // Setel Elemen Badges di Panel Kanan
        const clsOne = elemClassMap[data.element_one.toLowerCase()] || 'fire';
        const clsTwo = elemClassMap[data.element_two.toLowerCase()] || 'water';

        badgeOne.className = `element-badge ${clsOne}`;
        badgeOne.innerText = data.element_one;

        badgeTwo.className = `element-badge ${clsTwo}`;
        badgeTwo.innerText = data.element_two;

        // Render mode hubungan yang terpilih
        renderSelectedMode(data, currentMode);
    }

    function renderSelectedMode(data, mode) {
        // Ambil data mode terpilih (romance / friendship / work)
        const modeInfo = (data.modes && data.modes[mode]) ? data.modes[mode] : {
            score: data.score || 75,
            status: data.status || 'Harmonis',
            summary: data.narrative || '',
            strengths: data.strengths || [],
            challenges: data.challenges || [],
            metrics: { love: data.love || 80, comm: data.communication || 80, trust: data.trust || 80, future: data.future || 80 }
        };

        const score = modeInfo.score;

        // 1. Animasi Lingkaran Kemajuan SVG
        const circumference = 251.2;
        resultCircle.style.strokeDasharray = circumference;
        resultCircle.style.strokeDashoffset = circumference;

        setTimeout(() => {
            const offsetValue = circumference - (circumference * score) / 100;
            resultCircle.style.strokeDashoffset = offsetValue;

            // Atur warna lingkaran berdasarkan persentase
            if (score >= 85) {
                resultCircle.style.stroke = '#10b981'; // Hijau
            } else if (score >= 70) {
                resultCircle.style.stroke = '#3b82f6'; // Biru
            } else if (score >= 55) {
                resultCircle.style.stroke = '#f59e0b'; // Amber
            } else {
                resultCircle.style.stroke = '#ef4444'; // Merah
            }
        }, 50);

        // Animasi angka persentase utama
        animateCount('result-percentage-large', score);
        resultStatus.innerText = modeInfo.status;

        // 2. Setel Teks Narasi Penjelasan Detil
        narrativeText.innerText = modeInfo.summary;

        // 3. Reset & Animasi Progress Bar untuk Detail Parameter
        loveBar.style.width = '0%';
        commBar.style.width = '0%';
        trustBar.style.width = '0%';
        futureBar.style.width = '0%';

        lovePercent.innerText = '0%';
        commPercent.innerText = '0%';
        trustPercent.innerText = '0%';
        futurePercent.innerText = '0%';

        const m = modeInfo.metrics;

        setTimeout(() => {
            loveBar.style.width = `${m.love}%`;
            commBar.style.width = `${m.comm}%`;
            trustBar.style.width = `${m.trust}%`;
            futureBar.style.width = `${m.future}%`;

            animateCount('param-love-percent', m.love);
            animateCount('param-comm-percent', m.comm);
            animateCount('param-trust-percent', m.trust);
            animateCount('param-future-percent', m.future);
        }, 150);

        // 4. Render Daftar Kekuatan dan Tantangan Hubungan
        strengthsList.innerHTML = '';
        challengesList.innerHTML = '';

        modeInfo.strengths.forEach(strength => {
            const li = document.createElement('li');
            li.innerText = strength;
            strengthsList.appendChild(li);
        });

        modeInfo.challenges.forEach(challenge => {
            const li = document.createElement('li');
            li.innerText = challenge;
            challengesList.appendChild(li);
        });
    }

    // Helper untuk menganimasikan penghitungan teks angka
    function animateCount(elementId, targetValue) {
        const element = document.getElementById(elementId);
        if (!element) return;
        let current = 0;
        const duration = 800; // 0.8s
        if (targetValue === 0) {
            element.innerText = '0%';
            return;
        }
        const stepTime = Math.abs(Math.floor(duration / targetValue));

        const timer = setInterval(() => {
            current += 1;
            element.innerText = `${current}%`;
            if (current >= targetValue) {
                clearInterval(timer);
                element.innerText = `${targetValue}%`;
            }
        }, stepTime);
    }
});
