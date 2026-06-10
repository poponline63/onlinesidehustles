"""Generate sitemap-pages.xml, sitemap-reviews.xml, sitemap-blog.xml and sitemap.xml.

URLs come from each page's canonical tag so the sitemap never disagrees with
on-page signals. Pages are skipped when they are noindexed, have no canonical,
or canonicalize to another page (redirect stubs dedupe away automatically).
Run from the repo root: python scripts/generate_sitemaps.py
"""
import datetime
import glob
import re

SITE = "https://onlinesidehustles.info"
TODAY = datetime.date.today().isoformat()

EXCLUDE_PATTERNS = ("404", "example", "-old", "test", "mockup")


def head_of(path):
    text = open(path, encoding="utf-8", errors="ignore").read()
    cut = text.find("</head>")
    return text[:cut] if cut != -1 else text[:8000]


def canonical_of(head):
    m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', head, re.I)
    return m.group(1).strip() if m else None


def is_noindex(head):
    return bool(re.search(r"<meta[^>]+noindex", head, re.I))


def url_entry(loc, freq, priority):
    return (
        "  <url>\n"
        f"    <loc>{loc}</loc>\n"
        f"    <lastmod>{TODAY}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>"
    )


def write_sitemap(filename, entries):
    body = "\n".join(
        ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
         *entries,
         "</urlset>", ""])
    open(filename, "w", encoding="utf-8", newline="\n").write(body)
    print(f"{filename}: {len(entries)} URLs")


def collect(files, freq, priority):
    seen, entries = set(), []
    for f in sorted(files):
        name = f.replace("\\", "/")
        if any(p in name for p in EXCLUDE_PATTERNS):
            continue
        head = head_of(f)
        if is_noindex(head):
            continue
        canon = canonical_of(head)
        if not canon or not canon.startswith(SITE):
            continue
        if canon in seen:
            continue
        seen.add(canon)
        entries.append(url_entry(canon, freq, priority))
    return seen, entries


# Pages: root html files, reviews excluded (they get their own sitemap)
page_files = [f for f in glob.glob("*.html") if not f.startswith("review-")]
page_seen, page_entries = collect(page_files, "monthly", "0.8")
home = url_entry(f"{SITE}/", "weekly", "1.0")
page_entries = [home] + [e for e in page_entries if f"<loc>{SITE}/</loc>" not in e]
write_sitemap("sitemap-pages.xml", page_entries)

# Reviews
_, review_entries = collect(glob.glob("review-*.html"), "monthly", "0.85")
write_sitemap("sitemap-reviews.xml", review_entries)

# Blog: clean /blog/<slug> URLs (canonical preferred, slug fallback)
blog_seen, blog_entries = set(), []
for f in sorted(glob.glob("blog/*.html")):
    head = head_of(f)
    if is_noindex(head):
        continue
    canon = canonical_of(head)
    slug = f.replace("\\", "/").removesuffix(".html")
    loc = canon if canon and canon.startswith(SITE) else f"{SITE}/{slug}"
    if loc in blog_seen:
        continue
    blog_seen.add(loc)
    blog_entries.append(url_entry(loc, "monthly", "0.75"))
blog_index = url_entry(f"{SITE}/blog", "daily", "0.8")
blog_entries = [blog_index] + [e for e in blog_entries if f"<loc>{SITE}/blog</loc>" not in e]
write_sitemap("sitemap-blog.xml", blog_entries)

# Index
index = "\n".join(
    ['<?xml version="1.0" encoding="UTF-8"?>',
     '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
     *[f"  <sitemap>\n    <loc>{SITE}/{n}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </sitemap>"
       for n in ("sitemap-pages.xml", "sitemap-reviews.xml", "sitemap-blog.xml")],
     "</sitemapindex>", ""])
open("sitemap.xml", "w", encoding="utf-8", newline="\n").write(index)
print("sitemap.xml index written")
