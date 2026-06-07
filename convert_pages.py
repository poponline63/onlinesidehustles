import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ── Pull RSA building blocks from a known-good page ──────────────────
ref = open('credit-card-churning.html', encoding='utf-8').read()
RSA_CSS    = ref[ref.find('<style>'):ref.find('</style>')+8]
BOT_SCRIPT = ref[ref.rfind('<script>'):ref.rfind('</script>')+9]

FONTS = (
    '    <link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&family=Inter:wght@400;500;600;700;900&display=swap" rel="stylesheet">\n'
)

BG_ELEMENTS = (
    '<canvas id="bgCanvas"></canvas>\n'
    '<div class="bg-orb" style="width:820px;height:820px;top:-220px;right:-180px;background:radial-gradient(circle,rgba(110,231,183,0.18) 0%,transparent 70%);--dur:32s;--tx:70px;--ty:55px;--ts:1.06;"></div>\n'
    '<div class="bg-orb" style="width:640px;height:640px;bottom:-160px;left:-160px;background:radial-gradient(circle,rgba(192,132,252,0.16) 0%,transparent 70%);--dur:40s;--tx:-55px;--ty:-65px;--ts:1.12;"></div>\n'
    '<div class="bg-orb" style="width:420px;height:420px;top:38%;left:2%;background:radial-gradient(circle,rgba(96,165,250,0.1) 0%,transparent 70%);--dur:24s;--tx:45px;--ty:35px;--ts:0.92;"></div>\n'
    '<div class="bg-grid"></div>\n'
    '<div class="bg-scanlines"></div>\n'
    '<div class="bg-vignette"></div>\n'
)

DISCORD_WIDGET = (
    '<a class="discord-widget" id="discordWidget" href="https://discord.com/invite/W9bPGH8crh" target="_blank" rel="noopener">'
    '<button class="discord-x" id="discordClose" aria-label="Dismiss">&#x2715;</button>'
    '<svg class="discord-icon" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M23.12 5.48A22.36 22.36 0 0 0 17.7 3.8a15.3 15.3 0 0 0-.7 1.44 20.67 20.67 0 0 0-6.02 0A15.3 15.3 0 0 0 10.3 3.8a22.41 22.41 0 0 0-5.44 1.68C1.88 10.04 1.1 14.48 1.5 18.86a22.6 22.6 0 0 0 6.82 3.42c.55-.74 1.04-1.53 1.46-2.36a14.66 14.66 0 0 1-2.3-1.1c.19-.14.38-.28.56-.43a16.06 16.06 0 0 0 13.92 0c.18.15.37.29.56.43a14.6 14.6 0 0 1-2.31 1.1c.42.83.91 1.62 1.46 2.36a22.53 22.53 0 0 0 6.82-3.42c.47-4.96-.8-9.36-3.37-13.38ZM9.68 16.28c-1.3 0-2.36-1.18-2.36-2.64s1.04-2.64 2.36-2.64 2.38 1.18 2.36 2.64c0 1.46-1.05 2.64-2.36 2.64Zm8.64 0c-1.3 0-2.36-1.18-2.36-2.64s1.04-2.64 2.36-2.64 2.38 1.18 2.36 2.64c0 1.46-1.04 2.64-2.36 2.64Z" fill="white"/></svg>'
    '<div class="discord-text"><span class="discord-title">Join Discord</span><span class="discord-sub">Free SC alerts &amp; tips</span></div></a>\n'
    "<script>(function(){var w=document.getElementById('discordWidget'),c=document.getElementById('discordClose');if(!w)return;if(localStorage.getItem('dcDismissed'))w.style.display='none';if(c)c.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();w.style.animation='none';w.style.transition='transform 0.3s,opacity 0.3s';w.style.transform='translateX(-130%)';w.style.opacity='0';setTimeout(function(){w.style.display='none';},300);localStorage.setItem('dcDismissed','1');});})();</script>\n"
)

