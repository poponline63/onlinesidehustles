import sys, os
sys.stdout.reconfigure(encoding='utf-8')

fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sweepstakes-casino-list.html')
c = open(fpath, encoding='utf-8').read()
changes = []

# ─────────────────────────────────────────────────────────────────
# 1. CSS: Default column widths (8 cols → 8 cols, Daily SC removed)
#    Old: Casino(20%) Tier(4%) DailySC(6%) Daily$(8%) Welcome(11%)
#         MinRedeem(6%) Notes(31%) Parent(13%)
#    New: Casino(21%) Tier(4%) Daily$(8%) Welcome(12%) MinRedeem(7%)
#         Notes(31%) Parent(11%) Review(6%)   → total 100%
# ─────────────────────────────────────────────────────────────────
old_widths = """/* Column widths — default 8 cols, no horizontal scroll */
#mainTable th:nth-child(1),#mainTable td:nth-child(1){width:20%;}  /* Casino+Signup */
#mainTable th:nth-child(2),#mainTable td:nth-child(2){width:4%;}   /* Tier */
#mainTable th:nth-child(3),#mainTable td:nth-child(3){width:6%;}   /* Daily SC */
#mainTable th:nth-child(4),#mainTable td:nth-child(4){width:8%;}   /* Daily $ */
#mainTable th:nth-child(5),#mainTable td:nth-child(5){width:11%;}  /* Welcome Pkg */
#mainTable th:nth-child(6),#mainTable td:nth-child(6){width:6%;}   /* Min Redeem */
#mainTable th:nth-child(7),#mainTable td:nth-child(7){width:31%;}  /* Notes */
#mainTable th:nth-child(8),#mainTable td:nth-child(8){width:13%;}  /* Parent Company */"""

new_widths = """/* Column widths — 8 cols (no Daily SC), fits PC screen without scroll */
#mainTable th:nth-child(1),#mainTable td:nth-child(1){width:21%;}  /* Casino+Signup */
#mainTable th:nth-child(2),#mainTable td:nth-child(2){width:4%;}   /* Tier */
#mainTable th:nth-child(3),#mainTable td:nth-child(3){width:8%;}   /* Daily $ */
#mainTable th:nth-child(4),#mainTable td:nth-child(4){width:12%;}  /* Welcome Pkg */
#mainTable th:nth-child(5),#mainTable td:nth-child(5){width:7%;}   /* Min Redeem */
#mainTable th:nth-child(6),#mainTable td:nth-child(6){width:31%;}  /* Notes */
#mainTable th:nth-child(7),#mainTable td:nth-child(7){width:11%;}  /* Parent Company */
#mainTable th:nth-child(8),#mainTable td:nth-child(8){width:6%;}   /* Review */"""

if old_widths in c:
    c = c.replace(old_widths, new_widths)
    changes.append('CSS default column widths updated (8 cols, Daily SC removed)')
else:
    print('[WARN] Default column widths not found — already updated?')

# ─────────────────────────────────────────────────────────────────
# 2. CSS: Canada mode column widths (11 cols → 10 cols, Daily SC removed)
#    Old: Casino Tier DailySC Daily$ Welcome MinRedeem Notes CA ON Parent
#    New: Casino Tier Daily$ Welcome MinRedeem Notes CA ON Parent Review
# ─────────────────────────────────────────────────────────────────
old_ca = """/* Canada mode — 10 cols (shrink notes/parent to fit 🇨🇦 + ON) */
#mainTable.ca-mode th:nth-child(1),#mainTable.ca-mode td:nth-child(1){width:17%;}
#mainTable.ca-mode th:nth-child(2),#mainTable.ca-mode td:nth-child(2){width:4%;}
#mainTable.ca-mode th:nth-child(3),#mainTable.ca-mode td:nth-child(3){width:5%;}
#mainTable.ca-mode th:nth-child(4),#mainTable.ca-mode td:nth-child(4){width:7%;}
#mainTable.ca-mode th:nth-child(5),#mainTable.ca-mode td:nth-child(5){width:10%;}
#mainTable.ca-mode th:nth-child(6),#mainTable.ca-mode td:nth-child(6){width:5%;}
#mainTable.ca-mode th:nth-child(7),#mainTable.ca-mode td:nth-child(7){width:26%;}
#mainTable.ca-mode th:nth-child(8),#mainTable.ca-mode td:nth-child(8){width:10%;}
#mainTable.ca-mode th:nth-child(9),#mainTable.ca-mode td:nth-child(9){width:8%;}
#mainTable.ca-mode th:nth-child(10),#mainTable.ca-mode td:nth-child(10){width:8%;}"""

