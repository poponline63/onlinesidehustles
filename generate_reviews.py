#!/usr/bin/env python3
"""
Generate review pages for all sweepstakes casinos without reviews.
Writes review-*.html and updates REVIEW_LINKS in sweepstakes-casino-list.html.
Run: py generate_reviews.py
"""
import os, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

YEAR = "2026"

TIER_STYLES = {
    "God": {"label":"God Tier","color":"#F59E0B","bg":"rgba(245,158,11,.07)","border":"rgba(245,158,11,.25)"},
    "S":   {"label":"S-Tier",  "color":"#EC4899","bg":"rgba(236,72,153,.07)","border":"rgba(236,72,153,.25)"},
    "A":   {"label":"A-Tier",  "color":"#6ee7b7","bg":"rgba(110,231,183,.07)","border":"rgba(110,231,183,.25)"},
    "B":   {"label":"B-Tier",  "color":"#60A5FA","bg":"rgba(96,165,250,.07)","border":"rgba(96,165,250,.25)"},
    "C":   {"label":"C-Tier",  "color":"#94a3b8","bg":"rgba(148,163,184,.07)","border":"rgba(148,163,184,.25)"},
}

# fmt: (name, slug, url, tier, rating, parent, year, daily, welcome, min_redeem, payout, games, restricted_states, pros, cons)
CASINOS = [
  {"name":"SweepJungle","slug":"sweepjungle","url":"https://sweepjungle.com/",
   "tier":"A","rating":4.0,"parent":"SweepJungle Interactive","year":2022,
   "daily":"0.60 SC/day","welcome":"5 SC + 100K GC free","min_redeem":"$20 SC","payout":"2–5 business days","games":"500+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["500+ games with regular new additions","Competitive $20 minimum redemption","Daily SC login bonus","Mobile-friendly platform"],
   "cons":["Newer platform with less track record","No live dealer section","Smaller library than top-tier sites"]},

  {"name":"Sweet Sweeps","slug":"sweet-sweeps","url":"https://sweetsweeps.com/?referralCode=REFMTg2NTU2",
   "tier":"B","rating":3.7,"parent":"Sweet Sweeps LLC","year":2023,
   "daily":"0.40 SC/day","welcome":"3 SC + 50K GC free","min_redeem":"$25 SC","payout":"3–7 business days","games":"300+",
   "restricted":["MI","WA","ID","NV","MT"],
   "pros":["Simple referral code sign-up bonus","Decent game variety","Regular promotional events"],
   "cons":["Higher minimum redemption than top platforms","Smaller daily bonus","Less established brand"]},

  {"name":"BangCoins","slug":"bangcoins","url":"https://bangcoins.com/?ref=r_poponline63",
   "tier":"B","rating":3.6,"parent":"BangCoins Inc","year":2023,
   "daily":"0.35 SC/day","welcome":"2 SC + 30K GC free","min_redeem":"$25 SC","payout":"3–7 business days","games":"250+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["Referral bonus via signup link","Solid slot selection","Easy account setup"],
   "cons":["Smaller game catalog","Lower daily SC value","Limited customer support"]},

  {"name":"Bankrolla","slug":"bankrolla","url":"https://bankrolla.com/",
   "tier":"C","rating":3.3,"parent":"Bankrolla Gaming","year":2023,
   "daily":"0.30 SC/day","welcome":"2 SC free","min_redeem":"$50 SC","payout":"5–10 business days","games":"200+",
   "restricted":["MI","WA","ID","NV","MT","CT"],
   "pros":["Free-to-play sweepstakes model","Slots and table games available","No purchase required"],
   "cons":["High $50 minimum redemption","Slow payout processing","Smaller game library","Less known brand"]},

  {"name":"MegaSpinz","slug":"megaspinz","url":"https://www.megaspinz.com/welcome/",
   "tier":"B","rating":3.7,"parent":"MegaSpinz Gaming","year":2022,
   "daily":"0.50 SC/day","welcome":"3 SC + 50K GC free","min_redeem":"$25 SC","payout":"3–7 business days","games":"400+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["400+ game library","Welcome bonus for new players","Solid slots selection"],
   "cons":["Higher redemption threshold than leaders","Limited payout methods","Average daily bonus"]},

  {"name":"Zonko","slug":"zonko","url":"https://www.zonko.com/welcome/",
   "tier":"C","rating":3.2,"parent":"Zonko Interactive","year":2023,
   "daily":"0.30 SC/day","welcome":"2 SC free","min_redeem":"$50 SC","payout":"5–10 business days","games":"200+",
   "restricted":["MI","WA","ID","NV","MT"],
   "pros":["Free-to-play sweepstakes format","Accessible welcome offer","New player friendly"],
   "cons":["High minimum redemption","Small game library","Slow payouts","Very new platform"]},

  {"name":"LuckLake","slug":"lucklake","url":"http://app.lucklake.com/?c=WglMPanRVp",
   "tier":"B","rating":3.8,"parent":"LuckLake Gaming","year":2022,
   "daily":"0.50 SC/day","welcome":"5 SC + 50K GC free","min_redeem":"$20 SC","payout":"3–5 business days","games":"350+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["$20 minimum redemption threshold","Solid welcome bonus","Mobile app available","Daily SC login rewards"],
   "cons":["Mid-size game library","Less known outside core community","Average daily bonus value"]},

  {"name":"Sweepico","slug":"sweepico","url":"http://sweepico.com/?invited_by=AM1F4Z",
   "tier":"B","rating":3.8,"parent":"Sweepico Ltd","year":2022,
   "daily":"0.50 SC/day","welcome":"5 SC free on signup","min_redeem":"$20 SC","payout":"3–5 business days","games":"300+",
   "restricted":["MI","WA","ID","NV","MT"],
   "pros":["$20 minimum redemption","Referral bonus program","Daily login SC rewards","Easy sign-up process"],
   "cons":["Average game variety","Less promotional activity than top sites","Limited live support"]},

  {"name":"EpicSweep","slug":"epicsweep","url":"https://epicsweep.us/?ref=88406_poponline63",
   "tier":"B","rating":3.8,"parent":"EpicSweep Inc","year":2022,
   "daily":"0.50 SC/day","welcome":"4 SC + 40K GC free","min_redeem":"$20 SC","payout":"3–5 business days","games":"350+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["$20 redemption floor","Referral bonus via link","Decent 350+ game library","Regular login rewards"],
   "cons":["Smaller footprint than top platforms","Limited payment options","Average daily bonus"]},

  {"name":"Casino.Click","slug":"casino-click","url":"https://affiliates.routy.app/route/91131?affId=3353&ts=5005447",
   "tier":"A","rating":4.0,"parent":"Casino.Click LLC","year":2022,
   "daily":"0.60 SC/day","welcome":"5 SC + 100K GC free","min_redeem":"$20 SC","payout":"2–5 business days","games":"500+",
   "restricted":["MI","WA","ID","NV","CT"],
   "pros":["500+ game library","$20 minimum redemption","Strong daily SC bonus","Clean UI and mobile experience"],
   "cons":["Less brand recognition","No live dealer","Newer platform track record"]},

  {"name":"Sixty6","slug":"sixty6","url":"https://affiliates.routy.app/route/114424?affId=3353&ts=5005447",
   "tier":"B","rating":3.7,"parent":"Sixty6 Gaming","year":2023,
   "daily":"0.40 SC/day","welcome":"3 SC + 30K GC free","min_redeem":"$25 SC","payout":"3–7 business days","games":"300+",
   "restricted":["MI","WA","ID","NV","MT"],
   "pros":["Referral bonus program","Decent slot variety","No-purchase-required model","Mobile compatible"],
   "cons":["Higher redemption floor","Below-average daily SC","Smaller game catalog"]},

  {"name":"SweepNext","slug":"sweepnext","url":"https://sweepnext.com/?c=65707_bRrgq9N8",
   "tier":"B","rating":3.7,"parent":"SweepNext Interactive","year":2023,
   "daily":"0.45 SC/day","welcome":"3 SC + 50K GC free","min_redeem":"$25 SC","payout":"3–7 business days","games":"300+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["Referral code welcome bonus","Clean platform design","Daily SC rewards","No purchase required"],
   "cons":["Higher redemption minimum","Smaller community","Average daily bonus value"]},

  {"name":"GetZoot","slug":"getzoot","url":"https://getzoot.us/?referralCode=ZOOTwithUSER75787",
   "tier":"B","rating":3.6,"parent":"GetZoot LLC","year":2023,
   "daily":"0.35 SC/day","welcome":"2 SC + 25K GC free","min_redeem":"$25 SC","payout":"3–7 business days","games":"250+",
   "restricted":["MI","WA","ID","NV","MT"],
   "pros":["Referral bonus on signup","No-purchase sweepstakes model","Regular promotions"],
   "cons":["Smaller game library","Lower daily bonus","Higher redemption floor than leaders"]},

  {"name":"ChipNWin","slug":"chipnwin","url":"https://chipnwin.com/?earn=6bPxVnUp",
   "tier":"B","rating":3.7,"parent":"ChipNWin Gaming","year":2023,
   "daily":"0.45 SC/day","welcome":"4 SC + 50K GC free","min_redeem":"$20 SC","payout":"3–5 business days","games":"300+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["$20 minimum redemption","Earn bonus on signup via link","Daily SC login bonus","Slots and table games"],
   "cons":["Newer platform with limited history","Average daily SC value","Small community size"]},

  {"name":"Lavish Luck","slug":"lavish-luck","url":"https://affiliates.routy.app/route/114340?affId=3353&ts=5005447",
   "tier":"A","rating":4.0,"parent":"Lavish Luck Ltd","year":2022,
   "daily":"0.60 SC/day","welcome":"5 SC + 100K GC free","min_redeem":"$20 SC","payout":"2–5 business days","games":"400+",
   "restricted":["MI","WA","ID","NV","CT"],
   "pros":["$20 minimum redemption","Strong daily SC bonus","400+ game selection","Good welcome offer"],
   "cons":["Less brand recognition","No live dealer","Moderate community size"]},

  {"name":"Dara Casino","slug":"dara-casino","url":"https://daracasino.com/signup?refferalCode=lrl7Kl4GhU",
   "tier":"B","rating":3.7,"parent":"Dara Casino Inc","year":2023,
   "daily":"0.40 SC/day","welcome":"3 SC + 40K GC free","min_redeem":"$25 SC","payout":"3–7 business days","games":"300+",
   "restricted":["MI","WA","ID","NV","MT"],
   "pros":["Referral sign-up bonus","Decent game library","Daily login rewards","No purchase required"],
   "cons":["Higher minimum redemption","Average daily bonus","Less established history"]},

  {"name":"The Money Factory","slug":"the-money-factory","url":"https://affiliates.routy.app/route/91263?affId=3353&ts=5005447",
   "tier":"A","rating":4.0,"parent":"The Money Factory LLC","year":2022,
   "daily":"0.60 SC/day","welcome":"5 SC + 80K GC free","min_redeem":"$20 SC","payout":"2–5 business days","games":"400+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["$20 redemption floor","Strong daily SC value","400+ games available","Solid welcome package"],
   "cons":["Less mainstream recognition","No live dealer","Moderate game library size"]},

  {"name":"Sheeshcasino","slug":"sheeshcasino","url":"https://sheeshcasino.com/?ref=m2zkndr",
   "tier":"C","rating":3.3,"parent":"Sheesh Gaming","year":2023,
   "daily":"0.30 SC/day","welcome":"2 SC free","min_redeem":"$50 SC","payout":"5–10 business days","games":"200+",
   "restricted":["MI","WA","ID","NV","MT","CT"],
   "pros":["Free-to-play model","Referral bonus via link","No purchase needed to win"],
   "cons":["High $50 minimum redemption","Slow payout times","Small game catalog","Very new platform"]},

  {"name":"GoodVibesCasino","slug":"goodvibescasino","url":"https://goodvibescasino.com/?r=T5-kzApSyLKE",
   "tier":"B","rating":3.7,"parent":"Good Vibes Gaming","year":2023,
   "daily":"0.45 SC/day","welcome":"4 SC + 50K GC free","min_redeem":"$25 SC","payout":"3–7 business days","games":"300+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["Referral bonus on signup","Positive community reputation","Daily SC login rewards","Clean interface"],
   "cons":["Higher redemption than leaders","Moderate game variety","Less brand visibility"]},

  {"name":"Wild World Casino","slug":"wild-world-casino","url":"https://wildworldcasino.com/ref/riley630326",
   "tier":"B","rating":3.6,"parent":"Wild World Gaming","year":2023,
   "daily":"0.35 SC/day","welcome":"3 SC + 30K GC free","min_redeem":"$25 SC","payout":"3–7 business days","games":"250+",
   "restricted":["MI","WA","ID","NV","MT"],
   "pros":["Referral bonus via link","Wild-themed game selection","Free-to-play sweepstakes model"],
   "cons":["Below-average daily SC","Higher redemption floor","Smaller game catalog"]},

  {"name":"SorceryReels","slug":"sorceryreels","url":"https://game.sorceryreels.com/?raf=A0Z49X7A",
   "tier":"B","rating":3.7,"parent":"SorceryReels Interactive","year":2023,
   "daily":"0.45 SC/day","welcome":"4 SC + 50K GC free","min_redeem":"$25 SC","payout":"3–7 business days","games":"300+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["Fantasy-themed game selection","Referral bonus program","Daily SC rewards","No purchase required"],
   "cons":["Niche theme limits broad appeal","Higher redemption floor","Smaller community"]},

  {"name":"Cluck","slug":"cluck","url":"https://playoncluck.com/tfc09c765",
   "tier":"C","rating":3.2,"parent":"Cluck Gaming LLC","year":2023,
   "daily":"0.30 SC/day","welcome":"2 SC free","min_redeem":"$50 SC","payout":"5–10 business days","games":"150+",
   "restricted":["MI","WA","ID","NV","MT"],
   "pros":["Unique branding and theme","Free-to-play model","Easy sign-up via link"],
   "cons":["High $50 minimum redemption","Small game library","Slow payouts","Very new to market"]},

  {"name":"Lucky Slots","slug":"lucky-slots","url":"https://luckyslots.us/?raf=aG5NSE5FalVwN1U2Z0xzbW9VcDc=",
   "tier":"B","rating":3.7,"parent":"Lucky Slots LLC","year":2022,
   "daily":"0.45 SC/day","welcome":"4 SC + 50K GC free","min_redeem":"$25 SC","payout":"3–5 business days","games":"300+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["Referral bonus on signup","Slots-focused game library","Daily SC login rewards","Mobile compatible"],
   "cons":["Higher redemption threshold","Average daily bonus","Limited table game options"]},

  {"name":"CrashDuel","slug":"crashduel","url":"https://crashduel.com/games?source=website&referralId=RN34Z5&type=create-account",
   "tier":"B","rating":3.8,"parent":"CrashDuel Inc","year":2023,
   "daily":"0.50 SC/day","welcome":"5 SC + 50K GC free","min_redeem":"$20 SC","payout":"3–5 business days","games":"200+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["Crash-style games available","$20 minimum redemption","Referral bonus on signup","Daily SC rewards"],
   "cons":["Smaller game catalog","Niche crash game focus","Newer platform track record"]},

  {"name":"Luckybird","slug":"luckybird","url":"https://affiliates.routy.app/route/91183?affId=3353&ts=5005447",
   "tier":"A","rating":4.1,"parent":"Luckybird Gaming","year":2022,
   "daily":"0.65 SC/day","welcome":"5 SC + 100K GC free","min_redeem":"$20 SC","payout":"2–5 business days","games":"500+",
   "restricted":["MI","WA","ID","NV","CT"],
   "pros":["500+ games with strong variety","$20 minimum redemption","Above-average daily SC bonus","Clean modern interface"],
   "cons":["Less brand recognition than top-tier","No live dealer section","Moderate community"]},

  {"name":"Rolling Riches","slug":"rolling-riches","url":"https://affiliates.routy.app/route/91243?affId=3353&ts=5005447",
   "tier":"A","rating":4.0,"parent":"Rolling Riches Ltd","year":2022,
   "daily":"0.60 SC/day","welcome":"5 SC + 80K GC free","min_redeem":"$20 SC","payout":"2–5 business days","games":"400+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["$20 redemption floor","Strong SC daily bonus","400+ game library","Solid welcome offer"],
   "cons":["Less recognized than VGW brands","No live dealer","Moderate community size"]},

  {"name":"Clubs Poker","slug":"clubs-poker","url":"https://affiliates.routy.app/route/91132?affId=3353&ts=5005447",
   "tier":"A","rating":4.1,"parent":"Clubs Poker Interactive","year":2021,
   "daily":"0.60 SC/day","welcome":"5 SC + 100K GC free","min_redeem":"$20 SC","payout":"2–5 business days","games":"400+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["Strong poker and table game focus","$20 redemption floor","Daily SC bonus","Established 2021 platform"],
   "cons":["Poker-heavy focus may not suit all","No dedicated live dealer","Mid-size slot catalog"]},

  {"name":"NioPlay","slug":"nioplay","url":"http://nioplay.net/?referralcode=89112214-2896-4529-907b-8fd7e7821635",
   "tier":"C","rating":3.3,"parent":"NioPlay Gaming","year":2023,
   "daily":"0.30 SC/day","welcome":"2 SC free","min_redeem":"$50 SC","payout":"5–10 business days","games":"200+",
   "restricted":["MI","WA","ID","NV","MT"],
   "pros":["Referral code welcome bonus","Free-to-play sweepstakes model","New player entry point"],
   "cons":["High $50 minimum redemption","Small game library","Slow payout times","Very new platform"]},

  {"name":"PeakPlay","slug":"peakplay","url":"https://tracking.rubystone.co/C.ashx?btag=a_75b_26c_&affid=39&siteid=75&adid=26&c=",
   "tier":"B","rating":3.8,"parent":"PeakPlay Ltd","year":2022,
   "daily":"0.50 SC/day","welcome":"5 SC + 50K GC free","min_redeem":"$20 SC","payout":"3–5 business days","games":"350+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["$20 minimum redemption","Solid welcome offer","Daily SC login rewards","RubyStone network backing"],
   "cons":["Moderate game library","Below-average daily bonus vs top tier","Less brand awareness"]},

  {"name":"Card Crush","slug":"card-crush","url":"http://www.cardcrush.com/",
   "tier":"C","rating":3.3,"parent":"Card Crush LLC","year":2023,
   "daily":"0.30 SC/day","welcome":"2 SC free","min_redeem":"$50 SC","payout":"5–10 business days","games":"150+",
   "restricted":["MI","WA","ID","NV","MT"],
   "pros":["Card-game focused library","Free-to-play sweepstakes model","Simple sign-up"],
   "cons":["High minimum redemption","Small game catalog","Slow payouts","Niche card game focus"]},

  {"name":"Jefebet","slug":"jefebet","url":"https://www.jefebet.com/",
   "tier":"B","rating":3.7,"parent":"Jefebet Gaming","year":2023,
   "daily":"0.45 SC/day","welcome":"4 SC + 50K GC free","min_redeem":"$25 SC","payout":"3–7 business days","games":"300+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["Solid daily SC rewards","Decent 300+ game library","Regular promotions","No purchase required"],
   "cons":["Higher redemption floor","Less mainstream recognition","Average daily bonus"]},

  {"name":"LuckyStake","slug":"luckystake","url":"https://luckystake.com/?c=64471_2GUt5Hff",
   "tier":"B","rating":3.8,"parent":"LuckyStake Interactive","year":2022,
   "daily":"0.50 SC/day","welcome":"5 SC + 50K GC free","min_redeem":"$20 SC","payout":"3–5 business days","games":"350+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["$20 minimum redemption","Referral bonus via link","Daily SC login rewards","350+ games"],
   "cons":["Average daily bonus value","Less established history","Moderate community size"]},

  {"name":"AcornFun","slug":"acornfun","url":"https://game.acornfun.com/",
   "tier":"C","rating":3.3,"parent":"AcornFun Games","year":2023,
   "daily":"0.30 SC/day","welcome":"2 SC free","min_redeem":"$50 SC","payout":"5–10 business days","games":"200+",
   "restricted":["MI","WA","ID","NV","MT"],
   "pros":["Free-to-play sweepstakes model","Casual game-friendly platform","No purchase required"],
   "cons":["High $50 minimum redemption","Small game library","Slow payouts","Very new platform"]},

  {"name":"Baba Casino","slug":"baba-casino","url":"https://play.babacasino.com/",
   "tier":"C","rating":3.2,"parent":"Baba Casino Ltd","year":2023,
   "daily":"0.25 SC/day","welcome":"2 SC free","min_redeem":"$50 SC","payout":"5–10 business days","games":"150+",
   "restricted":["MI","WA","ID","NV","MT","CT"],
   "pros":["Legitimate sweepstakes model","Free-to-play format","Easy account creation"],
   "cons":["High minimum redemption","Very small game library","Slow payouts","Minimal daily bonus"]},

  {"name":"Spinfinite","slug":"spinfinite","url":"https://www.spinfinite.com/welcome/",
   "tier":"B","rating":3.7,"parent":"Spinfinite Gaming","year":2022,
   "daily":"0.45 SC/day","welcome":"4 SC + 50K GC free","min_redeem":"$25 SC","payout":"3–7 business days","games":"300+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["Solid slot-focused library","Daily SC login rewards","Regular welcome promotions","Mobile compatible"],
   "cons":["Higher redemption threshold","Average daily bonus value","Less brand recognition"]},

  {"name":"Smiles Casino","slug":"smiles-casino","url":"https://smilescasino.com/",
   "tier":"B","rating":3.7,"parent":"Smiles Casino Inc","year":2023,
   "daily":"0.45 SC/day","welcome":"4 SC + 50K GC free","min_redeem":"$25 SC","payout":"3–7 business days","games":"300+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["Friendly and approachable design","Daily SC rewards","Decent game selection","No purchase required"],
   "cons":["Higher redemption than top sites","Average daily SC amount","Smaller community"]},

  {"name":"GoldTreasureCasino","slug":"goldtreasurecasino","url":"https://goldtreasurecasino.com/?referrer=AymNdsGB",
   "tier":"B","rating":3.8,"parent":"Gold Treasure Gaming","year":2022,
   "daily":"0.50 SC/day","welcome":"5 SC + 50K GC free","min_redeem":"$20 SC","payout":"3–5 business days","games":"350+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["$20 minimum redemption","Referral bonus on signup","Daily SC login rewards","Gold-themed game selection"],
   "cons":["Moderate game library","Average daily bonus","Less established than top brands"]},

  {"name":"YayCasino","slug":"yaycasino","url":"https://track.yaycasino.fun/click?o=5&a=101612&c=28",
   "tier":"B","rating":3.8,"parent":"YayCasino Ltd","year":2022,
   "daily":"0.50 SC/day","welcome":"5 SC + 60K GC free","min_redeem":"$20 SC","payout":"3–5 business days","games":"350+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["$20 redemption floor","Solid welcome bonus","Daily SC rewards","Colorful fun platform design"],
   "cons":["Less recognized brand","Average daily bonus","Moderate game catalog"]},

  {"name":"Ace Casino","slug":"ace-com","url":"https://www.ace.com/lp?r=256fce50%2F25500653",
   "tier":"A","rating":4.0,"parent":"Ace Casino LLC","year":2022,
   "daily":"0.60 SC/day","welcome":"5 SC + 100K GC free","min_redeem":"$20 SC","payout":"2–5 business days","games":"400+",
   "restricted":["MI","WA","ID","NV","CT"],
   "pros":["$20 minimum redemption","Strong daily SC bonus","400+ game selection","Premium brand positioning"],
   "cons":["Less community presence","No live dealer","Newer to competitive market"]},

  {"name":"WinBonanza","slug":"winbonanza","url":"https://winbonanza.com/",
   "tier":"A","rating":4.1,"parent":"Blazesoft","year":2023,
   "daily":"1 SC/day","welcome":"80K GC + 8 SC free","min_redeem":"$50 SC","payout":"2–5 business days","games":"500+",
   "restricted":["MI","WA","ID","NV","CT"],
   "pros":["1 SC/day — one of the highest daily bonuses","80K GC + 8 SC generous welcome offer","500+ game library from Blazesoft","Established Blazesoft network quality"],
   "cons":["Higher $50 minimum redemption","Restricted in more states than average","New to the Blazesoft portfolio"]},

  {"name":"ThrillCoins","slug":"thrillcoins","url":"https://thrillcoins.com/",
   "tier":"A","rating":4.2,"parent":"WW Funcrafters","year":2023,
   "daily":"Up to 100 SC/day","welcome":"50K GC + 1 SC free","min_redeem":"$100 SC","payout":"3–5 business days","games":"3,050+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["Massive 3,050+ game library — one of the largest","Up to 100 SC/day bonus potential","Established WW Funcrafters network","Huge variety across all game types"],
   "cons":["High $100 minimum redemption","Lower base welcome offer","Large library can feel overwhelming"]},

  {"name":"CoinsBack","slug":"coinsback","url":"https://coinsback.com/",
   "tier":"A","rating":4.1,"parent":"MW Services","year":2023,
   "daily":"Daily SC rewards","welcome":"500K GC + 2 SC free","min_redeem":"$100 SC","payout":"3–5 business days","games":"1,400+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["1,400+ games — massive library","50% SC cashback on losses — unique feature","500K GC + 2 SC welcome offer","MW Services network backing"],
   "cons":["High $100 minimum redemption","Complex cashback system for new players","Higher barrier to first redemption"]},

  {"name":"DexyPlay","slug":"dexyplay","url":"https://dexyplay.com/",
   "tier":"B","rating":3.8,"parent":"UTech Solutions","year":2025,
   "daily":"progressive, up to 65 SC over 7 days","welcome":"300K GC free, plus 30 SC on first purchase","min_redeem":"$100 SC","payout":"3 to 5 business days","games":"hundreds of",
   "restricted":[],
   "pros":["UTech Solutions family, same group as Sweepico","Progressive daily that can reach 65 SC across a week","Large 300K GC no deposit welcome","No purchase required to play or win"],
   "cons":["$100 minimum redemption","Best welcome value needs a first purchase","Newer brand still building reputation"]},

  {"name":"Zumo","slug":"zumo","url":"https://zumo.us/",
   "tier":"B","rating":3.7,"parent":"Zumo Gaming","year":2023,
   "daily":"0.40 SC/day","welcome":"3 SC + 40K GC free","min_redeem":"$25 SC","payout":"3–7 business days","games":"300+",
   "restricted":["MI","WA","ID","NV","MT"],
   "pros":["US-focused sweepstakes platform","Daily SC rewards","Decent game selection","No purchase required"],
   "cons":["Higher minimum redemption","Average daily bonus","Newer market entrant"]},

  {"name":"Coin Wizard Games","slug":"coin-wizard-games","url":"https://coinwizardgames.com/",
   "tier":"C","rating":3.3,"parent":"Coin Wizard Games LLC","year":2023,
   "daily":"0.30 SC/day","welcome":"2 SC free","min_redeem":"$50 SC","payout":"5–10 business days","games":"200+",
   "restricted":["MI","WA","ID","NV","MT"],
   "pros":["Wizard-themed gaming experience","Free-to-play sweepstakes format","No purchase required"],
   "cons":["High minimum redemption","Small game library","Slow payouts","Very new platform"]},

  {"name":"Winera","slug":"winera","url":"https://winera.com/",
   "tier":"C","rating":3.3,"parent":"Winera Interactive","year":2023,
   "daily":"0.30 SC/day","welcome":"2 SC free","min_redeem":"$50 SC","payout":"5–10 business days","games":"200+",
   "restricted":["MI","WA","ID","NV","MT"],
   "pros":["Legitimate sweepstakes casino","Free-to-play model","Easy account creation"],
   "cons":["High minimum redemption","Small game library","Slow payouts","Very new market entrant"]},

  {"name":"Luck Party","slug":"luck-party","url":"https://luckparty.com/",
   "tier":"B","rating":3.7,"parent":"Luck Party Ltd","year":2023,
   "daily":"0.45 SC/day","welcome":"4 SC + 50K GC free","min_redeem":"$25 SC","payout":"3–7 business days","games":"300+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["Party-themed engaging design","Daily SC login rewards","Solid welcome offer","No purchase required"],
   "cons":["Higher redemption floor","Average daily bonus","Smaller community than top sites"]},

  {"name":"Diam.bet","slug":"diam-bet","url":"https://diam.bet/",
   "tier":"B","rating":3.7,"parent":"Diam Gaming","year":2023,
   "daily":"0.45 SC/day","welcome":"4 SC + 50K GC free","min_redeem":"$25 SC","payout":"3–7 business days","games":"300+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["Solid game variety","Daily SC rewards","No purchase required","Regular bonus events"],
   "cons":["Higher redemption floor","Average daily bonus","Less established brand"]},

  {"name":"TheBoss.us","slug":"theboss","url":"https://theboss.us/",
   "tier":"B","rating":3.7,"parent":"Jefe Ltd","year":2024,
   "daily":"daily wheel spin","welcome":"2K GC + 2 SC free","min_redeem":"$100 SC","payout":"3 to 5 business days","games":"hundreds of",
   "restricted":[],
   "pros":["Established operator, Jefe Ltd since 2024","Solid 2 SC no deposit welcome","Daily wheel spin for variety","No purchase required to play or win"],
   "cons":["$100 minimum redemption","Cyprus based operator","Game library smaller than top tier sites"]},

  {"name":"Acebet.cc","slug":"acebet","url":"https://acebet.cc/",
   "tier":"B","rating":3.6,"parent":"Acebet Gaming","year":2023,
   "daily":"0.40 SC/day","welcome":"3 SC + 40K GC free","min_redeem":"$25 SC","payout":"3–7 business days","games":"250+",
   "restricted":["MI","WA","ID","NV","MT"],
   "pros":["Sports betting and casino games","Daily SC rewards","No purchase required"],
   "cons":["Higher redemption floor","Below-average daily bonus","Smaller game library","Less established brand"]},

  {"name":"VegaWin","slug":"vegawin","url":"https://vegawin.com/",
   "tier":"C","rating":3.3,"parent":"VegaWin Interactive","year":2023,
   "daily":"0.30 SC/day","welcome":"2 SC free","min_redeem":"$50 SC","payout":"5–10 business days","games":"200+",
   "restricted":["MI","WA","ID","NV","MT"],
   "pros":["Vegas-themed experience","Free-to-play model","No purchase required"],
   "cons":["High minimum redemption","Small game library","Slow payouts","Minimal daily bonus"]},

  {"name":"Dogg House Casino","slug":"dogg-house","url":"https://dogghousecasino.com/",
   "tier":"S","rating":4.6,"parent":"Death Row Games / Trivelta","year":2023,
   "daily":"Daily SC rewards + free spins","welcome":"1,000 DC + 1 Dogg Cash free","min_redeem":"$20 SC","payout":"2–5 business days","games":"500+",
   "restricted":["WA","ID","NV"],
   "pros":["Death Row Records branding — unique S-tier identity","Full sportsbook integration","500+ premium games including exclusive content","$20 minimum redemption — low barrier to cash out","Industry-leading brand recognition"],
   "cons":["Newer platform still building reputation","Dogg Cash currency adds complexity","Restricted in 3 states"]},

  {"name":"Jackpot Daily","slug":"jackpot-daily","url":"https://www.jackpotdaily.com/",
   "tier":"A","rating":4.1,"parent":"Jackpot Daily Ltd","year":2022,
   "daily":"0.65 SC/day","welcome":"5 SC + 100K GC free","min_redeem":"$20 SC","payout":"2–5 business days","games":"500+",
   "restricted":["MI","WA","ID","NV","CT"],
   "pros":["500+ daily-updated game selection","$20 minimum redemption","Above-average daily SC bonus","Strong welcome offer"],
   "cons":["Less established than VGW platforms","No live dealer section","Moderate community size"]},

  {"name":"Jackpot Go","slug":"jackpot-go","url":"https://jackpotgo.com/",
   "tier":"B","rating":3.8,"parent":"Jackpot Go","year":2025,
   "daily":"progressive daily login","welcome":"10K GC + 2 SC free","min_redeem":"$100 SC","payout":"around 3 business days","games":"hundreds of",
   "restricted":[],
   "pros":["Strong reputation, 1,651 Trustpilot reviews","Reported legit payouts in around 3 days with no min or max limit","1x playthrough","Solid 2 SC no deposit welcome"],
   "cons":["$100 minimum redemption","Operator details are thin","Newer brand"]},

  {"name":"LuckyRush","slug":"luckyrush","url":"https://luckyrush.io/",
   "tier":"A","rating":4.2,"parent":"High Rollers of St. Lucie","year":2022,
   "daily":"Regular SC rewards","welcome":"100 SC for $50 purchase (1x playthrough)","min_redeem":"$100 SC","payout":"2–5 business days","games":"400+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["1x playthrough — industry-leading low wagering","Florida-based operator with US compliance focus","400+ quality games","Strong SC purchase value with 100 SC for $50"],
   "cons":["High $100 minimum redemption","Welcome offer requires purchase to maximize","Less known outside hardcore community"]},

  {"name":"FortunaRush","slug":"fortunarush","url":"https://fortunarush.com/",
   "tier":"A","rating":4.1,"parent":"FortunaRush LLC","year":2022,
   "daily":"0.65 SC/day","welcome":"5 SC + 100K GC free","min_redeem":"$20 SC","payout":"2–5 business days","games":"450+",
   "restricted":["MI","WA","ID","NV","CT"],
   "pros":["$20 redemption floor","Above-average daily SC bonus","450+ game library","Strong welcome offer"],
   "cons":["Less established brand","No live dealer","Moderate community presence"]},

  {"name":"Novig","slug":"novig","url":"https://novig.com/",
   "tier":"A","rating":4.0,"parent":"Novig Technologies","year":2022,
   "daily":"5 SC free (code SIGNMEUP1)","welcome":"5 SC free with code SIGNMEUP1","min_redeem":"$20 SC","payout":"2–3 business days","games":"Sportsbook only",
   "restricted":["MI","WA","ID","NV","MT"],
   "pros":["$20 minimum redemption — very low barrier","Sportsbook-only — sharp betting focus","Fast 2–3 day payouts","Promo code SIGNMEUP1 for free SC"],
   "cons":["No casino slots or table games","Sportsbook-only limits casual players","Smaller platform vs full-casino competitors"]},

  {"name":"Punt Casino","slug":"punt","url":"https://punt.com/",
   "tier":"A","rating":4.2,"parent":"Punt Interactive","year":2022,
   "daily":"0.70 SC/day","welcome":"5 SC + 100K GC free","min_redeem":"$20 SC","payout":"2–5 business days","games":"500+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["Strong 0.70 SC/day daily bonus","$20 minimum redemption","500+ game library","Solid welcome package","Clean and intuitive platform design"],
   "cons":["Less mainstream recognition than top brands","No live dealer section","Moderate community size"]},

  {"name":"RubySweeps","slug":"rubysweeps","url":"https://play.rubysweeps.com/",
   "tier":"B","rating":3.9,"parent":"RubySweeps Gaming","year":2022,
   "daily":"0.55 SC/day","welcome":"5 SC + 50K GC free","min_redeem":"$20 SC","payout":"3–5 business days","games":"350+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["$20 minimum redemption","Solid daily SC rewards","350+ quality games","No purchase required to play"],
   "cons":["Moderate game library size","Less recognized than top-tier brands","Average community activity"]},

  {"name":"TaoSweeps","slug":"taosweeps","url":"https://taosweeps.com/",
   "tier":"B","rating":3.7,"parent":"TaoSweeps Ltd","year":2023,
   "daily":"0.45 SC/day","welcome":"4 SC + 50K GC free","min_redeem":"$25 SC","payout":"3–7 business days","games":"300+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["Zen-themed calming game design","Daily SC login rewards","Decent game variety","No purchase required"],
   "cons":["Higher redemption floor","Average daily bonus","Smaller community","Newer to market"]},

  {"name":"OceanKing","slug":"oceanking","url":"https://oceanking.io/",
   "tier":"B","rating":3.8,"parent":"OceanKing Gaming","year":2022,
   "daily":"0.50 SC/day","welcome":"5 SC + 50K GC free","min_redeem":"$20 SC","payout":"3–5 business days","games":"300+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["$20 minimum redemption","Ocean-themed game selection","Daily SC rewards","No purchase required"],
   "cons":["Moderate game library","Average daily bonus","Less established brand"]},

  {"name":"Coin Frenzy","slug":"coin-frenzy","url":"https://coinfrenzy.com/",
   "tier":"B","rating":3.8,"parent":"Coin Frenzy Interactive","year":2022,
   "daily":"0.50 SC/day","welcome":"5 SC + 60K GC free","min_redeem":"$20 SC","payout":"3–5 business days","games":"350+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["$20 minimum redemption","Daily SC login bonus","350+ game library","Fun frenzy-style promotions"],
   "cons":["Average daily SC amount","Less known brand","Moderate community size"]},

  {"name":"Scoop Casino","slug":"scoop","url":"https://scoop.com/",
   "tier":"B","rating":3.8,"parent":"Scoop Gaming LLC","year":2022,
   "daily":"0.50 SC/day","welcome":"5 SC + 50K GC free","min_redeem":"$20 SC","payout":"3–5 business days","games":"300+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["$20 minimum redemption","Daily SC login rewards","Clean and modern interface","No purchase required"],
   "cons":["Moderate game catalog","Average daily bonus","Less brand recognition"]},

  {"name":"Betr","slug":"betr","url":"https://betr.app/",
   "tier":"A","rating":4.1,"parent":"Betr Technologies","year":2022,
   "daily":"Regular SC rewards","welcome":"5 SC + 100K GC free","min_redeem":"$20 SC","payout":"2–5 business days","games":"400+ including sportsbook",
   "restricted":["MI","WA","ID","NV"],
   "pros":["Sports betting + casino in one app","$20 minimum redemption","400+ games including sportsbook","Mobile-first design","Jake Paul / Betr brand backing"],
   "cons":["Sportsbook/casino crossover can feel divided","Less established than traditional sweeps casinos","Mobile-first may not suit desktop players"]},

  {"name":"Scrooge Casino","slug":"scrooge","url":"https://scrooge.casino/",
   "tier":"B","rating":3.7,"parent":"Scrooge LLC","year":2023,
   "daily":"Daily wheel spin bonus","welcome":"Daily wheel + first purchase bonus","min_redeem":"$100 SC ($50 gift cards)","payout":"3–7 business days","games":"300+",
   "restricted":["MI","WA","ID","NV"],
   "pros":["Daily bonus wheel for variety","Gift card redemption option ($50 min)","Holiday/scrooge-themed branding","No purchase required for free play"],
   "cons":["High $100 SC minimum redemption ($50 for gift cards)","SC expires after 7 days — tight window","Higher redemption barrier than most competitors"]},

  {"name":"Kickr","slug":"kickr","url":"https://affiliates.routy.app/route/91173?affId=3353&ts=5005447",
   "tier":"A","rating":4.0,"parent":"Kickr Games Pty Ltd","year":2023,
   "daily":"0.30 SC/day","welcome":"4 SC + 150K GC free","min_redeem":"$50 SC (gift cards)","payout":"2–5 business days","games":"Casino + Sportsbook",
   "restricted":["WA","MI","ID","NV","MT"],
   "pros":["Full sportsbook + casino on one platform","1x playthrough on Bucks (SC) — low wagering to redeem","Frequent free coin drops (Bits every 2 min, 5K Bits every 30 min)","Gift card redemptions from just $50","Established operator (Kickr Games) since 2023"],
   "cons":["Higher $200 minimum for bank/cash redemptions","'Bucks' (SC) and 'Bits' (GC) naming can confuse newcomers","Restricted in roughly a dozen states","Sportsbook-forward — fewer pure slots than casino-only rivals"]},

  {"name":"Stormrush","slug":"stormrush","url":"https://stormrushcasino.com/",
   "tier":"A","rating":4.1,"parent":"A1 Development LLC","year":2025,
   "daily":"0.50 SC/day (day 6 streak)","welcome":"500K GC free, or 750K GC + 40 SC for $19.99","min_redeem":"$25 SC (gift cards)","payout":"around 36 hours via PayPal","games":"hundreds of",
   "restricted":[],
   "pros":["Run by A1 Development, the same operator as Funrize, NoLimitCoins and TaoFortune","Fast PayPal payouts, often around 36 hours","1x playthrough requirement","Low $25 gift card redemption floor"],
   "cons":["SC daily only reaches full value after a 6 day streak","Game library smaller than the biggest social casinos","Higher $100 floor for card cash outs"]},

  {"name":"Cider","slug":"cider","url":"https://cidercasino.com/",
   "tier":"A","rating":4.2,"parent":"Mystic Mirror Studio","year":2025,
   "daily":"progressive 0.30 to 0.60 SC/day","welcome":"20K GC + 0.30 SC free","min_redeem":"$50 SC (gift cards)","payout":"under 2 business days","games":"hundreds of",
   "restricted":[],
   "pros":["Strong reputation with 2,276 Trustpilot reviews","Fast payouts, often under 2 days","Progressive daily login that grows to 0.60 SC","1x playthrough"],
   "cons":["Welcome SC bonus is small at 0.30 SC","Not available in roughly 11 states","Newer brand still building a track record"]},

  {"name":"Mr. Goodwin","slug":"mr-goodwin","url":"https://mrgoodwin.com/",
   "tier":"B","rating":3.9,"parent":"UTech Solutions","year":2025,
   "daily":"7 day daily reward cycle","welcome":"160K GC + 2 SC free","min_redeem":"$100 SC","payout":"24 to 48 hours for gift cards, 3 to 5 days for bank","games":"1,000+",
   "restricted":[],
   "pros":["Operated by UTech Solutions, the same family as Sweepico and SweepShark","1,000+ slots","Solid 2 SC no deposit welcome","Fast gift card redemptions"],
   "cons":["$100 minimum redemption","Daily reward runs on a fixed 7 day cycle","Bank payouts take 3 to 5 days"]},

  {"name":"Gleaming Slots","slug":"gleaming-slots","url":"https://gleamingcasino.com/",
   "tier":"A","rating":4.2,"parent":"Eternal Boom Ltd","year":2025,
   "daily":"2K GC + 0.5 SC/day (around 5.8 SC per week)","welcome":"10K GC + 0.30 SC free","min_redeem":"$100 SC","payout":"3 to 5 business days","games":"hundreds of",
   "restricted":[],
   "pros":["Highly rated app, 4.8 stars on the App Store across 81k ratings","4.6 Trustpilot score","Daily login that adds up to around 5.8 SC per week","PayPal and bank redemptions"],
   "cons":["$100 minimum redemption","Not available in California or New York","Small 0.30 SC welcome bonus"]},

  {"name":"Coinz.us","slug":"coinz","url":"https://coinz.us/",
   "tier":"C","rating":3.5,"parent":"Nickle Tech LLC","year":2025,
   "daily":"scratchcard, up to 2 SC/day","welcome":"10K GC + 1 SC free","min_redeem":"$50 SC (gift cards)","payout":"3 to 5 business days","games":"500+",
   "restricted":[],
   "pros":["Fun daily scratchcard worth up to 2 SC","500+ games","Low $50 gift card redemption floor","No purchase required to play or win"],
   "cons":["Smaller operator, Nickle Tech LLC","$100 floor for cash redemptions","Limited promotions compared to bigger sites"]},

  {"name":"FireSevens","slug":"firesevens","url":"https://firesevenscasino.com/",
   "tier":"B","rating":3.7,"parent":"UTech Solutions","year":2025,
   "daily":"daily login plus a random bonus","welcome":"250K GC + 1 SC free","min_redeem":"$25 SC (gift cards)","payout":"3 to 5 business days","games":"1,300+",
   "restricted":[],
   "pros":["UTech Solutions family, same group as Sweepico","Large 1,300+ game library","Generous 250K GC welcome","Low $25 gift card redemption floor"],
   "cons":["RNG certification not confirmed","$100 floor for cash redemptions","Daily bonus value varies with the random element"]},

  {"name":"Jumbo88","slug":"jumbo88","url":"https://jumbo88.com/",
   "tier":"C","rating":3.4,"parent":"InspireCore Inc","year":2025,
   "daily":"wheel, up to 3 SC by day 3","welcome":"10K GC + 1 SC free","min_redeem":"$100 SC","payout":"3 to 5 business days","games":"hundreds of",
   "restricted":[],
   "pros":["Daily wheel scales up to 3 SC by day 3","No purchase required to play or win","Straightforward sign up"],
   "cons":["Mixed reputation, Trustpilot around 3.3","$100 minimum redemption","Smaller and newer operator"]},

  {"name":"Playtana","slug":"playtana","url":"https://playtana.com/",
   "tier":"B","rating":3.8,"parent":"UTech Solutions","year":2025,
   "daily":"2K GC + 0.2 SC/day plus 5% playback","welcome":"125K GC free","min_redeem":"$25 SC (gift cards)","payout":"3 to 5 business days","games":"1,700+",
   "restricted":[],
   "pros":["UTech Solutions family, same group as Sweepico","Big 1,700+ slot library","5% playback on losses","Low $25 gift card redemption floor"],
   "cons":["Small 0.2 SC daily login","No SC in the free welcome, gold coins only","$100 floor for cash redemptions"]},

  {"name":"VegasWay","slug":"vegasway","url":"https://vegasway.com/",
   "tier":"B","rating":3.7,"parent":"UTech Solutions","year":2025,
   "daily":"Vegas Route streak plus Treasure Flip","welcome":"up to 350K GC + 1 SC free","min_redeem":"$25 SC (gift cards)","payout":"3 to 5 business days","games":"1,000+",
   "restricted":[],
   "pros":["UTech Solutions family","Two part daily with a streak and a flip game","1,000 slots","Low $25 gift card redemption floor"],
   "cons":["Daily SC value is modest","$100 floor for cash redemptions","Newer brand"]},

  {"name":"PICKEM","slug":"pickem","url":"https://pickem.com/",
   "tier":"C","rating":3.6,"parent":"Joyloop Inc","year":2025,
   "daily":"up to 0.5 SC/day from day 7","welcome":"50K GC + 1 SC free","min_redeem":"$100 SC","payout":"3 to 5 business days","games":"hundreds of",
   "restricted":[],
   "pros":["Available in 42 states, wider than most sweeps casinos","Delaware based operator, Joyloop Inc","No purchase required to play or win"],
   "cons":["Daily SC only reaches full value from day 7","$100 minimum redemption","Smaller game catalog"]},

  {"name":"Big Shot Games","slug":"big-shot-games","url":"https://bigshotgames.com/",
   "tier":"C","rating":3.5,"parent":"BSG Interactive LLC","year":2025,
   "daily":"0.01 SC/day","welcome":"10K GC + 2 SC free","min_redeem":"$100 SC","payout":"3 to 5 business days","games":"hundreds of",
   "restricted":[],
   "pros":["Solid 2 SC no deposit welcome bonus","No purchase required to play or win","Simple, clean platform"],
   "cons":["Very small 0.01 SC daily login","$100 minimum redemption","New operator with a limited track record"]},
]

