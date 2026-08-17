"""
StudySmart -- Jinja templates (rendered with render_template_string) and the
render() helper that injects flash messages into every page.

Each page below is one plain triple-quoted string -- no template pieces are
glued together with string concatenation. Some markup (fonts/CSS link tags,
the top nav bar, the app sidebar) repeats across pages; that repetition is
intentional so each template can be read top to bottom on its own.
"""

from flask import render_template_string, g
from content import SIDEBAR_ITEMS, SIDEBAR_ENDPOINTS

FLASHES_HTML = """
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
  <div class="flash-stack">
    {% for category, message in messages %}
    <div class="flash flash-{{ category }}">
      <span>{{ message }}</span>
      <button class="flash-close" onclick="this.parentElement.remove()" aria-label="Dismiss">&times;</button>
    </div>
    {% endfor %}
  </div>
  {% endif %}
{% endwith %}
"""


INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>StudySmart — Track. Learn. Improve.</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static_css') }}">

</head>
<body>

<header class="site-header" id="top">
  <div class="nav-inner">
    <a href="{{ url_for('home') }}" class="logo">
      <span class="logo-mark">
        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 3L2 8l10 5 10-5-10-5z" fill="currentColor"/>
          <path d="M6 12v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5" stroke="currentColor" stroke-width="1.6" fill="none"/>
        </svg>
      </span>
      StudySmart
    </a>

    <nav class="main-nav" id="mainNav">
      <a href="{{ url_for('home') }}#features" class="nav-link">Features</a>
      <a href="{{ url_for('home') }}#about" class="nav-link">About</a>
      <a href="{{ url_for('home') }}#contact" class="nav-link">Contact</a>
      {% if session.username %}
      <a href="{{ url_for('dashboard') }}" class="nav-link nav-link-mobile-only">Dashboard</a>
      <a href="{{ url_for('logout') }}" class="nav-link nav-link-mobile-only">Logout</a>
      {% else %}
      <a href="{{ url_for('login') }}" class="nav-link nav-link-mobile-only">Login</a>
      <a href="{{ url_for('register') }}" class="nav-link nav-link-mobile-only">Get Started</a>
      {% endif %}
    </nav>

    <div class="nav-actions">
      {% if session.username %}
        <span class="nav-greeting">Hi, {{ session.username }}</span>
        <a href="{{ url_for('dashboard') }}" class="btn btn-outline btn-sm">Dashboard</a>
        <a href="{{ url_for('logout') }}" class="btn btn-primary btn-sm">Logout</a>
      {% else %}
        <a href="{{ url_for('login') }}" class="nav-link login-link">Login</a>
        <a href="{{ url_for('register') }}" class="btn btn-primary btn-sm">Get Started</a>
      {% endif %}
      <button class="nav-toggle" id="navToggle" aria-label="Toggle menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>
{{ flashes|safe }}


<section class="hero">
  <div class="hero-inner">
    <div class="hero-copy">
      <span class="badge-pill">✶ Your Academic Command Center</span>
      <h1 class="hero-title">Track. Learn.<br><span class="accent">Improve.</span></h1>
      <p class="hero-sub">All-in-one platform to manage your studies, track progress, and achieve more every day.</p>
      <div class="hero-cta">
        <a href="{{ url_for('dashboard') if session.username else url_for('register') }}" class="btn btn-primary">{{ 'Go to Dashboard' if session.username else 'Start Now' }}
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </a>
        <a href="#features" class="btn btn-outline">Explore Features</a>
      </div>
      <div class="hero-mini-stats">
        <div class="mini-stat"><span class="mini-icon">👤</span><div><strong>All Your Data</strong><br>In One Place</div></div>
        <div class="mini-stat"><span class="mini-icon">📈</span><div><strong>Track Progress</strong><br>Every Day</div></div>
        <div class="mini-stat"><span class="mini-icon">🎯</span><div><strong>Achieve Goals</strong><br>Consistently</div></div>
      </div>
    </div>

    <div class="hero-art">
      <div class="float-card float-top-left">
        <span class="float-label">Today's Study</span>
        <strong class="float-value">3h 25m</strong>
        <span class="float-delta up">↗ +12% from yesterday</span>
      </div>
      <div class="float-card float-mid-left">
        <span class="float-label">Study Streak</span>
        <strong class="float-value">12 <small>days</small> 🔥</strong>
      </div>
      <div class="hero-illustration" aria-hidden="true">
        <svg viewBox="0 0 420 380" width="100%" height="100%">
          <rect x="0" y="0" width="420" height="380" rx="18" fill="#12332d"/>
          <circle cx="330" cy="60" r="26" fill="#e9edf1" opacity="0.9"/>
          <rect x="30" y="230" width="150" height="8" rx="4" fill="#2ecf9c" opacity="0.5"/>
          <rect x="30" y="250" width="110" height="8" rx="4" fill="#2ecf9c" opacity="0.3"/>
          <circle cx="210" cy="190" r="70" fill="#1a4a41"/>
          <rect x="150" y="230" width="120" height="90" rx="6" fill="#0e2b26"/>
          <rect x="160" y="245" width="100" height="55" rx="4" fill="#1f5a4f"/>
          <circle cx="210" cy="165" r="42" fill="#f4b183"/>
          <path d="M172 150c0-24 18-42 38-42s38 18 38 42" fill="#2b2320"/>
          <rect x="185" y="200" width="50" height="60" rx="10" fill="#2ecf9c"/>
        </svg>
      </div>
      <div class="float-card float-goal">
        <span class="float-label">✔ Goal Progress</span>
        <div class="goal-bar"><div class="goal-fill" style="width:75%"></div></div>
        <strong>75%</strong>
      </div>
    </div>
  </div>
</section>

<section class="features" id="features">
  <div class="section-head">
    <h2>Powerful Features for Smarter Students</h2>
  </div>
  <div class="features-grid">
    {% for f in features %}
    <div class="feature-card">
      <div class="feature-icon icon-{{ f.color }}">{{ f.emoji }}</div>
      <h3>{{ f.title }}</h3>
      <p>{{ f.desc }}</p>
    </div>
    {% endfor %}
  </div>
  <div class="center-cta">
    <a href="{{ url_for('dashboard') }}" class="btn btn-primary">Explore All Features
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </a>
  </div>
</section>

<section class="why" id="about">
  <h2>Why Choose StudySmart?</h2>
  <div class="why-grid">
    {% for w in why %}
    <div class="why-item">
      <div class="why-icon">●</div>
      <div>
        <strong>{{ w.title }}</strong>
        <p>{{ w.desc }}</p>
      </div>
    </div>
    {% endfor %}
  </div>
</section>