new_ca = """/* Canada mode — 10 cols (no Daily SC, fits screen) */
#mainTable.ca-mode th:nth-child(1),#mainTable.ca-mode td:nth-child(1){width:18%;}
#mainTable.ca-mode th:nth-child(2),#mainTable.ca-mode td:nth-child(2){width:4%;}
#mainTable.ca-mode th:nth-child(3),#mainTable.ca-mode td:nth-child(3){width:7%;}
#mainTable.ca-mode th:nth-child(4),#mainTable.ca-mode td:nth-child(4){width:10%;}
#mainTable.ca-mode th:nth-child(5),#mainTable.ca-mode td:nth-child(5){width:6%;}
#mainTable.ca-mode th:nth-child(6),#mainTable.ca-mode td:nth-child(6){width:27%;}
#mainTable.ca-mode th:nth-child(7),#mainTable.ca-mode td:nth-child(7){width:8%;}
#mainTable.ca-mode th:nth-child(8),#mainTable.ca-mode td:nth-child(8){width:8%;}
#mainTable.ca-mode th:nth-child(9),#mainTable.ca-mode td:nth-child(9){width:8%;}
#mainTable.ca-mode th:nth-child(10),#mainTable.ca-mode td:nth-child(10){width:4%;}"""

if old_ca in c:
    c = c.replace(old_ca, new_ca)
    changes.append('CSS ca-mode column widths updated (10 cols, Daily SC removed)')
else:
    print('[WARN] ca-mode widths not found')

# ─────────────────────────────────────────────────────────────────
# 3. Static HTML <thead> — remove Daily SC, CA, ON columns
#    (JS replaces this immediately anyway, but fix for pre-load state)
# ─────────────────────────────────────────────────────────────────
old_thead = """            <tr>
              <th onclick="sortBy('name')">Casino <span class="th-sort">↕</span></th>
              <th onclick="sortBy('tier')">Tier <span class="th-sort">↕</span></th>
              <th onclick="sortBy('daily')">Daily SC</th>
              <th onclick="sortBy('amt')">Daily $ <span class="th-sort">↕</span></th>
              <th>Welcome Package</th>
              <th onclick="sortBy('redeem')">Min.<br>Redeem <span class="th-sort">↕</span></th>
              <th class="notes-cell">Notes</th>
              <th>🇨🇦</th>
              <th>ON</th>
              <th>Parent Company</th>
              <th>Review</th>
            </tr>"""

new_thead = """            <tr>
              <th onclick="sortBy('name')">Casino <span class="th-sort">↕</span></th>
              <th onclick="sortBy('tier')">Tier <span class="th-sort">↕</span></th>
              <th onclick="sortBy('amt')">Daily $ <span class="th-sort">↕</span></th>
              <th>Welcome Package</th>
              <th onclick="sortBy('redeem')">Min.<br>Redeem <span class="th-sort">↕</span></th>
              <th class="notes-cell">Notes</th>
              <th>Parent Company</th>
              <th>Review</th>
            </tr>"""

if old_thead in c:
    c = c.replace(old_thead, new_thead)
    changes.append('Static <thead> updated (Daily SC removed, CA/ON removed from static HTML)')
else:
    print('[WARN] Static thead not found — checking repr...')
    idx = c.find("Daily SC</th>")
    if idx != -1:
        print('  Found "Daily SC</th>" at index', idx, ':', repr(c[max(0,idx-100):idx+50]))

# ─────────────────────────────────────────────────────────────────
# 4. JS updateTableHeader() — remove Daily SC from dynamic header
# ─────────────────────────────────────────────────────────────────
old_dynhead = """      <th onclick="sortBy('name')">Casino <span class="th-sort">↕</span></th>
      <th onclick="sortBy('tier')">Tier <span class="th-sort">↕</span></th>
      <th onclick="sortBy('daily')">Daily SC</th>
      <th onclick="sortBy('amt')">Daily $ <span class="th-sort">↕</span></th>"""

