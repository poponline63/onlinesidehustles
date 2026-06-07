"""
Replace plain/wrong CTA button URLs in review pages with correct affiliate links.
Only touches pages where the cta-btn href is missing an affiliate parameter.
"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Map: review filename -> correct affiliate URL
# Only entries where the current link is plain/wrong
FIXES = {
    'review-crown-coins.html':  'https://crowncoinscasino.com/?utm_campaign=364f186b-7369-428b-a22c-dbeaf57940c7&utm_source=friends',
    'review-funrize.html':      'https://funrize.com/?invited_by=Z1Y2ZX',
    'review-high5.html':        'https://affiliates.routy.app/route/83977?affId=3353&ts=5004204',
    'review-lonestar.html':     'https://affiliates.routy.app/route/114339?affId=3353&ts=5005447',
    'review-megabonanza.html':  'https://affiliates.routy.app/route/91194?affId=3353&ts=5005447',
    'review-myprize.html':      'https://myprize.us/invite/harshRefrigerator34',
    'review-playfame.html':     'https://affiliates.routy.app/route/91215?affId=3353&ts=5005447',
    'review-pulsz-bingo.html':  'https://www.pulszbingo.com/home?invited_by=u358hj',
    'review-realprize.html':    'https://affiliates.routy.app/route/91231?affId=3353&ts=5005447',
    'review-shuffle.html':      'https://shuffle.us/?r=5b9js7cl9r',
    'review-spree.html':        'https://affiliates.routy.app/route/95239?affId=3353&ts=5005447',
    'review-stake-us.html':     'http://stake.us/?c=GZSweeps&offer=gzsweeps',
    'review-goldenhearts.html': 'https://www.goldenheartsgames.com/',
    'review-golden-hearts.html':'https://www.goldenheartsgames.com/',
}

# No affiliate available for these — skip silently
NO_AFFILIATE = {'review-legacy-arcade.html', 'review-sweeptastic.html', 'review-thrillz.html'}

def replace_cta_href(html, new_href):
    """Replace href inside every <a class="cta-btn"> tag."""
    def fix_tag(m):
        tag = m.group(0)
        return re.sub(r'href="[^"]*"', f'href="{new_href}"', tag)
    # Match opening <a> tag containing cta-btn in its class attribute
    return re.sub(r'<a\b[^>]*\bclass="[^"]*\bcta-btn\b[^"]*"[^>]*>', fix_tag, html)

changed = 0
for fname, aff_url in FIXES.items():
    if not os.path.exists(fname):
        print(f'  MISSING:  {fname}')
        continue
    with open(fname, 'r', encoding='utf-8') as f:
        original = f.read()

    updated = replace_cta_href(original, aff_url)

    if updated == original:
        print(f'  NO CHANGE:{fname}  (link may already be correct)')
        continue

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(updated)
    print(f'  FIXED:    {fname}')
    changed += 1

print(f'\nDone: {changed} files updated.')
print(f'Skipped (no affiliate available): {", ".join(sorted(NO_AFFILIATE))}')
