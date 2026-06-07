#!/usr/bin/env python3
"""
Rescale the editorial review scores from the 3.2-4.7 range up to 4.0-4.9,
preserving each casino's relative ranking. Updates every review page's
data-editorial anchor + displayed verdict-score + Overall, and regenerates
editorial-scores.json + editorial-map.js.txt.

    new = round(4.0 + (old - 3.2) * 0.6, 1)   clamped to [4.0, 4.9]

Run:  python rescale_editorial.py   (then paste the new map into
js/casino-ratings.js and casino-ratings/Code.gs)
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
OLD_MIN, OLD_MAX, NEW_MIN, NEW_MAX = 3.2, 4.7, 4.0, 4.9


def rescale(old):
    new = NEW_MIN + (old - OLD_MIN) / (OLD_MAX - OLD_MIN) * (NEW_MAX - NEW_MIN)
    return round(min(NEW_MAX, max(NEW_MIN, new)), 1)


def norm(n):
    return re.sub(r"[^a-z0-9]", "", str(n or "").lower())


CASINO_RE = re.compile(r'data-casino="([^"]+)"')
VERDICT_RE = re.compile(
    r'(<div class="verdict-score" data-editorial=")([0-9](?:\.[0-9])?)("[^>]*>)\s*[0-9](?:\.[0-9])?\s*/\s*5\.0\s*(</div>)'
)
OVERALL_RE = re.compile(
    r'(<div class="rating-item overall"><div class="rating-item-label">Overall</div>'
    r'<div class="rating-item-value">)[0-9](?:\.[0-9])?\s*/\s*5(</div>)'
)


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "review-*.html")))
    scores = {}
    changed = 0
    for path in files:
        html = open(path, encoding="utf-8").read()
        cm = CASINO_RE.search(html)
        vm = VERDICT_RE.search(html)
        if not cm or not vm:
            continue
        old = float(vm.group(2))
        new = rescale(old)
        nstr = "%.1f" % new
        scores[norm(cm.group(1))] = new

        html2 = VERDICT_RE.sub(
            lambda m: m.group(1) + nstr + m.group(3) + nstr + " / 5.0" + m.group(4),
            html, count=1)
        html2 = OVERALL_RE.sub(lambda m: m.group(1) + nstr + "/5" + m.group(2), html2, count=1)
        if html2 != html:
            open(path, "w", encoding="utf-8").write(html2)
            changed += 1

    out = os.path.join(ROOT, "casino-ratings")
    json.dump(scores, open(os.path.join(out, "editorial-scores.json"), "w", encoding="utf-8"),
              indent=0, sort_keys=True)
    open(os.path.join(out, "editorial-map.js.txt"), "w", encoding="utf-8").write(
        "var EDITORIAL = " + json.dumps(scores, sort_keys=True) + ";")

    print("review pages updated: %d" % changed)
    vals = sorted(scores.values())
    print("new range: %.1f - %.1f  avg %.2f" % (min(vals), max(vals), sum(vals) / len(vals)))
    print("below 4.0: %d" % sum(1 for v in vals if v < 4.0))


if __name__ == "__main__":
    main()
