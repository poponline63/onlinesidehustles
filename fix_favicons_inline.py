"""Fix favicon tags in the 15 'inline-meta' files where tags aren't on separate lines."""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

repo = os.path.dirname(os.path.abspath(__file__))

SKIPPED_FILES = [
    'complete-guide-list.html',
    'credit-card-churning.html',
    'credit-cards.html',
    'daily-login-reviews.html',
    'earnings-potential.html',
    'freelancing.html',
    'guide-luckyland-vip.html',
    'guide-stake-make-money-churning.html',
    'guide-to-quacky-hours.html',
    'income-calculator.html',
    'income-reports.html',
    'matched-betting.html',
    'reward-apps.html',
    'sell-on-tiktok-automated.html',
    'success-stories.html',
]

STANDARD = (
    '<link rel="icon" type="image/gif" href="/favicon.gif">\n'
    '    <link rel="icon" href="/favicon.ico">\n'
    '    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">'
)

# Patterns to strip from content (inline regex, removes the tag + trailing space)
REMOVE_PATTERNS = [
    r'<link\s+rel=["\']icon["\']\s+type=["\']image/gif["\']\s+href=["\'][^"\']*favicon\.gif["\'][^>]*>\s*',
    r'<link\s+rel=["\']icon["\']\s+type=["\']image/png["\']\s+sizes=["\']32x32["\']\s+href=[^>]*favicon-32x32[^>]*>\s*',
    r'<link\s+rel=["\']icon["\']\s+type=["\']image/png["\']\s+sizes=["\']16x16["\']\s+href=[^>]*favicon-16x16[^>]*>\s*',
    r'<link\s+rel=["\']icon["\']\s+href=["\'][^"\']*favicon\.ico["\'][^>]*>\s*',
    r'<link\s+rel=["\']apple-touch-icon["\'][^>]*>\s*',
    r'<script\s+src=["\'][^"\']*animated-favicon\.js["\'][^>]*></script>\s*\n?',
]

updated = []
skipped = []

for fname in SKIPPED_FILES:
    fpath = os.path.join(repo, fname)
    if not os.path.exists(fpath):
        skipped.append(fname + ' [file not found]')
        continue

    content = open(fpath, encoding='utf-8', errors='ignore').read()

    # Check if already correct
    has_gif   = 'favicon.gif' in content
    has_ico   = 'favicon.ico' in content
    has_apple = 'apple-touch-icon' in content
    has_anim  = 'animated-favicon.js' in content
    has_32    = 'favicon-32x32' in content

    if has_gif and has_ico and has_apple and not has_anim and not has_32:
        skipped.append(fname + ' [already correct]')
        continue

    original = content

    # Step 1: Remove all existing favicon tags via regex
    for pat in REMOVE_PATTERNS:
        content = re.sub(pat, '', content, flags=re.IGNORECASE)

    # Step 2: Remove animated-favicon.js line (may be on its own line)
    content = re.sub(r'\n\s*<script\s+src=["\'][^"\']*animated-favicon\.js["\'][^>]*></script>', '', content, flags=re.IGNORECASE)

    # Step 3: Insert standard favicons after <meta charset="UTF-8">
    # Find the charset meta tag (inline or on its own line)
    charset_match = re.search(r'<meta\s+charset=["\'][^"\']*["\']>', content, re.IGNORECASE)
    if not charset_match:
        # Try alternate: <meta charset=UTF-8>
        charset_match = re.search(r'<meta\s+charset=[^\s>]*[^>]*>', content, re.IGNORECASE)

    if charset_match:
        insert_pos = charset_match.end()
        content = content[:insert_pos] + '\n    ' + STANDARD + content[insert_pos:]
    else:
        # Fallback: insert before </head>
        head_end = content.find('</head>')
        if head_end != -1:
            content = content[:head_end] + '    ' + STANDARD + '\n' + content[head_end:]
        else:
            skipped.append(fname + ' [no insertion point]')
            continue

    if content != original:
        open(fpath, 'w', encoding='utf-8').write(content)
        updated.append(fname)
    else:
        skipped.append(fname + ' [no change after processing]')

print(f'=== UPDATED ({len(updated)} files) ===')
for f in updated:
    print(' ✓', f)
if skipped:
    print(f'\n=== SKIPPED ({len(skipped)} files) ===')
    for f in skipped:
        print(' ?', f)
print(f'\nDone: {len(updated)} updated, {len(skipped)} skipped')
