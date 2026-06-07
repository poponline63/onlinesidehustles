import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

# ── 1. Pages still missing RSA design ──────────────────────────────
old_pages = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git']]
    for f in files:
        if not f.endswith('.html'):
            continue
        full = os.path.join(root, f)
        c = open(full, encoding='utf-8', errors='ignore').read()
        if 'IBM Plex Mono' not in c and len(c) > 3000:
            rel = full.replace('.\\', '').replace('./', '')
            old_pages.append((rel, len(c)//1000))

old_pages.sort(key=lambda x: -x[1])
print(f'\n=== {len(old_pages)} pages WITHOUT RSA design ===')
for p, kb in old_pages[:25]:
    print(f'  {kb:4d}KB  {p}')

# ── 2. Large images still uncompressed ─────────────────────────────
big_imgs = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'node_modules']]
    for f in files:
        if not f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            continue
        full = os.path.join(root, f)
        sz = os.path.getsize(full)
        if sz > 200_000:
            rel = full.replace('.\\', '').replace('./', '')
            big_imgs.append((rel, sz // 1024))

big_imgs.sort(key=lambda x: -x[1])
print(f'\n=== {len(big_imgs)} images > 200KB ===')
for p, kb in big_imgs[:20]:
    print(f'  {kb:5d}KB  {p}')

# ── 3. New blog posts not in sitemap ───────────────────────────────
sm = open('sitemap-blog.xml', encoding='utf-8', errors='ignore').read() if os.path.exists('sitemap-blog.xml') else ''
sm2 = open('sitemap.xml', encoding='utf-8', errors='ignore').read() if os.path.exists('sitemap.xml') else ''
blog_files = [f.replace('.html', '') for f in os.listdir('blog') if f.endswith('.html')]
missing_sm = [f for f in blog_files if f not in sm and f not in sm2]
print(f'\n=== {len(missing_sm)} blog posts potentially missing from sitemaps ===')
for f in sorted(missing_sm)[:20]:
    print(f'  {f}')

# ── 4. Pages with broken/placeholder meta descriptions ─────────────
thin_meta = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git']]
    for f in files:
        if not f.endswith('.html'): continue
        full = os.path.join(root, f)
        c = open(full, encoding='utf-8', errors='ignore').read()
        m = re.search(r'<meta name="description" content="([^"]{0,40})"', c)
        if m and len(m.group(1)) < 40 and 'IBM Plex Mono' in c:
            rel = full.replace('.\\', '').replace('./', '')
            thin_meta.append((rel, m.group(1)))

print(f'\n=== {len(thin_meta)} styled pages with thin meta descriptions ===')
for p, desc in thin_meta[:15]:
    print(f'  "{desc}"  →  {p}')