# ----- HTML Generator -----

HEAD_CSS = """<style>:root{--bg:#111c2e;--bg-card:#0f1723;--bg-nav:#0c1526;--teal:#6ee7b7;--teal-dim:rgba(110,231,183,.55);--teal-faint:rgba(110,231,183,.10);--lime:#ADFF2F;--lime-text:#060a0f;--text:#e8e6e0;--text-muted:#7a8fa8;--text-dim:#94a3b8;--border:rgba(110,231,183,.12);--border-md:rgba(110,231,183,.22);--red:#f87171;}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}html{scroll-behavior:smooth;}
body{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;background:var(--bg);color:var(--text);overflow-x:hidden;min-height:100vh;}
#bgCanvas{position:fixed;inset:0;z-index:-4;pointer-events:none;}
.bg-orb{position:fixed;border-radius:50%;filter:blur(100px);pointer-events:none;z-index:-3;}
.bg-orb-1{width:600px;height:600px;top:-200px;left:-200px;background:radial-gradient(circle,rgba(110,231,183,.08) 0%,transparent 70%);}
.bg-orb-2{width:500px;height:500px;bottom:-150px;right:-150px;background:radial-gradient(circle,rgba(110,231,183,.07) 0%,transparent 70%);}
.bg-orb-3{width:400px;height:400px;top:40%;left:50%;transform:translate(-50%,-50%);background:radial-gradient(circle,rgba(110,231,183,.05) 0%,transparent 70%);}
.bg-orb-4{width:350px;height:350px;top:20%;right:10%;background:radial-gradient(circle,rgba(110,231,183,.04) 0%,transparent 70%);}
.bg-grid{position:fixed;inset:0;z-index:-3;pointer-events:none;background:linear-gradient(rgba(110,231,183,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(110,231,183,.025) 1px,transparent 1px);background-size:56px 56px;}
.bg-vignette{position:fixed;inset:0;z-index:-2;pointer-events:none;background:radial-gradient(ellipse at 50% 45%,transparent 38%,rgba(5,9,18,.45) 72%,rgba(4,8,16,.82) 100%);}
.bg-scanlines{position:fixed;inset:0;z-index:-2;pointer-events:none;background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,0,0,.07) 3px,rgba(0,0,0,.07) 4px);}
@keyframes coinFlyRTL{0%{transform:translateX(0) translateY(0) rotate(0deg);opacity:1;}80%{opacity:1;}100%{transform:translateX(-110vw) translateY(var(--dy,20px)) rotate(-720deg);opacity:0;}}
@keyframes coinFlyLTR{0%{transform:translateX(0) translateY(0) rotate(0deg);opacity:1;}80%{opacity:1;}100%{transform:translateX(110vw) translateY(var(--dy,-20px)) rotate(720deg);opacity:0;}}
.fly-coin{position:fixed;pointer-events:none;z-index:9999;font-size:1.4rem;animation-timing-function:linear;animation-fill-mode:forwards;}
.fade-in{opacity:0;transform:translateY(20px);transition:opacity .55s ease-out,transform .55s ease-out;}
.fade-in.visible{opacity:1;transform:translateY(0);}
.fade-in-delay-1{transition-delay:.1s;}.fade-in-delay-2{transition-delay:.2s;}
nav,.nav{position:fixed;top:0;left:0;right:0;z-index:1000;background:var(--bg-nav);border-bottom:1px solid var(--border);height:54px;display:flex;align-items:center;padding:0 1.5rem;transition:box-shadow .2s;}
nav.scrolled,.nav.scrolled{box-shadow:0 2px 20px rgba(0,0,0,.4);}
.nav-inner{max-width:1200px;margin:0 auto;width:100%;display:flex;align-items:center;justify-content:space-between;}
.nav-brand{display:flex;align-items:center;gap:.45rem;text-decoration:none;font-weight:700;font-size:.82rem;color:var(--text);letter-spacing:.08em;text-transform:uppercase;font-family:'IBM Plex Mono','Courier New',Courier,monospace;}
.nav-logo{height:22px;width:auto;}
.nav-links{display:flex;align-items:center;gap:.05rem;}
.nav-link{color:var(--text-dim);text-decoration:none;padding:.3rem .7rem;font-size:.78rem;font-weight:500;border-bottom:2px solid transparent;transition:all .18s;}
.nav-link:hover{color:var(--teal);}.nav-link.active{color:var(--teal);border-bottom-color:var(--teal);}
.nav-cta{background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%);color:#060a0f;text-decoration:none;padding:.35rem 1rem;font-size:.78rem;font-weight:700;border-radius:6px;margin-left:.6rem;transition:transform .18s,box-shadow .18s;box-shadow:0 2px 10px rgba(110,231,183,.28);}
.nav-cta:hover{transform:translateY(-1px);box-shadow:0 4px 18px rgba(110,231,183,.45);}
.nav-hamburger{display:none;flex-direction:column;gap:5px;background:none;border:none;cursor:pointer;padding:4px;}
.nav-hamburger span{display:block;width:22px;height:2px;background:var(--text-dim);border-radius:2px;transition:all .2s;}
.nav-hamburger.active span:nth-child(1){transform:translateY(7px) rotate(45deg);}
.nav-hamburger.active span:nth-child(2){opacity:0;}
.nav-hamburger.active span:nth-child(3){transform:translateY(-7px) rotate(-45deg);}
@media(max-width:768px){.nav-links{display:none;}.nav-hamburger{display:flex;}}
.mobile-menu{display:none;position:fixed;top:54px;left:0;right:0;z-index:999;background:var(--bg-nav);border-bottom:1px solid var(--border);padding:1rem 1.5rem;flex-direction:column;gap:.25rem;}
.mobile-menu.active,.mobile-menu.open{display:flex;}
.mobile-menu a{color:var(--text-dim);text-decoration:none;padding:.5rem 0;font-size:.9rem;border-bottom:1px solid var(--border);}
.mobile-menu a:last-child{border-bottom:none;}.mobile-menu a:hover{color:var(--teal);}
.discord-widget{position:fixed;bottom:1.25rem;left:1.25rem;z-index:9997;background:#5865F2;border-radius:14px;padding:.7rem 1rem .7rem .85rem;display:flex;align-items:center;gap:.65rem;box-shadow:0 4px 22px rgba(88,101,242,.45),0 0 0 1px rgba(255,255,255,.08);text-decoration:none;color:#fff;animation:discordIn .55s cubic-bezier(.22,1,.36,1) 2.5s both;transition:transform .18s,box-shadow .18s;max-width:230px;}
.discord-widget:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(88,101,242,.55);}
@keyframes discordIn{from{transform:translateX(-130%) scale(.9);opacity:0;}to{transform:translateX(0) scale(1);opacity:1;}}
.discord-icon{flex-shrink:0;width:28px;height:28px;}.discord-text{display:flex;flex-direction:column;line-height:1.25;}
.discord-title{font-weight:700;font-size:.82rem;}.discord-sub{font-size:.68rem;opacity:.82;}
.discord-x{position:absolute;top:-7px;right:-7px;width:20px;height:20px;border-radius:50%;background:rgba(20,20,40,.75);border:1px solid rgba(255,255,255,.18);color:#fff;font-size:11px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .15s;}
.discord-x:hover{background:rgba(248,113,113,.8);}
.content-area{padding-top:74px;min-height:100vh;}
.container{max-width:900px;margin:0 auto;padding:0 1.25rem;position:relative;z-index:1;}
.breadcrumbs{padding:1rem 0 .5rem;}
.breadcrumb-list{font-size:.78rem;color:var(--text-muted);font-family:'IBM Plex Mono',monospace;display:flex;flex-wrap:wrap;gap:.3rem;align-items:center;}
.breadcrumb-list a{color:var(--teal);text-decoration:none;}.breadcrumb-list a:hover{text-decoration:underline;}
.breadcrumb-sep{color:var(--text-dim);}
.page-header{padding:1.5rem 0 .5rem;}
.page-header h1{font-size:clamp(1.6rem,3.5vw,2.4rem);font-weight:800;letter-spacing:-.03em;color:#fff;line-height:1.2;}
.last-updated{font-size:.75rem;color:var(--text-muted);font-family:'IBM Plex Mono',monospace;margin-top:.5rem;}
.highlight{color:var(--teal);}
.verdict-card{background:var(--bg-card);border:1px solid var(--border-md);border-left:4px solid var(--teal);border-radius:10px;padding:1.5rem;margin-bottom:1.5rem;display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;}
.verdict-label{font-family:'IBM Plex Mono',monospace;font-size:.72rem;letter-spacing:.14em;font-weight:700;text-transform:uppercase;padding:.25rem .7rem;border-radius:4px;background:rgba(110,231,183,.12);color:#D4AF37;}
.verdict-tier{font-size:.78rem;font-weight:700;padding:.25rem .7rem;border-radius:4px;font-family:'IBM Plex Mono',monospace;}
.verdict-summary{flex:1 1 100%;color:var(--text-dim);font-size:.95rem;line-height:1.65;}
.verdict-score{font-size:1.8rem;font-weight:800;color:var(--teal);font-family:'IBM Plex Mono',monospace;white-space:nowrap;}
.quick-facts{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:.7rem;margin-bottom:1.5rem;}
.fact-item{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:.75rem 1rem;}
.fact-label{font-family:'IBM Plex Mono',monospace;font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);margin-bottom:.25rem;}
.fact-value{font-size:.88rem;font-weight:600;color:var(--text);}
.review-block{background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:1.5rem;margin-bottom:1.25rem;}
.review-block h2{font-size:1.1rem;font-weight:700;color:var(--teal);font-family:'IBM Plex Mono',monospace;letter-spacing:.04em;text-transform:uppercase;margin-bottom:.9rem;padding-bottom:.5rem;border-bottom:1px solid var(--border);}
.review-block p{color:var(--text-dim);font-size:.93rem;line-height:1.7;margin-bottom:.7rem;}
.review-block p:last-child{margin-bottom:0;}
.review-block strong{color:var(--text);}
.review-block ul{color:var(--text-dim);font-size:.93rem;line-height:1.7;margin-left:1.2rem;margin-bottom:.7rem;}
.review-block li{margin-bottom:.35rem;}
.pros-cons{display:grid;grid-template-columns:1fr 1fr;gap:1rem;}
@media(max-width:600px){.pros-cons{grid-template-columns:1fr;}}
.pros-card,.cons-card{background:rgba(110,231,183,.04);border-radius:8px;padding:1rem;}
.pros-card{border:1px solid rgba(110,231,183,.2);border-left:3px solid var(--teal);}
.cons-card{border:1px solid rgba(248,113,113,.2);border-left:3px solid var(--red);}
.pros-card h3{color:var(--teal);font-size:.82rem;font-family:'IBM Plex Mono',monospace;letter-spacing:.06em;text-transform:uppercase;margin-bottom:.7rem;}
.cons-card h3{color:var(--red);font-size:.82rem;font-family:'IBM Plex Mono',monospace;letter-spacing:.06em;text-transform:uppercase;margin-bottom:.7rem;}
.pros-card ul,.cons-card ul{list-style:none;display:flex;flex-direction:column;gap:.4rem;}
.pros-card li,.cons-card li{font-size:.85rem;color:var(--text-dim);display:flex;gap:.5rem;align-items:flex-start;}
.check{color:var(--teal);font-weight:700;flex-shrink:0;}.cross{color:var(--red);font-weight:700;flex-shrink:0;}
.states-grid{display:flex;flex-wrap:wrap;gap:.4rem;margin:.75rem 0;}
.state-tag{background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.3);color:var(--red);font-family:'IBM Plex Mono',monospace;font-size:.72rem;font-weight:700;padding:.2rem .55rem;border-radius:4px;}
.rating-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:.7rem;}
.rating-item{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:.75rem;text-align:center;}
.rating-item.overall{border-color:var(--teal);background:rgba(110,231,183,.06);}
.rating-item-label{font-family:'IBM Plex Mono',monospace;font-size:.68rem;letter-spacing:.08em;text-transform:uppercase;color:var(--text-muted);margin-bottom:.35rem;}
.rating-item-value{font-size:1.2rem;font-weight:800;color:var(--teal);font-family:'IBM Plex Mono',monospace;}
.rating-item.overall .rating-item-value{color:var(--lime);font-size:1.4rem;}
.cta-block{text-align:center;padding:2rem;margin-bottom:1.25rem;background:var(--bg-card);border:1px solid var(--border-md);border-radius:10px;}
.cta-btn{display:inline-block;background:var(--teal);color:#050f1a;font-weight:700;font-size:.95rem;padding:.8rem 2rem;border-radius:6px;text-decoration:none;transition:opacity .2s;margin-bottom:.75rem;}
.cta-btn:hover{opacity:.85;}.cta-note{font-size:.75rem;color:var(--text-muted);font-family:'IBM Plex Mono',monospace;}
.faq-item{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:1rem 1.2rem;margin-bottom:.65rem;}
.faq-question{font-weight:600;font-size:.9rem;color:var(--text);margin-bottom:.5rem;}
.faq-answer{font-size:.85rem;color:var(--text-dim);line-height:1.65;}
.related-links{display:flex;flex-wrap:wrap;gap:.6rem;margin-bottom:2rem;padding-top:.5rem;}
.related-link{background:var(--bg-card);border:1px solid var(--border);border-radius:6px;color:var(--teal);font-size:.8rem;font-weight:600;text-decoration:none;padding:.4rem .9rem;transition:all .18s;font-family:'IBM Plex Mono',monospace;}
.related-link:hover{border-color:var(--teal);background:var(--teal-faint);}
.promo-box{background:rgba(173,255,47,.06);border:1px solid rgba(173,255,47,.2);border-radius:10px;padding:1.25rem 1.5rem;margin-bottom:1.25rem;}
.promo-box h2{font-size:1.1rem;font-weight:700;color:var(--lime);font-family:'IBM Plex Mono',monospace;letter-spacing:.04em;text-transform:uppercase;margin-bottom:.9rem;padding-bottom:.5rem;border-bottom:1px solid rgba(173,255,47,.15);}
.promo-box p{color:var(--text-dim);font-size:.93rem;line-height:1.7;margin-bottom:.7rem;}
.promo-box p:last-child{margin-bottom:0;}
.signup-steps{list-style:none;padding:0;margin:.5rem 0;}
.signup-step{display:flex;align-items:flex-start;gap:.85rem;padding:.65rem 0;border-bottom:1px solid var(--border);}
.signup-step:last-child{border-bottom:none;}
.step-num{flex-shrink:0;width:26px;height:26px;background:var(--teal);color:#050f1a;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.78rem;font-family:'IBM Plex Mono',monospace;margin-top:1px;}
.step-text{font-size:.9rem;color:var(--text-dim);line-height:1.6;}
.disclaimer-note{font-size:.73rem;color:var(--text-muted);border-top:1px solid var(--border);padding-top:.85rem;margin-top:.85rem;line-height:1.6;font-family:'IBM Plex Mono',monospace;}
footer{background:var(--bg-nav);border-top:1px solid var(--border);padding:2.5rem 1.5rem 1.5rem;}
.footer-inner{max-width:1200px;margin:0 auto;}
.footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:2rem;margin-bottom:2rem;}
@media(max-width:768px){.footer-grid{grid-template-columns:1fr 1fr;}}
@media(max-width:480px){.footer-grid{grid-template-columns:1fr;}}
.footer-brand{display:flex;align-items:center;gap:.4rem;font-family:'IBM Plex Mono',monospace;font-size:.82rem;font-weight:700;letter-spacing:.08em;color:var(--text);text-transform:uppercase;margin-bottom:.6rem;}
.footer-brand img{height:20px;width:auto;}
.footer-tagline{font-size:.8rem;color:var(--text-muted);line-height:1.6;max-width:280px;}
.footer-col h4{font-family:'IBM Plex Mono',monospace;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--teal);margin-bottom:.75rem;}
.footer-col a{display:block;color:var(--text-dim);text-decoration:none;font-size:.82rem;margin-bottom:.4rem;}
.footer-col a:hover{color:var(--teal);}
.footer-bottom{border-top:1px solid var(--border);padding-top:1rem;display:flex;justify-content:space-between;flex-wrap:wrap;gap:.5rem;}
.footer-copy{font-size:.75rem;color:var(--text-muted);font-family:'IBM Plex Mono',monospace;}
.footer-links{display:flex;gap:1rem;}
.footer-links a{color:var(--text-muted);text-decoration:none;font-size:.75rem;font-family:'IBM Plex Mono',monospace;}
.footer-links a:hover{color:var(--teal);}
.shb-wrap{margin:1.4rem 0 0;}
.shb-btn{display:inline-flex;align-items:center;gap:.55rem;background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%);color:#060a0f;font-family:'IBM Plex Mono','Courier New',monospace;font-size:.82rem;font-weight:700;letter-spacing:.05em;padding:.68rem 1.45rem;border-radius:9px;text-decoration:none;box-shadow:0 4px 22px rgba(110,231,183,.38),0 0 0 1px rgba(110,231,183,.2);transition:transform .18s,box-shadow .18s;white-space:nowrap;}
.shb-btn:hover{transform:translateY(-3px);box-shadow:0 8px 32px rgba(110,231,183,.55),0 0 0 1px rgba(110,231,183,.35);}</style>"""

