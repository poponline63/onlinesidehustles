#!/usr/bin/env python3
"""
Add a polished "Browse Casinos by State" button to key site pages.
The button uses a teal gradient with map-pin icon and arrow, glows on hover.
"""

import re

# ── The button HTML ──────────────────────────────────────────────────────────
# Self-contained: inline <style> scoped to .shb-wrap + the <a> element.
# Safe to drop anywhere; won't conflict with existing CSS.

BUTTON_HTML = '''
<div class="shb-wrap">
<style>
.shb-wrap{margin:1.4rem 0 0;}
.shb-btn{
  display:inline-flex;align-items:center;gap:.55rem;
  background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%);
  color:#060a0f;
  font-family:'IBM Plex Mono','Courier New',monospace;
  font-size:.82rem;font-weight:700;letter-spacing:.05em;
  padding:.68rem 1.45rem;border-radius:9px;
  text-decoration:none;
  box-shadow:0 4px 22px rgba(110,231,183,.38),0 0 0 1px rgba(110,231,183,.2);
  transition:transform .18s,box-shadow .18s;
  white-space:nowrap;
}
.shb-btn:hover{transform:translateY(-3px);box-shadow:0 8px 32px rgba(110,231,183,.55),0 0 0 1px rgba(110,231,183,.35);}
.shb-btn svg{flex-shrink:0;}
</style>
<a href="/states-hub.html" class="shb-btn">
  <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
  Browse Casinos by Your State
  <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
</a>
</div>'''

# ── Per-page insertion rules ─────────────────────────────────────────────────
# Each entry: (filename, old_string, replacement)
# We INSERT the button by appending it inside old_string → replacement

PAGES = [

    # casino-reviews.html — replace the existing inline button
    (
        "casino-reviews.html",
        '''    <div style="margin-top:1.5rem;">
      <a href="/states-hub.html" style="display:inline-flex;align-items:center;gap:.5rem;background:transparent;border:1px solid var(--border-md);color:var(--teal);font-family:\'IBM Plex Mono\',monospace;font-size:.78rem;font-weight:700;letter-spacing:.06em;padding:.5rem 1.2rem;border-radius:8px;text-decoration:none;transition:all .18s;" onmouseover="this.style.background=\'rgba(110,231,183,.1)\'" onmouseout="this.style.background=\'transparent\'">
        &#128205; Find Casinos Available in Your State &#8594;
      </a>
    </div>
  </section>''',
        BUTTON_HTML + "\n  </section>"
    ),

    # sweepstakes-casino-list.html — after the stats div, before closing hero-text
    (
        "sweepstakes-casino-list.html",
        "          <div class=\"stat\"><div class=\"stat-val\">$8,532</div><div class=\"stat-lbl\">Welcome SC Total</div></div>\n        </div>\n      </div>",
        "          <div class=\"stat\"><div class=\"stat-val\">$8,532</div><div class=\"stat-lbl\">Welcome SC Total</div></div>\n        </div>" + BUTTON_HTML + "\n      </div>"
    ),

    # daily-login-guide.html — same pattern as casino-list (same template)
    (
        "daily-login-guide.html",
        "          <div class=\"stat\"><div class=\"stat-val\">$8,532</div><div class=\"stat-lbl\">Welcome SC Total</div></div>\n        </div>\n      </div>",
        "          <div class=\"stat\"><div class=\"stat-val\">$8,532</div><div class=\"stat-lbl\">Welcome SC Total</div></div>\n        </div>" + BUTTON_HTML + "\n      </div>"
    ),
]


def apply_single(filepath, old, new):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if old not in content:
        return False, "marker not found"
    updated = content.replace(old, new, 1)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated)
    return True, "ok"


def inject_into_blog(filepath):
    """Add button banner before the closing </article> on all blog posts."""
    BANNER = '''
    <div style="margin:2.5rem 0 0;padding:1.75rem;background:linear-gradient(135deg,rgba(110,231,183,.08) 0%,rgba(52,211,153,.04) 100%);border:1px solid rgba(110,231,183,.2);border-radius:14px;text-align:center;">
      <p style="color:#94a3b8;font-size:.88rem;margin-bottom:1rem;font-family:\'IBM Plex Mono\',monospace;letter-spacing:.04em;text-transform:uppercase;">&#127968; Playing from a specific state?</p>
''' + BUTTON_HTML.strip() + '''
    </div>'''

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Only add if not already there
    if 'shb-btn' in content:
        return False, "already has button"

    # Insert before closing </article>
    if '</article>' not in content:
        return False, "no </article> tag"

    updated = content.replace('</article>', BANNER + '\n  </article>', 1)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated)
    return True, "ok"


def inject_into_getting_started(filepath):
    """Add button after hero-stats in getting-started, before phase 1."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'shb-btn' in content:
        return False, "already has button"
    # After hero-stats closing div, before outer hero div closes
    old = '    </div>\n  </div>\n\n  <!-- PHASE 1 -->'
    new = '    </div>' + BUTTON_HTML + '\n  </div>\n\n  <!-- PHASE 1 -->'
    if old in content:
        updated = content.replace(old, new, 1)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated)
        return True, "inserted after hero-stats"
    return False, "anchor not found"


def inject_into_blog_index(filepath):
    """Add button inside portal-hero, after description paragraph."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'shb-btn' in content:
        return False, "already has button"
    old = '        <p>Expert breakdowns on sweepstakes casinos, automation tools, and side hustles that actually work.</p>\n    </div>'
    new = '        <p>Expert breakdowns on sweepstakes casinos, automation tools, and side hustles that actually work.</p>\n    ' + BUTTON_HTML.strip() + '\n    </div>'
    if old in content:
        updated = content.replace(old, new, 1)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated)
        return True, "inserted inside portal-hero"
    return False, "anchor not found"


if __name__ == '__main__':
    import glob

    print("=== Main pages ===")
    for filepath, old, new in PAGES:
        ok, msg = apply_single(filepath, old, new)
        print(f"  {'OK' if ok else 'SKIP'}: {filepath} — {msg}")

    print("\n=== getting-started.html ===")
    ok, msg = inject_into_getting_started("getting-started.html")
    print(f"  {'OK' if ok else 'SKIP'}: {msg}")

    print("\n=== blog.html ===")
    ok, msg = inject_into_blog_index("blog.html")
    print(f"  {'OK' if ok else 'SKIP'}: {msg}")

    print("\n=== All blog posts ===")
    blog_files = sorted(glob.glob("blog/*.html"))
    done = 0
    for fp in blog_files:
        ok, msg = inject_into_blog(fp)
        if ok:
            done += 1
            print(f"  OK: {fp}")
        else:
            print(f"  SKIP: {fp} — {msg}")
    print(f"  {done}/{len(blog_files)} blog posts updated")
