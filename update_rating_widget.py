#!/usr/bin/env python3
"""
Update the community-rating init script already injected into every
review-*.html page so it:
  - reads the casino's editorial tier from the page's .verdict-tier element
    and passes it to the widget (drives the house seed), and
  - uses the new blended-score response shape.

Also bumps the casino-ratings.js cache version. Idempotent.

Run:  python update_rating_widget.py
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
VER = "20260607a"

NEW_BLOCK = (
    '<script src="/js/casino-ratings.js?v=' + VER + '"></script>\n'
    '<script>\n'
    '(function(){\n'
    '  function tierFromPage(){var el=document.querySelector(".verdict-tier");return el?el.textContent:"";}\n'
    '  function go(){\n'
    '    if(!window.OSHRatings||!OSHRatings.enabled)return;\n'
    '    var card=document.getElementById("oshr-review"); if(!card)return;\n'
    '    var name=card.getAttribute("data-casino");\n'
    '    var tier=OSHRatings.tierCode(tierFromPage());\n'
    '    var mount=document.getElementById("oshr-mount");\n'
    '    var thanks=document.getElementById("oshr-thanks");\n'
    '    card.style.display="";\n'
    '    function render(){ mount.innerHTML=OSHRatings.widgetHTML(name,{tier:tier}); }\n'
    '    render();\n'
    '    OSHRatings.attach(card,function(n,res){\n'
    '      render();\n'
    '      if(res&&res.ok){\n'
    '        var br=OSHRatings.blendedRating(tier,{cs:res.cs,cw:res.cw,c:res.c});\n'
    '        thanks.textContent="Thanks for rating! Community score "+br.value.toFixed(1)+"/5 ("+res.c+" votes).";\n'
    '      }\n'
    '    });\n'
    '    OSHRatings.load().then(render);\n'
    '  }\n'
    '  if(document.readyState!=="loading") go(); else document.addEventListener("DOMContentLoaded",go);\n'
    '})();\n'
    '</script>'
)

# Matches the previously-injected script block (src tag + IIFE), any ?v=.
BLOCK_RE = re.compile(
    r'<script src="/js/casino-ratings\.js[^"]*"></script>\s*'
    r'<script>\s*\(function\(\)\{.*?\}\)\(\);\s*</script>',
    re.S,
)


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "review-*.html")))
    updated, missing = 0, []
    for path in files:
        s = open(path, encoding="utf-8").read()
        if 'id="oshr-review"' not in s:
            missing.append(os.path.basename(path) + " (no widget)")
            continue
        s2, n = BLOCK_RE.subn(NEW_BLOCK, s, count=1)
        if n == 0:
            missing.append(os.path.basename(path) + " (script block not matched)")
            continue
        if s2 != s:
            open(path, "w", encoding="utf-8").write(s2)
            updated += 1
    print("Updated %d / %d review pages (ver %s)" % (updated, len(files), VER))
    if missing:
        print("Not updated:")
        for m in missing:
            print("  " + m)


if __name__ == "__main__":
    main()
