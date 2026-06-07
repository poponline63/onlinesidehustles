#!/usr/bin/env python3
"""
1. Copy sportsbetting-automation.html → bookie-bandit-sportsbetting.html
   - Update canonical, OG, Twitter URLs
   - Update title & description (review-focused)
   - Add Review JSON-LD schema alongside existing BreadcrumbList
   - Update breadcrumb URL
2. Turn sportsbetting-automation.html into a 301 redirect page
3. Update _redirects file
4. Update all internal links site-wide
"""
import os, re, glob, shutil

OLD_SLUG = "sportsbetting-automation"
NEW_SLUG = "bookie-bandit-sportsbetting"
BASE_URL = "https://onlinesidehustles.info"

# ── Review JSON-LD to inject ─────────────────────────────────────────────────
REVIEW_SCHEMA = '''    <script type="application/ld+json">
    {"@context":"https://schema.org","@type":"Review","name":"Bookie Bandit Review 2026","reviewBody":"Bookie Bandit is an AI-powered automated sports betting bot that finds and places +EV bets across 14+ sportsbooks including FanDuel, DraftKings, PrizePicks, and Underdog. No sports knowledge needed — the bot scans odds 24/7 and places bets automatically.","author":{"@type":"Organization","name":"Online Sidehustles","url":"https://onlinesidehustles.info"},"datePublished":"2026-06-06","reviewRating":{"@type":"Rating","ratingValue":"4.5","bestRating":"5","worstRating":"1"},"itemReviewed":{"@type":"SoftwareApplication","name":"Bookie Bandit","applicationCategory":"SportsApplication","operatingSystem":"Windows, MacOS","url":"https://whop.com/bookiebandit/bookiebanditdfs?a=aei0n","offers":{"@type":"Offer","price":"333","priceCurrency":"USD"}}}
    </script>'''

# ── Step 1: create bookie-bandit-sportsbetting.html ──────────────────────────
src = "sportsbetting-automation.html"
dst = "bookie-bandit-sportsbetting.html"

with open(src, "r", encoding="utf-8") as f:
    content = f.read()

# Update canonical + OG/Twitter URLs
content = content.replace(
    f'<link rel="canonical" href="{BASE_URL}/{OLD_SLUG}">',
    f'<link rel="canonical" href="{BASE_URL}/{NEW_SLUG}">'
)
content = content.replace(
    f'"og:url" content="{BASE_URL}/{OLD_SLUG}"',
    f'"og:url" content="{BASE_URL}/{NEW_SLUG}"'
)
content = content.replace(
    f'"twitter:url" content="{BASE_URL}/{OLD_SLUG}"',
    f'"twitter:url" content="{BASE_URL}/{NEW_SLUG}"'
)

# Update breadcrumb URL in existing JSON-LD
content = content.replace(
    f'"item":"{BASE_URL}/{OLD_SLUG}"',
    f'"item":"{BASE_URL}/{NEW_SLUG}"'
)

# Update title — make it review-focused
content = content.replace(
    "<title>Bookie Bandit 2026 | AI Sports Betting Automation Bot</title>",
    "<title>Bookie Bandit Review 2026: AI Sports Betting Bot — Legit or Not? | Online Sidehustles</title>"
)

# Update meta description — review-focused
content = content.replace(
    '<meta name="description" content="Bookie Bandit AI sports betting bot 2026. Automate PrizePicks, Underdog, FanDuel, DraftKings &amp; more. No sports knowledge needed. Best betting side hustle 2026.">',
    '<meta name="description" content="Honest Bookie Bandit review 2026. AI bot that automates +EV sports betting across 14+ sportsbooks including PrizePicks, FanDuel, DraftKings &amp; Underdog. 4.8/5 from 362 Whop reviews.">'
)

# Update OG title to review-focused
content = content.replace(
    '"og:title" content="Bookie Bandit 2026 | AI Sports Betting Automation Bot"',
    '"og:title" content="Bookie Bandit Review 2026 | AI Sports Betting Bot Tested"'
)
content = content.replace(
    '"twitter:title" content="Bookie Bandit 2026 | AI Sports Betting Automation Bot"',
    '"twitter:title" content="Bookie Bandit Review 2026 | AI Sports Betting Bot Tested"'
)

