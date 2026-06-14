#!/usr/bin/env python3
"""
Add Nate Sterling as the named human reviewer to every review-*.html page.
Idempotent: only rewrites pages that still credit "Online Sidehustles" so it
is safe to re-run. New pages from generate_reviews.py already ship with the
Nate byline, so they are skipped automatically.
Run: py add_author_byline.py
"""
import os, glob, sys
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

REPLACEMENTS = [
    # Visible byline under the H1
    ('&nbsp;|&nbsp; Reviewed by Online Sidehustles</p>',
     '&nbsp;|&nbsp; Reviewed by <a href="/author/nate-sterling" style="color:var(--teal);text-decoration:none;">Nate Sterling</a>, Sweepstakes Casino Writer</p>'),
    # Review schema author: Organization -> Person
    ('"author":{"@type":"Organization","name":"Online Sidehustles","url":"https://onlinesidehustles.info"},',
     '"author":{"@type":"Person","name":"Nate Sterling","url":"https://onlinesidehustles.info/author/nate-sterling","jobTitle":"Sweepstakes Casino Writer"},'),
    # Meta author tag
    ('<meta name="author" content="Online Sidehustles">',
     '<meta name="author" content="Nate Sterling">'),
]

changed, skipped = [], []
for fname in sorted(glob.glob('review-*.html')):
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()
    new = html
    for old, repl in REPLACEMENTS:
        new = new.replace(old, repl)
    if new != html:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new)
        changed.append(fname)
    else:
        skipped.append(fname)

print(f"Updated {len(changed)} files, skipped {len(skipped)} (already credited Nate).")
