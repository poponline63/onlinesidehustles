import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ── Bare URL → referral URL mapping ───────────────────────────────────────
# Sourced directly from SIGNUP_LINKS in sweepstakes-casino-list.html.
# Only exact bare URLs (no query params) are replaced.
# URLs pointing to help articles / PDFs / rules pages are never touched.

REPLACE_MAP = [
    # ── Major casinos (50+ state files each) ────────────────────────────────
    ('https://www.chanced.com',        'https://www.chanced.com/c/q9xsr3'),
    ('https://www.chumbacasino.com/',  'https://login.chumbacasino.com/register'),
    ('https://www.chumbacasino.com',   'https://login.chumbacasino.com/register'),
    ('https://www.fortunecoins.com',   'https://track.fortunecoins.fun/click?o=1&a=101612&c=16'),
    ('https://www.getfliff.com',       'https://apps.apple.com/us/app/fliff-social-sports-picks/id1489145500'),
    ('https://www.globalpoker.com/',   'https://play.globalpoker.com'),
    ('https://www.globalpoker.com',    'https://play.globalpoker.com'),
    ('https://play.globalpoker.com',   'https://play.globalpoker.com'),  # normalize (already canonical)
    ('https://www.hellomillions.com',  'https://affiliates.routy.app/route/91164?affId=3353&ts=5005447'),
    ('https://www.jackpota.com',       'https://www.jackpota.com/?r=55627563'),
    ('https://www.mcluck.com',         'https://affiliates.routy.app/route/91184?affId=3353&ts=5005447'),
    ('https://www.moozi.com',          'https://moozi.com/signup?referral_code=1483842358'),
    ('https://www.pulsz.com',          'https://affiliates.routy.app/route/91228?affId=3353&ts=5005447'),
    ('https://www.rebet.com',          'https://rebet.page.link/2Rmytf3dtYSbor9m9'),
    ('https://www.sixty6.com',         'https://affiliates.routy.app/route/114424?affId=3353&ts=5005447'),
    ('https://www.sportzino.com',      'https://track.sportzino.fun/click?o=2&a=101612&c=18'),
    ('https://www.zulacasino.com',     'https://track.zulacasino.fun/click?o=3&a=101612&c=17'),
    ('https://www.wowvegas.com',       'https://www.wowvegas.com/?raf=4166140'),
    # ── Single-file / review-page-only ──────────────────────────────────────
    ('https://www.nolimitcoins.com',   'https://nolimitcoins.com/lobby/?invited_by=0MB973'),
    ('https://www.modo.us',            'https://modo.us/?referralCode=VF29HS'),
    ('https://www.taofortune.com',     'https://taofortune.com/lobby/?invited_by=N9YAYZ'),
    ('https://www.luckyhands.com',     'https://luckyhands.com/sign-up?code=0f6adf5b-61c1-47c4-b19d-ed570fcb6263'),
    # ── These exist in SIGNUP_LINKS but have no referral code — normalise only
    ('https://www.luckylandslots.com/', 'https://luckylandslots.com/'),
    ('https://www.luckylandslots.com',  'https://luckylandslots.com/'),
    ('https://www.moonspin.us',         'https://moonspin.us/'),
]

# ── URLs to NEVER touch (help articles, PDFs, rules pages) ────────────────
SKIP_SUBSTRINGS = [
    'help.stake.us',
    'help.wowvegas.com',
    '/documents/',
    '/sweeps-rules',
    'sweepstakes-rules',
    'media.luckylandcasino.com',
    '#/?lpPanel',
    'play.globalpoker.com',      # don't re-replace already-canonical GP links
]

