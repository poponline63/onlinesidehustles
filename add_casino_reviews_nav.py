import sys, os, glob
sys.stdout.reconfigure(encoding='utf-8')

repo = os.path.dirname(os.path.abspath(__file__))

# ── Patterns to find and replace ──────────────────────────────────────────────
# Desktop nav (6-space or different indentation variants)
# Pattern: sweepstakes-casino-list nav-link ... followed by side-hustles nav-link
# We cover both "class="nav-link"" and "class="nav-link active"" for the SC list
NAV_REPLACEMENTS = [
    # Standard pattern across most pages (6 spaces indent)
    (
        'href="/sweepstakes-casino-list" class="nav-link">Sweepstakes Casinos List</a>\n      <a href="/side-hustles"',
        'href="/sweepstakes-casino-list" class="nav-link">Sweepstakes Casinos List</a>\n      <a href="/casino-reviews" class="nav-link">Casino Reviews</a>\n      <a href="/side-hustles"'
    ),
    # Variant: sweepstakes-casino-list is the ACTIVE link (on sweepstakes-casino-list page itself)
    (
        'href="/sweepstakes-casino-list" class="nav-link active">Sweepstakes Casinos List</a>\n      <a href="/side-hustles"',
        'href="/sweepstakes-casino-list" class="nav-link active">Sweepstakes Casinos List</a>\n      <a href="/casino-reviews" class="nav-link">Casino Reviews</a>\n      <a href="/side-hustles"'
    ),
]

# Mobile menu pattern
MOBILE_REPLACEMENTS = [
    (
        '  <a href="/sweepstakes-casino-list">Sweepstakes Casinos List</a>\n  <a href="/side-hustles">',
        '  <a href="/sweepstakes-casino-list">Sweepstakes Casinos List</a>\n  <a href="/casino-reviews">Casino Reviews</a>\n  <a href="/side-hustles">'
    ),
]

# ── Collect all HTML files ─────────────────────────────────────────────────────
all_html = (
    glob.glob(os.path.join(repo, '*.html')) +
    glob.glob(os.path.join(repo, 'blog', '*.html')) +
    glob.glob(os.path.join(repo, 'blog', '**', '*.html')) +
    glob.glob(os.path.join(repo, 'comparisons', '*.html')) +
    glob.glob(os.path.join(repo, 'reports', '*.html'))
)

updated = []
skipped_has_it = []
skipped_no_nav = []

for fpath in sorted(all_html):
    fname = os.path.relpath(fpath, repo).replace('\\', '/')

    # Skip index.html (React SPA — nav is in JS bundle)
    if fname in ('index.html', 'index2.html'):
        continue

    content = open(fpath, encoding='utf-8', errors='ignore').read()

    # Skip if casino-reviews is already in the file
    if '/casino-reviews' in content:
        skipped_has_it.append(fname)
        continue

    # Skip if no nav-link at all (not a page with our nav)
    if 'nav-link' not in content and 'class="nav-link"' not in content:
        skipped_no_nav.append(fname)
        continue

    original = content

    # Apply desktop nav replacements
    for old, new in NAV_REPLACEMENTS:
        if old in content:
            content = content.replace(old, new)
            break  # only one variant will match

    # Apply mobile menu replacement
    for old, new in MOBILE_REPLACEMENTS:
        if old in content:
            content = content.replace(old, new)
            break

    if content != original:
        open(fpath, 'w', encoding='utf-8').write(content)
        updated.append(fname)
    else:
        # Has nav-link but pattern didn't match — report for diagnosis
        # Check if it has the sweepstakes-casino-list link at all
        if 'sweepstakes-casino-list' not in content:
            skipped_no_nav.append(fname + ' [no sweepstakes link]')
        else:
            skipped_no_nav.append(fname + ' [pattern mismatch — manual check needed]')

print(f'=== UPDATED ({len(updated)} files) ===')
for f in updated:
    print(' ✓', f)

print(f'\n=== SKIPPED — already has Casino Reviews ({len(skipped_has_it)} files) ===')
for f in skipped_has_it:
    print(' –', f)

if skipped_no_nav:
    print(f'\n=== SKIPPED — no matching nav pattern ({len(skipped_no_nav)} files) ===')
    for f in skipped_no_nav:
        print(' ?', f)
