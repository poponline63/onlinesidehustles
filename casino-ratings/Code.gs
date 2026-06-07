/* ==========================================================================
   Online Sidehustles — Community Casino Ratings backend (Google Apps Script)

   1) Web App (doGet): stores/serves community votes in the "Ratings" tab.
      Low (1-2 star) votes are de-weighted to blunt trolling.
   2) syncRatingsToList(): stamps the blended rating ("house" seed per tier +
      community votes) as a 2nd line under each casino name in the
      "Daily Casinos List" tab. Runs hourly via a trigger, and from a menu.

   Ratings tab columns:
     WeightedSum = Σ stars_i*weight(stars_i)   WeightedWeight = Σ weight(stars_i)
     Votes = raw count   CommunityAvg = WeightedSum/WeightedWeight

   Deploy as a Web App (Execute as: Me, Who has access: Anyone). Run setup()
   once to populate the list + install the hourly trigger.
   ========================================================================== */

var SPREADSHEET_ID = '1yJAKLouHPn3AvV2PKEhulepc6HQ4uj9hfEPkl3WaMog';
var SHEET_NAME = 'Ratings';
var LIST_SHEET_NAME = 'Daily Casinos List';

// Anti-troll weighting — keep in sync with js/casino-ratings.js LOW_STAR_WEIGHT.
var LOW_STAR_WEIGHT = { 1: 0.3, 2: 0.6, 3: 1.0, 4: 1.0, 5: 1.0 };

// Per-casino editorial review scores (the anchor). Tier SEED is only a fallback
// for casinos with no review page. Flat WEIGHT so the blend matches the website
// and the daily updater. Keep EDITORIAL in sync with editorial-scores.json.
var SEED = { S: 5.0, A: 4.8, B: 4.6, NEW: 4.5 };          // NEW = community-only (no seed)
var WEIGHT = 55;   // ~55 votes one tier off moves a casino's score across a tier boundary
var EDITORIAL = {"acebetcc": 4.5, "acecasino": 4.5, "acornfun": 4.6, "americanluck": 4.8, "babacasino": 4.6, "bangcoins": 4.5, "bankrolla": 4.5, "betr": 4.5, "cardcrush": 4.6, "casinoclick": 5.0, "cazino": 4.6, "chancedcom": 4.6, "chipnwin": 4.6, "chumbacasino": 4.6, "clubspoker": 4.6, "cluck": 4.6, "coinfrenzy": 4.5, "coinsback": 4.5, "coinwizardgames": 4.5, "courtside": 4.5, "crashduel": 4.0, "crowncoins": 5.0, "daracasino": 4.6, "dexyplay": 4.5, "diambet": 4.5, "dimesweeps": 4.8, "dogghousecasino": 4.5, "epicsweep": 4.5, "fliff": 4.8, "fortunarush": 4.5, "fortunewheelz": 4.6, "fortunewins": 4.6, "funrize": 4.6, "funzcity": 4.6, "getzoot": 4.6, "globalpoker": 5.0, "goldenheartsgames": 4.8, "goldrushcity": 5.0, "goldtreasurecasino": 5.0, "goodvibescasino": 4.6, "hellomillions": 4.6, "high5casino": 4.6, "jackpota": 4.6, "jackpotdaily": 4.5, "jackpotgo": 4.5, "jackpotrabbit": 4.6, "jefebet": 4.6, "lavishluck": 4.6, "legacyarcade": 4.5, "legendz": 4.8, "lonestar": 5.0, "lucklake": 4.5, "luckparty": 4.5, "luckybird": 4.0, "luckybitsvegas": 5.0, "luckyhands": 4.6, "luckylandslots": 5.0, "luckyrush": 4.5, "luckyslots": 4.6, "luckystake": 4.6, "lunalandcasino": 4.6, "mcluck": 4.6, "megabonanza": 4.6, "megafrenzy": 4.6, "megaspinz": 4.5, "modo": 4.6, "moonspin": 4.8, "moozi": 4.6, "myprize": 5.0, "nioplay": 5.0, "nolimitcoins": 4.6, "novig": 4.5, "oceanking": 4.5, "peakplay": 4.6, "playfame": 4.6, "pulsz": 5.0, "pulszbingo": 5.0, "puntcasino": 4.5, "realprize": 5.0, "rebet": 4.8, "richsweeps": 4.8, "rolla": 5.0, "rollingriches": 4.6, "rubysweeps": 4.8, "scarletsands": 5.0, "scoopcasino": 4.5, "scroogecasino": 4.5, "sheeshcasino": 4.6, "shuffleus": 4.6, "sidepot": 4.8, "sixty6": 4.8, "smilescasino": 4.6, "sorceryreels": 4.6, "speedsweeps": 4.8, "spinblitz": 4.6, "spindoo": 5.0, "spinfinite": 4.6, "spinpals": 5.0, "spinquest": 4.6, "spinsaga": 5.0, "sportzino": 5.0, "spree": 4.6, "stackr": 5.0, "stakeus": 5.0, "sweepico": 4.5, "sweepjungle": 4.5, "sweepnext": 4.8, "sweepshark": 4.6, "sweepsroyal": 4.6, "sweeptastic": 4.5, "sweetsweeps": 4.5, "taofortune": 4.6, "taosweeps": 4.5, "thebossus": 4.5, "themoneyfactory": 4.6, "thrillcoins": 4.5, "thrillz": 4.5, "vegawin": 4.5, "wildworldcasino": 4.6, "winbonanza": 4.5, "winera": 4.5, "wowvegas": 5.0, "yaycasino": 5.0, "zonko": 4.5, "zula": 5.0, "zumo": 4.5};