# ── Casinos with NO referral link available → report only ─────────────────
NO_REF = [
    ('rubysweeps.com',       'RubySweeps — not in your SIGNUP_LINKS at all'),
    ('legacyarcade.com',     'Legacy Arcade — not in your SIGNUP_LINKS at all'),
    ('goldrushcity.com',     'GoldRushCity — in your list but NO referral code (just the homepage URL)'),
    ('goldenheartsgames.com','Golden Hearts Games — in your list but NO referral code'),
    ('sidepot.us',           'Sidepot — in your list but NO referral code'),
    ('moonspin.us',          'MoonSpin — in your list but NO referral code (normalised www → non-www)'),
    ('luckylandslots.com',   'LuckyLandSlots — in your list but NO referral code (normalised www → non-www)'),
    ('funrize.com',          'FunRize — SIGNUP_LINKS maps it to FunzCity (funzcity.com). Looks like a mistake. Skipped — please correct the referral URL in your list.'),
]

# ── Walk all HTML files ────────────────────────────────────────────────────
html_files = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ['__pycache__','.git','images','node_modules']]
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

print(f'Scanning {len(html_files)} HTML files...\n')

total_replacements = 0
files_changed = 0
per_casino = {}

for path in sorted(html_files):
    try:
        c = open(path, encoding='utf-8').read()
    except Exception:
        continue
    original = c

    for bare, ref in REPLACE_MAP:
        if bare not in c:
            continue

        # Split on bare, but only replace when immediately followed by " or /
        # and the surrounding context is not a skip URL
        parts = c.split(bare)
        new_parts = [parts[0]]
        replaced_here = 0
        for i, part in enumerate(parts[1:], 1):
            # What comes right after bare?
            next_char = part[0] if part else ''
            # Reconstruct the full URL to check for skip substrings
            # (the bare URL IS the full thing we'd replace)
            if next_char == '"':
                # Bare domain followed directly by closing quote — perfect match
                # Check the preceding chars to verify it's actually in an href
                preceding = new_parts[-1][-20:] if new_parts else ''
                if 'href=' in preceding or 'action=' in preceding:
                    new_parts.append(ref)
                    replaced_here += 1
                else:
                    new_parts.append(bare)
            elif next_char in ('/', ' ', '\n', '\t'):
                # Could be bare/ — check if remaining URL has a skip substring
                closing = part.find('"')
                full_tail = part[:closing] if closing != -1 else part[:100]
                if any(s in (bare + full_tail) for s in SKIP_SUBSTRINGS):
                    new_parts.append(bare)
                elif closing == 0 or full_tail.strip('/') == '':
                    # Trailing slash only (e.g. bare + "/")
                    preceding = new_parts[-1][-20:] if new_parts else ''
                    if 'href=' in preceding or 'action=' in preceding:
                        new_parts.append(ref)
                        if closing != -1:
                            part = part[1:]  # skip the trailing slash
                        replaced_here += 1
                    else:
                        new_parts.append(bare)
                else:
                    new_parts.append(bare)
            else:
                # Part of a longer URL (e.g. /lobby, /signup) — don't replace
                new_parts.append(bare)
            new_parts.append(part)

        c = ''.join(new_parts)
        if replaced_here:
            per_casino[bare] = per_casino.get(bare, 0) + replaced_here
            total_replacements += replaced_here

    if c != original:
        open(path, 'w', encoding='utf-8').write(c)
        files_changed += 1

# ── Report ─────────────────────────────────────────────────────────────────
print(f'Replaced {total_replacements} bare links across {files_changed} files.\n')
print('Per-casino breakdown:')
for bare, ref in REPLACE_MAP:
    count = per_casino.get(bare, 0)
    domain = bare.replace('https://www.','').replace('https://','').rstrip('/')
    if count:
        print(f'  ✓ {domain:35s} {count} replacements')
    else:
        print(f'  - {domain:35s} 0 (none found or already correct)')

print()
print('─' * 60)
print('SKIPPED (no referral link available):')
for domain, note in NO_REF:
    # Count remaining occurrences
    cnt = sum(
        1 for path in html_files
        for m in re.findall(rf'href="https?://(?:www\.)?{re.escape(domain)}"',
                            open(path, encoding='utf-8', errors='ignore').read())
    )
    print(f'  ✗ {note}')
    if cnt:
        print(f'      ({cnt} bare occurrences still in site)')
