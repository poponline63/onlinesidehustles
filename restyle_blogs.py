#!/usr/bin/env python3
"""
Restyle all blog posts to match the casino-reviews.html visual system:
- Dark navy #111c2e background (bgCanvas + orbs + grid + scanlines + vignette)
- IBM Plex Mono + Inter fonts
- Teal #6ee7b7 accent
- Casino-reviews nav & footer
- Preserves all article content and its original CSS classes
"""

import re, os, glob

NAV_HTML = """<nav id="nav">
  <div class="nav-inner">
    <a href="/" class="nav-brand">
      <img src="/logo.png" alt="Online Sidehustles" class="nav-logo" style="height:22px;width:auto;">
      ONLINE SIDEHUSTLES
    </a>
    <div class="nav-links">
      <a href="/getting-started" class="nav-link">Get Started</a>
      <a href="/sweepstakes-casino-list" class="nav-link">Sweepstakes Casinos List</a>
      <a href="/casino-reviews" class="nav-link">Casino Reviews</a>
      <a href="/side-hustles" class="nav-link">Side Hustles</a>
      <a href="/tools" class="nav-link">Tools</a>
      <a href="/blog" class="nav-link active">Blog</a>
      <a href="https://discord.gg/W9bPGH8crh" class="nav-cta" target="_blank" rel="noopener">&#128225; Join Discord</a>
    </div>
    <button class="nav-hamburger" id="hamburger" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>
<div class="mobile-menu" id="mobileMenu">
  <a href="/getting-started">Get Started</a>
  <a href="/sweepstakes-casino-list">Sweepstakes Casinos List</a>
  <a href="/casino-reviews">Casino Reviews</a>
  <a href="/side-hustles">Side Hustles</a>
  <a href="/tools">Tools</a>
  <a href="/blog">Blog</a>
  <a href="https://discord.gg/W9bPGH8crh" target="_blank" rel="noopener">&#128225; Join Discord</a>
</div>"""

FOOTER_HTML = """<footer>
  <div class="footer-inner">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">&#127794; ONLINE SIDEHUSTLES</div>
        <p class="footer-tagline">Free guides, community tips, and automation tools for earning from sweepstakes casinos and daily login sites.</p>
      </div>
      <div class="footer-col"><h4>Guides</h4><a href="/sweepstakes-casino-list">Sweepstakes Casinos List</a><a href="/getting-started">Getting Started</a><a href="/side-hustles">Side Hustles</a><a href="/blog">Blog</a></div>
      <div class="footer-col"><h4>Resources</h4><a href="/tools">Tools</a><a href="/sweepstakes">Sweepstakes</a><a href="/faq">FAQ</a></div>
      <div class="footer-col"><h4>Community</h4><a href="https://discord.gg/W9bPGH8crh" target="_blank" rel="noopener">Discord</a><a href="https://onlinesidehustles.info">Website</a></div>
    </div>
    <div class="footer-bottom">
      <span class="footer-copy">&#169; 2026 Online Sidehustles &middot; All rights reserved</span>
      <div class="footer-links"><a href="/privacy">Privacy</a><a href="/terms">Terms</a><a href="/disclaimer">Disclaimer</a></div>
    </div>
  </div>
</footer>"""

