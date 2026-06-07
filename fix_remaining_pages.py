
import re

# ============================================================
# Shared RSA page CSS for content pages
# ============================================================
SHARED_PAGE_CSS = '''<style>
/* ===== PAGE CONTENT - RSA STYLE ===== */

/* Hero */
.page-hero { text-align:center; padding:88px 2rem 60px; max-width:1200px; margin:0 auto; }
.page-hero-content { max-width:800px; margin:0 auto; }
.hero-badge {
  display:inline-flex; align-items:center; gap:0.5rem;
  background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%);
  padding:0.5rem 1.2rem; border-radius:20px; color:#060a0f;
  font-family:'IBM Plex Mono',monospace; font-size:0.85rem; font-weight:700; letter-spacing:0.05em;
  animation:pulseBadge 2s infinite; box-shadow:0 0 30px rgba(110,231,183,0.4); margin-bottom:1.5rem;
}
@keyframes pulseBadge { 0%,100%{box-shadow:0 0 30px rgba(110,231,183,0.4);} 50%{box-shadow:0 0 50px rgba(110,231,183,0.7);} }
.page-hero h1 { font-size:clamp(2rem,4vw,3.5rem); font-weight:900; font-family:'IBM Plex Mono',monospace; margin:0 0 1rem; line-height:1.15; color:#fff; }
.page-hero h1 span, .page-hero h1 .accent { background:linear-gradient(135deg,#6ee7b7,#a7f3d0,#34d399); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.page-hero > p, .page-hero-content > p { color:var(--text-dim); font-size:1.1rem; max-width:680px; margin:0 auto 2rem; line-height:1.7; }
.hero-btns { display:flex; gap:1rem; flex-wrap:wrap; justify-content:center; }
.btn-emerald { display:inline-flex; align-items:center; gap:0.5rem; background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%); color:#060a0f; text-decoration:none; padding:0.85rem 2rem; border-radius:50px; font-size:1rem; font-weight:700; box-shadow:0 0 20px rgba(110,231,183,0.4); transition:transform 0.2s,box-shadow 0.2s; }
.btn-emerald:hover { transform:translateY(-2px); box-shadow:0 0 35px rgba(110,231,183,0.6); }
.btn-secondary { display:inline-flex; align-items:center; gap:0.5rem; background:transparent; color:var(--teal); text-decoration:none; padding:0.85rem 2rem; border-radius:50px; font-size:1rem; font-weight:700; border:2px solid rgba(110,231,183,0.35); transition:all 0.2s; }
.btn-secondary:hover { border-color:var(--teal); background:rgba(110,231,183,0.07); }

/* Stats */
.stats-section { max-width:1200px; margin:0 auto 3rem; padding:0 2rem; }
.stats-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:1.5rem; }
.stat-card { background:var(--bg-card); border:1px solid var(--border); border-radius:15px; padding:1.5rem; text-align:center; transition:all 0.3s; }
.stat-card:hover { transform:translateY(-4px); box-shadow:0 10px 30px rgba(0,0,0,0.3); }
.stat-number { font-size:1.8rem; font-weight:bold; background:linear-gradient(135deg,#6ee7b7,#a7f3d0); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; font-family:'IBM Plex Mono',monospace; margin-bottom:0.25rem; }
.stat-label { color:var(--text-dim); font-size:0.8rem; text-transform:uppercase; letter-spacing:0.05em; }

/* Content sections */
.section { background:var(--bg-card); border:1px solid var(--border); border-left:4px solid var(--teal); border-radius:20px; padding:3rem; margin-bottom:3rem; max-width:1200px; margin-left:auto; margin-right:auto; box-shadow:0 10px 40px rgba(0,0,0,0.3); }
.section-title { font-size:1.75rem; font-weight:bold; color:#fff; font-family:'IBM Plex Mono',monospace; margin-bottom:0.75rem; line-height:1.2; }
.section-title span { background:linear-gradient(135deg,#6ee7b7,#a7f3d0); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.section-sub { color:var(--text-dim); font-size:0.95rem; line-height:1.8; margin-bottom:2rem; }

/* Tip / warn boxes */
.tip-box { background:rgba(110,231,183,0.06); border:1px solid rgba(110,231,183,0.2); border-left:4px solid var(--teal); border-radius:10px; padding:1.5rem; margin:1.5rem 0; }
.tip-box h4 { color:var(--teal); font-size:0.95rem; font-weight:700; margin-bottom:0.6rem; }
.tip-box p { color:var(--text-dim); font-size:0.9rem; line-height:1.7; margin:0; }
.tip-box strong { color:#fff; }
.warn-box { background:rgba(251,191,36,0.06); border:1px solid rgba(251,191,36,0.2); border-left:4px solid #fbbf24; border-radius:10px; padding:1.5rem; margin:1.5rem 0; }
.warn-box h4 { color:#fbbf24; font-size:0.95rem; font-weight:700; margin-bottom:0.6rem; }
.warn-box p { color:var(--text-dim); font-size:0.9rem; line-height:1.7; margin:0; }
.warn-box strong { color:#fff; }

/* Steps grids */
.steps-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin-top:1.5rem; }
.step-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:1rem; margin-top:1.5rem; }
.step-card { background:rgba(110,231,183,0.03); border:1px solid var(--border); border-radius:12px; padding:1.5rem 1.2rem; transition:all 0.3s; position:relative; overflow:hidden; }
.step-card::before { content:''; position:absolute; top:0;left:0;right:0;height:3px; background:linear-gradient(90deg,var(--teal),#34d399); transform:translateX(-100%); transition:transform 0.5s; }
.step-card:hover::before { transform:translateX(0); }
.step-card:hover { border-color:var(--border-md); transform:translateY(-3px); }
.step-num { width:40px; height:40px; background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:1.1rem; font-weight:800; color:#060a0f; margin:0 auto 0.8rem; box-shadow:0 0 15px rgba(110,231,183,0.4); }
.step-card h3, .step-card h4 { font-size:0.95rem; font-weight:700; color:#fff; margin-bottom:0.5rem; }
.step-card p { font-size:0.82rem; color:var(--text-dim); line-height:1.5; }

/* Card items (credit cards) */
.cards-grid { display:flex; flex-direction:column; gap:1rem; margin-top:1.5rem; }
.card-item { background:rgba(110,231,183,0.03); border:1px solid var(--border); border-radius:15px; padding:1.5rem 2rem; display:flex; justify-content:space-between; align-items:flex-start; gap:1.5rem; transition:all 0.3s; position:relative; overflow:hidden; }
.card-item::before { content:''; position:absolute; top:0;left:0;right:0;height:3px; background:linear-gradient(90deg,var(--teal),#34d399); transform:translateX(-100%); transition:transform 0.5s; }
.card-item:hover::before { transform:translateX(0); }
.card-item:hover { border-color:var(--border-md); }
.card-emoji { font-size:2rem; flex-shrink:0; }
.card-info { flex:1; }
.card-info h3 { font-size:1.05rem; font-weight:700; color:#fff; margin-bottom:0.5rem; }
.card-info p { font-size:0.88rem; color:var(--text-dim); line-height:1.7; margin-bottom:0.75rem; }
.card-bonus { text-align:right; flex-shrink:0; }
.bonus-amt { font-size:1.3rem; font-weight:800; background:linear-gradient(135deg,#6ee7b7,#a7f3d0); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; font-family:'IBM Plex Mono',monospace; }
.bonus-label { font-size:0.75rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.05em; }

/* Badges */
.badge, .card-badge { display:inline-block; font-size:0.68rem; font-weight:700; letter-spacing:0.06em; padding:0.2rem 0.6rem; border-radius:6px; margin-right:0.3rem; margin-bottom:0.3rem; }
.badge-gold  { background:rgba(251,191,36,0.10);  color:#fbbf24; border:1px solid rgba(251,191,36,0.25); }
.badge-green { background:rgba(110,231,183,0.12); color:#6ee7b7; border:1px solid rgba(110,231,183,0.25); }
.badge-blue  { background:rgba(96,165,250,0.10);  color:#60a5fa; border:1px solid rgba(96,165,250,0.22); }
.badge-red   { background:rgba(248,113,113,0.08); color:#f87171; border:1px solid rgba(248,113,113,0.18); }
.badge-purple{ background:rgba(192,132,252,0.08); color:#c084fc; border:1px solid rgba(192,132,252,0.18); }

/* Category headers */
.cat-header { display:flex; align-items:center; gap:1rem; margin:2rem 0 1rem; }
.cat-header h3 { font-size:1rem; font-weight:700; color:var(--teal); font-family:'IBM Plex Mono',monospace; margin:0; white-space:nowrap; }
.cat-line { flex:1; height:1px; background:rgba(110,231,183,0.2); }

/* App items */
.apps-grid { display:flex; flex-direction:column; gap:1rem; margin-top:1rem; }
.app-item { background:rgba(110,231,183,0.03); border:1px solid var(--border); border-radius:15px; padding:1.5rem 2rem; display:flex; justify-content:space-between; align-items:flex-start; gap:1.5rem; transition:all 0.3s; position:relative; overflow:hidden; }
.app-item::before { content:''; position:absolute; top:0;left:0;right:0;height:3px; background:linear-gradient(90deg,var(--teal),#34d399); transform:translateX(-100%); transition:transform 0.5s; }
.app-item:hover::before { transform:translateX(0); }
.app-item:hover { border-color:var(--border-md); }
.app-info { flex:1; }
.app-info h3 { font-size:1.05rem; font-weight:700; color:#fff; margin-bottom:0.5rem; }
.app-info p { font-size:0.88rem; color:var(--text-dim); line-height:1.7; margin-bottom:0.75rem; }
.app-earn { text-align:right; flex-shrink:0; }
.earn-amt { font-size:1.3rem; font-weight:800; background:linear-gradient(135deg,#6ee7b7,#a7f3d0); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; font-family:'IBM Plex Mono',monospace; }
.earn-label { font-size:0.75rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.05em; }

/* Math box */
.math-box { background:var(--bg-darker); border:1px solid var(--border); border-radius:12px; overflow:hidden; margin-bottom:1.2rem; }
.math-box h3 { padding:1.2rem 1.5rem; font-size:1rem; font-weight:700; color:var(--teal); font-family:'IBM Plex Mono',monospace; background:rgba(110,231,183,0.07); border-bottom:1px solid var(--border); }
.math-rows { padding:0.5rem 1.5rem 1.2rem; }
.math-row { display:flex; justify-content:space-between; align-items:center; padding:0.6rem 0; border-bottom:1px solid var(--border); font-size:0.9rem; }
.math-row:last-child { border-bottom:none; }
.r-name, .card-name { color:var(--text-dim); }
.r-val, .card-value { color:var(--teal); font-weight:600; font-family:'IBM Plex Mono',monospace; }
.math-total { display:flex; justify-content:space-between; align-items:center; padding:0.8rem 0 0; margin-top:0.3rem; border-top:1px solid var(--border-md); font-size:0.95rem; font-weight:700; color:#fff; }

/* Synergy grid */
.synergy-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:1rem; margin-top:1.5rem; }
.synergy-card { background:rgba(110,231,183,0.04); border:1px solid var(--border); border-radius:12px; padding:1.5rem; transition:all 0.3s; }
.synergy-card:hover { border-color:var(--border-md); transform:translateY(-2px); }
.synergy-card h3 { font-size:0.95rem; font-weight:700; color:var(--teal); margin-bottom:0.75rem; }
.synergy-card p { font-size:0.85rem; color:var(--text-dim); line-height:1.7; }

/* CTA section */
.cta-section { background:rgba(110,231,183,0.06); border:2px solid rgba(110,231,183,0.25); border-radius:20px; padding:4rem 3rem; text-align:center; max-width:1200px; margin:0 auto 3rem; }
.cta-section h2 { font-size:2rem; font-weight:900; background:linear-gradient(135deg,#6ee7b7,#a7f3d0,#34d399); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; font-family:'IBM Plex Mono',monospace; margin-bottom:1rem; }
.cta-section p { color:var(--text-dim); font-size:1rem; line-height:1.7; max-width:600px; margin:0 auto 2rem; }

/* Credit cards page specific */
.cc-card { background:var(--bg-card); border:1px solid var(--border); border-left:4px solid var(--teal); border-radius:16px; padding:2rem; margin-bottom:1.5rem; max-width:1200px; margin-left:auto; margin-right:auto; box-shadow:0 8px 30px rgba(0,0,0,0.25); }
.cc-card-header { margin-bottom:1rem; }
.cc-best-for { display:inline-block; font-size:0.75rem; font-weight:700; color:var(--teal); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem; }
.cc-card-name { font-size:1.3rem; font-weight:800; color:#fff; font-family:'IBM Plex Mono',monospace; margin-bottom:0.5rem; }
.cc-rating { display:flex; align-items:center; gap:0.5rem; }
.cc-stars { font-size:0.9rem; }
.cc-rating-text { font-size:0.82rem; color:var(--text-dim); }
.cc-welcome { background:rgba(110,231,183,0.06); border:1px solid rgba(110,231,183,0.2); border-radius:10px; padding:1rem 1.25rem; margin-bottom:1.2rem; }
.cc-welcome-label { font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:var(--teal); margin-bottom:0.3rem; }
.cc-welcome-text { font-size:0.9rem; color:#fff; font-weight:600; }
.cc-card-body { display:grid; gap:1rem; }
.cc-rewards { background:rgba(110,231,183,0.04); border:1px solid var(--border); border-radius:8px; padding:1rem; }
.cc-rewards-label { font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:var(--teal); margin-bottom:0.3rem; }
.cc-rewards-text { font-size:0.88rem; color:var(--text-dim); line-height:1.6; }
.cc-details { display:grid; grid-template-columns:1fr 1fr; gap:0.75rem; }
.cc-detail { background:rgba(110,231,183,0.03); border:1px solid var(--border); border-radius:8px; padding:0.75rem 1rem; }
.cc-detail-label { font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:var(--text-muted); margin-bottom:0.25rem; }
.cc-detail-value { font-size:0.9rem; font-weight:700; color:#fff; font-family:'IBM Plex Mono',monospace; }
.cc-detail-value.free { color:var(--teal); }
.cc-detail-value.na { color:var(--text-muted); font-style:italic; }
.cc-apply-btn { display:inline-flex; align-items:center; gap:0.5rem; background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%); color:#060a0f; text-decoration:none; padding:0.7rem 1.5rem; border-radius:50px; font-size:0.9rem; font-weight:700; box-shadow:0 0 15px rgba(110,231,183,0.3); transition:all 0.2s; margin-top:0.75rem; }
.cc-apply-btn:hover { transform:translateY(-2px); box-shadow:0 0 25px rgba(110,231,183,0.5); }

/* Choose / how-to-pick section */
.choose-section { max-width:1200px; margin:0 auto 3rem; }
.section-header { text-align:center; margin-bottom:2rem; }
.section-header .section-title { font-size:1.75rem; font-weight:bold; color:#fff; font-family:'IBM Plex Mono',monospace; }
.highlight { background:linear-gradient(135deg,#6ee7b7,#a7f3d0); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.section-subtitle { color:var(--text-dim); font-size:0.95rem; margin-top:0.5rem; }
.choose-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:1rem; }
.choose-card { background:var(--bg-card); border:1px solid var(--border); border-radius:14px; padding:1.5rem; transition:all 0.3s; }
.choose-card:hover { border-color:var(--border-md); transform:translateY(-3px); box-shadow:0 10px 25px rgba(0,0,0,0.3); }
.choose-icon { font-size:1.8rem; margin-bottom:0.75rem; }
.choose-title { font-size:1rem; font-weight:800; color:#fff; margin-bottom:0.5rem; }
.choose-text { font-size:0.85rem; color:var(--text-dim); line-height:1.65; }
.choose-text strong { color:#fff; }

/* Disclaimer */
.disclaimer-section { max-width:1200px; margin:0 auto 3rem; }
.disclaimer-box { background:rgba(255,193,7,0.05); border:1px solid rgba(255,193,7,0.15); border-radius:12px; padding:1.25rem 1.5rem; }
.disclaimer-box p { font-size:0.78rem; color:rgba(220,200,140,0.7); line-height:1.6; margin:0; }

/* Fade-in */
.fade-in { opacity:0; transform:translateY(24px); transition:opacity 0.6s ease-out,transform 0.6s ease-out; }
.fade-in.visible { opacity:1; transform:translateY(0); }

@media(max-width:768px){
  .page-hero { padding:80px 1.25rem 40px; }
  .stats-section { padding:0 1.25rem; }
  .stats-grid { grid-template-columns:repeat(2,1fr); }
  .section { padding:2rem 1.25rem; border-radius:16px; }
  .cta-section { padding:2.5rem 1.25rem; }
  .app-item, .card-item { flex-direction:column; }
  .app-earn, .card-bonus { text-align:left; }
  .steps-grid { grid-template-columns:1fr 1fr; }
  .step-grid { grid-template-columns:1fr; }
  .synergy-grid, .choose-grid { grid-template-columns:1fr; }
  .cc-details { grid-template-columns:1fr; }
}
</style>
</head>'''