<section class="dash-preview">
  <div class="dash-preview-grid">
    <div class="dash-mock" id="dashMockLink" role="link" tabindex="0" data-href="{{ url_for('dashboard') }}">
      <div class="dash-mock-sidebar">
        <div class="dash-mock-logo">📗 StudySmart</div>
        <div class="dash-mock-item active">🏠 Dashboard</div>
        <div class="dash-mock-item">📘 Subjects</div>
        <div class="dash-mock-item">📖 Chapters</div>
        <div class="dash-mock-item">📝 Tests</div>
        <div class="dash-mock-item">📋 Assignments</div>
      </div>
      <div class="dash-mock-main">
        <div class="dash-mock-top">
          <div><strong>Dashboard</strong><br><span class="muted">Good morning, {{ session.username or 'Student' }}! 👋</span></div>
        </div>
        <div class="dash-mock-stats">
          <div class="mini-card"><span>⏱ Study Hours</span><strong>18h 45m</strong><em class="up">+15%</em></div>
          <div class="mini-card"><span>📊 Tests Taken</span><strong>6</strong><em class="up">+2</em></div>
          <div class="mini-card"><span>⭐ Avg. Score</span><strong>82%</strong><em class="up">+8%</em></div>
          <div class="mini-card"><span>🔥 Study Streak</span><strong>12 Days</strong><em class="up">+3</em></div>
        </div>
        <div class="dash-mock-charts">
          <div class="chart-box">
            <span>Study Hours</span>
            <svg viewBox="0 0 240 90" class="sparkline"><polyline points="0,70 35,55 70,60 105,30 140,40 175,15 210,25" fill="none" stroke="#2ecf9c" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </div>
          <div class="chart-box donut-box">
            <span>Subject Progress</span>
            <div class="donut" style="--p:75"><span>75%</span></div>
          </div>
        </div>
      </div>
    </div>

    <div class="dash-copy">
      <h2>Everything You Need,<br>All in One Dashboard</h2>
      <p>Get a complete overview of your academic life. Track progress, analyze performance, and make smarter decisions every day.</p>
      <ul class="check-list">
        <li>✔ Real-time progress tracking</li>
        <li>✔ Performance analytics</li>
        <li>✔ Smart insights &amp; recommendations</li>
        <li>✔ Beautiful, easy-to-use interface</li>
      </ul>
      <a href="{{ url_for('dashboard') }}" class="btn btn-primary">See Dashboard In Action
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </a>
    </div>
  </div>
</section>

<section class="testimonials">
  <h2>What Our Users Say</h2>
  <div class="testimonial-grid">
    {% for t in testimonials %}
    <div class="testimonial-card">
      <div class="stars">{{ '★' * t.stars }}{{ '☆' * (5 - t.stars) }}</div>
      <p>"{{ t.quote }}"</p>
      <div class="testimonial-user">
        <div class="avatar">{{ t.name[0] }}</div>
        <div><strong>{{ t.name }}</strong><br><span class="muted">{{ t.role }}</span></div>
      </div>
    </div>
    {% endfor %}
  </div>
</section>

<footer class="site-footer" id="contact">
  <div class="footer-grid">
    <div>
      <h2>Contact Us</h2>
      <a class="contact-email" href="mailto:shreyanshjha2012@gmail.com">✉ shreyanshjha2012@gmail.com</a>
      <p class="muted">We'd love to hear from you!</p>
      <div class="social-row">
        <a href="https://instagram.com" target="_blank" rel="noopener" aria-label="Instagram">📷</a>
        <a href="https://github.com" target="_blank" rel="noopener" aria-label="GitHub">💻</a>
        <a href="https://twitter.com" target="_blank" rel="noopener" aria-label="Twitter">🐦</a>
        <a href="https://youtube.com" target="_blank" rel="noopener" aria-label="YouTube">▶</a>
      </div>
    </div>
    <div class="footer-art" aria-hidden="true">🧑‍💻📚👩‍🎓</div>
  </div>
  <div class="footer-bottom">
    <span>© 2026 StudySmart. All rights reserved.</span>
    <span>Track. Learn. Improve. 💚</span>
  </div>
</footer>

<div class="toast" id="toast"></div>

<script src="{{ url_for('static_main_js') }}"></script>
</body>
</html>
"""


LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Log In — StudySmart</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static_css') }}">

</head>
<body>

<header class="site-header" id="top">
  <div class="nav-inner">
    <a href="{{ url_for('home') }}" class="logo">
      <span class="logo-mark">
        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 3L2 8l10 5 10-5-10-5z" fill="currentColor"/>
          <path d="M6 12v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5" stroke="currentColor" stroke-width="1.6" fill="none"/>
        </svg>
      </span>
      StudySmart
    </a>

    <nav class="main-nav" id="mainNav">
      <a href="{{ url_for('home') }}#features" class="nav-link">Features</a>
      <a href="{{ url_for('home') }}#about" class="nav-link">About</a>
      <a href="{{ url_for('home') }}#contact" class="nav-link">Contact</a>
      {% if session.username %}
      <a href="{{ url_for('dashboard') }}" class="nav-link nav-link-mobile-only">Dashboard</a>
      <a href="{{ url_for('logout') }}" class="nav-link nav-link-mobile-only">Logout</a>
      {% else %}
      <a href="{{ url_for('login') }}" class="nav-link nav-link-mobile-only">Login</a>
      <a href="{{ url_for('register') }}" class="nav-link nav-link-mobile-only">Get Started</a>
      {% endif %}
    </nav>

    <div class="nav-actions">
      {% if session.username %}
        <span class="nav-greeting">Hi, {{ session.username }}</span>
        <a href="{{ url_for('dashboard') }}" class="btn btn-outline btn-sm">Dashboard</a>
        <a href="{{ url_for('logout') }}" class="btn btn-primary btn-sm">Logout</a>
      {% else %}
        <a href="{{ url_for('login') }}" class="nav-link login-link">Login</a>
        <a href="{{ url_for('register') }}" class="btn btn-primary btn-sm">Get Started</a>
      {% endif %}
      <button class="nav-toggle" id="navToggle" aria-label="Toggle menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>
{{ flashes|safe }}


<section class="auth-page">
  <div class="auth-card">
    <span class="badge-pill">✶ Welcome back</span>
    <h2>Log in to StudySmart</h2>
    <p class="auth-sub">Pick up right where you left off.</p>

    <form method="POST" class="auth-form">
      <div class="input-box">
        <span class="input-icon">👤</span>
        <input type="text" name="login" placeholder=" " required autofocus>
        <label>Username or email</label>
      </div>

      <div class="input-box">
        <span class="input-icon">🔒</span>
        <input type="password" name="password" placeholder=" " required>
        <label>Password</label>
      </div>

      <button type="submit" class="btn btn-primary btn-block">Log In
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
    </form>

    <p class="auth-switch">Don't have an account? <a href="{{ url_for('register') }}">Register</a></p>
  </div>
</section>

<script src="{{ url_for('static_main_js') }}"></script>
</body>
</html>
"""


REGISTER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Create Account — StudySmart</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static_css') }}">

</head>
<body>

<header class="site-header" id="top">
  <div class="nav-inner">
    <a href="{{ url_for('home') }}" class="logo">
      <span class="logo-mark">
        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 3L2 8l10 5 10-5-10-5z" fill="currentColor"/>
          <path d="M6 12v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5" stroke="currentColor" stroke-width="1.6" fill="none"/>
        </svg>
      </span>
      StudySmart
    </a>

    <nav class="main-nav" id="mainNav">
      <a href="{{ url_for('home') }}#features" class="nav-link">Features</a>
      <a href="{{ url_for('home') }}#about" class="nav-link">About</a>
      <a href="{{ url_for('home') }}#contact" class="nav-link">Contact</a>
      {% if session.username %}
      <a href="{{ url_for('dashboard') }}" class="nav-link nav-link-mobile-only">Dashboard</a>
      <a href="{{ url_for('logout') }}" class="nav-link nav-link-mobile-only">Logout</a>
      {% else %}
      <a href="{{ url_for('login') }}" class="nav-link nav-link-mobile-only">Login</a>
      <a href="{{ url_for('register') }}" class="nav-link nav-link-mobile-only">Get Started</a>
      {% endif %}
    </nav>

    <div class="nav-actions">
      {% if session.username %}
        <span class="nav-greeting">Hi, {{ session.username }}</span>
        <a href="{{ url_for('dashboard') }}" class="btn btn-outline btn-sm">Dashboard</a>
        <a href="{{ url_for('logout') }}" class="btn btn-primary btn-sm">Logout</a>
      {% else %}
        <a href="{{ url_for('login') }}" class="nav-link login-link">Login</a>
        <a href="{{ url_for('register') }}" class="btn btn-primary btn-sm">Get Started</a>
      {% endif %}
      <button class="nav-toggle" id="navToggle" aria-label="Toggle menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>
{{ flashes|safe }}