var COL = { KEY: 1, NAME: 2, WSUM: 3, WWEIGHT: 4, VOTES: 5, AVG: 6, UPDATED: 7 };
var HEADERS = ['NormKey', 'Casino', 'WeightedSum', 'WeightedWeight', 'Votes', 'CommunityAvg', 'LastUpdated'];

/* ---------- Web app ---------- */

function doGet(e) {
  var p = (e && e.parameter) ? e.parameter : {};
  var action = (p.action || 'list').toLowerCase();
  var callback = p.callback || '';
  var result;
  try {
    result = (action === 'vote') ? handleVote(p) : handleList();
  } catch (err) {
    result = { ok: false, error: String(err) };
  }
  return respond(result, callback);
}

function respond(obj, callback) {
  var json = JSON.stringify(obj);
  if (callback) {
    return ContentService.createTextOutput(callback + '(' + json + ');')
      .setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return ContentService.createTextOutput(json)
    .setMimeType(ContentService.MimeType.JSON);
}

function getSheet() {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
    sh.setFrozenRows(1);
    return sh;
  }
  var hdr = sh.getRange(1, 1, 1, HEADERS.length).getValues()[0];
  var ok = true;
  for (var i = 0; i < HEADERS.length; i++) { if (String(hdr[i]) !== HEADERS[i]) { ok = false; break; } }
  if (!ok) {
    sh.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
    sh.setFrozenRows(1);
  }
  return sh;
}

function normName(n) {
  return String(n || '').toLowerCase().replace(/[^a-z0-9]/g, '');
}

function starWeight(stars) {
  var w = LOW_STAR_WEIGHT[stars];
  return (w === undefined) ? 1.0 : w;
}

function round2(x) { return Math.round(x * 100) / 100; }

function handleList() {
  var sh = getSheet();
  var last = sh.getLastRow();
  var out = {};
  if (last >= 2) {
    var values = sh.getRange(2, 1, last - 1, HEADERS.length).getValues();
    for (var i = 0; i < values.length; i++) {
      var row = values[i];
      var key = String(row[COL.KEY - 1] || '');
      if (!key) continue;
      out[key] = {
        n: String(row[COL.NAME - 1] || ''),
        cs: Number(row[COL.WSUM - 1]) || 0,
        cw: Number(row[COL.WWEIGHT - 1]) || 0,
        c: Number(row[COL.VOTES - 1]) || 0
      };
    }
  }
  return { ok: true, ratings: out };
}

