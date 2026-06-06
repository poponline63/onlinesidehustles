#!/usr/bin/env python3
"""Add noindex,nofollow to all duplicate/test/draft pages."""

PAGES = [
    "blog2.html",
    "casino-ratings.html",
    "daily-login-guide-mockup.html",
    "daily-login-guide2.html",
    "daily-login-reviews.html",
    "gameplay-sheet.html",
    "getting-started2.html",
    "guide-player-2.html",
    "index2.html",
    "jupiter-post.html",
    "logo_test.html",
    "logo_test2.html",
    "side-hustles2.html",
    "tools2.html",
    "tracking-number-generator.html",
    "vote.html",
]

NOINDEX_TAG = '<meta name="robots" content="noindex, nofollow">'

for fp in PAGES:
    try:
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()

        if "noindex" in content:
            print(f"SKIP (already noindex): {fp}")
            continue

        # Insert right after <head> or <head ...>
        if "<head>" in content:
            updated = content.replace("<head>", f"<head>\n  {NOINDEX_TAG}", 1)
        elif "<head " in content:
            # find end of opening head tag
            idx = content.index("<head ")
            end = content.index(">", idx) + 1
            updated = content[:end] + f"\n  {NOINDEX_TAG}" + content[end:]
        else:
            # fallback: insert after <meta charset
            updated = content.replace("<meta charset", f"{NOINDEX_TAG}\n  <meta charset", 1)

        with open(fp, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"OK: {fp}")

    except FileNotFoundError:
        print(f"MISSING: {fp}")
