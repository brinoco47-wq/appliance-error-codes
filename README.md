# Appliance Error Codes & Troubleshooting

A free, independent, static guide to household appliance error codes: what they
mean, what usually causes them, and which safe checks to try first. No backend,
no database, no build step — plain HTML, CSS, and vanilla JavaScript.

## Contents

- `index.html` — homepage with working search (code + appliance + manufacturer)
- `categories/` — one page per appliance category, with filters
- `codes/` — one SEO-friendly detail page per verified error code
- `guides/` — general troubleshooting guides
- `about.html`, `contact.html`, `privacy.html`, `terms.html`, `disclaimer.html`
- `sitemap.html`, `sitemap.xml`, `robots.txt`, `404.html`
- `assets/css/styles.css`, `assets/js/search.js`, `assets/img/logo.svg`
- `data/codes.json` — the single source of truth for error-code entries
- `tools/build.py` — the generator that renders every page from `data/codes.json`

## Editing content

1. **Add or fix an error code:** edit `data/codes.json`, then run:
   `python3 tools/build.py`
   Every page, the search index, and both sitemaps regenerate from that file.
2. **Add a guide:** add an entry to the `GUIDES` list in `tools/build.py` and
   rebuild.
3. **Add a category:** add an entry to `CATEGORIES` in `tools/build.py` and
   rebuild. Categories with no verified codes automatically show an honest
   "no entries yet" state instead of guessed codes.

## Content rules (do not break these)

- Never publish a manufacturer-specific error-code meaning that has not been
  verified against at least two published sources (manufacturer manuals or
  support pages preferred). If it cannot be verified, leave it out.
- Never claim coverage of every manufacturer or every code.
- Never invent parts, prices, model compatibility, reviews, ratings, or
  credentials. Keep placeholders visibly marked as placeholders.
- Safety warnings stay on every code page. Gas, high-voltage, and sealed-system
  work is always referred to qualified technicians.

## Deploying on GitHub Pages

1. Push this folder to a repository (as the repository root).
2. Repository → Settings → Pages → Build and deployment → Deploy from a branch
   → branch `main`, folder `/ (root)`.
3. The site works under a project subpath (`<user>.github.io/<repo>/`) because
   every internal link is relative — no configuration needed.

## Before launch — placeholders to replace

- `https://example.com/` in `tools/build.py` (`CANON_BASE`), `robots.txt`, and
  `sitemap.xml` — replace with the real domain or GitHub Pages URL, then rebuild.
- The contact email on `contact.html` — currently `[to be added — placeholder]`.
- Ad slots: empty `<div class="ad-slot">` blocks marked `AD PLACEHOLDER` in the
  generated HTML. Paste your ad network's code inside them only. No ad scripts
  are loaded by default, and slots are styled to look fine while empty.

## Testing

After a rebuild, check: homepage search (exact + partial + no-results),
category filters, every internal link, mobile layout (narrow viewport), and
keyboard focus order. A link checker that flags missing targets:

`python3 - <<'EOF'
import os, re
root = '.'
missing = []
for dp, _, fs in os.walk(root):
    if 'tools' in dp: continue
    for f in fs:
        if not f.endswith('.html'): continue
        p = os.path.join(dp, f)
        html = open(p).read()
        for href in re.findall(r'href="([^"#]+)"', html):
            if href.startswith(('http', 'mailto:')): continue
            t = os.path.normpath(os.path.join(dp, href))
            if os.path.isdir(t): t = os.path.join(t, 'index.html')
            if not os.path.exists(t): missing.append((p, href))
print('missing:', missing if missing else 'none')
EOF`
