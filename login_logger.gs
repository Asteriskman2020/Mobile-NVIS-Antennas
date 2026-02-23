// ═══════════════════════════════════════════════════════════════════
//  HS2GJG Project Gallery — Login Logger & Password Recovery
//  Deploy as Google Apps Script Web App
// ═══════════════════════════════════════════════════════════════════
const RECIPIENT  = 'jakkrit.kunthong@gmail.com';
const PASSWORD   = 'hs2gjg73';
const SITE_NAME  = 'HS2GJG Project Gallery';
const SHEET_NAME = 'LoginLog';

// ── Handle incoming POST requests ────────────────────────────────
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
  } catch (err) {
    return jsonReply({status:'error', message:'Invalid JSON'});
  }

  var sheet = getOrCreateSheet();
  var now = new Date();
  var ts  = Utilities.formatDate(now, 'Asia/Bangkok', 'yyyy-MM-dd HH:mm:ss');

  // ── Password Recovery ──
  if (data.action === 'recover') {
    var email = data.email || '';
    if (email.toLowerCase() !== RECIPIENT.toLowerCase()) {
      sheet.appendRow([ts, 'RECOVERY_DENIED', email, 'Email mismatch']);
      return jsonReply({status:'denied', message:'Email not recognized'});
    }
    MailApp.sendEmail({
      to: RECIPIENT,
      subject: '[' + SITE_NAME + '] Password Recovery',
      htmlBody:
        '<div style="font-family:Arial;max-width:500px;margin:auto;padding:24px;background:#0a0e1a;color:#e0e8f0;border-radius:16px">' +
        '<h2 style="color:#00e5ff;margin-top:0">Password Recovery</h2>' +
        '<p>Your password is:</p>' +
        '<div style="background:#121830;padding:16px;border-radius:12px;text-align:center;font-size:24px;font-weight:bold;letter-spacing:3px;color:#ffd600;border:1px solid #ffd600">' +
        PASSWORD + '</div>' +
        '<p style="color:#7888a0;font-size:13px;margin-top:16px">Requested: ' + ts + '<br>Browser: ' + (data.ua || 'N/A') + '</p>' +
        '<hr style="border-color:#222">' +
        '<p style="color:#556;font-size:11px">' + SITE_NAME + ' — Automated message</p></div>'
    });
    sheet.appendRow([ts, 'RECOVERY_SENT', email, 'Password emailed']);
    return jsonReply({status:'ok', message:'Password sent to your email'});
  }

  // ── Login Attempt Logging ──
  var type = data.success ? 'LOGIN_OK' : 'LOGIN_FAIL';
  sheet.appendRow([ts, type, data.ua || '', data.detail || '']);
  return jsonReply({status:'ok'});
}

function doGet(e) {
  return ContentService.createTextOutput('HS2GJG Login Logger Active')
    .setMimeType(ContentService.MimeType.TEXT);
}