NAV_HTML = (
    '<nav id="nav">\n'
    '  <div class="nav-inner">\n'
    '    <a href="/" class="nav-brand">\n'
    '      <img src="/logo.png" alt="Online Sidehustles" class="nav-logo" style="height:22px;width:auto;">\n'
    '      ONLINE SIDEHUSTLES\n'
    '    </a>\n'
    '    <div class="nav-links">\n'
    '      <a href="/getting-started" class="nav-link">Get Started</a>\n'
    '      <a href="/sweepstakes-casino-list" class="nav-link">Sweepstakes Casinos List</a>\n'
    '      <a href="/casino-reviews" class="nav-link">Casino Reviews</a>\n'
    '      <a href="/side-hustles" class="nav-link">Side Hustles</a>\n'
    '      <a href="/tools" class="nav-link">Tools</a>\n'
    '      <a href="/blog" class="nav-link">Blog</a>\n'
    '      <a href="https://discord.gg/W9bPGH8crh" class="nav-cta" target="_blank" rel="noopener">Join Discord</a>\n'
    '    </div>\n'
    '    <button class="nav-hamburger" id="hamburger" aria-label="Menu">\n'
    '      <span></span><span></span><span></span>\n'
    '    </button>\n'
    '  </div>\n'
    '</nav>\n'
    '<div class="mobile-menu" id="mobileMenu">\n'
    '  <a href="/getting-started">Get Started</a>\n'
    '  <a href="/sweepstakes-casino-list">Sweepstakes Casinos List</a>\n'
    '  <a href="/casino-reviews">Casino Reviews</a>\n'
    '  <a href="/side-hustles">Side Hustles</a>\n'
    '  <a href="/tools">Tools</a>\n'
    '  <a href="/blog">Blog</a>\n'
    '  <a href="https://discord.gg/W9bPGH8crh" target="_blank" rel="noopener">Join Discord</a>\n'
    '</div>\n'
)

FOOTER_HTML = (
    '<footer>\n'
    '  <div class="footer-inner">\n'
    '    <div class="footer-grid">\n'
    '      <div>\n'
    '        <div class="footer-brand">Online Sidehustles</div>\n'
    '        <p class="footer-tagline">Free guides, community tips, and automation tools for earning from sweepstakes casinos and daily login sites.</p>\n'
    '      </div>\n'
    '      <div class="footer-col">\n'
    '        <h4>Guides</h4>\n'
    '        <a href="/sweepstakes-casino-list">Sweepstakes Casinos List</a>\n'
    '        <a href="/getting-started">Getting Started</a>\n'
    '        <a href="/side-hustles">Side Hustles</a>\n'
    '        <a href="/blog">Blog</a>\n'
    '        <a href="/daily-free-sc">Daily Free SC</a>\n'
    '        <a href="/new-sites">New Sites</a>\n'
    '      </div>\n'
    '      <div class="footer-col">\n'
    '        <h4>Resources</h4>\n'
    '        <a href="/tools">Tools</a>\n'
    '        <a href="/sweepstakes">Sweepstakes</a>\n'
    '        <a href="/faq">FAQ</a>\n'
    '        <a href="/casino-reviews">Casino Reviews</a>\n'
    '      </div>\n'
    '      <div class="footer-col">\n'
    '        <h4>Community</h4>\n'
    '        <a href="https://discord.gg/W9bPGH8crh" target="_blank" rel="noopener">Discord</a>\n'
    '      </div>\n'
    '    </div>\n'
    '    <div class="footer-bottom">\n'
    '      <span class="footer-copy">&#169; 2026 Online Sidehustles &#xB7; All rights reserved</span>\n'
    '      <div class="footer-links">\n'
    '        <a href="/privacy">Privacy</a>\n'
    '        <a href="/terms">Terms</a>\n'
    '        <a href="/disclaimer">Disclaimer</a>\n'
    '      </div>\n'
    '    </div>\n'
    '  </div>\n'
    '</footer>\n'
)

FADE_IN_SCRIPT = (
    '<script>\n'
    'const _fi=new IntersectionObserver(e=>{e.forEach(x=>{if(x.isIntersecting){x.target.classList.add("visible");_fi.unobserve(x.target);}});},{threshold:0.1,rootMargin:"0px 0px -40px 0px"});\n'
    'document.querySelectorAll(".fade-in").forEach(el=>_fi.observe(el));\n'
    '</script>\n'
)

# ── Per-page CSS ──────────────────────────────────────────────────────
PAGE_CSS = {}

