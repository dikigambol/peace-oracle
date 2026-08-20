document.addEventListener('DOMContentLoaded', () => {
    const views = {
        shioList: document.getElementById('view-shio-list'),
        elementList: document.getElementById('view-element-list'),
        result: document.getElementById('view-result')
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

    // View 2 Handlers (Manual Shio Selection)
    document.querySelectorAll('.shio-item').forEach(btn => {
        btn.addEventListener('click', (e) => {
            selectedShio = e.currentTarget.dataset.shio;
            switchView('elementList');
        });
    });

    // View 3 Handlers (Element Selection)
    document.getElementById('back-to-shio').addEventListener('click', () => switchView('shioList'));
    
    document.querySelectorAll('.element-card').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const selectedElement = e.currentTarget.dataset.element;
            fetchFortune(selectedShio, selectedElement);
            
            const resultCard = document.getElementById('main-fortune-card');
            resultCard.classList.remove('hidden');
            switchView('result');
            
            // Scroll to result slightly delayed to allow transition
            setTimeout(() => {
                const container = document.querySelector('.shio-content-wrapper');
                if (container) container.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 100);
        });
    });

    // View 4 Handlers (Result)
    document.getElementById('back-to-start').addEventListener('click', () => {
        selectedShio = null;
        switchView('shioList');
    });

    // Fetch Fortune Logic
    function fetchFortune(shioKey, elementKey) {
        const payload = { shio: shioKey, element: elementKey };
        
        fetch('/api/shio/fortune', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            // Update title
            const resTitle = document.getElementById('res-title');
            if (resTitle) {
                resTitle.textContent = data.title;
                resTitle.style.color = getComputedStyle(document.documentElement).getPropertyValue(`--${elementKey}-color`) || '#ffd700';
            }
            
            document.getElementById('res-fortune').textContent = data.fortune;
            document.getElementById('res-traits').textContent = data.traits;
            document.getElementById('res-vibe').textContent = data.vibe;
            
            const secretWrapper = document.getElementById('res-secret-wrapper');
            if (secretWrapper) {
                if (data.secret_animal) {
                    secretWrapper.style.display = 'block';
                    document.getElementById('res-secret-animal').textContent = data.secret_animal;
                } else {
                    secretWrapper.style.display = 'none';
                }
            }

            document.getElementById('res-karir').textContent = data.karir;
            document.getElementById('res-keuangan').textContent = data.keuangan;
            document.getElementById('res-asmara').textContent = data.asmara;
            document.getElementById('res-kesehatan').textContent = data.kesehatan;
            
            document.getElementById('res-dir').textContent = data.lucky_direction;
            document.getElementById('res-num').textContent = data.lucky_numbers.join(', ');
        })
        .catch(err => {
            console.error("Gagal mendapatkan ramalan:", err);
            alert("Terjadi gangguan energi kosmik. Silakan coba lagi.");
        });
    }

    // Optional Easter Egg Canvas (same as in shio.js)
    const canvas = document.getElementById('particle-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        // Simple starfield
        for (let i = 0; i < 100; i++) {
            ctx.fillStyle = `rgba(255, 255, 255, ${Math.random()})`;
            ctx.beginPath();
            ctx.arc(Math.random() * canvas.width, Math.random() * canvas.height, Math.random() * 2, 0, Math.PI * 2);
            ctx.fill();
        }
    }
});
