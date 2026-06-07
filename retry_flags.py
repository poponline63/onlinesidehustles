import os, sys, time, urllib.request, random
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

OUT_DIR = 'images/states'

WIKI_NAMES = {
    'California':     'Flag_of_California',
    'Connecticut':    'Flag_of_Connecticut',
    'Florida':        'Flag_of_Florida',
    'Hawaii':         'Flag_of_Hawaii',
    'Illinois':       'Flag_of_Illinois',
    'Iowa':           'Flag_of_Iowa',
    'Kentucky':       'Flag_of_Kentucky',
    'Maine':          'Flag_of_Maine',
    'Massachusetts':  'Flag_of_Massachusetts',
    'Minnesota':      'Flag_of_Minnesota',
    'Missouri':       'Flag_of_Missouri',
    'New Hampshire':  'Flag_of_New_Hampshire',
    'New Mexico':     'Flag_of_New_Mexico',
    'North Carolina': 'Flag_of_North_Carolina',
    'Ohio':           'Flag_of_Ohio',
    'Oregon':         'Flag_of_Oregon',
    'South Carolina': 'Flag_of_South_Carolina',
    'Utah':           'Flag_of_Utah',
    'Virginia':       'Flag_of_Virginia',
    'West Virginia':  'Flag_of_West_Virginia',
    'Wyoming':        'Flag_of_Wyoming',
}

ABBR = {
    'California':'ca','Connecticut':'ct','Florida':'fl','Hawaii':'hi',
    'Illinois':'il','Iowa':'ia','Kentucky':'ky','Maine':'me',
    'Massachusetts':'ma','Minnesota':'mn','Missouri':'mo',
    'New Hampshire':'nh','New Mexico':'nm','North Carolina':'nc',
    'Ohio':'oh','Oregon':'or','South Carolina':'sc','Utah':'ut',
    'Virginia':'va','West Virginia':'wv','Wyoming':'wy',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

ok, fail = [], []

for state, wiki_name in WIKI_NAMES.items():
    abbr = ABBR[state]
    out_path = f'{OUT_DIR}/{abbr}.png'
    if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
        print(f'  SKIP  {state}')
        ok.append(state)
        continue

    # Longer delay + jitter to avoid rate limits
    delay = random.uniform(2.5, 4.5)
    time.sleep(delay)

    url = f'https://en.wikipedia.org/wiki/Special:FilePath/{wiki_name}.svg?width=200'
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
            with open(out_path, 'wb') as fout:
                fout.write(data)
            print(f'  OK    {state:22s} → {abbr}.png  ({len(data)//1024}KB)')
            ok.append(state)
            break
        except Exception as e:
            print(f'  attempt {attempt+1} failed: {e}')
            if attempt < 2:
                time.sleep(5 + attempt * 3)
    else:
        fail.append(state)

print(f'\nDone: {len(ok)} OK, {len(fail)} failed')
if fail:
    print('Still failed:', fail)

# Count total downloaded
total = sum(1 for f in os.listdir(OUT_DIR) if f.endswith('.png'))
print(f'Total flags in {OUT_DIR}: {total}/50')