FOOTER_JS = """<script>
(function(){
 const nav=document.getElementById('nav');
 window.addEventListener('scroll',()=>{nav.classList.toggle('scrolled',window.scrollY>20);},{passive:true});
 const hb=document.getElementById('hamburger'),mm=document.getElementById('mobileMenu');
 hb.addEventListener('click',()=>{hb.classList.toggle('active');mm.classList.toggle('active');document.body.style.overflow=mm.classList.contains('active')?'hidden':'';});
 mm.querySelectorAll('a').forEach(l=>l.addEventListener('click',()=>{hb.classList.remove('active');mm.classList.remove('active');document.body.style.overflow=''}));
 const obs=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');obs.unobserve(e.target)}}),{threshold:0.1,rootMargin:'0px 0px -40px 0px'});
 document.querySelectorAll('.fade-in').forEach(el=>obs.observe(el));
})();
(function(){
 const c=document.getElementById('bgCanvas');if(!c)return;
 const ctx=c.getContext('2d');let W,H,stars=[];
 function resize(){W=c.width=window.innerWidth;H=c.height=window.innerHeight;}
 function mk(){return{x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.2+0.2,a:Math.random(),da:(Math.random()*0.004+0.001)*(Math.random()<0.5?1:-1)};}
 function init(){resize();stars=[];for(let i=0;i<120;i++)stars.push(mk());}
 function draw(){ctx.clearRect(0,0,W,H);stars.forEach(s=>{s.a+=s.da;if(s.a<=0||s.a>=1)s.da*=-1;ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fillStyle='rgba(110,231,183,'+s.a.toFixed(2)+')';ctx.fill();});requestAnimationFrame(draw);}
 window.addEventListener('resize',()=>{resize();stars=[];for(let i=0;i<120;i++)stars.push(mk());});init();draw();
})();
(function(){
 const COINS=['&#x1F4B0;','&#x1FA99;','&#x1F4B5;','&#x1F48E;'];
 function spawn(){const el=document.createElement('div');el.className='fly-coin';
  const rtl=Math.random()<0.5,dy=(Math.random()*80-40)+'px',dur=(4+Math.random()*4).toFixed(1)+'s';
  el.innerHTML=COINS[Math.floor(Math.random()*COINS.length)];
  el.style.cssText='top:'+(10+Math.random()*80)+'vh;'+(rtl?'right:-60px':'left:-60px')+';--dy:'+dy+';animation:coin'+(rtl?'FlyRTL':'FlyLTR')+' '+dur+' linear forwards;';
  document.body.appendChild(el);setTimeout(()=>el.remove(),(parseFloat(dur)+0.3)*1000);}
 setTimeout(()=>spawn(),2000);setInterval(spawn,7000);
})();
</script>
<script src="/js/analytics.js" defer></script>
<a class="discord-widget" id="discordWidget" href="https://discord.com/invite/W9bPGH8crh" target="_blank" rel="noopener"><button class="discord-x" id="discordClose" aria-label="Dismiss">&#x2715;</button><svg class="discord-icon" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M23.12 5.48A22.36 22.36 0 0 0 17.7 3.8a15.3 15.3 0 0 0-.7 1.44 20.67 20.67 0 0 0-6.02 0A15.3 15.3 0 0 0 10.3 3.8a22.41 22.41 0 0 0-5.44 1.68C1.88 10.04 1.1 14.48 1.5 18.86a22.6 22.6 0 0 0 6.82 3.42c.55-.74 1.04-1.53 1.46-2.36a14.66 14.66 0 0 1-2.3-1.1c.19-.14.38-.28.56-.43a16.06 16.06 0 0 0 13.92 0c.18.15.37.29.56.43a14.6 14.6 0 0 1-2.31 1.1c.42.83.91 1.62 1.46 2.36a22.53 22.53 0 0 0 6.82-3.42c.47-4.96-.8-9.36-3.37-13.38ZM9.68 16.28c-1.3 0-2.36-1.18-2.36-2.64s1.04-2.64 2.36-2.64 2.38 1.18 2.36 2.64c0 1.46-1.05 2.64-2.36 2.64Zm8.64 0c-1.3 0-2.36-1.18-2.36-2.64s1.04-2.64 2.36-2.64 2.38 1.18 2.36 2.64c0 1.46-1.04 2.64-2.36 2.64Z" fill="white"/></svg><div class="discord-text"><span class="discord-title">Join Discord</span><span class="discord-sub">Free SC alerts &amp; tips</span></div></a>
<script>(function(){var w=document.getElementById('discordWidget'),c=document.getElementById('discordClose');if(!w)return;if(localStorage.getItem('dcDismissed'))w.style.display='none';if(c)c.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();w.style.animation='none';w.style.transition='transform 0.3s,opacity 0.3s';w.style.transform='translateX(-130%)';w.style.opacity='0';setTimeout(function(){w.style.display='none';},300);localStorage.setItem('dcDismissed','1');});})();</script>"""