<section class="auth-page">
  <div class="auth-card">
    <span class="badge-pill">✶ Free to join</span>
    <h2>Create your account</h2>
    <p class="auth-sub">Set up your academic command center in seconds.</p>

    <form method="POST" class="auth-form">
      <div class="input-box">
        <span class="input-icon">👤</span>
        <input type="text" name="username" placeholder=" " required autofocus minlength="3">
        <label>Username</label>
      </div>

      <div class="input-box">
        <span class="input-icon">✉</span>
        <input type="email" name="email" placeholder=" ">
        <label>Email (optional)</label>
      </div>

      <div class="input-box">
        <span class="input-icon">🔒</span>
        <input type="password" name="password" placeholder=" " required minlength="6">
        <label>Password (min. 6 characters)</label>
      </div>

      <button type="submit" class="btn btn-primary btn-block">Create Account
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
    </form>

    <p class="auth-switch">Already have an account? <a href="{{ url_for('login') }}">Log in</a></p>
  </div>
</section>

<script src="{{ url_for('static_main_js') }}"></script>
</body>
</html>
"""


DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en" data-theme="{{ theme }}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Dashboard — StudySmart</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static_css') }}">

</head>
<body class="app-body">

{{ flashes|safe }}

<div class="app-shell">
  <aside class="app-sidebar" id="appSidebar">
    <a href="{{ url_for('home') }}" class="dash-mock-logo app-logo">📗 StudySmart</a>
    <nav class="app-nav">
      {% for item in sidebar_items %}
      <a href="{{ url_for(nav_endpoints[item]) }}" class="app-nav-item {{ 'active' if active_item == item else '' }}">{{ item }}</a>
      {% endfor %}
    </nav>
    <a href="{{ url_for('home') }}" class="app-nav-item back-link">← Back to site</a>
    <a href="{{ url_for('logout') }}" class="app-nav-item logout-link">⎋ Logout</a>
  </aside>

  <button class="app-sidebar-toggle" id="sidebarToggle" aria-label="Toggle sidebar">☰</button>


  <main class="app-main">
    <div class="app-topbar">
      <div>
        <h1 id="panelTitle">Dashboard</h1>
        <p class="muted" id="panelSubtitle">Good morning, {{ username }}! 👋</p>
      </div>
      <div class="range-select">
        <button class="range-btn active" data-range="week">This Week</button>
        <button class="range-btn" data-range="month">This Month</button>
      </div>
    </div>

    <section class="xp-panel">
      <span class="xp-level">Lvl {{ xp_info.level }}</span>
      <div class="xp-bar-track">
        <div class="xp-bar-fill" style="width:{{ xp_info.into_level }}%"></div>
      </div>
      <span class="xp-count muted">{{ xp_info.into_level }} / {{ xp_info.for_level }} XP · {{ xp_info.xp }} total</span>
    </section>

    <section class="app-stats">
      <div class="stat-card">
        <span class="stat-icon">⏱</span>
        <span class="stat-label">Study Hours</span>
        <strong class="stat-value" id="statHours">{{ stat_hours }}</strong>
        <em class="up">this week</em>
      </div>
      <div class="stat-card">
        <span class="stat-icon">📊</span>
        <span class="stat-label">Sessions Logged</span>
        <strong class="stat-value" id="statTests">{{ stat_sessions }}</strong>
        <em class="up">total</em>
      </div>
      <div class="stat-card">
        <span class="stat-icon">⭐</span>
        <span class="stat-label">Avg. Score</span>
        <strong class="stat-value" id="statScore">82%</strong>
        <em class="up">demo</em>
      </div>
      <div class="stat-card">
        <span class="stat-icon">🔥</span>
        <span class="stat-label">Study Streak</span>
        <strong class="stat-value" id="statStreak">{{ stat_streak }}</strong>
        <em class="up">keep it going</em>
      </div>
    </section>

    <section class="app-charts">
      <div class="panel">
        <div class="panel-head">
          <span>Study Hours</span>
        </div>
        <svg viewBox="0 0 500 220" class="bar-chart" id="barChart">
          {% for label in week_labels %}
          <text x="{{ 20 + loop.index0 * 68 }}" y="212" class="axis-label">{{ label }}</text>
          {% endfor %}
        </svg>
      </div>
      <div class="panel donut-panel">
        <div class="panel-head"><span>Subject Progress</span></div>
        {% if progress.total_subjects == 0 %}
        <div class="donut" style="--p:0" id="donutChart"><span>0%</span></div>
        <p class="muted panel-note" style="margin-top:10px;">
          No subjects yet — <a href="{{ url_for('subjects') }}">add one</a> to see real progress here.
        </p>
        {% else %}
        <div class="donut" style="--p:{{ progress.overall_pct }}" id="donutChart"><span>{{ progress.overall_pct }}%</span></div>
        <ul class="donut-legend">
          <li><i style="background:#2ecf9c"></i> Completed <b>{{ progress.completed }}</b></li>
          <li><i style="background:#6c63ff"></i> In Progress <b>{{ progress.in_progress }}</b></li>
          <li><i style="background:#f5768e"></i> Not Started <b>{{ progress.not_started }}</b></li>
        </ul>
        {% endif %}
      </div>
    </section>

    <section class="panel" id="panelBody">
      <div class="panel-head"><span>Quick actions</span></div>
      <p class="muted panel-note" id="panelNote">Select an item from the sidebar to preview it — this demo focuses on the dashboard overview.</p>
      <div class="quick-actions">
        <a href="{{ url_for('study_sessions') }}" class="btn btn-outline btn-sm">+ Log study session</a>
        <button class="btn btn-outline btn-sm" data-toast="Add a test score to update your average automatically.">+ Add test score</button>
        <button class="btn btn-outline btn-sm" data-toast="Create a new goal and track it on your streak calendar.">+ New goal</button>
      </div>
    </section>
  </main>
</div>

<div class="toast" id="toast"></div>
<script>
  window.__WEEK_LABELS__ = {{ week_labels|tojson }};
  window.__WEEK_HOURS__ = {{ week_hours|tojson }};
  window.__STAT_HOURS__ = {{ stat_hours|tojson }};
  window.__STAT_SESSIONS__ = {{ stat_sessions|tojson }};
  window.__STAT_STREAK__ = {{ stat_streak|tojson }};
  window.__USERNAME__ = {{ username|tojson }};
</script>
<script src="{{ url_for('static_dashboard_js') }}"></script>
</body>
</html>
"""


