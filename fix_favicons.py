import sys, os, glob
sys.stdout.reconfigure(encoding='utf-8')

repo = os.path.dirname(os.path.abspath(__file__))

# ── Target standard (from casino-reviews.html) ────────────────────────────────
FAVICON_LINES = [
    '<link rel="icon" type="image/gif" href="/favicon.gif">',
    '<link rel="icon" href="/favicon.ico">',
    '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">',
]

# Skip these files
SKIP_FILES = {'index.html', 'index2.html', 'reviews-hub.html'}

# ── Process a single file's content ──────────────────────────────────────────
def process_file(content):
    lines = content.split('\n')
    result_lines = []
    insertion_point = -1
    indent = '    '

    for line in lines:
        stripped = line.strip()

        # Remove lines that are favicon <link> tags or animated-favicon.js script
        is_favicon_link = (
            stripped.startswith('<link') and (
                'rel="icon"' in stripped or
                "rel='icon'" in stripped or
                'rel="apple-touch-icon"' in stripped or
                "rel='apple-touch-icon'" in stripped
            )
        )
        is_anim_script = 'animated-favicon.js' in stripped and '<script' in stripped

        if is_favicon_link or is_anim_script:
            continue  # drop this line

        result_lines.append(line)

        # Mark insertion point: right after <meta charset line
        if insertion_point == -1 and stripped.lower().startswith('<meta') and 'charset' in stripped.lower():
            insertion_point = len(result_lines)
            indent = ''
            for ch in line:
                if ch in ' \t':
                    indent += ch
                else:
                    break

    # Fallback: insert after <meta name="viewport"> if charset not found
    if insertion_point == -1:
        for i, line in enumerate(result_lines):
            stripped = line.strip()
            if stripped.lower().startswith('<meta') and 'viewport' in stripped.lower():
                insertion_point = i + 1
                indent = ''
                for ch in line:
                    if ch in ' \t':
                        indent += ch
                    else:
                        break
                break

    if insertion_point == -1:
        return None  # can't determine insertion point

    # Insert the standard 3 favicon lines
    favicon_block = [indent + fl for fl in FAVICON_LINES]
    result_lines = result_lines[:insertion_point] + favicon_block + result_lines[insertion_point:]
    return '\n'.join(result_lines)

# ── Gather all HTML files ─────────────────────────────────────────────────────
all_html = (
    glob.glob(os.path.join(repo, '*.html')) +
    glob.glob(os.path.join(repo, 'blog', '*.html')) +
    glob.glob(os.path.join(repo, 'comparisons', '*.html')) +
    glob.glob(os.path.join(repo, 'reports', '*.html'))
)

updated      = []
already_ok   = []
skipped      = []

for fpath in sorted(all_html):
    fname = os.path.relpath(fpath, repo).replace('\\', '/')

    if os.path.basename(fpath) in SKIP_FILES:
        skipped.append(fname + ' [skip list]')
        continue

    content = open(fpath, encoding='utf-8', errors='ignore').read()

    # Skip pages with no <head> (redirect stubs etc)
    if '<head' not in content:
        skipped.append(fname + ' [no <head>]')
        continue

    # Check current favicon state
    has_gif     = '<link rel="icon" type="image/gif" href="/favicon.gif">' in content
    has_ico     = '<link rel="icon" href="/favicon.ico">'                   in content
    has_apple   = '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">' in content
    has_animated = 'animated-favicon.js' in content
    has_32      = 'favicon-32x32' in content

    # Already exactly right — nothing to do
    if has_gif and has_ico and has_apple and not has_animated and not has_32:
        already_ok.append(fname)
        continue

    new_content = process_file(content)

    if new_content is None:
        skipped.append(fname + ' [no insertion point found]')
        continue

    if new_content != content:
        open(fpath, 'w', encoding='utf-8').write(new_content)
        updated.append(fname)
    else:
        skipped.append(fname + ' [no change after processing — check manually]')

# ── Report ────────────────────────────────────────────────────────────────────
print(f'=== UPDATED ({len(updated)} files) ===')
for f in updated:
    print(' ✓', f)

print(f'\n=== ALREADY CORRECT ({len(already_ok)} files) ===')
for f in already_ok[:15]:
    print(' –', f)
if len(already_ok) > 15:
    print(f'   ...and {len(already_ok)-15} more')

if skipped:
    print(f'\n=== SKIPPED ({len(skipped)} files) ===')
    for f in skipped:
        print(' ?', f)

print(f'\nDone: {len(updated)} updated | {len(already_ok)} already correct | {len(skipped)} skipped')
