"""
Retry failed and poor-quality logos with alternative sources.
"""
import sys, os, re, time, urllib.request, io, random
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image

OUT_DIR = 'images/logos'
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
}

def fetch(url, timeout=18):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def save_img(data, slug, min_size=64):
    img = Image.open(io.BytesIO(data)).convert('RGBA')
    if img.width < min_size or img.height < min_size:
        return False, f'too small ({img.width}x{img.height})'
    orig = f'{img.width}x{img.height}'
    img.thumbnail((256, 256), Image.LANCZOS)
    canvas = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    off = ((256 - img.width)//2, (256 - img.height)//2)
    canvas.paste(img, off, img)
    out = f'{OUT_DIR}/{slug}.png'
    canvas.save(out, optimize=True)
    return True, f'{orig} -> 256x256 ({os.path.getsize(out)//1024}KB)'

def try_urls(slug, urls, min_size=80, force=False):
    out = f'{OUT_DIR}/{slug}.png'
    if not force and os.path.exists(out) and os.path.getsize(out) > 3000:
        # Check if existing image is good quality
        try:
            img = Image.open(out)
            if img.width >= 200:
                print(f'  SKIP  {slug} (existing {img.width}x{img.height})')
                return True
        except:
            pass
    for url in urls:
        try:
            time.sleep(random.uniform(0.5, 1.2))
            data = fetch(url)
            ok, msg = save_img(data, slug, min_size)
            if ok:
                print(f'  OK    {slug:20s} {url[:70]}  [{msg}]')
                return True
        except Exception as e:
            pass
    print(f'  FAIL  {slug}: all {len(urls)} URLs failed')
    return False

# ── Targeted fixes for failed/poor-quality casinos ─────────────────────────

# ReBet - their main domain is rebet.com, app at getrebet.com
try_urls('rebet', [
    'https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/4b/6c/65/4b6c65a3-f6f5-4ea6-d7d4-8e71d1e4a97c/AppIcon-0-0-1x_U007ephone-0-0-85-220.png/1200x630wa.png',
    'https://play-lh.googleusercontent.com/BFb7lSSzBXBLGCT36X7dJxYLs7KvJP5hD0Ck9C4YLrqcE45IVQPMC3J3-gqy3QFB=w2560-h1440-rw',
    'https://rebet.com/logo.png',
    'https://rebet.com/favicon.png',
    'https://rebet.com/img/logo.png',
    'https://www.rebet.com/logo.png',
    'https://static.rebet.com/logo.png',
    'https://cdn.rebet.com/logo.png',
], min_size=80, force=True)

# Legendz Casino
try_urls('legendz', [
    'https://legendzcasino.com/wp-content/uploads/2024/01/legendz-logo.png',
    'https://legendzcasino.com/wp-content/themes/legendz/assets/img/logo.png',
    'https://legendzcasino.com/images/logo.png',
    'https://legendzcasino.com/img/logo.png',
    'https://legendzcasino.com/assets/logo.png',
    'https://play-lh.googleusercontent.com/FN4FpRrWU3hXnlFLxjAyqyiVFrEIJLf5g31S3VfQ1X9Iz4dT-tSP4pQD8U3N-mLc=w2560-h1440-rw',
    'https://affiliates.routy.app/route/91174?affId=3353',
], min_size=80, force=True)

# SpinQuest - favicon was only 48x48
try_urls('spinquest', [
    'https://spinquest.com/images/logo.png',
    'https://spinquest.com/img/logo.png',
    'https://spinquest.com/assets/logo.png',
    'https://spinquest.com/apple-touch-icon.png',
    'https://spinquest.com/apple-touch-icon-180x180.png',
    'https://spinquest.com/logo192.png',
    'https://spinquest.com/logo512.png',
    'https://spinquest.com/static/media/logo.png',
], min_size=80, force=True)

# Chanced - couldn't fetch HTML
try_urls('chanced', [
    'https://chanced.com/img/logo.png',
    'https://chanced.com/images/logo.png',
    'https://chanced.com/assets/logo.png',
    'https://chanced.com/apple-touch-icon.png',
    'https://chanced.com/logo192.png',
    'https://chanced.com/logo512.png',
    'https://chanced.com/static/images/chanced-og.png',
    'https://chanced.com/uploads/og-image.png',
], min_size=80, force=True)

# Moozi
try_urls('moozi', [
    'https://moozi.com/images/logo.png',
    'https://moozi.com/img/logo.png',
    'https://moozi.com/logo.png',
    'https://moozi.com/assets/logo.png',
    'https://moozi.com/apple-touch-icon.png',
    'https://moozi.com/logo192.png',
    'https://moozi.com/logo512.png',
], min_size=80, force=True)

# Scarlet Sands
try_urls('scarletsands', [
    'https://scarletsands.com/images/logo.png',
    'https://scarletsands.com/img/logo.png',
    'https://scarletsands.com/logo.png',
    'https://scarletsands.com/apple-touch-icon.png',
    'https://scarletsands.com/logo192.png',
    'https://scarletsands.com/logo512.png',
    'https://scarletsands.com/assets/images/logo.png',
], min_size=80, force=True)

# LuckyLand Slots
try_urls('luckyland', [
    'https://luckylandslots.com/apple-touch-icon.png',
    'https://luckylandslots.com/apple-touch-icon-180x180.png',
    'https://luckylandslots.com/logo512.png',
    'https://luckylandslots.com/logo192.png',
    'https://luckylandslots.com/img/logo.png',
    'https://luckylandslots.com/images/logo.png',
    'https://luckylandslots.com/favicon-512x512.png',
], min_size=80, force=True)

# SpeedSweeps
try_urls('speedsweeps', [
    'https://speedsweeps.com/apple-touch-icon.png',
    'https://speedsweeps.com/logo192.png',
    'https://speedsweeps.com/logo512.png',
    'https://speedsweeps.com/img/logo.png',
    'https://speedsweeps.com/images/logo.png',
    'https://speedsweeps.com/assets/logo.png',
], min_size=80, force=True)

# Stake.us - Cloudflare blocked, try CDN paths
try_urls('stake', [
    'https://stake.us/apple-touch-icon.png',
    'https://stake.us/logo192.png',
    'https://stake.us/logo512.png',
    'https://stake.us/img/logo.png',
    'https://s.stake.com/stake-og.png',
    'https://cdn.stake.us/logo.png',
], min_size=80, force=True)

# Chumba - Cloudflare blocked
try_urls('chumbacasino', [
    'https://chumbacasino.com/apple-touch-icon.png',
    'https://chumbacasino.com/logo192.png',
    'https://chumbacasino.com/logo512.png',
    'https://cdn.chumbacasino.com/logo.png',
    'https://www.chumbacasino.com/media/images/logo.png',
], min_size=80, force=True)

# Fix small-icon ones (< 100px source) — try alternative URLs
# RealPrize (was 48x48)
try_urls('realprize', [
    'https://realprize.com/img/270/favicon.ico',
    'https://realprize.com/logo192.png',
    'https://realprize.com/logo512.png',
    'https://realprize.com/apple-touch-icon.png',
    'https://realprize.com/images/logo.png',
    'https://realprize.com/img/logo.png',
], min_size=100, force=True)

# Lonestar (was 48x48)
try_urls('lonestar', [
    'https://lonestarcasino.com/img/270/favicon.ico',
    'https://lonestarcasino.com/logo192.png',
    'https://lonestarcasino.com/logo512.png',
    'https://lonestarcasino.com/apple-touch-icon.png',
    'https://lonestarcasino.com/images/logo.png',
    'https://lonestarcasino.com/img/logo.png',
], min_size=100, force=True)

# Sixty6 (was 48x48)
try_urls('sixty6', [
    'https://sixty6.com/logo192.png',
    'https://sixty6.com/logo512.png',
    'https://sixty6.com/apple-touch-icon.png',
    'https://sixty6.com/apple-touch-icon-180x180.png',
    'https://sixty6.com/images/logo.png',
    'https://sixty6.com/img/logo.png',
], min_size=100, force=True)

# Fortune Coins (was 80x80)
try_urls('fortunecoins', [
    'https://fortunecoins.com/logo192.png',
    'https://fortunecoins.com/logo512.png',
    'https://fortunecoins.com/apple-touch-icon.png',
    'https://fortunecoins.com/apple-touch-icon-180x180.png',
    'https://fortunecoins.com/images/logo.png',
    'https://fortunecoins.com/img/logo.png',
], min_size=100, force=True)

# Global Poker (was 64x64)
try_urls('globalpoker', [
    'https://globalpoker.com/logo192.png',
    'https://globalpoker.com/logo512.png',
    'https://play.globalpoker.com/apple-touch-icon.png',
    'https://globalpoker.com/apple-touch-icon-180x180.png',
    'https://globalpoker.com/images/logo.png',
    'https://globalpoker.com/img/logo.png',
    'https://cdn.globalpoker.com/logo.png',
], min_size=100, force=True)

print('\nDone.')
