#!/usr/bin/env python3
"""
Make content tables horizontally scrollable on mobile (instead of overflowing
the page) on the handful of pages whose tables aren't wrapped. Idempotent.
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
PAGES = [
    "affiliate-marketing.html",
    "jupiter-post.html",
    "comparisons/chumba-vs-stake.html",
    "blog/best-cashback-cards-package-churning-2026.html",
    "blog/stake-us-review-2026.html",
    "blog/sweeps-coins-vs-gold-coins-2026.html",
    "blog/sweepstakes-casino-tax-guide-2026.html",
]

MARKER = "/* responsive-tables */"
SNIPPET = (
    f"<style>{MARKER}@media(max-width:768px){{"
    "table{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch;max-width:100%;}"
    "}</style>\n</head>"
)

done = skip = 0
for rel in PAGES:
    p = os.path.join(BASE, rel)
    html = open(p, encoding="utf-8").read()
    if MARKER in html:
        print(f"  SKIP (already done): {rel}")
        skip += 1
        continue
    if "</head>" not in html:
        print(f"  SKIP (no </head>): {rel}")
        skip += 1
        continue
    html = html.replace("</head>", SNIPPET, 1)
    open(p, "w", encoding="utf-8").write(html)
    print(f"  OK: {rel}")
    done += 1

print(f"\nDone. {done} updated, {skip} skipped.")
