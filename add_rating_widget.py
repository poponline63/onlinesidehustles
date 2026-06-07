#!/usr/bin/env python3
"""
Inject the community rating widget into every review-*.html page.

- Canonical casino names come from the REVIEW_LINKS map in
  sweepstakes-casino-list.html, so a vote on a review page shares the same
  key as the matching row on the main list (normalized name).
- The widget card is inserted right before <div class="cta-block ...>, with a
  fallback to just before </body>.
- Idempotent: pages already containing id="oshr-review" are skipped.

Run:  python add_rating_widget.py
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
LIST_PAGE = os.path.join(ROOT, "sweepstakes-casino-list.html")


def build_url_to_name():
    """Parse REVIEW_LINKS {'Name':'/review-x'} -> {'review-x.html': 'Name'} (first name wins)."""
    html = open(LIST_PAGE, encoding="utf-8").read()
    m = re.search(r"const REVIEW_LINKS\s*=\s*\{(.*?)\};", html, re.S)
    if not m:
        print("!! Could not find REVIEW_LINKS in list page.")
        sys.exit(1)
    body = m.group(1)
    url2name = {}
    for name, url in re.findall(r"'([^']+)'\s*:\s*'([^']+)'", body):
        slug = url.strip().lstrip("/")
        if not slug.endswith(".html"):
            slug += ".html"
        url2name.setdefault(slug, name)  # first occurrence is the canonical list name
    return url2name


def derive_name_from_title(html, fallback):
    m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    if m:
        t = re.sub(r"\s+", " ", m.group(1)).strip()
        t = re.split(r"\s+Review\b", t, flags=re.I)[0]
        t = t.split("|")[0].split("—")[0].split(":")[0].strip()
        if t:
            return t
    return fallback


def card_html(name):
    esc = name.replace("&", "&amp;").replace('"', "&quot;")
    return (
        '\n<!-- OSH community rating widget -->\n'
        '<div class="oshr-card" id="oshr-review" data-casino="' + esc + '" style="display:none">\n'
        '  <h3>&#11088; Rate ' + esc + '</h3>\n'
        '  <p class="oshr-sub">Tap a star to rate it. Your vote feeds the community average and helps '
        'move casinos up or down the tiers on our <a href="/sweepstakes-casino-list">main list</a>.</p>\n'
        '  <div id="oshr-mount"></div>\n'
        '  <div class="oshr-thanks" id="oshr-thanks"></div>\n'
        '</div>\n'
    )


INIT_SCRIPT = (
    '\n<script src="/js/casino-ratings.js"></script>\n'
    '<script>\n'
    '(function(){\n'
    '  function go(){\n'
    '    if(!window.OSHRatings||!OSHRatings.enabled)return;\n'
    '    var card=document.getElementById("oshr-review"); if(!card)return;\n'
    '    var name=card.getAttribute("data-casino");\n'
    '    var mount=document.getElementById("oshr-mount");\n'
    '    var thanks=document.getElementById("oshr-thanks");\n'
    '    card.style.display="";\n'
    '    function render(){ mount.innerHTML=OSHRatings.widgetHTML(name); }\n'
    '    render();\n'
    '    OSHRatings.attach(card,function(n,res){\n'
    '      render();\n'
    '      if(res&&res.ok) thanks.textContent="Thanks for rating! Community average "+res.a.toFixed(1)+"/5 ("+res.c+" votes).";\n'
    '    });\n'
    '    OSHRatings.load().then(render);\n'
    '  }\n'
    '  if(document.readyState!=="loading") go(); else document.addEventListener("DOMContentLoaded",go);\n'
    '})();\n'
    '</script>\n'
)


def inject(path, url2name):
    fname = os.path.basename(path)
    html = open(path, encoding="utf-8").read()
    if 'id="oshr-review"' in html:
        return "skip-exists"

    name = url2name.get(fname) or derive_name_from_title(
        html, fname.replace("review-", "").replace(".html", "").replace("-", " ").title()
    )
    mapped = "mapped" if fname in url2name else "DERIVED"

    card = card_html(name)
    # Insert card before the CTA block, else before </body>.
    cta = re.search(r'<div class="cta-block', html)
    if cta:
        html = html[:cta.start()] + card + html[cta.start():]
    else:
        idx = html.rfind("</body>")
        if idx == -1:
            return "no-body"
        html = html[:idx] + card + html[idx:]

    # Insert init script before </body> (only once).
    idx = html.rfind("</body>")
    html = html[:idx] + INIT_SCRIPT + html[idx:]

    open(path, "w", encoding="utf-8").write(html)
    return "ok-" + mapped + " (" + name + ")"


def main():
    url2name = build_url_to_name()
    files = sorted(glob.glob(os.path.join(ROOT, "review-*.html")))
    counts = {}
    derived = []
    for path in files:
        res = inject(path, url2name)
        tag = res.split(" ")[0]
        counts[tag] = counts.get(tag, 0) + 1
        if tag.startswith("ok-DERIVED"):
            derived.append(os.path.basename(path) + " -> " + res)
    print("Processed %d review pages:" % len(files))
    for k in sorted(counts):
        print("  %-14s %d" % (k, counts[k]))
    if derived:
        print("\nNames DERIVED from <title> (verify these match the sheet/list):")
        for d in derived:
            print("  " + d)


if __name__ == "__main__":
    main()
