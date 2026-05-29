/**
 * Online Side Hustles - GA4 growth event tracking.
 *
 * The GA4 snippet loads gtag in page <head> files. This shared script adds
 * intent-level events for the growth funnel without requiring every link to
 * be manually tagged.
 */

(function () {
  'use strict';

  function track(eventName, params) {
    if (typeof window.gtag !== 'function') return;
    window.gtag('event', eventName, params || {});
  }

  function cleanText(text) {
    return (text || '').replace(/\s+/g, ' ').trim().substring(0, 120);
  }

  function linkHost(url) {
    try {
      return new URL(url).hostname.replace(/^www\./, '');
    } catch (err) {
      return '';
    }
  }

  function isDiscordLink(url) {
    return /discord\.gg|discord\.com\/invite/i.test(url);
  }

  function isAffiliateLikeLink(url) {
    var host = linkHost(url);
    var lowerUrl = url.toLowerCase();

    if (!host || host === window.location.hostname.replace(/^www\./, '')) return false;

    return (
      lowerUrl.includes('affid=') ||
      lowerUrl.includes('affiliate') ||
      lowerUrl.includes('ref=') ||
      lowerUrl.includes('raf=') ||
      lowerUrl.includes('utm_campaign=') ||
      lowerUrl.includes('?c=') ||
      host.includes('routy.app') ||
      host.includes('stake.us') ||
      host.includes('wowvegas.com') ||
      host.includes('crowncoinscasino.com') ||
      host.includes('sweepstats.com')
    );
  }

  function internalIntent(url) {
    var path;
    try {
      path = new URL(url).pathname;
    } catch (err) {
      path = url || '';
    }

    if (/newsletter/i.test(path)) return 'newsletter';
    if (/getting-started|daily-login-guide|daily-free-sc|new-sites|sweepstakes|review|casino/i.test(path)) return 'sweepstakes_guide';
    if (/blog|guide|tools|calculator|sweepstats/i.test(path)) return 'guide_or_tool';
    if (/methodology|affiliate-disclosure|privacy|terms|faq/i.test(path)) return 'trust';
    return 'internal';
  }

  document.addEventListener('click', function (event) {
    var link = event.target.closest('a[href]');
    if (!link) return;

    var href = link.href || '';
    var text = cleanText(link.textContent);
    var baseParams = {
      link_url: href,
      link_text: text,
      page_location: window.location.pathname,
      page_title: document.title
    };

    if (isDiscordLink(href)) {
      track('discord_join_click', Object.assign({
        event_category: 'community',
        destination: 'discord'
      }, baseParams));
    }

    if (isAffiliateLikeLink(href)) {
      track('affiliate_click', Object.assign({
        event_category: 'monetization',
        link_domain: linkHost(href)
      }, baseParams));
      return;
    }

    if (/^https?:\/\//i.test(href) && !href.includes(window.location.hostname)) {
      track('outbound_link_click', Object.assign({
        event_category: 'outbound',
        link_domain: linkHost(href)
      }, baseParams));
      return;
    }

    track('internal_link_click', Object.assign({
      event_category: 'navigation',
      link_intent: internalIntent(href)
    }, baseParams));
  });

  document.querySelectorAll('form').forEach(function (form) {
    var hasEmailInput = !!form.querySelector('input[type="email"], input[name*="email" i]');
    var formName = form.getAttribute('name') || form.querySelector('input[name="form-name"]')?.value || 'unknown';
    var action = form.getAttribute('action') || '';
    var looksLikeNewsletter = /newsletter|subscribe|email/i.test(formName + ' ' + action);

    if (!hasEmailInput && !looksLikeNewsletter) return;

    form.addEventListener('submit', function () {
      var interest = form.querySelector('[name="interest"]');
      track('newsletter_signup', {
        event_category: 'lead',
        form_name: formName,
        form_location: window.location.pathname,
        form_action: action || 'inline',
        signup_interest: interest ? interest.value : ''
      });
    });
  });

  if (window.location.pathname.includes('tools') || window.location.pathname.includes('calculator')) {
    document.querySelectorAll('button').forEach(function (button) {
      var label = cleanText(button.textContent).toLowerCase();
      if (!/calculate|estimate|compute|check/.test(label)) return;

      button.addEventListener('click', function () {
        var section = button.closest('section, .calculator, .tool-card, .calc-card, [class*="calc"]');
        var heading = section ? section.querySelector('h1, h2, h3, h4') : null;
        track('calculator_used', {
          event_category: 'tool',
          calculator_name: heading ? cleanText(heading.textContent) : 'unknown',
          page_location: window.location.pathname
        });
      });
    });
  }

  var scrollMarks = { 25: false, 50: false, 75: false, 100: false };

  function getScrollPercent() {
    var doc = document.documentElement;
    var body = document.body;
    var scrollTop = doc.scrollTop || body.scrollTop;
    var scrollHeight = (doc.scrollHeight || body.scrollHeight) - doc.clientHeight;
    if (scrollHeight <= 0) return 100;
    return Math.round((scrollTop / scrollHeight) * 100);
  }

  var scrollTimer;
  window.addEventListener('scroll', function () {
    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(function () {
      var percent = getScrollPercent();
      [25, 50, 75, 100].forEach(function (mark) {
        if (percent < mark || scrollMarks[mark]) return;
        scrollMarks[mark] = true;
        track('scroll_depth', {
          event_category: 'engagement',
          depth_percentage: mark,
          page_location: window.location.pathname,
          page_title: document.title
        });
      });
    }, 200);
  }, { passive: true });
})();