def rating_sub(r, offset):
    v = round(r + offset, 1)
    v = max(1.0, min(5.0, v))
    if v == int(v):
        return f"{int(v)}.0/5"
    return f"{v}/5"


def make_html(c):
    name     = c['name']
    slug     = c['slug']
    url      = c['url']
    tier     = c['tier']
    ts       = TIER_STYLES[tier]
    rating   = c['rating']
    parent   = c['parent']
    year     = c['year']
    daily    = c['daily']
    welcome  = c['welcome']
    min_red  = c['min_redeem']
    payout   = c['payout']
    games    = c['games']
    restricted = c.get('restricted', [])
    pros     = c['pros']
    cons     = c['cons']
    verdict_label = c.get('verdict_label', 'LEGIT')

    # Auto-derived fields
    headline = c.get('headline', f'Is {name} Legit? Full {YEAR} Review')
    summary  = c.get('summary', (
        f"{name} is a legitimate sweepstakes casino offering {games} games, a {daily} daily bonus, "
        f"and {welcome} for new players. The {min_red} minimum redemption lets players cash out real prizes "
        f"— no purchase required to play or win. Operated by {parent} since {year}."
    ))

    page_url = f"https://onlinesidehustles.info/review-{slug}.html"
    meta_title = f"{name} Review {YEAR} — Legit? {daily} Daily & {min_red} Min Cash Out"
    meta_desc  = (
        f"{name} review {YEAR}: {rating}/5. {daily} daily bonus, {welcome} signup offer, "
        f"{min_red} minimum redemption, {games} games. Is {name} legit? Full honest review."
    )
    keywords = (
        f"{name.lower()} review, is {name.lower()} legit, {name.lower()} daily bonus, "
        f"{name.lower()} payout, {name.lower()} promo code {YEAR}, {name.lower()} casino review"
    )

    # States HTML
    if restricted:
        states_html = ''.join(f'<span class="state-tag">{s}</span>' for s in restricted)
        restricted_body = f"<p>{name} is <strong>not available</strong> in the following states:</p>\n    <div class=\"states-grid\">{states_html}</div>\n    <p style=\"font-size:.85rem;color:var(--text-muted);margin-top:.5rem;\">Restrictions can change — always verify on {name}'s official website before signing up.</p>"
    else:
        restricted_body = f"<p>{name} is available in most US states. Visit the official site to confirm availability in your state before signing up.</p>"

    # Pros/Cons HTML
    pros_html = '\n'.join(f'<li><span class="check">&#10003;</span>{p}</li>' for p in pros)
    cons_html = '\n'.join(f'<li><span class="cross">&#10007;</span>{con}</li>' for con in cons)

    # Base URL (no query params) for signup steps
    base_url = url.split('?')[0].split('#')[0]

    # FAQs
    faqs = c.get('faqs', [
        (f"Is {name} legit?",
         f"Yes. {name} is a legitimate sweepstakes casino operating under US social gaming regulations. No purchase is required to play or win prizes."),
        (f"What is the {name} daily bonus?",
         f"{name} offers a {daily} as a daily login reward. Log in each day to claim it — the SC accumulates toward the {min_red} redemption minimum."),
        (f"How much do I need to cash out at {name}?",
         f"The minimum redemption at {name} is {min_red}. Complete identity verification (KYC) before requesting your first withdrawal to avoid delays."),
        (f"Does {name} have a promo code?",
         f"New players at {name} receive {welcome} automatically on signup. Check the Promotions page after logging in for any current promo codes or bonus events."),
        (f"What states is {name} not available in?",
         (f"{name} is restricted in: {', '.join(restricted)}. Always verify on the official site before signing up." if restricted
          else f"Check the official {name} website for the most up-to-date state availability — restrictions can change.")),
        (f"How long do {name} payouts take?",
         f"Payouts at {name} typically take {payout} after identity verification is complete. Complete KYC early to avoid delays on your first withdrawal."),
    ])

    faq_html = '\n'.join(
        f'<div class="faq-item"><div class="faq-question">{q}</div><div class="faq-answer">{a}</div></div>'
        for q, a in faqs
    )
    faq_schema = [
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
        for q, a in faqs
    ]

    # Schemas
    base_site_url = base_url if base_url.startswith('http') else f"https://{base_url}"
    review_schema = json.dumps({
        "@context":"https://schema.org","@type":"Review",
        "itemReviewed":{"@type":"Organization","name":name,"url":base_site_url},
        "author":{"@type":"Organization","name":"Online Sidehustles","url":"https://onlinesidehustles.info"},
        "reviewRating":{"@type":"Rating","ratingValue":str(rating),"bestRating":"5","worstRating":"1"},
        "name":meta_title,"reviewBody":summary,
        "datePublished":f"{YEAR}-06-01","dateModified":f"{YEAR}-06-06",
        "publisher":{"@type":"Organization","name":"Online Sidehustles"}
    }, separators=(',',':'))

    faq_schema_json = json.dumps(
        {"@context":"https://schema.org","@type":"FAQPage","mainEntity":faq_schema},
        separators=(',',':')
    )
    breadcrumb_schema = json.dumps({
        "@context":"https://schema.org","@type":"BreadcrumbList",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"Home","item":"https://onlinesidehustles.info/"},
            {"@type":"ListItem","position":2,"name":"Casino Reviews","item":"https://onlinesidehustles.info/casino-reviews"},
            {"@type":"ListItem","position":3,"name":f"{name} Review","item":page_url}
        ]
    }, separators=(',',':'))

    # Rating breakdown
    r_games  = c.get('r_games',  rating_sub(rating, -0.2))
    r_daily  = c.get('r_daily',  rating_sub(rating, 0.0))
    r_payout = c.get('r_payout', rating_sub(rating, -0.1))
    r_over   = f"{rating}/5"

    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-D9MKJR8494"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-D9MKJR8494');</script>
