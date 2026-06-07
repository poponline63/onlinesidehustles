"""
blog_casino_links.py
Scans every blog/*.html post and wraps the FIRST mention of each casino name
(not already inside an <a> tag, script, style, or head) with a link to that
casino's review page.

SAFE rules:
  - Only touches body text — head/meta/JSON-LD never modified
  - Skips any occurrence already inside <a>…</a>
  - Skips <script> and <style> content
  - Only the FIRST occurrence per casino per page is linked
  - Does not link a casino to itself (e.g., the Pulsz review blog post won't
    get a Pulsz link — it already CTAs to Pulsz)
  - Longer names matched first to avoid "Chumba" matching inside "Chumba Casino"
"""

import re
from pathlib import Path

BASE  = Path(r"C:\Users\popon\Desktop\Claude Code\onlinesidehustles")
BLOG  = BASE / "blog"

# ── (display_name, slug) for every casino that has a review page ──────────────
# Listed longest-name first so multi-word names match before single-word ones.
CASINOS = [
    ("LuckyLand Slots",  "review-luckyland"),
    ("Luckyland Slots",  "review-luckyland"),
    ("LuckyLand",        "review-luckyland"),
    ("Lonestar Casino",  "review-lonestar"),
    ("Hello Millions",   "review-hello-millions"),
    ("Global Poker",     "review-global-poker"),
    ("Fortune Coins",    "review-fortune-coins"),
    ("Golden Hearts",    "review-golden-hearts"),
    ("Crown Coins",      "review-crown-coins"),
    ("Chumba Casino",    "review-chumba"),
    ("Scarlet Sands",    "review-scarletsands"),
    ("Legendz Casino",   "review-legendz"),
    ("Zula Casino",      "review-zula"),
    ("WOW Vegas",        "review-wow-vegas"),
    ("Wow Vegas",        "review-wow-vegas"),
    ("Tao Fortune",      "review-tao-fortune"),
    ("No Limit Coins",   "review-nolimitcoins"),
    ("NoLimitCoins",     "review-nolimitcoins"),
    ("American Luck",    "review-american-luck"),
    ("Stake.us",         "review-stake-us"),
    ("stake.us",         "review-stake-us"),
    ("McLuck",           "review-mcluck"),
    ("RealPrize",        "review-realprize"),
    ("Realprize",        "review-realprize"),
    ("Sportzino",        "review-sportzino"),
    ("SpinSaga",         "review-spinsaga"),
    ("Spinsaga",         "review-spinsaga"),
    ("Legendz",          "review-legendz"),
    ("Lonestar",         "review-lonestar"),
    ("Pulsz",            "review-pulsz"),
    ("ReBet",            "review-rebet"),
    ("Rebet",            "review-rebet"),
    ("Fliff",            "review-fliff"),
    ("Chanced",          "review-chanced"),
    ("SpinQuest",        "review-spinquest"),
    ("Spinquest",        "review-spinquest"),
    ("FunRize",          "review-funrize"),
    ("Funrize",          "review-funrize"),
    ("Moozi",            "review-moozi"),
    ("Jackpota",         "review-jackpota"),
    ("DimeSweeps",       "review-dimesweeps"),
    ("Dimesweeps",       "review-dimesweeps"),
    ("SpeedSweeps",      "review-speedsweeps"),
    ("Speedsweeps",      "review-speedsweeps"),
    ("SweepTastic",      "review-sweeptastic"),
    ("Sweeptastic",      "review-sweeptastic"),
    ("MoonSpin",         "review-moonspin"),
    ("Moonspin",         "review-moonspin"),
    ("SpinBlitz",        "review-spinblitz"),
    ("Spinblitz",        "review-spinblitz"),
    ("High5Casino",      "review-high5"),
    ("High 5 Casino",    "review-high5"),
    ("Modo Casino",      "review-modo"),
    ("Spree",            "review-spree"),
    ("Chumba",           "review-chumba"),
    ("Zula",             "review-zula"),
    ("McLuck",           "review-mcluck"),
    ("RichSweeps",       "review-richsweeps"),
    ("Richsweeps",       "review-richsweeps"),
    ("Cazino",           "review-cazino"),
    ("DinerSweeps",      "review-dinersweeps"),
    ("Dinersweeps",      "review-dinersweeps"),
    ("FunzCity",         "review-funzcity"),
    ("Funzcity",         "review-funzcity"),
    ("GoldRushCity",     "review-goldrushcity"),
    ("Goldrushcity",     "review-goldrushcity"),
    ("SpinDoo",          "review-spindoo"),
    ("SpinPals",         "review-spinpals"),
    ("Stackr",           "review-stackr"),
    ("SweepShark",       "review-sweepshark"),
    ("Sweepshark",       "review-sweepshark"),
    ("SweepsRoyal",      "review-sweepsroyal"),
    ("Sweepsroyal",      "review-sweepsroyal"),
    ("Thrillz",          "review-thrillz"),
    ("Rolla",            "review-rolla"),
    ("SidePot",          "review-sidepot"),
    ("Sidepot",          "review-sidepot"),
    ("MegaBonanza",      "review-megabonanza"),
    ("MegaFrenzy",       "review-megafrenzy"),
    ("MyPrize",          "review-myprize"),
    ("Myprise",          "review-myprize"),
    ("PlayFame",         "review-playfame"),
    ("Playfame",         "review-playfame"),
    ("Jackpot Rabbit",   "review-jackpotrabbit"),
    ("Legacy Arcade",    "review-legacy-arcade"),
    ("LuckyBitsVegas",   "review-luckybitsveg"),
    ("LuckyHands",       "review-luckyhands"),
    ("LunaLand",         "review-lunaland"),
    ("Fortune Wheelz",   "review-fortunewheelz"),
]

