"""Generate "Casinos like X" alternative pages from the new-sites.html template.

Run from repo root: python scripts/generate_alternatives.py
Creates casinos-like-<brand>.html for each brand below. Pages reuse the
new-sites.html design (nav, hero, casino cards, footer) with unique copy,
metadata, and FAQ/ItemList/Breadcrumb schema per page.
"""
import json
import re

SITE = "https://onlinesidehustles.info"

# Facts per casino, sourced from the live review pages. Chips show only
# claims that already appear in that casino's review.
CASINOS = {
    "mcluck":        ("McLuck", 4.4, ["$1 SC/day", "7,500 GC + 2.5 SC free", "$10 min redeem"], "B2 Group flagship with a $1 daily SC bonus, 400+ games, and one of the lowest redemption minimums anywhere at $10."),
    "pulsz":         ("Pulsz", 4.6, ["$0.30 SC/day", "600+ premium slots", "PayPal in 2-5 days"], "Yellow Social Interactive's slot powerhouse: 600+ premium titles, a 250% welcome match, and dependable PayPal payouts."),
    "chumba":        ("Chumba Casino", 4.5, ["$0.25-$5 SC/day", "$10 min redeem", "PayPal payouts"], "The household name of sweepstakes casinos. A progressive daily bonus that grows with your streak and the lowest cash minimum in the industry."),
    "stake-us":      ("Stake.us", 4.7, ["$1 SC/day", "25 SC free signup", "Crypto payouts 1-3 days"], "The crypto-native giant with exclusive Stake Originals, a huge 25 SC signup offer, and payouts in 1 to 3 days."),
    "luckyland":     ("LuckyLand Slots", 4.4, ["10 SC free signup", "$10 min redeem", "Reliable PayPal"], "VGW's slots-focused platform (same family as Chumba) with a generous 10 SC signup offer and quick PayPal redemptions."),
    "funrize":       ("Funrize", 4.2, ["10 SC free signup", "$0.40 SC/day", "$25 min redeem"], "TruePlay's flagship with one of the biggest free welcome offers in sweeps: 10 SC just for signing up, plus 350+ games."),
    "wow-vegas":     ("WOW Vegas", 4.2, ["1.5 SC + 8,500 WC free", "$25 min redeem", "500+ games"], "A polished Vegas-style lobby with 500+ games and frequent promo events."),
    "fortune-coins": ("Fortune Coins", 4.3, ["$0.50 SC/day", "$20 min redeem", "2-5 day payouts"], "A veteran platform (now Fortune Wins) with a strong $0.50 daily bonus and a fair $20 minimum."),
    "crown-coins":   ("Crown Coins", 4.5, ["$0.60 SC/day", "10 SC free signup", "$20 min redeem"], "One of the best-reviewed sweeps casinos in the US: $0.60 daily SC, a 10 SC welcome offer, and famously fast redemptions."),
    "global-poker":  ("Global Poker", 4.4, ["#1 sweeps poker site", "$10 min cash out", "VGW Group"], "The biggest sweepstakes poker room in the US: Hold'em, Omaha, and daily tournaments backed by VGW."),
    "zula":          ("Zula Casino", 4.6, ["$0.60 SC/day", "5 SC free signup", "400+ games"], "A fast-rising favorite with a $0.60 daily bonus, 400+ games, and quick payouts."),
    "megabonanza":   ("MegaBonanza", 4.6, ["$1 SC/day", "5 SC free signup", "$10 gift card min"], "B2 Group sister site to McLuck with the same $1 daily SC and a $10 gift card minimum."),
    "jackpota":      ("Jackpota", 4.5, ["$1 SC/day", "5 SC free signup", "$10 gift card min"], "The top-rated B2 Group casino: $1 daily SC, 5 SC free at signup, and easy $10 gift card redemptions."),
    "playfame":      ("PlayFame", 4.5, ["$1 SC/day", "5 SC free signup", "$10 gift card min"], "Another strong B2 Group platform with the family's signature $1 daily bonus and 400+ games."),
    "spinblitz":     ("SpinBlitz", 4.3, ["$1 SC/day", "800+ games", "$10 gift card min"], "McLuck's sister site with a huge 800+ game library and the same $1 daily SC bonus."),
    "realprize":     ("RealPrize", 4.3, ["$0.50 SC/day", "$5 SC free signup", "350+ games"], "A heavyweight lobby with 350+ games and a solid $0.50 daily bonus."),
    "hello-millions": ("Hello Millions", 4.3, ["5 SC free signup", "$50 min redeem", "400+ games"], "A Mega-style casino with 400+ games, a 5 SC welcome offer, and fast payouts."),
    "sportzino":     ("Sportzino", 4.5, ["$0.50 SC/day", "25 SC free signup", "Casino + sportsbook"], "The only sweepstakes platform that combines a full casino with sports betting, plus a massive 25 SC signup offer."),
    "legendz":       ("Legendz", 3.8, ["Instant redemptions", "$10 gift card min", "1,500+ games"], "1,500+ games and instant redemptions with a $10 gift card minimum."),
    "myprize":       ("MyPrize", 4.4, ["Crypto + bank payouts", "5 SC free signup", "300+ games"], "A modern platform with both crypto and bank payouts plus a VIP program."),
    "clubs-poker":   ("Clubs Poker", 4.1, ["0.60 SC/day", "5 SC + 100K GC free", "$20 min redeem"], "A dedicated sweepstakes poker room with daily SC, 400+ games, and a $20 minimum."),
    "punt":          ("Punt Casino", 4.2, ["0.70 SC/day", "5 SC + 100K GC free", "$20 min redeem"], "A crypto-friendly casino with one of the higher daily bonuses around at 0.70 SC."),
    "nolimitcoins":  ("NoLimitCoins", 4.2, ["5 SC free signup", "$0.50 SC/day", "$20 min redeem"], "Funrize's TruePlay sister site with a 5 SC welcome offer and the same fish-game-heavy library."),
    "sweeptastic":   ("Sweeptastic", 4.1, ["3 SC free signup", "$0.50 SC/day", "$25 min redeem"], "A clean, simple casino with a 3 SC welcome offer and steady $0.50 daily SC."),
    "chanced":       ("Chanced", 4.3, ["$0.50 SC/day", "5 SC free signup", "$25 min redeem"], "A reliable daily earner with $0.50 SC per day and 300+ games."),
    "dogg-house":    ("Dogg House", 4.6, ["Daily SC + free spins", "$20 min redeem", "500+ games"], "One of our highest-rated newer sites: daily SC plus free spins and a 500+ game lobby."),
    "high5":         ("High 5 Casino", 4.2, ["1,000+ games", "5 SC free signup", "$20 min cash out"], "The largest game library in sweepstakes with over 1,000 titles from a veteran slot studio."),
    "rebet":         ("Rebet", 4.5, ["Sports + casino", "$20 min redeem", "2-4 day payouts"], "The lowest minimum redemption among sports sweeps platforms, with casino games on the side."),
    "fliff":         ("Fliff", 4.4, ["1,000+ sports markets", "Free Fliff Cash signup", "Fast payouts"], "The leading sweepstakes sportsbook with 1,000+ markets plus casino games."),
    "pulsz-bingo":   ("Pulsz Bingo", 4.5, ["$0.30 SC/day", "5 SC free signup", "$25 gift card min"], "Yellow Social's bingo-first platform, the natural second account for Pulsz players."),
}