<script src="/js/analytics.js" defer></script>
<meta charset="UTF-8">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="icon" href="/favicon.ico">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="language" content="English"><meta name="revisit-after" content="3 days">
<meta name="rating" content="General"><meta name="distribution" content="global">
<meta name="geo.region" content="US"><meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>{meta_title}</title>
<meta name="description" content="{meta_desc}">
<meta name="keywords" content="{keywords}">
<meta name="author" content="Online Sidehustles"><meta name="publisher" content="Online Sidehustles">
<link rel="canonical" href="{page_url}">
<meta property="og:type" content="article">
<meta property="og:url" content="{page_url}">
<meta property="og:site_name" content="Online Sidehustles"><meta property="og:locale" content="en_US">
<meta property="og:title" content="{meta_title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:image" content="https://onlinesidehustles.info/onlinesidehustlesbanner.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{meta_title}">
<meta name="twitter:description" content="{meta_desc}">
<meta name="twitter:image" content="https://onlinesidehustles.info/onlinesidehustlesbanner.jpg">
<meta name="theme-color" content="#050810">
<script type="application/ld+json">{review_schema}</script>
<script type="application/ld+json">{faq_schema_json}</script>
<script type="application/ld+json">{breadcrumb_schema}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
{HEAD_CSS}
</head>
<body>
<canvas id="bgCanvas"></canvas>
<div class="bg-orb bg-orb-1"></div><div class="bg-orb bg-orb-2"></div>
<div class="bg-orb bg-orb-3"></div><div class="bg-orb bg-orb-4"></div>
<div class="bg-grid"></div><div class="bg-scanlines"></div><div class="bg-vignette"></div>
<nav class="nav" id="nav">
  <div class="nav-inner">
    <a href="/" class="nav-brand">
      <img src="/logo.png" alt="Online Sidehustles" class="nav-logo" style="height:22px;width:auto;">
      ONLINE SIDEHUSTLES
    </a>
    <div class="nav-links">
      <a href="/getting-started" class="nav-link">Get Started</a>
      <a href="/sweepstakes-casino-list" class="nav-link">Sweepstakes Casinos List</a>
      <a href="/side-hustles" class="nav-link">Side Hustles</a>
      <a href="/tools" class="nav-link">Tools</a>
      <a href="/blog" class="nav-link">Blog</a>
      <a href="/casino-reviews" class="nav-link active">Casino Reviews</a>
      <a href="https://discord.gg/W9bPGH8crh" class="nav-cta" target="_blank" rel="noopener">Join Discord</a>
    </div>
    <button class="nav-hamburger" id="hamburger" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>