# Deduplicate by slug — once a slug is matched on this page, skip further variants
# (handled at runtime in linked_slugs set)


def count_open_close(html_before, open_re, close_str):
    """Count unmatched open tags before a position."""
    opens  = len(re.findall(open_re,  html_before, re.IGNORECASE))
    closes = len(re.findall(re.escape(close_str), html_before, re.IGNORECASE))
    return opens - closes


def is_in_skip_context(html, pos):
    """Return True if pos is inside <a>, <script>, <style>, or <head>/<title>."""
    before = html[:pos]
    # <a ...>...</a>
    if count_open_close(before, r'<a[\s>]', '</a>') > 0:
        return True
    # <script>...</script>
    if count_open_close(before, r'<script[\s>]', '</script>') > 0:
        return True
    # <style>...</style>
    if count_open_close(before, r'<style[\s>]', '</style>') > 0:
        return True
    # <head>...</head>  (covers <title>, <meta>, JSON-LD etc.)
    if count_open_close(before, r'<head[\s>]', '</head>') > 0:
        return True
    return False


def link_casinos_in_post(html, post_slug, casinos):
    """
    For each casino (in order, longest first), find the first plain-text
    occurrence not in a skip context, and wrap it with a review link.
    Returns modified html.
    """
    linked_slugs = set()

    for display, slug in casinos:
        # Don't self-link
        if post_slug and slug.replace("review-", "") in post_slug:
            continue
        # Already linked this casino via another display variant
        if slug in linked_slugs:
            continue

        lower_html = html.lower()
        lower_display = display.lower()

        # We need word-boundary matching to avoid "Pulsz" matching "Pulsz Bingo"
        # Use a simple check: character before and after must not be alphanumeric
        search_start = 0
        while True:
            idx = lower_html.find(lower_display, search_start)
            if idx == -1:
                break

            # Word-boundary check
            char_before = html[idx - 1] if idx > 0 else " "
            char_after  = html[idx + len(display)] if (idx + len(display)) < len(html) else " "
            if char_before.isalnum() or char_after.isalnum():
                search_start = idx + len(display)
                continue

            if is_in_skip_context(html, idx):
                search_start = idx + len(display)
                continue

            # Found a valid occurrence — wrap it
            original_text = html[idx: idx + len(display)]
            replacement   = f'<a href="/{slug}">{original_text}</a>'
            html = html[:idx] + replacement + html[idx + len(display):]
            linked_slugs.add(slug)
            print(f"    Linked: {original_text!r} -> /{slug}")
            break  # only the first occurrence

    return html


# ── Main ─────────────────────────────────────────────────────────────────────
blog_files = sorted(BLOG.glob("*.html"))
print(f"Found {len(blog_files)} blog posts.\n")

total_links = 0
for path in blog_files:
    html     = path.read_text(encoding="utf-8")
    # Derive a short slug from the filename for self-link avoidance
    post_slug = path.stem   # e.g. "fortune-coins-review-2026-fortune-wins-rebrand"

    links_before = html.count('<a href="/review-')
    html = link_casinos_in_post(html, post_slug, CASINOS)
    links_after  = html.count('<a href="/review-')
    added = links_after - links_before

    if added:
        path.write_text(html, encoding="utf-8")
        total_links += added
        print(f"  {path.name}: +{added} link(s)")
    else:
        print(f"  {path.name}: (no changes)")

print(f"\nTotal review links added across all blog posts: {total_links}")
