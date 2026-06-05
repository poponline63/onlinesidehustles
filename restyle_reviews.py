import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

NEW_CSS = '''<style>
/* ===== REVIEW PAGE DESIGN SYSTEM ===== */
:root{
  --bg:#111c2e;--bg-card:#0f1723;--bg-nav:#0c1526;
  --teal:#6ee7b7;--teal-dim:rgba(110,231,183,.55);--teal-faint:rgba(110,231,183,.10);
  --lime:#ADFF2F;--lime-text:#060a0f;
  --text:#e8e6e0;--text-muted:#7a8fa8;--text-dim:#94a3b8;
  --border:rgba(110,231,183,.12);--border-md:rgba(110,231,183,.22);
  --red:#f87171;
}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;background:var(--bg);color:var(--text);overflow-x:hidden;min-height:100vh;}
#bgCanvas{position:fixed;inset:0;z-index:-4;pointer-events:none;}
.bg-orb{position:fixed;border-radius:50%;filter:blur(100px);pointer-events:none;z-index:-3;}
.bg-orb-1{width:600px;height:600px;top:-200px;left:-200px;background:radial-gradient(circle,rgba(110,231,183,.08) 0%,transparent 70%);}
.bg-orb-2{width:500px;height:500px;bottom:-150px;right:-150px;background:radial-gradient(circle,rgba(110,231,183,.07) 0%,transparent 70%);}
.bg-orb-3{width:400px;height:400px;top:40%;left:50%;transform:translate(-50%,-50%);background:radial-gradient(circle,rgba(110,231,183,.05) 0%,transparent 70%);}
.bg-orb-4{width:350px;height:350px;top:20%;right:10%;background:radial-gradient(circle,rgba(110,231,183,.04) 0%,transparent 70%);}
.bg-grid{position:fixed;inset:0;z-index:-3;pointer-events:none;background:linear-gradient(rgba(110,231,183,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(110,231,183,.025) 1px,transparent 1px);background-size:56px 56px;}
.bg-vignette{position:fixed;inset:0;z-index:-2;pointer-events:none;background:radial-gradient(ellipse at 50% 45%,transparent 38%,rgba(5,9,18,.45) 72%,rgba(4,8,16,.82) 100%);}
.bg-scanlines{position:fixed;inset:0;z-index:-2;pointer-events:none;background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,0,0,.07) 3px,rgba(0,0,0,.07) 4px);}
@keyframes coinFlyRTL{0%{transform:translateX(0) translateY(0) rotate(0deg);opacity:1;}80%{opacity:1;}100%{transform:translateX(-110vw) translateY(var(--dy,20px)) rotate(-720deg);opacity:0;}}
@keyframes coinFlyLTR{0%{transform:translateX(0) translateY(0) rotate(0deg);opacity:1;}80%{opacity:1;}100%{transform:translateX(110vw) translateY(var(--dy,-20px)) rotate(720deg);opacity:0;}}
.fly-coin{position:fixed;pointer-events:none;z-index:9999;font-size:1.4rem;animation-timing-function:linear;animation-fill-mode:forwards;}
.fade-in{opacity:0;transform:translateY(20px);transition:opacity .55s ease-out,transform .55s ease-out;}
.fade-in.visible{opacity:1;transform:translateY(0);}
.fade-in-delay-1{transition-delay:.1s;}
.fade-in-delay-2{transition-delay:.2s;}
nav,.nav{position:fixed;top:0;left:0;right:0;z-index:1000;background:var(--bg-nav);border-bottom:1px solid var(--border);height:54px;display:flex;align-items:center;padding:0 1.5rem;transition:box-shadow .2s;}
nav.scrolled,.nav.scrolled{box-shadow:0 2px 20px rgba(0,0,0,.4);}
.nav-inner{max-width:1200px;margin:0 auto;width:100%;display:flex;align-items:center;justify-content:space-between;}
.nav-brand{display:flex;align-items:center;gap:.45rem;text-decoration:none;font-weight:700;font-size:.82rem;color:var(--text);letter-spacing:.08em;text-transform:uppercase;font-family:'IBM Plex Mono','Courier New',Courier,monospace;}
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
.mobile-menu.active,.mobile-menu.open{display:flex;}
.mobile-menu a{color:var(--text-dim);text-decoration:none;padding:.5rem 0;font-size:.9rem;border-bottom:1px solid var(--border);}
.mobile-menu a:last-child{border-bottom:none;}
.mobile-menu a:hover{color:var(--teal);}
.discord-widget{position:fixed;bottom:1.25rem;left:1.25rem;z-index:9997;background:#5865F2;border-radius:14px;padding:.7rem 1rem .7rem .85rem;display:flex;align-items:center;gap:.65rem;box-shadow:0 4px 22px rgba(88,101,242,.45),0 0 0 1px rgba(255,255,255,.08);text-decoration:none;color:#fff;animation:discordIn .55s cubic-bezier(.22,1,.36,1) 2.5s both;transition:transform .18s,box-shadow .18s;max-width:230px;}
.discord-widget:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(88,101,242,.55);}
@keyframes discordIn{from{transform:translateX(-130%) scale(.9);opacity:0;}to{transform:translateX(0) scale(1);opacity:1;}}
.discord-icon{flex-shrink:0;width:28px;height:28px;}
.discord-text{display:flex;flex-direction:column;line-height:1.25;}
.discord-title{font-weight:700;font-size:.82rem;}
.discord-sub{font-size:.68rem;opacity:.82;}
.discord-x{position:absolute;top:-7px;right:-7px;width:20px;height:20px;border-radius:50%;background:rgba(20,20,40,.75);border:1px solid rgba(255,255,255,.18);color:#fff;font-size:11px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .15s;}
.discord-x:hover{background:rgba(248,113,113,.8);}
.content-area{padding-top:74px;min-height:100vh;}
.container{max-width:900px;margin:0 auto;padding:0 1.25rem;position:relative;z-index:1;}
.breadcrumbs{padding:1rem 0 .5rem;}
.breadcrumb-list{font-size:.78rem;color:var(--text-muted);font-family:'IBM Plex Mono',monospace;display:flex;flex-wrap:wrap;gap:.3rem;align-items:center;}
.breadcrumb-list a{color:var(--teal);text-decoration:none;}
.breadcrumb-list a:hover{text-decoration:underline;}
.breadcrumb-sep{color:var(--text-dim);}
.page-header{padding:1.5rem 0 1rem;}
.page-header h1{font-size:clamp(1.6rem,3.5vw,2.4rem);font-weight:800;letter-spacing:-.03em;color:#fff;line-height:1.2;}
.highlight{color:var(--teal);}
.verdict-card{background:var(--bg-card);border:1px solid var(--border-md);border-left:4px solid var(--teal);border-radius:10px;padding:1.5rem;margin-bottom:1.5rem;display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;}
.verdict-label{font-family:'IBM Plex Mono',monospace;font-size:.72rem;letter-spacing:.14em;font-weight:700;text-transform:uppercase;padding:.25rem .7rem;border-radius:4px;background:rgba(110,231,183,.12);color:var(--teal);}
.verdict-tier{font-size:.78rem;font-weight:700;padding:.25rem .7rem;border-radius:4px;background:rgba(173,255,47,.1);color:var(--lime);border:1px solid rgba(173,255,47,.25);font-family:'IBM Plex Mono',monospace;}
.verdict-summary{flex:1 1 100%;color:var(--text-dim);font-size:.95rem;line-height:1.65;}
.verdict-score{font-size:1.8rem;font-weight:800;color:var(--teal);font-family:'IBM Plex Mono',monospace;white-space:nowrap;}
.quick-facts{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:.7rem;margin-bottom:1.5rem;}
.fact-item{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:.75rem 1rem;}
.fact-label{font-family:'IBM Plex Mono',monospace;font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);margin-bottom:.25rem;}
.fact-value{font-size:.88rem;font-weight:600;color:var(--text);}
.review-block{background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:1.5rem;margin-bottom:1.25rem;}
.review-block h2{font-size:1.1rem;font-weight:700;color:var(--teal);font-family:'IBM Plex Mono',monospace;letter-spacing:.04em;text-transform:uppercase;margin-bottom:.9rem;padding-bottom:.5rem;border-bottom:1px solid var(--border);}
.review-block p{color:var(--text-dim);font-size:.93rem;line-height:1.7;margin-bottom:.7rem;}
.review-block p:last-child{margin-bottom:0;}
.review-block strong{color:var(--text);}
.pros-cons{display:grid;grid-template-columns:1fr 1fr;gap:1rem;}
@media(max-width:600px){.pros-cons{grid-template-columns:1fr;}}
.pros-card,.cons-card{background:rgba(110,231,183,.04);border-radius:8px;padding:1rem;}
.pros-card{border:1px solid rgba(110,231,183,.2);border-left:3px solid var(--teal);}
.cons-card{border:1px solid rgba(248,113,113,.2);border-left:3px solid var(--red);}
.pros-card h3{color:var(--teal);font-size:.82rem;font-family:'IBM Plex Mono',monospace;letter-spacing:.06em;text-transform:uppercase;margin-bottom:.7rem;}
.cons-card h3{color:var(--red);font-size:.82rem;font-family:'IBM Plex Mono',monospace;letter-spacing:.06em;text-transform:uppercase;margin-bottom:.7rem;}
.pros-card ul,.cons-card ul{list-style:none;display:flex;flex-direction:column;gap:.4rem;}
.pros-card li,.cons-card li{font-size:.85rem;color:var(--text-dim);display:flex;gap:.5rem;align-items:flex-start;}
.check{color:var(--teal);font-weight:700;flex-shrink:0;}
.cross{color:var(--red);font-weight:700;flex-shrink:0;}
.states-grid{display:flex;flex-wrap:wrap;gap:.4rem;margin:.75rem 0;}
.state-tag{background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.3);color:var(--red);font-family:'IBM Plex Mono',monospace;font-size:.72rem;font-weight:700;padding:.2rem .55rem;border-radius:4px;}
.rating-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:.7rem;}
.rating-item{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:.75rem;text-align:center;}
.rating-item.overall{border-color:var(--teal);background:rgba(110,231,183,.06);}
.rating-item-label{font-family:'IBM Plex Mono',monospace;font-size:.68rem;letter-spacing:.08em;text-transform:uppercase;color:var(--text-muted);margin-bottom:.35rem;}
.rating-item-value{font-size:1.2rem;font-weight:800;color:var(--teal);font-family:'IBM Plex Mono',monospace;}
.rating-item.overall .rating-item-value{color:var(--lime);font-size:1.4rem;}
.cta-block{text-align:center;padding:2rem;margin-bottom:1.25rem;background:var(--bg-card);border:1px solid var(--border-md);border-radius:10px;}
.cta-btn{display:inline-block;background:var(--teal);color:#050f1a;font-weight:700;font-size:.95rem;padding:.8rem 2rem;border-radius:6px;text-decoration:none;transition:opacity .2s;margin-bottom:.75rem;}
.cta-btn:hover{opacity:.85;}
.cta-note{font-size:.75rem;color:var(--text-muted);font-family:'IBM Plex Mono',monospace;}
.faq-item{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:1rem 1.2rem;margin-bottom:.65rem;}
.faq-question{font-weight:600;font-size:.9rem;color:var(--text);margin-bottom:.5rem;}
.faq-answer{font-size:.85rem;color:var(--text-dim);line-height:1.65;}
.related-links{display:flex;flex-wrap:wrap;gap:.6rem;margin-bottom:2rem;padding-top:.5rem;}
.related-link{background:var(--bg-card);border:1px solid var(--border);border-radius:6px;color:var(--teal);font-size:.8rem;font-weight:600;text-decoration:none;padding:.4rem .9rem;transition:all .18s;font-family:'IBM Plex Mono',monospace;}
.related-link:hover{border-color:var(--teal);background:var(--teal-faint);}
footer{background:var(--bg-nav);border-top:1px solid var(--border);padding:2.5rem 1.5rem 1.5rem;}
.footer-inner{max-width:1200px;margin:0 auto;}
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
</style>'''

