#!/usr/bin/env python3
"""Builds the Appliance Error Codes & Troubleshooting static site.

Reads data/codes.json (verified error-code entries) and emits every HTML page,
sitemap.html and sitemap.xml. All links are RELATIVE so the site works under
any GitHub Pages subdirectory (or a custom domain) without changes.

Usage: python3 tools/build.py
"""
import json, os, re, html as htmllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "data", "codes.json")))
CODES = DATA["codes"]
SITE = DATA["site_name"]
CANON_BASE = "https://example.com/"  # PLACEHOLDER: replace with the real domain before launch (see README.md)

CATEGORIES = [
    ("washing-machines", "Washing Machines", "Front-load and top-load washers. The most common codes are water, drain, balance, and door faults — most have a simple first check.",
     '<circle cx="32" cy="32" r="26"/><circle cx="32" cy="32" r="11"/><circle cx="52" cy="14" r="3"/>'),
    ("refrigerators-freezers", "Refrigerators & Freezers", "Fridges, freezers, and ice makers. Verified error-code entries for this category are being added — start with the guides below.",
     '<rect x="18" y="8" width="28" height="48" rx="3"/><line x1="18" y1="26" x2="46" y2="26"/><line x1="40" y1="14" x2="40" y2="20"/><line x1="40" y1="32" x2="40" y2="40"/>'),
    ("dishwashers", "Dishwashers", "Built-in and portable dishwashers. Drain, leak, and fill faults dominate — most are a filter, a hose, or a float switch.",
     '<rect x="14" y="8" width="36" height="48" rx="3"/><line x1="20" y1="20" x2="44" y2="20"/><line x1="20" y1="30" x2="44" y2="30"/><line x1="20" y1="40" x2="44" y2="40"/>'),
    ("ovens-ranges", "Ovens & Ranges", "Wall ovens, ranges, and cooktops. Verified error-code entries for this category are being added — start with the guides below.",
     '<rect x="12" y="10" width="40" height="44" rx="3"/><rect x="20" y="20" width="24" height="18" rx="2"/><line x1="18" y1="16" x2="26" y2="16"/>'),
    ("microwaves", "Microwaves", "Countertop and over-range microwaves. Verified error-code entries for this category are being added — start with the guides below.",
     '<rect x="10" y="14" width="44" height="36" rx="3"/><rect x="16" y="20" width="20" height="24" rx="2"/><path d="M40 24h4M40 30h4M40 36h4"/>'),
    ("dryers", "Clothes Dryers", "Electric and gas dryers. Airflow warnings (Flow Sense and friends) are the most urgent codes a dryer can show — they are fire-safety alerts.",
     '<circle cx="32" cy="32" r="26"/><path d="M32 18v6M22 26l5 3M42 26l-5 3"/><path d="M24 44c4-4 12-4 16 0"/>'),
    ("air-conditioners", "Air Conditioners", "Split, window, and portable air conditioners. Verified error-code entries for this category are being added — start with the guides below.",
     '<path d="M32 8v48M12 20l40 24M52 20L12 44"/><circle cx="32" cy="32" r="5"/>'),
    ("water-heaters", "Water Heaters", "Tank, tankless, and heat-pump water heaters. Verified error-code entries for this category are being added — start with the guides below.",
     '<path d="M22 10h20v34a10 10 0 0 1-20 0z"/><path d="M26 22h12M26 30h12"/><path d="M32 54c-3 4 3 4 0 0"/>'),
]
CAT = {c[0]: c for c in CATEGORIES}
CAT_LABEL = {c[0]: c[1] for c in CATEGORIES}

def esc(s):
    return htmllib.escape(str(s), quote=True)