DISCORD_HTML = """<a class="discord-widget" id="discordWidget" href="https://discord.com/invite/W9bPGH8crh" target="_blank" rel="noopener">
  <button class="discord-x" id="discordClose" aria-label="Dismiss">&#x2715;</button>
  <svg class="discord-icon" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M23.12 5.48A22.36 22.36 0 0 0 17.7 3.8a15.3 15.3 0 0 0-.7 1.44 20.67 20.67 0 0 0-6.02 0A15.3 15.3 0 0 0 10.3 3.8a22.41 22.41 0 0 0-5.44 1.68C1.88 10.04 1.1 14.48 1.5 18.86a22.6 22.6 0 0 0 6.82 3.42c.55-.74 1.04-1.53 1.46-2.36a14.66 14.66 0 0 1-2.3-1.1c.19-.14.38-.28.56-.43a16.06 16.06 0 0 0 13.92 0c.18.15.37.29.56.43a14.6 14.6 0 0 1-2.31 1.1c.42.83.91 1.62 1.46 2.36a22.53 22.53 0 0 0 6.82-3.42c.47-4.96-.8-9.36-3.37-13.38ZM9.68 16.28c-1.3 0-2.36-1.18-2.36-2.64s1.04-2.64 2.36-2.64 2.38 1.18 2.36 2.64c0 1.46-1.05 2.64-2.36 2.64Zm8.64 0c-1.3 0-2.36-1.18-2.36-2.64s1.04-2.64 2.36-2.64 2.38 1.18 2.36 2.64c0 1.46-1.04 2.64-2.36 2.64Z" fill="white"/></svg>
  <div class="discord-text"><span class="discord-title">Join Discord</span><span class="discord-sub">Free SC alerts &amp; tips</span></div>
</a>
<script>(function(){var w=document.getElementById('discordWidget'),c=document.getElementById('discordClose');if(!w)return;if(localStorage.getItem('dcDismissed'))w.style.display='none';if(c)c.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();w.style.animation='none';w.style.transition='transform 0.3s,opacity 0.3s';w.style.transform='translateX(-130%)';w.style.opacity='0';setTimeout(function(){w.style.display='none';},300);localStorage.setItem('dcDismissed','1');});})();</script>"""

