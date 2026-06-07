#!/usr/bin/env python3
"""
Bulletproof the fade-in reveal on every review page.

Root cause of "visual/background elements show but the information is hidden":
`.fade-in{opacity:0}` hides ALL page content until JS adds the `.visible` class.
That class is added by an IntersectionObserver set up at the END of a single
IIFE that FIRST touches #nav / #hamburger / #mobileMenu. If any of those throw
(missing element, etc.), the IIFE aborts before the observer is created, so the
reveal never runs and every content block stays at opacity:0 forever, while the
background decorations (which need no JS) keep showing. To the user that reads as
"the visual elements go over / hide the information."

Fix (applied to all review-*.html):
  1. CSS: respect prefers-reduced-motion + a hard safety so content is never
     permanently invisible.
  2. A standalone, error-proof reveal script injected right after </footer>,
     BEFORE the fragile nav IIFE, with three independent failsafes:
       - its own try/catch observer (decoupled from nav code),
       - a window 'error' listener that reveals everything,
       - a 2.5s timeout + load handler that force-reveals anything still hidden.

Run:  python fix_review_reveal.py
"""
import glob
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

CSS_ANCHOR = ".fade-in.visible{opacity:1;transform:translateY(0);}"
CSS_ADD = (CSS_ANCHOR +
           "@media (prefers-reduced-motion:reduce){.fade-in{opacity:1!important;"
           "transform:none!important;transition:none!important;}}")

FOOTER_ANCHOR = "</footer>"
FAILSAFE = """</footer>
<script>
/* Failsafe content reveal: keep .fade-in content visible no matter what else
   on the page throws. Independent of the nav/hamburger script below. */
(function(){
 function revealAll(){try{var n=document.querySelectorAll('.fade-in');for(var i=0;i<n.length;i++)n[i].classList.add('visible');}catch(e){}}
 function setup(){
  try{
   if(!('IntersectionObserver' in window)){revealAll();return;}
   var obs=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('visible');obs.unobserve(e.target);}});},{threshold:0.1,rootMargin:'0px 0px -40px 0px'});
   var n=document.querySelectorAll('.fade-in');for(var i=0;i<n.length;i++)obs.observe(n[i]);
  }catch(e){revealAll();}
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',setup);else setup();
 window.addEventListener('error',revealAll);
 window.addEventListener('load',function(){setTimeout(revealAll,400);});
 setTimeout(revealAll,2500);
})();
</script>"""

# Remove the now-redundant observer lines from the original nav IIFE so there is
# a single reveal path and the nav IIFE no longer matters for visibility.
OBS_OLD = (" const obs=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');obs.unobserve(e.target)}}),{threshold:0.1,rootMargin:'0px 0px -40px 0px'});\n"
           " document.querySelectorAll('.fade-in').forEach(el=>obs.observe(el));\n")


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "review-*.html")))
    changed = 0
    skipped = []
    for path in files:
        html = open(path, encoding="utf-8").read()
        orig = html

        if CSS_ADD not in html and CSS_ANCHOR in html:
            html = html.replace(CSS_ANCHOR, CSS_ADD, 1)

        if "Failsafe content reveal" not in html and FOOTER_ANCHOR in html:
            html = html.replace(FOOTER_ANCHOR, FAILSAFE, 1)

        # drop the duplicate observer from the fragile nav IIFE if present
        if OBS_OLD in html:
            html = html.replace(OBS_OLD, "", 1)

        if html != orig:
            open(path, "w", encoding="utf-8").write(html)
            changed += 1
        else:
            skipped.append(os.path.basename(path))

    print("review pages patched: %d / %d" % (changed, len(files)))
    if skipped:
        print("unchanged (already patched or anchor missing): %d" % len(skipped))
        for s in skipped[:10]:
            print("  -", s)


if __name__ == "__main__":
    main()