# Inline script to replace (same in credit-card-churning, freelancing, reward-apps, credit-cards)
OLD_INLINE_SCRIPT = ''' <script> // Nav scroll
 const nav = document.getElementById('nav');
 window.addEventListener('scroll', () => {
 nav.classList.toggle('scrolled', window.scrollY > 20);
 }, { passive: true });
 // Mobile menu
 const hamburger = document.getElementById('hamburger');
 const mobileMenu = document.getElementById('mobileMenu');
 hamburger.addEventListener('click', () => {
 hamburger.classList.toggle('active');
 mobileMenu.classList.toggle('active');
 document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
 });
 mobileMenu.querySelectorAll('a').forEach(link => {
 link.addEventListener('click', () => {
 hamburger.classList.remove('active');
 mobileMenu.classList.remove('active');
 document.body.style.overflow = '';
 });
 });
 // Fade-in
 const fadeObs = new IntersectionObserver((entries) => {
 entries.forEach(entry => {
 if (entry.isIntersecting) { entry.target.classList.add('visible'); fadeObs.unobserve(entry.target); }
 });
 }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
 document.querySelectorAll('.fade-in').forEach(el => fadeObs.observe(el));
 </script>'''

NEW_INLINE_SCRIPT = '''
<script>
// Fade-in observer
const fadeObs = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add('visible'); fadeObs.unobserve(entry.target); }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.fade-in').forEach(el => fadeObs.observe(el));
</script>'''

