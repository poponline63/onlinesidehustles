/* ==========================================================================
   Online Sidehustles — Community Casino Ratings backend (Google Apps Script)

   Stores user star ratings in a "Ratings" tab of your casino spreadsheet and
   serves running averages + a computed community tier back to the website.

   Deploy as a Web App (Execute as: Me, Who has access: Anyone). See SETUP.md.

   All requests come in via JSONP GET (?callback=...) so there are zero CORS
   problems from onlinesidehustles.info.
   ========================================================================== */

// Your existing casino spreadsheet (same one the list page reads).
var SPREADSHEET_ID = '1a202Ul8JDL21ikdYet9ieUeTKHFAsDTXLm2HIkI4328';
var SHEET_NAME = 'Ratings';

// Average (1-5) -> tier. Keep in sync with js/casino-ratings.js CFG.
var THRESHOLDS = [[4.5, 'S'], [3.8, 'A'], [2.5, 'B']];
var NEW_TIER = 'NEW';

// Columns in the Ratings sheet.
var COL = { KEY: 1, NAME: 2, SUM: 3, COUNT: 4, AVG: 5, TIER: 6, UPDATED: 7 };
var HEADERS = ['NormKey', 'Casino', 'Sum', 'Count', 'Average', 'CommunityTier', 'LastUpdated'];

function doGet(e) {
  var params = (e && e.params) ? e.params : ((e && e.parameter) ? e.parameter : {});
  // GAS gives single values in e.parameter; normalize.
  var p = (e && e.parameter) ? e.parameter : {};
  var action = (p.action || 'list').toLowerCase();
  var callback = p.callback || '';

  var result;
  try {
    if (action === 'vote') {
      result = handleVote(p);
    } else {
      result = handleList();
    }
  } catch (err) {
    result = { ok: false, error: String(err) };
  }
  return respond(result, callback);
}

function respond(obj, callback) {
  var json = JSON.stringify(obj);
  if (callback) {
    return ContentService
      .createTextOutput(callback + '(' + json + ');')
      .setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return ContentService
    .createTextOutput(json)
    .setMimeType(ContentService.MimeType.JSON);
}

function getSheet() {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
    sh.setFrozenRows(1);
  }
  return sh;
}

function normName(n) {
  return String(n || '').toLowerCase().replace(/[^a-z0-9]/g, '');
}

function scoreToTier(avg) {
  for (var i = 0; i < THRESHOLDS.length; i++) {
    if (avg >= THRESHOLDS[i][0]) return THRESHOLDS[i][1];
  }
  return NEW_TIER;
}

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
      var count = Number(row[COL.COUNT - 1]) || 0;
      var avg = Number(row[COL.AVG - 1]) || 0;
      out[key] = {
        n: String(row[COL.NAME - 1] || ''),
        a: Math.round(avg * 100) / 100,
        c: count,
        t: String(row[COL.TIER - 1] || '')
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

    var sum, count;
    if (rowIndex === -1) {
      // New casino row.
      sum = stars;
      count = 1;
      rowIndex = (last < 1 ? 1 : last) + 1;
      writeRow(sh, rowIndex, key, name, sum, count);
    } else {
      sum = Number(sh.getRange(rowIndex, COL.SUM).getValue()) || 0;
      count = Number(sh.getRange(rowIndex, COL.COUNT).getValue()) || 0;
      if (isChange && count >= 1) {
        sum = sum - prev + stars; // same voter changed their mind: count unchanged
      } else {
        sum = sum + stars;
        count = count + 1;
      }
      var existingName = String(sh.getRange(rowIndex, COL.NAME).getValue() || '');
      writeRow(sh, rowIndex, key, existingName || name, sum, count);
    }

    var avg = count > 0 ? sum / count : 0;
    return {
      ok: true,
      n: String(sh.getRange(rowIndex, COL.NAME).getValue() || name),
      a: Math.round(avg * 100) / 100,
      c: count,
      t: scoreToTier(avg)
    };
  } finally {
    lock.releaseLock();
  }
}

function writeRow(sh, rowIndex, key, name, sum, count) {
  var avg = count > 0 ? sum / count : 0;
  sh.getRange(rowIndex, 1, 1, HEADERS.length).setValues([[
    key, name, sum, count, Math.round(avg * 100) / 100, scoreToTier(avg), new Date()
  ]]);
}
