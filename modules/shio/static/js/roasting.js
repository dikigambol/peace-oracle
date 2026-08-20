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

    // Fetch Fortune Logic (Mocked for Coming Soon)
    function fetchFortune(shioKey, elementKey) {
        // Just show the result card
        const resTitle = document.getElementById('res-title');
        if (resTitle) {
            const shioName = document.querySelector(`.shio-item[data-shio="${shioKey}"] .name`).textContent;
            const elName = document.querySelector(`.element-item[data-element="${elementKey}"] .name`).textContent;
            resTitle.textContent = `${shioName} ${elName}`;
            resTitle.style.color = getComputedStyle(document.documentElement).getPropertyValue(`--${elementKey}-color`) || '#ffd700';
        }
        
        const resultCard = document.getElementById('main-fortune-card');
        resultCard.classList.remove('hidden');
        setTimeout(() => resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100);
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