# ============================================================
# Process pages 1-4: add CSS + fix inline script
# ============================================================
PAGES = ['credit-card-churning.html', 'freelancing.html', 'reward-apps.html', 'credit-cards.html']

for fname in PAGES:
    with open(fname, encoding='utf-8') as f:
        content = f.read()

    # Fix theme-color
    content = content.replace('content="#050810"', 'content="#111c2e"')

    # Add RSA page CSS before </head>
    if '<style>\n/* ===== PAGE CONTENT' not in content:
        content = content.replace('</style>\n</head>', '</style>\n' + SHARED_PAGE_CSS)

    # Fix duplicate inline script
    if OLD_INLINE_SCRIPT in content:
        content = content.replace(OLD_INLINE_SCRIPT, NEW_INLINE_SCRIPT)
    else:
        print(f'  WARNING: inline script not found in {fname} — check manually')

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Processed {fname} — length: {len(content)}')


# ============================================================
# Process sweepstats.html — full RSA content rewrite
# ============================================================
with open('sweepstats.html', encoding='utf-8') as f:
    ss = f.read()

# Fix theme-color
ss = ss.replace('content="#050810"', 'content="#111c2e"')

# Add RSA page CSS before </head>
SWEEPSTATS_CSS = '''<style>
/* ===== SWEEPSTATS PAGE - RSA STYLE ===== */

/* Hero */
.ss-hero { text-align:center; padding:88px 2rem 60px; max-width:1200px; margin:0 auto; }
.ss-badge { display:inline-flex; align-items:center; gap:0.5rem; background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%); padding:0.5rem 1.2rem; border-radius:20px; color:#060a0f; font-family:'IBM Plex Mono',monospace; font-size:0.85rem; font-weight:700; letter-spacing:0.05em; animation:pulseBadge 2s infinite; box-shadow:0 0 30px rgba(110,231,183,0.4); margin-bottom:1.5rem; }
@keyframes pulseBadge { 0%,100%{box-shadow:0 0 30px rgba(110,231,183,0.4);} 50%{box-shadow:0 0 50px rgba(110,231,183,0.7);} }
.ss-hero h1 { font-size:clamp(2rem,4vw,3.5rem); font-weight:900; font-family:'IBM Plex Mono',monospace; margin:0 0 1rem; line-height:1.15; }
.ss-gradient { background:linear-gradient(135deg,#6ee7b7,#a7f3d0,#34d399); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.ss-hero p { color:var(--text-dim); font-size:1.1rem; max-width:680px; margin:0 auto 2rem; line-height:1.7; }
.ss-hero-btns { display:flex; gap:1rem; flex-wrap:wrap; justify-content:center; }
.btn-teal { display:inline-flex; align-items:center; gap:0.5rem; background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%); color:#060a0f; text-decoration:none; padding:0.9rem 2.2rem; border-radius:50px; font-size:1rem; font-weight:700; box-shadow:0 0 25px rgba(110,231,183,0.4); transition:transform 0.2s,box-shadow 0.2s; animation:ctaPulse 2.5s ease-in-out infinite; }
.btn-teal:hover { transform:translateY(-2px); box-shadow:0 0 40px rgba(110,231,183,0.6); }
@keyframes ctaPulse { 0%,100%{box-shadow:0 0 25px rgba(110,231,183,0.4);} 50%{box-shadow:0 0 45px rgba(110,231,183,0.65);} }
.btn-ghost { display:inline-flex; align-items:center; gap:0.5rem; background:transparent; color:var(--teal); text-decoration:none; padding:0.9rem 2.2rem; border-radius:50px; font-size:1rem; font-weight:700; border:2px solid rgba(110,231,183,0.35); transition:all 0.2s; }
.btn-ghost:hover { border-color:var(--teal); background:rgba(110,231,183,0.07); }

/* Stats */
.ss-stats { display:grid; grid-template-columns:repeat(4,1fr); gap:1.5rem; max-width:1200px; margin:0 auto 3rem; padding:0 2rem; }
.ss-stat { background:var(--bg-card); border:1px solid var(--border); border-radius:15px; padding:1.5rem; text-align:center; transition:all 0.3s; }
.ss-stat:hover { transform:translateY(-4px); box-shadow:0 10px 30px rgba(0,0,0,0.3); }
.ss-stat-num { font-size:1.8rem; font-weight:bold; background:linear-gradient(135deg,#6ee7b7,#a7f3d0); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; font-family:'IBM Plex Mono',monospace; margin-bottom:0.25rem; }
.ss-stat-lbl { color:var(--text-dim); font-size:0.8rem; text-transform:uppercase; letter-spacing:0.05em; }

/* Content sections */
.ss-section { background:var(--bg-card); border:1px solid var(--border); border-left:4px solid var(--teal); border-radius:20px; padding:3rem; margin-bottom:3rem; max-width:1200px; margin-left:auto; margin-right:auto; box-shadow:0 10px 40px rgba(0,0,0,0.3); }
.ss-section-title { font-size:1.75rem; font-weight:bold; color:var(--teal); font-family:'IBM Plex Mono',monospace; display:flex; align-items:center; gap:0.75rem; margin-bottom:1.5rem; }
.ss-section-sub { color:var(--text-dim); font-size:0.95rem; line-height:1.8; margin-bottom:2rem; }

/* Feature grid */
.feature-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin-top:1.5rem; }
.feature-card { background:rgba(110,231,183,0.04); border:1px solid var(--border); border-radius:14px; padding:1.6rem; transition:all 0.3s; position:relative; overflow:hidden; }
.feature-card::before { content:''; position:absolute; top:0;left:0;right:0;height:3px; background:linear-gradient(90deg,var(--teal),#34d399); transform:translateX(-100%); transition:transform 0.5s; }
.feature-card:hover::before { transform:translateX(0); }
.feature-card:hover { border-color:var(--border-md); transform:translateY(-3px); box-shadow:0 10px 25px rgba(0,0,0,0.3); }
.feature-icon { font-size:1.8rem; margin-bottom:0.8rem; }
.feature-card h3 { font-size:1rem; font-weight:700; color:#fff; margin-bottom:0.5rem; font-family:'IBM Plex Mono',monospace; }
.feature-card p { font-size:0.85rem; color:var(--text-dim); line-height:1.65; }

/* Steps */
.ss-steps { display:flex; flex-direction:column; gap:1rem; margin-top:1.5rem; }
.ss-step { background:rgba(110,231,183,0.03); border:1px solid var(--border); border-radius:14px; padding:1.4rem 1.5rem; display:flex; gap:1.2rem; align-items:flex-start; transition:border-color 0.2s,transform 0.2s; position:relative; overflow:hidden; }
.ss-step::before { content:''; position:absolute; top:0;left:0;bottom:0;width:3px; background:linear-gradient(180deg,var(--teal),#34d399); opacity:0.7; }
.ss-step:hover { border-color:var(--border-md); transform:translateX(4px); }
.ss-step-num { width:40px; height:40px; min-width:40px; background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%); border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1rem; color:#060a0f; box-shadow:0 0 15px rgba(110,231,183,0.4); }
.ss-step-body h3 { font-size:1.05rem; font-weight:800; color:#fff; margin:0 0 0.4rem; }
.ss-step-body p { font-size:0.88rem; color:var(--text-dim); line-height:1.65; margin:0; }

/* Why use box */
.why-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:1rem; margin-top:1.5rem; }
.why-item { background:rgba(110,231,183,0.04); border:1px solid var(--border); border-radius:12px; padding:1.25rem 1.5rem; display:flex; gap:1rem; align-items:flex-start; }
.why-check { color:var(--teal); font-size:1.2rem; flex-shrink:0; margin-top:2px; }
.why-item h4 { font-size:0.92rem; font-weight:700; color:#fff; margin-bottom:0.3rem; }
.why-item p { font-size:0.82rem; color:var(--text-dim); line-height:1.55; margin:0; }

/* CTA */
.ss-cta { background:rgba(110,231,183,0.06); border:2px solid rgba(110,231,183,0.25); border-radius:20px; padding:4rem 3rem; text-align:center; max-width:1200px; margin:0 auto 3rem; }
.ss-cta h2 { font-size:2rem; font-weight:900; background:linear-gradient(135deg,#6ee7b7,#a7f3d0,#34d399); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; font-family:'IBM Plex Mono',monospace; margin-bottom:1rem; }
.ss-cta p { color:var(--text-dim); font-size:1rem; line-height:1.7; max-width:620px; margin:0 auto 2rem; }

/* Fade */
.fade-in { opacity:0; transform:translateY(24px); transition:opacity 0.6s ease-out,transform 0.6s ease-out; }
.fade-in.visible { opacity:1; transform:translateY(0); }

@media(max-width:768px){
  .ss-hero { padding:80px 1.25rem 40px; }
  .ss-stats { grid-template-columns:repeat(2,1fr); padding:0 1.25rem; }
  .ss-section { padding:2rem 1.25rem; border-radius:16px; }
  .feature-grid { grid-template-columns:1fr 1fr; }
  .ss-cta { padding:2.5rem 1.25rem; }
  .why-grid { grid-template-columns:1fr; }
}
</style>
</head>'''

