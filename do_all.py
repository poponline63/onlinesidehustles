import os, sys, shutil, re
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ══════════════════════════════════════════════════════════════════
# 1.  COMPRESS logo.png  (328KB → target ~12KB)
# ══════════════════════════════════════════════════════════════════
print('=== 1. Compressing logo.png ===')
from PIL import Image

img = Image.open('logo.png').convert('RGBA')
print(f'  Original: {img.size}  {os.path.getsize("logo.png")//1024}KB')

# Resize to 256×256 — still 11× larger than the 22px nav display
img_resized = img.resize((256, 256), Image.LANCZOS)

# Save back as optimised PNG
img_resized.save('logo.png', optimize=True, compress_level=9)
print(f'  Saved:    256×256  {os.path.getsize("logo.png")//1024}KB')

# Remove the identical duplicate
if os.path.exists('logo-transparent.png'):
    os.remove('logo-transparent.png')
    print('  Removed logo-transparent.png (was identical duplicate)')


# ══════════════════════════════════════════════════════════════════
# 2.  DELETE ORPHANED IMAGES
# ══════════════════════════════════════════════════════════════════
print('\n=== 2. Deleting orphaned images ===')
orphans = [
    '2026-03-24-osh-logo-v1.png',
    '2026-03-24-osh-logo-v2.png',
    '2026-03-24-osh-logo-v3.png',
    'logo-original.png',
    'ufo-money.png',
    'dropship-calendar-portal.png',
]
freed = 0
for f in orphans:
    if os.path.exists(f):
        sz = os.path.getsize(f)
        os.remove(f)
        freed += sz
        print(f'  Deleted {f}  ({sz//1024}KB)')
print(f'  Total freed: {freed//1024}KB')


# ══════════════════════════════════════════════════════════════════
# 3.  ADD comparisons/ PAGES TO sitemap-pages.xml
# ══════════════════════════════════════════════════════════════════
print('\n=== 3. Updating sitemap-pages.xml ===')
sm = open('sitemap-pages.xml', encoding='utf-8').read()

new_entries = ''
for slug in ['best-welcome-packages', 'chumba-vs-stake', 'fastest-payout-sites']:
    full_url = f'https://onlinesidehustles.info/comparisons/{slug}'
    if full_url not in sm:
        new_entries += (
            f'  <url>\n'
            f'  <loc>{full_url}</loc>\n'
            f'  <lastmod>2026-06-06</lastmod>\n'
            f'  <changefreq>monthly</changefreq>\n'
            f'  <priority>0.7</priority>\n'
            f'</url>\n'
        )
        print(f'  Added: {slug}')

if new_entries:
    sm = sm.replace('</urlset>', new_entries + '</urlset>')
    open('sitemap-pages.xml', 'w', encoding='utf-8').write(sm)
else:
    print('  Already present')


print('\nAll quick fixes done.')
