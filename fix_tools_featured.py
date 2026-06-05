import sys
sys.stdout.reconfigure(encoding='utf-8')

c = open('tools.html', encoding='utf-8').read()

# Find the Featured section start
feat_start = c.find('<!-- ===== FEATURED =====')
# Find the Sweepstakes Automation section start (this is what comes AFTER the two grids)
sweeps_start = c.find('<!-- ===== SWEEPSTAKES AUTOMATION =====')

old_block = c[feat_start:sweeps_start]

new_block = '''<!-- ===== FEATURED ===== -->
  <div class="cat-header dlg-fade">
    <span class="cat-label">&#11088; Featured</span>
    <div class="cat-line"></div>
  </div>

  <div class="tools-grid dlg-fade">
    <!-- #1 — Sweeps App -->
    <div class="tool-card featured-tool" style="--accent:var(--teal);">
      <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.2rem;">
        <div style="font-size:2.2rem;line-height:1;">&#128187;</div>
        <div style="flex:1;">
          <div class="card-title" style="font-size:1.3rem;margin-bottom:0.2rem;">Sweeps App &mdash; Sweepstake Casino Daily Login Software Automation Collector</div>
          <div class="card-subtitle" style="margin-bottom:0;">Multi-Site Daily Bonus Automation</div>
        </div>
        <span class="card-tag tag-teal">TOP PICK</span>
      </div>
      <p class="card-desc">
        Automate daily logins and bonus collection across dozens of sweepstakes casinos at once. Sweeps App handles all the repetitive clicking, site-hopping, and bonus claiming so you don't have to. Set it up once and collect every day on autopilot.
      </p>
      <div style="display:flex;flex-wrap:wrap;align-items:center;gap:0.5rem;margin-bottom:1.2rem;">
        <span class="card-tag tag-teal">DAILY COLLECTION</span>
        <span class="card-tag tag-lime">MULTI-SITE</span>
        <span class="card-tag tag-teal">AUTOMATED</span>
      </div>
      <div style="display:flex;flex-wrap:wrap;align-items:center;gap:1rem;">
        <a href="/bonus-collection-software" class="featured-cta" style="background:var(--teal);color:var(--lime-text);">Learn More &rarr;</a>
        <a href="/bonus-collection-software" class="featured-link">Get Sweeps App</a>
      </div>
    </div>
    <!-- #2 — Greenseed RSA -->
    <div class="tool-card featured-tool" style="--accent:var(--lime);">
      <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.2rem;">
        <div style="font-size:2.2rem;line-height:1;">&#128200;</div>
        <div style="flex:1;">
          <div class="card-title" style="font-size:1.3rem;margin-bottom:0.2rem;">Greenseed &mdash; Reverse Stock Arbitrage Automation</div>
          <div class="card-subtitle" style="margin-bottom:0;">Automated RSA Trading Bot &mdash; Earn $400+/day</div>
        </div>
        <span class="card-tag tag-lime">GREENSEED</span>
      </div>
      <p class="card-desc">
        Reverse Stock Arbitrage (RSA) exploits brokerage rounding rules during reverse stock splits.
        Greenseed automates the entire process &mdash; finding splits, sizing positions, and executing trades across multiple brokerages 24/7.
        Start with alerts at $25/month or full hands-free automation at $75/month. No trading experience needed.
      </p>
      <div style="display:flex;flex-wrap:wrap;align-items:center;gap:0.5rem;margin-bottom:1.2rem;">
        <span class="card-tag tag-lime">$400+/DAY POTENTIAL</span>
        <span class="card-tag tag-teal">FULLY AUTOMATED</span>
        <span class="card-tag tag-white">FROM $25/MO</span>
      </div>
      <div style="display:flex;flex-wrap:wrap;align-items:center;gap:1rem;">
        <a href="/reverse-stock-arbitrage" class="featured-cta">Learn More &rarr;</a>
        <a href="https://greenseed.life/?affiliate=crossroads" class="featured-link" target="_blank" rel="noopener">Get Greenseed</a>
        <a href="https://discord.gg/cdRvNkWxqR" class="featured-link-dim" target="_blank" rel="noopener">Join Their Discord</a>
      </div>
    </div>
    <!-- #3 — Bookie Bandit -->
    <div class="tool-card featured-tool" style="--accent:var(--lime);">
      <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.2rem;">
        <div style="font-size:2.2rem;line-height:1;">&#129302;</div>
        <div style="flex:1;">
          <div class="card-title" style="font-size:1.3rem;margin-bottom:0.2rem;">Bookie Bandit &mdash; Automated Sportsbetting</div>
          <div class="card-subtitle" style="margin-bottom:0;">AI Sports Betting Bot &mdash; 14+ Sportsbooks</div>
        </div>
        <span class="card-tag tag-lime">FEATURED</span>
      </div>
      <p class="card-desc">
        AI-powered desktop app that finds and places positive expected value (+EV) bets automatically 24/7.
        Supports FanDuel, DraftKings, PrizePicks, Underdog, Bovada, and 9 more platforms.
        No sports knowledge needed &mdash; the bot handles everything. Built-in analytics track your profit, win rate, and ROI.
      </p>
      <div style="display:flex;flex-wrap:wrap;align-items:center;gap:0.5rem;margin-bottom:1.2rem;">
        <span class="card-tag tag-teal">24/7 AUTOMATED</span>
        <span class="card-tag tag-gold">14+ SPORTSBOOKS</span>
        <span class="card-tag tag-white">WINDOWS &amp; MAC</span>
      </div>
      <div style="display:flex;flex-wrap:wrap;align-items:center;gap:1rem;">
        <a href="/sportsbetting-automation" class="featured-cta">Learn More &rarr;</a>
        <a href="https://shorturl.at/2CwIc" class="featured-link" target="_blank" rel="noopener">Get Bookie Bandit</a>
        <a href="https://discord.gg/kFSctbB7JY" class="featured-link-dim" target="_blank" rel="noopener">Join Their Discord</a>
      </div>
    </div>
  </div>

  '''

c = c[:feat_start] + new_block + c[sweeps_start:]
open('tools.html', 'w', encoding='utf-8').write(c)
print('Done. Featured section now has 3 cards: Sweeps App, Greenseed, Bookie Bandit')
print('Stock Automation section removed.')