# The full CSS: casino-reviews shell + article content styles
SHELL_CSS = """
/* ===== TOKENS ===== */
:root{
  --bg:#111c2e;--bg-card:#0f1723;--bg-nav:#0c1526;--bg-card2:#131e30;
  --teal:#6ee7b7;--teal-dim:rgba(110,231,183,.55);--teal-faint:rgba(110,231,183,.10);
  --lime:#ADFF2F;--lime-text:#060a0f;
  --text:#e8e6e0;--text-muted:#7a8fa8;--text-dim:#94a3b8;
  --border:rgba(110,231,183,.12);--border-md:rgba(110,231,183,.22);
  --accent:#6ee7b7;--accent-bright:#a7f3d0;--accent-deep:#34d399;
  --surface:rgba(15,23,35,0.92);
  --shadow:0 4px 24px rgba(0,0,0,.45);
}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;background:var(--bg);color:var(--text);overflow-x:hidden;min-height:100vh;}

/* ===== BACKGROUND ===== */
#bgCanvas{position:fixed;inset:0;z-index:-100;pointer-events:none;}
.bg-orb{position:fixed;border-radius:50%;filter:blur(110px);pointer-events:none;z-index:-99;}
.bg-orb-1{width:600px;height:600px;top:-200px;left:-200px;background:radial-gradient(circle,rgba(110,231,183,.07) 0%,transparent 70%);}
.bg-orb-2{width:500px;height:500px;bottom:-150px;right:-150px;background:radial-gradient(circle,rgba(110,231,183,.06) 0%,transparent 70%);}
.bg-orb-3{width:400px;height:400px;top:40%;left:50%;transform:translate(-50%,-50%);background:radial-gradient(circle,rgba(110,231,183,.04) 0%,transparent 70%);}
.bg-grid{position:fixed;inset:0;z-index:-98;pointer-events:none;background:linear-gradient(rgba(110,231,183,.018) 1px,transparent 1px),linear-gradient(90deg,rgba(110,231,183,.018) 1px,transparent 1px);background-size:56px 56px;}
.bg-vignette{position:fixed;inset:0;z-index:-97;pointer-events:none;background:radial-gradient(ellipse at 50% 45%,transparent 38%,rgba(5,9,18,.5) 72%,rgba(4,8,16,.85) 100%);}
.bg-scanlines{position:fixed;inset:0;z-index:-97;pointer-events:none;background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,0,0,.06) 3px,rgba(0,0,0,.06) 4px);}

/* ===== NAV ===== */
nav{position:fixed;top:0;left:0;right:0;z-index:1000;background:var(--bg-nav);border-bottom:1px solid var(--border);height:54px;display:flex;align-items:center;padding:0 1.5rem;transition:box-shadow .2s;}
nav.scrolled{box-shadow:0 2px 20px rgba(0,0,0,.4);}
.nav-inner{max-width:1600px;margin:0 auto;width:100%;display:flex;align-items:center;justify-content:space-between;}
.nav-brand{display:flex;align-items:center;gap:.45rem;text-decoration:none;font-weight:700;font-size:.82rem;color:var(--text);letter-spacing:.08em;text-transform:uppercase;font-family:'IBM Plex Mono',monospace;}
.nav-logo{height:22px;width:auto;}
.nav-links{display:flex;align-items:center;gap:.05rem;}
.nav-link{color:var(--text-dim);text-decoration:none;padding:.3rem .7rem;font-size:.78rem;font-weight:500;border-bottom:2px solid transparent;transition:all .18s;}
.nav-link:hover{color:var(--teal);}
.nav-link.active{color:var(--teal);border-bottom-color:var(--teal);}
.nav-cta{background:var(--lime);color:var(--lime-text);text-decoration:none;padding:.35rem 1rem;font-size:.78rem;font-weight:700;border-radius:4px;margin-left:.6rem;transition:opacity .2s;}
.nav-cta:hover{opacity:.88;}
.nav-hamburger{display:none;flex-direction:column;gap:5px;background:none;border:none;cursor:pointer;padding:4px;}
.nav-hamburger span{display:block;width:22px;height:2px;background:var(--text-dim);border-radius:2px;transition:all .2s;}
.nav-hamburger.active span:nth-child(1){transform:translateY(7px) rotate(45deg);}
.nav-hamburger.active span:nth-child(2){opacity:0;}
.nav-hamburger.active span:nth-child(3){transform:translateY(-7px) rotate(-45deg);}
@media(max-width:768px){.nav-links{display:none;}.nav-hamburger{display:flex;}}
.mobile-menu{display:none;position:fixed;top:54px;left:0;right:0;z-index:999;background:var(--bg-nav);border-bottom:1px solid var(--border);padding:1rem 1.5rem;flex-direction:column;gap:.25rem;}
.mobile-menu.open{display:flex;}
.mobile-menu a{color:var(--text-dim);text-decoration:none;padding:.5rem 0;font-size:.9rem;border-bottom:1px solid var(--border);}
.mobile-menu a:last-child{border-bottom:none;}
.mobile-menu a:hover{color:var(--teal);}

/* ===== DISCORD WIDGET ===== */
.discord-widget{position:fixed;bottom:1.25rem;left:1.25rem;z-index:900;background:#5865F2;border-radius:14px;padding:.7rem 1rem .7rem .85rem;display:flex;align-items:center;gap:.65rem;box-shadow:0 4px 22px rgba(88,101,242,.45),0 0 0 1px rgba(255,255,255,.08);text-decoration:none;color:#fff;animation:discordIn .55s cubic-bezier(.22,1,.36,1) 2.5s both;transition:transform .18s,box-shadow .18s;max-width:230px;}
.discord-widget:hover{transform:translateY(-2px);}
@keyframes discordIn{from{transform:translateX(-130%) scale(.9);opacity:0;}to{transform:none;opacity:1;}}
.discord-icon{flex-shrink:0;width:28px;height:28px;}
.discord-text{display:flex;flex-direction:column;line-height:1.25;}
.discord-title{font-weight:700;font-size:.82rem;}
.discord-sub{font-size:.68rem;opacity:.82;}
.discord-x{position:absolute;top:-7px;right:-7px;width:20px;height:20px;border-radius:50%;background:rgba(20,20,40,.75);border:1px solid rgba(255,255,255,.18);color:#fff;font-size:11px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .15s;}
.discord-x:hover{background:rgba(248,113,113,.8);}

/* ===== PAGE SHELL ===== */
.blog-page{max-width:860px;margin:0 auto;padding:74px 1.25rem 5rem;position:relative;}

/* ===== PROGRESS BAR ===== */
#progress-bar{position:fixed;top:54px;left:0;height:3px;background:var(--teal);z-index:9999;width:0;transition:width .1s;}

/* ===== ARTICLE SHELL ===== */
article{background:var(--bg-card);border:1px solid var(--border);border-radius:16px;overflow:hidden;margin-bottom:2rem;}

/* ===== OC-HERO (article header area) ===== */
.oc-hero{background:linear-gradient(135deg,#0a1628 0%,#0d1f38 55%,#0a1620 100%);border-bottom:1px solid var(--border-md);padding:2.5rem 2.5rem 2rem;position:relative;overflow:hidden;}
.oc-hero::before{content:'';position:absolute;top:-90px;right:-70px;width:360px;height:360px;background:radial-gradient(circle,rgba(110,231,183,.10),transparent 66%);pointer-events:none;}
.breadcrumb{margin-bottom:1.2rem;font-size:.82rem;position:relative;z-index:1;color:var(--text-muted);}
.breadcrumb a{color:var(--text-muted);text-decoration:none;}
.breadcrumb a:hover{color:var(--teal);}
.category-badge{position:relative;z-index:1;display:inline-block;margin-bottom:.9rem;padding:.3rem .9rem;border-radius:20px;background:rgba(110,231,183,.12);border:1px solid rgba(110,231,183,.3);color:var(--teal);font-size:.75rem;font-weight:800;letter-spacing:.1em;font-family:'IBM Plex Mono',monospace;}
.oc-hero h1{position:relative;z-index:1;font-size:clamp(1.55rem,3.5vw,2.2rem);line-height:1.2;margin:0 0 1rem;font-weight:900;color:#fff;}
.hero-desc{position:relative;z-index:1;color:var(--text-dim);font-size:.98rem;line-height:1.72;max-width:720px;}
.article-meta{position:relative;z-index:1;margin-top:1.2rem;padding-top:1.2rem;border-top:1px solid var(--border);display:flex;gap:.6rem;flex-wrap:wrap;}
.meta-item{background:rgba(110,231,183,.06);border:1px solid var(--border);padding:.25rem .75rem;border-radius:20px;font-size:.78rem;color:var(--text-muted);font-family:'IBM Plex Mono',monospace;}

/* ===== ARTICLE BODY ===== */
.article-body{padding:2rem 2.5rem 2.5rem;line-height:1.8;color:var(--text-dim);font-size:.97rem;}
@media(max-width:600px){.oc-hero,.article-body{padding-left:1.25rem;padding-right:1.25rem;}}
.article-body h2{font-size:1.35rem;font-weight:800;color:#fff;margin:2.2rem 0 .9rem;letter-spacing:-.02em;}
.article-body h3{font-size:1.1rem;font-weight:700;color:var(--text);margin:1.6rem 0 .7rem;}
.article-body h4{font-size:.95rem;font-weight:700;color:var(--teal);margin:1.2rem 0 .5rem;font-family:'IBM Plex Mono',monospace;letter-spacing:.04em;}
.article-body p{margin-bottom:1.1rem;}
.article-body a{color:var(--teal);text-decoration:none;}
.article-body a:hover{text-decoration:underline;}
.article-body ul,.article-body ol{margin:.5rem 0 1rem 1.4rem;}
.article-body li{margin-bottom:.4rem;}
.article-body strong{color:var(--text);font-weight:700;}
.article-body code{background:rgba(110,231,183,.08);border:1px solid var(--border);padding:.1rem .4rem;border-radius:4px;font-family:'IBM Plex Mono',monospace;font-size:.85em;color:var(--teal);}
.article-body pre{background:var(--bg);border:1px solid var(--border);border-radius:10px;padding:1.25rem;overflow-x:auto;margin:1rem 0;}
.article-body pre code{background:none;border:none;padding:0;}
.article-body hr{border:none;border-top:1px solid var(--border);margin:2rem 0;}
.article-body table{width:100%;border-collapse:collapse;margin:1rem 0;}
.article-body th{background:rgba(110,231,183,.08);color:var(--teal);font-family:'IBM Plex Mono',monospace;font-size:.78rem;letter-spacing:.06em;text-transform:uppercase;padding:.65rem 1rem;border:1px solid var(--border);text-align:left;}
.article-body td{padding:.65rem 1rem;border:1px solid var(--border);color:var(--text-dim);}
.article-body tr:hover td{background:rgba(110,231,183,.03);}
.article-body img{max-width:100%;border-radius:10px;border:1px solid var(--border);}
.article-body blockquote{border-left:3px solid var(--teal);padding:.75rem 1.25rem;margin:1rem 0;background:rgba(110,231,183,.04);border-radius:0 8px 8px 0;color:var(--text-dim);font-style:italic;}

/* ===== ARTICLE COMPONENTS ===== */
.highlight-box{background:rgba(110,231,183,.06);border:1px solid rgba(110,231,183,.2);border-left:3px solid var(--teal);border-radius:0 10px 10px 0;padding:1rem 1.25rem;margin:1.25rem 0;color:var(--text-dim);font-size:.92rem;}
.highlight-box strong{color:var(--teal);}
.warning-box{background:rgba(251,191,36,.06);border:1px solid rgba(251,191,36,.2);border-left:3px solid #fbbf24;border-radius:0 10px 10px 0;padding:1rem 1.25rem;margin:1.25rem 0;color:var(--text-dim);font-size:.92rem;}
.warning-box strong{color:#fbbf24;}
.cta-box{background:linear-gradient(135deg,rgba(110,231,183,.08) 0%,rgba(110,231,183,.04) 100%);border:1px solid var(--border-md);border-radius:14px;padding:1.75rem;text-align:center;margin:2rem 0;}
.cta-box h3{color:#fff;font-size:1.2rem;margin-bottom:.5rem;}
.cta-box p{color:var(--text-dim);font-size:.9rem;margin-bottom:1.25rem;}
.cta-row{display:flex;gap:.75rem;justify-content:center;flex-wrap:wrap;}
.cta-btn{display:inline-block;background:var(--teal);color:#060a0f;font-weight:700;font-family:'IBM Plex Mono',monospace;font-size:.82rem;padding:.6rem 1.5rem;border-radius:8px;text-decoration:none;transition:opacity .2s;letter-spacing:.04em;}
.cta-btn:hover{opacity:.88;}
.cta-btn-outline{display:inline-block;border:1px solid var(--teal);color:var(--teal);font-weight:700;font-family:'IBM Plex Mono',monospace;font-size:.82rem;padding:.6rem 1.5rem;border-radius:8px;text-decoration:none;transition:all .2s;}
.cta-btn-outline:hover{background:rgba(110,231,183,.1);}
.toc{background:var(--bg);border:1px solid var(--border);border-radius:12px;padding:1.25rem 1.5rem;margin:0 0 2rem;}
.toc h4{font-family:'IBM Plex Mono',monospace;font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);margin-bottom:.75rem;}
.toc ol,.toc ul{margin-left:1.1rem;}
.toc li{margin-bottom:.3rem;font-size:.88rem;}
.toc a{color:var(--text-dim);text-decoration:none;}
.toc a:hover{color:var(--teal);}
.step-card{background:var(--bg);border:1px solid var(--border);border-radius:12px;padding:1.1rem 1.25rem;margin:.75rem 0;display:flex;gap:1rem;align-items:flex-start;}
.step-card:hover{border-color:var(--border-md);}
.step-num{flex-shrink:0;width:32px;height:32px;background:rgba(110,231,183,.12);border:1px solid var(--border-md);border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'IBM Plex Mono',monospace;font-weight:700;font-size:.8rem;color:var(--teal);}
.step-content{flex:1;}
.step-content h4{color:var(--text);font-size:.95rem;font-weight:700;margin-bottom:.35rem;}
.step-content p{color:var(--text-dim);font-size:.88rem;margin:0;}
.quick-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1rem;margin:1rem 0;}
.quick-card{background:var(--bg);border:1px solid var(--border);border-radius:12px;padding:1rem;transition:border-color .2s,transform .2s;}
.quick-card:hover{border-color:var(--border-md);transform:translateY(-2px);}
.quick-label{font-family:'IBM Plex Mono',monospace;font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;color:var(--teal);margin-bottom:.4rem;}
.quick-card h4{color:var(--text);font-size:.9rem;font-weight:700;margin-bottom:.35rem;}
.quick-card p{color:var(--text-dim);font-size:.82rem;margin:0;}
.comp-table{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.88rem;}
.comp-table th{background:rgba(110,231,183,.08);color:var(--teal);font-family:'IBM Plex Mono',monospace;font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;padding:.6rem 1rem;border:1px solid var(--border);text-align:left;}
.comp-table td{padding:.6rem 1rem;border:1px solid var(--border);color:var(--text-dim);}
.comp-table tr:hover td{background:rgba(110,231,183,.03);}
.badge-good{display:inline-block;background:rgba(110,231,183,.12);color:var(--teal);border:1px solid rgba(110,231,183,.25);padding:.15rem .5rem;border-radius:4px;font-size:.75rem;font-weight:700;font-family:'IBM Plex Mono',monospace;}
.badge-mid{display:inline-block;background:rgba(251,191,36,.1);color:#fbbf24;border:1px solid rgba(251,191,36,.25);padding:.15rem .5rem;border-radius:4px;font-size:.75rem;font-weight:700;font-family:'IBM Plex Mono',monospace;}
.badge-bad{display:inline-block;background:rgba(248,113,113,.1);color:#f87171;border:1px solid rgba(248,113,113,.25);padding:.15rem .5rem;border-radius:4px;font-size:.75rem;font-weight:700;font-family:'IBM Plex Mono',monospace;}
.timeline{border-left:2px solid var(--border-md);margin:1.25rem 0 1.25rem 1rem;padding-left:1.5rem;}
.time-step{position:relative;margin-bottom:1.25rem;}
.time-step::before{content:'';position:absolute;left:-1.95rem;top:.35rem;width:10px;height:10px;background:var(--teal);border-radius:50%;border:2px solid var(--bg-card);}
.time-pill{display:inline-block;background:rgba(110,231,183,.1);color:var(--teal);border:1px solid var(--border-md);padding:.2rem .65rem;border-radius:4px;font-family:'IBM Plex Mono',monospace;font-size:.72rem;font-weight:700;margin-bottom:.4rem;}
.time-step h4{color:var(--text);font-size:.95rem;font-weight:700;margin-bottom:.3rem;}
.time-step p{color:var(--text-dim);font-size:.88rem;margin:0;}
.related-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:.75rem;margin-top:.75rem;}
.related-card{display:block;background:var(--bg);border:1px solid var(--border);border-radius:10px;padding:.9rem;text-decoration:none;transition:border-color .2s,transform .2s;}
.related-card:hover{border-color:var(--border-md);transform:translateY(-2px);}
.related-label{font-family:'IBM Plex Mono',monospace;font-size:.65rem;letter-spacing:.1em;text-transform:uppercase;color:var(--teal);margin-bottom:.3rem;}
.related-card h4{color:var(--text);font-size:.85rem;font-weight:600;margin:0;}

/* ===== FOOTER ===== */
footer{background:var(--bg-nav);border-top:1px solid var(--border);padding:2.5rem 1.5rem 1.5rem;}
.footer-inner{max-width:1280px;margin:0 auto;}
.footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:2rem;margin-bottom:2rem;}
@media(max-width:768px){.footer-grid{grid-template-columns:1fr 1fr;}}
@media(max-width:480px){.footer-grid{grid-template-columns:1fr;}}
.footer-brand{font-family:'IBM Plex Mono',monospace;font-size:.82rem;font-weight:700;letter-spacing:.08em;color:var(--text);text-transform:uppercase;margin-bottom:.6rem;}
.footer-tagline{font-size:.8rem;color:var(--text-muted);line-height:1.6;max-width:280px;}
.footer-col h4{font-family:'IBM Plex Mono',monospace;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--teal);margin-bottom:.75rem;}
.footer-col a{display:block;color:var(--text-dim);text-decoration:none;font-size:.82rem;margin-bottom:.4rem;}
.footer-col a:hover{color:var(--teal);}
.footer-bottom{border-top:1px solid var(--border);padding-top:1rem;display:flex;justify-content:space-between;flex-wrap:wrap;gap:.5rem;}
.footer-copy{font-size:.75rem;color:var(--text-muted);font-family:'IBM Plex Mono',monospace;}
.footer-links{display:flex;gap:1rem;}
.footer-links a{color:var(--text-muted);text-decoration:none;font-size:.75rem;font-family:'IBM Plex Mono',monospace;}
.footer-links a:hover{color:var(--teal);}
"""

