#!/usr/bin/env python3
"""
Set every casino's score from its TIER on the Daily Casinos List (the real
ratings), not the auto-generated per-page numbers:

    God 5.0 | High 4.8 | Medium 4.6 | New 4.5 | (Trash 4.0)

Updates each review page (data-editorial anchor + displayed verdict-score +
Overall) and regenerates editorial-scores.json + editorial-map.js.txt. The
EDITORIAL map then anchors the list, the sheet, and the review pages alike.

Run:  python rebuild_tier_scores.py
"""
import csv
import glob
import io
import json
import os
import re
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
CSV_URL = ("https://docs.google.com/spreadsheets/d/"
           "1yJAKLouHPn3AvV2PKEhulepc6HQ4uj9hfEPkl3WaMog/export?format=csv&gid=1136185769")
TIER_SCORE = {"S": 5.0, "A": 4.8, "B": 4.6, "NEW": 4.5, "SKIP": 4.0}
FALLBACK = 4.5  # review casino not found on the list
# Review-page name -> list-name normKey, where the list uses a suffix (.us/.io/.com)
ALIASES = {"luckyslots": "luckyslotsus", "luckybird": "luckybirdio", "yaycasino": "yaycasinocom"}


def norm(n):
    return re.sub(r"[^a-z0-9]", "", str(n or "").lower())


def tier_of(label):
    l = str(label or "").lower()
    if "god tier" in l: return "S"
    if "high tier" in l: return "A"
    if "medium tier" in l: return "B"
    if "trash" in l: return "SKIP"
    if "new website" in l or "new casino" in l: return "NEW"
    return None


def build_list_tiers():
    data = urllib.request.urlopen(CSV_URL, timeout=30).read().decode("utf-8")
    rows = list(csv.reader(io.StringIO(data)))
    cur = "NEW"
    out = {}
    for r in rows:
        a = r[0] if len(r) > 0 else ""
        b = r[1] if len(r) > 1 else ""
        bfirst = b.split("\n")[0].strip()
        if "signup" not in a.lower():
            t = tier_of(bfirst)
            if t: cur = t
            continue
        if not bfirst: continue
        out[norm(bfirst)] = cur
    return out


CASINO_RE = re.compile(r'data-casino="([^"]+)"')
VERDICT_RE = re.compile(
    r'(<div class="verdict-score" data-editorial=")([0-9](?:\.[0-9])?)("[^>]*>)\s*[0-9](?:\.[0-9])?\s*/\s*5\.0\s*(</div>)'
)
OVERALL_RE = re.compile(
    r'(<div class="rating-item overall"><div class="rating-item-label">Overall</div>'
    r'<div class="rating-item-value">)[0-9](?:\.[0-9])?\s*/\s*5(</div>)'
)


def main():
    tiers = build_list_tiers()
    print("casinos with a tier on the list: %d" % len(tiers))
    files = sorted(glob.glob(os.path.join(ROOT, "review-*.html")))
    scores = {}
    changed = 0
    unmatched = []
    for path in files:
        html = open(path, encoding="utf-8").read()
        cm = CASINO_RE.search(html)
        vm = VERDICT_RE.search(html)
        if not cm or not vm:
            continue
        key = norm(cm.group(1))
        tier = tiers.get(key) or tiers.get(ALIASES.get(key, ""))
        if tier is None:
            unmatched.append(cm.group(1))
            score = FALLBACK
        else:
            score = TIER_SCORE.get(tier, FALLBACK)
        scores[key] = score
        nstr = "%.1f" % score
        html2 = VERDICT_RE.sub(lambda m: m.group(1) + nstr + m.group(3) + nstr + " / 5.0" + m.group(4),
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

    from collections import Counter
    print("review pages updated: %d" % changed)
    print("score distribution:", dict(Counter(scores.values())))
    if unmatched:
        print("review casinos not found on list (got %.1f fallback): %s" % (FALLBACK, unmatched))


if __name__ == "__main__":
    main()