// ── Daily Summary Email (triggered at noon) ──────────────────────
function sendDailySummary() {
  var sheet = getOrCreateSheet();
  var data  = sheet.getDataRange().getValues();
  var now   = new Date();
  var cutoff = new Date(now.getTime() - 24 * 60 * 60 * 1000);

  var ok = 0, fail = 0, recovered = 0, denied = 0;
  var rows = [];

  for (var i = 1; i < data.length; i++) {
    var ts = new Date(data[i][0]);
    if (ts >= cutoff) {
      var t = data[i][1];
      if (t === 'LOGIN_OK')         ok++;
      else if (t === 'LOGIN_FAIL')  fail++;
      else if (t === 'RECOVERY_SENT')   recovered++;
      else if (t === 'RECOVERY_DENIED') denied++;
      rows.push('<tr><td style="padding:6px 10px;border:1px solid #333">' +
        Utilities.formatDate(ts, 'Asia/Bangkok', 'HH:mm:ss') + '</td><td style="padding:6px 10px;border:1px solid #333">' +
        t + '</td><td style="padding:6px 10px;border:1px solid #333">' +
        (data[i][3] || '') + '</td></tr>');
    }
  }

  var total = ok + fail + recovered + denied;
  var html =
    '<div style="font-family:Arial;max-width:600px;margin:auto;padding:24px;background:#0a0e1a;color:#e0e8f0;border-radius:16px">' +
    '<h2 style="color:#00e5ff;margin-top:0">' + SITE_NAME + '</h2>' +
    '<h3 style="color:#ffd600">Daily Login Summary</h3>' +
    '<p style="color:#7888a0">' + Utilities.formatDate(now, 'Asia/Bangkok', 'yyyy-MM-dd') + ' (last 24 hours)</p>' +
    '<table style="width:100%;border-collapse:collapse;margin:16px 0">' +
    '<tr style="background:#1565c0"><td style="padding:10px;color:#fff;font-weight:bold">Metric</td>' +
    '<td style="padding:10px;color:#fff;font-weight:bold;text-align:center">Count</td></tr>' +
    '<tr style="background:#1b5e20"><td style="padding:10px;color:#a5d6a7">Successful Logins</td>' +
    '<td style="padding:10px;text-align:center;font-size:20px;font-weight:bold;color:#76ff03">' + ok + '</td></tr>' +
    '<tr style="background:#b71c1c"><td style="padding:10px;color:#ef9a9a">Failed Attempts</td>' +
    '<td style="padding:10px;text-align:center;font-size:20px;font-weight:bold;color:#ff4081">' + fail + '</td></tr>' +
    '<tr style="background:#0d47a1"><td style="padding:10px;color:#90caf9">Password Recoveries</td>' +
    '<td style="padding:10px;text-align:center;font-size:20px;font-weight:bold;color:#00e5ff">' + recovered + '</td></tr>' +
    '<tr style="background:#4a148c"><td style="padding:10px;color:#ce93d8">Recovery Denied</td>' +
    '<td style="padding:10px;text-align:center;font-size:20px;font-weight:bold;color:#e040fb">' + denied + '</td></tr>' +
    '<tr style="background:#263238"><td style="padding:10px;color:#b0bec5;font-weight:bold">Total Events</td>' +
    '<td style="padding:10px;text-align:center;font-size:20px;font-weight:bold;color:#ffd600">' + total + '</td></tr>' +
    '</table>';

  if (rows.length > 0) {
    html += '<h4 style="color:#ff9100">Event Log</h4>' +
      '<table style="width:100%;border-collapse:collapse;font-size:12px">' +
      '<tr style="background:#37474f"><td style="padding:6px 10px;color:#fff;font-weight:bold">Time</td>' +
      '<td style="padding:6px 10px;color:#fff;font-weight:bold">Type</td>' +
      '<td style="padding:6px 10px;color:#fff;font-weight:bold">Detail</td></tr>' +
      rows.join('') + '</table>';
  } else {
    html += '<p style="color:#556">No login events in the last 24 hours.</p>';
  }

  html += '<hr style="border-color:#222;margin-top:20px">' +
    '<p style="color:#445;font-size:11px">' + SITE_NAME + ' — Automated daily summary</p></div>';

  MailApp.sendEmail({
    to: RECIPIENT,
    subject: '[' + SITE_NAME + '] Daily Login Summary — ' +
      Utilities.formatDate(now, 'Asia/Bangkok', 'yyyy-MM-dd'),
    htmlBody: html
  });
}

// ── Setup: run ONCE to create daily noon trigger ─────────────────
function setupDailyTrigger() {
  // Remove any existing triggers
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    ScriptApp.deleteTrigger(triggers[i]);
  }
  // Create daily trigger at noon (Bangkok time)
  ScriptApp.newTrigger('sendDailySummary')
    .timeBased()
    .atHour(12)
    .everyDays(1)
    .inTimezone('Asia/Bangkok')
    .create();
  Logger.log('Daily summary trigger created for 12:00 noon (Asia/Bangkok)');
}

// ── Helper ───────────────────────────────────────────────────────
function getOrCreateSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.appendRow(['Timestamp', 'Type', 'Info', 'Details']);
    sheet.getRange('1:1').setFontWeight('bold');
    sheet.setColumnWidth(1, 160);
    sheet.setColumnWidth(2, 140);
    sheet.setColumnWidth(3, 250);
    sheet.setColumnWidth(4, 250);
  }
  return sheet;
}

function jsonReply(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
