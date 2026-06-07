/* ==========================================================================
   Online Sidehustles — Community Casino Ratings
   Single source of truth for the rating widget, tier logic, and the
   Google Apps Script backend connection. Used by the list page AND every
   review-*.html page so a vote anywhere counts toward the same average.

   SETUP: After deploying the Apps Script web app (see casino-ratings/SETUP.md),
   paste the deployment URL (ends in /exec) into ENDPOINT below. Until then the
   widget is disabled and pages render exactly as before.
   ========================================================================== */
(function () {
  'use strict';

  var CFG = {
    // <<< PASTE YOUR DEPLOYED APPS SCRIPT /exec URL HERE >>>
    ENDPOINT: 'https://script.google.com/macros/s/AKfycbzPbH1tgaYiQ1xBgAG0QfTMt4KqBy7VhSWyxN74dSuG3reewr0DmfrDGcdRVdhgpYrZLA/exec',

    // Minimum community votes before a casino's tier can be overridden by the
    // crowd. Below this it keeps your editorial (sheet) tier.
    MIN_VOTES: 10,

    // Average score (1-5) -> tier. Checked top to bottom; first match wins.
    // S = God Tier, A = High Tier, B = Medium Tier, NEW = New.
    THRESHOLDS: [[4.5, 'S'], [3.8, 'A'], [2.5, 'B']],
    NEW_TIER: 'NEW',

    JSONP_TIMEOUT_MS: 12000
  };

  var enabled = !!CFG.ENDPOINT;

  // Same normalization the list page uses so keys line up everywhere.
  function normName(n) {
    return String(n || '').toLowerCase().replace(/[^a-z0-9]/g, '');
  }

  function scoreToTier(avg) {
    for (var i = 0; i < CFG.THRESHOLDS.length; i++) {
      if (avg >= CFG.THRESHOLDS[i][0]) return CFG.THRESHOLDS[i][1];
    }
    return CFG.NEW_TIER;
  }

  // RATINGS[normKey] = { n: displayName, a: average, c: count, t: communityTier }
  var RATINGS = {};

  // ---- JSONP transport (avoids all CORS issues with Apps Script) ----------
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
      qs.push('t=' + Date.now()); // cache-buster
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
    setMyVote(name, stars); // optimistic so re-render shows it immediately
    return jsonp({ action: 'vote', casino: name, key: normName(name), stars: stars, prev: prev || '' })
      .then(function (res) {
        if (res && res.ok) {
          RATINGS[normName(name)] = { n: res.n || name, a: res.a, c: res.c, t: res.t };
        }
        return res;
      });
  }

  // ---- widget rendering ---------------------------------------------------
  // DOM is built star5..star1 and laid out row-reverse so pure-CSS hover can
  // highlight the hovered star plus every lower one (to its left).
  function widgetHTML(name, opts) {
    opts = opts || {};
    var r = get(name);
    var avg = r ? r.a : 0;
    var count = r ? r.c : 0;
    var mine = myVote(name);
    var filled = Math.round(avg);
    var stars = '';
    for (var v = 5; v >= 1; v--) {
      var on = v <= filled ? ' oshr-on' : '';
      var youOn = mine && v <= mine ? ' oshr-mine' : '';
      stars += '<button type="button" class="oshr-star' + on + youOn + '" data-v="' + v +
        '" aria-label="Rate ' + v + ' out of 5">★</button>';
    }
    var meta;
    if (count > 0) {
      meta = '<b>' + avg.toFixed(1) + '</b><span class="oshr-n">(' + count + ')</span>';
      if (mine) meta += '<span class="oshr-you">you ' + mine + '★</span>';
    } else {
      meta = mine ? '<span class="oshr-you">you ' + mine + '★</span>'
                  : '<span class="oshr-first">Rate it</span>';
    }
    return '<span class="oshr' + (opts.compact ? ' oshr-compact' : '') + '" data-c="' + esc(name) + '">' +
      '<span class="oshr-stars" role="radiogroup" aria-label="Community rating for ' + esc(name) + '">' +
      stars + '</span><span class="oshr-meta">' + meta + '</span></span>';
  }

  function esc(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // Re-render one widget element in place from current state.
  function refresh(el) {
    if (!el) return;
    var name = el.getAttribute('data-c');
    var compact = el.classList.contains('oshr-compact');
    var tmp = document.createElement('div');
    tmp.innerHTML = widgetHTML(name, { compact: compact });
    el.innerHTML = tmp.firstChild.innerHTML;
  }

  // Delegated click handling. Call once per page on a container that holds
  // (or will hold) widgets. onVoted(name, res, widgetEl) fires after success.
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
      refresh(widget); // optimistic (myVote already set on click path? set now)
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

  // ---- inject self-contained CSS so every page styles widgets identically -
  function injectCSS() {
    if (document.getElementById('oshr-css')) return;
    var css = [
      '.oshr{display:inline-flex;align-items:center;gap:.4rem;font-family:inherit;line-height:1;}',
      '.oshr-stars{display:inline-flex;flex-direction:row-reverse;gap:1px;}',
      '.oshr-star{background:none;border:0;padding:0 1px;margin:0;cursor:pointer;font-size:1.05rem;color:#3a4860;transition:color .12s;line-height:1;}',
      '.oshr-star.oshr-on{color:#f5b301;}',
      '.oshr-star.oshr-mine{color:#6ee7b7;}',
      '.oshr-stars:hover .oshr-star{color:#3a4860;}',
      '.oshr-stars:hover .oshr-star:hover,.oshr-stars:hover .oshr-star:hover ~ .oshr-star{color:#ffd23f;}',
      '.oshr-busy .oshr-star{cursor:progress;opacity:.6;}',
      '.oshr-meta{font-size:.74rem;color:#9fb0c8;display:inline-flex;align-items:baseline;gap:.28rem;white-space:nowrap;}',
      '.oshr-meta b{color:#f5b301;font-size:.82rem;}',
      '.oshr-n{opacity:.7;}',
      '.oshr-you{color:#6ee7b7;font-size:.66rem;}',
      '.oshr-first{color:#9fb0c8;font-size:.7rem;font-style:italic;}',
      '.oshr-compact .oshr-star{font-size:.92rem;}',
      '.oshr-compact .oshr-meta{font-size:.66rem;}',
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
    scoreToTier: scoreToTier,
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
