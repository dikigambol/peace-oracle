/**
 * Oraculum Zodiacalis — Elegant Celestial Vector Sigils
 * Handcrafted SVG vectors for the 12 Zodiac signs.
 * Eliminates cheap system emoji rendering (e.g. Windows purple emoji boxes).
 */

const ZODIAC_SVG_PATHS = {
  aries: '<path d="M12 21V8M12 8C10 5 6 4 4 7C2 10 4 13 6 13M12 8C14 5 18 4 20 7C22 10 20 13 18 13" />',
  taurus: '<circle cx="12" cy="14" r="6" /><path d="M6 5C7 8 10 9 12 9C14 9 17 8 18 5" />',
  gemini: '<path d="M5 4C9 6 15 6 19 4M5 20C9 18 15 18 19 20M9 5V19M15 5V19" />',
  cancer: '<circle cx="7" cy="8" r="3" /><path d="M10 8C14 8 18 10 18 13" /><circle cx="17" cy="16" r="3" /><path d="M14 16C10 16 6 14 6 11" />',
  leo: '<circle cx="7" cy="15" r="3" /><path d="M9.5 13.5C10.5 8 15 6 17 9C19 12 17 18 20 18" />',
  virgo: '<path d="M4 6V17M4 10C4 7 8 7 8 10V17M8 10C8 7 12 7 12 10V17M12 10C12 7 16 7 16 10V16C16 19 14 20 13 20M14 14L18 20" />',
  libra: '<path d="M4 19H20M4 15H8C8 11.5 10 10 12 10C14 10 16 11.5 16 15H20" />',
  scorpio: '<path d="M4 6V17M4 10C4 7 8 7 8 10V17M8 10C8 7 12 7 12 10V17C12 17 14 17 16 15M16 11V18L19 15M16 18H19" />',
  sagittarius: '<path d="M6 18L18 6M18 6H12M18 6V12M9 15L15 9" />',
  capricorn: '<path d="M5 7L10 17L14 8C15 6 18 6 19 8C20 10 18 13 16 14C14 15 14 19 17 19C19 19 20 17 20 15" />',
  aquarius: '<path d="M4 9L7 7L10 9L13 7L16 9L19 7M4 15L7 13L10 15L13 13L16 15L19 13" />',
  pisces: '<path d="M6 4C9 8 9 16 6 20M18 4C15 8 15 16 18 20M4 12H20" />'
};

window.getZodiacSvg = function (signKey, size = 28) {
  const key = String(signKey || 'aries').toLowerCase().trim();
  const path = ZODIAC_SVG_PATHS[key] || ZODIAC_SVG_PATHS.aries;
  return `
    <svg class="celestial-sigil-svg" viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
      ${path}
    </svg>
  `;
};

// Auto-populate any element with data-zodiac-icon
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-zodiac-icon]").forEach(el => {
    const sign = el.getAttribute("data-zodiac-icon");
    const size = parseInt(el.getAttribute("data-icon-size") || "24", 10);
    el.innerHTML = window.getZodiacSvg(sign, size);
  });
});
