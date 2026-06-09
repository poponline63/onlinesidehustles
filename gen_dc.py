#!/usr/bin/env python3
"""
gen_dc.py  -  Generate ONLY the Washington D.C. state page.

Uses the canonical build_page() from regen_state_pages so the page is identical
in structure to the 50 state pages, then bakes in the same "Read In-Depth Casino
Reviews" cross-link section the other state pages have. Also renders a local D.C.
flag PNG to match the existing /images/states/ set.

Does NOT touch the other 50 pages (importing regen_state_pages is safe; its
main() is guarded by __main__).
"""

import os
import re
import math
from PIL import Image, ImageDraw

from regen_state_pages import build_page

BASE = os.path.dirname(os.path.abspath(__file__))

# --- D.C. data (matches the tuple added to regen_state_pages.STATES) --------
DC = ("washington-dc", "Washington D.C.", "DC", 104, 40, 13, 91,
      "limited local casino options, making sweepstakes casinos a popular and legal way to play")

# --- review cross-link section (copied from inject_review_links.py so we can
#     reuse the exact markup without triggering that script's module-level run)
CASINO_MAP = {
    "stake.us": ("Stake.us", "review-stake-us"), "wow vegas": ("WOW Vegas", "review-wow-vegas"),
    "crown coins": ("Crown Coins", "review-crown-coins"), "realprize": ("RealPrize", "review-realprize"),
    "mcluck": ("McLuck", "review-mcluck"), "chumba casino": ("Chumba Casino", "review-chumba"),
    "pulsz": ("Pulsz", "review-pulsz"), "sportzino": ("Sportzino", "review-sportzino"),
    "zula casino": ("Zula Casino", "review-zula"), "spinsaga": ("SpinSaga", "review-spinsaga"),
    "global poker": ("Global Poker", "review-global-poker"), "lonestar casino": ("Lonestar Casino", "review-lonestar"),
    "scarlet sands": ("Scarlet Sands", "review-scarletsands"), "legendz casino": ("Legendz Casino", "review-legendz"),
    "rebet": ("ReBet", "review-rebet"), "fliff": ("Fliff", "review-fliff"),
    "fortune coins": ("Fortune Coins", "review-fortune-coins"), "luckyland slots": ("LuckyLand Slots", "review-luckyland"),
    "hello millions": ("Hello Millions", "review-hello-millions"), "chanced": ("Chanced", "review-chanced"),
    "spinquest": ("SpinQuest", "review-spinquest"), "funrize": ("FunRize", "review-funrize"),
    "moozi": ("Moozi", "review-moozi"), "jackpota": ("Jackpota", "review-jackpota"),
    "dimesweeps": ("DimeSweeps", "review-dimesweeps"), "speedsweeps": ("SpeedSweeps", "review-speedsweeps"),
    "americanluck": ("American Luck", "review-american-luck"),
}
LINK_STYLE = (
    "display:inline-flex;align-items:center;background:var(--bg-card);"
    "border:1px solid rgba(110,231,183,.2);border-radius:7px;padding:.38rem .82rem;"
    "color:var(--teal);text-decoration:none;font-size:.75rem;font-weight:600;"
    "font-family:'IBM Plex Mono',monospace;letter-spacing:.04em;white-space:nowrap;"
)
INJECT_BEFORE = '<section class="faq-section dlg-fade">'
MARKER = "<!-- In-Depth Casino Reviews -->"


def review_section(casino_list):
    links = "\n".join(f'    <a href="/{slug}" style="{LINK_STYLE}">{label}</a>'
                      for label, slug in casino_list)
    return (
        "\n" + MARKER + "\n"
        '<div class="dlg-fade" style="margin:3rem 0 0;padding:2rem 0;border-top:1px solid var(--border);">\n'
        '  <h2 style="font-size:1.3rem;font-weight:800;color:#fff;margin-bottom:.5rem;">Read In-Depth Casino Reviews</h2>\n'
        '  <p style="color:var(--text-muted);font-size:.88rem;line-height:1.7;margin-bottom:1.1rem;">'
        "We&#39;ve tested and reviewed every casino on this page. Read our full breakdown&#x202F;&#8212;&#x202F;"
        "bonuses, payouts, daily rewards, and who it&#39;s best for.</p>\n"
        '  <div style="display:flex;flex-wrap:wrap;gap:.45rem;">\n'
        f"{links}\n  </div>\n</div>\n\n"
    )


def make_dc_flag(path):
    """Render a clean public-domain D.C. flag (3 red stars over 2 red bars)."""
    W, H = 250, 175
    RED = (191, 13, 62)
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    def star(cx, cy, r_out, r_in, pts=5, rot=-90):
        p = []
        for i in range(pts * 2):
            ang = math.radians(rot + i * 180 / pts)
            r = r_out if i % 2 == 0 else r_in
            p.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        return p

    for cx in (75, 125, 175):
        d.polygon(star(cx, 45, 22, 9), fill=RED)
    d.rectangle([0, 95, W, 117], fill=RED)
    d.rectangle([0, 132, W, 154], fill=RED)
    img.save(path)


def main():
    # flag
    make_dc_flag(os.path.join(BASE, "images", "states", "dc.png"))

    # page
    html = build_page(DC)
    if MARKER not in html:
        order = []
        for m in re.finditer(r'data-name="([^"]+)"', html, re.IGNORECASE):
            key = m.group(1).lower()
            if key in CASINO_MAP and CASINO_MAP[key] not in order:
                order.append(CASINO_MAP[key])
        ip = html.find(INJECT_BEFORE)
        if order and ip != -1:
            html = html[:ip] + review_section(order) + html[ip:]

    out = os.path.join(BASE, "casinos-in-washington-dc.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {os.path.basename(out)} ({len(html):,} bytes) + images/states/dc.png")


if __name__ == "__main__":
    main()
