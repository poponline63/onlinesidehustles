
with open('guide-player-2.html', encoding='utf-8') as f:
    content = f.read()

# ---- 1. Fix theme-color ----
content = content.replace(
    '<meta name="theme-color" content="#050810">',
    '<meta name="theme-color" content="#111c2e">'
)

# ---- 2. Remove dark-forest-theme.css link and add IBM Plex Mono font ----
content = content.replace(
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">\n<link rel="stylesheet" href="/css/dark-forest-theme.css?v=2">',
    '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">'
)

# ---- 3. Replace the two <style> blocks with RSA infrastructure + page CSS ----
# Find old style section (from first <style> to </style>\n</head>)
style_start = content.find('\n<style>\n/* ===== PLAYER 2 GUIDE')
head_end = content.find('</head>', style_start) + len('</head>')
style_end = head_end

new_styles = """
<style>
/* ===== DESIGN TOKENS ===== */
:root {
  --bg:        #111c2e;
  --bg-card:   #0f1723;
  --bg-nav:    #0c1526;
  --bg-darker: #0a1120;
  --teal:      #6ee7b7;
  --teal-dim:  rgba(110,231,183,0.55);
  --teal-faint:rgba(110,231,183,0.10);
  --green:     hsl(150,60%,52%);
  --text:      #e8e6e0;
  --text-muted:#7a8fa8;
  --text-dim:  #94a3b8;
  --border:    rgba(110,231,183,0.12);
  --border-md: rgba(110,231,183,0.22);
}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{
  font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  background:var(--bg);color:var(--text);overflow-x:hidden;min-height:100vh;
}
.mono{font-family:'IBM Plex Mono','Courier New',Courier,monospace;}

/* ===== DISCORD WIDGET ===== */
.discord-widget{position:fixed;bottom:1.25rem;left:1.25rem;z-index:9997;background:#5865F2;border-radius:14px;padding:.7rem 1rem .7rem .85rem;display:flex;align-items:center;gap:.65rem;box-shadow:0 4px 22px rgba(88,101,242,.45),0 0 0 1px rgba(255,255,255,.08);text-decoration:none;color:#fff;animation:discordIn .55s cubic-bezier(.22,1,.36,1) 2.5s both;transition:transform .18s,box-shadow .18s;max-width:230px;position:fixed;}
.discord-widget:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(88,101,242,.55);}
@keyframes discordIn{from{transform:translateX(-130%) scale(.9);opacity:0;}to{transform:translateX(0) scale(1);opacity:1;}}
.discord-icon{flex-shrink:0;width:28px;height:28px;}
.discord-text{display:flex;flex-direction:column;line-height:1.25;}
.discord-title{font-weight:700;font-size:.82rem;}
.discord-sub{font-size:.68rem;opacity:.82;}
.discord-x{position:absolute;top:-7px;right:-7px;width:20px;height:20px;border-radius:50%;background:rgba(20,20,40,.75);border:1px solid rgba(255,255,255,.18);color:#fff;font-size:11px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .15s;}
.discord-x:hover{background:rgba(248,113,113,.8);}

/* ===== BACKGROUND VISUALS ===== */
#bgCanvas{position:fixed;top:0;left:0;width:100%;height:100%;z-index:-4;pointer-events:none;}
.bg-orb{position:fixed;border-radius:50%;pointer-events:none;z-index:-3;filter:blur(100px);animation:orbDrift var(--dur,26s) ease-in-out infinite alternate;}
@keyframes orbDrift{0%{transform:translate(0,0) scale(1);}100%{transform:translate(var(--tx,40px),var(--ty,-30px)) scale(var(--ts,1.08));}}
.bg-grid{position:fixed;inset:0;z-index:-3;pointer-events:none;background:linear-gradient(rgba(110,231,183,0.025) 1px,transparent 1px),linear-gradient(90deg,rgba(110,231,183,0.025) 1px,transparent 1px);background-size:56px 56px;}
.bg-vignette{position:fixed;inset:0;z-index:-2;pointer-events:none;background:radial-gradient(ellipse at 50% 45%,transparent 38%,rgba(5,9,18,0.45) 72%,rgba(4,8,16,0.82) 100%);}
.bg-scanlines{position:fixed;inset:0;z-index:-2;pointer-events:none;background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,0,0,0.07) 3px,rgba(0,0,0,0.07) 4px);}

/* ===== NAV ===== */
nav{position:fixed;top:0;left:0;right:0;z-index:1000;background:var(--bg-nav);border-bottom:1px solid var(--border);height:54px;display:flex;align-items:center;padding:0 1.5rem;transition:box-shadow 0.2s;}
nav.scrolled{box-shadow:0 2px 20px rgba(0,0,0,0.4);}
.nav-inner{max-width:1600px;margin:0 auto;width:100%;display:flex;align-items:center;justify-content:space-between;}
.nav-brand{display:flex;align-items:center;gap:0.45rem;text-decoration:none;font-weight:700;font-size:0.82rem;color:var(--text);letter-spacing:0.08em;text-transform:uppercase;font-family:'IBM Plex Mono','Courier New',Courier,monospace;}
.nav-links{display:flex;align-items:center;gap:0.05rem;}
.nav-link{color:var(--text-dim);text-decoration:none;padding:0.3rem 0.7rem;font-size:0.78rem;font-weight:500;border-bottom:2px solid transparent;transition:all 0.18s;}
.nav-link:hover{color:var(--teal);}
.nav-cta{background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%);color:#060a0f;text-decoration:none;padding:0.35rem 1rem;font-size:0.78rem;font-weight:700;border-radius:6px;margin-left:0.6rem;transition:transform 0.18s,box-shadow 0.18s;box-shadow:0 2px 10px rgba(110,231,183,.28);}
.nav-cta:hover{transform:translateY(-1px);box-shadow:0 4px 18px rgba(110,231,183,.45);}
.nav-hamburger{display:none;flex-direction:column;gap:5px;background:none;border:none;cursor:pointer;padding:4px;}
.nav-hamburger span{display:block;width:22px;height:2px;background:var(--text-dim);border-radius:2px;transition:all 0.2s;}
.nav-hamburger.active span:nth-child(1){transform:translateY(7px) rotate(45deg);}
.nav-hamburger.active span:nth-child(2){opacity:0;}
.nav-hamburger.active span:nth-child(3){transform:translateY(-7px) rotate(-45deg);}
@media(max-width:768px){.nav-links{display:none;}.nav-hamburger{display:flex;}}
.mobile-menu{display:none;position:fixed;top:54px;left:0;right:0;z-index:999;background:var(--bg-nav);border-bottom:1px solid var(--border);padding:1rem 1.5rem;flex-direction:column;gap:0.25rem;}
.mobile-menu.open{display:flex;}
.mobile-menu a{color:var(--text-dim);text-decoration:none;padding:0.5rem 0;font-size:0.9rem;border-bottom:1px solid var(--border);}
.mobile-menu a:last-child{border-bottom:none;}
.mobile-menu a:hover{color:var(--teal);}

/* ===== PAGE LAYOUT ===== */
.content-area{max-width:1600px;margin:0 auto;padding:68px 1.25rem 3rem;position:relative;z-index:1;}
.container{max-width:1200px;margin:0 auto;}

/* ===== FOOTER ===== */
footer{background:var(--bg-nav);border-top:1px solid var(--border);padding:1.75rem;margin-top:3rem;}
.footer-inner{max-width:1600px;margin:0 auto;}
.footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:2rem;margin-bottom:1.2rem;}
@media(max-width:768px){.footer-grid{grid-template-columns:1fr 1fr;}}
.footer-brand{font-weight:700;font-size:0.82rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--text);margin-bottom:0.4rem;}
.footer-tagline{font-size:0.72rem;color:var(--text-muted);line-height:1.55;}
.footer-col h4{font-size:0.6rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--teal);margin-bottom:0.5rem;}
.footer-col a{display:block;color:var(--text-muted);text-decoration:none;font-size:0.74rem;margin-bottom:0.28rem;transition:color 0.18s;}
.footer-col a:hover{color:var(--teal);}
.footer-bottom{display:flex;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;padding-top:1rem;border-top:1px solid var(--border);}
.footer-copy,.footer-links a{font-size:0.7rem;color:var(--text-muted);}
.footer-links{display:flex;gap:1rem;}
.footer-links a:hover{color:var(--text);}
</style>
<style>
/* ===== PLAYER 2 GUIDE — RSA STYLE ===== */

/* Content area override */
.content-area .container { max-width:1200px !important; padding:0 !important; background:transparent !important; border:none !important; box-shadow:none !important; }

/* Hero */
.p2-hero { text-align:center; padding:88px 2rem 50px; max-width:1200px; margin:0 auto; }
.hero-icon { width:90px; height:90px; border-radius:50%; background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%); display:flex; align-items:center; justify-content:center; font-size:2.6rem; margin:0 auto 1.5rem; box-shadow:0 0 40px rgba(110,231,183,0.4); animation:heroGlow 3s ease-in-out infinite; }
@keyframes heroGlow { 0%,100%{box-shadow:0 0 40px rgba(110,231,183,0.3);} 50%{box-shadow:0 0 65px rgba(110,231,183,0.6);} }
.guide-badge { display:inline-flex; align-items:center; gap:0.5rem; background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%); padding:0.5rem 1.2rem; border-radius:20px; color:#060a0f; font-family:'IBM Plex Mono',monospace; font-size:0.85rem; font-weight:700; letter-spacing:0.05em; animation:pulseBadge 2s infinite; box-shadow:0 0 30px rgba(110,231,183,0.4); margin-bottom:1.5rem; }
@keyframes pulseBadge { 0%,100%{box-shadow:0 0 30px rgba(110,231,183,0.4);} 50%{box-shadow:0 0 50px rgba(110,231,183,0.7);} }
.p2-hero h1 { font-size:clamp(2rem,4vw,3.5rem); font-weight:900; font-family:'IBM Plex Mono',monospace; margin:0 0 1rem; line-height:1.15; color:#fff; }
.p2-hero h1 .accent { background:linear-gradient(135deg,#6ee7b7,#a7f3d0,#34d399); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.p2-hero > p { color:var(--text-dim); font-size:1.05rem; max-width:680px; margin:0 auto; line-height:1.7; }

/* Stats Row */
.stats-row { display:grid; grid-template-columns:repeat(4,1fr); gap:1.2rem; margin:2.5rem auto 0; max-width:900px; }
@media(max-width:700px){ .stats-row { grid-template-columns:repeat(2,1fr); } }
.stat-card { background:var(--bg-card) !important; border:1px solid var(--border) !important; border-radius:14px; padding:1.3rem 1rem; text-align:center; transition:all 0.3s; }
.stat-card:hover { transform:translateY(-3px); box-shadow:0 8px 25px rgba(0,0,0,0.3); }
.stat-value { font-size:1.7rem; font-weight:800; background:linear-gradient(135deg,#6ee7b7,#a7f3d0); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; font-family:'IBM Plex Mono',monospace; margin-bottom:0.25rem; }
.stat-label { font-size:0.75rem; color:var(--text-dim); text-transform:uppercase; letter-spacing:0.05em; }

/* Divider */
.divider { border:none; border-top:1px solid var(--border); margin:2.5rem 0; }

/* Section Headers */
.section-head { display:flex; align-items:center; gap:0.8rem; margin:2.5rem 0 1.5rem; }
.section-head h2 { font-size:1.3rem; font-weight:800; color:var(--teal); font-family:'IBM Plex Mono',monospace; margin:0; white-space:nowrap; }
.section-head .line { flex:1; height:1px; background:linear-gradient(90deg,rgba(110,231,183,0.3),transparent); }

/* Intro box */
.intro-box { background:var(--bg-card) !important; border:1px solid var(--border) !important; border-left:4px solid var(--teal) !important; border-radius:14px; padding:2rem; margin-bottom:1rem; }
.intro-box p { color:var(--text-dim); font-size:0.95rem; line-height:1.8; margin:0 0 0.8rem; }
.intro-box p:last-child { margin:0; }
.intro-box strong { color:#fff; }

/* Steps */
.steps-list { display:flex; flex-direction:column; gap:1rem; }
.step-item { background:rgba(110,231,183,0.03); border:1px solid var(--border); border-radius:14px; padding:1.4rem 1.5rem; display:flex; gap:1.2rem; align-items:flex-start; position:relative; overflow:hidden; transition:border-color 0.2s,transform 0.2s; }
.step-item:hover { border-color:var(--border-md); transform:translateX(4px); }
.step-item::before { content:''; position:absolute; top:0; left:0; bottom:0; width:3px; background:linear-gradient(180deg,var(--teal),#34d399); opacity:0.7; }
.step-num { width:40px; height:40px; min-width:40px; background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%); border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1rem; color:#060a0f; box-shadow:0 0 15px rgba(110,231,183,0.4); }
.step-body h3 { font-size:1.05rem; font-weight:800; color:#fff; margin:0 0 0.4rem; }
.step-body p { font-size:0.88rem; color:var(--text-dim); line-height:1.65; margin:0; }

/* Requirements Cards */
.req-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:1rem; }
@media(max-width:700px){ .req-grid { grid-template-columns:1fr; } }
.req-card { background:rgba(110,231,183,0.03); border:1px solid var(--border); border-radius:14px; padding:1.4rem; position:relative; overflow:hidden; transition:border-color 0.2s,transform 0.2s; }
.req-card:hover { border-color:var(--border-md); transform:translateY(-3px); }
.req-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; background:linear-gradient(90deg,var(--teal),#34d399); transform:translateX(-100%); transition:transform 0.5s; }
.req-card:hover::before { transform:translateX(0); }
.req-icon { font-size:1.8rem; margin-bottom:0.7rem; }
.req-card h3 { font-size:1rem; font-weight:800; color:#fff; margin:0 0 0.5rem; }
.req-card p { font-size:0.85rem; color:var(--text-dim); line-height:1.65; margin:0; }
.req-card a { color:var(--teal); text-decoration:none; }
.req-card a:hover { color:#a7f3d0; }

/* Benefits list */
.benefits-box { background:var(--bg-card) !important; border:1px solid var(--border) !important; border-left:4px solid var(--teal) !important; border-radius:14px; padding:2rem; }
.benefits-box ul { list-style:none; padding:0; margin:0; }
.benefits-box li { font-size:0.9rem; color:var(--text-dim); line-height:1.7; padding:0.5rem 0 0.5rem 1.6rem; position:relative; border-bottom:1px solid var(--border); }
.benefits-box li:last-child { border-bottom:none; }
.benefits-box li::before { content:'✓'; position:absolute; left:0; color:var(--teal); font-weight:700; }
.benefits-box li strong { color:#fff; }

/* Skrill callout */
.skrill-box { background:rgba(110,231,183,0.05) !important; border:1px solid rgba(110,231,183,0.2) !important; border-radius:16px; padding:2rem; text-align:center; margin-top:0; }
.skrill-box h3 { font-size:1.2rem; font-weight:800; color:#fff; margin:0 0 0.7rem; font-family:'IBM Plex Mono',monospace; }
.skrill-box p { font-size:0.9rem; color:var(--text-dim); line-height:1.75; max-width:620px; margin:0 auto 1.2rem; }
.skrill-box strong { color:var(--teal); }

/* FAQ */
.faq-list { display:flex; flex-direction:column; gap:0.8rem; }
.faq-item { background:rgba(110,231,183,0.03) !important; border:1px solid var(--border) !important; border-radius:12px !important; overflow:hidden; transition:border-color 0.3s; }
.faq-item:hover { border-color:var(--border-md) !important; }
.faq-q { padding:1.2rem 1.5rem; cursor:pointer; display:flex; align-items:center; justify-content:space-between; transition:background 0.2s; gap:1rem; }
.faq-q:hover { background:rgba(110,231,183,0.04); }
.faq-q span { font-size:0.95rem; font-weight:700; color:#fff; }
.faq-arrow { color:var(--teal); font-size:1.1rem; transition:transform 0.3s; flex-shrink:0; }
.faq-item.open .faq-arrow { transform:rotate(180deg); }
.faq-a { padding:0 1.5rem; display:none; }
.faq-item.open .faq-a { display:block; padding:0 1.5rem 1.2rem; }
.faq-a p { font-size:0.88rem; color:var(--text-dim); line-height:1.7; margin:0; }

/* CTA row */
.cta-row { display:flex; gap:1rem; flex-wrap:wrap; justify-content:center; margin:2rem 0; }
.btn-primary { display:inline-flex; align-items:center; gap:0.5rem; background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%); color:#060a0f !important; padding:0.9rem 2rem; border-radius:50px; text-decoration:none !important; font-weight:800; font-size:1rem; box-shadow:0 0 25px rgba(110,231,183,0.4); transition:transform 0.2s,box-shadow 0.2s; }
.btn-primary:hover { transform:translateY(-3px); box-shadow:0 0 40px rgba(110,231,183,0.6); }
.btn-secondary { display:inline-flex; align-items:center; gap:0.5rem; background:transparent; border:2px solid rgba(110,231,183,0.3); color:var(--teal) !important; padding:0.9rem 2rem; border-radius:50px; text-decoration:none !important; font-weight:700; font-size:1rem; transition:all 0.2s; }
.btn-secondary:hover { background:rgba(110,231,183,0.08); border-color:var(--teal); }

/* Fade animations */
.anim-fade-up { opacity:0; transform:translateY(24px); transition:opacity 0.55s ease-out,transform 0.55s ease-out; }
.anim-fade-up.visible { opacity:1; transform:translateY(0); }

@media(max-width:768px){
  .p2-hero { padding:80px 1.25rem 40px; }
  .step-item { padding:1.2rem; }
  .benefits-box, .intro-box, .skrill-box { padding:1.25rem; }
}
</style>
</head>"""

