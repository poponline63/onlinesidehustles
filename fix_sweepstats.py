with open('sweepstats.html', encoding='utf-8') as f:
    c = f.read()

start = c.find('<!-- PAGE CONTENT -->')
end   = c.find('<!-- FOOTER -->')
assert start != -1 and end != -1, "markers not found!"

NEW_CONTENT = '''<!-- PAGE CONTENT -->
<div class="content-area">
  <div class="container">

    <!-- HERO -->
    <div class="ss-hero fade-in">
      <div class="ss-badge">&#x1F4CA; Community-Built Tool</div>
      <h1><span class="ss-gradient">SweepStats</span><br>Transaction Tracker</h1>
      <p>The free sweepstakes portfolio tracker built by the community. Track every deposit, redemption, and profit across all your casinos &mdash; with dashboards, charts, per-casino breakdowns, and CSV import. No account required.</p>
      <div class="ss-hero-btns">
        <a href="https://www.sweepstats.com/" class="btn-teal" target="_blank" rel="noopener">&#x1F680; Open SweepStats</a>
        <a href="https://discord.gg/W9bPGH8crh" class="btn-ghost" target="_blank" rel="noopener">Join Community</a>
      </div>
    </div>

    <!-- STATS -->
    <div class="ss-stats fade-in">
      <div class="ss-stat">
        <div class="ss-stat-num">$0</div>
        <div class="ss-stat-lbl">Cost &mdash; Free Forever</div>
      </div>
      <div class="ss-stat">
        <div class="ss-stat-num">100%</div>
        <div class="ss-stat-lbl">Privacy &mdash; Data Stays Local</div>
      </div>
      <div class="ss-stat">
        <div class="ss-stat-num">All</div>
        <div class="ss-stat-lbl">Casinos Supported</div>
      </div>
      <div class="ss-stat">
        <div class="ss-stat-num">Live</div>
        <div class="ss-stat-lbl">Charts &amp; Dashboard</div>
      </div>
    </div>

    <!-- WHAT IS IT -->
    <div class="ss-section fade-in">
      <div class="ss-section-title">&#x1F4CA; What is SweepStats?</div>
      <p class="ss-section-sub">SweepStats is a free web-based tool built specifically for sweepstakes casino players. It solves one of the biggest pain points in sweepstakes: <strong style="color:#fff;">knowing your actual numbers.</strong></p>
      <p style="color:var(--text-dim);font-size:0.95rem;line-height:1.8;margin-bottom:1.5rem;">Most players have a rough idea of whether they're up or down, but no clear picture of their ROI per casino, which sites are actually paying out, or what their total profit/loss is across the board. SweepStats gives you that clarity &mdash; in real time, for free, with no signup required.</p>
      <div style="background:rgba(110,231,183,0.06);border:1px solid rgba(110,231,183,0.2);border-left:4px solid var(--teal);border-radius:10px;padding:1.5rem;margin-top:1rem;">
        <h4 style="color:var(--teal);font-size:0.95rem;font-weight:700;margin-bottom:0.6rem;">&#x1F4A1; Built by the Community</h4>
        <p style="color:var(--text-dim);font-size:0.9rem;line-height:1.7;margin:0;">SweepStats was created by a member of the sweepstakes community who wanted a better way to track profits. It's free, open, and continuously improved based on community feedback. Find it and discuss it in our Discord server.</p>
      </div>
    </div>

    <!-- FEATURES -->
    <div class="ss-section fade-in">
      <div class="ss-section-title">&#x26A1; Features</div>
      <div class="feature-grid">
        <div class="feature-card">
          <div class="feature-icon">&#x1F4C8;</div>
          <h3>Dashboard Overview</h3>
          <p>See your total deposits, redemptions, and net profit across all casinos in one clean view. Know your overall numbers at a glance.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">&#x1F3B0;</div>
          <h3>Per-Casino Breakdown</h3>
          <p>See exactly which casinos are profitable for you and which aren't. Stop wasting time on sites with poor ROI and double down on winners.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">&#x1F4C9;</div>
          <h3>Charts &amp; Trends</h3>
          <p>Visualize your earnings over time with interactive charts. Spot seasonal trends, track your growth, and identify your best months.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">&#x1F4C2;</div>
          <h3>CSV Import</h3>
          <p>Import your transaction history from bank statements or casino transaction exports. Get started in minutes with your existing data.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">&#x1F512;</div>
          <h3>Privacy First</h3>
          <p>Your financial data stays on your device. No account required, no data sent to external servers. Your numbers are yours alone.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">&#x1F193;</div>
          <h3>Free &amp; Open</h3>
          <p>Built by the community, for the community. Completely free to use with no hidden fees, no premium tiers, no paywalls &mdash; ever.</p>
        </div>
      </div>
    </div>

    <!-- HOW TO USE -->
    <div class="ss-section fade-in">
      <div class="ss-section-title">&#x1F680; How to Get Started</div>
      <p class="ss-section-sub">Takes less than 5 minutes to set up. No account, no downloads, no credit card.</p>
      <div class="ss-steps">
        <div class="ss-step">
          <div class="ss-step-num">1</div>
          <div class="ss-step-body">
            <h3>Visit sweepstats.com</h3>
            <p>Open the tool directly in your browser at sweepstats.com. No installation, no signup. It runs entirely in your browser using local storage to keep your data private.</p>
          </div>
        </div>
        <div class="ss-step">
          <div class="ss-step-num">2</div>
          <div class="ss-step-body">
            <h3>Add Your Casinos</h3>
            <p>Create entries for each sweepstakes casino you play. Add the casino name and start logging your transactions, or use CSV import if you have existing data ready.</p>
          </div>
        </div>
        <div class="ss-step">
          <div class="ss-step-num">3</div>
          <div class="ss-step-body">
            <h3>Log Deposits &amp; Redemptions</h3>
            <p>Every time you buy a package or cash out, add the transaction. Takes 10 seconds per entry. The dashboard updates instantly to show your running profit/loss.</p>
          </div>
        </div>
        <div class="ss-step">
          <div class="ss-step-num">4</div>
          <div class="ss-step-body">
            <h3>Review Your Dashboard</h3>
            <p>Check your dashboard regularly to see which casinos are performing best, your overall ROI, and trends over time. Use this data to optimize where you spend your time and money.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- WHY TRACK -->
    <div class="ss-section fade-in">
      <div class="ss-section-title">&#x2705; Why Tracking Matters</div>
      <p class="ss-section-sub">Most people think they're making more than they are &mdash; or don't know they're losing on certain sites. Data changes everything.</p>
      <div class="why-grid">
        <div class="why-item">
          <div class="why-check">&#x2713;</div>
          <div>
            <h4>Know Your Actual ROI</h4>
            <p>Package welcome bonuses look attractive on paper. Tracking reveals which ones actually pay off after wagering requirements and time spent.</p>
          </div>
        </div>
        <div class="why-item">
          <div class="why-check">&#x2713;</div>
          <div>
            <h4>Cut Losing Sites</h4>
            <p>Some casinos simply pay out less for you. Data lets you identify which sites to drop and reallocate that bankroll to better performers.</p>
          </div>
        </div>
        <div class="why-item">
          <div class="why-check">&#x2713;</div>
          <div>
            <h4>Optimize Your Bankroll</h4>
            <p>See which sites give the best returns and shift more of your capital there. Small optimizations compound significantly over time.</p>
          </div>
        </div>
        <div class="why-item">
          <div class="why-check">&#x2713;</div>
          <div>
            <h4>Tax Record Keeping</h4>
            <p>A clean log of all deposits and redemptions makes tax time straightforward. Know exactly what you earned and spent on each platform.</p>
          </div>
        </div>
        <div class="why-item">
          <div class="why-check">&#x2713;</div>
          <div>
            <h4>Track Multiple Accounts</h4>
            <p>Running the Player 2 strategy? Track each account separately and see which of your managed accounts are the most profitable.</p>
          </div>
        </div>
        <div class="why-item">
          <div class="why-check">&#x2713;</div>
          <div>
            <h4>Motivation &amp; Accountability</h4>
            <p>Seeing your profit chart grow over time is motivating. Seeing a loss on a site is the accountability you need to change your approach.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA -->
    <div class="ss-cta fade-in">
      <h2>Start Tracking Your Profits</h2>
      <p>SweepStats is free, takes 5 minutes to set up, and will immediately give you clarity on your sweepstakes portfolio. Join our Discord to connect with others using the tool and get tips on optimizing your strategy.</p>
      <div style="display:flex;gap:1rem;flex-wrap:wrap;justify-content:center;">
        <a href="https://www.sweepstats.com/" class="btn-teal" target="_blank" rel="noopener">&#x1F680; Open SweepStats Free</a>
        <a href="https://discord.gg/W9bPGH8crh" class="btn-ghost" target="_blank" rel="noopener">&#x1F4AC; Join Discord Community</a>
      </div>
    </div>

  </div>
</div>

'''

c = c[:start] + NEW_CONTENT + c[end:]
with open('sweepstats.html', 'w', encoding='utf-8') as f:
    f.write(c)
print(f'Done — length: {len(c)}')
