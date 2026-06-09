#!/usr/bin/env python3
"""
add_discord_utm.py
Appends UTM parameters to the main Discord invite links (W9bPGH8crh) across the
site so GA4 can attribute Discord joins to the page/section that drove them.

  before: https://discord.gg/W9bPGH8crh
  after:  https://discord.gg/W9bPGH8crh?utm_source=site&utm_medium=review&utm_campaign=discord

medium is derived from the file type (review / state-page / blog / page).

SAFE + idempotent: only touches the W9bPGH8crh invite, only when it has no
query string yet, and never touches index.html (homepage left untouched per
request) or the unrelated kFSctbB7JY invite.
"""

import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
EXCLUDE = {"index.html"}

# Match the main invite (discord.gg/CODE or discord.com/invite/CODE) only when
# it is NOT already followed by a query string or extra path/word characters.
INVITE_RE = re.compile(
    r"(https?://discord\.(?:gg|com)/(?:invite/)?W9bPGH8crh)(?![\w?/])"
)


def medium_for(path: Path) -> str:
    name = path.name
    if name.startswith("review-"):
        return "review"
    if name.startswith("casinos-in-"):
        return "state-page"
    if path.parent.name == "blog":
        return "blog"
    return "page"


def process(path: Path) -> int:
    html = path.read_text(encoding="utf-8")
    medium = medium_for(path)
    utm = f"?utm_source=site&utm_medium={medium}&utm_campaign=discord"

    def repl(m):
        return m.group(1) + utm

    new_html, n = INVITE_RE.subn(repl, html)
    if n:
        path.write_text(new_html, encoding="utf-8")
    return n


def main():
    targets = [p for p in BASE.glob("*.html") if p.name not in EXCLUDE]
    targets += sorted(BASE.glob("blog/*.html"))

    total = 0
    touched = 0
    for path in sorted(targets):
        n = process(path)
        if n:
            touched += 1
            total += n
    print(f"Done. Tagged {total} Discord links across {touched} files "
          f"(index.html excluded).")


if __name__ == "__main__":
    main()
