#!/usr/bin/env python3
"""
Fix nav-cta lime buttons missed by the first pass.
These pages use '0.35rem' (leading zero) instead of '.35rem'.
Also cleans any stray nav emoji variants.
"""
import glob

# ── CSS replacements ─────────────────────────────────────────────────────────

OLD_CTA = (
    "nav-cta{background:var(--lime);color:var(--lime-text);"
    "text-decoration:none;padding:0.35rem 1rem;"
    "font-size:0.78rem;font-weight:700;border-radius:4px;"
    "margin-left:0.6rem;transition:opacity 0.2s;}"
)
NEW_CTA = (
    "nav-cta{background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%);"
    "color:#060a0f;"
    "text-decoration:none;padding:0.35rem 1rem;"
    "font-size:0.78rem;font-weight:700;border-radius:6px;"
    "margin-left:0.6rem;transition:transform 0.18s,box-shadow 0.18s;"
    "box-shadow:0 2px 10px rgba(110,231,183,.28);}"
)

OLD_HOVER = "nav-cta:hover{opacity:0.88;}"
NEW_HOVER = "nav-cta:hover{transform:translateY(-1px);box-shadow:0 4px 18px rgba(110,231,183,.45);}"

# Also catch the compact version (no leading zero, already handled but belt+suspenders)
OLD_CTA_COMPACT = (
    "nav-cta{background:var(--lime);color:var(--lime-text);"
    "text-decoration:none;padding:.35rem 1rem;"
    "font-size:.78rem;font-weight:700;border-radius:4px;"
    "margin-left:.6rem;transition:opacity .2s;}"
)
NEW_CTA_COMPACT = (
    "nav-cta{background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%);"
    "color:#060a0f;"
    "text-decoration:none;padding:.35rem 1rem;"
    "font-size:.78rem;font-weight:700;border-radius:6px;"
    "margin-left:.6rem;transition:transform .18s,box-shadow .18s;"
    "box-shadow:0 2px 10px rgba(110,231,183,.28);}"
)
OLD_HOVER_COMPACT = "nav-cta:hover{opacity:.88;}"
NEW_HOVER_COMPACT = "nav-cta:hover{transform:translateY(-1px);box-shadow:0 4px 18px rgba(110,231,183,.45);}"

# ── Text replacements (all emoji variants in nav button) ─────────────────────
TEXT_FIXES = [
    # satellite dish emoji (sweepstakes-casino-list)
    ("\U0001f4e1 Join Discord", "Join Discord"),
    ("📡 Join Discord",        "Join Discord"),
    # megaphone (already handled, belt+suspenders)
    ("&#128225; Join Discord", "Join Discord"),
    ("📣 Join Discord",        "Join Discord"),
    # pager / other
    ("&#128226; Join Discord", "Join Discord"),
    ("📢 Join Discord",        "Join Discord"),
]


def fix(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # CSS
    content = content.replace(OLD_CTA, NEW_CTA)
    content = content.replace(OLD_HOVER, NEW_HOVER)
    content = content.replace(OLD_CTA_COMPACT, NEW_CTA_COMPACT)
    content = content.replace(OLD_HOVER_COMPACT, NEW_HOVER_COMPACT)

    # Text / emoji
    for old, new in TEXT_FIXES:
        content = content.replace(old, new)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


if __name__ == "__main__":
    files = sorted(set(glob.glob("**/*.html", recursive=True) + glob.glob("*.html")))
    updated, skipped = 0, 0
    for fp in files:
        if fix(fp):
            print(f"  OK: {fp}")
            updated += 1
        else:
            skipped += 1
    print(f"\nUpdated: {updated}  |  Already clean: {skipped}")
