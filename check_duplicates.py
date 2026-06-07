"""
Check SIGNUP_LINKS for duplicate casino names (same name with different spacing/casing/punctuation).
Also check if any new SIGNUP_LINKS keys are already used as data-name in state pages.
"""
import sys, os, re, glob
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ---- Extract all SIGNUP_LINKS keys from the HTML ----
with open('sweepstakes-casino-list.html', 'r', encoding='utf-8') as f:
    html = f.read()

keys = re.findall(r'"([^"]{1,50})":\s*"https?://', html)

def normalize(s):
    """Strip spaces, dots, hyphens, .us/.com/.io/.cc, lowercase"""
    s = s.lower()
    s = re.sub(r'\.(us|com|io|cc|bet)$', '', s)  # strip TLDs at end
    s = re.sub(r'[^a-z0-9]', '', s)               # strip non-alphanumeric
    return s

# Build normalized map
norm_map = {}
for k in keys:
    n = normalize(k)
    norm_map.setdefault(n, []).append(k)

# Report duplicates
print("=== DUPLICATE KEYS (same casino, different format) ===\n")
found_dupes = False
for n, ks in sorted(norm_map.items()):
    if len(ks) > 1:
        print(f"  DUPE [{n}]: {ks}")
        found_dupes = True
if not found_dupes:
    print("  None found.\n")

# ---- Check state pages for data-name vs SIGNUP_LINKS ----
print("\n=== STATE PAGE data-names with NO matching SIGNUP_LINKS key ===\n")
state_names = set()
for f in glob.glob('casinos-in-*.html'):
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    for m in re.finditer(r'data-name="([^"]+)"', content):
        state_names.add(m.group(1).lower())

all_keys_norm = {normalize(k): k for k in keys}

unmatched = []
for sn in sorted(state_names):
    # Check if any SIGNUP_LINKS key normalizes to match this data-name
    sn_norm = re.sub(r'[^a-z0-9]', '', sn)
    if sn_norm not in all_keys_norm:
        unmatched.append(sn)

if unmatched:
    for u in unmatched:
        print(f"  NO LINK: data-name=\"{u}\"")
else:
    print("  All state page casinos have a matching SIGNUP_LINKS entry.")