# slug: (brand, alternatives [(casino_key, why_sentence)], hero_sub, intro_paras, picks, faqs)
PAGES = {
    "chumba": {
        "brand": "Chumba Casino",
        "review": "/review-chumba.html",
        "sub": "Chumba is the biggest name in sweepstakes, but it is far from the only option. These are the sites our community actually plays alongside it, ranked by daily value and payout speed.",
        "intro": [
            "Chumba Casino earned its reputation with a $10 redemption minimum, PayPal payouts, and a daily bonus that grows with your login streak. The downsides players mention most: a smaller game library than newer rivals, slower redemption processing during busy periods, and a daily bonus that starts at just $0.25 until your streak builds.",
            "The good news is that the sites below fix each of those complaints. Several match Chumba's $10 minimum while paying a bigger flat daily bonus, and a few process redemptions noticeably faster. All of them are free to join, so most of our members simply stack 3 or 4 of these alongside Chumba and collect every daily bonus."
        ],
        "alts": [
            ("mcluck", "Compared with Chumba's $0.25 starting bonus, McLuck hands you a flat $1 of SC every day from day one and matches the $10 minimum."),
            ("luckyland", "Same VGW family as Chumba, so the wallet experience and PayPal payouts feel identical, but the 10 SC welcome offer is far bigger."),
            ("crown-coins", "Community payout reports consistently rank Crown Coins faster than Chumba for cash redemptions."),
            ("zula", "Zula's $0.60 flat daily beats Chumba's early-streak rate and the lobby is more modern."),
            ("megabonanza", "Matches Chumba's $10 threshold with gift cards and pays a $1 daily bonus."),
            ("pulsz", "If Chumba's slot selection feels thin, Pulsz has 600+ premium titles and the same PayPal payout rail."),
        ],
        "picks": [
            ("Best overall Chumba alternative", "mcluck", "bigger daily bonus, same $10 minimum"),
            ("Most similar experience", "luckyland", "same VGW group and PayPal payouts"),
            ("Fastest payouts", "crown-coins", "consistently quick cash redemptions"),
        ],
        "faqs": [
            ("What is the best alternative to Chumba Casino?", "For most players it is McLuck: a flat $1 SC daily bonus from day one, a $10 redemption minimum that matches Chumba's, and 400+ games. LuckyLand Slots is the closest like-for-like swap since it is run by the same company."),
            ("Are there casinos like Chumba with faster payouts?", "Yes. Crown Coins is the standout for redemption speed in our community's payout reports, typically processing cash redemptions in 24 to 48 hours."),
            ("Can I play Chumba and these alternatives at the same time?", "Yes. Sweepstakes casinos are free to join and there is no rule against holding accounts at multiple sites. Most of our members collect daily bonuses across several platforms, which multiplies free SC without spending anything."),
        ],
    },
    "stake-us": {
        "brand": "Stake.us",
        "review": "/review-stake-us.html",
        "sub": "Stake.us dominates crypto sweepstakes, but its $1 daily and Originals games are not unique anymore. Here are the platforms closest to the Stake experience.",
        "intro": [
            "Stake.us built its lead on three things: a generous 25 SC welcome offer, crypto redemptions that land in 1 to 3 days, and exclusive Originals like Crash, Plinko, and Mines. The common complaints are the wagering requirement on bonuses, no PayPal option, and a lobby that can feel built for crypto users first.",
            "If any of that bothers you, the alternatives below cover every angle: crypto payouts without the Stake branding, the same daily-bonus value with lower minimums, and sportsbook hybrids Stake.us does not offer."
        ],
        "alts": [
            ("myprize", "The closest match to Stake's crypto DNA, but it adds bank payouts too, so you are not locked into crypto."),
            ("sportzino", "Stake.us has no sportsbook; Sportzino pairs a full casino with sports betting and matches the 25 SC signup offer."),
            ("crown-coins", "If Stake's crypto-only redemptions put you off, Crown Coins pays cash fast with a $20 minimum."),
            ("mcluck", "Matches Stake's $1 daily SC but redeems from just $10, far below Stake's effective cash-out threshold."),
            ("punt", "A crypto-friendly lobby with a higher daily bonus at 0.70 SC per day."),
            ("legendz", "Instant redemptions from $10 and a 1,500+ game library if Stake's catalog feels samey."),
        ],
        "picks": [
            ("Best overall Stake.us alternative", "myprize", "crypto payouts plus bank options"),
            ("For sports bettors", "sportzino", "casino and sportsbook in one"),
            ("Lowest cash-out threshold", "mcluck", "$1 daily and a $10 minimum"),
        ],
        "faqs": [
            ("What is the most similar casino to Stake.us?", "MyPrize is the closest in feel: crypto-native, modern lobby, VIP program. The advantage is it also supports bank payouts, which Stake.us does not."),
            ("Is there a Stake.us alternative with sports betting?", "Yes, Sportzino. It is the only sweepstakes platform that combines a full casino with a sportsbook, and its 25 SC welcome offer matches Stake's."),
            ("Do these alternatives have Stake Originals style games?", "Several have their own takes on Crash, Plinko, and Mines style games, with MyPrize and Punt closest in style. The exact titles are exclusive to Stake, but the gameplay is nearly identical."),
        ],
    },
    "pulsz": {
        "brand": "Pulsz",
        "review": "/review-pulsz.html",
        "sub": "Pulsz nails the slot selection, but its $0.30 daily bonus is one of the smaller ones. These alternatives pay more per day or redeem at lower minimums.",
        "intro": [
            "Pulsz is the slot lover's sweepstakes casino: 600+ premium titles, a 250% welcome match, and PayPal payouts in 2 to 5 days. Its weak spots are a modest $0.30 daily SC bonus and redemption minimums that sit above the cheapest competitors.",
            "Every site below either pays a bigger daily bonus, redeems at a lower minimum, or extends the Pulsz experience into a new vertical. They are all free to join, and stacking 3 or 4 of them effectively triples your daily collection rate."
        ],
        "alts": [
            ("zula", "Double Pulsz's daily rate at $0.60 SC, with a similarly polished modern lobby."),
            ("crown-coins", "Twice the daily bonus and a strong reputation for redemption speed."),
            ("mcluck", "More than three times the daily SC, and the $10 minimum undercuts Pulsz."),
            ("pulsz-bingo", "Same operator, separate wallet, so Pulsz players can claim a second daily bonus without learning a new site."),
            ("hello-millions", "A similar slots-first lobby with 400+ games and a 5 SC welcome offer."),
            ("megabonanza", "$1 daily SC with $10 gift card redemptions if Pulsz minimums feel high."),
        ],
        "picks": [
            ("Best overall Pulsz alternative", "zula", "double the daily bonus, same polish"),
            ("Easiest add-on", "pulsz-bingo", "same login, second daily bonus"),
            ("Biggest daily bonus", "mcluck", "$1 per day and a $10 minimum"),
        ],
        "faqs": [
            ("What casino is most like Pulsz?", "Zula Casino is the closest match in quality and feel, and it pays double the daily bonus at $0.60 SC. Hello Millions is the closest pure-slots equivalent."),
            ("Does Pulsz have sister sites?", "Yes. Pulsz Bingo is run by the same operator, Yellow Social Interactive, with its own separate daily bonus. Playing both is the easiest way to double your free SC from one company."),
            ("Which Pulsz alternative pays out fastest?", "Crown Coins, based on our community's tracked payout reports. Most cash redemptions there complete within 24 to 48 hours."),
        ],
    },
    "luckyland": {
        "brand": "LuckyLand Slots",
        "review": "/review-luckyland.html",
        "sub": "LuckyLand's 10 SC welcome offer and $10 minimum set the standard. These sites match or beat both, and several pay better daily bonuses.",
        "intro": [
            "LuckyLand Slots is VGW's slots specialist: a 10 SC signup offer, a $10 redemption minimum, and the same reliable PayPal rail as Chumba. Players' main gripes are a smaller game count than rivals and daily bonuses that depend on streaks rather than a flat rate.",
            "The alternatives below keep what works (low minimums, free welcome SC) and fix what does not. The B2 Group sites in particular pay a flat $1 every day, no streak required."
        ],
        "alts": [
            ("chumba", "The obvious sibling: same VGW wallet and PayPal payouts with a bigger brand and more table games."),
            ("jackpota", "A 5 SC welcome offer plus a flat $1 daily, with $10 gift card redemptions to match LuckyLand's threshold."),
            ("mcluck", "Flat $1 daily SC and a $10 cash minimum: better steady-state value than LuckyLand's streak system."),
            ("playfame", "Same B2 Group value: $1 daily, 5 SC free, 400+ games."),
            ("crown-coins", "A 10 SC welcome offer that matches LuckyLand's, with faster payouts."),
            ("funrize", "Matches the 10 SC free welcome offer if that is what drew you to LuckyLand."),
        ],
        "picks": [
            ("Most similar to LuckyLand", "chumba", "same VGW group and payout rail"),
            ("Best daily value", "mcluck", "flat $1 per day, $10 minimum"),
            ("Matching welcome offer", "crown-coins", "10 SC free plus faster payouts"),
        ],
        "faqs": [
            ("What happened to LuckyLand Slots and is it still worth playing?", "LuckyLand is still operated by VGW and remains a solid platform, especially for its 10 SC welcome offer and $10 minimum. Most players now pair it with newer sites that pay flat daily bonuses."),
            ("What is the best LuckyLand alternative?", "McLuck for ongoing value: a flat $1 SC daily bonus with the same $10 redemption minimum. Chumba Casino is the most familiar switch since both are VGW platforms."),
            ("Are these LuckyLand alternatives free?", "Yes. Every site listed is free to join with no purchase required, and each gives free SC at signup or through daily login bonuses."),
        ],
    },
    "funrize": {
        "brand": "Funrize",
        "review": "/review-funrize.html",
        "sub": "Funrize's 10 SC welcome offer is among the biggest in sweeps. These sites compete on welcome value, daily rate, or redemption minimums.",
        "intro": [
            "Funrize leads with one of the largest free welcome offers in the industry, 10 SC on signup, backed by a $0.40 daily bonus and a fish-game-heavy library of 350+ titles. The trade-offs are a $25 redemption minimum and a lobby that leans hard on TruePlay's in-house games rather than big studio slots.",
            "Below are the sites that either beat Funrize's welcome math, pay a better daily rate, or offer the mainstream slot catalogs it lacks. NoLimitCoins deserves special mention as Funrize's own sister site with a separate wallet and bonus stream."
        ],
        "alts": [
            ("nolimitcoins", "Funrize's TruePlay sister site: a second 5 SC welcome offer and daily bonus on top of your Funrize account."),
            ("crown-coins", "A matching 10 SC welcome offer plus a better daily rate at $0.60 and a lower $20 minimum."),
            ("zula", "Beats the daily rate at $0.60 SC and carries mainstream slots Funrize lacks."),
            ("mcluck", "More than double the daily bonus and a $10 minimum, well under Funrize's $25."),
            ("sweeptastic", "A similar straightforward earner with a 3 SC welcome offer and $0.50 daily."),
            ("chanced", "A $0.50 daily and 5 SC free signup with the same $25 redemption threshold."),
        ],
        "picks": [
            ("Easiest add-on", "nolimitcoins", "same operator, second bonus stream"),
            ("Best overall alternative", "crown-coins", "matches the welcome offer, beats everything else"),
            ("Biggest daily bonus", "mcluck", "$1 per day, $10 minimum"),
        ],
        "faqs": [
            ("Does Funrize have sister sites?", "Yes. NoLimitCoins (and the wider TruePlay family) is run by the same operator. Each has its own wallet, welcome offer, and daily bonus, so playing both doubles your free collection from one company."),
            ("What is the best alternative to Funrize?", "Crown Coins. It matches Funrize's 10 SC welcome offer, pays a better daily bonus at $0.60 SC, and redeems from $20 instead of $25."),
            ("Why is my Funrize redemption minimum so high?", "Funrize sets a $25 minimum for redemptions, higher than sites like McLuck or MegaBonanza at $10. If the threshold is the issue, those two are the easiest places to actually cash out small balances."),
        ],
    },
    "wow-vegas": {
        "brand": "WOW Vegas",
        "review": "/review-wow-vegas.html",
        "sub": "WOW Vegas delivers the Vegas feel, but its welcome offer and daily rate are beatable. Here is where our community goes for more value.",
        "intro": [
            "WOW Vegas stands out for its polished lobby, 500+ games, and frequent promo events. Where it loses ground is raw value: the welcome offer is 1.5 SC (small next to the 5 to 10 SC competitors give), and the $25 redemption minimum is higher than the best-in-class sites.",
            "These alternatives keep the premium-slots experience while paying you more to show up every day. Most of our members run WOW Vegas alongside two or three of them rather than replacing it outright."
        ],
        "alts": [
            ("crown-coins", "A 10 SC welcome offer versus WOW Vegas's 1.5 SC, plus a lower $20 minimum and faster payouts."),
            ("pulsz", "Even more slots (600+) with reliable PayPal payouts."),
            ("mcluck", "A $1 daily bonus and $10 minimum: much easier to actually redeem."),
            ("zula", "Comparable polish with a $0.60 daily and 5 SC welcome offer."),
            ("hello-millions", "A similar big-lobby feel with a 5 SC signup offer."),
            ("dogg-house", "Our highest-rated newer site: daily SC plus free spins and a 500+ game lobby that matches WOW Vegas's size."),
        ],
        "picks": [
            ("Best overall alternative", "crown-coins", "bigger welcome, lower minimum, faster payouts"),
            ("Most slots", "pulsz", "600+ premium titles"),
            ("Easiest to cash out", "mcluck", "$10 minimum, $1 daily"),
        ],
        "faqs": [
            ("What is the best alternative to WOW Vegas?", "Crown Coins. Its 10 SC welcome offer is several times larger than WOW Vegas's 1.5 SC, the daily bonus is bigger, and the redemption minimum is lower at $20."),
            ("Is WOW Vegas still worth playing?", "Yes, especially for its promo events and game selection. But on pure bonus math, sites like Crown Coins and McLuck pay more for the same daily login habit, so most players run them together."),
            ("Which WOW Vegas alternative has the most games?", "Pulsz, with over 600 premium slots. High 5 Casino is the overall record holder in sweepstakes at 1,000+ titles if library size is all you care about."),
        ],
    },
    "mcluck": {
        "brand": "McLuck",
        "review": "/review-mcluck.html",
        "sub": "McLuck's $1 daily and $10 minimum are hard to beat, but its B2 Group sister sites let you multiply that exact formula across several wallets.",
        "intro": [
            "McLuck is the value benchmark in sweepstakes right now: a flat $1 SC daily bonus, a 7,500 GC + 2.5 SC welcome offer, 400+ games, and a $10 redemption minimum. Honestly, there are few reasons to leave it. The smarter question is what to stack next to it.",
            "McLuck belongs to the B2 Group, which runs several near-identical platforms, each with its own wallet, welcome offer, and $1 daily bonus. Signing up across the family is the single highest-value move in sweepstakes: the same daily habit collects 4 to 5 dollars instead of one."
        ],
        "alts": [
            ("jackpota", "The top-rated B2 sister site: same $1 daily, separate wallet, 5 SC free at signup."),
            ("megabonanza", "Another B2 clone of the McLuck formula with its own 5 SC welcome offer."),
            ("playfame", "B2 Group again: $1 daily, 5 SC free, 400+ games."),
            ("spinblitz", "The B2 site with the biggest library at 800+ games, same $1 daily."),
            ("crown-coins", "The best non-B2 pairing: 10 SC welcome offer and famously fast payouts."),
            ("zula", "A polished independent alternative with a $0.60 daily and quick redemptions."),
        ],
        "picks": [
            ("First site to add", "jackpota", "highest-rated of the B2 family"),
            ("Biggest library", "spinblitz", "800+ games, same daily bonus"),
            ("Best non-B2 pairing", "crown-coins", "10 SC welcome, fast payouts"),
        ],
        "faqs": [
            ("What are McLuck's sister sites?", "McLuck is part of the B2 Group, which also runs Jackpota, MegaBonanza, PlayFame, SpinBlitz, and Hello Millions. Each has a separate wallet and its own $1-style daily bonus, so they stack."),
            ("Is it allowed to play McLuck and its sister sites together?", "Yes. Each platform is a separate site with its own account and sweepstakes rules. One account per person per site is the rule; playing five different sites is fine."),
            ("What is the best McLuck alternative outside the B2 Group?", "Crown Coins. It cannot match the $1 flat daily, but the 10 SC welcome offer is bigger and its payout speed is the best our community tracks."),
        ],
    },
    "fortune-coins": {
        "brand": "Fortune Coins",
        "review": "/review-fortune-coins.html",
        "sub": "Fortune Coins (now Fortune Wins) is a dependable daily earner. These sites beat its daily rate, lower its minimum, or extend it with sports betting.",
        "intro": [
            "Fortune Coins, recently rebranded to Fortune Wins, has been a community staple for years thanks to a $0.50 daily bonus, a fair $20 minimum, and payouts in 2 to 5 days. The knocks against it: a dated lobby, a 250+ game count that trails the big libraries, and no sportsbook.",
            "The list below includes its own corporate siblings (Zula and Sportzino share the same family), plus independents that simply pay more per day."
        ],
        "alts": [
            ("zula", "Same family, newer platform: a higher $0.60 daily and a much more modern lobby."),
            ("sportzino", "The family's sports arm: casino plus sportsbook and a 25 SC welcome offer."),
            ("crown-coins", "Higher daily ($0.60), same $20 minimum, faster payouts."),
            ("mcluck", "Double the daily bonus and a lower $10 minimum."),
            ("realprize", "A similar veteran platform with a $0.50 daily and a bigger 350+ game lobby."),
            ("nolimitcoins", "Matches the $0.50 daily and $20 minimum with a different game catalog."),
        ],
        "picks": [
            ("Best same-family upgrade", "zula", "newer, higher daily, same group"),
            ("For sports bettors", "sportzino", "adds a sportsbook to the same formula"),
            ("Best overall value", "mcluck", "$1 daily, $10 minimum"),
        ],
        "faqs": [
            ("Is Fortune Coins the same as Fortune Wins?", "Yes. Fortune Coins rebranded to Fortune Wins; accounts, balances, and the bonus structure carried over. Our review covers the rebrand in detail."),
            ("Does Fortune Coins have sister sites?", "Yes. Zula Casino and Sportzino are operated by the same family. Each has its own wallet and daily bonus, so all three stack into one daily routine."),
            ("What pays better than Fortune Coins daily?", "McLuck pays a flat $1 SC per day, double Fortune Coins' rate, with a lower $10 redemption minimum. Zula and Crown Coins both pay $0.60."),
        ],
    },
    "crown-coins": {
        "brand": "Crown Coins",
        "review": "/review-crown-coins.html",
        "sub": "Crown Coins sets the bar for payout speed. If you want more accounts with the same reliability, start with these.",
        "intro": [
            "Crown Coins earns its 4.5 rating with a 10 SC welcome offer, a $0.60 daily bonus, a $20 minimum, and the fastest redemption processing our community tracks, usually 24 to 48 hours. There is not much to fix, so think of this list as what to stack next to it.",
            "The picks below prioritize the things Crown Coins players care about: real payout reliability, meaningful daily bonuses, and welcome offers that are actually worth the signup."
        ],
        "alts": [
            ("zula", "The closest match in quality and daily rate, with a 5 SC welcome offer."),
            ("mcluck", "A higher flat daily at $1 and a lower $10 minimum."),
            ("jackpota", "B2 Group value: $1 daily and $10 gift card redemptions."),
            ("pulsz", "Adds 600+ premium slots and PayPal payouts to your rotation."),
            ("dogg-house", "Matches Crown Coins' 4.6-tier rating with daily SC plus free spins."),
            ("realprize", "A big 350+ game lobby with a $0.50 daily."),
        ],
        "picks": [
            ("Closest equivalent", "zula", "same daily rate and polish"),
            ("Best daily value add", "mcluck", "$1 flat daily, $10 minimum"),
            ("Highest rated pairing", "dogg-house", "daily SC plus free spins"),
        ],
        "faqs": [
            ("What casino is most similar to Crown Coins?", "Zula Casino: the same $0.60 daily bonus, a comparable modern lobby, and quick payouts. It is the natural second account."),
            ("Is anything faster than Crown Coins for payouts?", "Crown Coins is the fastest cash payer our community tracks. Legendz advertises instant gift card redemptions if speed matters more than cash."),
            ("Why play more than one site if Crown Coins is the best?", "Daily bonuses are per site. Adding Zula, McLuck, and Jackpota turns one $0.60 daily into roughly $3 of free SC per day for the same five minutes of logins."),
        ],
    },
    "global-poker": {
        "brand": "Global Poker",
        "review": "/review-global-poker.html",
        "sub": "Global Poker owns sweepstakes poker, but it is not the only table in town. Here is where poker players go for a second bankroll.",
        "intro": [
            "Global Poker is the biggest sweepstakes poker room in the US: real Texas Hold'em and Omaha against real opponents, daily tournaments, a $10 minimum cash out, and VGW's backing. Its limits: no casino games beyond the poker room to speak of, and one account means one bonus stream.",
            "True like-for-like poker alternatives are rare, but they exist, and several casino platforms now run poker or pair well as a side bankroll. These are the ones worth your signup."
        ],
        "alts": [
            ("clubs-poker", "The only dedicated sweepstakes poker alternative: cash games and tournaments with a daily 0.60 SC bonus Global Poker does not offer."),
            ("stake-us", "Runs poker alongside its casino, with a 25 SC welcome offer and crypto payouts."),
            ("punt", "Card-game friendly lobby and a high 0.70 SC daily to build a side bankroll."),
            ("chumba", "Same VGW wallet family, so redemptions feel identical while you collect a second daily bonus."),
            ("rebet", "Adds sports betting plus casino with a $20 minimum, a different way to use a sweeps bankroll."),
            ("myprize", "A modern lobby with VIP rewards and flexible payouts for when you want a break from the tables."),
        ],
        "picks": [
            ("Best true poker alternative", "clubs-poker", "dedicated sweeps poker with a daily bonus"),
            ("Biggest platform with poker", "stake-us", "poker plus casino plus 25 SC free"),
            ("Same company comfort", "chumba", "VGW sibling with familiar payouts"),
        ],
        "faqs": [
            ("Is there another sweepstakes poker site besides Global Poker?", "Yes. Clubs Poker is a dedicated sweepstakes poker room with cash games and tournaments, plus a 0.60 SC daily login bonus that Global Poker does not offer. Stake.us also runs poker tables alongside its casino."),
            ("Does Global Poker give a daily bonus?", "No regular daily SC bonus, which is its biggest gap versus casino sweeps sites. Pairing it with Clubs Poker and a couple of daily-bonus casinos keeps free SC flowing on days you do not buy in."),
            ("Can I use my Global Poker account on Chumba or LuckyLand?", "Accounts are separate, but all three are VGW platforms, so signup, verification, and PayPal redemptions work the same way. You will need to register at each site individually."),
        ],
    },
}