ss = ss.replace('</style>\n</head>', '</style>\n' + SWEEPSTATS_CSS)

# Replace page content between <!-- PAGE CONTENT --> and <!-- FOOTER -->
OLD_SS_CONTENT = '''<!-- PAGE CONTENT -->
<div class="content-area" style="padding-top:80px;">
  <div class="container">
<section class="page-hero">
        <div class="container">
            <span class="badge fade-in">Community Spotlight</span>
            <h1 class="fade-in fade-in-delay-1"><span class="emerald">SweepStats</span> Transaction Tracker</h1>
            <p class="subtitle fade-in fade-in-delay-2">A free sweepstakes transaction tracker built by the community. Track deposits, redemptions, and profit across all your sweepstakes casinos with dashboards, charts, and CSV import.</p>
        </div>
    </section>

    <hr class="divider">
    <section class="section">
        <div class="container">
            <p class="section-label fade-in">Features</p>
            <div class="feature-grid fade-in">
                <div class="feature-card"><h3>Dashboard Overview</h3><p>See your total deposits, redemptions, and net profit across all casinos in one clean dashboard view.</p></div>
                <div class="feature-card"><h3>Per-Casino Tracking</h3><p>Break down performance by individual casino to see which sites are most profitable for you.</p></div>
                <div class="feature-card"><h3>Charts & Trends</h3><p>Visualize your earnings over time with interactive charts. Spot trends and optimize your strategy.</p></div>
                <div class="feature-card"><h3>CSV Import</h3><p>Import your transaction history from bank statements or casino exports to get started quickly.</p></div>
                <div class="feature-card"><h3>Free & Open</h3><p>Built by the community, for the community. Completely free to use with no hidden fees or premium tiers.</p></div>
                <div class="feature-card"><h3>Privacy First</h3><p>Your data stays on your device. No account required, no data sent to external servers.</p></div>
            </div>

            <div style="text-align:center;margin-top:48px;" class="fade-in">
                <a href="https://discord.gg/W9bPGH8crh" class="btn-primary" target="_blank">Join Discord to Access SweepStats</a>
            </div>
        </div>
    </section>



  </div>
</div>'''

