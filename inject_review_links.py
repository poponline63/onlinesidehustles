"""
inject_review_links.py
Adds an "In-Depth Casino Reviews" section to every casinos-in-*.html state page,
injected just before the existing <section class="faq-section dlg-fade"> block.

SAFE: only inserts new HTML; never touches existing cards, affiliate links, or CSS.
"""

import re
from pathlib import Path

BASE = Path(r"C:\Users\popon\Desktop\Claude Code\onlinesidehustles")

# ── casino data-name → (display label, review slug) ──────────────────────────
# Only includes casinos that have a review page on the site.
CASINO_MAP = {
    "stake.us":        ("Stake.us",          "review-stake-us"),
    "wow vegas":       ("WOW Vegas",          "review-wow-vegas"),
    "crown coins":     ("Crown Coins",        "review-crown-coins"),
    "realprize":       ("RealPrize",          "review-realprize"),
    "mcluck":          ("McLuck",             "review-mcluck"),
    "chumba casino":   ("Chumba Casino",      "review-chumba"),
    "pulsz":           ("Pulsz",              "review-pulsz"),
    "sportzino":       ("Sportzino",          "review-sportzino"),
    "zula casino":     ("Zula Casino",        "review-zula"),
    "spinsaga":        ("SpinSaga",           "review-spinsaga"),
    "global poker":    ("Global Poker",       "review-global-poker"),
    "lonestar casino": ("Lonestar Casino",    "review-lonestar"),
    "scarlet sands":   ("Scarlet Sands",      "review-scarletsands"),
    "legendz casino":  ("Legendz Casino",     "review-legendz"),
    "rebet":           ("ReBet",              "review-rebet"),
    "fliff":           ("Fliff",              "review-fliff"),
    "fortune coins":   ("Fortune Coins",      "review-fortune-coins"),
    "luckyland slots": ("LuckyLand Slots",    "review-luckyland"),
    "hello millions":  ("Hello Millions",     "review-hello-millions"),
    "chanced":         ("Chanced",            "review-chanced"),
    "spinquest":       ("SpinQuest",          "review-spinquest"),
    "funrize":         ("FunRize",            "review-funrize"),
    "moozi":           ("Moozi",              "review-moozi"),
    "jackpota":        ("Jackpota",           "review-jackpota"),
    "dimesweeps":      ("DimeSweeps",         "review-dimesweeps"),
    "speedsweeps":     ("SpeedSweeps",        "review-speedsweeps"),
    "americanluck":    ("American Luck",      "review-american-luck"),
}

LINK_STYLE = (
    "display:inline-flex;align-items:center;"
    "background:var(--bg-card);"
    "border:1px solid rgba(110,231,183,.2);"
    "border-radius:7px;"
    "padding:.38rem .82rem;"
    "color:var(--teal);"
    "text-decoration:none;"
    "font-size:.75rem;font-weight:600;"
    "font-family:'IBM Plex Mono',monospace;"
    "letter-spacing:.04em;white-space:nowrap;"
)


def build_section(casino_list):
    """Return the HTML block to inject, given an ordered list of (label, slug)."""
    links = "\n".join(
        f'    <a href="/{slug}" style="{LINK_STYLE}">{label}</a>'
        for label, slug in casino_list
    )
    return (
        "\n"
        "<!-- In-Depth Casino Reviews -->\n"
        '<div class="dlg-fade" '
        'style="margin:3rem 0 0;padding:2rem 0;border-top:1px solid var(--border);">\n'
        '  <h2 style="font-size:1.3rem;font-weight:800;color:#fff;margin-bottom:.5rem;">'
        "Read In-Depth Casino Reviews</h2>\n"
        '  <p style="color:var(--text-muted);font-size:.88rem;line-height:1.7;'
        'margin-bottom:1.1rem;">'
        "We&#39;ve tested and reviewed every casino on this page. "
        "Read our full breakdown&#x202F;&#8212;&#x202F;bonuses, payouts, daily rewards, "
        "and who it&#39;s best for.</p>\n"
        '  <div style="display:flex;flex-wrap:wrap;gap:.45rem;">\n'
        f"{links}\n"
        "  </div>\n"
        "</div>\n\n"
    )


INJECT_BEFORE = '<section class="faq-section dlg-fade">'
ALREADY_DONE_MARKER = "<!-- In-Depth Casino Reviews -->"

state_files = sorted(BASE.glob("casinos-in-*.html"))
print(f"Found {len(state_files)} state pages.")

updated = 0
skipped = 0

for path in state_files:
    html = path.read_text(encoding="utf-8")

    # Skip if already injected
    if ALREADY_DONE_MARKER in html:
        print(f"  SKIP (already done): {path.name}")
        skipped += 1
        continue

    # Collect which casinos appear on this page (in order of first appearance)
    casino_order = []
    for m in re.finditer(r'data-name="([^"]+)"', html, re.IGNORECASE):
        key = m.group(1).lower()
        if key in CASINO_MAP and CASINO_MAP[key] not in casino_order:
            casino_order.append(CASINO_MAP[key])

    if not casino_order:
        print(f"  SKIP (no matching casinos): {path.name}")
        skipped += 1
        continue

    inject_point = html.find(INJECT_BEFORE)
    if inject_point == -1:
        print(f"  SKIP (no faq-section found): {path.name}")
        skipped += 1
        continue

    section_html = build_section(casino_order)
    new_html = html[:inject_point] + section_html + html[inject_point:]
    path.write_text(new_html, encoding="utf-8")
    print(f"  OK ({len(casino_order)} review links): {path.name}")
    updated += 1

print(f"\nDone. {updated} updated, {skipped} skipped.")
