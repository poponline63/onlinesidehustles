# Community Casino Ratings — Setup

A star-rating widget on the casino list **and** every review page. Votes go to
your Google Sheet, build a running average per casino, and **auto-move casinos
between tiers** (God / High / Medium / New) once a casino passes the minimum
vote count.

Nothing is live until you do **Step 1–3 below** (deploy the Google Apps Script
and paste its URL). Until then every page renders exactly as it did before —
the widget hides itself when no backend is configured.

---

## How it works

```
 Visitor clicks stars
        │  (JSONP GET — no CORS issues)
        ▼
 Google Apps Script Web App  ──►  "Ratings" tab in your casino spreadsheet
        │                          (NormKey | Casino | Sum | Count | Average |
        │                           CommunityTier | LastUpdated)
        ▼
 Returns updated average + tier
        │
        ▼
 sweepstakes-casino-list.html re-computes each casino's tier from the
 community average and re-renders — a casino visibly jumps tiers.
```

- **Your editorial sheet is never modified.** All votes live in a separate
  `Ratings` tab. Your curated tiers stay as the baseline/fallback.
- A casino keeps its editorial tier until it reaches **MIN_VOTES** (default 10).
  After that, the community average decides its tier:
  - `4.5+` → 👑 God Tier (S)
  - `3.8+` → 🔥 High Tier (A)
  - `2.5+` → 🎯 Medium Tier (B)
  - below → ✨ New (NEW)
- **One vote per device** (localStorage). A visitor can change their vote and
  the average adjusts correctly (no double-counting).

---

## Step 1 — Create the Apps Script

1. Open your casino spreadsheet:
   <https://docs.google.com/spreadsheets/d/1yJAKLouHPn3AvV2PKEhulepc6HQ4uj9hfEPkl3WaMog/edit>
2. Menu: **Extensions → Apps Script**.
3. Delete the default `Code.gs` contents and paste the entire contents of
   [`Code.gs`](Code.gs) from this folder.
4. Click **Save** (disk icon).

> The `SPREADSHEET_ID` at the top of `Code.gs` is already set to your sheet.
> It creates the `Ratings` tab automatically on the first vote.

## Step 2 — Deploy as a Web App

1. In the Apps Script editor: **Deploy → New deployment**.
2. Click the gear icon → choose **Web app**.
3. Settings:
   - **Description:** `Casino ratings`
   - **Execute as:** **Me** (your account)
   - **Who has access:** **Anyone**  ← required so visitors can vote
4. Click **Deploy**. Approve the permission prompt (it needs access to your
   spreadsheet). You may see an "unverified app" screen — click
   **Advanced → Go to (project) → Allow**. This is normal for your own script.
5. Copy the **Web app URL**. It looks like:
   `https://script.google.com/macros/s/AKfy.....long.....string/exec`

## Step 3 — Connect the website

1. Open [`js/casino-ratings.js`](../js/casino-ratings.js).
2. Paste your URL into the `ENDPOINT` line near the top:
   ```js
   ENDPOINT: 'https://script.google.com/macros/s/AKfy....../exec',
   ```
3. Save, commit, and push. Netlify redeploys and the widget goes live
   everywhere automatically.

That's it. ✅

---

## Test it

1. Load <https://onlinesidehustles.info/sweepstakes-casino-list> — you should
   see a **Community** column with stars.
2. Click some stars on any casino.
3. Open the **Ratings** tab in your spreadsheet — a row appears with the
   running Sum / Count / Average / CommunityTier.
4. Rate the same casino 10+ times (different devices/browsers, or clear
   localStorage) to watch it cross `MIN_VOTES` and move tiers on reload.

To clear your own vote for re-testing in the browser console:
```js
Object.keys(localStorage).filter(k=>k.startsWith('oshvote_')).forEach(k=>localStorage.removeItem(k));
```

---

## Tuning

All knobs live in **one place** — `js/casino-ratings.js`, the `CFG` object:

| Setting       | Default                          | Meaning |
|---------------|----------------------------------|---------|
| `MIN_VOTES`   | `10`                             | Votes needed before the crowd can override your tier |
| `THRESHOLDS`  | `[[4.5,'S'],[3.8,'A'],[2.5,'B']]`| Average → tier cutoffs |
| `NEW_TIER`    | `'NEW'`                          | Tier when below all thresholds |

If you change `THRESHOLDS`, make the **same edit** in `casino-ratings/Code.gs`
(the `THRESHOLDS` near the top) so the tier stored in the sheet matches what the
site shows. Then **re-deploy** (Deploy → Manage deployments → edit → new
version).

---

## Anti-abuse notes

- One vote per browser via localStorage; deters casual ballot-stuffing without
  forcing logins.
- `MIN_VOTES` stops a single troll from yanking a casino across tiers.
- Determined abusers can clear storage / use many devices. If a casino ever
  gets brigaded, you can:
  - delete or correct its row in the `Ratings` tab, and/or
  - raise `MIN_VOTES`, and/or
  - I can add server-side IP rate-limiting (the "per-device + server
    rate-limit" option) on request.

## Removing / disabling

Set `ENDPOINT: ''` in `js/casino-ratings.js` and push. Every page instantly
reverts to its original look (widget self-hides). No HTML changes needed.
