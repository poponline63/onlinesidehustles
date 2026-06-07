import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

CASINO_DOMAINS = [
    'stake.us','wowvegas.com','crowncoinscasino.com','mcluck.com','chumbacasino.com',
    'pulsz.com','sportzino.com','zulacasino.com','spinsagacasino.com','globalpoker.com',
    'sixty6.com','rebet.com','getfliff.com','fortunecoins.com','luckylandslots.com',
    'hellomillions.com','chanced.com','funrize.com','moozi.com','jackpota.com',
    'nolimitcoins.com','modo.us','funzcity.com','moonspin.us','goldrushcity.com',
    'goldenheartsgames.com','shuffle.us','spindoo.us','spinpals.com','stackrcasino.com',
    'lunalandcasino.com','richsweeps.com','sweepsroyal.com','dimesweeps.com','speedsweeps.com',
    'americanluck.com','spinquest.com','fortunewheelz.com','myprize.us','taofortune.com',
    'jackpotrabbit.com','luckyhands.com','daracasino.com','goodvibescasino.com',
    'wildworldcasino.com','sorceryreels.com','sheeshcasino.com','pulszbingo.com',
    'rubysweeps.com','high5casino.com','luckystake.com','luckylandcasino.com',
    'luckyslots.us','sweepnext.com','getzoot.us','chipnwin.com','crashduel.com',
    'sweepjungle.com','sweetsweeps.com','bangcoins.com','epicsweep.us','sweepico.com',
    'nioplay.net','goldtreasurecasino.com','smilescasino.com','sidepot.us',
    'spinfinite.com','acornfun.com','babacasino.com','lucklake.com',
    'zonko.com','cardcrush.com','jefebet.com','bankrolla.com','megaspinz.com',
    'legacyarcade','nolimitcoins.com','fliff.com','getfliff.com','rubystone.co',
    'hello-millions','hellomillions.com','luckyland','global-poker',
]

SKIP_DOMAINS = [
    'onlinesidehustles','discord','gstatic','fonts.','google','wikipedia',
    'w3.org','schema','ogp.me','affiliates.routy','track.sportzino',
    'track.zulacasino','track.fortunecoins','track.yaycasino',
    'rebet.page.link','play.spinsaga','tracking.ruby','apps.apple',
    'cdn.sheetjs','login.auth.poker','login.chumbacasino',
]

REF_PARAMS = [
    '?ref=','?raf=','?c=','?invited_by=','?inviter=','?referral','referralCode',
    'referralcode','signup/','?r=','?u=','?utm_campaign=','?earn=',
    'login.chumba','login.auth.poker','apps.apple','?affId','?code=',
    'sign-up?code=','?source=website','play.globalpoker.com',
]

results = {}
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ['__pycache__','.git','images','node_modules']]
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        c = open(path, encoding='utf-8', errors='ignore').read()
        links = re.findall(r'href="(https?://[^"]+)"', c)
        for link in links:
            if any(s in link for s in SKIP_DOMAINS):
                continue
            for domain in CASINO_DOMAINS:
                if domain in link:
                    has_ref = any(p in link for p in REF_PARAMS)
                    if not has_ref:
                        rel = path.replace('.\\','').replace('./','').lstrip('.')
                        if domain not in results:
                            results[domain] = {'urls': set(), 'files': set()}
                        results[domain]['urls'].add(link)
                        results[domain]['files'].add(rel)
                    break

for domain in sorted(results.keys()):
    d = results[domain]
    print(f'\n=== {domain} ({len(d["files"])} files, {len(d["urls"])} unique bare URLs) ===')
    for url in sorted(d['urls']):
        print(f'  URL: {url}')
    print(f'  Files: {len(d["files"])}')
