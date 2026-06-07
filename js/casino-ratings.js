/* ==========================================================================
   Online Sidehustles — Community Casino Ratings
   Single source of truth for the rating widget, the blended-score model, and
   the Google Apps Script backend connection. Used by the list page AND every
   review-*.html page so a vote anywhere counts toward the same score.

   SCORING MODEL ("editorial rating is king, community only nudges"):
     Each casino starts from an artificial "house" rating based on its editorial
     tier (a strong prior). Real community votes are blended in, but the house
     rating carries a large weight, so the crowd can only move the score
     slightly — and higher tiers resist movement more than lower ones.

       displayed = (SEED[tier]*SEED_WEIGHT[tier] + communityWeightedSum)
                   ---------------------------------------------------------
                            (SEED_WEIGHT[tier] + communityWeightedWeight)

     Low votes are de-weighted to blunt trolling: a 1-star vote counts ~0.3 of
     a normal vote, a 2-star ~0.6, and 3/4/5-star count fully.

     Tiers stay locked to your editorial order (Daily Casinos List sheet) — the
     community score is shown next to the name but never reorders the tiers.

   SETUP: paste the deployed Apps Script /exec URL into ENDPOINT below.
   ========================================================================== */
(function () {
  'use strict';

  var CFG = {
    ENDPOINT: 'https://script.google.com/macros/s/AKfycbzPbH1tgaYiQ1xBgAG0QfTMt4KqBy7VhSWyxN74dSuG3reewr0DmfrDGcdRVdhgpYrZLA/exec',

    // Each casino's own editorial review score is the anchor (see EDITORIAL
    // below). These tier values are only a FALLBACK for casinos that have no
    // review page (S=God, A=High, B=Medium). NEW with no review = community-only.
    SEED: { S: 5.0, A: 4.85, B: 4.7 },

    // How strongly the editorial anchor resists community movement (phantom
    // votes). Flat across casinos so the blend is identical everywhere.
    WEIGHT: 130,

    // Anti-troll: weight applied to each star value when accumulating votes.
    // 1- and 2-star votes count less than 3/4/5-star votes.
    LOW_STAR_WEIGHT: { 1: 0.3, 2: 0.6, 3: 1.0, 4: 1.0, 5: 1.0 },

    JSONP_TIMEOUT_MS: 12000
  };

  // Per-casino editorial review scores (the anchor). Keyed by normalized name.
  // Generated from review pages by build_editorial_anchors.py — keep in sync
  // with casino-ratings/editorial-scores.json.
  var EDITORIAL = {"acebetcc": 4.2, "acecasino": 4.5, "acornfun": 4.1, "americanluck": 4.5, "babacasino": 4.0, "bangcoins": 4.2, "bankrolla": 4.1, "betr": 4.5, "cardcrush": 4.1, "casinoclick": 4.5, "cazino": 4.3, "chancedcom": 4.7, "chipnwin": 4.3, "chumbacasino": 4.8, "clubspoker": 4.5, "cluck": 4.0, "coinfrenzy": 4.4, "coinsback": 4.5, "coinwizardgames": 4.1, "courtside": 4.3, "crashduel": 4.4, "crowncoins": 4.8, "daracasino": 4.3, "dexyplay": 4.3, "diambet": 4.3, "dimesweeps": 4.6, "dogghousecasino": 4.8, "epicsweep": 4.4, "fliff": 4.7, "fortunarush": 4.5, "fortunewheelz": 4.4, "fortunewins": 4.7, "funrize": 4.6, "funzcity": 4.2, "getzoot": 4.2, "globalpoker": 4.7, "goldenheartsgames": 4.6, "goldrushcity": 4.2, "goldtreasurecasino": 4.4, "goodvibescasino": 4.3, "hellomillions": 4.7, "high5casino": 4.6, "jackpota": 4.8, "jackpotdaily": 4.5, "jackpotgo": 4.5, "jackpotrabbit": 4.3, "jefebet": 4.3, "lavishluck": 4.5, "legacyarcade": 4.5, "legendz": 4.4, "lonestar": 4.7, "lucklake": 4.4, "luckparty": 4.3, "luckybird": 4.5, "luckybitsvegas": 4.3, "luckyhands": 4.7, "luckylandslots": 4.7, "luckyrush": 4.6, "luckyslots": 4.3, "luckystake": 4.4, "lunalandcasino": 4.3, "mcluck": 4.7, "megabonanza": 4.8, "megafrenzy": 4.3, "megaspinz": 4.3, "modo": 4.5, "moonspin": 4.6, "moozi": 4.5, "myprize": 4.7, "nioplay": 4.1, "nolimitcoins": 4.6, "novig": 4.5, "oceanking": 4.4, "peakplay": 4.4, "playfame": 4.8, "pulsz": 4.8, "pulszbingo": 4.8, "puntcasino": 4.6, "realprize": 4.7, "rebet": 4.8, "richsweeps": 4.5, "rolla": 4.5, "rollingriches": 4.5, "rubysweeps": 4.4, "scarletsands": 4.4, "scoopcasino": 4.4, "scroogecasino": 4.3, "sheeshcasino": 4.1, "shuffleus": 4.9, "sidepot": 4.3, "sixty6": 4.3, "smilescasino": 4.3, "sorceryreels": 4.3, "speedsweeps": 4.7, "spinblitz": 4.7, "spindoo": 4.2, "spinfinite": 4.3, "spinpals": 4.3, "spinquest": 4.2, "spinsaga": 4.4, "sportzino": 4.8, "spree": 4.5, "stackr": 4.3, "stakeus": 4.9, "sweepico": 4.4, "sweepjungle": 4.5, "sweepnext": 4.3, "sweepshark": 4.3, "sweepsroyal": 4.6, "sweeptastic": 4.5, "sweetsweeps": 4.3, "taofortune": 4.5, "taosweeps": 4.3, "thebossus": 4.3, "themoneyfactory": 4.5, "thrillcoins": 4.6, "thrillz": 4.6, "vegawin": 4.1, "wildworldcasino": 4.2, "winbonanza": 4.5, "winera": 4.1, "wowvegas": 4.6, "yaycasino": 4.4, "zonko": 4.0, "zula": 4.8, "zumo": 4.3};

  var enabled = !!CFG.ENDPOINT;

  function normName(n) {
    return String(n || '').toLowerCase().replace(/[^a-z0-9]/g, '');
  }

  function starWeight(stars) {
    var w = CFG.LOW_STAR_WEIGHT[stars];
    return (w === undefined) ? 1.0 : w;
  }

  // Normalize a tier label ("God Tier", "S", "high", …) to S/A/B/NEW.
  function tierCode(t) {
    if (!t) return 'NEW';
    var s = String(t).toUpperCase();
    if (s === 'S' || s === 'A' || s === 'B' || s === 'NEW') return s;
    var l = String(t).toLowerCase();
    if (l.indexOf('god') !== -1) return 'S';
    if (l.indexOf('high') !== -1) return 'A';
    if (l.indexOf('medium') !== -1 || l.indexOf('med') !== -1) return 'B';
    return 'NEW';
  }

  // RATINGS[normKey] = { n:name, cs:weightedSum, cw:weightedWeight, c:rawVotes }
  var RATINGS = {};

  // Blend a casino's editorial review score (anchor) with community votes.
  // anchor = its own review score if it has one, else the tier fallback.
  // Returns { value:Number, votes:Number, seeded:Boolean }.
  function blendedRating(tier, r, name) {
    var cs = r ? (r.cs || 0) : 0;
    var cw = r ? (r.cw || 0) : 0;
    var votes = r ? (r.c || 0) : 0;
    var anchor = EDITORIAL[normName(name)];
    if (anchor === undefined) anchor = CFG.SEED[tierCode(tier)]; // tier fallback (no review page)
    if (anchor === undefined) {
      return { value: cw > 0 ? cs / cw : 0, votes: votes, seeded: false }; // community-only
    }
    return { value: (anchor * CFG.WEIGHT + cs) / (CFG.WEIGHT + cw), votes: votes, seeded: true };
  }

  // ---- JSONP transport (no CORS issues with Apps Script) ------------------
  var _cb = 0;
  function jsonp(params) {
    return new Promise(function (resolve, reject) {
      if (!CFG.ENDPOINT) { reject(new Error('ratings endpoint not configured')); return; }
      var name = 'oshr_cb_' + (++_cb) + '_' + Date.now();
      var script = document.createElement('script');
      var qs = [];
      for (var k in params) {
        if (params.hasOwnProperty(k)) qs.push(encodeURIComponent(k) + '=' + encodeURIComponent(params[k]));
      }
      qs.push('callback=' + name);
      qs.push('t=' + Date.now());
      var done = false;
      function cleanup() { try { delete window[name]; } catch (e) { window[name] = undefined; } if (script.parentNode) script.parentNode.removeChild(script); }
      window[name] = function (data) { done = true; cleanup(); resolve(data); };
      script.onerror = function () { if (!done) { cleanup(); reject(new Error('jsonp network error')); } };
      setTimeout(function () { if (!done) { cleanup(); reject(new Error('jsonp timeout')); } }, CFG.JSONP_TIMEOUT_MS);
      script.src = CFG.ENDPOINT + '?' + qs.join('&');
      document.head.appendChild(script);
    });
  }

  function load() {
    if (!enabled) return Promise.resolve(RATINGS);
    return jsonp({ action: 'list' }).then(function (data) {
      if (data && data.ratings) {
        var r = data.ratings;
        for (var k in r) { if (r.hasOwnProperty(k)) RATINGS[k] = r[k]; }
      }
      return RATINGS;
    }).catch(function (e) {
      console.warn('[OSHRatings] load failed:', e.message);
      return RATINGS;
    });
  }

  function get(name) { return RATINGS[normName(name)] || null; }

  // ---- per-device vote memory --------------------------------------------
  function voteKey(name) { return 'oshvote_' + normName(name); }
  function myVote(name) {
    try { var v = localStorage.getItem(voteKey(name)); return v ? parseInt(v, 10) : 0; } catch (e) { return 0; }
  }
  function setMyVote(name, stars) { try { localStorage.setItem(voteKey(name), String(stars)); } catch (e) {} }

  function vote(name, stars) {
    stars = parseInt(stars, 10);
    if (!enabled || !(stars >= 1 && stars <= 5)) return Promise.reject(new Error('invalid vote'));
    var prev = myVote(name);
    setMyVote(name, stars);
    return jsonp({ action: 'vote', casino: name, key: normName(name), stars: stars, prev: prev || '' })
      .then(function (res) {
        if (res && res.ok) {
          RATINGS[normName(name)] = { n: res.n || name, cs: res.cs, cw: res.cw, c: res.c };
        }
        return res;
      });
  }

  // ---- widget rendering ---------------------------------------------------
  function esc(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // opts: { compact:Boolean, tier:String }  tier drives the house seed.
  function widgetHTML(name, opts) {
    opts = opts || {};
    var tier = tierCode(opts.tier);
    var br = blendedRating(tier, get(name), name);
    var mine = myVote(name);
    var filled = Math.round(br.value);
    var stars = '';
    for (var v = 5; v >= 1; v--) {
      var on = v <= filled ? ' oshr-on' : '';
      var youOn = mine && v <= mine ? ' oshr-mine' : '';
      stars += '<button type="button" class="oshr-star' + on + youOn + '" data-v="' + v +
        '" aria-label="Rate ' + v + ' out of 5">★</button>';
    }
    var meta;
    if (br.value > 0) {
      meta = '<b>' + br.value.toFixed(1) + '</b>';
      if (br.votes > 0) meta += '<span class="oshr-n">(' + br.votes + ')</span>';
      if (mine) meta += '<span class="oshr-you">you ' + mine + '★</span>';
    } else {
      meta = mine ? '<span class="oshr-you">you ' + mine + '★</span>'
                  : '<span class="oshr-first">Rate it</span>';
    }
    return '<span class="oshr' + (opts.compact ? ' oshr-compact' : '') + '" data-c="' + esc(name) +
      '" data-t="' + esc(tier) + '">' +
      '<span class="oshr-stars" role="radiogroup" aria-label="Community rating for ' + esc(name) + '">' +
      stars + '</span><span class="oshr-meta">' + meta + '</span></span>';
  }

  function refresh(el) {
    if (!el) return;
    var name = el.getAttribute('data-c');
    var tier = el.getAttribute('data-t') || 'NEW';
    var compact = el.classList.contains('oshr-compact');
    var tmp = document.createElement('div');
    tmp.innerHTML = widgetHTML(name, { compact: compact, tier: tier });
    el.innerHTML = tmp.firstChild.innerHTML;
  }

  function attach(root, onVoted) {
    if (!enabled || !root || root._oshrAttached) return;
    root._oshrAttached = true;
    root.addEventListener('click', function (ev) {
      var star = ev.target.closest ? ev.target.closest('.oshr-star') : null;
      if (!star || !root.contains(star)) return;
      var widget = star.closest('.oshr');
      if (!widget || widget.classList.contains('oshr-busy')) return;
      var name = widget.getAttribute('data-c');
      var stars = parseInt(star.getAttribute('data-v'), 10);
      widget.classList.add('oshr-busy');
      refresh(widget);
      vote(name, stars).then(function (res) {
        widget.classList.remove('oshr-busy');
        if (onVoted) onVoted(name, res, widget); else refresh(widget);
      }).catch(function (e) {
        widget.classList.remove('oshr-busy');
        refresh(widget);
        console.warn('[OSHRatings] vote failed:', e.message);
      });
    });
  }

  function injectCSS() {
    if (document.getElementById('oshr-css')) return;
    var css = [
      '.oshr{display:inline-flex;align-items:center;gap:.4rem;font-family:inherit;line-height:1;}',
      '.oshr-stars{display:inline-flex;flex-direction:row-reverse;gap:1px;}',
      '.oshr-star{background:none;border:0;padding:0 1px;margin:0;cursor:pointer;font-size:1.02rem;color:#3a4860;transition:color .12s;line-height:1;}',
      '.oshr-star.oshr-on{color:#f5b301;}',
      '.oshr-star.oshr-mine{color:#6ee7b7;}',
      '.oshr-stars:hover .oshr-star{color:#3a4860;}',
      '.oshr-stars:hover .oshr-star:hover,.oshr-stars:hover .oshr-star:hover ~ .oshr-star{color:#ffd23f;}',
      '.oshr-busy .oshr-star{cursor:progress;opacity:.6;}',
      '.oshr-meta{font-size:.72rem;color:#9fb0c8;display:inline-flex;align-items:baseline;gap:.26rem;white-space:nowrap;}',
      '.oshr-meta b{color:#f5b301;font-size:.8rem;}',
      '.oshr-n{opacity:.7;}',
      '.oshr-you{color:#6ee7b7;font-size:.64rem;}',
      '.oshr-first{color:#9fb0c8;font-size:.7rem;font-style:italic;}',
      '.oshr-compact{gap:.32rem;}',
      '.oshr-compact .oshr-star{font-size:.9rem;}',
      '.oshr-compact .oshr-meta{font-size:.64rem;}',
      /* In the casino name cell on the list */
      '.name-cell .oshr{margin:5px 0 2px;}',
      /* Larger review-page card */
      '.oshr-card{margin:1.4rem 0;padding:1.1rem 1.25rem;border:1px solid rgba(245,179,1,.22);background:rgba(245,179,1,.05);border-radius:12px;text-align:center;}',
      '.oshr-card h3{margin:0 0 .15rem;font-size:1.05rem;}',
      '.oshr-card .oshr-sub{margin:0 0 .7rem;font-size:.82rem;color:#9fb0c8;}',
      '.oshr-card .oshr-star{font-size:1.7rem;padding:0 2px;}',
      '.oshr-card .oshr-meta{font-size:.95rem;margin-top:.5rem;justify-content:center;}',
      '.oshr-card .oshr{flex-direction:column;gap:.5rem;}',
      '.oshr-thanks{color:#6ee7b7;font-size:.8rem;min-height:1em;margin-top:.4rem;}'
    ].join('');
    var st = document.createElement('style');
    st.id = 'oshr-css';
    st.textContent = css;
    document.head.appendChild(st);
  }
  if (document.readyState !== 'loading') injectCSS();
  else document.addEventListener('DOMContentLoaded', injectCSS);

  window.OSHRatings = {
    CFG: CFG,
    enabled: enabled,
    normName: normName,
    tierCode: tierCode,
    blendedRating: blendedRating,
    RATINGS: RATINGS,
    load: load,
    get: get,
    vote: vote,
    myVote: myVote,
    widgetHTML: widgetHTML,
    refresh: refresh,
    attach: attach
  };
})();