def stars(rating):
    full = int(round(rating))
    return "&#9733;" * full + "&#9734;" * (5 - full)


def card(key, why):
    name, rating, chips, base = CASINOS[key]
    chip_html = "".join(f'<span class="meta-chip">{c}</span>' for c in chips)
    return f'''  <div class="casino-card">
    <div class="casino-name">{name}</div>
    <div class="casino-meta">
      {chip_html}
    </div>
    <p class="casino-desc">{base} {why}</p>
    <div class="casino-footer">
      <div class="rating">
        <span class="stars">{stars(rating)}</span>
        <span class="rating-text">{rating} / 5</span>
      </div>
      <a href="/review-{key}.html" class="signup-btn">Read Our {name} Review &#8594;</a>
    </div>
  </div>
'''


EXTRA_CSS = """<style>
.alt-intro{background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:1.4rem 1.6rem;margin-bottom:2rem;}
.alt-intro p{color:var(--text-dim);line-height:1.8;font-size:.95rem;}
.alt-intro p + p{margin-top:.9rem;}
.alt-section-title{font-size:1.3rem;font-weight:800;color:#fff;margin:2.4rem 0 1rem;}
.alt-section-title span{color:var(--teal);}
.picks-list{background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:1.2rem 1.5rem;margin-bottom:1rem;}
.picks-list li{color:var(--text-dim);line-height:2;list-style:none;}
.picks-list strong{color:#fff;}
.picks-list a{color:var(--teal);text-decoration:none;}
.faq-item{background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:1.1rem 1.4rem;margin-bottom:.8rem;}
.faq-item h3{color:#fff;font-size:1rem;margin-bottom:.5rem;}
.faq-item p{color:var(--text-dim);line-height:1.75;font-size:.92rem;}
</style>
"""


