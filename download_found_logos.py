"""
Download casino logos from the URLs discovered via browser inspection.
"""
import sys, os, io, time, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image

OUT_DIR = 'images/logos'
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Referer': 'https://onlinesidehustles.info/',
}

def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()

def save(data, slug, min_px=80):
    img = Image.open(io.BytesIO(data)).convert('RGBA')
    orig = f'{img.width}x{img.height}'
    if img.width < min_px and img.height < min_px:
        return False, f'too small {orig}'
    img.thumbnail((256, 256), Image.LANCZOS)
    canvas = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    canvas.paste(img, ((256-img.width)//2, (256-img.height)//2), img)
    out = f'{OUT_DIR}/{slug}.png'
    canvas.save(out, optimize=True)
    sz = os.path.getsize(out)
    return True, f'{orig} → 256x256 ({sz//1024}KB)'

# Discovered via browser JavaScript inspection
FOUND = [
    # slug, url, force_overwrite
    ('moozi',       'https://assets.moozi.com/assets/img/logo/logo.webp',                    True),
    ('stake',       'https://stake.us/apple-touch-icon-180.png',                              True),
    ('speedsweeps', 'https://d1aar7bd6ump5y.cloudfront.net/assets/png/logo-web.png',          True),
    # SpinQuest - use their wider banner/logo asset (560x230 >> 48x48 favicon)
    ('spinquest',   'https://spinquest.com/assets/DPiQxX_g.webp',                             True),
]

# Also retry the small-icon ones found earlier using browser-confirmed paths
SMALL_RETRIES = [
    ('globalpoker', 'https://play.globalpoker.com/apple-touch-icon.png'),  # was 64x64, try again
    ('realprize',   'https://realprize.com/img/192/favicon.ico'),
    ('lonestar',    'https://lonestarcasino.com/img/192/favicon.ico'),
    ('sixty6',      'https://sixty6.com/apple-touch-icon-180x180.png'),
]

for slug, url, *opts in FOUND:
    force = opts[0] if opts else False
    out = f'{OUT_DIR}/{slug}.png'
    print(f'  Fetching {slug} from {url[:70]}...')
    time.sleep(0.5)
    try:
        data = fetch(url)
        ok, msg = save(data, slug, min_px=60)
        if ok:
            print(f'  ✓ {slug}: {msg}')
        else:
            print(f'  ✗ {slug}: {msg}')
    except Exception as e:
        print(f'  ✗ {slug}: {e}')

print()
for slug, url in SMALL_RETRIES:
    out = f'{OUT_DIR}/{slug}.png'
    existing_sz = os.path.getsize(out) if os.path.exists(out) else 0
    print(f'  Retrying {slug} (existing {existing_sz//1024}KB)...')
    time.sleep(0.5)
    try:
        data = fetch(url)
        ok, msg = save(data, slug, min_px=100)
        if ok:
            print(f'  ✓ {slug}: {msg}')
        else:
            print(f'  ✗ {slug}: {msg} — keeping existing')
    except Exception as e:
        print(f'  ✗ {slug}: {e}')

print('\n─── Final inventory ───')
for f in sorted(os.listdir(OUT_DIR)):
    if f.endswith('.png'):
        p = f'{OUT_DIR}/{f}'
        try:
            img = Image.open(p)
            sz = os.path.getsize(p)
            quality = '✓ GOOD' if sz > 8000 else '⚠ SMALL'
            print(f'  {f:30s} {img.width}x{img.height}  {sz//1024}KB  {quality}')
        except:
            print(f'  {f} ERROR')
