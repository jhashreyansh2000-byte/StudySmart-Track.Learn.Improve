"""
StudySmart — shared CSS, served at /static/style.css
"""

STYLE_CSS = r"""
/* ============================================================
   DESIGN TOKENS
   ============================================================ */
:root{
  color-scheme:light;
  --bg-dark:#0d211d;
  --bg-darker:#0a1a17;
  --panel-dark:#12332d;
  --accent:#2ecf9c;
  --accent-light:#a9f0d6;
  --bg-light:#eef6f3;
  --text-light:#f3f7f5;
  --text-muted:#9db3ac;
  --text-dark:#12211d;
  --text-dark-muted:#5c6f6a;
  --card-bg:#ffffff;
  --border:#e1ebe7;
  --radius:16px;
  --radius-sm:10px;
  --shadow:0 10px 30px rgba(13,33,29,0.08);
  --purple:#6c63ff; --blue:#4a7bf7; --orange:#f59e0b; --teal:#12b8a6;
  --pink:#ec4899; --amber:#d97706; --indigo:#4f46e5; --emerald:#059669; --sky:#0284c7; --green:#2ecf9c;
}
/* ============================================================
   BASE / RESET
   ============================================================ */
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{
  margin:0;
  font-family:'Inter',sans-serif;
  color:var(--text-dark);
  background:var(--bg-light);
  -webkit-font-smoothing:antialiased;
}
h1,h2,h3{font-family:'Sora',sans-serif; margin:0 0 .4em; letter-spacing:-0.02em;}
p{margin:0 0 1em; line-height:1.6; color:var(--text-dark-muted);}
a{color:inherit; text-decoration:none;}
.muted{color:var(--text-muted);}
img,svg{display:block;}
ul{list-style:none; margin:0; padding:0;}

/* Sane, theme-aware default for every plain form control in the app --
   anything more specific (.auth-form input, .inline-form input, etc.)
   still wins via normal cascade rules since those are declared later
   and/or more specific. This is what was missing for Settings' bare
   inputs (avatar, full name, class, disabled username/email), which
   is why their text was unreadable in dark mode -- they were falling
   back to the browser's own default colors instead of ours. */
input, select, textarea{
  color:var(--text-dark); background:var(--card-bg); border:1px solid var(--border);
  border-radius:var(--radius-sm); padding:9px 12px; font-family:inherit; font-size:.88rem;
}
input:disabled, select:disabled, textarea:disabled{opacity:.6; cursor:not-allowed;}
input::placeholder, textarea::placeholder{color:var(--text-dark-muted); opacity:.8;}

/* ============================================================
   BUTTONS
   ============================================================ */

.btn{
  display:inline-flex; align-items:center; gap:8px; justify-content:center;
  padding:14px 24px; border-radius:999px; font-weight:600; font-size:.95rem;
  border:1px solid transparent; cursor:pointer; transition:transform .15s ease, box-shadow .15s ease, background .15s ease;
  white-space:nowrap;
}
.btn:active{transform:scale(.97);}
.btn-primary{background:var(--accent); color:#06231c;}
.btn-primary:hover{background:#25b98a; box-shadow:0 8px 20px rgba(46,207,156,.35);}
.btn-outline{background:transparent; color:var(--text-light); border-color:rgba(255,255,255,.35);}
.btn-outline:hover{background:rgba(255,255,255,.08);}
.btn-block{width:100%;}
.btn-sm{padding:9px 16px; font-size:.85rem;}
.badge-pill{
  display:inline-flex; align-items:center; gap:6px; padding:6px 14px; border-radius:999px;
  background:rgba(46,207,156,.12); color:var(--accent); font-size:.8rem; font-weight:600; margin-bottom:16px;
}

/* ============================================================
   SITE HEADER / NAV
   ============================================================ */

.site-header{position:sticky; top:0; z-index:50; background:var(--bg-dark); border-bottom:1px solid rgba(255,255,255,.06);}
.nav-inner{max-width:1240px; margin:0 auto; display:flex; align-items:center; justify-content:space-between; padding:16px 32px;}
.logo{display:flex; align-items:center; gap:8px; font-family:'Sora',sans-serif; font-weight:700; font-size:1.15rem; color:var(--text-light);}
.logo-mark{width:32px; height:32px; border-radius:9px; background:var(--accent); color:#06231c; display:flex; align-items:center; justify-content:center;}
.main-nav{display:flex; gap:32px;}
.nav-link{color:var(--text-muted); font-weight:500; font-size:.95rem; transition:color .15s;}
.nav-link:hover{color:var(--text-light);}
.nav-actions{display:flex; align-items:center; gap:14px;}
.nav-toggle{display:none; flex-direction:column; gap:4px; background:none; border:none; cursor:pointer; padding:6px;}
.nav-toggle span{width:22px; height:2px; background:var(--text-light); border-radius:2px;}
.nav-greeting{color:var(--text-muted); font-size:.85rem; margin-right:2px;}
.login-link{color:var(--text-light); font-weight:500; font-size:.9rem;}
.nav-actions .btn-outline{color:var(--text-light); border-color:rgba(255,255,255,.3);}
.nav-link-mobile-only{display:none;}

/* ============================================================
   HERO SECTION
   ============================================================ */

.hero{background:var(--bg-dark); padding:64px 32px 90px; overflow:hidden;}
.hero-inner{max-width:1240px; margin:0 auto; display:grid; grid-template-columns:1fr 1fr; gap:56px; align-items:center;}
.hero-title{font-size:3.4rem; line-height:1.05; color:var(--text-light); font-weight:800;}
.hero-title .accent{color:var(--accent);}
.hero-sub{color:var(--text-muted); font-size:1.05rem; max-width:460px;}
.hero-cta{display:flex; gap:14px; margin:28px 0 40px; flex-wrap:wrap;}
.hero-mini-stats{display:flex; gap:28px; flex-wrap:wrap;}
.mini-stat{display:flex; gap:10px; align-items:flex-start; color:var(--text-light); font-size:.85rem;}
.mini-stat strong{font-size:.85rem;}
.mini-icon{font-size:1.1rem;}

.hero-art{position:relative; min-height:380px;}
.hero-illustration{border-radius:18px; overflow:hidden; box-shadow:var(--shadow);}
.float-card{
  position:absolute; background:var(--panel-dark); border:1px solid rgba(255,255,255,.08);
  border-radius:var(--radius-sm); padding:14px 18px; color:var(--text-light);
  box-shadow:0 12px 30px rgba(0,0,0,.35); font-size:.85rem; z-index:2;
}
.float-label{display:block; color:var(--text-muted); font-size:.75rem; margin-bottom:4px;}
.float-value{font-size:1.3rem; display:block;}
.float-delta{font-size:.75rem; color:var(--accent);}
.float-top-left{top:-10px; left:-10px;}
.float-mid-left{top:100px; left:-30px;}
.float-goal{bottom:20px; right:-20px; width:150px;}
.goal-bar{width:100%; height:6px; background:rgba(255,255,255,.1); border-radius:4px; margin:8px 0 6px;}
.goal-fill{height:100%; background:var(--accent); border-radius:4px;}

/* ============================================================
   SECTION HEADINGS (shared)
   ============================================================ */

.section-head{text-align:center; margin-bottom:44px;}
.section-head h2{font-size:2.1rem; position:relative; display:inline-block; padding-bottom:14px;}
.section-head h2::after{content:""; position:absolute; bottom:0; left:50%; transform:translateX(-50%); width:56px; height:3px; background:var(--accent); border-radius:2px;}

/* ============================================================
   FEATURES SECTION
   ============================================================ */

.features{padding:90px 32px; max-width:1240px; margin:0 auto;}
.features-grid{display:grid; grid-template-columns:repeat(5,1fr); gap:22px;}
.feature-card{
  background:var(--card-bg); border:1px solid var(--border); border-radius:var(--radius);
  padding:26px 22px; transition:transform .18s ease, box-shadow .18s ease;
}
.feature-card:hover{transform:translateY(-4px); box-shadow:var(--shadow); border-color:transparent;}
.feature-icon{
  width:46px; height:46px; border-radius:12px; display:flex; align-items:center; justify-content:center;
  font-size:1.3rem; margin-bottom:16px;
}
.icon-green{background:rgba(46,207,156,.15);} .icon-purple{background:rgba(108,99,255,.15);}
.icon-blue{background:rgba(74,123,247,.15);} .icon-orange{background:rgba(245,158,11,.15);}
.icon-teal{background:rgba(18,184,166,.15);} .icon-pink{background:rgba(236,72,153,.15);}
.icon-amber{background:rgba(217,119,6,.15);} .icon-indigo{background:rgba(79,70,229,.15);}
.icon-emerald{background:rgba(5,150,105,.15);} .icon-sky{background:rgba(2,132,199,.15);}
.feature-card h3{font-size:1.02rem; margin-bottom:8px;}
.feature-card p{font-size:.87rem; margin:0;}
.center-cta{text-align:center; margin-top:40px;}

/* ============================================================
   WHY CHOOSE SECTION
   ============================================================ */

.why{background:var(--bg-dark); padding:70px 32px; text-align:center;}
.why h2{color:var(--text-light); font-size:2rem; margin-bottom:44px; position:relative; display:inline-block; padding-bottom:14px;}
.why h2::after{content:""; position:absolute; bottom:0; left:50%; transform:translateX(-50%); width:56px; height:3px; background:var(--accent); border-radius:2px;}
.why-grid{max-width:1240px; margin:0 auto; display:flex; justify-content:space-between; gap:24px; flex-wrap:wrap; text-align:left;}
.why-item{display:flex; gap:12px; align-items:flex-start; flex:1 1 200px; color:var(--text-light);}
.why-icon{width:38px; height:38px; border-radius:10px; background:rgba(46,207,156,.15); color:var(--accent); display:flex; align-items:center; justify-content:center; flex-shrink:0;}
.why-item strong{font-size:.95rem;}
.why-item p{color:var(--text-muted); font-size:.82rem; margin:4px 0 0;}

/* ============================================================
   LANDING PAGE — DASHBOARD PREVIEW MOCK
   ============================================================ */

.dash-preview{padding:90px 32px; background:var(--bg-light);}
.dash-preview-grid{max-width:1240px; margin:0 auto; display:grid; grid-template-columns:1.2fr 1fr; gap:56px; align-items:center;}
.dash-mock{
  display:grid; grid-template-columns:150px 1fr; background:var(--bg-dark); border-radius:var(--radius);
  overflow:hidden; box-shadow:var(--shadow); min-height:360px; cursor:pointer; border:1px solid rgba(255,255,255,.06);
  transition:transform .2s ease;
}
.dash-mock:hover{transform:translateY(-4px);}
.dash-mock-sidebar{background:var(--panel-dark); padding:18px 12px; display:flex; flex-direction:column; gap:4px;}
.dash-mock-logo{color:var(--text-light); font-weight:700; font-size:.8rem; margin-bottom:14px;}
.dash-mock-item{color:var(--text-muted); font-size:.72rem; padding:8px 10px; border-radius:8px;}
.dash-mock-item.active{background:var(--accent); color:#06231c; font-weight:600;}
.dash-mock-main{padding:18px 20px; color:var(--text-light);}
.dash-mock-top{margin-bottom:14px; font-size:.85rem;}
.dash-mock-stats{display:grid; grid-template-columns:repeat(4,1fr); gap:8px; margin-bottom:16px;}
.mini-card{background:var(--panel-dark); border-radius:10px; padding:10px; font-size:.65rem; display:flex; flex-direction:column; gap:4px;}
.mini-card strong{font-size:.95rem;}
.mini-card em{font-style:normal; color:var(--accent); font-size:.65rem;}
.dash-mock-charts{display:grid; grid-template-columns:1.4fr 1fr; gap:12px;}
.chart-box{background:var(--panel-dark); border-radius:10px; padding:10px; font-size:.65rem; display:flex; flex-direction:column; gap:6px;}
.sparkline{width:100%; height:60px;}
.donut-box{align-items:center; text-align:center;}
.donut{
  --p:75; width:64px; height:64px; border-radius:50%;
  background:conic-gradient(var(--accent) calc(var(--p)*1%), rgba(255,255,255,.08) 0);
  display:flex; align-items:center; justify-content:center; position:relative;
}
.donut span{background:var(--panel-dark); width:42px; height:42px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:.6rem; font-weight:700;}

.dash-copy h2{font-size:2rem;}
.check-list{margin:20px 0 28px; display:flex; flex-direction:column; gap:10px;}
.check-list li{color:var(--text-dark); font-weight:500; font-size:.95rem;}

/* ============================================================
   TESTIMONIALS SECTION
   ============================================================ */

.testimonials{background:var(--bg-dark); padding:80px 32px; text-align:center;}
.testimonials h2{color:var(--text-light); font-size:2rem; margin-bottom:44px; position:relative; display:inline-block; padding-bottom:14px;}
.testimonials h2::after{content:""; position:absolute; bottom:0; left:50%; transform:translateX(-50%); width:56px; height:3px; background:var(--accent); border-radius:2px;}
.testimonial-grid{max-width:1240px; margin:0 auto; display:grid; grid-template-columns:repeat(3,1fr); gap:22px; text-align:left;}
.testimonial-card{background:var(--panel-dark); border-radius:var(--radius); padding:26px; border:1px solid rgba(255,255,255,.06);}
.stars{color:#f5b942; margin-bottom:10px; letter-spacing:2px;}
.testimonial-card p{color:var(--text-light); font-size:.9rem;}
.testimonial-user{display:flex; align-items:center; gap:10px; margin-top:16px;}
.avatar{width:38px; height:38px; border-radius:50%; background:var(--accent); color:#06231c; display:flex; align-items:center; justify-content:center; font-weight:700;}
.testimonial-user strong{color:var(--text-light); font-size:.88rem;}

/* ============================================================
   FOOTER
   ============================================================ */

.site-footer{background:var(--bg-darker); padding:70px 32px 24px;}
.footer-grid{max-width:1240px; margin:0 auto; display:grid; grid-template-columns:1fr 1fr; gap:40px; align-items:center; border-bottom:1px solid rgba(255,255,255,.08); padding-bottom:36px;}
.footer-grid h2{color:var(--text-light);}
.contact-email{color:var(--accent); font-weight:600; display:inline-block; margin-bottom:8px;}
.social-row{display:flex; gap:12px; margin-top:16px;}
.social-row a{width:38px; height:38px; border-radius:50%; background:var(--panel-dark); display:flex; align-items:center; justify-content:center; transition:background .15s;}
.social-row a:hover{background:var(--accent);}
.footer-art{font-size:2.4rem; text-align:right; opacity:.85;}
.footer-bottom{max-width:1240px; margin:0 auto; display:flex; justify-content:space-between; padding-top:20px; color:var(--text-muted); font-size:.82rem; flex-wrap:wrap; gap:10px;}

/* ============================================================
   FLASH MESSAGES
   ============================================================ */

.flash-stack{
  position:sticky; top:65px; z-index:40; max-width:1240px; margin:0 auto; padding:12px 32px 0;
  display:flex; flex-direction:column; gap:8px;
}
.flash{
  display:flex; align-items:center; justify-content:space-between; gap:12px;
  padding:12px 18px; border-radius:10px; font-size:.88rem; font-weight:500;
  animation:flashIn .25s ease; transition:opacity .3s ease;
}
@keyframes flashIn{from{opacity:0; transform:translateY(-6px);} to{opacity:1; transform:translateY(0);}}
.flash-success{background:rgba(46,207,156,.14); color:#0f6b4f; border:1px solid rgba(46,207,156,.35);}
.flash-error{background:rgba(239,68,68,.1); color:#b91c1c; border:1px solid rgba(239,68,68,.3);}
.flash-close{background:none; border:none; font-size:1.1rem; cursor:pointer; color:inherit; opacity:.7; line-height:1;}
.flash-close:hover{opacity:1;}

/* ============================================================
   AUTH PAGES (LOGIN / REGISTER)
   ============================================================ */

.auth-page{
  min-height:calc(100vh - 65px); display:flex; align-items:center; justify-content:center; padding:60px 24px;
  background:
    radial-gradient(circle at 15% 20%, rgba(46,207,156,.12), transparent 45%),
    radial-gradient(circle at 85% 80%, rgba(108,99,255,.12), transparent 45%),
    var(--bg-dark);
}
.auth-card{
  width:100%; max-width:420px; background:rgba(18,51,45,.55); backdrop-filter:blur(18px);
  border:1px solid rgba(255,255,255,.1); border-radius:20px; padding:40px 36px;
  box-shadow:0 30px 60px rgba(0,0,0,.35);
}
.auth-card h2{color:var(--text-light); font-size:1.6rem;}
.auth-sub{color:var(--text-muted); font-size:.9rem; margin-bottom:26px;}
.auth-form .input-box{position:relative; margin-bottom:24px;}
.auth-form input{
  width:100%; height:50px; background:rgba(255,255,255,.04); border:none; border-bottom:2px solid rgba(255,255,255,.25);
  outline:none; color:var(--text-light); font-size:.95rem; padding:0 12px 0 36px; border-radius:6px 6px 0 0;
  font-family:'Inter',sans-serif; transition:border-color .2s ease;
}
.auth-form input:focus{border-color:var(--accent);}
.auth-form label{
  position:absolute; left:36px; top:50%; transform:translateY(-50%); color:var(--text-muted);
  font-size:.9rem; transition:.2s ease; pointer-events:none;
}
.auth-form input:focus + label,
.auth-form input:not(:placeholder-shown) + label{
  top:-8px; left:12px; font-size:.72rem; color:var(--accent);
}
.input-icon{position:absolute; left:8px; top:50%; transform:translateY(-50%); color:var(--text-muted); font-size:1rem; z-index:1;}
.auth-switch{text-align:center; margin-top:22px; color:var(--text-muted); font-size:.88rem;}
.auth-switch a{color:var(--accent); font-weight:600;}
.auth-switch a:hover{text-decoration:underline;}

/* ============================================================
   TOAST NOTIFICATION
   ============================================================ */

.toast{
  position:fixed; bottom:24px; left:50%; transform:translateX(-50%) translateY(20px); background:var(--panel-dark); color:var(--text-light);
  padding:14px 22px; border-radius:999px; font-size:.88rem; box-shadow:0 12px 30px rgba(0,0,0,.3);
  opacity:0; pointer-events:none; transition:opacity .25s ease, transform .25s ease; z-index:300; max-width:90vw; text-align:center;
}
.toast.show{opacity:1; transform:translateX(-50%) translateY(0);}

/* ============================================================
   DASHBOARD APP SHELL (sidebar + layout)
   ============================================================ */

.app-body{background:var(--bg-light);}
.app-shell{display:grid; grid-template-columns:230px 1fr; min-height:100vh;}
.app-sidebar{background:var(--bg-dark); padding:22px 16px; display:flex; flex-direction:column; gap:4px; position:sticky; top:0; height:100vh; overflow-y:auto;}
.app-logo{color:var(--text-light); font-weight:700; margin-bottom:18px; display:inline-block;}
.app-nav{display:flex; flex-direction:column; gap:2px; flex:1;}
.app-nav-item{
  background:none; border:none; text-align:left; color:var(--text-muted); font-size:.88rem; font-family:inherit;
  padding:10px 12px; border-radius:9px; cursor:pointer;
}
.app-nav-item:hover{background:rgba(255,255,255,.06); color:var(--text-light);}
.app-nav-item.active{background:var(--accent); color:#06231c; font-weight:600;}
.back-link{margin-top:12px; border-top:1px solid rgba(255,255,255,.08); padding-top:16px;}
.logout-link{color:#f5a3a3;}
.logout-link:hover{background:rgba(239,68,68,.12); color:#fecaca;}
.app-body .flash-stack{position:relative; top:0; padding:14px 20px 0; max-width:none;}
.app-sidebar-toggle{display:none; position:fixed; top:14px; left:14px; z-index:60; background:var(--bg-dark); color:var(--text-light); border:none; border-radius:8px; width:38px; height:38px; font-size:1.1rem; cursor:pointer;}

.app-main{padding:32px 40px 60px;}
.app-topbar{display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px; margin-bottom:26px;}
.range-select{display:flex; gap:6px; background:#fff; border:1px solid var(--border); border-radius:999px; padding:4px;}
.range-btn{border:none; background:none; padding:8px 16px; border-radius:999px; font-size:.82rem; font-weight:600; cursor:pointer; color:var(--text-dark-muted);}
.range-btn.active{background:var(--bg-dark); color:var(--text-light);}

/* ============================================================
   STAT CARDS
   ============================================================ */
.app-stats{display:grid; grid-template-columns:repeat(4,1fr); gap:18px; margin-bottom:22px;}
.stat-card{background:#fff; border:1px solid var(--border); border-radius:var(--radius); padding:20px; display:flex; flex-direction:column; gap:6px;}
.stat-icon{font-size:1.2rem;}
.stat-label{color:var(--text-dark-muted); font-size:.82rem;}
.stat-value{font-size:1.5rem;}
.stat-card em{font-style:normal; color:var(--accent); font-size:.8rem; font-weight:600;}

/* ============================================================
   CHARTS (bar chart + donut)
   ============================================================ */
.app-charts{display:grid; grid-template-columns:1.5fr 1fr; gap:18px; margin-bottom:18px;}
.panel{background:#fff; border:1px solid var(--border); border-radius:var(--radius); padding:22px;}
.panel-head{font-weight:700; margin-bottom:14px;}
.bar-chart{width:100%; height:220px;}
.bar{fill:var(--accent); rx:6;}
.axis-label{fill:var(--text-dark-muted); font-size:11px; text-anchor:middle; font-family:'Inter',sans-serif;}
.donut-panel{display:flex; flex-direction:column; align-items:center; text-align:center;}
.donut-panel .donut{width:130px; height:130px; margin:6px 0 18px;}
.donut-panel .donut span{width:90px; height:90px; font-size:1.2rem; background:#fff;}
.donut-legend{display:flex; flex-direction:column; gap:8px; width:100%;}
.donut-legend li{display:flex; align-items:center; gap:8px; font-size:.85rem; color:var(--text-dark-muted);}
.donut-legend i{width:10px; height:10px; border-radius:50%; display:inline-block;}
.donut-legend b{margin-left:auto; color:var(--text-dark);}

/* ============================================================
   QUICK ACTIONS PANEL
   ============================================================ */
.panel-note{margin-bottom:16px;}
.quick-actions{display:flex; gap:12px; flex-wrap:wrap;}
.quick-actions .btn-outline{color:var(--text-dark); border-color:var(--border);}
.quick-actions .btn-outline:hover{background:var(--bg-light);}

/* ============================================================
   SUBJECTS PANEL
   ============================================================ */

.subject-form{display:flex; gap:10px; flex-wrap:wrap; margin-bottom:18px;}
.subject-form input{
  padding:10px 14px; border:1px solid var(--border); border-radius:var(--radius-sm);
  font-size:.9rem; color:var(--text-dark); font-family:inherit; background:var(--card-bg);
}
.subject-form input[type="text"]{flex:1 1 220px;}
.subject-form input[type="number"]{width:140px;}
.subject-form input:focus{outline:none; border-color:var(--accent);}
.subject-grid{display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:16px;}
.subject-card{
  background:var(--bg-light); border:1px solid var(--border); border-radius:var(--radius-sm);
  padding:16px; display:flex; flex-direction:column; gap:10px;
}
.subject-card-head{display:flex; align-items:center; gap:10px;}
.subject-dot{width:12px; height:12px; border-radius:50%; flex-shrink:0;}
.subject-card-head strong{font-size:.95rem; flex:1;}
.subject-card-head form, .subject-stepper form{display:inline-flex; margin:0;}
.subject-delete{background:none; border:none; color:var(--text-dark-muted); cursor:pointer; font-size:1rem; line-height:1; padding:2px 4px;}
.subject-delete:hover{color:#e0455f;}
.subject-progress-track{width:100%; height:8px; background:var(--border); border-radius:4px; overflow:hidden;}
.subject-progress-fill{height:100%; background:var(--accent); border-radius:4px; transition:width .3s ease;}
.subject-card-footer{display:flex; align-items:center; justify-content:space-between; font-size:.82rem; color:var(--text-dark-muted);}
.subject-stepper{display:flex; align-items:center; gap:8px;}
.subject-stepper button{
  width:24px; height:24px; border-radius:6px; border:1px solid var(--border); background:#fff;
  cursor:pointer; font-size:.9rem; line-height:1; color:var(--text-dark);
}
.subject-stepper button:hover{background:var(--bg-light);}

/* ============================================================
   FLOATING ADD BUTTON (appears on scroll, jumps to add-subject form)
   ============================================================ */
.fab{
  position:fixed; bottom:28px; right:28px; width:56px; height:56px; border-radius:50%;
  background:var(--accent); color:#06231c; border:none; font-size:1.7rem; font-weight:700;
  display:flex; align-items:center; justify-content:center; line-height:1; cursor:pointer;
  box-shadow:0 12px 30px rgba(0,0,0,.25); z-index:200;
  opacity:0; transform:scale(.6) translateY(12px); pointer-events:none;
  transition:opacity .25s ease, transform .25s ease, background .15s ease;
}
.fab.show{opacity:1; transform:scale(1) translateY(0); pointer-events:auto;}
.fab:hover{background:#25b98a; transform:scale(1.08);}
.fab:active{transform:scale(.95);}



/*=============================================================
  STUDY SESSION / TIMER
  ============================================================ */

  
/* ============================================================
   RESPONSIVE / MEDIA QUERIES
   ============================================================ */

@media (max-width: 980px){
  .hero-inner, .dash-preview-grid, .why-grid{grid-template-columns:1fr;}
  .features-grid{grid-template-columns:repeat(2,1fr);}
  .app-shell{grid-template-columns:1fr;}
  .app-sidebar{position:fixed; left:-260px; top:0; width:230px; z-index:55; transition:left .2s ease;}
  .app-sidebar.open{left:0;}
  .app-sidebar-toggle{display:flex; align-items:center; justify-content:center;}
  .app-main{padding-top:70px;}
  .app-stats{grid-template-columns:repeat(2,1fr);}
  .app-charts{grid-template-columns:1fr;}
}
@media (max-width: 720px){
  .main-nav{
    position:absolute; top:100%; left:0; right:0; background:var(--bg-dark); flex-direction:column; gap:0;
    padding:10px 24px 20px; display:none; border-bottom:1px solid rgba(255,255,255,.08);
  }
  .main-nav.open{display:flex;}
  .nav-link{padding:12px 0; border-bottom:1px solid rgba(255,255,255,.06);}
  .nav-link-mobile-only{display:block;}
  .nav-toggle{display:flex;}
  .nav-greeting, .nav-actions .btn-outline, .nav-actions > .btn-primary, .nav-actions .login-link{display:none;}
  .flash-stack{top:0;}
  .hero-title{font-size:2.4rem;}
  .features-grid{grid-template-columns:1fr;}
  .testimonial-grid{grid-template-columns:1fr;}
  .footer-grid{grid-template-columns:1fr;}
  .footer-art{text-align:left;}
  .float-card{position:static; margin-bottom:10px; width:auto !important;}
  .hero-art{display:flex; flex-direction:column;}
}

/* ============================================================
   STUDY SESSIONS PANEL
   ============================================================ */

.mode-toggle{display:flex; gap:10px; margin-bottom:20px;}
.mode-btn{
  padding:10px 18px; border:1px solid var(--border); border-radius:999px; background:#fff;
  font-size:.88rem; font-weight:600; color:var(--text-dark-muted); cursor:pointer; transition:all .15s;
}
.mode-btn.active{background:var(--bg-dark); color:var(--text-light); border-color:var(--bg-dark);}

.session-form{display:flex; flex-direction:column; gap:6px; max-width:420px;}
.field-label{font-size:.82rem; font-weight:600; color:var(--text-dark-muted); margin-top:10px;}
.session-form select, .session-form input[type="text"], .session-form input[type="number"]{
  padding:10px 14px; border:1px solid var(--border); border-radius:var(--radius-sm);
  font-size:.9rem; color:var(--text-dark); font-family:inherit; width:100%; background:var(--card-bg);
}
.session-form select:focus, .session-form input:focus{outline:none; border-color:var(--accent);}
.pomodoro-fields{display:flex; gap:14px;}
.pomodoro-fields > div{flex:1;}
.session-form .btn{margin-top:18px; align-self:flex-start;}

.timer-display{
  font-family:'Sora',sans-serif; font-size:3.4rem; font-weight:800; text-align:center;
  color:var(--text-dark); margin:18px 0; letter-spacing:1px;
}
.timer-controls{display:flex; gap:10px; flex-wrap:wrap; justify-content:center;}

.session-history{display:flex; flex-direction:column; gap:2px;}
.session-row{
  display:grid; grid-template-columns:1.2fr 1.4fr 1fr .9fr 1.3fr; gap:10px; align-items:center;
  padding:10px 0; border-bottom:1px solid var(--border); font-size:.85rem;
}
.session-row:last-child{border-bottom:none;}
.session-subject{font-weight:600;}

@media (max-width: 640px){
  .session-row{grid-template-columns:1fr 1fr; row-gap:2px;}
  .pomodoro-fields{flex-direction:column;}
}

/* ============================================================
   SHARED FORM ELEMENTS (Tests, Assignments, Attendance, Goals,
   Notes, Calendar — anywhere a page has a quick add-row form)
   ============================================================ */

.inline-form{display:flex; gap:10px; flex-wrap:wrap; align-items:center;}
.inline-form input, .inline-form select{
  padding:9px 12px; border:1px solid var(--border); border-radius:var(--radius-sm);
  font-size:.85rem; font-family:inherit; color:var(--text-dark); background:var(--card-bg);
}
.inline-form input:focus, .inline-form select:focus{outline:none; border-color:var(--accent);}

.note-form textarea{
  width:100%; padding:10px 14px; border:1px solid var(--border); border-radius:var(--radius-sm);
  font-size:.88rem; font-family:inherit; color:var(--text-dark); background:var(--card-bg); resize:vertical;
}
.note-form textarea:focus{outline:none; border-color:var(--accent);}

.app-stats-narrow{grid-template-columns:minmax(200px,260px);}

/* ============================================================
   CHAPTERS
   ============================================================ */

.chapter-panel{margin-bottom:16px;}
.chapter-panel-head{display:flex; align-items:center; gap:10px;}
.chapter-count{margin-left:auto; font-size:.8rem;}
.chapter-list{list-style:none; margin:14px 0; padding:0; display:flex; flex-direction:column; gap:2px;}
.chapter-item{display:flex; align-items:center; gap:12px; padding:8px 0; border-bottom:1px solid var(--border); font-size:.88rem;}
.chapter-item:last-child{border-bottom:none;}
.chapter-item.done .chapter-name{color:var(--text-dark-muted); text-decoration:line-through;}
.chapter-name{flex:1;}
.chapter-check{
  width:22px; height:22px; border:2px solid var(--border); border-radius:50%; background:var(--card-bg);
  color:#06231c; font-size:.7rem; font-weight:700; display:flex; align-items:center; justify-content:center;
  cursor:pointer; flex-shrink:0; padding:0;
}
.chapter-check:not(:empty){background:var(--accent); border-color:var(--accent);}
.chapter-delete, .record-delete{
  background:none; border:none; color:var(--text-dark-muted); cursor:pointer; font-size:.9rem;
  padding:4px 6px; border-radius:6px; flex-shrink:0;
}
.chapter-delete:hover, .record-delete:hover{background:rgba(220,38,38,.1); color:#dc2626;}
.chapter-add-form{display:flex; gap:8px; margin-top:6px;}
.chapter-add-form input{
  flex:1; padding:8px 12px; border:1px solid var(--border); border-radius:var(--radius-sm);
  font-size:.85rem; font-family:inherit; color:var(--text-dark); background:var(--card-bg);
}

/* ============================================================
   RECORD LISTS (Tests, Assignments, Attendance, Goals, Calendar)
   ============================================================ */

.record-list{display:flex; flex-direction:column; gap:2px;}
.record-row{display:flex; align-items:center; gap:16px; padding:11px 0; border-bottom:1px solid var(--border); font-size:.85rem;}
.record-row:last-child{border-bottom:none;}
.record-row.record-done .record-primary{color:var(--text-dark-muted); text-decoration:line-through;}
.record-primary{font-weight:600; flex:1 1 160px;}
.record-score{font-weight:600;}
.record-row .record-delete{margin-left:auto;}
.record-row form{display:flex; align-items:center;}

.status-present{color:var(--accent); font-weight:600; font-size:.8rem;}
.status-absent{color:#e0576b; font-weight:600; font-size:.8rem;}
.countdown-soon{color:#e0576b; font-weight:700; font-size:.8rem; white-space:nowrap;}
.countdown-normal{color:var(--text-dark-muted); font-size:.8rem; white-space:nowrap;}

/* ============================================================
   NOTES
   ============================================================ */

.notes-grid{display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:14px; margin-top:14px;}
.note-card{background:var(--bg-light); border:1px solid var(--border); border-radius:var(--radius-sm); padding:16px; display:flex; flex-direction:column; gap:6px;}
.note-card-head{display:flex; align-items:flex-start; justify-content:space-between; gap:8px;}
.note-subject{font-size:.72rem; font-weight:600; color:var(--accent); text-transform:uppercase; letter-spacing:.03em;}
.note-body{font-size:.85rem; color:var(--text-dark-muted); white-space:pre-wrap; margin:0;}
.note-date{font-size:.72rem;}

/* ============================================================
   SETTINGS — profile + appearance
   ============================================================ */

.avatar-picker{display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin:6px 0 4px;}
.avatar-preview{
  width:46px; height:46px; border-radius:50%; background:var(--bg-light); border:1px solid var(--border);
  display:flex; align-items:center; justify-content:center; font-size:1.3rem; flex-shrink:0;
}
.avatar-options{display:flex; gap:6px; flex-wrap:wrap;}
.avatar-option{
  width:34px; height:34px; border-radius:50%; border:1px solid var(--border); background:var(--card-bg);
  font-size:1rem; cursor:pointer; display:flex; align-items:center; justify-content:center;
}
.avatar-option:hover{border-color:var(--accent);}

.theme-toggle{display:flex; gap:10px; flex-wrap:wrap; margin-top:8px;}
.theme-option{
  display:flex; align-items:center; gap:8px; padding:12px 18px; border:1.5px solid var(--border);
  border-radius:var(--radius-sm); cursor:pointer; font-size:.88rem; font-weight:600; color:var(--text-dark-muted);
}
.theme-option input{accent-color:var(--accent);}
.theme-option:has(input:checked){border-color:var(--accent); color:var(--text-dark); background:rgba(46,207,156,.08);}

.settings-form label.field-label:first-child{margin-top:0;}

/* ============================================================
   XP / LEVEL BAR (Dashboard)
   ============================================================ */

.xp-panel{
  display:flex; align-items:center; gap:14px; background:var(--card-bg); border:1px solid var(--border);
  border-radius:var(--radius); padding:14px 20px; margin-bottom:22px;
}
.xp-level{
  background:var(--accent); color:#06231c; font-weight:800; font-size:.8rem;
  padding:6px 14px; border-radius:999px; flex-shrink:0;
}
.xp-bar-track{flex:1; height:10px; border-radius:999px; background:var(--bg-light); overflow:hidden;}
.xp-bar-fill{height:100%; background:linear-gradient(90deg, var(--accent), var(--accent-light)); border-radius:999px; transition:width .4s ease;}
.xp-count{font-size:.78rem; white-space:nowrap; flex-shrink:0;}
/* ============================================================
   LIGHT / DARK / SYSTEM THEME
   Only the app-shell pages (dashboard, subjects, chapters, tests,
   study sessions, assignments, attendance, goals, notes, calendar,
   settings) opt in via <html data-theme="...">. The marketing site,
   login, and register pages keep their fixed look.
   ============================================================ */

html[data-theme="dark"]{
  color-scheme:dark;
  --bg-light:#0e1a17;
  --card-bg:#16241f;
  --text-dark:#eef6f3;
  --text-dark-muted:#9db3ac;
  --border:#26362f;
  --shadow:0 10px 30px rgba(0,0,0,0.45);
}
html[data-theme="dark"] .note-card{background:#101d19;}
html[data-theme="dark"] .donut span{background:var(--card-bg);}
html[data-theme="dark"] .flash-success{color:#7fe8bf; background:rgba(46,207,156,.16); border-color:rgba(46,207,156,.4);}
html[data-theme="dark"] .flash-error{color:#fca5a5; background:rgba(239,68,68,.16); border-color:rgba(239,68,68,.4);}

@media (prefers-color-scheme: dark){
  html[data-theme="system"]{
    color-scheme:dark;
    --bg-light:#0e1a17;
    --card-bg:#16241f;
    --text-dark:#eef6f3;
    --text-dark-muted:#9db3ac;
    --border:#26362f;
    --shadow:0 10px 30px rgba(0,0,0,0.45);
  }
  html[data-theme="system"] .note-card{background:#101d19;}
  html[data-theme="system"] .donut span{background:var(--card-bg);}
  html[data-theme="system"] .flash-success{color:#7fe8bf; background:rgba(46,207,156,.16); border-color:rgba(46,207,156,.4);}
  html[data-theme="system"] .flash-error{color:#fca5a5; background:rgba(239,68,68,.16); border-color:rgba(239,68,68,.4);}
}
"""