template = open("new-sites.html", encoding="utf-8").read()
head_part, rest = template.split("<!-- CASINO: KICKR -->", 1)
_, tail_part = rest.split("<!-- COMING SOON -->", 1)
tail_part = "<!-- CROSSLINKS -->" + tail_part.split("</div>", 1)[1]  # drop coming-soon inner

for slug, page in PAGES.items():
    brand = page["brand"]
    fname = f"casinos-like-{slug}.html"
    clean = f"/casinos-like-{slug}"
    n = len(page["alts"])
    title = f"Casinos Like {brand}: {n} Best Alternatives 2026"
    desc = f"Looking for casinos like {brand}? We compare the {n} best {brand} alternatives for 2026 by daily bonuses, welcome offers, and redemption minimums."

    h = head_part
    h = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", h, flags=re.S)
    h = re.sub(r'<meta name="description" content=".*?"', f'<meta name="description" content="{desc}"', h, flags=re.S)
    h = h.replace('<link rel="canonical" href="https://onlinesidehustles.info/new-sites">',
                  f'<link rel="canonical" href="{SITE}{clean}">')
    h = re.sub(r'<meta property="og:url" content=".*?"', f'<meta property="og:url" content="{SITE}{clean}"', h)
    h = re.sub(r'<meta property="og:title" content=".*?"', f'<meta property="og:title" content="{title}"', h)
    h = re.sub(r'<meta property="og:description" content=".*?"', f'<meta property="og:description" content="{desc}"', h)
    h = re.sub(r'<meta name="twitter:title" content=".*?"', f'<meta name="twitter:title" content="{title}"', h)
    h = re.sub(r'<meta name="twitter:description" content=".*?"', f'<meta name="twitter:description" content="{desc}"', h)

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Casino Reviews", "item": f"{SITE}/casino-reviews"},
                {"@type": "ListItem", "position": 3, "name": f"Casinos Like {brand}", "item": f"{SITE}{clean}"},
            ]},
            {"@type": "ItemList", "name": title, "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": CASINOS[k][0],
                 "url": f"{SITE}/review-{k}.html"}
                for i, (k, _) in enumerate(page["alts"])
            ]},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in page["faqs"]
            ]},
        ],
    }
    h = re.sub(r'<script type="application/ld\+json">.*?</script>',
               '<script type="application/ld+json">\n' + json.dumps(schema, indent=1) + "\n</script>",
               h, flags=re.S)

    h = h.replace("</head>", EXTRA_CSS + "</head>")
    h = h.replace("<h1>New Sweepstakes<br><span>Casino Sites</span></h1>",
                  f"<h1>Casinos Like<br><span>{brand}</span></h1>")
    h = re.sub(r'<p class="hero-sub">.*?</p>', f'<p class="hero-sub">{page["sub"]}</p>', h, flags=re.S)
    h = h.replace('<a href="/sweepstakes" class="back-link">&#8592; Back to Sweepstakes Hub</a>',
                  '<a href="/casino-reviews" class="back-link">&#8592; Back to Casino Reviews</a>')

    intro = '<div class="alt-intro">\n' + "\n".join(f"    <p>{p}</p>" for p in page["intro"]) + "\n  </div>\n"
    cards = "".join(card(k, why) for k, why in page["alts"])

    picks = '<h2 class="alt-section-title">Which <span>Alternative</span> Fits You</h2>\n  <ul class="picks-list">\n'
    for label, k, reason in page["picks"]:
        picks += f'    <li><strong>{label}:</strong> <a href="/review-{k}.html">{CASINOS[k][0]}</a> ({reason})</li>\n'
    picks += "  </ul>\n"

    faq = '<h2 class="alt-section-title">Casinos Like ' + brand + ': <span>FAQ</span></h2>\n'
    for q, a in page["faqs"]:
        faq += f'  <div class="faq-item">\n    <h3>{q}</h3>\n    <p>{a}</p>\n  </div>\n'

    cross = f'''  <div class="coming-soon">
    <p>&#128204; <strong>Want the full picture?</strong><br>
    Read our complete <a href="{page["review"]}">{brand} review</a>, browse all <a href="/casino-reviews">126+ casino reviews</a>, or see every site ranked on the <a href="/sweepstakes-casino-list">sweepstakes casino list</a>. New platforms land on <a href="/new-sites">new sites</a> first.</p>
  </div>
'''

    body = intro + cards + "\n  " + picks + "\n  " + faq + "\n" + cross
    out = h + body + tail_part
    open(fname, "w", encoding="utf-8", newline="\n").write(out)
    print(f"wrote {fname} ({len(out)} bytes)")

print("done:", len(PAGES), "pages")
