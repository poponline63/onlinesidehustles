#!/usr/bin/env python3
"""
Move the "Casino Reviews" nav item to right after "Sweepstakes Casinos List"
(and before "Side Hustles") on every review page, in BOTH the desktop nav and
the mobile menu — matching the order on sweepstakes-casino-list.

Idempotent. Run:  python fix_review_nav.py [--dry]
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = "--dry" in sys.argv

DESK_SWEEPS = '<a href="/sweepstakes-casino-list" class="nav-link">Sweepstakes Casinos List</a>'
MOB_SWEEPS = '<a href="/sweepstakes-casino-list">Sweepstakes Casinos List</a>'

# desktop active casino-reviews link, with its leading newline+indent
DESK_CR_RE = re.compile(r'(\n[ \t]*<a href="/casino-reviews" class="nav-link active">Casino Reviews</a>)')
# mobile casino-reviews link: the one immediately followed by the Join Discord link
MOB_CR_RE = re.compile(r'(\n[ \t]*<a href="/casino-reviews">Casino Reviews</a>)(\s*<a href="https://discord)')


def fix(s):
    # ---- desktop ----
    m = DESK_CR_RE.search(s)
    if m and (DESK_SWEEPS + m.group(1)) not in s:  # not already right after sweeps
        cr = m.group(1)
        s = s.replace(cr, '', 1)                                   # remove from end
        s = s.replace(DESK_SWEEPS, DESK_SWEEPS + cr, 1)            # insert after sweeps
    # ---- mobile ----
    m2 = MOB_CR_RE.search(s)
    if m2 and (MOB_SWEEPS + m2.group(1)) not in s:
        cr2 = m2.group(1)
        s = s.replace(cr2 + m2.group(2), m2.group(2), 1)          # remove (keep discord)
        s = s.replace(MOB_SWEEPS, MOB_SWEEPS + cr2, 1)            # insert after sweeps
    return s


def nav_order(s):
    links = re.findall(r'<a href="/(getting-started|sweepstakes-casino-list|casino-reviews|side-hustles|tools|blog)"[^>]*class="nav-link', s)
    return links


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "review-*.html")))
    changed, skipped = 0, []
    for path in files:
        s = open(path, encoding="utf-8").read()
        s2 = fix(s)
        if s2 != s:
            changed += 1
            if not DRY:
                open(path, "w", encoding="utf-8").write(s2)
        elif "casino-reviews" not in nav_order(s) and DESK_CR_RE.search(s) is None:
            skipped.append(os.path.basename(path))
    print(("DRY-RUN: would update" if DRY else "updated") + " %d / %d review pages" % (changed, len(files)))
    if skipped:
        print("no desktop CR nav link found in:", skipped[:10])
    # show resulting order for one file
    sample = os.path.join(ROOT, "review-stake-us.html")
    if os.path.exists(sample):
        print("review-stake-us desktop nav order:", nav_order(open(sample, encoding="utf-8").read()))


if __name__ == "__main__":
    main()