def icon(svg_inner):
    return ('<svg class="cat-icon" viewBox="0 0 64 64" fill="none" stroke="currentColor" '
            'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + svg_inner + '</svg>')

def logo_svg():
    return ('<svg class="logo-mark" viewBox="0 0 48 48" role="img" aria-label="Appliance Error Codes &amp; Troubleshooting logo">'
            '<rect x="6" y="4" width="36" height="40" rx="5" fill="#1d4ed8"/>'
            '<circle cx="24" cy="25" r="9" fill="none" stroke="#fff" stroke-width="2.5"/>'
            '<path d="M24 21v4l3 2" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>'
            '<circle cx="37" cy="37" r="9" fill="#16a34a" stroke="#fff" stroke-width="2"/>'
            '<path d="M33.5 37l2.5 2.5 4.5-5" stroke="#fff" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            '</svg>')

def header(prefix, current=""):
    nav = [("", "Home"), ("codes/", "Error Codes"), ("categories/", "Appliances"),
           ("guides/", "Troubleshooting"), ("about.html", "About"), ("contact.html", "Contact")]
    links = ""
    for href, label in nav:
        # nav targets live at root; from a subpage they need ../
        full = (prefix + href) if href else (prefix if prefix else "index.html")
        if href == "":
            full = prefix + "index.html" if prefix else "index.html"
        cls = ' aria-current="page"' if label.lower().replace(" ", "") == current else ""
        links += f'<a href="{full}"{cls}>{label}</a>'
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap header-in">
<a class="brand" href="{prefix}index.html">{logo_svg()}<span>Appliance Error Codes <em>&amp; Troubleshooting</em></span></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav">Menu</button>
<nav id="main-nav" class="site-nav" aria-label="Main">{links}</nav>
</div></header>'''

def footer(prefix):
    return f'''<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div><h3>About this site</h3><p>An independent, free guide to household appliance error codes. We are not affiliated with, or endorsed by, any appliance manufacturer. Meanings vary by model — always confirm in your exact model's manual.</p></div>
<div><h3>Browse</h3><ul>
<li><a href="{prefix}index.html">Home</a></li>
<li><a href="{prefix}categories/">All appliances</a></li>
<li><a href="{prefix}codes/">All error codes</a></li>
<li><a href="{prefix}guides/">Troubleshooting guides</a></li>
</ul></div>
<div><h3>Site</h3><ul>
<li><a href="{prefix}about.html">About Us</a></li>
<li><a href="{prefix}contact.html">Contact</a></li>
<li><a href="{prefix}privacy.html">Privacy Policy</a></li>
<li><a href="{prefix}terms.html">Terms of Use</a></li>
<li><a href="{prefix}disclaimer.html">Disclaimer</a></li>
<li><a href="{prefix}sitemap.html">Sitemap</a></li>
</ul></div>
</div>
<p class="foot-base">© 2026 Appliance Error Codes &amp; Troubleshooting. General guidance only — not a substitute for your model's manual or a qualified technician.</p>
</div></footer>'''

def crumbs(prefix, items):
    lis = "".join(f'<li><a href="{u}">{esc(t)}</a></li>' if u else f'<li aria-current="page">{esc(t)}</li>'
                     for t, u in items)
    return f'<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>{lis}</ol></div></nav>'

def ad_slot(label):
    return f'''<!-- AD PLACEHOLDER: paste your ad network code (e.g. Adsterra) inside this div. Leave empty until then; the layout holds. -->
<div class="ad-slot" role="complementary" aria-label="Advertisement"><span class="ad-label">Advertisement</span></div>'''

def page(prefix, title, desc, h1, body, current="", crumbs_html="", extra_head=""):
    canon = CANON_BASE  # page-level canonicals are filled in by the caller via extra_head when known
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<link rel="stylesheet" href="{prefix}assets/css/styles.css">
{extra_head}</head>
<body>
{header(prefix, current)}
{crumbs_html}
<main id="main" class="wrap">{body}</main>
{footer(prefix)}
<script src="{prefix}assets/js/search.js"></script>
</body>
</html>
'''

def code_card(prefix, c, badge=""):
    return (f'<article class="card code-card" data-code="{esc(c["code"])}" data-mfr="{esc(c["manufacturer"])}" '
            f'data-cat="{esc(c["appliance"])}">'
            f'<p class="code-big">{esc(c["code"])}</p>'
            f'<h3><a href="{prefix}codes/{c["slug"]}.html">{esc(c["manufacturer"])} {esc(c["code"])} — {esc(c["title"])}</a></h3>'
            f'<p>{esc(c["appliance_label"])} · {esc(c["manufacturer"])}</p>'
            f'<p class="card-meaning">{esc(c["meaning"][:150])}…</p>{badge}</article>')

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print("wrote", os.path.relpath(path, ROOT))

GUIDES = [
    ("how-to-read-an-error-code", "How to Read an Appliance Error Code", "2026-10-20",
     "What the letters and numbers mean, why the same code can differ by brand, and what to note down before you search.",
     """<p>An error code is your appliance's way of pointing at a problem area — it is a clue, not a diagnosis. Most codes combine a letter (the system: water, drain, door, motor) with a number (the specific fault). The same code on two brands can mean different things, and sometimes the same brand reuses a code across model families with different meanings.</p>
<h2>Before you search: note three things</h2>
<ol>
<li><strong>The exact code, exactly as shown.</strong> Case matters on some machines (LG's lowercase <em>uE</em> and uppercase <em>UE</em> are different stages of the same problem). Photograph the display if you can.</li>
<li><strong>Brand and appliance type.</strong> A washer code and a dishwasher code that look alike are unrelated.</li>
<li><strong>Your model number.</strong> It turns a generic code page into the right answer for your machine. See <a href="find-your-model-number.html">how to find your model number</a>.</li>
</ol>
<h2>What a code can and cannot tell you</h2>
<p>A code can tell you <em>which system</em> reported a problem — water inlet, drain, door lock, motor, vent. It cannot tell you <em>which part</em> has failed. A drain code, for example, can be a kinked hose, a blocked filter, or a dead pump. Work through the cheap, visible causes first before assuming a part has failed.</p>
<h2>When the same code appears on another brand</h2>
<p>Never carry a meaning across brands. For example, LE on an LG washer means a locked or overloaded motor. Other brands use the same letters for other faults. Always search by brand <em>and</em> appliance together — that is why this site's search asks for both.</p>
<h2>What to do with a code you cannot find here</h2>
<p>Check your model's manual first (search the model number plus the code). If the code is not documented anywhere, treat it as a prompt to call the manufacturer's support line with the model number ready — not as permission to open the machine.</p>"""),
    ("find-your-model-number", "How to Find Your Appliance Model Number", "2026-10-19",
     "Where the rating plate lives on washers, dryers, fridges, dishwashers, ovens, and water heaters.",
     """<p>Nearly every error-code answer depends on the model number. Manufacturers reuse codes across model families, so the model number is what turns a generic page into the right answer. It is printed on a rating plate (also called a serial plate) somewhere on the machine.</p>
<h2>Where to look, by appliance</h2>
<ul>
<li><strong>Washing machine:</strong> inside the door frame, on the back panel, or behind the detergent drawer.</li>
<li><strong>Dryer:</strong> inside the door opening, or on the back panel.</li>
<li><strong>Refrigerator:</strong> on an inside wall of the fridge or freezer compartment, or on the side of the door.</li>
<li><strong>Dishwasher:</strong> on the edge of the door, or on the side wall of the tub (visible when the door is open).</li>
<li><strong>Oven / range:</strong> on the door frame, behind the storage drawer, or on the back.</li>
<li><strong>Water heater:</strong> on a label on the side of the tank, or the front of a tankless unit.</li>
<li><strong>Air conditioner:</strong> on a side or rear panel label.</li>
</ul>
<h2>What to write down</h2>
<p>Copy the full model number and the serial number, exactly as printed — including any suffix letters. A photo of the plate is even better: support lines and parts lookups use the exact string. If the plate is worn, a photo taken at an angle with a flashlight often reveals it.</p>
<h2>If you cannot find the plate</h2>
<p>Check the original manual, the purchase receipt, or the manufacturer's app if the appliance was registered. As a last resort, the brand's support line can sometimes identify a model from a photo of the control panel — but a rating-plate photo is always faster.</p>"""),
    ("before-you-troubleshoot", "What to Do Before Troubleshooting an Appliance", "2026-10-18",
     "The five-minute safety routine: power, water, gas, and when to stop.",
     """<p>Most appliance injuries happen before the repair starts — on a machine that is still powered, still connected to water, or still hot. Run this routine first, every time.</p>
<h2>1. Cut the power</h2>
<p>Unplug the appliance. If the plug is not reachable, switch the circuit off at the breaker and confirm the machine is dead (no lights, no display). Never work on a machine that is only switched off at its own controls — internal parts can still be live.</p>
<h2>2. Cut the water</h2>
<p>For washers and dishwashers, turn the supply taps off before disconnecting any hose, and keep towels and a tray ready. A litre or more of water hides in hoses and filters.</p>
<h2>3. Mind the gas</h2>
<p>For gas dryers, ovens, and water heaters, know where the gas shut-off is before you start. If you smell gas at any point: do not touch electrical switches, leave the building, and call your gas utility or emergency services from outside.</p>
<h2>4. Let it cool</h2>
<p>Ovens, dryers, and water heaters stay dangerously hot long after they stop. Give them time, and test with the back of your hand near — never on — the surface.</p>
<h2>5. Know your stop line</h2>
<p>Decide in advance what you will not do: no opening sealed panels, no bypassing safety switches or door locks, no touching gas valves or high-voltage parts without qualifications. See <a href="when-to-call-a-technician.html">when to call a qualified technician</a>.</p>"""),
    ("when-to-call-a-technician", "When to Call a Qualified Technician", "2026-10-17",
     "The signs that mean stop: burning smells, repeated codes, gas, water near electrics, and sealed systems.",
     """<p>DIY checks fix a large share of appliance faults — blocked filters, kinked hoses, unbalanced loads. Some signs mean the safe move is to stop and call a professional.</p>
<h2>Stop and call if you see any of these</h2>
<ul>
<li><strong>A burning smell, scorch marks, or smoke.</strong> Unplug (if safe to reach the plug) and do not run the machine again.</li>
<li><strong>The same code returns immediately</strong> after every basic check. The cause is a failed part or sensor, not a blockage.</li>
<li><strong>Water anywhere near electrics</strong> — a leak onto a motor, control board, or outlet.</li>
<li><strong>Gas work of any kind</strong> — valves, connectors, burners, or a suspected leak.</li>
<li><strong>Sealed refrigeration systems</strong> — compressors, refrigerant lines, and sealed-system repairs need licensed handling.</li>
<li><strong>High-voltage parts</strong> — microwave capacitors hold a dangerous charge even unplugged; oven and dryer heating circuits are not beginner work.</li>
<li><strong>The machine is under warranty.</strong> Opening it can void the warranty — call the manufacturer first.</li>
</ul>
<h2>What to tell the technician</h2>
<p>Have ready: the exact error code, the model number, what you already checked, and when the fault appears (every cycle, only on spin, only when hot). That short list often saves a second visit.</p>"""),
    ("reset-an-appliance-safely", "How to Reset an Appliance Safely", "2026-10-16",
     "What a power cycle does, what it cannot fix, and when resetting is the wrong move.",
     """<p>A reset (usually a power cycle: unplug, wait, plug back in) clears the machine's electronics back to a known state. It fixes one-off glitches — a sensor hiccup after a power cut, a control confused by a voltage dip. It does not fix blockages, leaks, or broken parts.</p>
<h2>The safe power-cycle routine</h2>
<ol>
<li>Switch the appliance off at its own controls.</li>
<li>Unplug it (or switch the breaker off if the plug is unreachable).</li>
<li>Wait at least one full minute so the electronics discharge.</li>
<li>Plug back in, switch on, and run a short cycle.</li>
<li>Watch whether the code returns immediately, later in the cycle, or not at all — that timing is useful information.</li>
</ol>
<h2>When resetting is the wrong move</h2>
<ul>
<li><strong>An active leak.</strong> Resetting a dishwasher showing a leak code just lets it leak again.</li>
<li><strong>A burning smell or scorching.</strong> Do not power it back up.</li>
<li><strong>A gas smell.</strong> Do not touch switches at all — leave and call the gas utility.</li>
<li><strong>A dryer airflow warning (d90/d95).</strong> The vent is still blocked; running it again is a fire risk.</li>
</ul>
<h2>If the code returns straight away</h2>
<p>The fault is still present. Work through the code's own checks on this site instead of resetting repeatedly — repeated resets hide nothing and fix nothing.</p>"""),
]
GUIDE = {g[0]: g for g in GUIDES}

SIMPLE_PAGES = {
    "about": ("About Us", "Who runs this site, how error-code meanings are verified, and what this site is not.",
     """<p>Appliance Error Codes &amp; Troubleshooting is an independent, free information site. It exists for one job: help you understand the code on your appliance's display, work out the likely cause, and decide what to do next.</p>
<h2>How our content is written</h2>
<p>Error-code meanings on this site are cross-checked against multiple published sources, including manufacturer user manuals and manufacturer support pages where available. Where sources disagree, or where a meaning depends on the exact model, we say so rather than pick a confident-sounding answer. We never invent manufacturer-specific meanings, model compatibility, parts, prices, or official citations.</p>
<h2>What this site is not</h2>
<ul>
<li>We are not affiliated with, endorsed by, or sponsored by any appliance manufacturer.</li>
<li>We are not a repair service and we do not take bookings.</li>
<li>We do not claim to cover every manufacturer or every error code. Categories and codes are added as they are verified.</li>
<li>Nothing here replaces your model's official manual or a qualified technician's judgment.</li>
</ul>
<h2>Corrections</h2>
<p>If you spot a wrong meaning, tell us via the <a href="contact.html">contact page</a> with the brand, model, and code. Corrections are made as soon as they are verified.</p>"""),
    "contact": ("Contact", "How to reach this site, and what to include in a correction report.",
     """<p>This site is run as an independent information project. We do not offer phone support or a repair booking service.</p>
<h2>Contact details</h2>
<p><strong>Email:</strong> [to be added — placeholder]</p>
<p class="note">The contact email address is intentionally left as a placeholder until the site owner publishes one. Please do not send personal details, photos of rating plates, or account information to any address found elsewhere claiming to be this site.</p>
<h2>Reporting a correction</h2>
<p>If an error-code meaning on this site is wrong for your model, include: the brand, the full model number, the exact code as displayed, and what your model's manual says it means. That is enough for us to verify and correct the page.</p>
<h2>What we cannot help with</h2>
<p>We cannot diagnose an individual appliance by message, recommend a specific repairer, or quote repair prices. For a fault that needs hands-on work, see <a href="guides/when-to-call-a-technician.html">when to call a qualified technician</a>.</p>"""),
    "privacy": ("Privacy Policy", "What this site collects (nothing by default), and what changes if advertising is added later.",
     """<p>This site is a static information website. It has no accounts, no login, and no comment system.</p>
<h2>What we collect</h2>
<p>Nothing, by default. Reading a page, using the on-site search, and filtering lists all happen in your browser — search terms are not sent to us or to any server.</p>
<h2>Server logs</h2>
<p>Like most websites, the hosting provider may keep standard server logs (such as the page requested and the time) for security and reliability. We do not control those logs and we do not use them to identify visitors.</p>
<h2>Advertising</h2>
<p>No advertising code is currently loaded on this site. If advertising is added in future, this policy will be updated to name the network and what it collects, before any ad code goes live.</p>
<h2>External links</h2>
<p>Links to manufacturer manuals and support pages leave this site. Their privacy practices are their own — check their policies before sharing personal details with them.</p>
<h2>Changes</h2>
<p>Material changes to this policy will be noted here with a new date.</p>
<p class="note">Last updated: 20 October 2026.</p>"""),
    "terms": ("Terms of Use", "The rules for using this free information site.",
     """<p>By using this site you agree to these terms. If you do not agree, please do not use the site.</p>
<h2>Informational use only</h2>
<p>All content is general information, not professional advice. It is not a substitute for your appliance's official manual, the manufacturer's support, or a qualified technician.</p>
<h2>Accuracy</h2>
<p>We verify error-code meanings against multiple sources, but codes vary by brand and model, and documentation changes. We do not guarantee that any page matches your exact model. Confirm critical information in your model's manual before acting on it.</p>
<h2>Your responsibility</h2>
<p>You are responsible for your own safety. Do not open energized appliances, bypass safety systems, or handle gas or high-voltage components without appropriate qualifications. See the <a href="disclaimer.html">Disclaimer</a> for the full safety notice.</p>
<h2>Content reuse</h2>
<p>Text on this site may be quoted with attribution and a link back. Do not republish whole pages, and do not present this site's content as your own or as manufacturer documentation.</p>
<h2>Liability</h2>
<p>To the extent permitted by law, this site is provided “as is” without warranties of any kind, and we are not liable for loss or damage arising from reliance on its content or from any repair you undertake.</p>"""),
    "disclaimer": ("Disclaimer", "Safety first: general guidance only, codes vary by model, and some jobs are for qualified technicians only.",
     """<p class="warning"><strong>Safety notice:</strong> Troubleshooting information on this site is general guidance only. Error-code meanings vary by brand and model, and a wrong guess on a gas, water, or high-voltage appliance can cause injury or property damage. Always consult your exact model's official manual first.</p>
<h2>What this site does not do</h2>
<ul>
<li>It does not diagnose your individual appliance.</li>
<li>It does not replace a manufacturer's manual, a warranty service, or a qualified technician.</li>
<li>It does not cover every manufacturer, model, or code — absence of a code here does not mean the code is unimportant.</li>
</ul>
<h2>Do not do these things</h2>
<ul>
<li>Do not open an energized appliance or work on live electrical parts.</li>
<li>Do not bypass safety systems, door locks, thermal cut-outs, or float switches.</li>
<li>Do not handle gas valves, gas connectors, or sealed refrigeration systems without appropriate qualifications.</li>
<li>Do not run a machine that smells of burning, leaks water onto electrics, or shows a severe airflow warning.</li>
</ul>
<h2>If you smell gas</h2>
<p>Do not touch electrical switches or phones inside the building. Leave immediately and call your gas utility or emergency services from outside.</p>
<h2>When in doubt, stop</h2>
<p>If a step feels unsafe, is not in your model's manual, or needs a tool you do not understand, stop and call a qualified technician. See <a href="guides/when-to-call-a-technician.html">when to call a qualified technician</a>.</p>"""),
}

def manufacturers_for(appliance=None):
    ms = sorted({c["manufacturer"] for c in CODES if appliance is None or c["appliance"] == appliance})
    return ms

def options(items, label):
    out = f'<option value="">{label}</option>'
    for it in items:
        out += f'<option value="{esc(it)}">{esc(it)}</option>'
    return out

def build_home():
    cats_html = ""
    for slug, name, desc, svg in CATEGORIES:
        n = len([c for c in CODES if c["appliance"] == slug])
        note = f"{n} verified code page{'s' if n != 1 else ''}" if n else "Guides available — codes being verified"
        cats_html += (f'<article class="card cat-card"><a href="categories/{slug}.html" class="card-link">'
                      f'{icon(svg)}<h3>{esc(name)}</h3><p>{esc(desc)}</p><p class="card-meta">{note} →</p></a></article>')
    recent = sorted(GUIDES, key=lambda g: g[2], reverse=True)[:3]
    recent_html = "".join(
        f'<article class="card"><h3><a href="guides/{g[0]}.html">{esc(g[1])}</a></h3><p>{esc(g[3])}</p><p class="card-meta">{g[2]}</p></article>'
        for g in recent)
    guides_html = "".join(
        f'<article class="card"><h3><a href="guides/{g[0]}.html">{esc(g[1])}</a></h3><p>{esc(g[3])}</p></article>'
        for g in GUIDES)
    index = [{"code": c["code"], "aliases": c["aliases"], "appliance": c["appliance"],
              "appliance_label": c["appliance_label"], "manufacturer": c["manufacturer"],
              "title": c["title"], "url": "codes/" + c["slug"] + ".html"} for c in CODES]
    body = f'''
<section class="hero">
<h1>Find Your Appliance Error Code &amp; Fix the Problem</h1>
<p class="hero-sub">{esc(DATA["tagline"])}</p>
<form id="hero-search" class="search-form" role="search" aria-label="Search error codes">
<div class="field"><label for="q-code">Error code</label>
<input id="q-code" name="code" type="text" placeholder="e.g. E15" autocomplete="off" aria-describedby="q-hint"></div>
<div class="field"><label for="q-appliance">Appliance</label>
<select id="q-appliance" name="appliance">{options([c[1] for c in CATEGORIES], "All appliances")}</select></div>
<div class="field"><label for="q-mfr">Manufacturer</label>
<select id="q-mfr" name="manufacturer">{options(manufacturers_for(), "All manufacturers")}</select></div>
<div class="field btns"><button type="submit" class="btn">Search</button>
<button type="button" class="btn btn-ghost" id="q-clear">Clear</button></div>
</form>
<p class="hint" id="q-hint">Example formats: E1, F21, LE — shown as format examples only. A code's meaning depends on the brand and model, so pick both where you can.</p>
<div id="search-results" class="results" aria-live="polite"></div>
</section>
{ad_slot("Below hero")}
<section><h2>Popular Appliance Categories</h2><div class="grid">{cats_html}</div></section>
<section><h2>How It Works</h2><ol class="steps">
<li><strong>Select your appliance and manufacturer.</strong> Codes are brand-specific — the same letters can mean different things elsewhere.</li>
<li><strong>Enter the exact error code</strong> shown on the appliance display.</li>
<li><strong>Review possible causes, safe checks, and next steps</strong> — and stop at any step that feels unsafe.</li>
</ol></section>
<section><h2>Recently Added Guides</h2><div class="grid">{recent_html}</div></section>
<section><h2>Helpful Troubleshooting Guides</h2><div class="grid">{guides_html}</div>
<p>Also: <a href="guides/">browse all troubleshooting guides</a> · <a href="codes/">browse all error codes</a></p></section>
<script type="application/json" id="search-index">{json.dumps(index)}</script>'''
    return page("", SITE + " — Find & Fix Your Code",
                "Search appliance error codes by brand and appliance, with meanings, causes, and safe troubleshooting steps.",
                "Find Your Appliance Error Code & Fix the Problem", body, current="home")

def build_category(slug):
    _, name, desc, svg = CAT[slug]
    items = [c for c in CODES if c["appliance"] == slug]
    mfrs = sorted({c["manufacturer"] for c in items})
    if items:
        cards = "".join(code_card("../", c) for c in items)
        filt = f'''<form class="filter-form" role="search" aria-label="Filter codes in this category">
<div class="field"><label for="f-code">Filter by code</label><input id="f-code" type="text" placeholder="e.g. E15" autocomplete="off"></div>
<div class="field"><label for="f-mfr">Manufacturer</label><select id="f-mfr">{options(mfrs, "All manufacturers")}</select></div>
<div class="field btns"><button type="button" class="btn btn-ghost" id="f-clear">Clear filters</button></div></form>
<div class="grid" id="code-list">{cards}</div>
<p class="no-results" id="no-results" hidden>No codes in this category match your filters. Try clearing the filters, or <a href="../codes/">browse all error codes</a>.</p>'''
    else:
        filt = (f'<div class="empty-state"><p>No verified error-code entries yet for {esc(name)}.</p>'
                f'<p>We only publish codes after verifying their meaning — unverified codes are left out rather than guessed. '
                f'Until entries arrive, the guides below apply to this appliance too.</p>'
                f'<p><a href="../codes/">Browse verified codes for other appliances</a></p></div>')
    others = "".join(f'<li><a href="{s}.html">{esc(n)}</a></li>' for s, n, _, _ in CATEGORIES if s != slug)
    guides = "".join(f'<li><a href="../guides/{g[0]}.html">{esc(g[1])}</a></li>' for g in GUIDES)
    body = f'''<h1>{esc(name)} Error Codes</h1><p class="lede">{esc(desc)}</p>
{ad_slot("Category top")}
{filt}
<section><h2>Troubleshooting guides</h2><ul>{guides}</ul></section>
<section><h2>Related categories</h2><ul>{others}</ul></section>'''
    return page("../", f"{name} Error Codes & Troubleshooting",
                f"{name} error codes explained: meanings, causes, and safe troubleshooting steps. Verified entries only.",
                f"{name} Error Codes", body, current="appliances",
                crumbs_html=crumbs("../", [("Home", "../index.html"), ("Appliances", "index.html"), (name, "")]))

def build_codes_index():
    groups = ""
    for slug, name, _, _ in CATEGORIES:
        items = [c for c in CODES if c["appliance"] == slug]
        if not items:
            continue
        groups += f'<section class="code-group"><h2>{esc(name)}</h2><div class="grid">' + "".join(code_card("../", c) for c in items) + '</div></section>'
    body = f'''<h1>All Error Codes</h1><p class="lede">Every verified error-code entry on this site, grouped by appliance. Use the search box to filter by code, or pick a manufacturer.</p>
<form class="filter-form" role="search" aria-label="Filter all codes">
<div class="field"><label for="f-code">Filter by code</label><input id="f-code" type="text" placeholder="e.g. E15" autocomplete="off"></div>
<div class="field"><label for="f-mfr">Manufacturer</label><select id="f-mfr">{options(manufacturers_for(), "All manufacturers")}</select></div>
<div class="field btns"><button type="button" class="btn btn-ghost" id="f-clear">Clear filters</button></div></form>
<p class="no-results" id="no-results" hidden>No codes match your filters. Try a different code or manufacturer, or <a href="../index.html">search from the homepage</a>.</p>
{groups}'''
    return page("../", "All Appliance Error Codes — Search by Code, Brand & Appliance",
                "Browse every verified appliance error code on this site, by appliance and manufacturer, with safe troubleshooting steps.",
                "All Error Codes", body, current="errorcodes",
                crumbs_html=crumbs("../", [("Home", "../index.html"), ("Error Codes", "")]))

def build_categories_index():
    cards = "".join(
        f'<article class="card cat-card"><a href="{s}.html" class="card-link">{icon(svg)}<h3>{esc(n)}</h3><p>{esc(d)}</p></a></article>'
        for s, n, d, svg in CATEGORIES)
    body = f'<h1>Appliances</h1><p class="lede">Browse error codes by appliance type. Only verified entries are published — categories without entries yet link to the general guides instead of guessed codes.</p><div class="grid">{cards}</div>'
    return page("../", "Appliances — Browse Error Codes by Appliance Type",
                "Browse appliance error codes by category: washing machines, dishwashers, dryers, refrigerators, ovens, microwaves, air conditioners, and water heaters.",
                "Appliances", body, current="appliances",
                crumbs_html=crumbs("../", [("Home", "../index.html"), ("Appliances", "")]))

def build_guides_index():
    cards = "".join(
        f'<article class="card"><h3><a href="{g[0]}.html">{esc(g[1])}</a></h3><p>{esc(g[3])}</p><p class="card-meta">{g[2]}</p></article>'
        for g in GUIDES)
    body = f'<h1>Troubleshooting Guides</h1><p class="lede">General guides that apply across brands: reading codes, finding model numbers, safety basics, and knowing when to call a professional.</p><div class="grid">{cards}</div>'
    return page("../", "Troubleshooting Guides — Appliance Help Basics",
                "General appliance troubleshooting guides: how to read error codes, find model numbers, reset safely, and know when to call a technician.",
                "Troubleshooting Guides", body, current="troubleshooting",
                crumbs_html=crumbs("../", [("Home", "../index.html"), ("Troubleshooting", "")]))

def build_code(c):
    by_slug = {x["slug"]: x for x in CODES}
    rel = [by_slug[s] for s in c["related"] if s in by_slug]
    rel_html = "".join(f'<li><a href="{r["slug"]}.html">{esc(r["manufacturer"])} {esc(r["code"])} — {esc(r["title"])}</a></li>' for r in rel)
    alias_txt = "" if len(c["aliases"]) == 1 else f' Also shown as: {", ".join(esc(a) for a in c["aliases"][1:])}.'
    faq_json = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in c["faqs"]]}
    crumb_json = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": CANON_BASE},
        {"@type": "ListItem", "position": 2, "name": c["appliance_label"], "item": CANON_BASE + "categories/" + c["appliance"] + ".html"},
        {"@type": "ListItem", "position": 3, "name": c["manufacturer"] + " " + c["code"]}]}
    extra = ('<script type="application/ld+json">' + json.dumps(crumb_json) + '</script>\n'
             '<script type="application/ld+json">' + json.dumps(faq_json) + '</script>')
    def lis(items):
        return "<ul>" + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"
    def steps(items):
        return "<ol>" + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ol>"
    faqs_html = "".join(f"<details><summary>{esc(f['q'])}</summary><p>{esc(f['a'])}</p></details>" for f in c["faqs"])
    src_html = "".join(f'<li><a href="{esc(s["url"])}" rel="noopener">{esc(s["label"])}</a></li>' for s in c["sources"])
    body = f'''<h1>{esc(c["manufacturer"])} {esc(c["code"])} — {esc(c["title"])}</h1>
<table class="meta-table"><tbody>
<tr><th>Appliance</th><td><a href="../categories/{c["appliance"]}.html">{esc(c["appliance_label"])}</a></td></tr>
<tr><th>Manufacturer</th><td>{esc(c["manufacturer"])}</td></tr>
<tr><th>Error code</th><td><strong>{esc(c["code"])}</strong>{alias_txt}</td></tr>
<tr><th>Verification</th><td>Meaning cross-checked against multiple published sources. Confirm in your exact model's manual — codes vary by model.</td></tr>
</tbody></table>
<h2>What this code means</h2><p>{esc(c["meaning"])}</p>
<h2>Common possible causes</h2>{lis(c["causes"])}
{ad_slot("In-content")}
<h2>Safe initial checks</h2>{lis(c["checks"])}
<h2>Step-by-step troubleshooting</h2>{steps(c["steps"])}
<h2>When a reset may help</h2><p>{esc(c["reset"])}</p>
<h2>When to call a professional</h2>{lis(c["call_tech"])}
<div class="warning" role="note"><strong>Safety warning:</strong> {esc(c["safety"])} See also <a href="../guides/before-you-troubleshoot.html">what to do before troubleshooting</a>.</div>
{ad_slot("End of article")}
<section><h2>Related error codes</h2><ul>{rel_html}</ul></section>
<section><h2>Related guides</h2><ul>
<li><a href="../guides/before-you-troubleshoot.html">What to Do Before Troubleshooting an Appliance</a></li>
<li><a href="../guides/when-to-call-a-technician.html">When to Call a Qualified Technician</a></li>
<li><a href="../guides/reset-an-appliance-safely.html">How to Reset an Appliance Safely</a></li>
</ul></section>
<section class="faq"><h2>Frequently asked questions</h2>{faqs_html}</section>
<p class="note"><strong>Reminder:</strong> this page is general guidance for {esc(c["manufacturer"])} {esc(c["appliance_label"].lower())}. Your exact model's manual is the final word — if it disagrees with this page, follow the manual.</p>
<section><h2>Sources &amp; verification</h2><ul>{src_html}</ul>
<p class="note">Sources are the published pages this meaning was cross-checked against. They are not endorsements, and their own content may change. Model-specific manuals take precedence.</p></section>'''
    return page("../", f"{c['manufacturer']} {c['code']} — {c['title']}",
                f"{c['manufacturer']} {c['code']} — {c['title']}. Causes, safe checks, and step-by-step troubleshooting.",
                f"{c['manufacturer']} {c['code']} — {c['title']}", body, current="errorcodes",
                crumbs_html=crumbs("../", [("Home", "../index.html"), (c["appliance_label"], f"../categories/{c['appliance']}.html"), (f"{c['manufacturer']} {c['code']}", "")]),
                extra_head=extra)

