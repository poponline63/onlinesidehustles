#!/usr/bin/env python3
"""
fix_logos.py
Replaces Google Favicon API src with Clearbit Logo API on every casino card
in casino-reviews.html, and adds unique background colours to the letter fallbacks.
"""
import re, os

BASE = r"C:\Users\popon\Desktop\Claude Code\onlinesidehustles"
FILE = os.path.join(BASE, "casino-reviews.html")

# ── unique accent colours per domain ─────────────────────────────────────────
COLORS = {
    "stake.us":            "#0f5c3a",
    "pulsz.com":           "#c51e8a",
    "zulacasino.com":      "#4c2aaf",
    "chumbacasino.com":    "#d97706",
    "crowncoins.com":      "#b8860b",
    "sportzino.com":       "#1565c0",
    "shuffle.com":         "#6d28d9",
    "megabonanza.com":     "#92400e",
    "playfame.com":        "#7e22ce",
    "jackpota.com":        "#b45309",
    "mcluck.com":          "#166534",
    "globalpoker.com":     "#1e40af",
    "luckylandcasino.com": "#a16207",
    "luckylandslots.com":  "#a16207",
    "realprize.com":       "#9d174d",
    "getfliff.com":        "#0369a1",
    "moonspin.com":        "#5b21b6",
    "moonspin.us":         "#5b21b6",
    "rebet.com":           "#0f766e",
    "pulszingo.com":       "#be185d",
    "pulszbingo.com":      "#be185d",
    "luckyhands.com":      "#15803d",
    "lonestarcasino.com":  "#854d0e",
    "myprize.com":         "#1d4ed8",
    "thrillz.com":         "#7c3aed",
    "moozi.com":           "#b91c1c",
    "fortunecoins.com":    "#b45309",
    "wowvegas.com":        "#7c2d12",
    "goldenheartsgames.com":"#b45309",
    "high5casino.com":     "#1e3a8a",
    "chanced.com":         "#0e7490",
    "hellomillions.com":   "#6b21a8",
    "modo.us":             "#0f766e",
    "nolimitcoins.com":    "#dc2626",
    "spree.com":           "#4338ca",
    "funrize.com":         "#c2410c",
    "sweeptastic.com":     "#0369a1",
    "taofortune.com":      "#7c3aed",
    "legacyarcade.com":    "#0f5c3a",
}

with open(FILE, encoding="utf-8") as f:
    html = f.read()

# ── 1. Replace every Google-Favicon src with Clearbit ────────────────────────
GFAVICON = re.compile(
    r'src="https://t1\.gstatic\.com/faviconV2[^"]*?url=https?://(?:www\.)?([^&"]+)[^"]*?"'
)

def clearbit_src(m):
    domain = m.group(1).rstrip("/")
    return f'src="https://logo.clearbit.com/{domain}"'

html = GFAVICON.sub(clearbit_src, html)

# ── 2. Colour every rc-logo-fallback ─────────────────────────────────────────
# Each fallback div sits right after its img tag; the img has the domain in src.
# Strategy: walk block by block — find each img+fallback pair and inject colour.

IMG_BLOCK = re.compile(
    r'(<img[^>]+src="https://logo\.clearbit\.com/(?:www\.)?([^/"]+)"[^>]*>)'
    r'(\s*<div class="rc-logo-fallback"[^>]*)(>)',
    re.DOTALL
)

def colour_fallback(m):
    img_tag   = m.group(1)
    domain    = m.group(2).lower().strip()
    div_open  = m.group(3)
    close_gt  = m.group(4)
    color     = COLORS.get(domain, "#1a5c4a")   # sensible teal default
    # inject background colour, keep any existing style attrs
    if 'style=' in div_open:
        div_open = re.sub(r'style="[^"]*"', f'style="background:{color}"', div_open)
    else:
        div_open = div_open + f' style="background:{color}"'
    return img_tag + "\n          " + div_open + close_gt

html = IMG_BLOCK.sub(colour_fallback, html)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Done — Clearbit logos + fallback colours applied.")