PAGE_SCRIPTS = """<script>
  // Nav scroll
  const nav = document.getElementById('nav');
  window.addEventListener('scroll', () => { nav.classList.toggle('scrolled', window.scrollY > 20); }, { passive: true });
  // Mobile menu
  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobileMenu');
  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    mobileMenu.classList.toggle('open');
    document.body.style.overflow = mobileMenu.classList.contains('open') ? 'hidden' : '';
  });
  mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      hamburger.classList.remove('active');
      mobileMenu.classList.remove('open');
      document.body.style.overflow = '';
    });
  });
  // Reading progress bar
  const bar = document.getElementById('progress-bar');
  if (bar) {
    window.addEventListener('scroll', () => {
      const doc = document.documentElement;
      const total = doc.scrollHeight - doc.clientHeight;
      bar.style.width = (window.scrollY / total * 100) + '%';
    }, { passive: true });
  }
  // Fade in observer
  const fadeObs = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); fadeObs.unobserve(e.target); } });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.dlg-fade').forEach(el => fadeObs.observe(el));
</script>"""

BG_CANVAS_SCRIPT = """<script>
(function(){
  var c=document.getElementById('bgCanvas');
  if(!c)return;
  var ctx=c.getContext('2d');
  var stars=[];
  function resize(){c.width=window.innerWidth;c.height=window.innerHeight;}
  function init(){stars=[];for(var i=0;i<180;i++){stars.push({x:Math.random()*c.width,y:Math.random()*c.height,r:Math.random()*1.2+.2,o:Math.random()*.7+.1,s:Math.random()*.4+.1,d:Math.random()>.5?1:-1});}}
  function draw(){
    ctx.clearRect(0,0,c.width,c.height);
    stars.forEach(function(s){
      s.o+=s.s*.012*s.d;
      if(s.o>0.9||s.o<0.1)s.d*=-1;
      ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
      ctx.fillStyle='rgba(110,231,183,'+s.o+')';ctx.fill();
    });
    requestAnimationFrame(draw);
  }
  window.addEventListener('resize',function(){resize();init();});
  resize();init();draw();
})();
</script>"""


