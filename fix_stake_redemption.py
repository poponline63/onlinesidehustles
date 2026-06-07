"""
Add "Redemption Mode Only" notice to Stake.us card on all restricted state pages.
Stake.us is fully restricted (no new signups/gameplay) in 21 states.
Existing users can only redeem their existing Stake Cash balance.
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 21 states where Stake.us is restricted (no new signups or gameplay)
RESTRICTED_STATES = [
    'arizona', 'california', 'connecticut', 'delaware', 'idaho',
    'illinois', 'indiana', 'kentucky', 'louisiana', 'maryland',
    'michigan', 'montana', 'nevada', 'new-jersey', 'new-york',
    'pennsylvania', 'rhode-island', 'tennessee', 'vermont',
    'washington', 'west-virginia',
]

# The exact Stake.us card body opening (unique across the file)
OLD_BODY = '''        <div class="rc-body">
          <div class="rc-name">Stake.us</div>'''

NEW_BODY = '''        <div class="rc-body">
          <div style="background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.25);border-radius:5px;padding:.3rem .65rem;font-size:.72rem;color:#fca5a5;font-weight:700;margin-bottom:.5rem;letter-spacing:.02em;">&#9888; Redemption Mode Only &#8212; no new signups in this state</div>
          <div class="rc-name">Stake.us</div>'''

# Also change the CTA button text
OLD_CTA = '<div class="rc-cta-btn">Sign Up Free &#8594;</div>'
NEW_CTA = '<div class="rc-cta-btn" style="background:rgba(239,68,68,.15);border-color:rgba(239,68,68,.3);color:#fca5a5;">Redeem SC Only &#8594;</div>'

changed = 0
for state in RESTRICTED_STATES:
    filepath = f'casinos-in-{state}.html'
    if not os.path.exists(filepath):
        print(f'  MISSING: {filepath}')
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check it has the Stake card and hasn't already been patched
    if OLD_BODY not in content:
        if 'Redemption Mode Only' in content:
            print(f'  ALREADY PATCHED: {filepath}')
        else:
            print(f'  NO STAKE CARD FOUND: {filepath}')
        continue

    content = content.replace(OLD_BODY, NEW_BODY, 1)

    # Also patch the CTA button — only in the Stake card context
    # Find the Stake card block and replace only that CTA
    stake_start = content.find('data-name="stake.us"')
    if stake_start != -1:
        # Find next rc-cta-btn after the stake card start
        cta_pos = content.find(OLD_CTA, stake_start)
        if cta_pos != -1:
            content = content[:cta_pos] + NEW_CTA + content[cta_pos + len(OLD_CTA):]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'  PATCHED: {filepath}')
    changed += 1

print(f'\nDone: {changed}/{len(RESTRICTED_STATES)} state pages updated')