SUBJECTS_HTML = """
<!DOCTYPE html>
<html lang="en" data-theme="{{ theme }}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Subjects — StudySmart</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static_css') }}">

</head>
<body class="app-body">

{{ flashes|safe }}

<div class="app-shell">
  <aside class="app-sidebar" id="appSidebar">
    <a href="{{ url_for('home') }}" class="dash-mock-logo app-logo">📗 StudySmart</a>
    <nav class="app-nav">
      {% for item in sidebar_items %}
      <a href="{{ url_for(nav_endpoints[item]) }}" class="app-nav-item {{ 'active' if active_item == item else '' }}">{{ item }}</a>
      {% endfor %}
    </nav>
    <a href="{{ url_for('home') }}" class="app-nav-item back-link">← Back to site</a>
    <a href="{{ url_for('logout') }}" class="app-nav-item logout-link">⎋ Logout</a>
  </aside>

  <button class="app-sidebar-toggle" id="sidebarToggle" aria-label="Toggle sidebar">☰</button>


  <main class="app-main">
    <div class="app-topbar">
      <div>
        <h1>Subjects</h1>
        <p class="muted">Add a subject, then track chapters as you complete them.</p>
      </div>
    </div>

    {% if progress.total_subjects > 0 %}
    <section class="panel donut-panel" style="margin-bottom:20px;">
      <div class="panel-head"><span>Subject Progress</span></div>
      <div class="donut" style="--p:{{ progress.overall_pct }}"><span>{{ progress.overall_pct }}%</span></div>
      <ul class="donut-legend">
        <li><i style="background:#2ecf9c"></i> Completed <b>{{ progress.completed }}</b></li>
        <li><i style="background:#6c63ff"></i> In Progress <b>{{ progress.in_progress }}</b></li>
        <li><i style="background:#f5768e"></i> Not Started <b>{{ progress.not_started }}</b></li>
      </ul>
    </section>
    {% endif %}

    <section class="panel">
      <div class="panel-head"><span>Your subjects</span></div>

      {% if not subjects %}
      <p class="muted panel-note">No subjects yet — add your first one below.</p>
      {% endif %}

      <div class="subject-grid">
        {% for s in subjects %}
        <div class="subject-card">
          <div class="subject-card-head">
            <span class="subject-dot icon-{{ s['color'] }}"></span>
            <form method="POST"
      action="{{ url_for('subject_edit', subject_id=s['id']) }}"
      class="subject-edit-form">

    <input type="text"
           name="name"
           value="{{ s['name'] }}"
           maxlength="60"
           required>

    <button type="submit">💾</button>

</form>
            <form method="POST" action="{{ url_for('subject_delete', subject_id=s['id']) }}">
              <button type="submit" class="subject-delete" title="Delete subject">✕</button>
            </form>
          </div>

          {% set pct = (s['chapters_done'] * 100 // s['chapters_total']) if s['chapters_total'] else 0 %}
          <div class="subject-progress-track">
            <div class="subject-progress-fill" style="width:{{ pct }}%"></div>
          </div>

          <div class="subject-card-footer">
            <span>{{ s['chapters_done'] }} / {{ s['chapters_total'] }} chapters ({{ pct }}%)</span>
            <span class="subject-stepper">
              <form method="POST" action="{{ url_for('subject_decrement', subject_id=s['id']) }}">
                <button type="submit">−</button>
              </form>
              <form method="POST" action="{{ url_for('subject_increment', subject_id=s['id']) }}">
                <button type="submit">+</button>
              </form>
            </span>
          </div>
        </div>
        {% endfor %}
      </div>
    </section>

    <section class="panel" id="addSubjectSection">
      <div class="panel-head"><span>Add a subject</span></div>
      <form method="POST" action="{{ url_for('subjects') }}" class="subject-form">
        <input type="text" name="name" placeholder="Subject name (e.g. Physics)" maxlength="60" required />
        <input type="number" name="chapters_total" placeholder="Total chapters" min="1" max="200" required />
        <button type="submit" class="btn btn-primary btn-sm">+ Add subject</button>
      </form>
    </section>
  </main>
</div>

<button class="fab" id="addSubjectFab" title="Add a subject" aria-label="Add a subject">+</button>

<div class="toast" id="toast"></div>
<script>
const sidebar = document.getElementById('appSidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
if (sidebarToggle) {
  sidebarToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
}

const fab = document.getElementById('addSubjectFab');
const addSubjectSection = document.getElementById('addSubjectSection');

window.addEventListener('scroll', () => {
  if (window.scrollY > 150) {
    fab.classList.add('show');
  } else {
    fab.classList.remove('show');
  }
});

fab.addEventListener('click', () => {
  addSubjectSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
});

</script>
</body>
</html>
"""


STUDY_SESSIONS_HTML = """
<!DOCTYPE html>
<html lang="en" data-theme="{{ theme }}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Study Sessions — StudySmart</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static_css') }}">

</head>
<body class="app-body">

{{ flashes|safe }}

<div class="app-shell">
  <aside class="app-sidebar" id="appSidebar">
    <a href="{{ url_for('home') }}" class="dash-mock-logo app-logo">⏰ StudySmart</a>
    <nav class="app-nav">
      {% for item in sidebar_items %}
      <a href="{{ url_for(nav_endpoints[item]) }}" class="app-nav-item {{ 'active' if active_item == item else '' }}">{{ item }}</a>
      {% endfor %}
    </nav>
    <a href="{{ url_for('home') }}" class="app-nav-item back-link">← Back to site</a>
    <a href="{{ url_for('logout') }}" class="app-nav-item logout-link">⎋ Logout</a>
  </aside>

  <button class="app-sidebar-toggle" id="sidebarToggle" aria-label="Toggle sidebar">☰</button>

  <main class="app-main">
    <div class="app-topbar">
      <div>
        <h1>Study Sessions</h1>
        <p class="muted">Every focused session, timed and logged.</p>
      </div>
    </div>

    <section class="app-stats">
      <div class="stat-card">
        <span class="stat-icon">⏱</span>
        <span class="stat-label">Total Time Studied</span>
        <strong class="stat-value">{{ session_stats.total_time }}</strong>
        <em class="up">all time</em>
      </div>
      <div class="stat-card">
        <span class="stat-icon">📈</span>
        <span class="stat-label">Sessions Logged</span>
        <strong class="stat-value">{{ session_stats.total_sessions }}</strong>
        <em class="up">all time</em>
      </div>
      <div class="stat-card">
        <span class="stat-icon">🔥</span>
        <span class="stat-label">Studied Today</span>
        <strong class="stat-value">{{ session_stats.today_time }}</strong>
        <em class="up">so far</em>
      </div>
      <div class="stat-card">
        <span class="stat-icon">🔁</span>
        <span class="stat-label">Study Streak</span>
        <strong class="stat-value">{{ session_stats.streak }} Day{{ 's' if session_stats.streak != 1 else '' }}</strong>
        <em class="up">keep it going</em>
      </div>
    </section>

    {% if not subjects %}
    <section class="panel">
      <p class="muted panel-note">You don't have any subjects yet. <a href="{{ url_for('subjects') }}">Add a subject</a> first, then come back here to start a session.</p>
    </section>
    {% endif %}

    <section class="panel" id="sessionSetup" {% if not subjects %}style="display:none"{% endif %}>
      <div class="panel-head"><span>Start a session</span></div>

      <div class="mode-toggle">
        <button type="button" class="mode-btn active" data-mode="stopwatch">⏱ Stopwatch</button>
        <button type="button" class="mode-btn" data-mode="pomodoro">🍅 Pomodoro</button>
      </div>

      <div class="session-form">
        <label class="field-label" for="subjectSelect">Subject</label>
        <select id="subjectSelect">
          <option value="">Choose a subject…</option>
          {% for s in subjects %}
          <option value="{{ s['id'] }}">{{ s['name'] }}</option>
          {% endfor %}
        </select>

        <label class="field-label" for="chapterInput">Chapter <span class="muted">(optional)</span></label>
        <input type="text" id="chapterInput" placeholder="e.g. Chapter 4 — Thermodynamics" maxlength="80">

        <div id="pomodoroFields" class="pomodoro-fields" style="display:none">
          <div>
            <label class="field-label" for="workMinutes">Focus (minutes)</label>
            <input type="number" id="workMinutes" min="1" max="180" value="25">
          </div>
          <div>
            <label class="field-label" for="breakMinutes">Break (minutes)</label>
            <input type="number" id="breakMinutes" min="1" max="60" value="5">
          </div>
        </div>

        <button type="button" class="btn btn-primary" id="startSessionBtn">▶ Start session</button>
      </div>
    </section>

    <section class="panel" id="sessionTimer" style="display:none">
      <div class="panel-head"><span id="timerPhaseLabel">Stopwatch</span></div>
      <p class="muted panel-note" id="timerMeta"></p>
      <div class="timer-display" id="timerDisplay">00:00</div>
      <div class="timer-controls">
        <button type="button" class="btn btn-outline btn-sm" id="pauseBtn">⏸ Pause</button>
        <button type="button" class="btn btn-outline btn-sm" id="resumeBtn" style="display:none">▶ Resume</button>
        <button type="button" class="btn btn-primary btn-sm" id="finishBtn">✔ Finish & save</button>
        <button type="button" class="btn btn-outline btn-sm" id="cancelBtn">✕ Cancel</button>
      </div>
    </section>

    <section class="panel">
      <div class="panel-head"><span>Recent sessions</span></div>
      {% if not recent_sessions %}
      <p class="muted panel-note">No sessions logged yet — finish a timer above and it'll show up here.</p>
      {% else %}
      <div class="session-history">
        {% for r in recent_sessions %}
        <div class="session-row">
          <span class="session-subject">{{ r['subject_name'] or 'No subject' }}</span>
          <span class="session-chapter muted">{{ r['chapter_name'] or '—' }}</span>
          <span class="session-mode">{{ '🍅 Pomodoro' if r['mode'] == 'pomodoro' else '⏱ Stopwatch' }}</span>
          <span class="session-duration">{{ (r['duration_seconds'] // 60) }}m {{ (r['duration_seconds'] % 60) }}s</span>
          <span class="session-date muted">{{ r['started_at'][:16].replace('T', ' ') }}</span>
        </div>
        {% endfor %}
      </div>
      {% endif %}
    </section>
  </main>
</div>

<div class="toast" id="toast"></div>
<script>
  window.__ACTIVE_SESSION__ = {{ active_session_json|safe }};
</script>
<script src="{{ url_for('static_study_sessions_js') }}"></script>
</body>
</html>
"""

