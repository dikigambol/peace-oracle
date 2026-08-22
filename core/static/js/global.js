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
});
