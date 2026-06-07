import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

REGIONS = {
    'Alabama':'se','Alaska':'wt','Arizona':'sw','Arkansas':'se',
    'California':'wt','Colorado':'sw','Connecticut':'ne','Delaware':'ne',
    'Florida':'se','Georgia':'se','Hawaii':'wt','Idaho':'wt',
    'Illinois':'mw','Indiana':'mw','Iowa':'mw','Kansas':'mw',
    'Kentucky':'se','Louisiana':'se','Maine':'ne','Maryland':'ne',
    'Massachusetts':'ne','Michigan':'mw','Minnesota':'mw','Mississippi':'se',
    'Missouri':'mw','Montana':'wt','Nebraska':'mw','Nevada':'wt',
    'New Hampshire':'ne','New Jersey':'ne','New Mexico':'sw','New York':'ne',
    'North Carolina':'se','North Dakota':'mw','Ohio':'mw','Oklahoma':'sw',
    'Oregon':'wt','Pennsylvania':'ne','Rhode Island':'ne','South Carolina':'se',
    'South Dakota':'mw','Tennessee':'se','Texas':'sw','Utah':'sw',
    'Vermont':'ne','Virginia':'se','Washington':'wt','West Virginia':'se',
    'Wisconsin':'mw','Wyoming':'wt',
}
ABBR = {
    'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR',
    'California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE',
    'Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID',
    'Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS',
    'Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD',
    'Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS',
    'Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV',
    'New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY',
    'North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK',
    'Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC',
    'South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT',
    'Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV',
    'Wisconsin':'WI','Wyoming':'WY',
}

NEW_CSS = '''
/* ===== STATE ICON (mirrors casino review card style) ===== */
.state-card.ne{--sa:#60a5fa;--sa-faint:rgba(96,165,250,.1);--sa-border:rgba(96,165,250,.28);--sa-glow:rgba(96,165,250,.15);}
.state-card.se{--sa:#6ee7b7;--sa-faint:rgba(110,231,183,.1);--sa-border:rgba(110,231,183,.28);--sa-glow:rgba(110,231,183,.15);}
.state-card.mw{--sa:#c084fc;--sa-faint:rgba(192,132,252,.1);--sa-border:rgba(192,132,252,.28);--sa-glow:rgba(192,132,252,.15);}
.state-card.sw{--sa:#fbbf24;--sa-faint:rgba(251,191,36,.1);--sa-border:rgba(251,191,36,.28);--sa-glow:rgba(251,191,36,.15);}
.state-card.wt{--sa:#34d399;--sa-faint:rgba(52,211,153,.1);--sa-border:rgba(52,211,153,.28);--sa-glow:rgba(52,211,153,.15);}
.state-icon-wrap{height:90px;background:linear-gradient(160deg,var(--bg-card2,#131e30) 0%,var(--bg,#111c2e) 100%);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;flex-shrink:0;border-radius:12px 12px 0 0;}
.state-icon-wrap::before{content:'';position:absolute;inset:0;background:radial-gradient(circle at 50% 60%,var(--sa-glow,rgba(110,231,183,.12)) 0%,transparent 68%);}
.state-icon-wrap::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:var(--sa,var(--teal));opacity:.85;}
.state-abbr{width:58px;height:58px;border-radius:13px;background:var(--sa-faint,rgba(110,231,183,.08));color:var(--sa,var(--teal));font-size:1.1rem;font-weight:800;display:flex;align-items:center;justify-content:center;position:relative;z-index:2;border:2px solid var(--sa-border,rgba(110,231,183,.25));box-shadow:0 4px 18px rgba(0,0,0,.55);font-family:'IBM Plex Mono',monospace;letter-spacing:.05em;}
.state-body{padding:.9rem 1rem .95rem;display:flex;flex-direction:column;justify-content:space-between;flex:1;}
.state-card:hover{border-color:var(--sa,var(--border-md));}
'''

c = open('states-hub.html', encoding='utf-8').read()

# ── 1. Patch .state-card CSS: remove padding, remove min-height, add padding:0 ──
c = c.replace(
    '  padding:1.1rem 1rem 1rem;\n  text-decoration:none;\n  color:var(--text);\n  transition:border-color .18s,transform .18s,box-shadow .18s;\n  position:relative;\n  overflow:hidden;\n  min-height:110px;',
    '  padding:0;\n  text-decoration:none;\n  color:var(--text);\n  transition:border-color .18s,transform .18s,box-shadow .18s;\n  position:relative;\n  overflow:hidden;'
)

# ── 2. Remove old hover border override that uses --border-md (will be overridden per region) ──
# (The .state-card:hover rule uses --border-md, we'll let region class override it via specificity)

# ── 3. Insert new CSS before </style> ──
c = c.replace('</style>', NEW_CSS + '</style>', 1)

# ── 4. Replace each state card using a direct string search per state ──
count = 0
for state, abbr in ABBR.items():
    region = REGIONS[state]
    slug = state.lower().replace(' ', '-')
    old_card = (
        f'    <a href="/casinos-in-{slug}" class="state-card">\n'
        f'      <div><div class="state-name">{state}</div>'
    )
    # Find full card
    start = c.find(old_card)
    if start == -1:
        print(f'  WARNING: card not found for {state}')
        continue
    end = c.find('</a>', start) + 4
    old_full = c[start:end]

    # Extract count from old card
    m = re.search(r'<div class="state-count">(.+?)</div>', old_full)
    count_html = m.group(1) if m else '<strong>?</strong> sites available'

    # Extract link text (before &#8594; or &#x2192; arrow)
    lm = re.search(r'<span class="state-link">([^<]+)</span>', old_full)
    link_text = lm.group(1) if lm else f'View {state} &#8594;'

    new_card = (
        f'    <a href="/casinos-in-{slug}" class="state-card {region}">\n'
        f'      <div class="state-icon-wrap"><div class="state-abbr">{abbr}</div></div>\n'
        f'      <div class="state-body">\n'
        f'        <div><div class="state-name">{state}</div><div class="state-count">{count_html}</div></div>\n'
        f'        <span class="state-link">{link_text}</span>\n'
        f'      </div>\n'
        f'    </a>'
    )
    c = c[:start] + new_card + c[end:]
    count += 1

print(f'Updated {count} state cards')
open('states-hub.html', 'w', encoding='utf-8').write(c)
print(f'Done — {len(c)//1000}KB')
