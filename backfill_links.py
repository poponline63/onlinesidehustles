#!/usr/bin/env python3
"""
Backfill referral links into all state page casino cards.
Works on both single-line and multi-line HTML card formats.
"""

import re
import os
import glob

CASINO_LINKS = {
    "stake.us": "https://stake.us/?c=OnlineSideHustles",
    "lonestar": "https://affiliates.routy.app/route/114339?affId=3353&ts=5005447",
    "lonestar casino": "https://affiliates.routy.app/route/114339?affId=3353&ts=5005447",
    "realprize": "https://affiliates.routy.app/route/91184?affId=3353&ts=5005447",
    "crown coins": "https://crowncoinscasino.com/?utm_campaign=364f186b-7369-428b-a22c-dbeaf57940c7&utm_source=friends",
    "wow vegas": "https://www.wowvegas.com/?raf=4166140",
    "dimesweeps": "https://dimesweeps.com/?ref=r_poponline63",
    "speedsweeps": "https://speedsweeps.com/?ref=r_poponline63",
    "richsweeps": "https://richsweeps.com/?ref=r_poponline63",
    "sweepsroyal": "https://sweepsroyal.com/?ref=r_poponline63",
    "fortunewheelz": "https://fortunewheelz.com/lobby/?invited_by=97XS6G",
    "funzcity": "http://funzcity.com/?invited_by=Z1Y2ZX",
    "spinquest": "http://spinquest.com/?u=WXSBTAN",
    "american luck": "https://americanluck.com/signup/90a4a8d4-856c-46e8-b853-26c91db2051e",
    "americanluck": "https://americanluck.com/signup/90a4a8d4-856c-46e8-b853-26c91db2051e",
    "jackpotrabbit": "https://jackpotrabbit.com/?invited_by=8ZGOFC",
    "jackpot rabbit": "https://jackpotrabbit.com/?invited_by=8ZGOFC",
    "lunaland": "https://lunalandcasino.com/?inviter=9d8611a0-3ce7-5f54-a691-261bb2e300e2",
    "luna land": "https://lunalandcasino.com/?inviter=9d8611a0-3ce7-5f54-a691-261bb2e300e2",
    "spinsaga": "https://play.spinsagacasino.com/?ref=29904&campaign=referFriend",
    "spin saga": "https://play.spinsagacasino.com/?ref=29904&campaign=referFriend",
    "spindoo": "https://www.spindoo.us/?r=28402933",
    "spinpals": "https://www.spinpals.com/?referralcode=50405075-7105-4b67-b399-a16f9599a795",
    "stackr": "https://www.stackrcasino.com/?referralcode=bbde20f1-7e87-497b-862b-c49b3f11024c",
    "cazino": "https://affiliates.routy.app/route/114303?affId=3353&ts=5005447",
    "legendz": "https://affiliates.routy.app/route/91174?affId=3353&ts=5005447",
    "kickr": "https://affiliates.routy.app/route/91173?affId=3353&ts=5005447",
    "luckybitsveg": "https://affiliates.routy.app/route/114338?affId=3353&ts=5005447",
    "luckybits": "https://affiliates.routy.app/route/114338?affId=3353&ts=5005447",
    "lucky bits": "https://affiliates.routy.app/route/114338?affId=3353&ts=5005447",
    "megafrenzy": "https://affiliates.routy.app/route/114341?affId=3353&ts=5005447",
    "mega frenzy": "https://affiliates.routy.app/route/114341?affId=3353&ts=5005447",
    "rolla": "https://affiliates.routy.app/route/114425?affId=3353&ts=5005447",
    "scarletsands": "https://affiliates.routy.app/route/114302?affId=3353&ts=5005447",
    "scarlet sands": "https://affiliates.routy.app/route/114302?affId=3353&ts=5005447",
    "spinblitz": "https://affiliates.routy.app/route/114426?affId=3353&ts=5005447",
    "spin blitz": "https://affiliates.routy.app/route/114426?affId=3353&ts=5005447",
    "sweepshark": "https://affiliates.routy.app/route/114301?affId=3353&ts=5005447",
    "sweep shark": "https://affiliates.routy.app/route/114301?affId=3353&ts=5005447",
    "pulsz": "https://www.pulsz.com",
    "pulsz bingo": "https://www.pulszingo.com",
    "pulszingo": "https://www.pulszingo.com",
    "chumba": "https://www.chumbacasino.com",
    "chumba casino": "https://www.chumbacasino.com",
    "luckyland": "https://www.luckylandslots.com",
    "luckylandslots": "https://www.luckylandslots.com",
    "luckylandcasino": "https://www.luckylandslots.com",
    "lucky land": "https://www.luckylandslots.com",
    "mcluck": "https://www.mcluck.com",
    "sportzino": "https://www.sportzino.com",
    "zula": "https://www.zulacasino.com",
    "zula casino": "https://www.zulacasino.com",
    "moozi": "https://www.moozi.com",
    "myprize": "https://www.myprize.com",
    "my prize": "https://www.myprize.com",
    "modo": "https://www.modo.us",
    "moonspin": "https://www.moonspin.us",
    "moon spin": "https://www.moonspin.us",
    "nolimitcoins": "https://www.nolimitcoins.com",
    "no limit coins": "https://www.nolimitcoins.com",
    "high5": "https://www.high5casino.com",
    "high 5": "https://www.high5casino.com",
    "fliff": "https://www.getfliff.com",
    "fortune coins": "https://www.fortunecoins.com",
    "fortunecoins": "https://www.fortunecoins.com",
    "chanced": "https://www.chanced.com",
    "global poker": "https://www.globalpoker.com",
    "globalpoker": "https://www.globalpoker.com",
    "golden hearts": "https://www.goldenheartsgames.com",
    "goldenhearts": "https://www.goldenheartsgames.com",
    "goldrush": "https://www.goldrushcity.com/",
    "gold rush": "https://www.goldrushcity.com/",
    "goldrushcity": "https://www.goldrushcity.com/",
    "gold rush city": "https://www.goldrushcity.com/",
    "hello millions": "https://www.hellomillions.com",
    "hellomillions": "https://www.hellomillions.com",
    "jackpota": "https://www.jackpota.com",
    "legacy arcade": "https://www.legacyarcade.com",
    "legacyarcade": "https://www.legacyarcade.com",
    "lucky hands": "https://www.luckyhands.com",
    "luckyhands": "https://www.luckyhands.com",
    "megabonanza": "https://www.megabonanza.com",
    "mega bonanza": "https://www.megabonanza.com",
    "playfame": "https://www.playfame.com",
    "play fame": "https://www.playfame.com",
    "rebet": "https://www.rebet.com",
    "shuffle": "https://www.shuffle.com",
    "spree": "https://www.spree.com",
    "sweeptastic": "https://www.sweeptastic.com",
    "tao fortune": "https://www.taofortune.com",
    "taofortune": "https://www.taofortune.com",
    "thrillz": "https://www.thrillz.com",
    "sidepot": "https://sidepot.us/home",
    "side pot": "https://sidepot.us/home",
    "yaycasino": "https://yaycasino.com",
    "yay casino": "https://yaycasino.com",
    "funrize": "https://www.funrize.com",
    "fun rize": "https://www.funrize.com",
    "rubysweeps": "https://www.rubysweeps.com",
    "ruby sweeps": "https://www.rubysweeps.com",
    "sixty6": "https://www.sixty6.com",
    "sixty 6": "https://www.sixty6.com",
    "spinsweeps": "https://www.spinsweeps.com",
    "goldtreasure": "https://www.goldtreasure.com",
    "gold treasure": "https://www.goldtreasure.com",
    "spinroll": "https://www.spinroll.com",
    "sweepstastic": "https://www.sweeptastic.com",
    "hello millions": "https://www.hellomillions.com",
}