def extract_meta(content):
    """Extract key head metadata from existing blog post."""
    def get(pattern, default=''):
        m = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        return m.group(1).strip() if m else default

    title = get(r'<title>(.*?)</title>', 'Blog Post')
    desc = get(r'<meta name="description" content="(.*?)"', '')
    keywords = get(r'<meta name="keywords" content="(.*?)"', '')
    canonical = get(r'<link rel="canonical" href="(.*?)"', '')
    og_title = get(r'<meta property="og:title" content="(.*?)"', title)
    og_image = get(r'<meta property="og:image" content="(.*?)"', 'https://onlinesidehustles.info/onlinesidehustlesbanner.png')
    tw_desc = get(r'<meta name="twitter:description" content="(.*?)"', desc)

    # Schema markup blocks
    schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)

    return {
        'title': title,
        'desc': desc,
        'keywords': keywords,
        'canonical': canonical,
        'og_title': og_title,
        'og_image': og_image,
        'tw_desc': tw_desc,
        'schemas': schemas,
    }


def extract_article(content):
    """Extract article content between <article> tags."""
    m = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL)
    if m:
        return m.group(1)
    # Fallback: try to find main content div
    m = re.search(r'<div class="article[^"]*">(.*?)</div>\s*(?:</div>|<footer)', content, re.DOTALL)
    if m:
        return m.group(1)
    return ''


