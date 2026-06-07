#!/usr/bin/env python3
"""
Daily: blend each review page's editorial score (data-editorial) with the
current community votes, and write the result into the review's displayed
score(s). Same formula as js/casino-ratings.js so the number matches the
list, the sheet, and the live widget.

    blended = (editorial * WEIGHT + communityWeightedSum) / (WEIGHT + communityWeightedWeight)

Run by .github/workflows/update-review-scores.yml once a day (and manually).
"""
import glob
import json
import os
import re
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
ENDPOINT = ("https://script.google.com/macros/s/"
            "AKfycbzPbH1tgaYiQ1xBgAG0QfTMt4KqBy7VhSWyxN74dSuG3reewr0DmfrDGcdRVdhgpYrZLA/exec")
WEIGHT = 130.0  # keep in sync with js/casino-ratings.js CFG.WEIGHT


def norm(n):
    return re.sub(r"[^a-z0-9]", "", str(n or "").lower())


def fetch_ratings():
    req = urllib.request.Request(ENDPOINT + "?action=list",
                                 headers={"User-Agent": "osh-review-updater"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("ratings", {}) if data.get("ok") else {}


def blended(editorial, r):
    cs = float(r.get("cs", 0)) if r else 0.0
    cw = float(r.get("cw", 0)) if r else 0.0
    return round((editorial * WEIGHT + cs) / (WEIGHT + cw), 1)


CASINO_RE = re.compile(r'data-casino="([^"]+)"')
VERDICT_RE = re.compile(
    r'(<div class="verdict-score" data-editorial=")([0-9](?:\.[0-9])?)("[^>]*>)\s*[0-9](?:\.[0-9])?\s*/\s*5\.0\s*(</div>)'
)
OVERALL_RE = re.compile(
    r'(<div class="rating-item overall"><div class="rating-item-label">Overall</div>'
    r'<div class="rating-item-value">)[0-9](?:\.[0-9])?\s*/\s*5(</div>)'
)


def main():
    ratings = fetch_ratings()
    print("community-rated casinos: %d" % len(ratings))
    files = sorted(glob.glob(os.path.join(ROOT, "review-*.html")))
    changed = 0
    for path in files:
        html = open(path, encoding="utf-8").read()
        cm = CASINO_RE.search(html)
        vm = VERDICT_RE.search(html)
        if not cm or not vm:
            continue
        editorial = float(vm.group(2))
        r = ratings.get(norm(cm.group(1)))
        b = blended(editorial, r)
        bstr = ("%.1f" % b)

        new = VERDICT_RE.sub(lambda m: m.group(1) + m.group(2) + m.group(3) + bstr + " / 5.0" + m.group(4),
                             html, count=1)
        new = OVERALL_RE.sub(lambda m: m.group(1) + bstr + "/5" + m.group(2), new, count=1)

        if new != html:
            open(path, "w", encoding="utf-8").write(new)
            changed += 1

    print("review pages updated: %d / %d" % (changed, len(files)))


if __name__ == "__main__":
    main()