# Update OG description
content = content.replace(
    '"og:description" content="Automate sports betting with Bookie Bandit AI 2026. Find +EV bets automatically across 14+ sportsbooks. No sports knowledge needed."',
    '"og:description" content="Honest Bookie Bandit review 2026. AI sports betting bot with 4.8/5 Whop rating and 1.13M+ bets placed. +EV automation across 14+ sportsbooks."'
)
content = content.replace(
    '"twitter:description" content="Bookie Bandit automated sports betting with AI. Zero sports knowledge needed. Fully automated +EV picks across 14+ sportsbooks."',
    '"twitter:description" content="Honest Bookie Bandit review 2026. AI sports betting bot with 4.8/5 Whop rating. +EV automation across 14+ sportsbooks — legit or not?"'
)

# Inject Review schema right after the existing BreadcrumbList script block
BREADCRUMB_END = '    </script>\n\n    <link rel="preconnect"'
INJECT_AFTER = f'    </script>\n{REVIEW_SCHEMA}\n\n    <link rel="preconnect"'
content = content.replace(BREADCRUMB_END, INJECT_AFTER, 1)

with open(dst, "w", encoding="utf-8") as f:
    f.write(content)
print(f"  CREATED: {dst}")

# ── Step 2: turn sportsbetting-automation.html into a redirect ────────────────
redirect_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0;url=/{NEW_SLUG}">
  <link rel="canonical" href="{BASE_URL}/{NEW_SLUG}">
  <title>Redirecting to Bookie Bandit Review...</title>
</head>
<body>
  <p>Redirecting to <a href="/{NEW_SLUG}">Bookie Bandit Review</a>...</p>
  <script>window.location.replace('/{NEW_SLUG}');</script>
</body>
</html>"""

with open(src, "w", encoding="utf-8") as f:
    f.write(redirect_html)
print(f"  REDIRECTED: {src} → /{NEW_SLUG}")

# ── Step 3: update _redirects ─────────────────────────────────────────────────
with open("_redirects", "r", encoding="utf-8") as f:
    redirects = f.read()

# Change the 200 rewrite for old slug to a 301, add new 200 rewrite
redirects = redirects.replace(
    f"/{OLD_SLUG}   /{OLD_SLUG}.html      200",
    f"/{OLD_SLUG}   /{NEW_SLUG}              301"
)
# Insert new 200 rewrite for new slug after the 301 line
new_rewrite = f"/{NEW_SLUG}   /{NEW_SLUG}.html   200\n"
redirects = redirects.replace(
    f"/{OLD_SLUG}   /{NEW_SLUG}              301\n",
    f"/{OLD_SLUG}   /{NEW_SLUG}              301\n{new_rewrite}"
)

with open("_redirects", "w", encoding="utf-8") as f:
    f.write(redirects)
print("  UPDATED: _redirects")

# ── Step 4: update internal links site-wide ───────────────────────────────────
# Patterns to replace (both with and without .html extension, with and without leading slash)
replacements = [
    # absolute links
    (f'href="/sportsbetting-automation"',        f'href="/{NEW_SLUG}"'),
    (f'href="/sportsbetting-automation.html"',   f'href="/{NEW_SLUG}"'),
    # relative links from root-level pages
    (f'href="sportsbetting-automation.html"',    f'href="{NEW_SLUG}.html"'),
    (f'href="sportsbetting-automation"',         f'href="{NEW_SLUG}"'),
    # relative links from subdirectories (comparisons/, reports/)
    (f'href="../sportsbetting-automation.html"', f'href="../{NEW_SLUG}.html"'),
    (f'href="../sportsbetting-automation"',      f'href="../{NEW_SLUG}"'),
]

html_files = sorted(set(
    glob.glob("**/*.html", recursive=True) + glob.glob("*.html")
))
# Skip the files we just wrote
skip = {src, dst}
updated_links = []
for fp in html_files:
    if fp in skip:
        continue
    with open(fp, "r", encoding="utf-8") as f:
        original = f.read()
    changed = original
    for old, new in replacements:
        changed = changed.replace(old, new)
    if changed != original:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(changed)
        updated_links.append(fp)
        print(f"  LINKS: {fp}")

print(f"\nDone. Created: {dst}  |  Redirect: {src}  |  Links updated: {len(updated_links)}")
