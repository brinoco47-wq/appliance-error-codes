/* Appliance Error Codes & Troubleshooting — vanilla JS.
   Homepage search reads the embedded #search-index JSON.
   Category / all-codes pages filter their pre-rendered cards. No network, no tracking. */
(function () {
  'use strict';

  // Mobile navigation
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  function norm(s) {
    return (s || '').toUpperCase().replace(/[\s\-_]/g, '');
  }

  // ---- Homepage hero search ----
  var form = document.getElementById('hero-search');
  var indexEl = document.getElementById('search-index');
  if (form && indexEl) {
    var index = JSON.parse(indexEl.textContent);
    var results = document.getElementById('search-results');
    var codeInput = document.getElementById('q-code');
    var appSel = document.getElementById('q-appliance');
    var mfrSel = document.getElementById('q-mfr');
    var clearBtn = document.getElementById('q-clear');

    function render(list, query) {
      if (!list.length) {
        results.innerHTML = '<div class="result-card"><h3>No exact match found</h3>'
          + '<p>Try the code exactly as shown on the display (for example, E15), pick the appliance and manufacturer, '
          + 'or <a href="codes/">browse all verified codes</a>. Codes vary by brand and model — if your code is not listed, '
          + 'your model\u2019s manual is the right source. See also <a href="guides/how-to-read-an-error-code.html">how to read an error code</a>.</p></div>';
        return;
      }
      var q = norm(query);
      var html = '';
      list.slice(0, 30).forEach(function (e) {
        var exact = q && (norm(e.code) === q || e.aliases.some(function (a) { return norm(a) === q; }));
        html += '<article class="result-card">' + (exact ? '<span class="badge">Exact match</span>' : '<span class="badge">Related</span>')
          + '<h3><a href="' + e.url + '">' + e.manufacturer + ' ' + e.code + ' — ' + e.title + '</a></h3>'
          + '<p>' + e.appliance_label + ' · ' + e.manufacturer + '</p></article>';
      });
      results.innerHTML = html;
    }

    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var q = codeInput.value.trim();
      var qn = norm(q);
      var app = appSel.value;
      var mfr = mfrSel.value;
      var pool = index.filter(function (e) {
        if (app && e.appliance_label !== app) return false;
        if (mfr && e.manufacturer !== mfr) return false;
        return true;
      });
      var exact = [], partial = [];
      pool.forEach(function (e) {
        if (qn && (norm(e.code) === qn || e.aliases.some(function (a) { return norm(a) === qn; }))) exact.push(e);
        else if (!qn) partial.push(e);
        // Partial matches only on the code itself (e.g. E1 -> E15), never on
        // title words — otherwise unrelated codes surface as "related".
        else if (norm(e.code).indexOf(qn) !== -1) partial.push(e);
      });
      render(exact.concat(partial), q);
    });
    if (clearBtn) clearBtn.addEventListener('click', function () {
      form.reset();
      results.innerHTML = '';
      codeInput.focus();
    });
  }

  // ---- Category / all-codes list filtering ----
  var fCode = document.getElementById('f-code');
  var fMfr = document.getElementById('f-mfr');
  if (fCode) {
    var cards = Array.prototype.slice.call(document.querySelectorAll('.code-card'));
    var noRes = document.getElementById('no-results');
    var clear = document.getElementById('f-clear');
    function apply() {
      var q = norm(fCode.value);
      var m = fMfr ? fMfr.value : '';
      var visible = 0;
      cards.forEach(function (card) {
        var ok = (!q || norm(card.getAttribute('data-code')).indexOf(q) !== -1)
          && (!m || card.getAttribute('data-mfr') === m);
        card.style.display = ok ? '' : 'none';
        if (ok) visible++;
      });
      if (noRes) noRes.hidden = visible !== 0;
      document.querySelectorAll('.code-group').forEach(function (g) {
        var any = Array.prototype.some.call(g.querySelectorAll('.code-card'), function (c) { return c.style.display !== 'none'; });
        g.style.display = any ? '' : 'none';
      });
    }
    fCode.addEventListener('input', apply);
    if (fMfr) fMfr.addEventListener('change', apply);
    if (clear) clear.addEventListener('click', function () {
      fCode.value = '';
      if (fMfr) fMfr.value = '';
      apply();
      fCode.focus();
    });
  }
})();
