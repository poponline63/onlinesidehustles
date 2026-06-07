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

var SPREADSHEET_ID = '1a202Ul8JDL21ikdYet9ieUeTKHFAsDTXLm2HIkI4328';
var SHEET_NAME = 'Ratings';
var LIST_SHEET_NAME = 'Daily Casinos List';

// Anti-troll weighting — keep in sync with js/casino-ratings.js LOW_STAR_WEIGHT.
var LOW_STAR_WEIGHT = { 1: 0.3, 2: 0.6, 3: 1.0, 4: 1.0, 5: 1.0 };

// Per-casino editorial review scores (the anchor). Tier SEED is only a fallback
// for casinos with no review page. Flat WEIGHT so the blend matches the website
// and the daily updater. Keep EDITORIAL in sync with editorial-scores.json.
var SEED = { S: 5.0, A: 4.85, B: 4.7 };          // NEW = community-only (no seed)
var WEIGHT = 130;
var EDITORIAL = {"acebetcc": 4.2, "acecasino": 4.5, "acornfun": 4.1, "americanluck": 4.5, "babacasino": 4.0, "bangcoins": 4.2, "bankrolla": 4.1, "betr": 4.5, "cardcrush": 4.1, "casinoclick": 4.5, "cazino": 4.3, "chancedcom": 4.7, "chipnwin": 4.3, "chumbacasino": 4.8, "clubspoker": 4.5, "cluck": 4.0, "coinfrenzy": 4.4, "coinsback": 4.5, "coinwizardgames": 4.1, "courtside": 4.3, "crashduel": 4.4, "crowncoins": 4.8, "daracasino": 4.3, "dexyplay": 4.3, "diambet": 4.3, "dimesweeps": 4.6, "dogghousecasino": 4.8, "epicsweep": 4.4, "fliff": 4.7, "fortunarush": 4.5, "fortunewheelz": 4.4, "fortunewins": 4.7, "funrize": 4.6, "funzcity": 4.2, "getzoot": 4.2, "globalpoker": 4.7, "goldenheartsgames": 4.6, "goldrushcity": 4.2, "goldtreasurecasino": 4.4, "goodvibescasino": 4.3, "hellomillions": 4.7, "high5casino": 4.6, "jackpota": 4.8, "jackpotdaily": 4.5, "jackpotgo": 4.5, "jackpotrabbit": 4.3, "jefebet": 4.3, "lavishluck": 4.5, "legacyarcade": 4.5, "legendz": 4.4, "lonestar": 4.7, "lucklake": 4.4, "luckparty": 4.3, "luckybird": 4.5, "luckybitsvegas": 4.3, "luckyhands": 4.7, "luckylandslots": 4.7, "luckyrush": 4.6, "luckyslots": 4.3, "luckystake": 4.4, "lunalandcasino": 4.3, "mcluck": 4.7, "megabonanza": 4.8, "megafrenzy": 4.3, "megaspinz": 4.3, "modo": 4.5, "moonspin": 4.6, "moozi": 4.5, "myprize": 4.7, "nioplay": 4.1, "nolimitcoins": 4.6, "novig": 4.5, "oceanking": 4.4, "peakplay": 4.4, "playfame": 4.8, "pulsz": 4.8, "pulszbingo": 4.8, "puntcasino": 4.6, "realprize": 4.7, "rebet": 4.8, "richsweeps": 4.5, "rolla": 4.5, "rollingriches": 4.5, "rubysweeps": 4.4, "scarletsands": 4.4, "scoopcasino": 4.4, "scroogecasino": 4.3, "sheeshcasino": 4.1, "shuffleus": 4.9, "sidepot": 4.3, "sixty6": 4.3, "smilescasino": 4.3, "sorceryreels": 4.3, "speedsweeps": 4.7, "spinblitz": 4.7, "spindoo": 4.2, "spinfinite": 4.3, "spinpals": 4.3, "spinquest": 4.2, "spinsaga": 4.4, "sportzino": 4.8, "spree": 4.5, "stackr": 4.3, "stakeus": 4.9, "sweepico": 4.4, "sweepjungle": 4.5, "sweepnext": 4.3, "sweepshark": 4.3, "sweepsroyal": 4.6, "sweeptastic": 4.5, "sweetsweeps": 4.3, "taofortune": 4.5, "taosweeps": 4.3, "thebossus": 4.3, "themoneyfactory": 4.5, "thrillcoins": 4.6, "thrillz": 4.6, "vegawin": 4.1, "wildworldcasino": 4.2, "winbonanza": 4.5, "winera": 4.1, "wowvegas": 4.6, "yaycasino": 4.4, "zonko": 4.0, "zula": 4.8, "zumo": 4.3};

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
  return stamped;
}

// NOTE: The hourly auto-refresh is set up via the Apps Script Triggers UI
// (clock icon -> Add Trigger -> syncRatingsToList -> Time-driven -> Hour timer).
// We intentionally do NOT create the trigger in code, so the project only needs
// the spreadsheet scope (no extra script.scriptapp consent prompt).
// To refresh manually, just Run syncRatingsToList from the editor.

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Casino Ratings')
    .addItem('Sync ratings to list now', 'syncRatingsToList')
    .addToUi();
}
