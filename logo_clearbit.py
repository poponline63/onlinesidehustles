"""
Use Clearbit Logo API + other fallbacks for stubborn casinos.
Clearbit: https://logo.clearbit.com/{domain}  (128x128 PNG)
"""
import sys, os, time, urllib.request, io, random, re
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image

OUT_DIR = 'images/logos'
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*',
}

def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.geturl()

def save(data, slug, min_px=60):
    try:
        img = Image.open(io.BytesIO(data)).convert('RGBA')
        if img.width < min_px:
            return False, f'too small ({img.width}x{img.height})'
        orig = f'{img.width}x{img.height}'
        img.thumbnail((256, 256), Image.LANCZOS)
        c = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
        c.paste(img, ((256-img.width)//2, (256-img.height)//2), img)
        out = f'{OUT_DIR}/{slug}.png'
        c.save(out, optimize=True)
        return True, f'{orig} ({os.path.getsize(out)//1024}KB)'
    except Exception as e:
        return False, str(e)

TARGETS = [
    # (slug, domain, [extra_urls_to_try])
    ('rebet',       'rebet.com',          [
        'https://cdn.prod.website-files.com/6423c4ea78f20b56e36cac55/6423c4ea78f20b56e36cac62_ReBet-Logo.png',
        'https://images.ctfassets.net/rebet/logo.png',
        'https://rebet.com/icons/icon-512x512.png',
        'https://rebet.com/icons/icon-192x192.png',
        'https://rebet.com/static/images/logo.png',
    ]),
    ('legendz',     'legendzcasino.com',  [
        'https://legendzcasino.com/wp-content/uploads/2023/12/legendz-casino-logo.png',
        'https://legendzcasino.com/wp-content/uploads/legendz-logo.png',
        'https://legendzcasino.com/wp-content/uploads/logo.png',
        'https://legendzcasino.com/favicon-512x512.png',
        'https://legendzcasino.com/icons/icon-512x512.png',
        'https://legendzcasino.com/icons/icon-192x192.png',
    ]),
    ('spinquest',   'spinquest.com',      [
        'https://spinquest.com/icons/icon-512x512.png',
        'https://spinquest.com/icons/icon-192x192.png',
        'https://spinquest.com/favicon-512.png',
        'https://spinquest.com/favicon-192.png',
        'https://spinquest.com/static/img/logo.png',
        'https://spinquest.com/public/logo.png',
    ]),
    ('moozi',       'moozi.com',          [
        'https://moozi.com/icons/icon-512x512.png',
        'https://moozi.com/icons/icon-192x192.png',
        'https://moozi.com/favicon-512.png',
        'https://moozi.com/public/logo.png',
        'https://moozi.com/static/logo.png',
    ]),
    ('scarletsands','scarletsands.com',   [
        'https://scarletsands.com/icons/icon-512x512.png',
        'https://scarletsands.com/icons/icon-192x192.png',
        'https://scarletsands.com/favicon-512.png',
        'https://scarletsands.com/static/logo.png',
    ]),
    ('luckyland',   'luckylandslots.com', [
        'https://luckylandslots.com/icons/icon-512x512.png',
        'https://luckylandslots.com/icons/icon-192x192.png',
        'https://luckylandslots.com/favicon-512.png',
        'https://luckylandslots.com/static/logo.png',
        'https://luckylandslots.com/public/logo.png',
    ]),
    ('speedsweeps', 'speedsweeps.com',    [
        'https://speedsweeps.com/icons/icon-512x512.png',
        'https://speedsweeps.com/icons/icon-192x192.png',
        'https://speedsweeps.com/favicon-512.png',
        'https://speedsweeps.com/static/logo.png',
    ]),
    ('stake',       'stake.us',           [
        'https://stake.us/icons/icon-512x512.png',
        'https://stake.us/icons/icon-192x192.png',
        'https://stake.us/favicon-512.png',
        'https://stake.us/logo.png',
    ]),
    ('realprize',   'realprize.com',      [
        'https://realprize.com/img/192/favicon.ico',
        'https://realprize.com/img/512/favicon.ico',
        'https://realprize.com/icons/icon-512x512.png',
        'https://realprize.com/icons/icon-192x192.png',
        'https://realprize.com/logo.png',
    ]),
    ('lonestar',    'lonestarcasino.com', [
        'https://lonestarcasino.com/img/192/favicon.ico',
        'https://lonestarcasino.com/img/512/favicon.ico',
        'https://lonestarcasino.com/icons/icon-512x512.png',
        'https://lonestarcasino.com/icons/icon-192x192.png',
        'https://lonestarcasino.com/logo.png',
    ]),
    ('sixty6',      'sixty6.com',         [
        'https://sixty6.com/icons/icon-512x512.png',
        'https://sixty6.com/icons/icon-192x192.png',
        'https://sixty6.com/favicon-512.png',
        'https://sixty6.com/logo.png',
        'https://sixty6.com/static/logo.png',
    ]),
    ('globalpoker', 'globalpoker.com',    [
        'https://globalpoker.com/icons/icon-512x512.png',
        'https://globalpoker.com/icons/icon-192x192.png',
        'https://play.globalpoker.com/logo512.png',
        'https://play.globalpoker.com/icons/icon-512x512.png',
        'https://cdn.globalpoker.com/assets/logo.png',
    ]),
]

results = {}

for slug, domain, extras in TARGETS:
    out_path = f'{OUT_DIR}/{slug}.png'
    existing_ok = False
    if os.path.exists(out_path):
        try:
            img = Image.open(out_path)
            if img.width >= 150:
                print(f'  SKIP  {slug} (existing {img.width}x{img.height})')
                results[slug] = True
                continue
        except:
            pass

    saved = False

    # 1. Try Clearbit first (returns 128x128 for most known brands)
    time.sleep(random.uniform(0.4, 0.9))
    try:
        data, final_url = fetch(f'https://logo.clearbit.com/{domain}')
        ok, msg = save(data, slug, min_px=60)
        if ok:
            print(f'  OK    {slug:15s} clearbit [{msg}]')
            results[slug] = True
            saved = True
    except Exception as e:
        pass

    if saved:
        continue

    # 2. Try extra URLs
    for url in extras:
        time.sleep(random.uniform(0.3, 0.7))
        try:
            data, _ = fetch(url)
            ok, msg = save(data, slug, min_px=60)
            if ok:
                print(f'  OK    {slug:15s} {url[:65]}  [{msg}]')
                results[slug] = True
                saved = True
                break
        except:
            pass

    if not saved:
        print(f'  FAIL  {slug} ({domain})')
        results[slug] = False

print(f'\nResults: {sum(results.values())}/{len(results)} succeeded')
