"""
Try fetching site manifest files to find high-res PWA icons.
Also tries alternative HTML parsing approaches.
"""
import sys, os, re, time, urllib.request, urllib.parse, io, json, random
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image

OUT_DIR = 'images/logos'

HEADERS_BROWSER = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}
HEADERS_IMG = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
}

def fetch_bytes(url, headers=HEADERS_IMG, timeout=15):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
        final = r.geturl()
    return data, final

def save_img(data, slug, min_px=80):
    img = Image.open(io.BytesIO(data)).convert('RGBA')
    if img.width < min_px or img.height < min_px:
        return False, f'too small {img.width}x{img.height}'
    orig = f'{img.width}x{img.height}'
    img.thumbnail((256, 256), Image.LANCZOS)
    canvas = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    canvas.paste(img, ((256-img.width)//2, (256-img.height)//2), img)
    out = f'{OUT_DIR}/{slug}.png'
    canvas.save(out, optimize=True)
    return True, f'{orig} → 256x256 ({os.path.getsize(out)//1024}KB)'

def try_manifest(domain, slug, base='https://'):
    """Try to find icon URLs in manifest.json / site.webmanifest."""
    base_url = base + domain
    for mpath in ['/manifest.json', '/site.webmanifest', '/manifest.webmanifest', '/app.webmanifest']:
        try:
            time.sleep(0.4)
            data, _ = fetch_bytes(base_url + mpath, headers=HEADERS_BROWSER)
            manifest = json.loads(data.decode('utf-8', errors='replace'))
            icons = manifest.get('icons', [])
            # Sort by size desc
            def icon_size(ic):
                s = ic.get('sizes', '0x0').split('x')
                try: return int(s[0])
                except: return 0
            icons.sort(key=icon_size, reverse=True)
            for icon in icons:
                src = icon.get('src', '')
                if not src: continue
                if src.startswith('http'):
                    img_url = src
                elif src.startswith('/'):
                    img_url = base_url + src
                else:
                    img_url = base_url + '/' + src
                try:
                    time.sleep(0.3)
                    img_data, _ = fetch_bytes(img_url)
                    ok, msg = save_img(img_data, slug)
                    if ok:
                        return img_url, msg
                except:
                    continue
        except:
            continue
    return None, None

def try_html_for_icons(domain, slug):
    """Fetch HTML (mobile UA) and look for icon/og links."""
    for scheme in ('https://', 'http://'):
        try:
            time.sleep(0.6)
            data, _ = fetch_bytes(scheme + domain, headers=HEADERS_BROWSER)
            html = data.decode('utf-8', errors='replace')

            # og:image
            m = re.search(r'<meta[^>]*(?:property=["\']og:image["\'][^>]*content|content=[^>]*?(?=.*og:image))[^>]*=["\']([^"\']+)["\']', html, re.I | re.S)
            if not m:
                m = re.search(r'og:image["\'][^>]*content=["\']([^"\']+)["\']', html, re.I)
            if not m:
                m = re.search(r'content=["\']([^"\']+)["\'][^>]*og:image', html, re.I)
            if m:
                img_url = m.group(1).strip()
                if not img_url.startswith('http'):
                    img_url = scheme + domain + ('/' if not img_url.startswith('/') else '') + img_url
                try:
                    img_data, _ = fetch_bytes(img_url)
                    ok, msg = save_img(img_data, slug)
                    if ok:
                        return img_url, msg
                except:
                    pass

            # Apple touch icon
            m = re.search(r'<link[^>]*rel=["\']apple-touch-icon[^"\']*["\'][^>]*href=["\']([^"\']+)["\']', html, re.I)
            if m:
                img_url = m.group(1).strip()
                if not img_url.startswith('http'):
                    img_url = scheme + domain + ('/' if not img_url.startswith('/') else '') + img_url
                try:
                    img_data, _ = fetch_bytes(img_url)
                    ok, msg = save_img(img_data, slug, min_px=60)
                    if ok:
                        return img_url, msg
                except:
                    pass
        except:
            continue
    return None, None

TARGETS = [
    ('rebet',       'rebet.com'),
    ('legendz',     'legendzcasino.com'),
    ('spinquest',   'spinquest.com'),
    ('moozi',       'moozi.com'),
    ('scarletsands','scarletsands.com'),
    ('luckyland',   'luckylandslots.com'),
    ('speedsweeps', 'speedsweeps.com'),
    ('stake',       'stake.us'),
]

for slug, domain in TARGETS:
    out_path = f'{OUT_DIR}/{slug}.png'
    # Check if existing file is from a small source (bad quality)
    is_small = False
    if os.path.exists(out_path):
        try:
            img = Image.open(out_path)
            # If source was < 80px, it's bad quality despite being saved as 256
            sz = os.path.getsize(out_path)
            if sz < 4000:  # tiny file = upscaled small favicon
                is_small = True
            else:
                print(f'  SKIP  {slug} (existing, looks OK)')
                continue
        except:
            pass

    print(f'  Trying manifest for {domain}...')
    url, msg = try_manifest(domain, slug)
    if url:
        print(f'  OK    {slug:15s} via manifest: {url[:60]} [{msg}]')
        continue

    print(f'  Trying HTML parse for {domain}...')
    url, msg = try_html_for_icons(domain, slug)
    if url:
        print(f'  OK    {slug:15s} via HTML: {url[:60]} [{msg}]')
        continue

    print(f'  FAIL  {slug} ({domain}) — no logo found')

print('\nDone.')
print('\nFinal logo inventory:')
for f in sorted(os.listdir(OUT_DIR)):
    if f.endswith('.png'):
        path = f'{OUT_DIR}/{f}'
        try:
            img = Image.open(path)
            quality = 'GOOD' if img.width == 256 and os.path.getsize(path) > 8000 else 'small/thin'
            print(f'  {f:30s} {img.width}x{img.height}  {os.path.getsize(path)//1024}KB  {quality}')
        except:
            print(f'  {f:30s} ERROR')
