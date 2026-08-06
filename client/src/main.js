import './style.css';

// ── Config ───────────────────────────────────────────────────────
const API_BASE = '/server';  // Proxied through Vite
const BACKEND_URL = 'http://localhost';  // For display/copy

// ── Icons (inline SVGs) ──────────────────────────────────────────
const icons = {
  link: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>`,
  copy: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>`,
  check: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>`,
  alert: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`,
  clock: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
  click: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 9h.01"/><rect width="18" height="18" x="3" y="3" rx="2"/><path d="m15 15-6-6"/></svg>`,
  arrowRight: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>`,
  externalLink: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>`,
  linkLogo: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>`,
};

// ── State ────────────────────────────────────────────────────────
let isLoading = false;
let result = null;
let error = null;
let history = loadHistory();

// ── History persistence ──────────────────────────────────────────
function loadHistory() {
  try {
    return JSON.parse(localStorage.getItem('urlx_history') || '[]');
  } catch {
    return [];
  }
}

function saveHistory(entry) {
  // Avoid duplicates
  history = history.filter(h => h.short_url !== entry.short_url);
  history.unshift(entry);
  // Keep max 5
  history = history.slice(0, 5);
  localStorage.setItem('urlx_history', JSON.stringify(history));
}

// ── API ──────────────────────────────────────────────────────────
async function shortenUrl(originalUrl) {
  const response = await fetch(`${API_BASE}/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ original_url: originalUrl }),
  });

  if (!response.ok) {
    const data = await response.json().catch(() => null);
    throw new Error(data?.detail || `Server error (${response.status})`);
  }

  return await response.json();
}

// ── Clipboard ────────────────────────────────────────────────────
async function copyToClipboard(text, btnElement) {
  try {
    await navigator.clipboard.writeText(text);
    btnElement.classList.add('action-btn--copied');
    btnElement.innerHTML = `${icons.check} Copied`;
    setTimeout(() => {
      btnElement.classList.remove('action-btn--copied');
      btnElement.innerHTML = `${icons.copy} Copy`;
    }, 2000);
  } catch {
    // Fallback
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
  }
}

// ── Format date ──────────────────────────────────────────────────
function formatDate(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
}

// ── Build short URL display ──────────────────────────────────────
function getShortUrl(code) {
  return `${BACKEND_URL}/${code}`;
}

// ── Render ───────────────────────────────────────────────────────
function render() {
  const app = document.getElementById('app');

  app.innerHTML = `
    <div class="container">
      <!-- Header -->
      <header class="header">
        <div class="header__logo">
          ${icons.linkLogo}
        </div>
        <h1 class="header__title">urlX</h1>
        <p class="header__subtitle">Paste a long URL and get a clean, short link instantly.</p>
      </header>

      <!-- Input -->
      <div class="input-area">
        <form id="shorten-form" class="input-wrapper">
          <div class="input-wrapper__icon">${icons.link}</div>
          <input
            id="url-input"
            class="url-input"
            type="url"
            placeholder="Paste your URL here…"
            required
            autocomplete="off"
            spellcheck="false"
            ${isLoading ? 'disabled' : ''}
          />
          <button id="submit-btn" class="submit-btn" type="submit" ${isLoading ? 'disabled' : ''}>
            ${isLoading ? '<span class="spinner"></span>' : `Shorten ${icons.arrowRight}`}
          </button>
        </form>

        ${error ? `
          <div class="error-msg" id="error-msg">
            ${icons.alert}
            <span>${error}</span>
          </div>
        ` : ''}

        ${result ? `
          <div class="result-card" id="result-card">
            <div class="result-card__label">Your shortened URL</div>
            <div class="result-card__url-display">
              <span class="result-card__url">${getShortUrl(result.short_url)}</span>
            </div>
            <div class="result-card__actions">
              <button class="action-btn" id="copy-btn">
                ${icons.copy} Copy
              </button>
              <a class="action-btn action-btn--open" id="open-btn" href="${getShortUrl(result.short_url)}" target="_blank" rel="noopener noreferrer">
                ${icons.externalLink} Open
              </a>
            </div>
            <div class="result-card__meta">
              <div class="result-card__meta-item">
                ${icons.clock}
                <span>${formatDate(result.created_at)}</span>
              </div>
              <div class="result-card__meta-item">
                ${icons.click}
                <span>${result.click_count} click${result.click_count !== 1 ? 's' : ''}</span>
              </div>
            </div>
            <div class="result-card__original-section">
              <div class="result-card__original-label">Original URL</div>
              <div class="result-card__original-url" title="${result.original_url}">${result.original_url}</div>
            </div>
          </div>
        ` : ''}
      </div>

      ${history.length > 0 ? `
        <div class="history">
          <div class="history__title">Recent links</div>
          ${history.map((item, i) => `
            <div class="history__item" data-index="${i}" id="history-item-${i}">
              <div class="history__item-urls">
                <span class="history__item-short">${item.short_url}</span>
                <span class="history__item-original">${item.original_url}</span>
              </div>
              <div class="history__item-actions">
                <button class="history__item-btn" data-url="${getShortUrl(item.short_url)}" aria-label="Copy short URL" id="history-copy-${i}">
                  ${icons.copy}
                </button>
                <a class="history__item-btn" href="${getShortUrl(item.short_url)}" target="_blank" rel="noopener noreferrer" aria-label="Open short URL" id="history-open-${i}">
                  ${icons.externalLink}
                </a>
              </div>
            </div>
          `).join('')}
        </div>
      ` : ''}

      <!-- Footer -->
      <footer class="footer">
        Built by Aneesh
      </footer>
    </div>
  `;

  // ── Event listeners ──────────────────────────────────────────
  const form = document.getElementById('shorten-form');
  form.addEventListener('submit', handleSubmit);

  const copyBtn = document.getElementById('copy-btn');
  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      copyToClipboard(getShortUrl(result.short_url), copyBtn);
    });
  }

  // History copy buttons
  document.querySelectorAll('.history__item-btn[data-url]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const url = btn.dataset.url;
      copyToClipboard(url, btn);
    });
  });

  // History open links - stop propagation so they don't trigger the item click
  document.querySelectorAll('.history__item-btn[href]').forEach(link => {
    link.addEventListener('click', (e) => {
      e.stopPropagation();
    });
  });

  // Click history item to populate input
  document.querySelectorAll('.history__item').forEach(item => {
    item.addEventListener('click', () => {
      const idx = parseInt(item.dataset.index);
      const entry = history[idx];
      result = entry;
      error = null;
      render();
    });
  });

  // Auto-focus input
  const input = document.getElementById('url-input');
  if (input && !isLoading) {
    input.focus();
  }
}

// ── Submit handler ───────────────────────────────────────────────
async function handleSubmit(e) {
  e.preventDefault();
  const input = document.getElementById('url-input');
  const url = input.value.trim();

  if (!url) return;

  isLoading = true;
  error = null;
  result = null;
  render();

  try {
    const data = await shortenUrl(url);
    result = data;
    saveHistory({
      short_url: data.short_url,
      original_url: data.original_url,
      created_at: data.created_at,
      click_count: data.click_count,
    });
    history = loadHistory();
  } catch (err) {
    error = err.message || 'Something went wrong. Please try again.';
  } finally {
    isLoading = false;
    render();
  }
}

// ── Initial render ───────────────────────────────────────────────
render();
