"""
Replace gstatic favicon API URLs with local /images/logos/{slug}.png
in all 50 state HTML pages (and any other HTML that uses them).
Only replaces domains where we have a GOOD quality local file (>8KB).
"""
import sys, os, glob
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Domain → local slug mapping (only include ones with good quality logos)
DOMAIN_SLUG = {
    'americanluck.com':     'americanluck',
    'chanced.com':          'chanced',
    'chumbacasino.com':     'chumbacasino',
    'crowncoinscasino.com': 'crowncoinscasino',
    'dimesweeps.com':       'dimesweeps',
    'getfliff.com':         'fliff',
    'fortunecoins.com':     'fortunecoins',
    'funrize.com':          'funrize',
    'hellomillions.com':    'hellomillions',
    'jackpota.com':         'jackpota',
    'mcluck.com':           'mcluck',
    'moozi.com':            'moozi',
    'pulsz.com':            'pulsz',
    'rubysweeps.com':       'rubysweeps',
    'scarletsands.com':     'scarletsands',
    'speedsweeps.com':      'speedsweeps',
    'spinquest.com':        'spinquest',
    'spinsagacasino.com':   'spinsaga',
    'sportzino.com':        'sportzino',
    'wowvegas.com':         'wowvegas',
    'zulacasino.com':       'zulacasino',
}

# Verify local files exist and are good quality
LOGOS_DIR = 'images/logos'
verified = {}
for domain, slug in DOMAIN_SLUG.items():
    path = f'{LOGOS_DIR}/{slug}.png'
    if os.path.exists(path):
        sz = os.path.getsize(path)
        if sz > 8000:
            verified[domain] = slug
        else:
            print(f'  SKIP {domain}: {slug}.png only {sz//1024}KB (too small)')
    else:
        print(f'  SKIP {domain}: {slug}.png not found')

print(f'Verified {len(verified)} domains with good local logos\n')

# Build the gstatic prefix
GSTATIC_BASE = 'https://t1.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://'
GSTATIC_SUFFIX = '&size=256'

# Find all HTML files
html_files = glob.glob('casinos-in-*.html') + glob.glob('*.html')
html_files = sorted(set(html_files))

total_replacements = 0
total_files_changed = 0

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    file_replacements = 0

    for domain, slug in verified.items():
        old = f'{GSTATIC_BASE}{domain}{GSTATIC_SUFFIX}'
        new = f'/images/logos/{slug}.png'
        count = content.count(old)
        if count > 0:
            content = content.replace(old, new)
            file_replacements += count

    if file_replacements > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  {filepath:45s} → {file_replacements} replacements')
        total_replacements += file_replacements
        total_files_changed += 1

print(f'\nDone: {total_replacements} replacements across {total_files_changed} files')
print(f'Domains NOT replaced (keeping gstatic): stake.us, rebet.com, legendzcasino.com,')
print(f'  luckylandslots.com, globalpoker.com, lonestarcasino.com, realprize.com, sixty6.com')