PAGE_CSS['comparisons/best-welcome-packages.html'] = """<style>
.page-hero{text-align:center;padding:80px 2rem 40px;max-width:1200px;margin:0 auto;}
.page-hero h1{font-size:clamp(2rem,4vw,3rem);font-weight:900;font-family:'IBM Plex Mono',monospace;color:#fff;margin-bottom:.75rem;}
.page-hero p{color:var(--text-dim);font-size:1.1rem;line-height:1.7;max-width:700px;margin:0 auto;}
.info-box{background:rgba(110,231,183,.06);border:1px solid rgba(110,231,183,.2);border-left:4px solid var(--teal);border-radius:12px;padding:1.5rem 2rem;margin:0 auto 2rem;max-width:1200px;}
.info-box h3{color:var(--teal);font-size:1rem;font-weight:700;margin-bottom:.5rem;font-family:'IBM Plex Mono',monospace;}
.info-box p{color:var(--text-dim);font-size:.9rem;line-height:1.7;}
.info-box a{color:var(--teal);}
.pkg-card{background:var(--bg-card);border:1px solid var(--border);border-left:4px solid var(--teal);border-radius:16px;padding:2rem;margin:0 auto 1.5rem;max-width:1200px;box-shadow:0 8px 30px rgba(0,0,0,.25);transition:transform .2s;}
.pkg-card:hover{transform:translateY(-2px);}
.pkg-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:.75rem;gap:1rem;flex-wrap:wrap;}
.pkg-name{font-size:1.15rem;font-weight:800;color:#fff;font-family:'IBM Plex Mono',monospace;}
.pkg-bonus{font-size:1.35rem;font-weight:900;background:linear-gradient(135deg,#6ee7b7,#a7f3d0);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-family:'IBM Plex Mono',monospace;}
.pkg-details{color:var(--text-dim);font-size:.92rem;line-height:1.7;margin-bottom:1.25rem;}
.pkg-breakdown{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1.25rem;}
@media(max-width:700px){.pkg-breakdown{grid-template-columns:repeat(2,1fr);}}
.pkg-stat{background:rgba(110,231,183,.04);border:1px solid var(--border);border-radius:8px;padding:.75rem 1rem;text-align:center;}
.pkg-stat .label{font-size:.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:.3rem;}
.pkg-stat .value{font-size:.9rem;font-weight:700;color:#fff;font-family:'IBM Plex Mono',monospace;}
.pkg-stat .value.gold{background:linear-gradient(135deg,#6ee7b7,#a7f3d0);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.pkg-cta{text-align:right;}
.pkg-cta a{display:inline-flex;align-items:center;gap:.5rem;background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%);color:#060a0f;text-decoration:none;padding:.7rem 1.6rem;border-radius:50px;font-size:.9rem;font-weight:700;box-shadow:0 0 15px rgba(110,231,183,.3);transition:all .2s;}
.pkg-cta a:hover{transform:translateY(-2px);box-shadow:0 0 25px rgba(110,231,183,.5);}
.fade-in{opacity:0;transform:translateY(20px);transition:opacity .6s,transform .6s;}
.fade-in.visible{opacity:1;transform:translateY(0);}
</style>"""

