import os, sys, time, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

OUT_DIR = 'images/states'
os.makedirs(OUT_DIR, exist_ok=True)

# Wikipedia Special:FilePath follows redirects to the actual Wikimedia PNG.
# Most states: "Flag_of_{State}.svg"
# Georgia conflicts with the country → use U.S. state disambiguation
WIKI_NAMES = {
    'Alabama':        'Flag_of_Alabama',
    'Alaska':         'Flag_of_Alaska',
    'Arizona':        'Flag_of_Arizona',
    'Arkansas':       'Flag_of_Arkansas',
    'California':     'Flag_of_California',
    'Colorado':       'Flag_of_Colorado',
    'Connecticut':    'Flag_of_Connecticut',
    'Delaware':       'Flag_of_Delaware',
    'Florida':        'Flag_of_Florida',
    'Georgia':        'Flag_of_Georgia_(U.S._state)',
    'Hawaii':         'Flag_of_Hawaii',
    'Idaho':          'Flag_of_Idaho',
    'Illinois':       'Flag_of_Illinois',
    'Indiana':        'Flag_of_Indiana',
    'Iowa':           'Flag_of_Iowa',
    'Kansas':         'Flag_of_Kansas',
    'Kentucky':       'Flag_of_Kentucky',
    'Louisiana':      'Flag_of_Louisiana',
    'Maine':          'Flag_of_Maine',
    'Maryland':       'Flag_of_Maryland',
    'Massachusetts':  'Flag_of_Massachusetts',
    'Michigan':       'Flag_of_Michigan',
    'Minnesota':      'Flag_of_Minnesota',
    'Mississippi':    'Flag_of_Mississippi',
    'Missouri':       'Flag_of_Missouri',
    'Montana':        'Flag_of_Montana',
    'Nebraska':       'Flag_of_Nebraska',
    'Nevada':         'Flag_of_Nevada',
    'New Hampshire':  'Flag_of_New_Hampshire',
    'New Jersey':     'Flag_of_New_Jersey',
    'New Mexico':     'Flag_of_New_Mexico',
    'New York':       'Flag_of_New_York',
    'North Carolina': 'Flag_of_North_Carolina',
    'North Dakota':   'Flag_of_North_Dakota',
    'Ohio':           'Flag_of_Ohio',
    'Oklahoma':       'Flag_of_Oklahoma',
    'Oregon':         'Flag_of_Oregon',
    'Pennsylvania':   'Flag_of_Pennsylvania',
    'Rhode Island':   'Flag_of_Rhode_Island',
    'South Carolina': 'Flag_of_South_Carolina',
    'South Dakota':   'Flag_of_South_Dakota',
    'Tennessee':      'Flag_of_Tennessee',
    'Texas':          'Flag_of_Texas',
    'Utah':           'Flag_of_Utah',
    'Vermont':        'Flag_of_Vermont',
    'Virginia':       'Flag_of_Virginia',
    'Washington':     'Flag_of_Washington',
    'West Virginia':  'Flag_of_West_Virginia',
    'Wisconsin':      'Flag_of_Wisconsin',
    'Wyoming':        'Flag_of_Wyoming',
}

ABBR = {
    'Alabama':'al','Alaska':'ak','Arizona':'az','Arkansas':'ar',
    'California':'ca','Colorado':'co','Connecticut':'ct','Delaware':'de',
    'Florida':'fl','Georgia':'ga','Hawaii':'hi','Idaho':'id',
    'Illinois':'il','Indiana':'in','Iowa':'ia','Kansas':'ks',
    'Kentucky':'ky','Louisiana':'la','Maine':'me','Maryland':'md',
    'Massachusetts':'ma','Michigan':'mi','Minnesota':'mn','Mississippi':'ms',
    'Missouri':'mo','Montana':'mt','Nebraska':'ne','Nevada':'nv',
    'New Hampshire':'nh','New Jersey':'nj','New Mexico':'nm','New York':'ny',
    'North Carolina':'nc','North Dakota':'nd','Ohio':'oh','Oklahoma':'ok',
    'Oregon':'or','Pennsylvania':'pa','Rhode Island':'ri','South Carolina':'sc',
    'South Dakota':'sd','Tennessee':'tn','Texas':'tx','Utah':'ut',
    'Vermont':'vt','Virginia':'va','Washington':'wa','West Virginia':'wv',
    'Wisconsin':'wi','Wyoming':'wy',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; StateFlagDownloader/1.0; site: onlinesidehustles.info)'
}

ok, fail = [], []

for state, wiki_name in WIKI_NAMES.items():
    abbr = ABBR[state]
    out_path = f'{OUT_DIR}/{abbr}.png'

    if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
        print(f'  SKIP  {state} (already exists)')
        ok.append(state)
        continue

    url = f'https://en.wikipedia.org/wiki/Special:FilePath/{wiki_name}.svg?width=200'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        with open(out_path, 'wb') as fout:
            fout.write(data)
        kb = len(data) // 1024
        print(f'  OK    {state:20s} → {abbr}.png  ({kb}KB)')
        ok.append(state)
    except Exception as e:
        print(f'  FAIL  {state}: {e}')
        fail.append(state)

    time.sleep(0.3)   # be polite to Wikimedia

print(f'\nDone: {len(ok)} OK, {len(fail)} failed')
if fail:
    print('Failed states:', fail)