def build_page(meta, article_content):
    """Build the new styled blog post HTML."""
    canonical = meta['canonical'] or ''
    schema_blocks = '\n'.join(
        f'<script type="application/ld+json">{s}</script>'
        for s in meta['schemas']
    )

    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-D9MKJR8494"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-D9MKJR8494');</script>
<script src="/js/analytics.js" defer></script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<title>{meta['title']}</title>
<meta name="description" content="{meta['desc']}">
{f'<meta name="keywords" content="{meta["keywords"]}">' if meta['keywords'] else ''}
<meta name="author" content="Online Sidehustles">
{f'<link rel="canonical" href="{canonical}">' if canonical else ''}
<meta property="og:type" content="article">
{f'<meta property="og:url" content="{canonical}">' if canonical else ''}
<meta property="og:site_name" content="Online Sidehustles">
<meta property="og:title" content="{meta['og_title']}">
<meta property="og:description" content="{meta['desc']}">
<meta property="og:image" content="{meta['og_image']}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{meta['og_title']}">
<meta name="twitter:description" content="{meta['tw_desc'] or meta['desc']}">
<meta name="twitter:image" content="{meta['og_image']}">
{schema_blocks}
<link rel="icon" type="image/gif" href="/favicon.gif">
<link rel="icon" href="/favicon.ico">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta name="theme-color" content="#111c2e">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
{SHELL_CSS}
</style>
</head>
<body>

<!-- Background layers — always behind everything -->
<canvas id="bgCanvas"></canvas>
<div class="bg-orb bg-orb-1"></div>
<div class="bg-orb bg-orb-2"></div>
<div class="bg-orb bg-orb-3"></div>
<div class="bg-grid"></div>
<div class="bg-scanlines"></div>
<div class="bg-vignette"></div>

<div id="progress-bar"></div>

{NAV_HTML}

<div class="blog-page">
  <article>
{article_content}
  </article>
</div>

{FOOTER_HTML}

{DISCORD_HTML}

{PAGE_SCRIPTS}
{BG_CANVAS_SCRIPT}

</body>
</html>"""


def process_blog(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    meta = extract_meta(content)
    article = extract_article(content)

    if not article:
        print(f'  SKIP (no article found): {os.path.basename(filepath)}')
        return False

    new_html = build_page(meta, article)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    return True


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    files = sorted(glob.glob(os.path.join(base, 'blog', '*.html')))
    done = 0
    for fp in files:
        ok = process_blog(fp)
        name = os.path.basename(fp)
        if ok:
            print(f'  OK: {name}')
            done += 1

    print(f'\n{done}/{len(files)} blog posts restyled.')


if __name__ == '__main__':
    main()