PAGE_CSS['comparisons/chumba-vs-stake.html'] = """<style>
.vs-hero{text-align:center;padding:80px 2rem 40px;max-width:1200px;margin:0 auto;}
.vs-hero h1{font-size:clamp(1.8rem,4vw,3rem);font-weight:900;font-family:'IBM Plex Mono',monospace;color:#fff;margin-bottom:.5rem;}
.vs-hero p{color:var(--text-dim);font-size:1rem;line-height:1.7;}
.vs-header{display:flex;justify-content:center;align-items:center;gap:2.5rem;margin:0 auto 2rem;flex-wrap:wrap;max-width:1200px;padding:0 2rem;}
.vs-site{text-align:center;}
.vs-site h2{font-size:1.4rem;font-weight:900;color:#fff;font-family:'IBM Plex Mono',monospace;}
.tagline{color:var(--text-dim);font-size:.85rem;margin-top:.25rem;}
.vs-badge{font-size:2.5rem;font-weight:900;color:var(--teal);font-family:'IBM Plex Mono',monospace;}
.compare-section{max-width:1200px;margin:0 auto 2rem;padding:0 2rem;}
.compare-table{width:100%;border-collapse:collapse;background:var(--bg-card);border-radius:14px;overflow:hidden;border:1px solid var(--border);}
.compare-table th,.compare-table td{padding:.8rem 1.1rem;text-align:left;font-size:.88rem;border-bottom:1px solid var(--border);}
.compare-table th{background:rgba(110,231,183,.08);color:var(--teal);font-family:'IBM Plex Mono',monospace;font-weight:700;text-transform:uppercase;letter-spacing:.05em;font-size:.75rem;}
.compare-table td:first-child{color:var(--text-muted);}
.compare-table td:not(:first-child){color:#fff;}
.winner{color:var(--teal)!important;font-weight:700;}
.loser{color:#f87171!important;}
.tie{color:#fbbf24!important;}
.gold{background:linear-gradient(135deg,#6ee7b7,#a7f3d0);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-weight:800;}
.pros-cons{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;max-width:1200px;margin:0 auto 2rem;padding:0 2rem;}
@media(max-width:700px){.pros-cons{grid-template-columns:1fr;}}
.pros-cons-card{background:var(--bg-card);border:1px solid var(--border);border-radius:14px;padding:1.5rem;}
.pros-cons-card h3{font-size:1rem;font-weight:800;color:#fff;margin-bottom:1rem;font-family:'IBM Plex Mono',monospace;}
.pros,.cons{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:.5rem;}
.pros li,.cons li{font-size:.88rem;color:var(--text-dim);line-height:1.6;padding-left:1.4rem;position:relative;}
.pros li::before{content:"checkmark";content:"\\2713";position:absolute;left:0;color:var(--teal);font-weight:700;}
.cons li::before{content:"\\2717";position:absolute;left:0;color:#f87171;font-weight:700;}
.verdict{background:var(--bg-card);border:1px solid var(--border);border-left:4px solid var(--teal);border-radius:14px;padding:2rem;max-width:1200px;margin:0 auto 2rem;}
.verdict h3{color:var(--teal);font-family:'IBM Plex Mono',monospace;margin-bottom:.75rem;}
.verdict p{color:var(--text-dim);font-size:.92rem;line-height:1.7;}
.cta-row{display:flex;gap:1rem;flex-wrap:wrap;justify-content:center;margin:1.5rem 0 3rem;}
.cta-btn{display:inline-flex;align-items:center;gap:.5rem;background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%);color:#060a0f;text-decoration:none;padding:.8rem 1.8rem;border-radius:50px;font-size:.9rem;font-weight:700;box-shadow:0 0 15px rgba(110,231,183,.3);transition:all .2s;}
.cta-btn:hover{transform:translateY(-2px);}
.fade-in{opacity:0;transform:translateY(20px);transition:opacity .6s,transform .6s;}
.fade-in.visible{opacity:1;transform:translateY(0);}
</style>"""

PAGE_CSS['comparisons/fastest-payout-sites.html'] = """<style>
.page-hero{text-align:center;padding:80px 2rem 40px;max-width:1200px;margin:0 auto;}
.page-hero h1{font-size:clamp(2rem,4vw,3rem);font-weight:900;font-family:'IBM Plex Mono',monospace;color:#fff;margin-bottom:.75rem;}
.page-hero p{color:var(--text-dim);font-size:1.1rem;line-height:1.7;max-width:700px;margin:0 auto;}
.rank-card{background:var(--bg-card);border:1px solid var(--border);border-radius:16px;padding:2rem;margin:0 auto 1.5rem;max-width:1200px;display:flex;gap:1.5rem;align-items:flex-start;position:relative;overflow:hidden;transition:transform .2s;}
.rank-card:hover{transform:translateY(-2px);}
.rank-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--teal),#34d399);}
.rank-1::before{background:linear-gradient(90deg,#fbbf24,#f59e0b);}
.rank-2::before{background:linear-gradient(90deg,#94a3b8,#cbd5e1);}
.rank-3::before{background:linear-gradient(90deg,#cd7f32,#b87333);}
.rank-num{width:52px;height:52px;min-width:52px;background:linear-gradient(135deg,#6ee7b7,#34d399);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.3rem;font-weight:900;color:#060a0f;font-family:'IBM Plex Mono',monospace;box-shadow:0 0 20px rgba(110,231,183,.4);}
.rank-1 .rank-num{background:linear-gradient(135deg,#fbbf24,#f59e0b);box-shadow:0 0 20px rgba(251,191,36,.4);}
.rank-2 .rank-num{background:linear-gradient(135deg,#94a3b8,#cbd5e1);box-shadow:none;}
.rank-3 .rank-num{background:linear-gradient(135deg,#cd7f32,#b87333);}
.rank-info{flex:1;}
.rank-info h3{font-size:1.15rem;font-weight:800;color:#fff;font-family:'IBM Plex Mono',monospace;margin-bottom:.5rem;}
.rank-info p{color:var(--text-dim);font-size:.9rem;line-height:1.7;margin-bottom:.75rem;}
.rank-details{display:flex;flex-wrap:wrap;gap:.6rem;margin-bottom:.75rem;}
.speed-badge{display:inline-block;font-size:.72rem;font-weight:700;padding:.2rem .7rem;border-radius:20px;text-transform:uppercase;letter-spacing:.05em;}
.speed-fast{background:rgba(110,231,183,.12);color:#6ee7b7;border:1px solid rgba(110,231,183,.25);}
.speed-medium{background:rgba(251,191,36,.1);color:#fbbf24;border:1px solid rgba(251,191,36,.22);}
.rank-cta a{display:inline-flex;align-items:center;gap:.4rem;background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%);color:#060a0f;text-decoration:none;padding:.55rem 1.2rem;border-radius:50px;font-size:.82rem;font-weight:700;transition:all .2s;}
.rank-cta a:hover{transform:translateY(-2px);box-shadow:0 0 20px rgba(110,231,183,.4);}
.tip-box{background:rgba(110,231,183,.06);border:1px solid rgba(110,231,183,.2);border-left:4px solid var(--teal);border-radius:12px;padding:1.5rem 2rem;margin:0 auto 2rem;max-width:1200px;}
.tip-box h3{color:var(--teal);font-family:'IBM Plex Mono',monospace;font-size:.95rem;font-weight:700;margin-bottom:.5rem;}
.tip-box p{color:var(--text-dim);font-size:.9rem;line-height:1.7;}
.fade-in{opacity:0;transform:translateY(20px);transition:opacity .6s,transform .6s;}
.fade-in.visible{opacity:1;transform:translateY(0);}
</style>"""

