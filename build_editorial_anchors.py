#!/usr/bin/env python3
"""
Capture each review page's editorial score as a STABLE anchor and export a map.

- Adds data-editorial="X.X" to each review's <div class="verdict-score"> so the
  daily updater can blend community votes against the original score without
  drifting (the displayed number may change; data-editorial never does).
- Writes casino-ratings/editorial-scores.json  -> { normKey: editorialScore }
  used by the website (js/casino-ratings.js), the Apps Script sheet stamp, and
  the daily review-score updater so the blended rating is identical everywhere.

Idempotent. Run:  python build_editorial_anchors.py
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))


def norm(n):
    return re.sub(r"[^a-z0-9]", "", str(n or "").lower())


# <div class="verdict-score" [data-editorial="3.8"]>3.8 / 5.0</div>
SCORE_RE = re.compile(
    r'(<div class="verdict-score")([^>]*)>\s*([0-9](?:\.[0-9])?)\s*/\s*5\.0\s*</div>'
)
CASINO_RE = re.compile(r'data-casino="([^"]+)"')
EDITORIAL_ATTR_RE = re.compile(r'data-editorial="([0-9](?:\.[0-9])?)"')


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "review-*.html")))
    scores = {}
    updated = 0
    missing = []
    for path in files:
        html = open(path, encoding="utf-8").read()
        cm = CASINO_RE.search(html)
        sm = SCORE_RE.search(html)
        if not cm or not sm:
            missing.append(os.path.basename(path) + (" (no casino)" if not cm else " (no score)"))
            continue
        casino = cm.group(1)
        attrs = sm.group(2)
        existing = EDITORIAL_ATTR_RE.search(attrs)
        # The anchor is data-editorial if already set, else the current display number.
        editorial = existing.group(1) if existing else sm.group(3)
        scores[norm(casino)] = float(editorial)

        if not existing:
            # Inject data-editorial into the opening tag, keep the display as-is.
            new_open = sm.group(1) + ' data-editorial="' + editorial + '"' + attrs
            new_block = new_open + ">" + sm.group(3) + " / 5.0</div>"
            html2 = html[:sm.start()] + new_block + html[sm.end():]
            if html2 != html:
                open(path, "w", encoding="utf-8").write(html2)
                updated += 1

    out_dir = os.path.join(ROOT, "casino-ratings")
    with open(os.path.join(out_dir, "editorial-scores.json"), "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=0, sort_keys=True)

    # Also emit a JS snippet for embedding in js/casino-ratings.js
    js = "var EDITORIAL = " + json.dumps(scores, sort_keys=True) + ";"
    with open(os.path.join(out_dir, "editorial-map.js.txt"), "w", encoding="utf-8") as f:
        f.write(js)

    print("review files:        %d" % len(files))
    print("editorial anchors:   %d" % len(scores))
    print("data-editorial added:%d" % updated)
    if missing:
        print("MISSING:")
        for m in missing:
            print("  " + m)
    print("\nwrote casino-ratings/editorial-scores.json and editorial-map.js.txt")


if __name__ == "__main__":
    main()
