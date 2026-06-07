"""
Download high-quality casino logos from each casino's own website.
Tries: og:image, apple-touch-icon-precomposed, apple-touch-icon,
       /apple-touch-icon.png, largest favicon.
Saves as images/logos/{slug}.png  (256×256 square, padded white/transparent)
"""
import sys, os, re, time, urllib.request, urllib.error, random, io
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    from PIL import Image
except ImportError:
    print('Install Pillow first: py -m pip install Pillow')
    sys.exit(1)

OUT_DIR = 'images/logos'
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept': 'text/html,application/xhtml+xml,*/*;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
}

CASINOS = [
    ('stake.us',           'stake'),
    ('wowvegas.com',       'wowvegas'),
    ('crowncoinscasino.com','crowncoinscasino'),
    ('realprize.com',      'realprize'),
    ('mcluck.com',         'mcluck'),
    ('chumbacasino.com',   'chumbacasino'),
    ('pulsz.com',          'pulsz'),
    ('sportzino.com',      'sportzino'),
    ('zulacasino.com',     'zulacasino'),
    ('spinsagacasino.com', 'spinsaga'),
    ('globalpoker.com',    'globalpoker'),
    ('lonestarcasino.com', 'lonestar'),
    ('scarletsands.com',   'scarletsands'),
    ('legendzcasino.com',  'legendz'),
    ('sixty6.com',         'sixty6'),
    ('rebet.com',          'rebet'),
    ('getfliff.com',       'fliff'),
    ('rubysweeps.com',     'rubysweeps'),
    ('fortunecoins.com',   'fortunecoins'),
    ('luckylandslots.com', 'luckyland'),
    ('hellomillions.com',  'hellomillions'),
    ('chanced.com',        'chanced'),
    ('spinquest.com',      'spinquest'),
    ('funrize.com',        'funrize'),
    ('moozi.com',          'moozi'),
    ('jackpota.com',       'jackpota'),
    ('dimesweeps.com',     'dimesweeps'),
    ('speedsweeps.com',    'speedsweeps'),
    ('americanluck.com',   'americanluck'),
]

def fetch_url(url, timeout=15):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def fetch_html(domain):
    for scheme in ('https://', 'http://'):
        try:
            data = fetch_url(scheme + domain)
            return data.decode('utf-8', errors='replace')
        except Exception:
            pass
    return None

def extract_image_candidates(html, domain):
    """Return list of candidate image URLs in priority order."""
    candidates = []
    base = 'https://' + domain

    # 1. og:image (best quality, usually 512x512+)
    m = re.search(r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']', html, re.I)
    if not m:
        m = re.search(r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']', html, re.I)
    if m:
        candidates.append(m.group(1))

    # 2. twitter:image
    m = re.search(r'<meta[^>]*(?:name|property)=["\']twitter:image["\'][^>]*content=["\']([^"\']+)["\']', html, re.I)
    if not m:
        m = re.search(r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*(?:name|property)=["\']twitter:image["\']', html, re.I)
    if m:
        candidates.append(m.group(1))

    # 3. apple-touch-icon (180×180 typically)
    for size in ('180x180', '152x152', '144x144', '120x120', '114x114', '76x76', ''):
        pat = rf'<link[^>]*rel=["\']apple-touch-icon[^"\']*["\'][^>]*(?:sizes=["\'][^"\']*{size}[^"\']*["\'][^>]*)?href=["\']([^"\']+)["\']'
        m = re.search(pat, html, re.I)
        if m:
            candidates.append(m.group(1))
            break

    # 4. /apple-touch-icon.png fallback
    candidates.append(base + '/apple-touch-icon.png')
    candidates.append(base + '/apple-touch-icon-precomposed.png')

    # 5. icon 192 / 512 (PWA manifest icons)
    for size in ('512', '192', '180', '96'):
        m = re.search(
            rf'<link[^>]*(?:rel=["\'](?:icon|shortcut icon)["\'][^>]*sizes=["\'][^"\']*{size}[^"\']*["\']'
            rf'|sizes=["\'][^"\']*{size}[^"\']*["\'][^>]*rel=["\']icon["\'])[^>]*href=["\']([^"\']+)["\']',
            html, re.I
        )
        if m:
            candidates.append(m.group(1))

    # 6. Regular icon / shortcut icon
    m = re.search(r'<link[^>]*rel=["\'](?:shortcut )?icon["\'][^>]*href=["\']([^"\']+)["\']', html, re.I)
    if m:
        candidates.append(m.group(1))

    # Resolve relative URLs
    resolved = []
    for c in candidates:
        c = c.strip()
        if not c:
            continue
        if c.startswith('http'):
            resolved.append(c)
        elif c.startswith('//'):
            resolved.append('https:' + c)
        elif c.startswith('/'):
            resolved.append(base + c)
        else:
            resolved.append(base + '/' + c)
    return resolved

def process_image(data, slug):
    """Open image bytes, resize to 256×256 square with padding, save as PNG."""
    try:
        img = Image.open(io.BytesIO(data)).convert('RGBA')
        # If image is tiny (favicon 16-32px) skip and try next candidate
        if img.width < 48 or img.height < 48:
            return False, f'too small ({img.width}x{img.height})'
        # Resize to square 256×256 with padding (letterbox)
        img.thumbnail((256, 256), Image.LANCZOS)
        canvas = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
        offset = ((256 - img.width) // 2, (256 - img.height) // 2)
        canvas.paste(img, offset, img if img.mode == 'RGBA' else None)
        out = f'{OUT_DIR}/{slug}.png'
        canvas.save(out, optimize=True)
        sz = os.path.getsize(out) // 1024
        return True, f'{img.width}x{img.height} → 256×256 ({sz}KB)'
    except Exception as e:
        return False, str(e)

ok, failed = [], []

for domain, slug in CASINOS:
    out_path = f'{OUT_DIR}/{slug}.png'
    if os.path.exists(out_path) and os.path.getsize(out_path) > 2000:
        print(f'  SKIP  {domain} (already exists)')
        ok.append(domain)
        continue

    time.sleep(random.uniform(0.8, 1.8))

    # 1. Fetch site HTML
    html = fetch_html(domain)
    if not html:
        print(f'  FAIL  {domain}: could not fetch HTML')
        failed.append(domain)
        continue

    # 2. Get candidate image URLs
    candidates = extract_image_candidates(html, domain)

    # 3. Try each candidate until one works
    saved = False
    for img_url in candidates[:8]:  # try up to 8 candidates
        try:
            img_data = fetch_url(img_url, timeout=12)
            success, msg = process_image(img_data, slug)
            if success:
                print(f'  OK    {domain:30s} {img_url[:60]}  [{msg}]')
                ok.append(domain)
                saved = True
                break
            else:
                pass  # try next candidate
        except Exception:
            pass

    if not saved:
        print(f'  FAIL  {domain}: no usable image found from {len(candidates)} candidates')
        failed.append(domain)

print(f'\nDone: {len(ok)} OK, {len(failed)} failed')
if failed:
    print('Failed:', failed)
print(f'Logos saved to: {OUT_DIR}/')