PAGE_CSS['daily-login-reviews.html'] = """<style>
.hero{text-align:center;padding:80px 2rem 40px;max-width:900px;margin:0 auto;}
.hero h1{font-size:clamp(2rem,4vw,3rem);font-weight:900;font-family:'IBM Plex Mono',monospace;color:#fff;margin-bottom:.75rem;}
.hero-subtitle{color:var(--text-dim);font-size:1.1rem;line-height:1.7;max-width:680px;margin:0 auto;}
.section{background:var(--bg-card);border:1px solid var(--border);border-left:4px solid var(--teal);border-radius:16px;padding:2.5rem;margin:0 auto 2rem;max-width:1200px;box-shadow:0 8px 30px rgba(0,0,0,.25);}
.section h2{font-size:1.4rem;font-weight:800;color:#fff;font-family:'IBM Plex Mono',monospace;margin-bottom:1rem;}
.section h3{font-size:1.1rem;font-weight:700;color:var(--teal);margin-bottom:.75rem;}
.content-block{color:var(--text-dim);font-size:.92rem;line-height:1.8;}
.content-block p{margin-bottom:.75rem;}
.content-block a{color:var(--teal);}
.content-block strong{color:#fff;}
.divider{height:1px;background:var(--border);max-width:1200px;margin:1.5rem auto;}
.cta-section{background:rgba(110,231,183,.06);border:2px solid rgba(110,231,183,.25);border-radius:20px;padding:3rem 2rem;text-align:center;max-width:1200px;margin:0 auto 3rem;}
.cta-title{font-size:1.75rem;font-weight:900;background:linear-gradient(135deg,#6ee7b7,#a7f3d0,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-family:'IBM Plex Mono',monospace;margin-bottom:.75rem;}
.cta-subtitle{color:var(--text-dim);font-size:.95rem;line-height:1.7;max-width:600px;margin:0 auto 1.5rem;}
.btn-cta{display:inline-flex;align-items:center;gap:.5rem;background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%);color:#060a0f;text-decoration:none;padding:.85rem 2rem;border-radius:50px;font-size:1rem;font-weight:700;box-shadow:0 0 20px rgba(110,231,183,.4);transition:all .2s;}
.btn-cta:hover{transform:translateY(-2px);box-shadow:0 0 35px rgba(110,231,183,.6);}
.fade-in{opacity:0;transform:translateY(20px);transition:opacity .6s,transform .6s;}
.fade-in.visible{opacity:1;transform:translateY(0);}
</style>"""