NEW_BG = '''<canvas id="bgCanvas"></canvas>
<div class="bg-orb bg-orb-1"></div>
<div class="bg-orb bg-orb-2"></div>
<div class="bg-orb bg-orb-3"></div>
<div class="bg-orb bg-orb-4"></div>
<div class="bg-grid"></div>
<div class="bg-scanlines"></div>
<div class="bg-vignette"></div>'''

NEW_BG_JS = '''<script>
(function(){
  const canvas=document.getElementById('bgCanvas');
  if(!canvas)return;
  const ctx=canvas.getContext('2d');
  let W,H,stars=[];
  function resize(){W=canvas.width=window.innerWidth;H=canvas.height=window.innerHeight;}
  function mkStar(){return{x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.2+0.2,a:Math.random(),da:(Math.random()*0.004+0.001)*(Math.random()<0.5?1:-1)};}
  function init(){resize();stars=[];for(let i=0;i<120;i++)stars.push(mkStar());}
  function draw(){ctx.clearRect(0,0,W,H);stars.forEach(s=>{s.a+=s.da;if(s.a<=0||s.a>=1)s.da*=-1;ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fillStyle='rgba(110,231,183,'+s.a.toFixed(2)+')';ctx.fill();});requestAnimationFrame(draw);}
  window.addEventListener('resize',()=>{resize();stars=[];for(let i=0;i<120;i++)stars.push(mkStar());});
  init();draw();
})();
(function(){
  const COINS=['\U0001f4b0','\U0001fa99','\U0001f4b5','\U0001f48e'];
  function spawnCoin(){
    const el=document.createElement('div');el.className='fly-coin';
    const rtl=Math.random()<0.5;const dy=(Math.random()*80-40)+'px';const dur=(4+Math.random()*4).toFixed(1)+'s';
    el.textContent=COINS[Math.floor(Math.random()*COINS.length)];
    el.style.cssText='top:'+(10+Math.random()*80)+'vh;'+(rtl?'right:-60px':'left:-60px')+';--dy:'+dy+';animation:coin'+(rtl?'FlyRTL':'FlyLTR')+' '+dur+' linear forwards;';
    document.body.appendChild(el);setTimeout(()=>el.remove(),(parseFloat(dur)+0.3)*1000);
  }
  setTimeout(()=>spawnCoin(),2000);setInterval(spawnCoin,7000);
})();
</script>'''

