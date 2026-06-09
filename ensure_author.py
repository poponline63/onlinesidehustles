# -*- coding: utf-8 -*-
"""Ensure every blog post is authored by Nate Sterling.

Idempotent: only changes posts that still use the default "Online Sidehustles"
author (JSON-LD Organization, the meta-item byline, or the meta author tag).
Posts already authored by Nate are left untouched. Run from the repo root.
"""
import re, glob, os

AUTHOR_URL = "https://onlinesidehustles.info/author/nate-sterling"
BYLINE = ('&#9997;&#65039; By <a href="/author/nate-sterling" '
          'style="color:var(--teal);text-decoration:none;">Nate Sterling</a>')

# JSON-LD author: Organization "Online Sidehustles" -> Person "Nate Sterling"
jsonld_re = re.compile(
    r'"author"\s*:\s*\{\s*"@type"\s*:\s*"Organization"\s*,\s*'
    r'"name"\s*:\s*"Online Sidehustles"\s*'
    r'(?:,\s*"url"\s*:\s*"https://onlinesidehustles\.info"\s*)?\}'
)
jsonld_new = ('"author":{"@type":"Person","name":"Nate Sterling",'
              '"url":"' + AUTHOR_URL + '"}')

# Visible byline: a meta-item whose text is an optional pen emoji + "Online Sidehustles"
byline_re = re.compile(
    r'(<span class="meta-item">)\s*(?:&#9997;&#65039;|✍️|&#9997;)?\s*'
    r'Online Sidehustles(\s*</span>)'
)

changed = 0
files = sorted(f for f in glob.glob("blog/*.html") if os.path.basename(f) != "index.html")
for fp in files:
    with open(fp, encoding="utf-8") as f:
        s = f.read()
    orig = s
    s = jsonld_re.sub(jsonld_new, s)
    s = byline_re.sub(lambda m: m.group(1) + BYLINE + m.group(2), s)
    s = s.replace('<meta name="author" content="Online Sidehustles">',
                  '<meta name="author" content="Nate Sterling">')
    if s != orig:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(s)
        changed += 1
        print("updated:", os.path.basename(fp))

print(f"author pass complete: {changed} file(s) updated, {len(files)} scanned")