PAGE_CSS['reports/february-2026.html'] = """<style>
.rpt-header{text-align:center;padding:80px 2rem 40px;max-width:900px;margin:0 auto;}
.header-brand{font-size:.85rem;font-weight:700;color:var(--teal);text-transform:uppercase;letter-spacing:.1em;font-family:'IBM Plex Mono',monospace;margin-bottom:.75rem;}
.date{display:inline-block;background:rgba(110,231,183,.1);border:1px solid rgba(110,231,183,.2);border-radius:20px;padding:.3rem .9rem;font-size:.8rem;color:var(--teal);font-family:'IBM Plex Mono',monospace;margin-bottom:.75rem;}
.rpt-header h1{font-size:clamp(1.8rem,3.5vw,2.8rem);font-weight:900;color:#fff;font-family:'IBM Plex Mono',monospace;margin-bottom:.5rem;}
.subtitle{color:var(--text-dim);font-size:1rem;line-height:1.7;}
.summary{background:var(--bg-card);border:1px solid var(--border);border-left:4px solid var(--teal);border-radius:16px;padding:2rem;margin:0 auto 2rem;max-width:1200px;}
.summary-total{font-size:2.5rem;font-weight:900;background:linear-gradient(135deg,#6ee7b7,#a7f3d0);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-family:'IBM Plex Mono',monospace;}
.summary-label{color:var(--text-dim);font-size:.85rem;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem;}
.summary-note{color:var(--text-dim);font-size:.88rem;line-height:1.7;margin-top:1rem;}
.summary-streams{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.75rem;}
.stream-pill{background:rgba(110,231,183,.08);border:1px solid rgba(110,231,183,.2);border-radius:20px;padding:.2rem .7rem;font-size:.75rem;color:var(--teal);font-family:'IBM Plex Mono',monospace;}
.section{background:var(--bg-card);border:1px solid var(--border);border-radius:14px;padding:1.75rem;margin:0 auto 1.5rem;max-width:1200px;}
.section-header{display:flex;align-items:center;gap:.75rem;margin-bottom:1.25rem;}
.section-icon{font-size:1.4rem;}
.section-title{font-size:1.1rem;font-weight:800;color:#fff;font-family:'IBM Plex Mono',monospace;}
.section-subtitle{color:var(--text-dim);font-size:.82rem;margin-top:.15rem;}
.line-items{display:flex;flex-direction:column;gap:0;}
.line-item{display:flex;justify-content:space-between;align-items:center;padding:.7rem 0;border-bottom:1px solid var(--border);}
.line-item:last-child{border-bottom:none;}
.line-item-label{color:#fff;font-size:.9rem;font-weight:600;}
.line-item-detail{color:var(--text-dim);font-size:.8rem;margin-top:.1rem;}
.line-item-amount{font-size:.95rem;font-weight:700;color:var(--teal);font-family:'IBM Plex Mono',monospace;text-align:right;}
.total-row{display:flex;justify-content:space-between;align-items:center;padding:.85rem 0 0;margin-top:.25rem;border-top:2px solid var(--border-md);}
.gold{background:linear-gradient(135deg,#fbbf24,#f59e0b);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.pending-grid{display:grid;grid-template-columns:1fr 1fr;gap:.75rem;}
.pending-item{background:rgba(110,231,183,.04);border:1px solid var(--border);border-radius:8px;padding:.75rem 1rem;display:flex;gap:.6rem;align-items:center;}
.pending-dot{width:8px;height:8px;min-width:8px;border-radius:50%;background:#fbbf24;}
.pending-item span{color:var(--text-dim);font-size:.85rem;}
.stock-tickers{display:flex;flex-wrap:wrap;gap:.5rem;}
.ticker{background:rgba(96,165,250,.08);border:1px solid rgba(96,165,250,.2);border-radius:6px;padding:.2rem .6rem;font-size:.78rem;font-family:'IBM Plex Mono',monospace;color:#60a5fa;}
.disclaimer{max-width:1200px;margin:0 auto 3rem;padding:0 2rem;}
.disclaimer p{font-size:.78rem;color:rgba(220,200,140,.6);line-height:1.6;border:1px solid rgba(255,193,7,.12);border-radius:8px;padding:1rem 1.25rem;background:rgba(255,193,7,.04);}
.report-footer{text-align:center;padding:1rem 2rem 3rem;color:var(--text-muted);font-size:.82rem;}
.fade-in{opacity:0;transform:translateY(20px);transition:opacity .6s,transform .6s;}
.fade-in.visible{opacity:1;transform:translateY(0);}
</style>"""

