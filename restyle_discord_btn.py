#!/usr/bin/env python3
"""
Restyle the nav "Join Discord" button across every HTML page.

Changes:
  1. CSS .nav-cta  — lime green  →  teal gradient  (matches site theme)
  2. CSS .nav-cta:hover  — opacity fade  →  lift + glow
  3. Button text  — strip the 📣 megaphone emoji (&#128225;)
"""

import glob, os

# ── Old / New CSS strings ────────────────────────────────────────────────────

OLD_CTA = (
    "background:var(--lime);color:var(--lime-text);"
    "text-decoration:none;padding:.35rem 1rem;"
    "font-size:.78rem;font-weight:700;border-radius:4px;"
    "margin-left:.6rem;transition:opacity .2s;"
)
NEW_CTA = (
    "background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%);"
    "color:#060a0f;"
    "text-decoration:none;padding:.35rem 1rem;"
    "font-size:.78rem;font-weight:700;border-radius:6px;"
    "margin-left:.6rem;transition:transform .18s,box-shadow .18s;"
    "box-shadow:0 2px 10px rgba(110,231,183,.28);"
)

OLD_HOVER = "nav-cta:hover{opacity:.88;}"
NEW_HOVER = "nav-cta:hover{transform:translateY(-1px);box-shadow:0 4px 18px rgba(110,231,183,.45);}"

# ── Old / New button text ────────────────────────────────────────────────────
OLD_TEXT = "&#128225; Join Discord"
NEW_TEXT = "Join Discord"


def restyle(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    content = content.replace(OLD_CTA, NEW_CTA)
    content = content.replace(OLD_HOVER, NEW_HOVER)
    content = content.replace(OLD_TEXT, NEW_TEXT)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


if __name__ == '__main__':
    files = glob.glob("**/*.html", recursive=True) + glob.glob("*.html")
    # deduplicate
    files = sorted(set(files))

    done = 0
    skipped = 0
    for fp in files:
        if restyle(fp):
            done += 1
        else:
            skipped += 1

    print(f"Updated : {done}")
    print(f"Skipped : {skipped}  (already restyled or no match)")