function handleVote(p) {
  var stars = parseInt(p.stars, 10);
  if (!(stars >= 1 && stars <= 5)) return { ok: false, error: 'invalid stars' };
  var name = String(p.casino || '').trim();
  var key = normName(p.key || name);
  if (!key) return { ok: false, error: 'missing casino' };
  var prev = parseInt(p.prev, 10);
  var isChange = (prev >= 1 && prev <= 5);
  var w = starWeight(stars);

  var lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    var sh = getSheet();
    var last = sh.getLastRow();
    var rowIndex = -1;
    if (last >= 2) {
      var keys = sh.getRange(2, COL.KEY, last - 1, 1).getValues();
      for (var i = 0; i < keys.length; i++) {
        if (String(keys[i][0]) === key) { rowIndex = i + 2; break; }
      }
    }

    var wsum, wweight, votes;
    if (rowIndex === -1) {
      wsum = stars * w; wweight = w; votes = 1;
      rowIndex = (last < 1 ? 1 : last) + 1;
      writeRow(sh, rowIndex, key, name, wsum, wweight, votes);
    } else {
      wsum = Number(sh.getRange(rowIndex, COL.WSUM).getValue()) || 0;
      wweight = Number(sh.getRange(rowIndex, COL.WWEIGHT).getValue()) || 0;
      votes = Number(sh.getRange(rowIndex, COL.VOTES).getValue()) || 0;
      if (isChange && votes >= 1) {
        var pw = starWeight(prev);
        wsum = wsum - prev * pw + stars * w;
        wweight = wweight - pw + w;
        if (wweight < w) wweight = w;
      } else {
        wsum = wsum + stars * w; wweight = wweight + w; votes = votes + 1;
      }
      var existingName = String(sh.getRange(rowIndex, COL.NAME).getValue() || '');
      writeRow(sh, rowIndex, key, existingName || name, wsum, wweight, votes);
    }

    return {
      ok: true,
      n: String(sh.getRange(rowIndex, COL.NAME).getValue() || name),
      cs: round2(wsum), cw: round2(wweight), c: votes
    };
  } finally {
    lock.releaseLock();
  }
}

function writeRow(sh, rowIndex, key, name, wsum, wweight, votes) {
  var avg = wweight > 0 ? wsum / wweight : 0;
  sh.getRange(rowIndex, 1, 1, HEADERS.length).setValues([[
    key, name, round2(wsum), round2(wweight), votes, round2(avg), new Date()
  ]]);
}

/* ---------- Stamp ratings under each name in Daily Casinos List ---------- */

function blendedValue(tierCode, r, key) {
  var cs = r ? (r.cs || 0) : 0, cw = r ? (r.cw || 0) : 0;
  var anchor = EDITORIAL[key];                       // per-casino review score
  if (anchor === undefined) anchor = SEED[tierCode]; // tier fallback (no review)
  if (anchor === undefined) return (cw > 0) ? (cs / cw) : null; // community-only
  return (anchor * WEIGHT + cs) / (WEIGHT + cw);
}

function tierFromLabel(label) {
  var l = String(label || '').toLowerCase();
  if (l.indexOf('god tier') !== -1) return 'S';
  if (l.indexOf('high tier') !== -1) return 'A';
  if (l.indexOf('medium tier') !== -1) return 'B';
  if (l.indexOf('trash') !== -1) return 'SKIP';
  if (l.indexOf('new website') !== -1 || l.indexOf('new casino') !== -1) return 'NEW';
  return null;
}

// Remove any previously-stamped rating line(s); return the base name.
function stripRatingLines(text) {
  var parts = String(text || '').split('\n');
  var keep = [];
  for (var i = 0; i < parts.length; i++) {
    var t = parts[i].trim();
    if (t.charAt(0) === '★' || t.charAt(0) === '☆') continue; // ★ or ☆
    keep.push(parts[i]);
  }
  return keep.join('\n').trim();
}

function ratingLine(tierCode, r, key) {
  var votes = r ? (r.c || 0) : 0;
  var val = blendedValue(tierCode, r, key);
  if (val === null) return '☆ no votes yet'; // ☆
  return '★ ' + (Math.round(val * 10) / 10).toFixed(1) + (votes > 0 ? ' (' + votes + ')' : '');
}

