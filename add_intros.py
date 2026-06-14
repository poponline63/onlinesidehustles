#!/usr/bin/env python3
"""
Inject a unique, data-grounded intro paragraph into review pages that lack one,
to reduce templated/thin-content overlap for SEO.

- Reads each page's own quick-facts (parent, year, daily, welcome, min redeem,
  games) and first pro, then composes a varied intro (rotated sentence
  structures keyed off the slug) and inserts it after the "What is X?" heading.
- Re-runnable: strips any prior class="rev-intro" intro it added and rebuilds it,
  so improving the composer and re-running is safe.
- Leaves the casinos with bespoke hand-written intros (HAND) untouched.
- Safe: if a page's structure can't be parsed, it is skipped untouched.
Run: py add_intros.py
"""
import os, re, sys, glob, hashlib
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Casinos that already have bespoke hand-written intros (leave them alone)
HAND = {"stormrush","cider","mr-goodwin","jackpot-go","gleaming-slots","coinsback",
        "theboss","dexyplay","coinz","firesevens","jumbo88","playtana","vegasway",
        "pickem","big-shot-games"}

def _pick(slug, options, salt=''):
    h = int(hashlib.md5((slug + salt).encode()).hexdigest(), 16)
    return options[h % len(options)]

def clean(s):
    s = s.replace('&mdash;', ', ').replace('—', ', ').replace(' - ', ', ')
    return re.sub(r'\s+', ' ', s).strip().rstrip('.,').strip()

def tidy(s):
    s = re.sub(r'\s+', ' ', s)
    return s.replace(' ,', ',').replace(' .', '.').replace(',,', ',').strip()

def fact(html, label):
    m = re.search(r'%s</div><div class="fact-value">(.*?)</div>' % re.escape(label), html, re.S)
    return clean(m.group(1)) if m else ''

def is_low(mn):
    m = re.search(r'\$(\d+)', mn)
    return bool(m) and int(m.group(1)) <= 25

def compose(slug, name, parent, year, daily, welcome, mn, games, pro):
    if parent and year:
        opener = _pick(slug, [
            f"{name} is a sweepstakes casino from {parent}, live since {year}.",
            f"Launched in {year}, {name} is {parent}'s entry into the sweepstakes casino space.",
            f"Operated by {parent}, {name} has offered free-to-play sweepstakes gaming since {year}.",
            f"{name} has run on the sweepstakes model under {parent} since {year}.",
        ], 'o')
    else:
        opener = _pick(slug, [
            f"{name} is a free-to-play sweepstakes casino with Sweep Coins you can redeem for real prizes.",
            f"{name} runs on the standard sweepstakes model, no purchase required to play or win.",
        ], 'o')

    if welcome and daily:
        offer = _pick(slug, [
            f"New players start with {welcome}, and the login bonus is {daily}.",
            f"The signup offer is {welcome}, with {daily} on offer for logging in.",
            f"You get {welcome} to begin, plus {daily} for showing up each day.",
            f"Expect {welcome} up front and {daily} as the recurring reward.",
        ], 'f')
    elif welcome:
        offer = f"New players start with {welcome}."
    elif daily:
        offer = f"It rewards regular players with a {daily} login bonus."
    else:
        offer = "It rewards regular players with a daily login bonus."

    parts = [opener, offer]
    if mn:
        parts.append(_pick(slug, [
            f"Its {mn} minimum redemption sits on the lower, more accessible end.",
            f"A {mn} cash-out floor keeps the first redemption within reach.",
        ] if is_low(mn) else [
            f"Redemptions begin at {mn}.",
            f"The minimum to cash out is {mn}.",
        ], 'r'))
    if pro:
        p = clean(pro).lower()
        g = f"{games} games" if games else "its game library"
        parts.append(_pick(slug, [
            f"Across {g}, the main draw is {p}.",
            f"With {g} on the platform, what stands out is {p}.",
            f"It carries {g}, and its strongest point is {p}.",
        ], 't'))
    return tidy(' '.join(parts))

changed, skipped, unparsed = [], [], []
for fname in sorted(glob.glob('review-*.html')):
    slug = fname[len('review-'):-len('.html')]
    with open(fname, encoding='utf-8') as f:
        html = f.read()
    if slug in HAND:
        skipped.append(fname); continue
    # strip any intro this script previously injected, so we can rebuild it
    html = re.sub(r'\s*<p class="rev-intro">.*?</p>', '', html, flags=re.S)
    mname = re.search(r'<h2>What is (.+?)\?</h2>', html)
    if not mname:
        unparsed.append(fname); continue
    name = mname.group(1)
    parent = fact(html, 'Parent Company'); year = fact(html, 'Launch Year')
    daily = fact(html, 'Daily Bonus'); welcome = fact(html, 'Welcome Offer')
    mn = fact(html, 'Min Redemption'); games = fact(html, 'Games')
    mpro = re.search(r'<div class="pros-card">.*?<li><span class="check">&#10003;</span>(.*?)</li>', html, re.S)
    pro = clean(mpro.group(1)) if mpro else ''
    intro = compose(slug, name, parent, year, daily, welcome, mn, games, pro)
    block = f'<h2>What is {name}?</h2>\n    <p class="rev-intro">{intro}</p>'
    new = html.replace(f'<h2>What is {name}?</h2>', block, 1)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(new)
    changed.append(fname)

print(f"Injected/refreshed intros on {len(changed)} pages; skipped {len(skipped)} hand-written; could not parse {len(unparsed)}.")
if unparsed:
    print("Unparsed:", ", ".join(unparsed[:20]))
