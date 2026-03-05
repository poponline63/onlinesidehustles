/**
 * Online Side Hustles - GA4 Analytics & Event Tracking
 * 
 * Custom event tracking for key user actions.
 * GA4 Measurement ID is loaded via the gtag.js snippet in <head>.
 * 
 * Events tracked:
 *   - discord_join_click: User clicks a Discord invite link
 *   - newsletter_signup: User submits a newsletter/email form
 *   - outbound_link_click: User clicks an external link
 *   - guide_link_click: User clicks an internal guide/blog link
 *   - calculator_used: User interacts with a calculator on tools.html
 *   - scroll_depth: User reaches 25%, 50%, 75%, 100% of a page
 *   - cta_click: User clicks a prominent CTA button
 */

(function () {
  'use strict';

  // Helper: safe gtag call
  function track(eventName, params) {
    if (typeof gtag === 'function') {
      gtag('event', eventName, params || {});
    }
  }

  // ──────────────────────────────────────────────
  // 1. Discord Join Button Clicks
  // ──────────────────────────────────────────────
  document.querySelectorAll('a[href*="discord.gg"], a[href*="discord.com/invite"]').forEach(function (el) {
    el.addEventListener('click', function () {
      track('discord_join_click', {
        link_url: el.href,
        link_text: (el.textContent || '').trim().substring(0, 100),
        page_location: window.location.pathname
      });
    });
  });

  // ──────────────────────────────────────────────
  // 2. Newsletter / Email Signup Forms
  // ──────────────────────────────────────────────
  document.querySelectorAll('form').forEach(function (form) {
    // Detect newsletter-like forms by action URL or input names
    var isNewsletter = form.action && (
      form.action.includes('newsletter') ||
      form.action.includes('subscribe') ||
      form.action.includes('mailchimp') ||
      form.action.includes('convertkit') ||
      form.action.includes('buttondown') ||
      form.action.includes('sendfox')
    );
    var hasEmailInput = form.querySelector('input[type="email"], input[name*="email"]');
    
    if (isNewsletter || hasEmailInput) {
      form.addEventListener('submit', function () {
        track('newsletter_signup', {
          form_location: window.location.pathname,
          form_action: form.action || 'inline'
        });
      });
    }
  });

  // ──────────────────────────────────────────────
  // 3. Link Click Tracking (Outbound + Internal Guides)
  // ──────────────────────────────────────────────
  var ownHost = window.location.hostname;

  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href]');
    if (!link) return;

    var url = link.href || '';
    var text = (link.textContent || '').trim().substring(0, 100);

    // Outbound links (not our domain, not anchors, not javascript)
    if (url.startsWith('http') && !url.includes(ownHost)) {
      track('outbound_link_click', {
        link_url: url,
        link_text: text,
        page_location: window.location.pathname
      });
      return;
    }

    // Internal guide/blog links
    if (url.includes('/blog/') || url.includes('/guide') || url.includes('-guide')) {
      track('guide_link_click', {
        link_url: url,
        link_text: text,
        page_location: window.location.pathname
      });
    }
  });

  // ──────────────────────────────────────────────
  // 4. Calculator Usage (tools.html)
  // ──────────────────────────────────────────────
  if (window.location.pathname.includes('tools')) {
    // Track calculate button clicks
    document.querySelectorAll('button').forEach(function (btn) {
      var txt = (btn.textContent || '').toLowerCase();
      if (txt.includes('calculate') || txt.includes('estimate') || txt.includes('compute')) {
        btn.addEventListener('click', function () {
          // Try to determine which calculator
          var calcSection = btn.closest('section, .calculator, .tool-card, .calc-card, [class*="calc"]');
          var calcName = 'unknown';
          if (calcSection) {
            var heading = calcSection.querySelector('h2, h3, h4');
            if (heading) calcName = heading.textContent.trim().substring(0, 80);
          }
          track('calculator_used', {
            calculator_name: calcName,
            page_location: window.location.pathname
          });
        });
      }
    });

    // Also track input changes in calculator fields (debounced)
    var calcTimeout;
    document.querySelectorAll('input[type="number"], input[type="range"], select').forEach(function (input) {
      input.addEventListener('change', function () {
        clearTimeout(calcTimeout);
        calcTimeout = setTimeout(function () {
          track('calculator_interaction', {
            input_name: input.name || input.id || 'unnamed',
            page_location: window.location.pathname
          });
        }, 1000);
      });
    });
  }

  // ──────────────────────────────────────────────
  // 5. Scroll Depth Tracking
  // ──────────────────────────────────────────────
  var scrollMarks = { 25: false, 50: false, 75: false, 100: false };

  function getScrollPercent() {
    var h = document.documentElement;
    var b = document.body;
    var st = h.scrollTop || b.scrollTop;
    var sh = (h.scrollHeight || b.scrollHeight) - h.clientHeight;
    if (sh <= 0) return 100;
    return Math.round((st / sh) * 100);
  }

  var scrollTimer;
  window.addEventListener('scroll', function () {
    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(function () {
      var pct = getScrollPercent();
      [25, 50, 75, 100].forEach(function (mark) {
        if (pct >= mark && !scrollMarks[mark]) {
          scrollMarks[mark] = true;
          track('scroll_depth', {
            depth_percentage: mark,
            page_location: window.location.pathname,
            page_title: document.title
          });
        }
      });
    }, 200);
  }, { passive: true });

  // ──────────────────────────────────────────────
  // 6. CTA Button Clicks (generic catch-all for styled CTAs)
  // ──────────────────────────────────────────────
  document.querySelectorAll('.cta-button, .cta-btn, [class*="cta"], a.btn, button.btn').forEach(function (el) {
    el.addEventListener('click', function () {
      track('cta_click', {
        cta_text: (el.textContent || '').trim().substring(0, 100),
        cta_url: el.href || '',
        page_location: window.location.pathname
      });
    });
  });

})();
