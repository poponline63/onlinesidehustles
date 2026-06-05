import sys, os, glob
sys.stdout.reconfigure(encoding='utf-8')

repo = os.path.dirname(os.path.abspath(__file__))
changed = []

# ── 1. Fix broken emoji in casino-reviews.html ──────────────────────────────
cr_path = os.path.join(repo, 'casino-reviews.html')
c = open(cr_path, encoding='utf-8').read()
# The broken sequence from the write tool
if "'\uD83E滋'" in c or "'\uD83E滋'" in c:
    c = c.replace("'\uD83E滋'", "'🤑'").replace("'\uD83E滋'", "'🤑'")
    open(cr_path, 'w', encoding='utf-8').write(c)
    changed.append('casino-reviews.html — fixed broken emoji')
else:
    # Check the raw bytes for the malformed sequence and replace the whole COINS line
    needle = "const COINS=["
    idx = c.find(needle)
    if idx != -1:
        end = c.find("];", idx)
        if end != -1:
            old_coins = c[idx:end+2]
            new_coins = "const COINS=['💰','🤑','💵','💎'];"
            if old_coins != new_coins:
                c = c[:idx] + new_coins + c[end+2:]
                open(cr_path, 'w', encoding='utf-8').write(c)
                changed.append('casino-reviews.html — replaced COINS array: ' + repr(old_coins[:60]))

# ── 2. React bundle: update reviews-hub → casino-reviews in nav href ─────────
bundle_path = os.path.join(repo, 'assets', 'index-BeuzeApR.js')
if os.path.exists(bundle_path):
    b = open(bundle_path, encoding='utf-8').read()
    old1 = 'href:"https://onlinesidehustles.info/reviews-hub"'
    new1 = 'href:"https://onlinesidehustles.info/casino-reviews"'
    if old1 in b:
        b = b.replace(old1, new1)
        open(bundle_path, 'w', encoding='utf-8').write(b)
        changed.append('assets/index-BeuzeApR.js — nav href updated to /casino-reviews')
    else:
        print('  [WARN] bundle nav href not found — already updated or pattern changed')
        # Print surrounding context to diagnose
        idx = b.find('casino-reviews')
        if idx != -1:
            print('  Found "casino-reviews" at index', idx, ':', repr(b[max(0,idx-40):idx+50]))
        idx2 = b.find('reviews-hub')
        if idx2 != -1:
            print('  Still found "reviews-hub" at index', idx2, ':', repr(b[max(0,idx2-40):idx2+50]))

# ── 3. All review pages: update /reviews-hub → /casino-reviews in nav ────────
review_files = glob.glob(os.path.join(repo, 'review-*.html'))
print(f'Found {len(review_files)} review pages to update')

for fpath in sorted(review_files):
    fname = os.path.basename(fpath)
    content = open(fpath, encoding='utf-8').read()
    original = content

    # Desktop nav link
    content = content.replace('href="/reviews-hub" class="nav-link active">Casino Reviews',
                               'href="/casino-reviews" class="nav-link active">Casino Reviews')
    content = content.replace('href="/reviews-hub" class="nav-link">Casino Reviews',
                               'href="/casino-reviews" class="nav-link">Casino Reviews')

    # Mobile menu link
    content = content.replace('<a href="/reviews-hub">Casino Reviews</a>',
                               '<a href="/casino-reviews">Casino Reviews</a>')

    if content != original:
        open(fpath, 'w', encoding='utf-8').write(content)
        changed.append(f'{fname} — updated /reviews-hub → /casino-reviews')
    else:
        # Check if it already has casino-reviews
        if '/casino-reviews' in content:
            print(f'  {fname} — already has /casino-reviews, no change needed')
        else:
            print(f'  [WARN] {fname} — no matching pattern found')

print('\n=== CHANGES MADE ===')
for line in changed:
    print(' ✓', line)
print(f'\nTotal: {len(changed)} files updated')
