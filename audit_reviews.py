"""
Compare SIGNUP_LINKS keys vs REVIEW_LINKS keys to find casinos missing reviews.
"""
import sys, os, re, glob
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('sweepstakes-casino-list.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract SIGNUP_LINKS keys
signup_keys = re.findall(r'"([^"]{1,60})":\s*"https?://', html)
# Remove comment lines artifacts and obvious non-casino keys
skip = {'item'}
signup_keys = [k for k in signup_keys if k not in skip and not k.startswith('//')]

# Extract REVIEW_LINKS keys
review_block = re.search(r'const REVIEW_LINKS\s*=\s*\{([^}]+)\}', html, re.DOTALL)
review_keys = set()
if review_block:
    review_keys = set(re.findall(r"'([^']+)':\s*'[^']+'", review_block.group(1)))

# Existing review HTML files
existing_files = {os.path.basename(f) for f in glob.glob('review-*.html')}

def normalize(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

review_norm = {normalize(k): k for k in review_keys}
file_norm = {re.sub(r'[^a-z0-9]', '', f.replace('review-','').replace('.html','')): f for f in existing_files}

print(f"SIGNUP_LINKS entries:  {len(signup_keys)}")
print(f"REVIEW_LINKS entries:  {len(review_keys)}")
print(f"Existing review files: {len(existing_files)}")

print("\n=== CASINOS IN SIGNUP_LINKS WITH NO REVIEW ===\n")
missing = []
already_seen = set()
for k in signup_keys:
    n = normalize(k)
    if n in already_seen:
        continue
    already_seen.add(n)
    has_review_link = n in review_norm
    has_review_file = n in file_norm
    if not has_review_link and not has_review_file:
        missing.append(k)
        print(f"  MISSING: {k}")

print(f"\nTotal missing reviews: {len(missing)}")