new_dynhead = """      <th onclick="sortBy('name')">Casino <span class="th-sort">↕</span></th>
      <th onclick="sortBy('tier')">Tier <span class="th-sort">↕</span></th>
      <th onclick="sortBy('amt')">Daily $ <span class="th-sort">↕</span></th>"""

if old_dynhead in c:
    c = c.replace(old_dynhead, new_dynhead)
    changes.append('JS updateTableHeader() — Daily SC column removed from dynamic header')
else:
    print('[WARN] Dynamic header Daily SC line not found')

# ─────────────────────────────────────────────────────────────────
# 5. JS renderTable() — fix colCount (remove Daily SC from count)
# ─────────────────────────────────────────────────────────────────
old_colcount = "  const colCount = gameplayMode ? 9 : (showCa ? 11 : 9);"
new_colcount = "  const colCount = gameplayMode ? 9 : (showCa ? 10 : 8);"

if old_colcount in c:
    c = c.replace(old_colcount, new_colcount)
    changes.append('colCount fixed: default 8, CA mode 10, gameplay 9')
else:
    print('[WARN] colCount line not found')
    idx = c.find('colCount')
    if idx != -1:
        print('  Found colCount at:', repr(c[max(0,idx-10):idx+60]))

# ─────────────────────────────────────────────────────────────────
# 6. JS renderTable() row builder — remove dailyBadge TD
# ─────────────────────────────────────────────────────────────────
old_row = """      tr.innerHTML=nameCell+`
      <td>${tierBadge(c.tier)}</td>
      <td>${dailyBadge(c.daily)}</td>
      <td><span class="daily-val" title="${c.dailyRaw||''}">${esc(c.dailyRaw)||'—'}</span></td>"""

new_row = """      tr.innerHTML=nameCell+`
      <td>${tierBadge(c.tier)}</td>
      <td><span class="daily-val" title="${c.dailyRaw||''}">${esc(c.dailyRaw)||'—'}</span></td>"""

if old_row in c:
    c = c.replace(old_row, new_row)
    changes.append('Row builder — Daily SC badge <td> removed')
else:
    print('[WARN] Row builder pattern not found')
    idx = c.find('dailyBadge')
    if idx != -1:
        print('  Found dailyBadge at:', repr(c[max(0,idx-80):idx+60]))

# ─────────────────────────────────────────────────────────────────
# 7. Add Casino Reviews to this page's nav (if not already there)
# ─────────────────────────────────────────────────────────────────
old_nav = """      <a href="/sweepstakes-casino-list" class="nav-link active">Sweepstakes Casinos List</a>
      <a href="/side-hustles" class="nav-link">Side Hustles</a>"""

new_nav = """      <a href="/sweepstakes-casino-list" class="nav-link active">Sweepstakes Casinos List</a>
      <a href="/casino-reviews" class="nav-link">Casino Reviews</a>
      <a href="/side-hustles" class="nav-link">Side Hustles</a>"""

if old_nav in c:
    c = c.replace(old_nav, new_nav)
    changes.append('Nav: added Casino Reviews link')
elif '/casino-reviews' in c:
    changes.append('Nav: Casino Reviews already present, skipped')
else:
    print('[WARN] Nav pattern not found')

# ─────────────────────────────────────────────────────────────────
# Also add Casino Reviews to the mobile menu
# ─────────────────────────────────────────────────────────────────
old_mobile = """  <a href="/sweepstakes-casino-list">Sweepstakes Casinos List</a>
  <a href="/side-hustles">Side Hustles</a>"""

new_mobile = """  <a href="/sweepstakes-casino-list">Sweepstakes Casinos List</a>
  <a href="/casino-reviews">Casino Reviews</a>
  <a href="/side-hustles">Side Hustles</a>"""

if old_mobile in c:
    c = c.replace(old_mobile, new_mobile)
    changes.append('Mobile menu: added Casino Reviews link')
else:
    print('[INFO] Mobile menu pattern not matched (may already have Casino Reviews)')

# ─────────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────────
open(fpath, 'w', encoding='utf-8').write(c)

print('\n=== CHANGES APPLIED ===')
for ch in changes:
    print(' OK:', ch)
print(f'\nTotal: {len(changes)} changes saved to sweepstakes-casino-list.html')
