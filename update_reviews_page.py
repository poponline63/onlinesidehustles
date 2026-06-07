#!/usr/bin/env python3
"""Update casino-reviews.html with 66 new cards and update all counts/stats."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ==========================================
# CARD GENERATOR
# ==========================================
def card(slug, name, rating, tier_cls, tier_lbl, rank, favicon_url, highlight, tags):
    fill = int(round(rating / 5 * 100))
    words = name.split()
    initials = (words[0][0] + words[1][0]).upper() if len(words) >= 2 else name[:2].upper()
    tags_html = ''.join(
        f'<span class="rc-tag{" hot" if i == 0 else ""}">{t}</span>'
        for i, t in enumerate(tags)
    )
    return (
        f'      <a href="/review-{slug}" class="review-card {tier_cls} dlg-fade"'
        f' data-name="{name.lower()}" data-tier="{tier_cls}">\n'
        f'        <div class="rc-logo-wrap">\n'
        f'          <span class="rc-rank">#{rank}</span>\n'
        f'          <div class="rc-score-badge">{rating}<span>/5</span></div>\n'
        f'          <img class="rc-logo-img" src="https://t1.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url={favicon_url}&size=256"'
        f' alt="{name} logo" loading="lazy" onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\'">\n'
        f'          <div class="rc-logo-fallback" style="display:none">{initials}</div>\n'
        f'          <span class="rc-badge {tier_cls}">{tier_lbl}</span>\n'
        f'        </div>\n'
        f'        <div class="rc-body">\n'
        f'          <div class="rc-name">{name}</div>\n'
        f'          <div class="rc-rating-row">\n'
        f'            <div class="star-bar" aria-label="{rating} out of 5 stars">\n'
        f'              <div class="star-bg">&#9733;&#9733;&#9733;&#9733;&#9733;</div>\n'
        f'              <div class="star-fg" style="--fill:{fill}%">&#9733;&#9733;&#9733;&#9733;&#9733;</div>\n'
        f'            </div>\n'
        f'            <span class="rc-score">{rating}/5</span>\n'
        f'          </div>\n'
        f'          <div class="rc-highlight">&#9654; {highlight}</div>\n'
        f'          <div class="rc-tags">{tags_html}</div>\n'
        f'          <div class="rc-cta-btn">Read Full Review &#8594;</div>\n'
        f'        </div>\n'
        f'      </a>'
    )

# ==========================================
# CASINO DATA
# ==========================================

# --- NEW GOD TIER (1 card, rank #11) ---
god_new = [
    card('dogg-house','Dogg House Casino',4.6,'god','God Tier',11,
         'https://dogghousecasino.com',
         'Death Row Records Brand — Full Sportsbook + Casino',
         ['Death Row Brand','Sportsbook','$20 Min Cash']),
]

# --- NEW HIGH TIER (18 cards, ranks #26-#43) ---
high_new = [
    card('sweepjungle','SweepJungle',4.0,'high','High Tier',26,'https://sweepjungle.com',
         '500+ Games — $20 Min Redemption',['500+ Games','Daily SC','$20 Min Cash']),
    card('casino-click','Casino.Click',4.0,'high','High Tier',27,'https://casino.click',
         '500+ Games — Clean UI & Daily SC',['500+ Games','Daily SC','$20 Min Cash']),
    card('lavish-luck','Lavish Luck',4.0,'high','High Tier',28,'https://lavishluck.com',
         '$20 Min — Strong Daily SC, 400+ Games',['$20 Min Cash','Daily SC','400+ Games']),
    card('the-money-factory','The Money Factory',4.0,'high','High Tier',29,'https://themoneyfactory.com',
         '$20 Min — 400+ Games, Solid Welcome',['$20 Min Cash','400+ Games','Daily SC']),
    card('luckybird','Luckybird',4.1,'high','High Tier',30,'https://luckybird.io',
         '500+ Games — Above-Average Daily SC',['500+ Games','$20 Min Cash','Daily SC']),
    card('rolling-riches','Rolling Riches',4.0,'high','High Tier',31,'https://rollingriches.com',
         '$20 Min — 400+ Quality Games',['$20 Min Cash','400+ Games','Daily SC']),
    card('clubs-poker','Clubs Poker',4.1,'high','High Tier',32,'https://clubs.poker',
         'Poker Focus — $20 Min, Est. 2021',['Poker + Slots','$20 Min Cash','Since 2021']),
    card('ace-com','Ace Casino',4.0,'high','High Tier',33,'https://ace.com',
         '$20 Min — Premium Brand, 400+ Games',['$20 Min Cash','400+ Games','Daily SC']),
    card('winbonanza','WinBonanza',4.1,'high','High Tier',34,'https://winbonanza.com',
         '1 SC/Day — Blazesoft 500+ Games',['1 SC/Day','500+ Games','Blazesoft']),
    card('thrillcoins','ThrillCoins',4.2,'high','High Tier',35,'https://thrillcoins.com',
         '3,050+ Games — Up to 100 SC/Day',['3,050+ Games','100 SC/Day','WW Funcrafters']),
    card('coinsback','CoinsBack',4.1,'high','High Tier',36,'https://coinsback.com',
         '50% SC Cashback — 1,400+ Games',['50% Cashback','1,400+ Games','Daily Rewards']),
    card('jackpot-daily','Jackpot Daily',4.1,'high','High Tier',37,'https://jackpotdaily.com',
         '500+ Games — $20 Min, Strong Daily SC',['500+ Games','$20 Min Cash','Daily SC']),
    card('jackpot-go','Jackpot Go',4.1,'high','High Tier',38,'https://jackpotgo.com',
         '500+ Games — Above-Average Daily SC',['500+ Games','$20 Min Cash','Daily SC']),
    card('luckyrush','LuckyRush',4.2,'high','High Tier',39,'https://luckyrush.io',
         '1x Playthrough — Best Wagering Rate',['1x Playthrough','400+ Games','Fast Pay']),
    card('fortunarush','FortunaRush',4.1,'high','High Tier',40,'https://fortunarush.com',
         '$20 Min — 450+ Games, Strong Bonus',['$20 Min Cash','450+ Games','Daily SC']),
    card('novig','Novig',4.0,'high','High Tier',41,'https://novig.com',
         '$20 Min — Sharp Sportsbook, Fast Pay',['Sportsbook','$20 Min Cash','Fast 2-3 Days']),
    card('punt','Punt Casino',4.2,'high','High Tier',42,'https://punt.com',
         '0.70 SC/Day — 500+ Games, $20 Min',['0.70 SC/Day','500+ Games','$20 Min Cash']),
    card('betr','Betr',4.1,'high','High Tier',43,'https://betr.app',
         'Sports + Casino — Mobile-First App',['Sports + Casino','Mobile-First','$20 Min Cash']),
]

# --- NEW MID TIER B-tier (36 cards, ranks #44-#79) ---
mid_b = [
    card('sweet-sweeps','Sweet Sweeps',3.7,'mid','Mid Tier',44,'https://sweetsweeps.com',
         'Referral Code Bonus — 300+ Games',['Referral Bonus','Daily SC','300+ Games']),
    card('bangcoins','BangCoins',3.6,'mid','Mid Tier',45,'https://bangcoins.com',
         'Referral Bonus — Easy Sign-Up',['Referral Bonus','Daily SC','Easy KYC']),
    card('megaspinz','MegaSpinz',3.7,'mid','Mid Tier',46,'https://megaspinz.com',
         '400+ Games — Daily SC Login',['400+ Games','Daily SC','Welcome Bonus']),
    card('lucklake','LuckLake',3.8,'mid','Mid Tier',47,'https://lucklake.com',
         'Mobile App — $20 Min, 350+ Games',['Mobile App','$20 Min Cash','Daily SC']),
    card('sweepico','Sweepico',3.8,'mid','Mid Tier',48,'https://sweepico.com',
         '$20 Min — Referral Bonus + Daily SC',['$20 Min Cash','Referral Bonus','Daily SC']),
    card('epicsweep','EpicSweep',3.8,'mid','Mid Tier',49,'https://epicsweep.us',
         'Referral Bonus — $20 Min, 350+ Games',['$20 Min Cash','Referral Bonus','Daily SC']),
    card('sixty6','Sixty6',3.7,'mid','Mid Tier',50,'https://sixty6.com',
         'Referral Program — 300+ Games',['Referral Bonus','Daily SC','300+ Games']),
    card('sweepnext','SweepNext',3.7,'mid','Mid Tier',51,'https://sweepnext.com',
         'Referral Code — Clean Platform Design',['Referral Code','Daily SC','Clean UI']),
    card('getzoot','GetZoot',3.6,'mid','Mid Tier',52,'https://getzoot.us',
         'Referral Bonus — Free Sweepstakes SC',['Referral Bonus','Free SC','Daily Login']),
    card('chipnwin','ChipNWin',3.7,'mid','Mid Tier',53,'https://chipnwin.com',
         '$20 Min — Earn Bonus via Link',['$20 Min Cash','Earn Bonus','Daily SC']),
    card('dara-casino','Dara Casino',3.7,'mid','Mid Tier',54,'https://daracasino.com',
         'Referral Sign-Up — Daily SC Rewards',['Referral Bonus','Daily SC','300+ Games']),
    card('goodvibescasino','GoodVibesCasino',3.7,'mid','Mid Tier',55,'https://goodvibescasino.com',
         'Referral Bonus — Positive Community',['Referral Bonus','Daily SC','Clean UI']),
    card('wild-world-casino','Wild World Casino',3.6,'mid','Mid Tier',56,'https://wildworldcasino.com',
         'Wild Theme — Referral Bonus + SC',['Referral Bonus','Daily SC','Wild Theme']),
    card('sorceryreels','SorceryReels',3.7,'mid','Mid Tier',57,'https://sorceryreels.com',
         'Fantasy Theme — Referral Rewards',['Fantasy Theme','Referral Bonus','Daily SC']),
    card('lucky-slots','Lucky Slots',3.7,'mid','Mid Tier',58,'https://luckyslots.us',
         'Slots Focus — Referral Bonus + Daily',['Slots Focus','Referral Bonus','Daily SC']),
    card('crashduel','CrashDuel',3.8,'mid','Mid Tier',59,'https://crashduel.com',
         'Crash Games + $20 Min Redemption',['Crash Games','$20 Min Cash','Daily SC']),
    card('peakplay','PeakPlay',3.8,'mid','Mid Tier',60,'https://peakplay.com',
         '$20 Min — RubyStone Network',['$20 Min Cash','Daily SC','RubyStone']),
    card('jefebet','Jefebet',3.7,'mid','Mid Tier',61,'https://jefebet.com',
         '300+ Games — Daily SC Rewards',['300+ Games','Daily SC','No Purchase']),
    card('luckystake','LuckyStake',3.8,'mid','Mid Tier',62,'https://luckystake.com',
         '$20 Min — Referral Link Bonus',['$20 Min Cash','Referral Bonus','Daily SC']),
    card('spinfinite','Spinfinite',3.7,'mid','Mid Tier',63,'https://spinfinite.com',
         'Slots Focus — Daily SC Login Rewards',['Slots Focus','Daily SC','300+ Games']),
    card('smiles-casino','Smiles Casino',3.7,'mid','Mid Tier',64,'https://smilescasino.com',
         'Friendly Design — Daily SC Rewards',['Daily SC','Friendly UI','300+ Games']),
    card('goldtreasurecasino','GoldTreasureCasino',3.8,'mid','Mid Tier',65,'https://goldtreasurecasino.com',
         'Gold Theme — $20 Min, Referral Bonus',['$20 Min Cash','Referral Bonus','Gold Theme']),
    card('yaycasino','YayCasino',3.8,'mid','Mid Tier',66,'https://yaycasino.fun',
         '$20 Min — Fun Platform, Daily SC',['$20 Min Cash','Daily SC','Fun Design']),
    card('dexyplay','DexyPlay',3.7,'mid','Mid Tier',67,'https://dexyplay.com',
         'Daily SC Login — 300+ Games',['Daily SC','300+ Games','No Purchase']),
    card('zumo','Zumo',3.7,'mid','Mid Tier',68,'https://zumo.us',
         'US-Focused — Daily SC Rewards',['US-Focused','Daily SC','300+ Games']),
    card('luck-party','Luck Party',3.7,'mid','Mid Tier',69,'https://luckparty.com',
         'Party Theme — Daily SC Login Bonus',['Party Theme','Daily SC','300+ Games']),
    card('diam-bet','Diam.bet',3.7,'mid','Mid Tier',70,'https://diam.bet',
         'Daily SC — Regular Bonus Events',['Daily SC','Bonus Events','300+ Games']),
    card('theboss','TheBoss.us',3.7,'mid','Mid Tier',71,'https://theboss.us',
         'Strong Branding — Daily SC Login',['Strong Brand','Daily SC','300+ Games']),
    card('acebet','Acebet.cc',3.6,'mid','Mid Tier',72,'https://acebet.cc',
         'Sports + Casino — Daily SC Rewards',['Sports + Casino','Daily SC','250+ Games']),
    card('courtside','Courtside',3.7,'mid','Mid Tier',73,'https://courtsidegames.com',
         'Sports Theme — Daily SC Rewards',['Sports Theme','Daily SC','300+ Games']),
    card('rubysweeps','RubySweeps',3.9,'mid','Mid Tier',74,'https://rubysweeps.com',
         '$20 Min — Solid Daily SC, 350+ Games',['$20 Min Cash','Daily SC','350+ Games']),
    card('taosweeps','TaoSweeps',3.7,'mid','Mid Tier',75,'https://taosweeps.com',
         'Zen Theme — Daily SC Login Rewards',['Zen Theme','Daily SC','300+ Games']),
    card('oceanking','OceanKing',3.8,'mid','Mid Tier',76,'https://oceanking.io',
         'Ocean Theme — $20 Min, Daily SC',['$20 Min Cash','Ocean Theme','Daily SC']),
    card('coin-frenzy','Coin Frenzy',3.8,'mid','Mid Tier',77,'https://coinfrenzy.com',
         '$20 Min — 350+ Games, Daily Bonus',['$20 Min Cash','Daily SC','350+ Games']),
    card('scoop','Scoop Casino',3.8,'mid','Mid Tier',78,'https://scoop.com',
         '$20 Min — Clean Modern Interface',['$20 Min Cash','Daily SC','Clean UI']),
    card('scrooge','Scrooge Casino',3.7,'mid','Mid Tier',79,'https://scrooge.casino',
         'Daily Wheel Bonus — Gift Card Option',['Daily Wheel','Gift Card','300+ Games']),
]

# --- NEW MID TIER C-tier (11 cards, ranks #80-#90) ---
mid_c = [
    card('bankrolla','Bankrolla',3.3,'mid','Mid Tier',80,'https://bankrolla.com',
         'Free-to-Play — Slots and Table Games',['Free Play','Slots + Tables','Daily SC']),
    card('zonko','Zonko',3.2,'mid','Mid Tier',81,'https://zonko.com',
         'New Platform — Free Sweepstakes Play',['Free Play','New Platform','Daily SC']),
    card('sheeshcasino','Sheeshcasino',3.3,'mid','Mid Tier',82,'https://sheeshcasino.com',
         'Referral Bonus — Free-to-Play Model',['Referral Bonus','Free Play','Daily SC']),
    card('cluck','Cluck',3.2,'mid','Mid Tier',83,'https://playoncluck.com',
         'Unique Brand — Free-to-Play Sweepstakes',['Unique Brand','Free Play','Daily SC']),
    card('nioplay','NioPlay',3.3,'mid','Mid Tier',84,'https://nioplay.net',
         'Referral Code — Free Sweepstakes Play',['Referral Code','Free Play','Daily SC']),
    card('card-crush','Card Crush',3.3,'mid','Mid Tier',85,'https://cardcrush.com',
         'Card Games Focus — Free-to-Play',['Card Games','Free Play','Daily SC']),
    card('acornfun','AcornFun',3.3,'mid','Mid Tier',86,'https://acornfun.com',
         'Casual Platform — Free Sweepstakes',['Casual Games','Free Play','Daily SC']),
    card('baba-casino','Baba Casino',3.2,'mid','Mid Tier',87,'https://babacasino.com',
         'Free-to-Play — Sweepstakes Model',['Free Play','Daily SC','No Purchase']),
    card('coin-wizard-games','Coin Wizard Games',3.3,'mid','Mid Tier',88,'https://coinwizardgames.com',
         'Wizard Theme — Free Sweepstakes Play',['Wizard Theme','Free Play','Daily SC']),
    card('winera','Winera',3.3,'mid','Mid Tier',89,'https://winera.com',
         'Legitimate Sweepstakes — Free Play',['Free Play','Daily SC','No Purchase']),
    card('vegawin','VegaWin',3.3,'mid','Mid Tier',90,'https://vegawin.com',
         'Vegas Theme — Free-to-Play Model',['Vegas Theme','Free Play','Daily SC']),
]

# ==========================================
# READ casino-reviews.html
# ==========================================
with open('casino-reviews.html', 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)

# ==========================================
# 1. META/TITLE/OG UPDATES
# ==========================================
html = html.replace(
    'Sweepstakes Casino Reviews 2026 — 60 Honest Ratings | Online Sidehustles',
    'Sweepstakes Casino Reviews 2026 — 126 Honest Ratings | Online Sidehustles'
)
html = html.replace(
    'Sweepstakes Casino Reviews 2026 — 60 Honest Ratings',
    'Sweepstakes Casino Reviews 2026 — 126 Honest Ratings'
)
html = html.replace(
    'Honest, in-depth reviews of 60 sweepstakes casinos',
    'Honest, in-depth reviews of 126 sweepstakes casinos'
)
html = html.replace(
    '60 sweepstakes casino reviews ranked',
    '126 sweepstakes casino reviews ranked'
)
html = html.replace(
    'Honest rankings of 60 sweepstakes casinos',
    'Honest rankings of 126 sweepstakes casinos'
)
# JSON-LD description
html = html.replace(
    '"description":"25 sweepstakes casino reviews ranked',
    '"description":"126 sweepstakes casino reviews ranked'
)
html = html.replace(
    '"numberOfItems":24',
    '"numberOfItems":126'
)

# ==========================================
# 2. HERO STATS
# ==========================================
html = html.replace(
    '        <div class="hero-stat-val">60</div>',
    '        <div class="hero-stat-val">126</div>'
)
html = html.replace(
    '        <div class="hero-stat-val">10</div>',
    '        <div class="hero-stat-val">11</div>'
)
# Hero sub text
html = html.replace(
    'Honest reviews of 48 sweepstakes casinos',
    'Honest reviews of 126 sweepstakes casinos'
)

# ==========================================
# 3. FILTER TABS
# ==========================================
html = html.replace('>All (60)<', '>All (126)<')
html = html.replace('>&#127775; God Tier (10)<', '>&#127775; God Tier (11)<')
html = html.replace('>&#128293; High Tier (19)<', '>&#128293; High Tier (37)<')
html = html.replace('>&#128201; Mid Tier (31)<', '>&#128201; Mid Tier (78)<')

# ==========================================
# 4. TIER HEADER COUNTS
# ==========================================
# God: replace within sec-god context
html = html.replace(
    'id="sec-god">\n    <div class="tier-header dlg-fade">\n      <span class="tier-pill god">&#127775; God Tier</span>\n      <span class="tier-count">4.5+ Stars</span>\n      <div class="tier-line"></div>\n      <span class="tier-count">10 casinos</span>',
    'id="sec-god">\n    <div class="tier-header dlg-fade">\n      <span class="tier-pill god">&#127775; God Tier</span>\n      <span class="tier-count">4.5+ Stars</span>\n      <div class="tier-line"></div>\n      <span class="tier-count">11 casinos</span>'
)
# High: replace within sec-high context
html = html.replace(
    'id="sec-high">\n    <div class="tier-header dlg-fade">\n      <span class="tier-pill high">&#128293; High Tier</span>\n      <span class="tier-count">4.0 &#8211; 4.4 Stars</span>\n      <div class="tier-line"></div>\n      <span class="tier-count">19 casinos</span>',
    'id="sec-high">\n    <div class="tier-header dlg-fade">\n      <span class="tier-pill high">&#128293; High Tier</span>\n      <span class="tier-count">4.0 &#8211; 4.4 Stars</span>\n      <div class="tier-line"></div>\n      <span class="tier-count">37 casinos</span>'
)
# Fallback for high tier (in case the dash encoding differs)
html = html.replace(
    '<span class="tier-count">19 casinos</span>',
    '<span class="tier-count">37 casinos</span>'
)
# Mid
html = html.replace(
    '<span class="tier-count">31 casinos</span>',
    '<span class="tier-count">78 casinos</span>'
)

# ==========================================
# 5. INSERT GOD TIER CARDS
# ==========================================
god_html = '\n\n'.join(god_new)
anchor_god = '    </div>\n  </div>\n\n  <!-- ===== HIGH TIER ===== -->'
count = html.count(anchor_god)
print(f'God tier anchor count: {count}')
if count == 1:
    html = html.replace(
        anchor_god,
        f'\n{god_html}\n\n    </div>\n  </div>\n\n  <!-- ===== HIGH TIER ===== -->'
    )
    print('God tier card inserted.')
else:
    print(f'ERROR: god anchor found {count} times!')

# ==========================================
# 6. INSERT HIGH TIER CARDS
# ==========================================
high_html = '\n\n'.join(high_new)
anchor_high = '    </div>\n  </div>\n\n  <!-- ===== MID TIER ===== -->'
count = html.count(anchor_high)
print(f'High tier anchor count: {count}')
if count == 1:
    html = html.replace(
        anchor_high,
        f'\n{high_html}\n\n    </div>\n  </div>\n\n  <!-- ===== MID TIER ===== -->'
    )
    print('High tier cards inserted.')
else:
    print(f'ERROR: high anchor found {count} times!')

# ==========================================
# 7. INSERT MID TIER CARDS
# ==========================================
mid_html = '\n\n'.join(mid_b + mid_c)
anchor_mid = '\n\n    </div>\n  </div>\n\n</div><!-- /page -->'
count = html.count(anchor_mid)
print(f'Mid tier anchor count: {count}')
if count == 1:
    html = html.replace(
        anchor_mid,
        f'\n\n{mid_html}\n\n    </div>\n  </div>\n\n</div><!-- /page -->'
    )
    print('Mid tier cards inserted.')
else:
    print(f'ERROR: mid anchor found {count} times!')

# ==========================================
# WRITE casino-reviews.html
# ==========================================
with open('casino-reviews.html', 'w', encoding='utf-8') as f:
    f.write(html)

new_len = len(html)
print(f'\ncasino-reviews.html: {original_len:,} → {new_len:,} bytes (+{new_len-original_len:,})')
print('casino-reviews.html updated!')

# ==========================================
# UPDATE sweepstakes-casino-list.html DATE
# ==========================================
with open('sweepstakes-casino-list.html', 'r', encoding='utf-8') as f:
    csl = f.read()

csl_new = csl.replace('Last updated: Jun 4, 2026', 'Last updated: Jun 6, 2026')
if csl_new != csl:
    with open('sweepstakes-casino-list.html', 'w', encoding='utf-8') as f:
        f.write(csl_new)
    print('sweepstakes-casino-list.html: date updated to Jun 6, 2026')
else:
    print('WARNING: "Jun 4, 2026" not found in sweepstakes-casino-list.html')

# ==========================================
# UPDATE sitemap dates to 2026-06-06
# ==========================================
for fname in ['sitemap-pages.xml']:
    if os.path.exists(fname):
        with open(fname, 'r', encoding='utf-8') as f:
            s = f.read()
        # Update lastmod for casino-reviews
        import re
        # Update any 2026-06-04 or 2026-06-05 dates to 2026-06-06
        s2 = re.sub(r'<lastmod>2026-06-(0[1-5])</lastmod>', '<lastmod>2026-06-06</lastmod>', s)
        if s2 != s:
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(s2)
            print(f'{fname}: dates updated to 2026-06-06')
        else:
            print(f'{fname}: no date updates needed')

print('\nAll done!')