CHAPTERS_HTML = """
<!DOCTYPE html>
<html lang="en" data-theme="{{ theme }}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Chapters — StudySmart</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static_css') }}">
</head>
<body class="app-body">

{{ flashes|safe }}

<div class="app-shell">
  <aside class="app-sidebar" id="appSidebar">
    <a href="{{ url_for('home') }}" class="dash-mock-logo app-logo">📚 StudySmart</a>
    <nav class="app-nav">
      {% for item in sidebar_items %}
      <a href="{{ url_for(nav_endpoints[item]) }}" class="app-nav-item {{ 'active' if active_item == item else '' }}">{{ item }}</a>
      {% endfor %}
    </nav>
    <a href="{{ url_for('home') }}" class="app-nav-item back-link">← Back to site</a>
    <a href="{{ url_for('logout') }}" class="app-nav-item logout-link">⎋ Logout</a>
  </aside>

  <button class="app-sidebar-toggle" id="sidebarToggle" aria-label="Toggle sidebar">☰</button>

  <main class="app-main">
    <div class="app-topbar">
      <div>
        <h1>Chapters</h1>
        <p class="muted">Name and check off individual chapters for each subject.</p>
      </div>
    </div>

    {% if not subjects %}
    <section class="panel">
      <p class="muted panel-note">You don't have any subjects yet. <a href="{{ url_for('subjects') }}">Add a subject</a> first, then come back here to break it into chapters.</p>
    </section>
    {% else %}
      {% for s in subjects %}
      {% set group = chapters_by_subject[s['id']] %}
      <section class="panel chapter-panel">
        <div class="panel-head chapter-panel-head">
          <span class="subject-dot icon-{{ s['color'] }}"></span>
          <span>{{ s['name'] }}</span>
          <span class="muted chapter-count">{{ group['done'] }} / {{ group['total'] }} done</span>
        </div>

        {% if group['chs'] %}
        <ul class="chapter-list">
          {% for ch in group['chs'] %}
          <li class="chapter-item {{ 'done' if ch['done'] else '' }}">
            <form method="POST" action="{{ url_for('chapter_toggle', chapter_id=ch['id']) }}" class="chapter-toggle-form">
              <button type="submit" class="chapter-check" aria-label="Toggle chapter done">{{ '✓' if ch['done'] else '' }}</button>
            </form>
            <span class="chapter-name">{{ ch['name'] }}</span>
            <form method="POST" action="{{ url_for('chapter_delete', chapter_id=ch['id']) }}">
              <button type="submit" class="chapter-delete" title="Delete chapter">✕</button>
            </form>
          </li>
          {% endfor %}
        </ul>
        {% else %}
        <p class="muted panel-note">No chapters named yet for {{ s['name'] }}.</p>
        {% endif %}

        <form method="POST" action="{{ url_for('chapter_add') }}" class="chapter-add-form">
          <input type="hidden" name="subject_id" value="{{ s['id'] }}">
          <input type="text" name="name" placeholder="e.g. Chapter 5 — Optics" maxlength="80" required>
          <button type="submit" class="btn btn-outline btn-sm">+ Add chapter</button>
        </form>
      </section>
      {% endfor %}
    {% endif %}
  </main>
</div>

<div class="toast" id="toast"></div>
<script>
const sidebar = document.getElementById('appSidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
if (sidebarToggle) sidebarToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
</script>
</body>
</html>
"""


TESTS_HTML = """
<!DOCTYPE html>
<html lang="en" data-theme="{{ theme }}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Tests — StudySmart</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static_css') }}">
</head>
<body class="app-body">

{{ flashes|safe }}

<div class="app-shell">
  <aside class="app-sidebar" id="appSidebar">
    <a href="{{ url_for('home') }}" class="dash-mock-logo app-logo">📊 StudySmart</a>
    <nav class="app-nav">
      {% for item in sidebar_items %}
      <a href="{{ url_for(nav_endpoints[item]) }}" class="app-nav-item {{ 'active' if active_item == item else '' }}">{{ item }}</a>
      {% endfor %}
    </nav>
    <a href="{{ url_for('home') }}" class="app-nav-item back-link">← Back to site</a>
    <a href="{{ url_for('logout') }}" class="app-nav-item logout-link">⎋ Logout</a>
  </aside>

  <button class="app-sidebar-toggle" id="sidebarToggle" aria-label="Toggle sidebar">☰</button>

  <main class="app-main">
    <div class="app-topbar">
      <div>
        <h1>Tests</h1>
        <p class="muted">Log test scores and watch your average.</p>
      </div>
    </div>

    <section class="app-stats">
      <div class="stat-card">
        <span class="stat-icon">⭐</span>
        <span class="stat-label">Average Score</span>
        <strong class="stat-value">{{ avg_score }}</strong>
        <em class="up">across {{ tests|length }} test{{ 's' if tests|length != 1 else '' }}</em>
      </div>
    </section>

    <section class="panel">
      <div class="panel-head"><span>Log a test</span></div>
      {% if not subjects %}
      <p class="muted panel-note">You don't have any subjects yet. <a href="{{ url_for('subjects') }}">Add a subject</a> first.</p>
      {% else %}
      <form method="POST" action="{{ url_for('test_add') }}" class="inline-form">
        <select name="subject_id" required>
          <option value="">Subject…</option>
          {% for s in subjects %}
          <option value="{{ s['id'] }}">{{ s['name'] }}</option>
          {% endfor %}
        </select>
        <input type="text" name="name" placeholder="Test name, e.g. Unit Test 2" maxlength="80" required>
        <input type="number" name="score" placeholder="Score" min="0" step="0.5" required style="width:90px">
        <input type="number" name="max_score" placeholder="Out of" min="1" step="0.5" value="100" style="width:90px">
        <input type="date" name="test_date" value="{{ today }}">
        <button type="submit" class="btn btn-primary btn-sm">+ Add</button>
      </form>
      {% endif %}
    </section>

    <section class="panel">
      <div class="panel-head"><span>Test history</span></div>
      {% if not tests %}
      <p class="muted panel-note">No tests logged yet.</p>
      {% else %}
      <div class="record-list">
        {% for t in tests %}
        <div class="record-row">
          <span class="record-primary">{{ t['name'] }}</span>
          <span class="muted">{{ t['subject_name'] or '—' }}</span>
          <span class="record-score">{{ t['score']|round(1) }}/{{ t['max_score']|round(1) }} ({{ ((t['score'] / t['max_score']) * 100)|round|int }}%)</span>
          <span class="muted">{{ t['test_date'] }}</span>
          <form method="POST" action="{{ url_for('test_delete', test_id=t['id']) }}">
            <button type="submit" class="record-delete" title="Delete">✕</button>
          </form>
        </div>
        {% endfor %}
      </div>
      {% endif %}
    </section>
  </main>
</div>

<div class="toast" id="toast"></div>
<script>
const sidebar = document.getElementById('appSidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
if (sidebarToggle) sidebarToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
</script>
</body>
</html>
"""


