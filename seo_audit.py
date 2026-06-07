"""
Full SEO audit of all 50 state pages.
"""
import sys, re, glob
sys.stdout.reconfigure(encoding='utf-8')

pages = sorted(glob.glob('casinos-in-*.html'))
print('FULL SEO AUDIT - all 50 state pages\n')
print(f'{"Page":<35} {"Title":<10} {"Desc":<10} {"FAQs":<6} {"FAQSchema":<11} {"Breadcrumb":<12} {"Words":<8} {"Issues"}')
print('-'*115)

missing_faqschema = []
missing_breadcrumb = []
short_desc = []
long_title = []
low_words = []
no_internal_links = []

for pg in pages:
    with open(pg, encoding='utf-8') as f:
        html = f.read()

    state = pg.replace('casinos-in-','').replace('.html','')
    title_m = re.search(r'<title>(.*?)</title>', html)
    desc_m  = re.search(r'<meta name="description" content="([^"]+)"', html)
    faq_q   = len(re.findall(r'class="faq-question"', html))
    has_faq_schema  = 'FAQPage' in html
    has_breadcrumb  = 'BreadcrumbList' in html
    word_count = len(re.findall(r'\b\w+\b', re.sub(r'<[^>]+>', ' ', html)))
    # Count internal links (href="/casinos-in- or href="/best- or href="/guide)
    internal_links = len(re.findall(r'href="/(casinos-in|best-|guide|sweepstakes)', html))

    title_len = len(title_m.group(1)) if title_m else 0
    desc_len  = len(desc_m.group(1))  if desc_m  else 0

    flags = []
    if not has_faq_schema:    flags.append('NO FAQPage schema')
    if not has_breadcrumb:    flags.append('NO BreadcrumbList')
    if desc_len < 140:        flags.append(f'short desc ({desc_len}c)')
    if title_len > 70:        flags.append(f'long title ({title_len}c)')
    if word_count < 3000:     flags.append(f'low words ({word_count})')
    if internal_links < 3:    flags.append(f'few internal links ({internal_links})')

    flag_str = ' | '.join(flags) if flags else 'OK'

    print(f'{state:<35} {title_len:<10} {desc_len:<10} {faq_q:<6} {str(has_faq_schema):<11} {str(has_breadcrumb):<12} {word_count:<8} {flag_str}')

    if not has_faq_schema:    missing_faqschema.append(state)
    if not has_breadcrumb:    missing_breadcrumb.append(state)
    if desc_len < 140:        short_desc.append(state)
    if title_len > 70:        long_title.append(state)
    if word_count < 3000:     low_words.append(state)

print()
print('=== SUMMARY ===')
print(f'Missing FAQPage schema:   {len(missing_faqschema)}/50')
print(f'Missing BreadcrumbList:   {len(missing_breadcrumb)}/50')
print(f'Short meta desc (<140c):  {len(short_desc)}/50')
print(f'Title too long (>70c):    {len(long_title)}/50')
print(f'Low word count (<3000):   {len(low_words)}/50')
if long_title:
    print(f'\nLong title pages: {long_title}')
if short_desc:
    print(f'\nShort desc pages: {short_desc}')
if low_words:
    print(f'\nLow word count pages: {low_words}')