NEW_SS_CONTENT = '''<!-- PAGE CONTENT -->
<div class="content-area">
  <div class="container">

    <!-- HERO -->
    <div class="ss-hero fade-in">
      <div class="ss-badge">📊 Community-Built Tool</div>
      <h1><span class="ss-gradient">SweepStats</span><br>Transaction Tracker</h1>
      <p>The free sweepstakes portfolio tracker built by the community. Track every deposit, redemption, and profit across all your casinos — with dashboards, charts, per-casino breakdowns, and CSV import. No account required.</p>
      <div class="ss-hero-btns">
        <a href="https://www.sweepstats.com/" class="btn-teal" target="_blank" rel="noopener">🚀 Open SweepStats</a>
        <a href="https://discord.gg/W9bPGH8crh" class="btn-ghost" target="_blank" rel="noopener">Join Community</a>
      </div>
    </div>

    <!-- STATS -->
    <div class="ss-stats fade-in">
      <div class="ss-stat">
        <div class="ss-stat-num">$0</div>
        <div class="ss-stat-lbl">Cost — Free Forever</div>
      </div>
      <div class="ss-stat">
        <div class="ss-stat-num">100%</div>
        <div class="ss-stat-lbl">Privacy — Data Stays Local</div>
      </div>
      <div class="ss-stat">
        <div class="ss-stat-num">All</div>
        <div class="ss-stat-lbl">Casinos Supported</div>
      </div>
      <div class="ss-stat">
        <div class="ss-stat-num">Live</div>
        <div class="ss-stat-lbl">Charts & Dashboard</div>
      </div>
    </div>

    <!-- WHAT IS IT -->
    <div class="ss-section fade-in">
      <div class="ss-section-title">📊 What is SweepStats?</div>
      <p class="ss-section-sub">SweepStats is a free web-based tool built specifically for sweepstakes casino players. It solves one of the biggest pain points in sweepstakes: <strong style="color:#fff;">knowing your actual numbers.</strong></p>
      <p style="color:var(--text-dim);font-size:0.95rem;line-height:1.8;margin-bottom:1.5rem;">Most players have a rough idea of whether they're up or down, but no clear picture of their ROI per casino, which sites are actually paying out, or what their total profit/loss is across the board. SweepStats gives you that clarity — in real time, for free, with no signup required.</p>
      <div style="background:rgba(110,231,183,0.06);border:1px solid rgba(110,231,183,0.2);border-left:4px solid var(--teal);border-radius:10px;padding:1.5rem;margin-top:1rem;">
        <h4 style="color:var(--teal);font-size:0.95rem;font-weight:700;margin-bottom:0.6rem;">💡 Built by the Community</h4>
        <p style="color:var(--text-dim);font-size:0.9rem;line-height:1.7;margin:0;">SweepStats was created by a member of the sweepstakes community who wanted a better way to track profits. It's free, open, and continuously improved based on community feedback. Find it and discuss it in our Discord server.</p>
      </div>
    </div>

    <!-- FEATURES -->
    <div class="ss-section fade-in">
      <div class="ss-section-title">⚡ Features</div>
      <div class="feature-grid">
        <div class="feature-card">
          <div class="feature-icon">📈</div>
          <h3>Dashboard Overview</h3>
          <p>See your total deposits, redemptions, and net profit across all casinos in one clean view. Know your overall numbers at a glance.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🎰</div>
          <h3>Per-Casino Breakdown</h3>
          <p>See exactly which casinos are profitable for you and which aren't. Stop wasting time on sites with poor ROI and double down on winners.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📉</div>
          <h3>Charts & Trends</h3>
          <p>Visualize your earnings over time with interactive charts. Spot seasonal trends, track your growth, and identify your best months.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📂</div>
          <h3>CSV Import</h3>
          <p>Import your transaction history from bank statements or casino transaction exports. Get started in minutes with your existing data.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🔒</div>
          <h3>Privacy First</h3>
          <p>Your financial data stays on your device. No account required, no data sent to external servers. Your numbers are yours alone.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🆓</div>
          <h3>Free & Open</h3>
          <p>Built by the community, for the community. Completely free to use with no hidden fees, no premium tiers, no paywalls — ever.</p>
        </div>
      </div>
    </div>

    <!-- HOW TO USE -->
    <div class="ss-section fade-in">
      <div class="ss-section-title">🚀 How to Get Started</div>
      <p class="ss-section-sub">Takes less than 5 minutes to set up. No account, no downloads, no credit card.</p>
      <div class="ss-steps">
        <div class="ss-step">
          <div class="ss-step-num">1</div>
          <div class="ss-step-body">
            <h3>Visit sweepstats.com</h3>
            <p>Open the tool directly in your browser at sweepstats.com. No installation, no signup. It runs entirely in your browser.</p>
          </div>
        </div>
        <div class="ss-step">
          <div class="ss-step-num">2</div>
          <div class="ss-step-body">
            <h3>Add Your Casinos</h3>
            <p>Create entries for each sweepstakes casino you play. Add the casino name and start logging your transactions manually, or use CSV import if you have existing data.</p>
          </div>
        </div>
        <div class="ss-step">
          <div class="ss-step-num">3</div>
          <div class="ss-step-body">
            <h3>Log Deposits & Redemptions</h3>
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
      <div class="ss-section-title">✅ Why Tracking Matters</div>
      <p class="ss-section-sub">Most people think they're making more than they are — or don't know they're losing on certain sites. Data changes everything.</p>
      <div class="why-grid">
        <div class="why-item">
          <div class="why-check">✓</div>
          <div>
            <h4>Know Your Actual ROI</h4>
            <p>Package welcome bonuses look attractive on paper. Tracking reveals which ones actually pay off after wagering requirements and time spent.</p>
          </div>
        </div>
        <div class="why-item">
          <div class="why-check">✓</div>
          <div>
            <h4>Cut Losing Sites</h4>
            <p>Some casinos simply pay out less for you. Data lets you identify which sites to drop and reallocate that bankroll to better performers.</p>
          </div>
        </div>
        <div class="why-item">
          <div class="why-check">✓</div>
          <div>
            <h4>Optimize Your Bankroll</h4>
            <p>See which sites give the best returns and shift more of your capital there. Small optimizations compound significantly over time.</p>
          </div>
        </div>
        <div class="why-item">
          <div class="why-check">✓</div>
          <div>
            <h4>Tax Record Keeping</h4>
            <p>Having a clean log of all deposits and redemptions makes tax time straightforward. Know exactly what you earned and spent on each platform.</p>
          </div>
        </div>
        <div class="why-item">
          <div class="why-check">✓</div>
          <div>
            <h4>Track Multiple Accounts</h4>
            <p>Running the Player 2 strategy? Track each account separately and see which of your managed accounts are the most profitable.</p>
          </div>
        </div>
        <div class="why-item">
          <div class="why-check">✓</div>
          <div>
            <h4>Motivation & Accountability</h4>
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
        <a href="https://www.sweepstats.com/" class="btn-teal" target="_blank" rel="noopener">🚀 Open SweepStats Free</a>
        <a href="https://discord.gg/W9bPGH8crh" class="btn-ghost" target="_blank" rel="noopener">💬 Join Discord Community</a>
      </div>
    </div>

  </div>
</div>'''

ss = ss.replace(OLD_SS_CONTENT, NEW_SS_CONTENT)

# Also add fade-in observer script before the bgCanvas script block
OLD_SS_SCRIPT_AREA = '// ===== BACKGROUND STARFIELD ====='
ss = ss.replace(
    '// ===== BACKGROUND STARFIELD =====',
    '''// Fade-in observer
const fadeObs = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add('visible'); fadeObs.unobserve(entry.target); }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.fade-in').forEach(el => fadeObs.observe(el));

// ===== BACKGROUND STARFIELD ====='''
)

with open('sweepstats.html', 'w', encoding='utf-8') as f:
    f.write(ss)
print(f'Processed sweepstats.html — length: {len(ss)}')

print('\nAll done!')