ASSIGNMENTS_HTML = """
<!DOCTYPE html>
<html lang="en" data-theme="{{ theme }}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Assignments — StudySmart</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static_css') }}">
</head>
<body class="app-body">

{{ flashes|safe }}

<div class="app-shell">
  <aside class="app-sidebar" id="appSidebar">
    <a href="{{ url_for('home') }}" class="dash-mock-logo app-logo">📋 StudySmart</a>
    <nav class="app-nav">
      {% for item in sidebar_items %}
      <a href="{{ url_for(nav_endpoints[item]) }}" class="app-nav-item {{ 'active' if active_item == item else '' }}">{{ item }}</a>
      {% endfor %}
    </nav>
    <a href="{{ url_for('home') }}" class="app-nav-item back-link">← Back to site</a>
    <a href="{{ url_for('logout') }}" class="app-nav-item logout-link">⎋ Logout</a>
  </aside>

  <button class="app-sidebar-toggle" id="sidebarToggle" aria-label="Toggle sidebar">☰</button>

  <main class="app-main">
    <div class="app-topbar">
      <div>
        <h1>Assignments</h1>
        <p class="muted">Never miss a deadline.</p>
      </div>
    </div>

    <section class="app-stats app-stats-narrow">
      <div class="stat-card">
        <span class="stat-icon">📋</span>
        <span class="stat-label">Pending</span>
        <strong class="stat-value">{{ pending_count }}</strong>
        <em class="up">of {{ assignments|length }} total</em>
      </div>
    </section>

    <section class="panel">
      <div class="panel-head"><span>Add an assignment</span></div>
      <form method="POST" action="{{ url_for('assignment_add') }}" class="inline-form">
        <input type="text" name="title" placeholder="Assignment title" maxlength="100" required style="flex:1 1 220px">
        <select name="subject_id">
          <option value="">Subject (optional)…</option>
          {% for s in subjects %}
          <option value="{{ s['id'] }}">{{ s['name'] }}</option>
          {% endfor %}
        </select>
        <input type="date" name="due_date" value="{{ today }}">
        <button type="submit" class="btn btn-primary btn-sm">+ Add</button>
      </form>
    </section>

    <section class="panel">
      <div class="panel-head"><span>All assignments</span></div>
      {% if not assignments %}
      <p class="muted panel-note">No assignments yet — add one above.</p>
      {% else %}
      <div class="record-list">
        {% for a in assignments %}
        <div class="record-row {{ 'record-done' if a['done'] else '' }}">
          <form method="POST" action="{{ url_for('assignment_toggle', assignment_id=a['id']) }}">
            <button type="submit" class="chapter-check" aria-label="Toggle done">{{ '✓' if a['done'] else '' }}</button>
          </form>
          <span class="record-primary">{{ a['title'] }}</span>
          <span class="muted">{{ a['subject_name'] or '—' }}</span>
          <span class="muted">{{ 'Due ' + a['due_date'] if a['due_date'] else 'No due date' }}</span>
          <form method="POST" action="{{ url_for('assignment_delete', assignment_id=a['id']) }}">
            <button type="submit" class="record-delete" title="Delete">✕</button>
          </form>
        </div>
        {% endfor %}
      </div>
      {% endif %}
    </section>
  </main>
</div>

<div class="toast" id="toast"></div>
<script>
const sidebar = document.getElementById('appSidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
if (sidebarToggle) sidebarToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
</script>
</body>
</html>
"""


ATTENDANCE_HTML = """
<!DOCTYPE html>
<html lang="en" data-theme="{{ theme }}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Attendance — StudySmart</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static_css') }}">
</head>
<body class="app-body">

{{ flashes|safe }}

<div class="app-shell">
  <aside class="app-sidebar" id="appSidebar">
    <a href="{{ url_for('home') }}" class="dash-mock-logo app-logo">📅 StudySmart</a>
    <nav class="app-nav">
      {% for item in sidebar_items %}
      <a href="{{ url_for(nav_endpoints[item]) }}" class="app-nav-item {{ 'active' if active_item == item else '' }}">{{ item }}</a>
      {% endfor %}
    </nav>
    <a href="{{ url_for('home') }}" class="app-nav-item back-link">← Back to site</a>
    <a href="{{ url_for('logout') }}" class="app-nav-item logout-link">⎋ Logout</a>
  </aside>

  <button class="app-sidebar-toggle" id="sidebarToggle" aria-label="Toggle sidebar">☰</button>

  <main class="app-main">
    <div class="app-topbar">
      <div>
        <h1>Attendance</h1>
        <p class="muted">Track attendance and keep your percentage up to date.</p>
      </div>
    </div>

    <section class="app-stats app-stats-narrow">
      <div class="stat-card">
        <span class="stat-icon">📅</span>
        <span class="stat-label">Attendance</span>
        <strong class="stat-value">{{ pct }}</strong>
        <em class="up">{{ present_count }} / {{ total_count }} present</em>
      </div>
    </section>

    <section class="panel">
      <div class="panel-head"><span>Log attendance</span></div>
      <form method="POST" action="{{ url_for('attendance_add') }}" class="inline-form">
        <select name="subject_id">
          <option value="">Subject (optional)…</option>
          {% for s in subjects %}
          <option value="{{ s['id'] }}">{{ s['name'] }}</option>
          {% endfor %}
        </select>
        <input type="date" name="att_date" value="{{ today }}">
        <select name="status">
          <option value="present">Present</option>
          <option value="absent">Absent</option>
        </select>
        <button type="submit" class="btn btn-primary btn-sm">+ Log</button>
      </form>
    </section>

    <section class="panel">
      <div class="panel-head"><span>History</span></div>
      {% if not records %}
      <p class="muted panel-note">No attendance logged yet.</p>
      {% else %}
      <div class="record-list">
        {% for r in records %}
        <div class="record-row">
          <span class="record-primary">{{ r['att_date'] }}</span>
          <span class="muted">{{ r['subject_name'] or 'All subjects' }}</span>
          <span class="{{ 'status-present' if r['status'] == 'present' else 'status-absent' }}">
            {{ '✓ Present' if r['status'] == 'present' else '✕ Absent' }}
          </span>
          <form method="POST" action="{{ url_for('attendance_delete', record_id=r['id']) }}">
            <button type="submit" class="record-delete" title="Delete">✕</button>
          </form>
        </div>
        {% endfor %}
      </div>
      {% endif %}
    </section>
  </main>
</div>

<div class="toast" id="toast"></div>
<script>
const sidebar = document.getElementById('appSidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
if (sidebarToggle) sidebarToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
</script>
</body>
</html>
"""