def get_url_for_casino(name: str) -> str | None:
    key = name.strip().lower()
    if key in CASINO_LINKS:
        return CASINO_LINKS[key]
    for k, url in CASINO_LINKS.items():
        if key.startswith(k) or k.startswith(key):
            return url
    for k, url in CASINO_LINKS.items():
        if k in key or key in k:
            return url
    return None


def process_state_page(filepath: str) -> tuple[int, list[str]]:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    replaced = 0
    unmatched = []
    out = []
    current_name = None
    name_re = re.compile(r'<span class="casino-name">(.*?)</span>')

    for line in lines:
        # Track most recent casino name seen
        nm = name_re.search(line)
        if nm:
            raw = nm.group(1)
            clean = re.sub(r'<span[^>]*>.*?</span>', '', raw, flags=re.DOTALL)
            clean = re.sub(r'<[^>]+>', '', clean).strip()
            current_name = clean

        # Replace href="#" on signup-btn lines
        if 'signup-btn' in line and 'href="#"' in line:
            if current_name:
                url = get_url_for_casino(current_name)
                if url:
                    line = line.replace('href="#"', f'href="{url}"', 1)
                    replaced += 1
                    current_name = None
                else:
                    unmatched.append(current_name)
                    current_name = None

        out.append(line)

    if replaced > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(out)

    return replaced, unmatched


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    pages = sorted(glob.glob(os.path.join(base, 'casinos-in-*.html')))

    total_replaced = 0
    all_unmatched = set()

    for page in pages:
        name = os.path.basename(page)
        count, unmatched = process_state_page(page)
        total_replaced += count
        all_unmatched.update(unmatched)
        status = f"{count} links updated"
        if unmatched:
            status += f" | no URL for: {set(unmatched)}"
        print(f"  {name}: {status}")

    print(f"\nTotal: {total_replaced} signup links updated across {len(pages)} state pages")
    if all_unmatched:
        print(f"\nCasinos with no URL found ({len(all_unmatched)}):")
        for u in sorted(all_unmatched):
            print(f"  - '{u}'")


if __name__ == '__main__':
    main()