review_files = [f for f in os.listdir('.') if f.startswith('review-') and f.endswith('.html')]
print(f'Processing {len(review_files)} review files...')

for fname in sorted(review_files):
    c = open(fname, encoding='utf-8').read()

    # A. Update fonts to add IBM Plex Mono
    c = c.replace(
        'family=Inter:wght@400;500;600;700&display=swap',
        'family=IBM+Plex+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap'
    )

    # B. Remove dark-forest CSS link
    c = c.replace('<link rel="stylesheet" href="/css/dark-forest-theme.css?v=2">', '')
    c = c.replace('<link rel="stylesheet" href="/css/dark-forest-theme.css">', '')

    # C. Remove animated-favicon.js
    c = c.replace('<script src="/js/animated-favicon.js" defer></script>', '')

    # D. Replace existing inline <style> block (discord widget only) with new CSS
    m = re.search(r'<style>\n\.discord-widget\{.*?</style>', c, re.DOTALL)
    if m:
        c = c[:m.start()] + NEW_CSS + c[m.end():]
    else:
        c = c.replace('</head>', NEW_CSS + '\n</head>', 1)

    # E. Replace starfield canvas
    for old_bg in [
        '<!-- Starfield Canvas -->\n<canvas id="starfield"></canvas>',
        '<canvas id="starfield"></canvas>',
    ]:
        if old_bg in c:
            c = c.replace(old_bg, NEW_BG, 1)
            break

    # F. Add Casino Reviews to desktop nav (after Blog link, before Discord CTA)
    old_nav = '<a href="/blog" class="nav-link">Blog</a>\n      <a href="https://discord.gg/W9bPGH8crh" class="nav-cta"'
    new_nav = '<a href="/blog" class="nav-link">Blog</a>\n      <a href="/reviews-hub" class="nav-link active">Casino Reviews</a>\n      <a href="https://discord.gg/W9bPGH8crh" class="nav-cta"'
    if old_nav in c:
        c = c.replace(old_nav, new_nav)

    # G. Add Casino Reviews to mobile menu (after Blog, before Discord)
    old_mob = '<a href="/blog">Blog</a>\n  <a href="https://discord.gg/W9bPGH8crh"'
    new_mob = '<a href="/blog">Blog</a>\n  <a href="/reviews-hub">Casino Reviews</a>\n  <a href="https://discord.gg/W9bPGH8crh"'
    if old_mob in c:
        c = c.replace(old_mob, new_mob)

    # H. Replace dark-forest.js script with bgCanvas JS
    if '<script src="/js/dark-forest.js"></script>' in c:
        c = c.replace('<script src="/js/dark-forest.js"></script>', NEW_BG_JS)
    else:
        c = c.replace('</body>', NEW_BG_JS + '\n</body>', 1)

    open(fname, 'w', encoding='utf-8').write(c)
    print(f'  OK: {fname}')

print('\nAll done.')