def build_guide(g):
    slug, title, date, desc, body_html = g
    body = f'<h1>{esc(title)}</h1><p class="card-meta">Guide · {date}</p><div class="article-body">{body_html}</div>'
    others = "".join(f'<li><a href="{o[0]}.html">{esc(o[1])}</a></li>' for o in GUIDES if o[0] != slug)
    body += f'<section><h2>More guides</h2><ul>{others}</ul></section>'
    return page("../", title + " — Appliance Help", desc, title, body,
                current="troubleshooting",
                crumbs_html=crumbs("../", [("Home", "../index.html"), ("Troubleshooting", "index.html"), (title, "")]))

def build_simple(slug):
    title, desc, body_html = SIMPLE_PAGES[slug]
    return page("", title + " — Appliance Error Codes & Troubleshooting", desc, title,
                f"<h1>{esc(title)}</h1>" + body_html, current="",
                crumbs_html=crumbs("", [("Home", "index.html"), (title, "")]))

def main():
    write(os.path.join(ROOT, "index.html"), build_home())
    for slug, _, _, _ in CATEGORIES:
        write(os.path.join(ROOT, "categories", slug + ".html"), build_category(slug))
    write(os.path.join(ROOT, "categories", "index.html"), build_categories_index())
    for c in CODES:
        write(os.path.join(ROOT, "codes", c["slug"] + ".html"), build_code(c))
    write(os.path.join(ROOT, "codes", "index.html"), build_codes_index())
    for g in GUIDES:
        write(os.path.join(ROOT, "guides", g[0] + ".html"), build_guide(g))
    write(os.path.join(ROOT, "guides", "index.html"), build_guides_index())
    for slug in SIMPLE_PAGES:
        write(os.path.join(ROOT, slug + ".html"), build_simple(slug))
    # Sitemap page (human-readable)
    links = [("index.html", "Home")]
    links += [(f"categories/{s}.html", n) for s, n, _, _ in CATEGORIES]
    links += [(f"codes/{c['slug']}.html", f"{c['manufacturer']} {c['code']} — {c['title']}") for c in CODES]
    links += [(f"guides/{g[0]}.html", g[1]) for g in GUIDES]
    links += [(f"{s}.html", SIMPLE_PAGES[s][0]) for s in SIMPLE_PAGES]
    links += [("categories/index.html", "All appliances"), ("codes/index.html", "All error codes"),
              ("guides/index.html", "All troubleshooting guides")]
    sitemap_body = "<h1>Sitemap</h1><ul>" + "".join(f'<li><a href="{u}">{esc(t)}</a></li>' for u, t in links) + "</ul>"
    write(os.path.join(ROOT, "sitemap.html"), page("", "Sitemap — Appliance Error Codes & Troubleshooting",
          "A complete list of pages on this site.", "Sitemap", sitemap_body,
          crumbs_html=crumbs("", [("Home", "index.html"), ("Sitemap", "")])))
    # sitemap.xml
    urls = [CANON_BASE] + [CANON_BASE + u for u, _ in links]
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "".join(f"  <url><loc>{esc(u)}</loc></url>\n" for u in urls) + "</urlset>\n")
    write(os.path.join(ROOT, "sitemap.xml"), xml)
    print(f"DONE: {len(CODES)} code pages, {len(CATEGORIES)} categories, {len(GUIDES)} guides, {len(SIMPLE_PAGES)} trust pages")

if __name__ == "__main__":
    main()
