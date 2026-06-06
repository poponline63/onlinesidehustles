#!/usr/bin/env python3
"""Inject state hub CTA button into review-*.html pages that don't already have it."""

import glob
import os
import re

SITE_DIR = r"C:\Users\popon\Desktop\Claude Code\onlinesidehustles"

BANNER = """
    <div style="margin:2.5rem 0 0;padding:1.75rem;background:linear-gradient(135deg,rgba(110,231,183,.08) 0%,rgba(52,211,153,.04) 100%);border:1px solid rgba(110,231,183,.2);border-radius:14px;text-align:center;">
      <p style="color:#94a3b8;font-size:.88rem;margin-bottom:1rem;font-family:'IBM Plex Mono',monospace;letter-spacing:.04em;text-transform:uppercase;">&#127968; Playing from a specific state?</p>
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
</div>
    </div>"""

pattern = os.path.join(SITE_DIR, "review-*.html")
files = sorted(glob.glob(pattern))

injected = []
skipped_already_has = []
skipped_no_anchor = []

for fpath in files:
    fname = os.path.basename(fpath)
    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Skip if already injected
    if "shb-btn" in content:
        skipped_already_has.append(fname)
        continue

    # Try insertion points in priority order
    inserted = False

    # 1. Before </article>
    if "</article>" in content:
        content = content.replace("</article>", BANNER + "\n</article>", 1)
        inserted = True

    # 2. Before <!-- FOOTER --> comment
    elif "<!-- FOOTER -->" in content:
        content = content.replace("<!-- FOOTER -->", BANNER + "\n<!-- FOOTER -->", 1)
        inserted = True

    # 3. Before <footer
    elif re.search(r"<footer[\s>]", content, re.IGNORECASE):
        content = re.sub(r"(<footer[\s>])", BANNER + "\n\\1", content, count=1, flags=re.IGNORECASE)
        inserted = True

    if inserted:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        injected.append(fname)
    else:
        skipped_no_anchor.append(fname)

print(f"\n=== State Hub CTA Injection Report ===")
print(f"Injected:          {len(injected)} files")
print(f"Already had shb-btn: {len(skipped_already_has)} files")
print(f"No anchor found:   {len(skipped_no_anchor)} files")

if injected:
    print(f"\nInjected into:")
    for f in injected:
        print(f"  + {f}")

if skipped_no_anchor:
    print(f"\nNo anchor found in:")
    for f in skipped_no_anchor:
        print(f"  ! {f}")
