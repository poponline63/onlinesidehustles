"""
Redesign casino-reviews.html card section:
- Google Favicon API logos (no screenshots)
- Bigger logos with border/glow
- Score badge in card header
- Highlight callout row
- Stronger CTA button
- Fix count 25→24, Mid Tier 13→12
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'casino-reviews.html')
c = open(fpath, encoding='utf-8').read()

# ─── 1. Fix counts: 25 → 24, Mid Tier 13 → 12 ──────────────────────────────
c = c.replace(
    '<div class="hero-stat-val">25</div>',
    '<div class="hero-stat-val">24</div>'
)
c = c.replace(
    '"numberOfItems":25',
    '"numberOfItems":24'
)
c = c.replace(
    '<button class="ftab active" data-f="all">All (25)</button>',
    '<button class="ftab active" data-f="all">All (24)</button>'
)
c = c.replace(
    '<button class="ftab" data-f="mid">&#128201; Mid Tier (13)</button>',
    '<button class="ftab" data-f="mid">&#128201; Mid Tier (12)</button>'
)
c = c.replace(
    '<span class="tier-count">13 casinos</span>',
    '<span class="tier-count">12 casinos</span>'
)

# ─── 2. Replace CSS: review grid + card styles ──────────────────────────────
OLD_CSS = """/* ── Logo/screenshot header ── */
.rc-logo-wrap{
  height:165px;
  background-color:var(--bg-card2);
  background-image:var(--card-screenshot,none);
  background-size:cover;
  background-position:center top;
  display:flex;align-items:center;justify-content:center;
  position:relative;
  overflow:hidden;
  flex-shrink:0;
}
/* dark cinematic overlay over screenshot */
.rc-logo-wrap::before{
  content:'';position:absolute;inset:0;z-index:1;
  background:linear-gradient(180deg,
    rgba(5,9,18,.55) 0%,
    rgba(5,9,18,.42) 35%,
    rgba(5,9,18,.72) 70%,
    var(--bg-card) 100%
  );
}
/* accent line at the bottom edge */
.rc-logo-wrap::after{
  content:'';position:absolute;bottom:0;left:0;right:0;height:2px;z-index:3;
  background:var(--card-accent,transparent);opacity:.9;
}
.rc-logo-img{
  width:80px;height:80px;object-fit:contain;
  border-radius:16px;
  position:relative;z-index:2;
  background:rgba(5,9,18,.75);
  border:2px solid rgba(255,255,255,.16);
  padding:6px;
  box-shadow:0 6px 28px rgba(0,0,0,.8);
}
.rc-logo-fallback{
  width:80px;height:80px;border-radius:16px;
  background:var(--card-accent,var(--teal-faint));
  color:#fff;font-size:1.55rem;font-weight:800;
  display:flex;align-items:center;justify-content:center;
  position:relative;z-index:2;
  border:2px solid rgba(255,255,255,.16);
  box-shadow:0 6px 28px rgba(0,0,0,.8);
  text-shadow:0 2px 8px rgba(0,0,0,.6);
}
.rc-rank{
  position:absolute;top:.65rem;left:.7rem;z-index:4;
  font-family:'IBM Plex Mono',monospace;font-size:.6rem;font-weight:700;
  letter-spacing:.08em;color:rgba(255,255,255,.8);
  background:rgba(5,9,18,.75);
  border:1px solid rgba(255,255,255,.14);
  padding:.18rem .5rem;border-radius:4px;
}"""

NEW_CSS = """/* ── Logo header ── */
.rc-logo-wrap{
  height:150px;
  background:linear-gradient(160deg,var(--bg-card2) 0%,var(--bg) 100%);
  display:flex;align-items:center;justify-content:center;
  position:relative;
  overflow:hidden;
  flex-shrink:0;
}
/* radial glow behind logo */
.rc-logo-wrap::before{
  content:'';position:absolute;inset:0;z-index:1;
  background:radial-gradient(circle at 50% 55%, var(--card-glow,rgba(110,231,183,.12)) 0%, transparent 68%);
}
/* accent line at the bottom edge */
.rc-logo-wrap::after{
  content:'';position:absolute;bottom:0;left:0;right:0;height:2px;z-index:3;
  background:var(--card-accent,transparent);opacity:.9;
}
.rc-logo-img{
  width:84px;height:84px;object-fit:contain;
  border-radius:18px;
  position:relative;z-index:2;
  background:rgba(5,9,18,.55);
  border:2px solid rgba(255,255,255,.14);
  padding:6px;
  box-shadow:0 6px 28px rgba(0,0,0,.7);
}
.rc-logo-fallback{
  width:84px;height:84px;border-radius:18px;
  background:var(--card-accent,var(--teal-faint));
  color:#fff;font-size:1.55rem;font-weight:800;
  display:flex;align-items:center;justify-content:center;
  position:relative;z-index:2;
  border:2px solid rgba(255,255,255,.14);
  box-shadow:0 6px 28px rgba(0,0,0,.7);
  text-shadow:0 2px 8px rgba(0,0,0,.6);
}
.rc-rank{
  position:absolute;top:.65rem;left:.7rem;z-index:4;
  font-family:'IBM Plex Mono',monospace;font-size:.6rem;font-weight:700;
  letter-spacing:.08em;color:rgba(255,255,255,.7);
  background:rgba(5,9,18,.65);
  border:1px solid rgba(255,255,255,.12);
  padding:.18rem .5rem;border-radius:4px;
}"""

if OLD_CSS in c:
    c = c.replace(OLD_CSS, NEW_CSS)
    print('OK: CSS updated')
else:
    print('WARN: CSS block not found — checking...')
    idx = c.find('/* ===== REVIEW GRID ===== */')
    print('  REVIEW GRID found at:', idx)

# ─── 3. Logo URL helper (Google Favicon API — best source for app icons) ─────
def favicon(domain):
    return f"https://t1.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://{domain}&size=256"

def card(slug, rank, tier, name, domain, score, fill, highlight, tags, fallback, logo_domain=None):
    """logo_domain: override domain used for the favicon logo URL (default: same as domain)"""
    tier_label = {'god':'God Tier','high':'High Tier','mid':'Mid Tier'}[tier]
    logo_url = favicon(logo_domain if logo_domain else domain)
    tags_html = ''.join(
        f'<span class="rc-tag{" "+cls if cls else ""}">{text}</span>'
        for cls, text in tags
    )
    return f'''
      <a href="/review-{slug}" class="review-card {tier} dlg-fade" data-name="{name.lower()}" data-tier="{tier}">
        <div class="rc-logo-wrap">
          <span class="rc-rank">#{rank}</span>
          <div class="rc-score-badge">{score}<span>/5</span></div>
          <img class="rc-logo-img" src="{logo_url}" alt="{name} logo" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
          <div class="rc-logo-fallback" style="display:none">{fallback}</div>
          <span class="rc-badge {tier}">{tier_label}</span>
        </div>
        <div class="rc-body">
          <div class="rc-name">{name}</div>
          <div class="rc-rating-row">
            <div class="star-bar" aria-label="{score} out of 5 stars">
              <div class="star-bg">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
              <div class="star-fg" style="--fill:{fill}%">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
            </div>
            <span class="rc-score">{score}/5</span>
          </div>
          <div class="rc-highlight">&#9654; {highlight}</div>
          <div class="rc-tags">{tags_html}</div>
          <div class="rc-cta-btn">Read Full Review &#8594;</div>
        </div>
      </a>'''

# ─── 4. Casino data ──────────────────────────────────────────────────────────
GOD_TIER_HTML = card('stake-us', 1, 'god', 'Stake.us', 'stake.us', '4.7', 94,
    'Daily Free Coins — Best Value',
    [('hot','Daily Free SC'),('','Originals'),('','Fast Payout')], 'S')

GOD_TIER_HTML += card('pulsz', 2, 'god', 'Pulsz', 'pulsz.com', '4.6', 92,
    'Daily SC Bonus + US & Canada',
    [('hot','Daily SC'),('ca','US + CA'),('','Slot Focus')], 'P')

GOD_TIER_HTML += card('zula', 3, 'god', 'Zula Casino', 'zulacasino.com', '4.6', 92,
    'Daily Bonus — Wide Game Selection',
    [('hot','Daily Bonus'),('ca','US + CA'),('','Wide Selection')], 'Z')

GOD_TIER_HTML += card('chumba', 4, 'god', 'Chumba Casino', 'chumbacasino.com', '4.5', 90,
    'Pioneer Site Since 2017',
    [('hot','Free SC Daily'),('','Since 2017'),('','Cash Prizes')], 'C')

GOD_TIER_HTML += card('crown-coins', 5, 'god', 'Crown Coins', 'crowncoins.com', '4.5', 90,
    'High Daily SC — Fast Payouts',
    [('hot','Strong Bonus'),('ca','US + CA'),('','Fast Pay')], 'CC')

GOD_TIER_HTML += card('sportzino', 6, 'god', 'Sportzino', 'sportzino.com', '4.5', 90,
    'Sports Betting + Casino Slots',
    [('hot','Sports + Slots'),('ca','US + CA'),('','Daily SC')], 'Sz')

HIGH_TIER_HTML = card('mcluck', 7, 'high', 'McLuck', 'mcluck.com', '4.4', 88,
    'Great Game Library — Daily SC',
    [('hot','Daily SC'),('','Great Games'),('ca','US + CA')], 'ML')

HIGH_TIER_HTML += card('global-poker', 8, 'high', 'Global Poker', 'globalpoker.com', '4.4', 88,
    'Best Poker Platform + Daily SC',
    [('hot','Poker Focus'),('ca','US + CA'),('','Gold Coins')], 'GP')

# LuckyLand: luckylandcasino.com has the real "LC" logo vs luckylandslots.com (wrong image)
HIGH_TIER_HTML += card('luckyland', 9, 'high', 'LuckyLand Slots', 'luckylandslots.com', '4.3', 86,
    'Slots Focused — Reliable Bonuses',
    [('hot','Slot Focus'),('ca','US + CA'),('','Daily Coins')], 'LL',
    logo_domain='luckylandcasino.com')

HIGH_TIER_HTML += card('realprize', 10, 'high', 'RealPrize', 'realprize.com', '4.3', 86,
    'Growing Game Library + Daily SC',
    [('hot','Daily SC'),('','Growing Library'),('','US Only')], 'RP')

HIGH_TIER_HTML += card('fliff', 11, 'high', 'Fliff', 'getfliff.com', '4.2', 84,
    'Best Social Sportsbook + Free SC',
    [('hot','Sports Picks'),('','Free SC'),('','US Only')], 'Fl')

# Moonspin: all domains return globe — favicon will fail, fallback text "Ms" shown
HIGH_TIER_HTML += card('moonspin', 12, 'high', 'Moonspin', 'moonspin.com', '4.0', 80,
    'Daily Login Bonus — Solid Slots',
    [('','Slots'),('hot','Daily Bonus'),('','US Only')], 'Ms')

MID_TIER_HTML = card('fortune-coins', 13, 'mid', 'Fortune Coins', 'fortunecoins.com', '3.9', 78,
    'Daily Coins — Classic Slots',
    [('','Daily Bonus'),('','Slots'),('','US Only')], 'FC')

MID_TIER_HTML += card('wow-vegas', 14, 'mid', 'WOW Vegas', 'wowvegas.com', '3.8', 76,
    'Daily SC — US + Canada Eligible',
    [('','Daily SC'),('ca','US + CA'),('','Good Slots')], 'WV')

MID_TIER_HTML += card('golden-hearts', 15, 'mid', 'Golden Hearts', 'goldenheartsgames.com', '3.8', 76,
    'Charitable Niche Casino',
    [('','Niche Site'),('ca','US + CA'),('','Daily Bonus')], 'GH')

MID_TIER_HTML += card('high5', 16, 'mid', 'High 5 Casino', 'high5casino.com', '3.7', 74,
    'Classic Slot Experience',
    [('','Classic Slots'),('ca','US + CA'),('','Daily Gold')], 'H5')

MID_TIER_HTML += card('chanced', 17, 'mid', 'Chanced', 'chanced.com', '3.6', 72,
    'Sports + Slots Combo',
    [('','Daily SC'),('','Sports'),('','US Only')], 'Ch')

MID_TIER_HTML += card('hello-millions', 18, 'mid', 'Hello Millions', 'hellomillions.com', '3.6', 72,
    'Daily Coins — Canada Friendly',
    [('','Daily Coins'),('ca','US + CA'),('','Slots')], 'HM')

MID_TIER_HTML += card('modo', 19, 'mid', 'Modo Casino', 'modo.us', '3.5', 70,
    'Canada Focused Daily SC',
    [('','New Platform'),('ca','Canada Focus'),('','Daily SC')], 'Mo')

MID_TIER_HTML += card('nolimitcoins', 20, 'mid', 'NoLimitCoins', 'nolimitcoins.com', '3.5', 70,
    'Crypto Deposits Accepted',
    [('','Daily SC'),('ca','US + CA'),('','Crypto OK')], 'NLC')

# Spree Casino: spreecasino.com has the real colorful Spree app icon
MID_TIER_HTML += card('spree', 21, 'mid', 'Spree Casino', 'spree.casino', '3.5', 70,
    'Daily SC — Simple Slots',
    [('','Daily SC'),('','Slots'),('','US Only')], 'Sp',
    logo_domain='spreecasino.com')

MID_TIER_HTML += card('funrize', 22, 'mid', 'Funrize', 'funrize.com', '3.4', 68,
    'Scratch Cards + Daily Bonus',
    [('','Scratch Cards'),('','Daily Bonus'),('','US Only')], 'Fr')

MID_TIER_HTML += card('sweeptastic', 23, 'mid', 'Sweeptastic', 'sweeptastic.com', '3.4', 68,
    'US + Canada — Simple Experience',
    [('','Daily SC'),('ca','US + CA'),('','Slots')], 'St')

MID_TIER_HTML += card('tao-fortune', 24, 'mid', 'Tao Fortune', 'taofortune.com', '3.4', 68,
    'Asian-Themed Slot Selection',
    [('','Asian Theme'),('','Daily Bonus'),('','US Only')], 'TF')

# ─── 5. Replace tier section HTML blocks ─────────────────────────────────────

def replace_grid(html, tier_id, new_cards_html):
    """Replace ALL content inside .review-grid for the given tier section using nesting-aware search."""
    sec_start = html.find(f'id="sec-{tier_id}"')
    if sec_start == -1:
        return None
    grid_open = html.find('<div class="review-grid">', sec_start)
    if grid_open == -1:
        return None
    content_start = grid_open + len('<div class="review-grid">')
    # Walk forward tracking <div> depth to find the exact matching </div>
    depth = 1
    pos = content_start
    content_end = -1
    while pos < len(html):
        next_open  = html.find('<div',  pos)
        next_close = html.find('</div>', pos)
        if next_close == -1:
            return None  # malformed
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            if depth == 0:
                content_end = next_close
                break
            pos = next_close + 6
    if content_end == -1:
        return None
    return html[:content_start] + '\n' + new_cards_html + '\n\n    ' + html[content_end:]

result = replace_grid(c, 'god', GOD_TIER_HTML)
if result:
    c = result
    print('OK: God Tier cards replaced')
else:
    print('WARN: God tier grid not found')

result = replace_grid(c, 'high', HIGH_TIER_HTML)
if result:
    c = result
    print('OK: High Tier cards replaced')
else:
    print('WARN: High tier grid not found')

result = replace_grid(c, 'mid', MID_TIER_HTML)
if result:
    c = result
    print('OK: Mid Tier cards replaced')
else:
    print('WARN: Mid tier grid not found')

# ─── 6. Save ─────────────────────────────────────────────────────────────────
open(fpath, 'w', encoding='utf-8').write(c)
print('\nSaved casino-reviews.html')