content = content[:style_start] + new_styles + content[head_end:]

print(f"Styles replaced. style_start={style_start}, head_end={head_end}")

# ---- 4. Replace <canvas id="starfield"> with bgCanvas + bg layers ----
content = content.replace(
    '<!-- Starfield Canvas -->\n<canvas id="starfield"></canvas>',
    '''<!-- Background layers -->
<canvas id="bgCanvas"></canvas>
<div class="bg-orb" style="width:520px;height:520px;top:-12%;left:-8%;background:radial-gradient(circle,rgba(110,231,183,0.13) 0%,transparent 70%);--dur:28s;--tx:50px;--ty:40px;--ts:1.1;"></div>
<div class="bg-orb" style="width:400px;height:400px;bottom:-10%;right:-5%;background:radial-gradient(circle,rgba(96,165,250,0.09) 0%,transparent 70%);--dur:34s;--tx:-40px;--ty:-30px;--ts:1.06;"></div>
<div class="bg-grid"></div>
<div class="bg-scanlines"></div>
<div class="bg-vignette"></div>'''
)

# ---- 5. Remove dark-forest.js script tag ----
content = content.replace('\n<script src="/js/dark-forest.js"></script>', '')

# ---- 6. Replace old inline script with RSA scripts ----
old_script_start = content.find('\n<script>\n// Nav scroll\nconst nav = document.getElementById(\'nav\');\nwindow.addEventListener(\'scroll\', () => { nav.classList.toggle(\'scrolled\', window.scrollY > 20); }')
old_script_end = content.find('</script>', old_script_start) + len('</script>')