function getListSheet(ss) {
  // Find the sheet that actually contains "Signup" rows (robust against tab
  // renames / sheet order), falling back to name then first sheet.
  var all = ss.getSheets();
  for (var i = 0; i < all.length; i++) {
    var sh = all[i];
    if (sh.getName() === SHEET_NAME) continue;
    var lr = sh.getLastRow();
    if (lr < 2) continue;
    var col = sh.getRange(1, 1, Math.min(lr, 300), 1).getValues();
    for (var r = 0; r < col.length; r++) {
      if (String(col[r][0] || '').toLowerCase().indexOf('signup') !== -1) return sh;
    }
  }
  return ss.getSheetByName(LIST_SHEET_NAME) || all[0];
}

function syncRatingsToList() {
  setupRankingTabs();   // ensure the frozen Editorial Anchor exists (idempotent)
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var list = getListSheet(ss);
  var last = list.getLastRow();
  if (last < 1) return;
  var ratings = handleList().ratings;
  var aVals = list.getRange(1, 1, last, 1).getValues();
  var bVals = list.getRange(1, 2, last, 1).getValues();

  var currentTier = 'NEW';
  var stamped = 0;
  for (var r = 0; r < last; r++) {
    if (r === 0) continue; // skip the header row ("Signups"/"Casinos")
    var a = String(aVals[r][0] || '');
    var bRaw = String(bVals[r][0] || '');
    var bFirst = bRaw.split('\n')[0].trim();
    var isSignup = a.toLowerCase().indexOf('signup') !== -1;

    if (!isSignup) {
      var t = tierFromLabel(bFirst);
      if (t) currentTier = t;
      continue;
    }
    if (!bFirst) continue;

    var base = stripRatingLines(bRaw);
    if (!base) continue;
    var key = normName(base);
    var line = ratingLine(currentTier, ratings[key], key);
    var newVal = base + '\n' + line;
    if (newVal !== bRaw) {
      list.getRange(r + 1, 2).setValue(newVal);
      stamped++;
    }
  }
  reorderByRatings();   // then physically move rows into their rating-based tiers
  return stamped;
}

// NOTE: The hourly auto-refresh is set up via the Apps Script Triggers UI
// (clock icon -> Add Trigger -> syncRatingsToList -> Time-driven -> Hour timer).
// We intentionally do NOT create the trigger in code, so the project only needs
// the spreadsheet scope (no extra script.scriptapp consent prompt).
// To refresh manually, just Run syncRatingsToList from the editor.

/* ---------- Community-driven row reordering (test on a copy first) ----------
   Casinos physically move between tier sections based on their rating. Baselines
   are read from a FROZEN "Editorial Anchor" tab, never from the live order, so
   there is no feedback loop. Only casino rows (col A = "signup") are moved; the
   link-less trash sites at the bottom are left untouched. moveRows relocates the
   whole row so image formulas / formatting come along.                        */

var ANCHOR_SHEET_NAME = 'Editorial Anchor';

// Tier band lower edges + ranking, and a hysteresis dead-band so a casino does
// not flip-flop between tiers when its score hovers on a boundary.
var TIER_LOWER = { S: 4.90, A: 4.70, B: 4.55, NEW: 4.25, SKIP: 0 };
var TIER_RANK  = { SKIP: 0, NEW: 1, B: 2, A: 3, S: 4 };
var HYSTERESIS = 0.03;

// Which tier a blended score earns — mirror of the website's tierFromScore.
function tierFromScore(score, editorial) {
  if (score === null || score === undefined) return editorial;
  if (score >= 4.90) return 'S';                              // God
  if (score >= 4.70) return 'A';                              // High
  if (score >= 4.55) return 'B';                              // Medium
  return (editorial === 'NEW') ? 'NEW' : (editorial === 'SKIP' ? 'SKIP' : 'B');
}

// Target tier with hysteresis: only leave the current tier once the score is
// clearly (>= HYSTERESIS) past the boundary, so the sheet does not churn hourly.
function targetTier(score, anchor, current) {
  if (score === null || score === undefined) return current || anchor;
  var raw = tierFromScore(score, anchor);
  if (!current || raw === current) return raw;
  if (TIER_RANK[raw] > TIER_RANK[current]) {                 // moving up
    return (score >= TIER_LOWER[raw] + HYSTERESIS) ? raw : current;
  }
  return (score <= TIER_LOWER[current] - HYSTERESIS) ? raw : current;  // moving down
}