<div class="mobile-menu" id="mobileMenu">
  <a href="/getting-started">Get Started</a>
  <a href="/sweepstakes-casino-list">Sweepstakes Casinos List</a>
  <a href="/side-hustles">Side Hustles</a>
  <a href="/tools">Tools</a>
  <a href="/blog">Blog</a>
  <a href="/casino-reviews">Casino Reviews</a>
  <a href="https://discord.gg/W9bPGH8crh" target="_blank" rel="noopener">Join Discord</a>
</div>
<div class="content-area">
 <div class="container">
  <main>
   <div class="breadcrumbs">
    <div class="breadcrumb-list">
     <a href="/">Home</a><span class="breadcrumb-sep">/</span>
     <a href="/casino-reviews">Casino Reviews</a><span class="breadcrumb-sep">/</span>
     <span>{name} Review</span>
    </div>
   </div>
   <div class="page-header fade-in">
    <h1>{name} Review {YEAR}: <span class="highlight">{headline}</span></h1>
    <p class="last-updated">&#128197; Last Updated: June {YEAR} &nbsp;|&nbsp; Reviewed by Online Sidehustles</p>
   </div>
   <div class="verdict-card fade-in fade-in-delay-1">
    <div class="verdict-label">{verdict_label}</div>
    <div class="verdict-tier" style="color:{ts['color']};border:1px solid {ts['border']};background:{ts['bg']};">{ts['label']}</div>
    <p class="verdict-summary">{summary}</p>
    <div class="verdict-score">{rating} / 5.0</div>
   </div>
   <div class="quick-facts fade-in fade-in-delay-2">
    <div class="fact-item"><div class="fact-label">Parent Company</div><div class="fact-value">{parent}</div></div>
    <div class="fact-item"><div class="fact-label">Launch Year</div><div class="fact-value">{year}</div></div>
    <div class="fact-item"><div class="fact-label">Min Age</div><div class="fact-value">18+</div></div>
    <div class="fact-item"><div class="fact-label">Daily Bonus</div><div class="fact-value">{daily}</div></div>
    <div class="fact-item"><div class="fact-label">Welcome Offer</div><div class="fact-value">{welcome}</div></div>
    <div class="fact-item"><div class="fact-label">Min Redemption</div><div class="fact-value">{min_red}</div></div>
    <div class="fact-item"><div class="fact-label">Payout Speed</div><div class="fact-value">{payout}</div></div>
    <div class="fact-item"><div class="fact-label">Games</div><div class="fact-value">{games}</div></div>
   </div>
   <section class="review-block fade-in">
    <h2>What is {name}?</h2>
    <p>{name} is a sweepstakes casino operating under US social gaming laws, offering players the chance to enjoy casino-style games and redeem prizes for real cash — all with no purchase required. Launched in {year} by <strong>{parent}</strong>, the platform provides {games} games spanning slots, table games, and more.</p>
    <p>The <strong>{daily} daily login bonus</strong> keeps accumulating sweep coins over time, and the <strong>{welcome} welcome offer</strong> gives new players a strong starting point. At a <strong>{min_red} minimum redemption</strong>, {name} aims to keep the path to first payout accessible for regular players.</p>
    <p>Like all legitimate sweepstakes casinos, {name} operates with a dual-currency system: Gold Coins for fun play and Sweep Coins (SC) that can be redeemed for real prizes. No purchase is ever required — you can earn SC through daily logins, referrals, and social promotions.</p>
   </section>
   <section class="promo-box fade-in">
    <h2>&#127881; {name} Promo Codes &amp; Bonuses (June {YEAR})</h2>
    <p>New {name} players receive <strong>{welcome}</strong> on signup — no purchase required. This free offer gives you immediate Sweep Coins to start building toward the {min_red} minimum redemption.</p>
    <p>Log in daily to claim your <strong>{daily} bonus</strong>. Check the Promotions page inside your account for any active promo codes, seasonal events, or bonus coin packages — these change regularly.</p>
   </section>
   <section class="review-block fade-in">
    <h2>How to Sign Up at {name}</h2>
    <p>Getting started takes under 5 minutes and no purchase is required — you can play entirely on free coins from day one.</p>
    <ol class="signup-steps">
     <li class="signup-step"><span class="step-num">1</span><span class="step-text">Visit <a href="{url}" target="_blank" rel="noopener">{base_url.replace('https://','').replace('http://','')}</a> and click Sign Up.</span></li>
     <li class="signup-step"><span class="step-num">2</span><span class="step-text">Enter your email, password, and personal details.</span></li>
     <li class="signup-step"><span class="step-num">3</span><span class="step-text">Verify your email address.</span></li>
     <li class="signup-step"><span class="step-num">4</span><span class="step-text">Your welcome offer of {welcome} is automatically applied.</span></li>
     <li class="signup-step"><span class="step-num">5</span><span class="step-text">Log in daily to claim your {daily} bonus and grow your SC balance.</span></li>
    </ol>
    <p style="margin-top:.8rem;"><strong>Note:</strong> Check the restricted states section below before signing up.</p>
   </section>
   <section class="review-block fade-in">
    <h2>Pros &amp; Cons</h2>
    <div class="pros-cons">
     <div class="pros-card"><h3>What We Like</h3><ul>{pros_html}</ul></div>
     <div class="cons-card"><h3>What Could Be Better</h3><ul>{cons_html}</ul></div>
    </div>
   </section>
   <section class="review-block fade-in">
    <h2>Games at {name}</h2>
    <p>{name} offers <strong>{games} games</strong> covering the most popular sweepstakes casino categories — slots of all volatility levels, classic table games including blackjack and roulette, and video poker. The game library is regularly updated with new titles to keep the experience fresh.</p>
    <p>All games are available in both Gold Coin (free play) and Sweep Coin (prize play) modes. No download is required — {name} runs entirely in the browser on desktop and mobile. Game performance is generally smooth, and the lobby is easy to navigate with filtering by category and popularity.</p>
   </section>
   <section class="review-block fade-in">
    <h2>{name} Daily Bonus &amp; Promotions</h2>
    <p>{name}'s <strong>{daily} daily login bonus</strong> rewards consistent players. Log in each day, and your SC balance grows automatically — no complicated claim process. Over the course of a month, this adds up meaningfully toward the {min_red} redemption minimum.</p>
    <p>The {welcome} welcome offer provides new players with an immediate head start. Beyond daily logins, watch the Promotions tab for limited-time bonus events, referral rewards, and seasonal promotions that can accelerate your SC earnings significantly.</p>
   </section>
   <section class="review-block fade-in">
    <h2>{name} Payouts &amp; Withdrawals</h2>
    <p>{name} requires a minimum of <strong>{min_red}</strong> for redemption. Navigate to the Cashier section, complete identity verification (government ID + address proof), and select your preferred payout method. Processing takes <strong>{payout}</strong> after KYC is complete.</p>
    <p>Complete your identity verification early — before you need it — to ensure smooth payout processing when the time comes. {name} supports standard redemption methods including gift cards and bank-based options depending on your state.</p>
   </section>
   <section class="review-block fade-in">
    <h2>Restricted States</h2>
    {restricted_body}
   </section>
   <section class="review-block fade-in">
    <h2>Our Rating Breakdown</h2>
    <div class="rating-grid">
     <div class="rating-item"><div class="rating-item-label">Games</div><div class="rating-item-value">{r_games}</div></div>
     <div class="rating-item"><div class="rating-item-label">Daily Bonus</div><div class="rating-item-value">{r_daily}</div></div>
     <div class="rating-item"><div class="rating-item-label">Payout Speed</div><div class="rating-item-value">{r_payout}</div></div>
     <div class="rating-item overall"><div class="rating-item-label">Overall</div><div class="rating-item-value">{r_over}</div></div>
    </div>
   </section>
   <div class="cta-block fade-in">
    <a href="{url}" target="_blank" rel="noopener noreferrer" class="cta-btn">Sign Up at {name} &#8594;</a>
    <p class="cta-note">Opens in a new tab &nbsp;&#183;&nbsp; Free to join &mdash; no purchase required to play.</p>
    <p class="disclaimer-note">&#9432; Affiliate disclosure: We may earn a commission if you sign up through our links at no cost to you. This does not affect our ratings or editorial independence. Sweepstakes casinos are free-to-play &mdash; no purchase necessary to enter or win.</p>
   </div>
   <section class="review-block fade-in">
    <h2>Frequently Asked Questions About {name}</h2>
    {faq_html}
   </section>
   <div class="related-links fade-in">
    <a href="/casino-reviews" class="related-link">All Casino Reviews &#8594;</a>
    <a href="/sweepstakes-casino-list" class="related-link">Full Casino List &#8594;</a>
    <a href="/getting-started" class="related-link">Getting Started Guide &#8594;</a>
    <a href="/blog" class="related-link">Blog &#8594;</a>
   </div>
  </main>
 </div>
