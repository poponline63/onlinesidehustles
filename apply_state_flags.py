import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

ABBR = {
    'Alabama':'al','Alaska':'ak','Arizona':'az','Arkansas':'ar',
    'California':'ca','Colorado':'co','Connecticut':'ct','Delaware':'de',
    'Florida':'fl','Georgia':'ga','Hawaii':'hi','Idaho':'id',
    'Illinois':'il','Indiana':'in','Iowa':'ia','Kansas':'ks',
    'Kentucky':'ky','Louisiana':'la','Maine':'me','Maryland':'md',
    'Massachusetts':'ma','Michigan':'mi','Minnesota':'mn','Mississippi':'ms',
    'Missouri':'mo','Montana':'mt','Nebraska':'ne','Nevada':'nv',
    'New Hampshire':'nh','New Jersey':'nj','New Mexico':'nm','New York':'ny',
    'North Carolina':'nc','North Dakota':'nd','Ohio':'oh','Oklahoma':'ok',
    'Oregon':'or','Pennsylvania':'pa','Rhode Island':'ri','South Carolina':'sc',
    'South Dakota':'sd','Tennessee':'tn','Texas':'tx','Utah':'ut',
    'Vermont':'vt','Virginia':'va','Washington':'wa','West Virginia':'wv',
    'Wisconsin':'wi','Wyoming':'wy',
}

c = open('states-hub.html', encoding='utf-8').read()

# ── 1. Swap CSS: replace abbreviation badge with flag image style ──────────
OLD_ABBR_CSS = (
    '.state-abbr{width:58px;height:58px;border-radius:13px;'
    'background:var(--sa-faint,rgba(110,231,183,.08));'
    'color:var(--sa,var(--teal));'
    'font-size:1.1rem;font-weight:800;'
    'display:flex;align-items:center;justify-content:center;'
    'position:relative;z-index:2;'
    'border:2px solid var(--sa-border,rgba(110,231,183,.25));'
    'box-shadow:0 4px 18px rgba(0,0,0,.55);'
    'font-family:\'IBM Plex Mono\',monospace;'
    'letter-spacing:.05em;}'
)
NEW_FLAG_CSS = (
    '.state-flag{'
    'width:90px;height:56px;'
    'object-fit:cover;'
    'border-radius:6px;'
    'position:relative;z-index:2;'
    'border:2px solid rgba(255,255,255,.12);'
    'box-shadow:0 4px 18px rgba(0,0,0,.55);'
    '}'
)
if OLD_ABBR_CSS in c:
    c = c.replace(OLD_ABBR_CSS, NEW_FLAG_CSS)
    print('Replaced .state-abbr CSS with .state-flag CSS')
else:
    # Try to find and replace just the .state-abbr block
    c = re.sub(
        r'\.state-abbr\{[^}]+\}',
        NEW_FLAG_CSS,
        c
    )
    print('Replaced via regex')

# ── 2. Update icon-wrap height to better suit landscape flags ──────────────
c = c.replace(
    'state-icon-wrap{height:90px;',
    'state-icon-wrap{height:86px;'
)

# ── 3. Replace each <div class="state-abbr">XX</div> with <img> ───────────
count = 0
for state, abbr in ABBR.items():
    old = f'<div class="state-abbr">{abbr.upper()}</div>'
    new = f'<img class="state-flag" src="/images/states/{abbr}.png" alt="{state} flag" loading="lazy">'
    if old in c:
        c = c.replace(old, new)
        count += 1
    else:
        print(f'  WARNING: abbr div not found for {state} ({abbr.upper()})')

print(f'Replaced {count} state abbreviation badges with flag images')

open('states-hub.html', 'w', encoding='utf-8').write(c)
print(f'Done — {len(c)//1000}KB')
