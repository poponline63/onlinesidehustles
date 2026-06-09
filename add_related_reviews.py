#!/usr/bin/env python3
"""
add_related_reviews.py
Adds a contextual "Popular alternatives" row of related casino-review links to
every review-*.html page, injected right before the existing generic
<div class="related-links ..."> block.

Why: all 126 review pages currently share the same 4 generic related links and
never link to each other. This builds a dense review<->review internal-link
graph (spreads crawl + ranking signal across the catalog) while giving readers
real "alternatives" to consider.

SAFE: only inserts a new block using the existing .related-link CSS class.
Idempotent via the RELATED_MARKER. Never touches index.html.
"""

import re
from pathlib import Path

BASE = Path(__file__).resolve().parent

# Pool of well-known brands that have review pages. Each review links to 6 of
# these (rotated per-slug so the graph is varied, not identical on every page).
POOL = [
    ("Stake.us",         "review-stake-us"),
    ("Pulsz",            "review-pulsz"),
    ("McLuck",           "review-mcluck"),
    ("WOW Vegas",        "review-wow-vegas"),
    ("Chumba Casino",    "review-chumba"),
    ("Crown Coins",      "review-crown-coins"),
    ("LuckyLand Slots",  "review-luckyland"),
    ("Global Poker",     "review-global-poker"),
    ("High 5 Casino",    "review-high5"),
    ("Fortune Coins",    "review-fortune-coins"),
    ("Funrize",          "review-funrize"),
    ("Sportzino",        "review-sportzino"),
    ("Zula Casino",      "review-zula"),
    ("Moozi",            "review-moozi"),
    ("Spree",            "review-spree"),
    ("ReBet",            "review-rebet"),
    ("Hello Millions",   "review-hello-millions"),
    ("Jackpota",         "review-jackpota"),
    ("Legendz Casino",   "review-legendz"),
    ("RealPrize",        "review-realprize"),
]

N_LINKS = 6
RELATED_MARKER = "<!-- Related Reviews -->"
INJECT_BEFORE = '<div class="related-links fade-in">'


def pick_related(own_slug, position):
    """Deterministically pick N_LINKS brands from POOL, excluding self.

    Always leads with the biggest brands (concentrates equity on money pages),
    then rotates the remainder by the page's position so links vary across the
    catalog instead of every page pointing at the identical six.
    """
    candidates = [(label, slug) for label, slug in POOL if slug != own_slug]
    head = candidates[:3]                      # always the 3 biggest
    tail = candidates[3:]
    if tail:
        off = position % len(tail)
        rotated = tail[off:] + tail[:off]
    else:
        rotated = []
    chosen = head + rotated
    return chosen[:N_LINKS]


def build_block(related):
    links = "\n".join(
        f'    <a href="/{slug}" class="related-link">{label} &#8594;</a>'
        for label, slug in related
    )
    return (
        f"   {RELATED_MARKER}\n"
        '   <div class="related-links fade-in" '
        'style="border-top:1px solid var(--border);padding-top:1.1rem;margin-top:.4rem;">\n'
        '    <span style="width:100%;display:block;font-size:.72rem;font-weight:700;'
        "letter-spacing:.06em;text-transform:uppercase;color:var(--text-muted);"
        'font-family:&#39;IBM Plex Mono&#39;,monospace;margin-bottom:.2rem;">'
        "Popular Alternatives</span>\n"
        f"{links}\n"
        "   </div>\n"
    )


def main():
    files = sorted(BASE.glob("review-*.html"))
    print(f"Found {len(files)} review pages.")
    updated = skipped = 0

    for pos, path in enumerate(files):
        html = path.read_text(encoding="utf-8")

        if RELATED_MARKER in html:
            skipped += 1
            continue

        idx = html.find(INJECT_BEFORE)
        if idx == -1:
            print(f"  SKIP (no related-links block): {path.name}")
            skipped += 1
            continue

        own_slug = path.stem  # e.g. "review-stake-us"
        related = pick_related(own_slug, pos)
        block = build_block(related)
        new_html = html[:idx] + block + html[idx:]
        path.write_text(new_html, encoding="utf-8")
        updated += 1

    print(f"\nDone. {updated} updated, {skipped} skipped.")


if __name__ == "__main__":
    main()
