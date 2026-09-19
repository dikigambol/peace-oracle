document.addEventListener('DOMContentLoaded', () => {
    const SHIO_NAMES = {
        tikus: 'Tikus 鼠', kerbau: 'Kerbau 牛', macan: 'Macan 虎', kelinci: 'Kelinci 兔',
        naga: 'Naga 龍', ular: 'Ular 蛇', kuda: 'Kuda 馬', kambing: 'Kambing 羊',
        monyet: 'Monyet 猴', ayam: 'Ayam 雞', anjing: 'Anjing 狗', babi: 'Babi 豬'
    };
    const SHIO_ORDER = ['tikus','kerbau','macan','kelinci','naga','ular','kuda','kambing','monyet','ayam','anjing','babi'];

    const viewSelect = document.getElementById('view-select');
    const viewResult = document.getElementById('view-result');
    const yearlyCard = document.getElementById('yearly-card');
    const btnCheck = document.getElementById('btn-check');
    const backBtn = document.getElementById('back-to-select');
    const yearNum = document.getElementById('year-number');
    const yearLabel = document.getElementById('year-shio-label');
    const btnPrev = document.getElementById('year-prev');
    const btnNext = document.getElementById('year-next');

    let selectedShio = null;
    const picker = document.querySelector('.year-picker');
    const seededYear = picker ? parseInt(picker.dataset.currentYear, 10) : NaN;
    let currentYear = Number.isFinite(seededYear)
        ? seededYear
        : new Date().getFullYear();

    function getYearShio(year) {
        const idx = ((year - 4) % 12 + 12) % 12;
        return SHIO_ORDER[idx];
    }

    function updateYearDisplay() {
        yearNum.textContent = currentYear;
        const yearShio = getYearShio(currentYear);
        yearLabel.textContent = `Tahun ${SHIO_NAMES[yearShio] || yearShio}`;
    }

    updateYearDisplay();

    btnPrev.addEventListener('click', () => { currentYear--; updateYearDisplay(); });
    btnNext.addEventListener('click', () => { currentYear++; updateYearDisplay(); });

    document.querySelectorAll('.shio-item').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.shio-item').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            selectedShio = btn.dataset.shio;
            btnCheck.disabled = false;
        });
    });

    btnCheck.addEventListener('click', () => {
        if (!selectedShio) return;
        fetchYearly(selectedShio, currentYear);
    });

    backBtn.addEventListener('click', () => {
        viewResult.classList.add('hidden');
        viewResult.classList.remove('active');
        viewSelect.classList.remove('hidden');
        viewSelect.classList.add('active');
        yearlyCard.classList.add('hidden');
        document
            .querySelectorAll('.shio-item')
            .forEach((b) => b.classList.remove('selected'));
        selectedShio = null;
        if (btnCheck) btnCheck.disabled = true;
    });

    function fetchYearly(shio, year) {
        viewSelect.classList.add('hidden');
        viewSelect.classList.remove('active');
        viewResult.classList.remove('hidden');
        viewResult.classList.add('active');
        yearlyCard.classList.add('hidden');

        fetch('/api/shio/yearly', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ shio: shio, year: year })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error && !data.user_shio) {
                alert(data.error);
                backBtn.click();
                return;
            }

            document.getElementById('y-user-hanzi').textContent = data.user_shio ? data.user_shio.hanzi : '';
            document.getElementById('y-user-name').textContent = data.user_shio ? data.user_shio.name : '';
            document.getElementById('y-year-hanzi').textContent = data.year_shio ? data.year_shio.hanzi : '';
            document.getElementById('y-year-name').textContent = data.year_shio ? data.year_shio.name : '';
            document.getElementById('y-year-num').textContent = data.year !== undefined ? data.year : '';

            const relation = data.relation || {};
            const badge = document.getElementById('y-relation-badge');
            badge.textContent = relation.hanzi
                ? relation.hanzi + ' \u00b7 ' + (relation.name_id || relation.label || '')
                : relation.name_id || relation.label || '';
            badge.className = 'yearly-badge code-' + (relation.code || 'neutral');
            const taiSui = document.getElementById('y-relation-taisui');
            taiSui.textContent = relation.tai_sui || '';
            taiSui.classList.toggle('hidden', !relation.tai_sui);
            document.getElementById('y-relation-note').textContent = relation.note || '';

            const stem = data.stem_layer || {};
            document.getElementById('y-stem-pillar').textContent = stem.year_pillar || '';
            document.getElementById('y-stem-summary').textContent = stem.summary || '';
            document.getElementById('y-stem-advice').textContent = stem.advice || '';
            document.getElementById('y-stem').className =
                'yearly-stem role-' + (stem.role || 'setara');

            document.getElementById('yearly-lichun').textContent =
                data.lichun_note || '';

            document.getElementById('y-saran').textContent = data.saran_utama || '';
            document.getElementById('y-saran-box').style.display = data.saran_utama ? 'flex' : 'none';

            document.getElementById('y-karir').textContent = data.karir || '-';
            document.getElementById('y-keuangan').textContent = data.keuangan || '-';
            document.getElementById('y-asmara').textContent = data.asmara || '-';
            document.getElementById('y-kesehatan').textContent = data.kesehatan || '-';

            document.querySelectorAll('.yearly-cat').forEach(el => {
                el.style.animation = 'none';
                el.offsetHeight;
                el.style.animation = '';
            });

            yearlyCard.classList.remove('hidden');

            setTimeout(() => {
                yearlyCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 100);
        })
        .catch(err => {
            console.error('Gagal memuat proyeksi:', err);
            alert('Terjadi gangguan energi kosmik. Silakan coba lagi.');
            backBtn.click();
        });
    }

  const canvas = document.getElementById('particle-canvas');
  if (canvas) {
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
        this.color = Math.random() > 0.5 ? '#ffd700' : '#ff4500';
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
    let isDragging = false;
    const shioBg = document.getElementById('shio-bg');
    if (shioBg) {
      shioBg.addEventListener('mousedown', (e) => {
        isDragging = true;
        createParticles(e.clientX, e.clientY);
      });
      shioBg.addEventListener('mousemove', (e) => {
        if (isDragging) {
          for (let i = 0; i < 5; i++) {
            particles.push(new Particle(e.clientX, e.clientY));
          }
        }
      });
      window.addEventListener('mouseup', () => {
        isDragging = false;
      });
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
    }
  }
});
