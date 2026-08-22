// ============================================================
// STRICT MULTI-LAYER CLIENT DEVICE FINGERPRINT & FETCH INTERCEPTOR
// ============================================================
(function() {
    function getOrCreateDeviceId() {
        let deviceId = '';
        try {
            deviceId = localStorage.getItem('zodiak_device_id') || '';
        } catch (e) {}

        if (!deviceId || deviceId.length < 8) {
            if (window.crypto && window.crypto.randomUUID) {
                deviceId = window.crypto.randomUUID();
            } else {
                deviceId = 'dev_' + Date.now().toString(36) + '_' + Math.random().toString(36).substring(2, 10);
            }
            try {
                localStorage.setItem('zodiak_device_id', deviceId);
            } catch (e) {}
        }
        try {
            document.cookie = `_z_device_id=${deviceId}; path=/; max-age=31536000; SameSite=Lax`;
        } catch (e) {}
        return deviceId;
    }

    const deviceId = getOrCreateDeviceId();

    const originalFetch = window.fetch;
    window.fetch = function(url, options) {
        options = options || {};
        options.headers = options.headers || {};

        if (options.headers instanceof Headers) {
            if (!options.headers.has('X-Device-Id')) {
                options.headers.append('X-Device-Id', deviceId);
            }
        } else if (typeof options.headers === 'object') {
            if (!options.headers['X-Device-Id']) {
                options.headers['X-Device-Id'] = deviceId;
            }
        }

        return originalFetch.call(this, url, options);
    };
})();

// Global AI Quota Toast Notification Function
window.showAiQuotaToast = function(message) {
    if (!message) return;
    let toast = document.getElementById('ai-quota-toast');
    if (toast) toast.remove();

    toast = document.createElement('div');
    toast.id = 'ai-quota-toast';
    toast.innerHTML = `
        <div class="ai-quota-toast-card">
            <div class="ai-quota-toast-icon">
                <i class="fa-solid fa-lock"></i>
            </div>
            <div class="ai-quota-toast-msg">${message}</div>
            <button type="button" class="ai-quota-toast-close" onclick="this.closest('#ai-quota-toast').remove()" aria-label="Tutup">&times;</button>
        </div>
    `;
    document.body.appendChild(toast);

    setTimeout(() => {
        if (toast && toast.parentElement) {
            toast.remove();
        }
    }, 7000);
};

document.addEventListener('DOMContentLoaded', () => {
    // Hide Loader on Window Load
    window.addEventListener('load', () => {
        setTimeout(() => {
            const loader = document.getElementById('global-loader');
            if (loader) {
                loader.classList.add('hidden');
            }
        }, 500); // 500ms delay for aesthetics
    });

    // Mobile & Desktop Click/Tap Toggle for Floating Mode Switcher
    const modeSwitcherToggle = document.getElementById('mode-switcher-toggle');
    const modeSwitcherContainer = document.querySelector('.mode-switcher-container');

    if (modeSwitcherToggle && modeSwitcherContainer) {
        modeSwitcherToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            modeSwitcherContainer.classList.toggle('active');
        });

        // Close mode switcher menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!modeSwitcherContainer.contains(e.target)) {
                modeSwitcherContainer.classList.remove('active');
            }
        });
    }
});
