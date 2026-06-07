/* ==========================================================================
   Online Sidehustles — Community Casino Ratings backend (Google Apps Script)

   Stores user star ratings in a "Ratings" tab of your casino spreadsheet.
   Low (1-2 star) votes are de-weighted to blunt trolling. The website blends
   these community numbers with an editorial "house" rating per tier, so the
   crowd can only nudge the score (see js/casino-ratings.js).

   Stored per casino:
     WeightedSum     = Σ stars_i * weight(stars_i)
     WeightedWeight  = Σ weight(stars_i)
     Votes           = raw number of votes
     CommunityAvg    = WeightedSum / WeightedWeight  (for your own insight)

   Deploy as a Web App (Execute as: Me, Who has access: Anyone). All requests
   arrive via JSONP GET (?callback=...) so there are zero CORS problems.
   ========================================================================== */

var SPREADSHEET_ID = '1a202Ul8JDL21ikdYet9ieUeTKHFAsDTXLm2HIkI4328';
var SHEET_NAME = 'Ratings';

// Anti-troll weighting — keep in sync with js/casino-ratings.js LOW_STAR_WEIGHT.
var LOW_STAR_WEIGHT = { 1: 0.3, 2: 0.6, 3: 1.0, 4: 1.0, 5: 1.0 };

var COL = { KEY: 1, NAME: 2, WSUM: 3, WWEIGHT: 4, VOTES: 5, AVG: 6, UPDATED: 7 };
var HEADERS = ['NormKey', 'Casino', 'WeightedSum', 'WeightedWeight', 'Votes', 'CommunityAvg', 'LastUpdated'];

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
  // Self-heal: make sure the header row matches the current schema.
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
      wsum = stars * w;
      wweight = w;
      votes = 1;
      rowIndex = (last < 1 ? 1 : last) + 1;
      writeRow(sh, rowIndex, key, name, wsum, wweight, votes);
    } else {
      wsum = Number(sh.getRange(rowIndex, COL.WSUM).getValue()) || 0;
      wweight = Number(sh.getRange(rowIndex, COL.WWEIGHT).getValue()) || 0;
      votes = Number(sh.getRange(rowIndex, COL.VOTES).getValue()) || 0;
      if (isChange && votes >= 1) {
        var pw = starWeight(prev);
        wsum = wsum - prev * pw + stars * w; // same voter changed their mind
        wweight = wweight - pw + w;
        if (wweight < w) wweight = w; // guard against drift
      } else {
        wsum = wsum + stars * w;
        wweight = wweight + w;
        votes = votes + 1;
      }
      var existingName = String(sh.getRange(rowIndex, COL.NAME).getValue() || '');
      writeRow(sh, rowIndex, key, existingName || name, wsum, wweight, votes);
    }

    return {
      ok: true,
      n: String(sh.getRange(rowIndex, COL.NAME).getValue() || name),
      cs: round2(wsum),
      cw: round2(wweight),
      c: votes
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