GOALS_HTML = """
<!DOCTYPE html>
<html lang="en" data-theme="{{ theme }}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Goals — StudySmart</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static_css') }}">
</head>
<body class="app-body">

{{ flashes|safe }}

<div class="app-shell">
  <aside class="app-sidebar" id="appSidebar">
    <a href="{{ url_for('home') }}" class="dash-mock-logo app-logo">🎯 StudySmart</a>
    <nav class="app-nav">
      {% for item in sidebar_items %}
      <a href="{{ url_for(nav_endpoints[item]) }}" class="app-nav-item {{ 'active' if active_item == item else '' }}">{{ item }}</a>
      {% endfor %}
    </nav>
    <a href="{{ url_for('home') }}" class="app-nav-item back-link">← Back to site</a>
    <a href="{{ url_for('logout') }}" class="app-nav-item logout-link">⎋ Logout</a>
  </aside>

  <button class="app-sidebar-toggle" id="sidebarToggle" aria-label="Toggle sidebar">☰</button>

  <main class="app-main">
    <div class="app-topbar">
      <div>
        <h1>Goals</h1>
        <p class="muted">Set goals and check them off as you go.</p>
      </div>
    </div>

    <section class="app-stats app-stats-narrow">
      <div class="stat-card">
        <span class="stat-icon">🎯</span>
        <span class="stat-label">Completed</span>
        <strong class="stat-value">{{ done_count }} / {{ goals|length }}</strong>
        <em class="up">goals</em>
      </div>
    </section>

    <section class="panel">
      <div class="panel-head"><span>Add a goal</span></div>
      <form method="POST" action="{{ url_for('goal_add') }}" class="inline-form">
        <input type="text" name="title" placeholder="e.g. Finish Physics ch. 4-6 this week" maxlength="120" required style="flex:1 1 260px">
        <input type="date" name="target_date" value="{{ today }}">
        <button type="submit" class="btn btn-primary btn-sm">+ Add</button>
      </form>
    </section>

    <section class="panel">
      <div class="panel-head"><span>Your goals</span></div>
      {% if not goals %}
      <p class="muted panel-note">No goals yet — add one above.</p>
      {% else %}
      <div class="record-list">
        {% for gl in goals %}
        <div class="record-row {{ 'record-done' if gl['done'] else '' }}">
          <form method="POST" action="{{ url_for('goal_toggle', goal_id=gl['id']) }}">
            <button type="submit" class="chapter-check" aria-label="Toggle done">{{ '✓' if gl['done'] else '' }}</button>
          </form>
          <span class="record-primary">{{ gl['title'] }}</span>
          <span class="muted">{{ 'by ' + gl['target_date'] if gl['target_date'] else 'no deadline' }}</span>
          <form method="POST" action="{{ url_for('goal_delete', goal_id=gl['id']) }}">
            <button type="submit" class="record-delete" title="Delete">✕</button>
          </form>
        </div>
        {% endfor %}
      </div>
      {% endif %}
    </section>
  </main>
</div>

<div class="toast" id="toast"></div>
<script>
const sidebar = document.getElementById('appSidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
if (sidebarToggle) sidebarToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
</script>
</body>
</html>
"""


NOTES_HTML = """
<!DOCTYPE html>
<html lang="en" data-theme="{{ theme }}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Notes — StudySmart</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static_css') }}">
</head>
<body class="app-body">

{{ flashes|safe }}

<div class="app-shell">
  <aside class="app-sidebar" id="appSidebar">
    <a href="{{ url_for('home') }}" class="dash-mock-logo app-logo">📔 StudySmart</a>
    <nav class="app-nav">
      {% for item in sidebar_items %}
      <a href="{{ url_for(nav_endpoints[item]) }}" class="app-nav-item {{ 'active' if active_item == item else '' }}">{{ item }}</a>
      {% endfor %}
    </nav>
    <a href="{{ url_for('home') }}" class="app-nav-item back-link">← Back to site</a>
    <a href="{{ url_for('logout') }}" class="app-nav-item logout-link">⎋ Logout</a>
  </aside>

  <button class="app-sidebar-toggle" id="sidebarToggle" aria-label="Toggle sidebar">☰</button>

  <main class="app-main">
    <div class="app-topbar">
      <div>
        <h1>Notes</h1>
        <p class="muted">Create and organize notes by subject.</p>
      </div>
    </div>

    <section class="panel">
      <div class="panel-head"><span>New note</span></div>
      <form method="POST" action="{{ url_for('note_add') }}" class="note-form">
        <div class="inline-form" style="margin-bottom:10px">
          <input type="text" name="title" placeholder="Note title" maxlength="100" required style="flex:1 1 220px">
          <select name="subject_id">
            <option value="">Subject (optional)…</option>
            {% for s in subjects %}
            <option value="{{ s['id'] }}">{{ s['name'] }}</option>
            {% endfor %}
          </select>
        </div>
        <textarea name="body" placeholder="Write your note…" rows="3"></textarea>
        <button type="submit" class="btn btn-primary btn-sm" style="margin-top:10px">+ Save note</button>
      </form>
    </section>

    <section class="panel">
      <div class="panel-head"><span>Your notes</span></div>
      {% if not notes %}
      <p class="muted panel-note">No notes yet — write your first one above.</p>
      {% else %}
      <div class="notes-grid">
        {% for n in notes %}
        <div class="note-card">
          <div class="note-card-head">
            <strong>{{ n['title'] }}</strong>
            <form method="POST" action="{{ url_for('note_delete', note_id=n['id']) }}">
              <button type="submit" class="record-delete" title="Delete">✕</button>
            </form>
          </div>
          {% if n['subject_name'] %}<span class="note-subject">{{ n['subject_name'] }}</span>{% endif %}
          {% if n['body'] %}<p class="note-body">{{ n['body'] }}</p>{% endif %}
          <span class="note-date muted">{{ n['created_at'][:10] }}</span>
        </div>
        {% endfor %}
      </div>
      {% endif %}
    </section>
  </main>
</div>

<div class="toast" id="toast"></div>
<script>
const sidebar = document.getElementById('appSidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
if (sidebarToggle) sidebarToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
</script>
</body>
</html>
"""