// One-time: freeze the current editorial order into an "Editorial Anchor" tab.
// The reorderer reads baselines from here, never from the live (reordered)
// order, so moving rows on the live list can never feed back on the scores.
function setupRankingTabs() {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var leftover = ss.getSheetByName('TEST Rankings'); if (leftover) ss.deleteSheet(leftover);
  if (!ss.getSheetByName(ANCHOR_SHEET_NAME)) { getListSheet(ss).copyTo(ss).setName(ANCHOR_SHEET_NAME); }
  return 'anchor ready';
}

// Each casino's frozen baseline tier, read from the anchor sheet (keyed by name).
function readAnchorTiers(ss) {
  var sh = ss.getSheetByName(ANCHOR_SHEET_NAME);
  var map = {};
  if (!sh) return map;
  var last = sh.getLastRow();
  var aV = sh.getRange(1, 1, last, 1).getValues();
  var bV = sh.getRange(1, 2, last, 1).getValues();
  var cur = 'NEW';
  for (var r = 0; r < last; r++) {
    var a = String(aV[r][0] || '');
    var bFull = String(bV[r][0] || '');
    var b = bFull.split('\n')[0].trim();
    if (a.toLowerCase().indexOf('signup') === -1) { var t = tierFromLabel(b); if (t) cur = t; continue; }
    if (!b) continue;
    map[normName(stripRatingLines(bFull))] = cur;
  }
  return map;
}

// Scan a sheet: first separator row per tier + casino rows with their section.
function scanList(sheet) {
  var last = sheet.getLastRow();
  var aV = sheet.getRange(1, 1, last, 1).getValues();
  var bV = sheet.getRange(1, 2, last, 1).getValues();
  var sepRow = {}, cur = null, casinos = [];
  for (var r = 0; r < last; r++) {
    var a = String(aV[r][0] || '');
    var bFull = String(bV[r][0] || '');
    var b = bFull.split('\n')[0].trim();
    if (a.toLowerCase().indexOf('signup') === -1) {
      var t = tierFromLabel(b);
      if (t) { cur = t; if (sepRow[t] === undefined) sepRow[t] = r + 1; }
      continue;
    }
    if (!b) continue;
    casinos.push({ row: r + 1, section: cur, key: normName(stripRatingLines(bFull)), name: b });
  }
  return { sepRow: sepRow, casinos: casinos };
}

// Reorder casino rows into rating-based tiers. overrides {key:tier} forces a
// target (used by the test harness). Moves one row at a time, re-scanning each
// time because row indices shift after every move.
function reorderByRatings(sheetName, overrides) {
  overrides = overrides || {};
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var sheet = sheetName ? ss.getSheetByName(sheetName) : getListSheet(ss);
  if (!sheet) return { error: 'no sheet: ' + sheetName };
  var anchors = readAnchorTiers(ss);
  var ratings = handleList().ratings;
  var width = sheet.getMaxColumns();

  var s = scanList(sheet);
  var moves = [];
  for (var i = 0; i < s.casinos.length; i++) {
    var c = s.casinos[i];
    if (!c.section) continue;
    var anchor = anchors[c.key] || c.section;
    var target = overrides[c.key] || targetTier(blendedValue(anchor, ratings[c.key], c.key), anchor, c.section);
    if (target && target !== c.section) moves.push({ key: c.key, name: c.name, from: c.section, to: target });
  }

  var applied = 0, log = [];
  for (var m = 0; m < moves.length; m++) {
    var sc = scanList(sheet);
    var cur = null;
    for (var j = 0; j < sc.casinos.length; j++) { if (sc.casinos[j].key === moves[m].key) { cur = sc.casinos[j]; break; } }
    if (!cur) continue;
    var sep = sc.sepRow[moves[m].to];
    if (sep === undefined) continue;
    // Land just under the target separator. Moving down, the row vacates first
    // (shifting indices up), so the pre-move destination index needs +2.
    var dest = (cur.row < sep) ? sep + 2 : sep + 1;
    sheet.moveRows(sheet.getRange(cur.row, 1, 1, width), dest);
    applied++;
    log.push(moves[m].name + ' ' + moves[m].from + '->' + moves[m].to);
  }
  return { planned: moves.length, applied: applied, moves: log };
}

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Casino Ratings')
    .addItem('Sync ratings to list now', 'syncRatingsToList')
    .addToUi();
}
