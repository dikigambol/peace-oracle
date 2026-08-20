document.addEventListener('DOMContentLoaded', () => {
    // Initialize Flatpickr for dates
    flatpickr("#birthdate-input", { dateFormat: "d F Y", theme: "dark" });
    flatpickr("#comp-date1", { dateFormat: "d F Y", theme: "dark" });
    flatpickr("#comp-date2", { dateFormat: "d F Y", theme: "dark" });

    // Populate Time Dropdowns
    function populateTimeDropdowns(hourId, minuteId) {
        const hSelect = document.getElementById(hourId);
        const mSelect = document.getElementById(minuteId);
        if (!hSelect || !mSelect) return;
        
        for(let i=0; i<=23; i++) {
            let opt = document.createElement('option');
            let val = i.toString().padStart(2, '0');
            opt.value = val; opt.text = val;
            hSelect.add(opt);
        }
        for(let i=0; i<=59; i++) {
            let opt = document.createElement('option');
            let val = i.toString().padStart(2, '0');
            opt.value = val; opt.text = val;
            mSelect.add(opt);
        }
    }
    
    populateTimeDropdowns("bt-hour", "bt-minute");
    populateTimeDropdowns("c1-hour", "c1-minute");
    populateTimeDropdowns("c2-hour", "c2-minute");

    const currentYear = new Date().getFullYear();
    const SHIOS_ARR = ["monyet", "ayam", "anjing", "babi", "tikus", "kerbau", "macan", "kelinci", "naga", "ular", "kuda", "kambing"];
    const ELEMENTS_ARR = ["logam", "logam", "air", "air", "kayu", "kayu", "api", "api", "tanah", "tanah"];
    
    // Helper to capitalize first letter
    const capitalize = (s) => s.charAt(0).toUpperCase() + s.slice(1);
    
    document.getElementById('yearly-subtitle').textContent = `Proyeksi Kosmik ${currentYear}`;
    document.getElementById('yearly-desc').textContent = `Masukkan tahun lahir Anda untuk melihat ramalan energi kosmik pada tahun berjalan (${currentYear} - ${capitalize(SHIOS_ARR[currentYear % 12])} ${capitalize(ELEMENTS_ARR[currentYear % 10])}).`;

    // UI State Management
    const views = {
        selection: document.getElementById('view-selection'),
        shioList: document.getElementById('view-shio-list'),
        elementList: document.getElementById('view-element-list'),
        result: document.getElementById('view-result'),
        auto: document.getElementById('view-auto'),
        yearly: document.getElementById('view-yearly'),
        compatibility: document.getElementById('view-compatibility'),
        daily: document.getElementById('view-daily')
    };

    let selectedShio = null;

    function switchView(viewName) {
        Object.values(views).forEach(v => {
            if (v) {
                v.classList.remove('active');
                v.classList.add('hidden');
            }
        });
        if (views[viewName]) {
            views[viewName].classList.remove('hidden');
            setTimeout(() => views[viewName].classList.add('active'), 10);
        }
    }

    // View 1 Handlers
    document.getElementById('btn-date').addEventListener('click', () => {
        switchView('auto');
    });



    document.getElementById('btn-yearly').addEventListener('click', () => switchView('yearly'));
    document.getElementById('btn-compatibility').addEventListener('click', () => switchView('compatibility'));
    document.getElementById('btn-daily').addEventListener('click', () => {
        switchView('daily');
        fetchDailyAlmanak();
    });

    // View 1.5 (Auto) Handlers
    document.getElementById('back-to-start-from-auto').addEventListener('click', () => {
        document.getElementById('main-fortune-card').classList.add('hidden');
        switchView('selection');
    });
    
    document.getElementById('btn-calculate').addEventListener('click', () => {
        const dateVal = document.getElementById('birthdate-input').value;
        
        if (!dateVal) {
            alert("Gulungan takdir tidak bisa dibaca tanpa jejak tanggal yang utuh!");
            return;
        }
        
        const year = parseInt(dateVal.split(' ').pop());
        
        const selectedShio = SHIOS_ARR[year % 12];
        const selectedElement = ELEMENTS_ARR[year % 10];
        
        const hVal = document.getElementById('bt-hour').value;
        const minVal = document.getElementById('bt-minute').value;
        const timeVal = (hVal && minVal) ? `${hVal}:${minVal}` : "";
        
        const formattedDate = dateVal;
        
        // Clear inputs after successful read
        document.getElementById('birthdate-input')._flatpickr.clear();
        document.getElementById('bt-hour').selectedIndex = 0;
        document.getElementById('bt-minute').selectedIndex = 0;
        
        fetchFortune(selectedShio, selectedElement, formattedDate, timeVal);
        
        const resultCard = document.getElementById('main-fortune-card');
        document.getElementById('view-auto').appendChild(resultCard);
        resultCard.classList.remove('hidden');
        
        // Scroll to result
        setTimeout(() => resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100);
    });

    // View 4 Handlers
    const backToStart = document.getElementById('back-to-start');
    if (backToStart) {
        backToStart.addEventListener('click', () => switchView('selection'));
    }



    // View 5 (Yearly) Handlers
    document.getElementById('back-to-start-from-yearly').addEventListener('click', () => {
        document.getElementById('yearly-result').classList.add('hidden');
        switchView('selection');
    });
    document.getElementById('btn-calc-yearly').addEventListener('click', () => {
        const year = document.getElementById('yearly-year-input').value;
        if (!year) return alert("Tahun kedatangan Anda ke bumi diperlukan untuk meneropong masa depan!");
        
        const userShio = SHIOS_ARR[year % 12];
        const currentYear = new Date().getFullYear();
        
        fetch('/api/shio/yearly', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ shio: userShio, year: currentYear })
        })
        .then(res => res.json())
        .then(data => {
            // Clear input
            document.getElementById('yearly-year-input').value = "";
            
            document.getElementById('res-yearly-title').textContent = `${data.user_shio} di Tahun ${data.year_shio}`;
            document.getElementById('res-yearly-status').textContent = data.status;
            document.getElementById('res-yearly-score').textContent = data.score;
            document.getElementById('res-yearly-desc').textContent = data.description;
            
            const resultDiv = document.getElementById('yearly-result');
            resultDiv.classList.remove('hidden');
            setTimeout(() => resultDiv.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100);
        });
    });

    // View 6 (Compatibility) Handlers
    document.getElementById('back-to-start-from-comp').addEventListener('click', () => {
        document.getElementById('comp-result').classList.add('hidden');
        switchView('selection');
    });
    document.getElementById('btn-calc-comp').addEventListener('click', () => {
        const date1 = document.getElementById('comp-date1').value;
        const date2 = document.getElementById('comp-date2').value;
        
        if (!date1 || !date2) {
            return alert("Garis waktu kedua pihak harus lengkap untuk menimbang keharmonisan!");
        }
        
        const year1 = parseInt(date1.split(' ').pop());
        const year2 = parseInt(date2.split(' ').pop());
        
        const h1 = document.getElementById('c1-hour').value;
        const min1 = document.getElementById('c1-minute').value;
        const time1 = (h1 && min1) ? `${h1}:${min1}` : "";
        
        const h2 = document.getElementById('c2-hour').value;
        const min2 = document.getElementById('c2-minute').value;
        const time2 = (h2 && min2) ? `${h2}:${min2}` : "";
        
        fetch('/api/shio/compatibility', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                shio1: SHIOS_ARR[year1 % 12], 
                shio2: SHIOS_ARR[year2 % 12],
                element1: ELEMENTS_ARR[year1 % 10],
                element2: ELEMENTS_ARR[year2 % 10],
                time1: time1,
                time2: time2
            })
        })
        .then(res => res.json())
        .then(data => {
            // Clear inputs
            document.getElementById('comp-date1')._flatpickr.clear();
            document.getElementById('c1-hour').selectedIndex = 0;
            document.getElementById('c1-minute').selectedIndex = 0;
            document.getElementById('comp-date2')._flatpickr.clear();
            document.getElementById('c2-hour').selectedIndex = 0;
            document.getElementById('c2-minute').selectedIndex = 0;
            
            document.getElementById('res-comp-title').innerText = `${data.s1_name} & ${data.s2_name}`;
            document.getElementById('res-comp-shio').innerText = data.shio_relation;
            document.getElementById('res-comp-elem').innerText = data.elem_relation;
            document.getElementById('res-comp-score').innerText = data.score;
            document.getElementById('res-comp-status').innerText = data.status;
            document.getElementById('res-comp-asmara').innerText = data.desc_asmara;
            document.getElementById('res-comp-bisnis').innerText = data.desc_bisnis;
            
            const secretRow = document.getElementById('res-comp-secret-row');
            if(data.secret_relation) {
                document.getElementById('res-comp-secret').innerText = data.secret_relation;
                secretRow.classList.remove('hidden');
            } else {
                secretRow.classList.add('hidden');
            }
            
            const resultDiv = document.getElementById('comp-result');
            resultDiv.classList.remove('hidden');
            setTimeout(() => resultDiv.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100);
        });
    });

    // View 7 (Daily Almanak) Handlers
    document.getElementById('back-to-start-from-daily').addEventListener('click', () => switchView('selection'));

    function fetchDailyAlmanak() {
        const grid = document.getElementById('daily-grid');
        grid.innerHTML = '<div style="text-align:center; width:100%; color:#ffd700;"><i class="fa-solid fa-spinner fa-spin fa-2x"></i><p>Menyelaraskan Energi Hari Ini...</p></div>';
        
        const now = new Date();
        const dateStr = `${now.getFullYear()}-${now.getMonth() + 1}-${now.getDate()}`;
        
        fetch(`/api/shio/daily?date=${dateStr}`)
            .then(res => res.json())
            .then(data => {
                document.getElementById('daily-master-name').textContent = data.today_shio_name;
                document.getElementById('daily-master-icon').innerHTML = `<span class="icon-hanzi">${data.today_shio_hanzi}</span>`;
                document.getElementById('daily-date-str').textContent = data.date_str;
                
                grid.innerHTML = ''; // clear loading
                
                data.fortunes.forEach(item => {
                    const card = document.createElement('div');
                    card.className = `daily-card status-${item.status_code}`;
                    
                    card.innerHTML = `
                        <div class="daily-card-header">
                            <span class="daily-card-icon icon-hanzi">${item.hanzi}</span>
                            <h3 class="daily-card-name">${item.name}</h3>
                        </div>
                        <div class="daily-card-status">${item.status}</div>
                        <p class="daily-card-message">${item.message}</p>
                        ${item.daily_tip ? `<div class="daily-card-tip"><i class="fa-solid fa-lightbulb"></i> <span>${item.daily_tip}</span></div>` : ''}
                    `;
                    grid.appendChild(card);
                });
            })
            .catch(err => {
                grid.innerHTML = '<p style="color:red; text-align:center;">Gagal memuat ramalan harian.</p>';
            });
    }

    // Fetch API
    function fetchFortune(shio, element, birthdateStr = null, timeStr = null) {
        document.getElementById('res-fortune').textContent = "Menghubungkan ke kosmik oriental...";
        
        const badge = document.getElementById('auto-result-badge');
        if (birthdateStr) {
            document.getElementById('res-birthdate').textContent = "Lahir: " + birthdateStr;
            badge.classList.remove('hidden');
        } else {
            badge.classList.add('hidden');
        }
        
        fetch('/api/shio/fortune', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ shio, element, time: timeStr })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('res-title').textContent = data.title;
            document.getElementById('res-fortune').textContent = data.fortune;
            document.getElementById('res-traits').textContent = data.traits;
            document.getElementById('res-vibe').textContent = data.vibe;
            
            if (data.secret_animal) {
                document.getElementById('res-secret-animal').textContent = data.secret_animal;
                document.getElementById('res-secret-wrapper').style.display = 'block';
            } else {
                document.getElementById('res-secret-wrapper').style.display = 'none';
            }
            
            document.getElementById('res-karir').textContent = data.karir;
            document.getElementById('res-keuangan').textContent = data.keuangan;
            document.getElementById('res-asmara').textContent = data.asmara;
            document.getElementById('res-kesehatan').textContent = data.kesehatan;
            document.getElementById('res-dir').textContent = data.lucky_direction;
            document.getElementById('res-num').textContent = data.lucky_numbers.join(', ');
        })
        .catch(err => {
            document.getElementById('res-fortune').textContent = "Gagal membaca takdir. Coba lagi.";
            document.getElementById('res-karir').textContent = "-";
            document.getElementById('res-keuangan').textContent = "-";
            document.getElementById('res-asmara').textContent = "-";
            document.getElementById('res-kesehatan').textContent = "-";
        });
    }

    // --- INTERACTIVE BACKGROUND (EASTER EGG) ---
    const canvas = document.getElementById('particle-canvas');
    const ctx = canvas.getContext('2d');
    let particles = [];

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    class Particle {
        constructor(x, y) {
            this.x = x;
            this.y = y;
            this.size = Math.random() * 5 + 2;
            this.speedX = Math.random() * 6 - 3;
            this.speedY = Math.random() * 6 - 3;
            this.color = Math.random() > 0.5 ? '#ffd700' : '#ff4500'; // Gold or Red-orange
            this.life = 1.0;
            this.decay = Math.random() * 0.02 + 0.02;
        }
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            this.life -= this.decay;
        }
        draw() {
            ctx.globalAlpha = this.life;
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
            ctx.globalAlpha = 1.0;
        }
    }

    function createParticles(x, y) {
        for (let i = 0; i < 30; i++) {
            particles.push(new Particle(x, y));
        }
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < particles.length; i++) {
            particles[i].update();
            particles[i].draw();
            if (particles[i].life <= 0) {
                particles.splice(i, 1);
                i--;
            }
        }
        requestAnimationFrame(animate);
    }
    animate();

    // Trigger on click and drag anywhere on the container
    let isDragging = false;
    
    const shioBg = document.getElementById('shio-bg');

    shioBg.addEventListener('mousedown', (e) => {
        isDragging = true;
        createParticles(e.clientX, e.clientY);
    });

    shioBg.addEventListener('mousemove', (e) => {
        if (isDragging) {
            // Create fewer particles on drag to prevent lag
            for (let i = 0; i < 5; i++) {
                particles.push(new Particle(e.clientX, e.clientY));
            }
        }
    });

    window.addEventListener('mouseup', () => {
        isDragging = false;
    });
    
    // Support for touch devices
    shioBg.addEventListener('touchstart', (e) => {
        isDragging = true;
        const touch = e.touches[0];
        createParticles(touch.clientX, touch.clientY);
    });
    
    shioBg.addEventListener('touchmove', (e) => {
        if (isDragging) {
            const touch = e.touches[0];
            for (let i = 0; i < 5; i++) {
                particles.push(new Particle(touch.clientX, touch.clientY));
            }
        }
    });
    
    window.addEventListener('touchend', () => {
        isDragging = false;
    });
});
