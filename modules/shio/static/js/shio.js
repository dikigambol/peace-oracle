document.addEventListener('DOMContentLoaded', () => {
    // Initialize Flatpickr for premium date selection
    flatpickr("#birthdate-input", {
        theme: "dark",
        locale: "id",
        dateFormat: "Y-m-d",
        altInput: true,
        altFormat: "j F Y",
        allowInput: false,
        maxDate: "today",
        disableMobile: "true"
    });

    // UI State Management
    const views = {
        selection: document.getElementById('view-selection'),
        shioList: document.getElementById('view-shio-list'),
        elementList: document.getElementById('view-element-list'),
        result: document.getElementById('view-result'),
        auto: document.getElementById('view-auto')
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

    document.getElementById('btn-manual').addEventListener('click', () => {
        switchView('shioList');
    });

    // View 1.5 (Auto) Handlers
    document.getElementById('back-to-start-from-auto').addEventListener('click', () => switchView('selection'));
    
    document.getElementById('btn-calculate').addEventListener('click', () => {
        const dateVal = document.getElementById('birthdate-input').value;
        if (!dateVal) {
            alert("Harap masukkan tanggal lahir Anda!");
            return;
        }
        
        const year = new Date(dateVal).getFullYear();
        if (isNaN(year)) return;

        const shios = ["monyet", "ayam", "anjing", "babi", "tikus", "kerbau", "macan", "kelinci", "naga", "ular", "kuda", "kambing"];
        const elements = ["logam", "logam", "air", "air", "kayu", "kayu", "api", "api", "tanah", "tanah"];
        
        selectedShio = shios[year % 12];
        const selectedElement = elements[year % 10];
        
        fetchFortune(selectedShio, selectedElement);
        switchView('result');
    });

    // View 2 Handlers
    document.getElementById('back-to-sel').addEventListener('click', () => switchView('selection'));
    
    document.querySelectorAll('.shio-item').forEach(btn => {
        btn.addEventListener('click', (e) => {
            selectedShio = e.currentTarget.dataset.shio;
            switchView('elementList');
        });
    });

    // View 3 Handlers
    document.getElementById('back-to-shio').addEventListener('click', () => switchView('shioList'));
    
    document.querySelectorAll('.element-card').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const selectedElement = e.currentTarget.dataset.element;
            fetchFortune(selectedShio, selectedElement);
            switchView('result');
        });
    });

    // View 4 Handlers
    document.getElementById('back-to-start').addEventListener('click', () => switchView('selection'));

    // Fetch API
    function fetchFortune(shio, element) {
        document.getElementById('res-fortune').textContent = "Menghubungkan ke kosmik oriental...";
        
        fetch('/api/shio/fortune', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ shio, element })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('res-title').textContent = data.title;
            document.getElementById('res-fortune').textContent = data.fortune;
            document.getElementById('res-traits').textContent = data.traits;
            document.getElementById('res-vibe').textContent = data.vibe;
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