if old_script_start == -1:
    print("Could not find old script — trying alternate search")
    old_script_start = content.find('// Nav scroll\nconst nav')
    if old_script_start != -1:
        old_script_start = content.rfind('<script>', 0, old_script_start)
        old_script_end = content.find('</script>', old_script_start) + len('</script>')
    else:
        print("ERROR: Could not find old script block")

print(f"Script block: {old_script_start} -> {old_script_end}")

rsa_scripts = '''
<script>
// ===== BACKGROUND STARFIELD =====
(function(){
  const c=document.getElementById('bgCanvas');
  if(!c)return;
  const ctx=c.getContext('2d');
  let W,H,stars=[],frame=0;
  function resize(){W=c.width=window.innerWidth;H=c.height=window.innerHeight;}
  function init(){
    stars=[];
    const n=Math.floor(W*H/3200);
    for(let i=0;i<n;i++){
      const r=Math.random();
      const col = r>0.93 ? 'rgba(110,231,183,' :
                  r>0.85 ? 'rgba(192,132,252,' :
                  r>0.80 ? 'rgba(173,255,47,'  : 'rgba(210,225,255,';
      stars.push({x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.5+0.15,a:Math.random()*0.65+0.12,s:Math.random()*0.004+0.0008,p:Math.random()*Math.PI*2,col});
    }
  }
  function draw(){
    ctx.clearRect(0,0,W,H);frame++;
    stars.forEach(s=>{
      const t=0.3+0.7*Math.sin(frame*s.s+s.p);
      ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
      ctx.fillStyle=s.col+(s.a*t).toFixed(2)+')';ctx.fill();
      if(s.r>1.2&&t>0.85&&s.col!=='rgba(210,225,255,'){
        ctx.globalAlpha=(s.a*t*0.5);ctx.strokeStyle=s.col+'0.6)';ctx.lineWidth=0.5;
        ctx.beginPath();ctx.moveTo(s.x-s.r*3,s.y);ctx.lineTo(s.x+s.r*3,s.y);
        ctx.moveTo(s.x,s.y-s.r*3);ctx.lineTo(s.x,s.y+s.r*3);ctx.stroke();ctx.globalAlpha=1;
      }
    });
    requestAnimationFrame(draw);
  }
  resize();init();draw();
  window.addEventListener('resize',()=>{resize();init();},{passive:true});
})();

// ===== NAV SCROLL =====
window.addEventListener('scroll',()=>{document.getElementById('nav').classList.toggle('scrolled',window.scrollY>20);},{passive:true});

// ===== HAMBURGER MENU =====
(function(){
  const ham=document.getElementById('hamburger');
  const mMenu=document.getElementById('mobileMenu');
  if(!ham||!mMenu)return;
  ham.addEventListener('click',()=>{
    ham.classList.toggle('active');
    mMenu.classList.toggle('open');
    document.body.style.overflow=mMenu.classList.contains('open')?'hidden':'';
  });
  mMenu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{
    ham.classList.remove('active');mMenu.classList.remove('open');document.body.style.overflow='';
  }));
})();

// ===== FADE-IN =====
(function(){
  const obs=new IntersectionObserver((entries)=>{
    entries.forEach((entry,i)=>{
      if(entry.isIntersecting){
        setTimeout(()=>entry.target.classList.add('visible'),i*60);
        obs.unobserve(entry.target);
      }
    });
  },{threshold:0.08,rootMargin:'0px 0px -30px 0px'});
  document.querySelectorAll('.anim-fade-up').forEach(el=>obs.observe(el));
})();

// ===== FAQ =====
document.querySelectorAll('.faq-q').forEach(q=>{
  q.addEventListener('click',()=>{
    const item=q.parentElement;
    const isOpen=item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(i=>i.classList.remove('open'));
    if(!isOpen)item.classList.add('open');
  });
});
</script>'''

content = content[:old_script_start] + rsa_scripts + content[old_script_end:]

# ---- 7. Update footer brand (remove 🌲) ----
content = content.replace(
    '<div class="footer-brand">🌲 ONLINE SIDEHUSTLES</div>',
    '<div class="footer-brand">ONLINE SIDEHUSTLES</div>'
)

with open('guide-player-2.html', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Done. Final file length: {len(content)}")
