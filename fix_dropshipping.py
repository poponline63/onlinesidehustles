
import re

with open('dropshipping.html', encoding='utf-8') as f:
    content = f.read()

# Find the second style block boundaries
style2_start = content.find('<style>\n/* ===== DROPSHIPPING PAGE CONTENT')
marker_end = '</style>\n</head>'
style2_end = content.find(marker_end, style2_start) + len(marker_end)

print(f"style2_start={style2_start}, style2_end={style2_end}, length={style2_end-style2_start}")

rsa_css = """<style>
/* ===== DROPSHIPPING PAGE CONTENT - RSA STYLE ===== */

/* Reset container override */
.content-area .container {
  max-width: 1200px !important; width: calc(100% - 2.5rem) !important;
  padding: 0 !important; margin: 0 auto !important;
  background: transparent !important; border: none !important;
  box-shadow: none !important; border-radius: 0 !important; overflow: visible !important;
}
.content-area { background: transparent !important; }
.main-container { max-width: 100% !important; padding: 0 !important; }
.content-wrapper { max-width: 100%; margin: 0; padding: 0; }

/* Hero */
.hero-section {
  text-align: center; padding: 88px 2rem 60px;
  max-width: 1200px; margin: 0 auto;
  background: transparent !important; border: none !important; border-radius: 0 !important;
}
.hero-icon {
  width: 90px; height: 90px; border-radius: 50%;
  background: linear-gradient(135deg, #6ee7b7 0%, #34d399 100%);
  display: flex; align-items: center; justify-content: center; font-size: 2.8rem;
  margin: 0 auto 1.5rem; box-shadow: 0 0 40px rgba(110,231,183,0.4);
  animation: heroGlow 3s ease-in-out infinite;
}
@keyframes heroGlow {
  0%,100%{box-shadow:0 0 40px rgba(110,231,183,0.3);}
  50%{box-shadow:0 0 65px rgba(110,231,183,0.6);}
}
.space-badge {
  display: inline-flex; align-items: center; gap: 0.5rem;
  background: linear-gradient(135deg, #6ee7b7 0%, #34d399 100%);
  padding: 0.5rem 1.2rem; border-radius: 20px; color: #060a0f;
  font-family: 'IBM Plex Mono', monospace; font-size: 0.85rem; font-weight: 700; letter-spacing: 0.05em;
  animation: pulseBadge 2s infinite; box-shadow: 0 0 30px rgba(110,231,183,0.4); margin-bottom: 1.5rem;
}
@keyframes pulseBadge { 0%,100%{box-shadow:0 0 30px rgba(110,231,183,0.4);} 50%{box-shadow:0 0 50px rgba(110,231,183,0.7);} }
.hero-section h1 {
  font-size: clamp(2rem, 4vw, 3.5rem); font-weight: 900;
  font-family: 'IBM Plex Mono', monospace; margin: 0 0 1rem; line-height: 1.15;
}
.shimmer-text {
  background: linear-gradient(135deg, #6ee7b7, #a7f3d0, #34d399);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-description { color: var(--text-dim); font-size: 1.1rem; line-height: 1.7; max-width: 700px; margin: 0 auto 2rem; }
.hero-btns { display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center; }
.btn-emerald {
  display: inline-flex; align-items: center; gap: 0.5rem;
  background: linear-gradient(135deg, #6ee7b7 0%, #34d399 100%); color: #060a0f;
  text-decoration: none; padding: 0.85rem 2rem; border-radius: 50px; font-size: 1rem; font-weight: 700;
  box-shadow: 0 0 20px rgba(110,231,183,0.4); transition: transform 0.2s, box-shadow 0.2s;
}
.btn-emerald:hover { transform: translateY(-2px); box-shadow: 0 0 35px rgba(110,231,183,0.6); }
.btn-outline {
  display: inline-flex; align-items: center; gap: 0.5rem;
  background: transparent; color: var(--teal);
  text-decoration: none; padding: 0.85rem 2rem; border-radius: 50px; font-size: 1rem; font-weight: 700;
  border: 2px solid rgba(110,231,183,0.4); transition: all 0.2s;
}
.btn-outline:hover { border-color: var(--teal); background: rgba(110,231,183,0.07); }

/* Stats */
.stats-grid {
  display: grid; grid-template-columns: repeat(4,1fr); gap: 1.5rem;
  max-width: 1200px; margin: 0 auto 3rem; padding: 0 2rem;
}
@media(max-width:768px){ .stats-grid { grid-template-columns: repeat(2,1fr); } }
.stat-card {
  background: var(--bg-card) !important; border: 1px solid var(--border) !important;
  border-radius: 15px; padding: 1.5rem; text-align: center;
  position: relative; overflow: hidden; transition: all 0.3s;
}
.stat-card:hover { transform: translateY(-4px); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
.stat-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
.stat-value {
  font-size: 1.8rem; font-weight: bold;
  background: linear-gradient(135deg, #6ee7b7, #a7f3d0);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  font-family: 'IBM Plex Mono', monospace; margin-bottom: 0.25rem;
}
.stat-label { color: var(--text-dim); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }

/* Content Sections */
.content-section {
  background: var(--bg-card) !important; border: 1px solid var(--border) !important;
  border-left: 4px solid var(--teal) !important; border-radius: 20px !important;
  padding: 3rem !important; margin-bottom: 3rem !important;
  max-width: 1200px !important; margin-left: auto !important; margin-right: auto !important;
  box-shadow: 0 10px 40px rgba(0,0,0,0.3) !important;
}
.section-title {
  font-size: 1.75rem; font-weight: bold; color: var(--teal);
  font-family: 'IBM Plex Mono', monospace; display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;
}
.section-icon { font-size: 1.4rem; }
.section-content p { color: var(--text-dim); line-height: 1.8; margin-bottom: 1rem; }
.section-content ul { color: var(--text-dim); line-height: 1.8; padding-left: 1.5rem; }
.section-content li { margin-bottom: 0.6rem; }
.highlight { color: var(--teal); font-weight: 700; }

/* App Items */
.apps-grid { display: flex; flex-direction: column; gap: 1rem; margin-top: 1.5rem; }
.app-item {
  background: rgba(110,231,183,0.04); border: 1px solid var(--border); border-radius: 15px;
  padding: 1.5rem 2rem; display: flex; justify-content: space-between; align-items: flex-start;
  gap: 1.5rem; transition: all 0.3s; position: relative; overflow: hidden;
}
.app-item::before { content:''; position:absolute; top:0;left:0;right:0;height:3px; background:linear-gradient(90deg,var(--teal),#34d399); transform:translateX(-100%); transition:transform 0.5s; }
.app-item:hover::before { transform: translateX(0); }
.app-item:hover { border-color: var(--border-md); }
.app-info { flex: 1; }
.app-info h3 { font-size: 1.05rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem; }
.app-info p { font-size: 0.88rem; color: var(--text-dim); line-height: 1.7; margin-bottom: 0.75rem; }
.app-earn { text-align: right; flex-shrink: 0; }
.earn-amt { font-size: 1.3rem; font-weight: 800; background: linear-gradient(135deg,#6ee7b7,#a7f3d0); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; font-family:'IBM Plex Mono',monospace; }
.earn-label { font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }

/* Badges */
.badge { display:inline-block; font-size:0.68rem; font-weight:700; letter-spacing:0.06em; padding:0.2rem 0.6rem; border-radius:6px; margin-right:0.3rem; margin-bottom:0.3rem; }
.badge-gold   { background:rgba(251,191,36,0.10);  color:#fbbf24; border:1px solid rgba(251,191,36,0.25); }
.badge-green  { background:rgba(110,231,183,0.12); color:#6ee7b7; border:1px solid rgba(110,231,183,0.25); }
.badge-blue   { background:rgba(96,165,250,0.10);  color:#60a5fa; border:1px solid rgba(96,165,250,0.22); }
.badge-red    { background:rgba(248,113,113,0.08); color:#f87171; border:1px solid rgba(248,113,113,0.18); }
.badge-purple { background:rgba(192,132,252,0.08); color:#c084fc; border:1px solid rgba(192,132,252,0.18); }

/* Category Headers */
.cat-header { display:flex; align-items:center; gap:1rem; margin:2rem 0 1rem; }
.cat-header h3 { font-size:1rem; font-weight:700; color:var(--teal); font-family:'IBM Plex Mono',monospace; margin:0; white-space:nowrap; }
.cat-line { flex:1; height:1px; background:rgba(110,231,183,0.2); }

/* Steps */
.steps-container { display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin-top:1.5rem; }
@media(max-width:768px){ .steps-container { grid-template-columns:repeat(2,1fr); } }
.step-card { background:rgba(110,231,183,0.04); border:1px solid var(--border); border-radius:12px; padding:1.5rem 1rem; text-align:center; transition:all 0.3s; }
.step-card:hover { border-color:var(--border-md); transform:translateY(-3px); }
.step-number { width:40px; height:40px; background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:1.1rem; font-weight:800; color:#060a0f; margin:0 auto 0.8rem; box-shadow:0 0 15px rgba(110,231,183,0.4); }
.step-title { font-size:0.95rem; font-weight:700; color:#fff; margin-bottom:0.5rem; }
.step-description { font-size:0.82rem; color:var(--text-dim); line-height:1.5; }

/* Info Boxes */
.info-box { background:rgba(110,231,183,0.06) !important; border:1px solid rgba(110,231,183,0.2) !important; border-left:4px solid var(--teal) !important; border-radius:10px !important; padding:1.5rem !important; margin:1.5rem 0 !important; }
.warning-box { background:rgba(255,215,0,0.06) !important; border:1px solid rgba(255,215,0,0.25) !important; border-left:4px solid #FFD700 !important; }
.info-box-title { font-size:1rem; font-weight:700; color:var(--teal); margin-bottom:0.75rem; }
.warning-box .info-box-title { color:#FFD700; }
.info-box-content { font-size:0.9rem; color:var(--text-dim); line-height:1.7; }
.info-box-content a { color:var(--teal); text-decoration:underline; }

/* Math Box */
.math-box { background:var(--bg-darker); border:1px solid var(--border); border-radius:12px; overflow:hidden; margin-bottom:1.2rem; }
.math-box h3 { padding:1.2rem 1.5rem; font-size:1rem; font-weight:700; color:var(--teal); font-family:'IBM Plex Mono',monospace; background:rgba(110,231,183,0.07); border-bottom:1px solid var(--border); }
.math-rows { padding:0.5rem 1.5rem 1.2rem; }
.math-row { display:flex; justify-content:space-between; align-items:center; padding:0.6rem 0; border-bottom:1px solid var(--border); font-size:0.9rem; }
.math-row:last-child { border-bottom:none; }
.r-name { color:var(--text-dim); }
.r-val { color:var(--teal); font-weight:600; font-family:'IBM Plex Mono',monospace; }
.math-total { display:flex; justify-content:space-between; align-items:center; padding:0.8rem 0 0; margin-top:0.3rem; border-top:1px solid var(--border-md); font-size:0.95rem; font-weight:700; color:#fff; }

/* Supplier Tags */
.supplier-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(140px,1fr)); gap:0.75rem; margin-top:1.5rem; }
.supplier-tag { background:rgba(110,231,183,0.07); border:1px solid var(--border); border-radius:10px; padding:0.8rem; text-align:center; font-size:0.85rem; font-weight:600; color:var(--teal); transition:all 0.2s; }
.supplier-tag:hover { transform:translateY(-2px); border-color:var(--border-md); box-shadow:0 4px 15px rgba(110,231,183,0.15); }

/* FAQ */
.faq-container { display:flex; flex-direction:column; gap:0.75rem; }
.faq-item { background:rgba(110,231,183,0.04) !important; border:1px solid var(--border) !important; border-radius:10px !important; overflow:hidden; transition:border-color 0.3s; }
.faq-item:hover { border-color:var(--border-md) !important; }
.faq-question { padding:1.2rem 1.5rem; font-weight:700; color:#fff; font-size:0.95rem; cursor:pointer; display:flex; justify-content:space-between; align-items:center; }
.faq-question::after { content:'+'; font-size:1.5rem; color:var(--teal); transition:transform 0.3s; }
.faq-item.open .faq-question::after { transform:rotate(45deg); }
.faq-answer { max-height:0; overflow:hidden; transition:max-height 0.4s ease,padding 0.4s ease; padding:0 1.5rem; }
.faq-item.open .faq-answer { max-height:300px; padding:0 1.5rem 1.2rem; }
.faq-answer p { color:var(--text-dim); font-size:0.9rem; line-height:1.7; margin:0; }

/* CTA Section */
.cta-section { background:rgba(110,231,183,0.06) !important; border:2px solid rgba(110,231,183,0.25) !important; border-radius:20px !important; padding:4rem 3rem !important; text-align:center; max-width:1200px !important; margin-left:auto !important; margin-right:auto !important; margin-bottom:3rem !important; }
.cta-title { font-size:2rem; font-weight:900; background:linear-gradient(135deg,#6ee7b7,#a7f3d0,#34d399); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; font-family:'IBM Plex Mono',monospace; margin-bottom:1rem; }
.cta-description { color:var(--text-dim); font-size:1rem; line-height:1.7; max-width:600px; margin:0 auto 2rem; }
.cta-button { display:inline-flex !important; align-items:center !important; gap:0.6rem !important; background:linear-gradient(135deg,#6ee7b7 0%,#34d399 100%) !important; color:#060a0f !important; text-decoration:none !important; padding:1rem 2.5rem !important; border-radius:50px !important; font-size:1.05rem !important; font-weight:700 !important; box-shadow:0 0 25px rgba(110,231,183,0.4) !important; animation:ctaPulse 2.5s ease-in-out infinite !important; transition:transform 0.2s !important; }
.cta-button:hover { transform:translateY(-3px) scale(1.03) !important; }
@keyframes ctaPulse { 0%,100%{box-shadow:0 0 25px rgba(110,231,183,0.4);} 50%{box-shadow:0 0 50px rgba(110,231,183,0.7);} }

/* Fade */
.anim-fade-up { opacity:0; transform:translateY(28px); transition:opacity 0.65s ease-out,transform 0.65s ease-out; }
.anim-fade-up.visible { opacity:1; transform:translateY(0); }

@media(max-width:768px){
  .hero-section { padding:80px 1.25rem 40px !important; }
  .stats-grid { padding:0 1.25rem; }
  .content-section { padding:2rem 1.25rem !important; border-radius:16px !important; }
  .cta-section { padding:2.5rem 1.25rem !important; }
  .app-item { flex-direction:column; }
  .app-earn { text-align:left; }
  .steps-container { grid-template-columns:1fr 1fr !important; }
}
</style>
</head>"""

content = content[:style2_start] + rsa_css + content[style2_end:]
with open('dropshipping.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Style block replaced. New file length:', len(content))