PAGE_CSS['tracking-number-generator.html'] = """<style>
.tng-hero{text-align:center;padding:80px 2rem 40px;max-width:900px;margin:0 auto;}
.tng-hero h1{font-size:clamp(2rem,4vw,3rem);font-weight:900;font-family:'IBM Plex Mono',monospace;color:#fff;margin-bottom:.75rem;}
.badge{display:inline-flex;align-items:center;gap:.5rem;background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%);padding:.5rem 1.2rem;border-radius:20px;color:#060a0f;font-family:'IBM Plex Mono',monospace;font-size:.85rem;font-weight:700;animation:pulseBadge 2s infinite;box-shadow:0 0 25px rgba(110,231,183,.4);margin-bottom:1rem;}
@keyframes pulseBadge{0%,100%{box-shadow:0 0 25px rgba(110,231,183,.4);}50%{box-shadow:0 0 45px rgba(110,231,183,.65);}}
.subtitle{color:var(--text-dim);font-size:1.05rem;line-height:1.7;max-width:680px;margin:0 auto 2rem;}
.stats-row{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;max-width:1200px;margin:0 auto 3rem;padding:0 2rem;}
.stat-block{background:var(--bg-card);border:1px solid var(--border);border-radius:14px;padding:1.5rem;text-align:center;}
.stat-num{font-size:1.8rem;font-weight:800;background:linear-gradient(135deg,#6ee7b7,#a7f3d0);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-family:'IBM Plex Mono',monospace;margin-bottom:.25rem;}
.stat-label{color:var(--text-dim);font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;}
.section{background:var(--bg-card);border:1px solid var(--border);border-left:4px solid var(--teal);border-radius:20px;padding:3rem;margin:0 auto 2rem;max-width:1200px;}
.section-label{font-size:.8rem;font-weight:700;color:var(--teal);text-transform:uppercase;letter-spacing:.1em;font-family:'IBM Plex Mono',monospace;margin-bottom:.5rem;}
.section h2{font-size:1.5rem;font-weight:800;color:#fff;font-family:'IBM Plex Mono',monospace;margin-bottom:1rem;}
.cards-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1rem;margin:1.5rem 0;}
.card{background:rgba(110,231,183,.04);border:1px solid var(--border);border-radius:12px;padding:1.5rem;transition:all .3s;}
.card:hover{border-color:var(--border-md);transform:translateY(-2px);}
.card-title{font-size:1rem;font-weight:700;color:#fff;margin-bottom:.5rem;}
.card-desc{font-size:.85rem;color:var(--text-dim);line-height:1.65;}
.feature-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:1.5rem 0;}
.feature-card{background:rgba(110,231,183,.03);border:1px solid var(--border);border-radius:12px;padding:1.25rem;}
.feature-card h3{font-size:.9rem;font-weight:700;color:var(--teal);margin-bottom:.4rem;}
.feature-card p{font-size:.82rem;color:var(--text-dim);line-height:1.6;}
.btn-primary,.btn-secondary{display:inline-flex;align-items:center;gap:.5rem;text-decoration:none;padding:.8rem 1.8rem;border-radius:50px;font-size:.9rem;font-weight:700;transition:all .2s;}
.btn-primary{background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%);color:#060a0f;box-shadow:0 0 15px rgba(110,231,183,.3);}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 0 25px rgba(110,231,183,.5);}
.btn-secondary{background:transparent;color:var(--teal);border:2px solid rgba(110,231,183,.3);}
.btn-secondary:hover{border-color:var(--teal);}
.cta-row{display:flex;gap:1rem;flex-wrap:wrap;justify-content:center;margin-top:1.5rem;}
.divider{height:1px;background:var(--border);max-width:1200px;margin:2rem auto;}
.article-content{color:var(--text-dim);font-size:.95rem;line-height:1.8;}
.article-content p{margin-bottom:.75rem;}
.article-content strong{color:#fff;}
.article-content a{color:var(--teal);}
.fade-in{opacity:0;transform:translateY(20px);transition:opacity .6s,transform .6s;}
.fade-in.visible{opacity:1;transform:translateY(0);}
@media(max-width:768px){.cards-grid,.feature-grid,.stats-row{grid-template-columns:1fr;}}
</style>"""

PAGE_CSS['vote.html'] = '<style>\n.fade-in{opacity:0;transform:translateY(20px);transition:opacity .6s,transform .6s;}\n.fade-in.visible{opacity:1;transform:translateY(0);}\n</style>'
PAGE_CSS['gameplay-sheet.html'] = '<style>\n.fade-in{opacity:0;transform:translateY(20px);transition:opacity .6s,transform .6s;}\n.fade-in.visible{opacity:1;transform:translateY(0);}\n</style>'