CALENDAR_HTML = """
<!DOCTYPE html>
<html lang="en" data-theme="{{ theme }}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Calendar — StudySmart</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static_css') }}">
</head>
<body class="app-body">

{{ flashes|safe }}

<div class="app-shell">
  <aside class="app-sidebar" id="appSidebar">
    <a href="{{ url_for('home') }}" class="dash-mock-logo app-logo">🗓 StudySmart</a>
    <nav class="app-nav">
      {% for item in sidebar_items %}
      <a href="{{ url_for(nav_endpoints[item]) }}" class="app-nav-item {{ 'active' if active_item == item else '' }}">{{ item }}</a>
      {% endfor %}
    </nav>
    <a href="{{ url_for('home') }}" class="app-nav-item back-link">← Back to site</a>
    <a href="{{ url_for('logout') }}" class="app-nav-item logout-link">⎋ Logout</a>
  </aside>

  <button class="app-sidebar-toggle" id="sidebarToggle" aria-label="Toggle sidebar">☰</button>

  <main class="app-main">
    <div class="app-topbar">
      <div>
        <h1>Calendar</h1>
        <p class="muted">Exam dates with live countdowns.</p>
      </div>
    </div>

    <section class="panel">
      <div class="panel-head"><span>Add an exam</span></div>
      <form method="POST" action="{{ url_for('exam_add') }}" class="inline-form">
        <input type="text" name="title" placeholder="e.g. Chemistry Midterm" maxlength="100" required style="flex:1 1 220px">
        <select name="subject_id">
          <option value="">Subject (optional)…</option>
          {% for s in subjects %}
          <option value="{{ s['id'] }}">{{ s['name'] }}</option>
          {% endfor %}
        </select>
        <input type="date" name="exam_date" value="{{ today }}" required>
        <button type="submit" class="btn btn-primary btn-sm">+ Add</button>
      </form>
    </section>

    <section class="panel">
      <div class="panel-head"><span>Upcoming</span></div>
      {% if not exams %}
      <p class="muted panel-note">Nothing on the calendar yet — add an exam above.</p>
      {% else %}
      <div class="record-list">
        {% for e in exams %}
        <div class="record-row">
          <span class="record-primary">{{ e['title'] }}</span>
          <span class="muted">{{ e['subject_name'] or '—' }}</span>
          <span class="muted">{{ e['exam_date'] }}</span>
          <span class="{{ 'countdown-soon' if e['days_left'] is not none and e['days_left'] <= 3 and e['days_left'] >= 0 else 'countdown-normal' }}">
            {% if e['days_left'] is none %}—
            {% elif e['days_left'] > 0 %}{{ e['days_left'] }} day{{ 's' if e['days_left'] != 1 else '' }} left
            {% elif e['days_left'] == 0 %}Today
            {% else %}Passed
            {% endif %}
          </span>
          <form method="POST" action="{{ url_for('exam_delete', exam_id=e['id']) }}">
            <button type="submit" class="record-delete" title="Delete">✕</button>
          </form>
        </div>
        {% endfor %}
      </div>
      {% endif %}
    </section>
  </main>
</div>

<div class="toast" id="toast"></div>
<script>
const sidebar = document.getElementById('appSidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
if (sidebarToggle) sidebarToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
</script>
</body>
</html>
"""


SETTINGS_HTML = """
<!DOCTYPE html>
<html lang="en" data-theme="{{ theme }}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Settings — StudySmart</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static_css') }}">
</head>
<body class="app-body">

{{ flashes|safe }}

<div class="app-shell">
  <aside class="app-sidebar" id="appSidebar">
    <a href="{{ url_for('home') }}" class="dash-mock-logo app-logo">⚙️ StudySmart</a>
    <nav class="app-nav">
      {% for item in sidebar_items %}
      <a href="{{ url_for(nav_endpoints[item]) }}" class="app-nav-item {{ 'active' if active_item == item else '' }}">{{ item }}</a>
      {% endfor %}
    </nav>
    <a href="{{ url_for('home') }}" class="app-nav-item back-link">← Back to site</a>
    <a href="{{ url_for('logout') }}" class="app-nav-item logout-link">⎋ Logout</a>
  </aside>

  <button class="app-sidebar-toggle" id="sidebarToggle" aria-label="Toggle sidebar">☰</button>

  <main class="app-main">
    <div class="app-topbar">
      <div>
        <h1>Settings</h1>
        <p class="muted">Your profile and app preferences.</p>
      </div>
    </div>

    <form method="POST" action="{{ url_for('settings') }}">
      <section class="panel" style="margin-bottom:20px; max-width:520px;">
        <div class="panel-head"><span>Profile</span></div>

        <label class="field-label" for="avatarInput">Avatar</label>
        <div class="avatar-picker">
          <span class="avatar-preview" id="avatarPreview">{{ user['avatar'] or '🎓' }}</span>
          <input type="text" id="avatarInput" name="avatar" value="{{ user['avatar'] or '🎓' }}" maxlength="4" style="width:70px; text-align:center;">
          <div class="avatar-options">
            {% for emo in ['🎓','📚','🧠','✏️','🚀','🌟','🦉','⚡'] %}
            <button type="button" class="avatar-option" data-emoji="{{ emo }}">{{ emo }}</button>
            {% endfor %}
          </div>
        </div>

        <label class="field-label" for="fullName">Full name</label>
        <input type="text" id="fullName" name="full_name" value="{{ user['full_name'] or '' }}" maxlength="80" placeholder="Your name">

        <label class="field-label" for="className">Class / Grade</label>
        <input type="text" id="className" name="class_name" value="{{ user['class_name'] or '' }}" maxlength="40" placeholder="e.g. Class 12, B.Sc Year 2">

        <label class="field-label">Username</label>
        <input type="text" value="{{ user['username'] }}" disabled>

        <label class="field-label">Email</label>
        <input type="text" value="{{ user['email'] or 'Not set' }}" disabled>
      </section>

      <section class="panel" style="margin-bottom:20px; max-width:520px;">
        <div class="panel-head"><span>Appearance</span></div>
        <p class="muted panel-note">Choose how StudySmart looks. "System" matches your device's setting automatically.</p>
        <div class="theme-toggle">
          <label class="theme-option">
            <input type="radio" name="theme" value="light" {{ 'checked' if user['theme'] == 'light' or not user['theme'] else '' }}>
            <span>☀️ Light</span>
          </label>
          <label class="theme-option">
            <input type="radio" name="theme" value="dark" {{ 'checked' if user['theme'] == 'dark' else '' }}>
            <span>🌙 Dark</span>
          </label>
          <label class="theme-option">
            <input type="radio" name="theme" value="system" {{ 'checked' if user['theme'] == 'system' else '' }}>
            <span>🖥 System</span>
          </label>
        </div>
      </section>

      <button type="submit" class="btn btn-primary">Save settings</button>
    </form>
  </main>
</div>

<div class="toast" id="toast"></div>
<script>
const sidebar = document.getElementById('appSidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
if (sidebarToggle) sidebarToggle.addEventListener('click', () => sidebar.classList.toggle('open'));

const avatarInput = document.getElementById('avatarInput');
const avatarPreview = document.getElementById('avatarPreview');
document.querySelectorAll('.avatar-option').forEach(btn => {
  btn.addEventListener('click', () => {
    avatarInput.value = btn.dataset.emoji;
    avatarPreview.textContent = btn.dataset.emoji;
  });
});
avatarInput.addEventListener('input', () => {
  avatarPreview.textContent = avatarInput.value || '🎓';
});

// Live-preview the theme pick immediately, before the form is even saved.
document.querySelectorAll('input[name="theme"]').forEach(radio => {
  radio.addEventListener('change', () => {
    document.documentElement.setAttribute('data-theme', radio.value);
  });
});
</script>
</body>
</html>
"""


def render(template_str, **ctx):
    flashes = render_template_string(FLASHES_HTML)
    ctx.setdefault("sidebar_items", SIDEBAR_ITEMS)
    ctx.setdefault("nav_endpoints", SIDEBAR_ENDPOINTS)
    ctx.setdefault("theme", getattr(g, "theme", "system"))
    return render_template_string(template_str, flashes=flashes, **ctx)