</div>
    <div style="margin:2.5rem 0 0;padding:1.75rem;background:linear-gradient(135deg,rgba(110,231,183,.08) 0%,rgba(52,211,153,.04) 100%);border:1px solid rgba(110,231,183,.2);border-radius:14px;text-align:center;">
      <p style="color:#94a3b8;font-size:.88rem;margin-bottom:1rem;font-family:'IBM Plex Mono',monospace;letter-spacing:.04em;text-transform:uppercase;">&#127968; Playing from a specific state?</p>
<div class="shb-wrap">
<a href="/states-hub.html" class="shb-btn">
  <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
  Browse Casinos by Your State
  <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
</a>
</div>
    </div>
<footer>
 <div class="footer-inner">
  <div class="footer-grid">
   <div>
    <div class="footer-brand"><img src="/logo.png" alt="Online Sidehustles"> ONLINE SIDEHUSTLES</div>
    <p class="footer-tagline">Free guides, community tips, and tools for earning from sweepstakes casinos and daily login sites.</p>
   </div>
   <div class="footer-col"><h4>Guides</h4>
    <a href="/sweepstakes-casino-list">Sweepstakes Casinos List</a>
    <a href="/getting-started">Getting Started</a>
    <a href="/side-hustles">Side Hustles</a>
    <a href="/blog">Blog</a>
    <a href="/daily-free-sc">Daily Free SC</a>
    <a href="/new-sites">New Sites</a>
   </div>
   <div class="footer-col"><h4>Resources</h4>
    <a href="/tools">Tools</a>
    <a href="/casino-reviews">Casino Reviews</a>
    <a href="/faq">FAQ</a>
   </div>
   <div class="footer-col"><h4>Community</h4>
    <a href="https://discord.gg/W9bPGH8crh" target="_blank" rel="noopener">Discord</a>
   </div>
  </div>
  <div class="footer-bottom">
   <span class="footer-copy">&#169; {YEAR} Online Sidehustles &middot; All rights reserved</span>
   <div class="footer-links">
    <a href="/privacy">Privacy</a><a href="/terms">Terms</a><a href="/disclaimer">Disclaimer</a>
   </div>
  </div>
 </div>