# ── Converter ─────────────────────────────────────────────────────────
def convert_dark_forest(c, page_css, fname):
    c = c.replace('content="#050810"', 'content="#111c2e"')

    # Replace head content (font+css) before </head>
    font_marker = '<link rel="preconnect" href="https://fonts.googleapis.com">'
    alt_marker  = '<link href="https://fonts.googleapis.com/css2?family=Inter'
    head_end    = c.find('</head>')
    insert_at   = c.find(font_marker)
    if insert_at == -1:
        insert_at = c.find(alt_marker)
    if insert_at == -1:
        insert_at = head_end

    new_head = FONTS + '\n' + RSA_CSS + '\n' + page_css + '\n</head>'
    c = c[:insert_at] + new_head + c[head_end+7:]

    # Remove starfield canvas
    c = c.replace('<canvas id="starfield"></canvas>', '')
    c = c.replace('<canvas id="starfield" />', '')

    # Insert bgCanvas after <body>
    body_idx = c.find('<body>')
    if body_idx != -1 and 'bgCanvas' not in c:
        c = c[:body_idx+6] + '\n' + BG_ELEMENTS + c[body_idx+6:]

    # Remove slide-menu overlay
    c = re.sub(r'\s*<div class="slide-menu-overlay"[^>]*></div>', '', c)
    # Remove entire slide-menu div
    sm_start = c.find('<div class="slide-menu"')
    if sm_start != -1:
        depth = 0
        i = sm_start
        while i < len(c):
            if c[i:i+4] == '<div':
                depth += 1
            elif c[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    c = c[:sm_start] + c[i+6:]
                    break
            i += 1

    # Remove toggleMenu script
    c = re.sub(r'<script>\s*function toggleMenu\(\)[^<]+</script>', '', c)

    # Replace nav+mobile-menu
    old_nav = c.find('<nav class="nav"')
    if old_nav == -1:
        old_nav = c.find('<nav ')
    if old_nav != -1:
        mm_pos  = c.find('class="mobile-menu"', old_nav)
        if mm_pos != -1:
            mm_end = c.find('</div>', mm_pos) + 6
            c = c[:old_nav] + NAV_HTML + c[mm_end:]

    # Replace footer
    foot_s = c.find('<footer>')
    foot_e = c.find('</footer>') + 9
    if foot_s != -1 and foot_e > 9:
        c = c[:foot_s] + FOOTER_HTML + c[foot_e:]

    # Remove dark-forest.js
    c = c.replace('<script src="/js/dark-forest.js"></script>', '')
    c = c.replace('<script src="/js/dark-forest.js" defer></script>', '')

    # Add discord widget if missing
    if 'discord-widget' not in c:
        c = c.replace('</body>', DISCORD_WIDGET + '</body>')

    # Add scripts before </body>
    c = c.replace('</body>', FADE_IN_SCRIPT + BOT_SCRIPT + '\n</body>')

    return c


def add_bgcanvas_only(c):
    if 'bgCanvas' not in c:
        body_idx = c.find('<body>')
        if body_idx != -1:
            c = c[:body_idx+6] + '\n' + BG_ELEMENTS + c[body_idx+6:]
    c = c.replace('<canvas id="starfield"></canvas>', '')
    if '// ===== BACKGROUND STARFIELD' not in c:
        c = c.replace('</body>', FADE_IN_SCRIPT + BOT_SCRIPT + '\n</body>')
    else:
        c = c.replace('</body>', FADE_IN_SCRIPT + '\n</body>')
    return c


# ── Run ───────────────────────────────────────────────────────────────
dark_forest_pages = [
    'comparisons/best-welcome-packages.html',
    'comparisons/chumba-vs-stake.html',
    'comparisons/fastest-payout-sites.html',
    'daily-login-reviews.html',
    'reports/february-2026.html',
    'tracking-number-generator.html',
    'vote.html',
]

for page in dark_forest_pages:
    print(f'Converting {page}...')
    c = open(page, encoding='utf-8').read()
    c = convert_dark_forest(c, PAGE_CSS.get(page, ''), page)
    open(page, 'w', encoding='utf-8').write(c)
    print(f'  OK -> {len(c)//1000}KB')

print('Adding bgCanvas to gameplay-sheet.html...')
c = open('gameplay-sheet.html', encoding='utf-8').read()
c = add_bgcanvas_only(c)
open('gameplay-sheet.html', 'w', encoding='utf-8').write(c)
print(f'  OK -> {len(c)//1000}KB')

print('\nAll done!')