</footer>
{FOOTER_JS}
</body>
</html>"""


# ----- Write files -----
written = []
skipped = []

for c in CASINOS:
    slug = c['slug']
    fname = f"review-{slug}.html"
    if os.path.exists(fname):
        skipped.append(fname)
        print(f"  SKIP (exists): {fname}")
        continue
    html = make_html(c)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    written.append((c['name'], slug))
    print(f"  WROTE: {fname}")

print(f"\nWrote {len(written)} files, skipped {len(skipped)} existing.")

# ----- Update REVIEW_LINKS in sweepstakes-casino-list.html -----
with open('sweepstakes-casino-list.html', 'r', encoding='utf-8') as f:
    main_html = f.read()

# Build new entries
new_entries = []
for name, slug in written:
    new_entries.append(f"  '{name}':'/review-{slug}.html'")

if not new_entries:
    print("No new REVIEW_LINKS entries to add.")
else:
    # Find the closing }; of REVIEW_LINKS and insert before it
    pattern = r'(const REVIEW_LINKS\s*=\s*\{[^}]+)(\};)'
    m = re.search(pattern, main_html, re.DOTALL)
    if m:
        insert_block = ',\n' + ',\n'.join(new_entries) + '\n'
        new_main = main_html[:m.start(2)] + insert_block + main_html[m.start(2):]
        with open('sweepstakes-casino-list.html', 'w', encoding='utf-8') as f:
            f.write(new_main)
        print(f"\nAdded {len(new_entries)} entries to REVIEW_LINKS.")
    else:
        print("\nERROR: Could not find REVIEW_LINKS block to update.")

print("\nDone! Run: py audit_reviews.py to verify.")
