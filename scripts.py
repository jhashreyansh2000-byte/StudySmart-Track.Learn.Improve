"""
StudySmart — client-side JavaScript.

MAIN_JS powers the landing/auth pages (served at /static/main.js).
DASHBOARD_JS powers the dashboard app shell (served at /static/dashboard.js).
SIDEBAR_TOGGLE_JS is the small bit both the dashboard and the plain
Subjects page need: opening/closing the sidebar on mobile.
"""

SIDEBAR_TOGGLE_JS = r"""
const sidebar = document.getElementById('appSidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
if (sidebarToggle) {
  sidebarToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
}
"""

MAIN_JS = r"""
const navToggle = document.getElementById('navToggle');
const mainNav = document.getElementById('mainNav');
if (navToggle) {
  navToggle.addEventListener('click', () => {
    const open = mainNav.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', open);
  });
  mainNav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    mainNav.classList.remove('open');
  }));
}

function showToast(msg, duration = 2600) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(showToast._t);
  showToast._t = setTimeout(() => toast.classList.remove('show'), duration);
}

document.querySelectorAll('.flash').forEach(f => {
  setTimeout(() => { f.style.opacity = '0'; setTimeout(() => f.remove(), 300); }, 5000);
});

const dashMockLink = document.getElementById('dashMockLink');
if (dashMockLink) {
  const go = () => { window.location.href = dashMockLink.dataset.href || '/dashboard'; };
  dashMockLink.addEventListener('click', go);
  dashMockLink.addEventListener('keypress', (e) => { if (e.key === 'Enter') go(); });
}
"""

STUDY_SESSIONS_JS = r"""
(function () {
  const sidebar = document.getElementById('appSidebar');
  const sidebarToggle = document.getElementById('sidebarToggle');
  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
  }

  function showToast(msg, duration = 2600) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(showToast._t);
    showToast._t = setTimeout(() => toast.classList.remove('show'), duration);
  }

  const modeButtons = document.querySelectorAll('.mode-btn');
  const pomodoroFields = document.getElementById('pomodoroFields');
  const setupPanel = document.getElementById('sessionSetup');
  const timerPanel = document.getElementById('sessionTimer');
  const subjectSelect = document.getElementById('subjectSelect');
  const chapterInput = document.getElementById('chapterInput');
  const workMinInput = document.getElementById('workMinutes');
  const breakMinInput = document.getElementById('breakMinutes');
  const startBtn = document.getElementById('startSessionBtn');
  const timerDisplay = document.getElementById('timerDisplay');
  const timerPhaseLabel = document.getElementById('timerPhaseLabel');
  const timerMeta = document.getElementById('timerMeta');
  const pauseBtn = document.getElementById('pauseBtn');
  const resumeBtn = document.getElementById('resumeBtn');
  const finishBtn = document.getElementById('finishBtn');
  const cancelBtn = document.getElementById('cancelBtn');

  if (!startBtn) return; // page not present

  // ------------------------------------------------------------------
  // Local ticking state. workSeconds is always "true accumulated study
  // time" -- what eventually gets logged. For pomodoro, phaseRemaining
  // counts the current phase down; for stopwatch it's unused.
  // The server (active_sessions table) is the source of truth for
  // SURVIVING a page leave -- this local state is just what animates
  // the display every second while the page is open.
  // ------------------------------------------------------------------
  let mode = 'stopwatch';
  let phase = 'work';
  let workSeconds = 0;
  let phaseRemaining = 0;
  let intervalId = null;

  function pad(n) { return String(n).padStart(2, '0'); }
  function formatTime(totalSeconds) {
    const t = Math.max(0, Math.round(totalSeconds));
    const h = Math.floor(t / 3600);
    const m = Math.floor((t % 3600) / 60);
    const s = t % 60;
    return h > 0 ? `${pad(h)}:${pad(m)}:${pad(s)}` : `${pad(m)}:${pad(s)}`;
  }

  function updateDisplay() {
    timerDisplay.textContent = mode === 'pomodoro' ? formatTime(phaseRemaining) : formatTime(workSeconds);
    timerPhaseLabel.textContent = mode === 'pomodoro' ? (phase === 'work' ? 'Focus' : 'Break') : 'Stopwatch';
  }

  function tick() {
    if (mode === 'stopwatch') {
      workSeconds += 1;
      updateDisplay();
      return;
    }
    phaseRemaining -= 1;
    if (phase === 'work') workSeconds += 1;
    if (phaseRemaining <= 0) {
      if (phase === 'work') {
        phase = 'break';
        const breakMin = Math.max(parseInt(breakMinInput.value, 10) || 5, 1);
        phaseRemaining = breakMin * 60;
        showToast('Focus session done — take a break!');
      } else {
        phase = 'work';
        const workMin = Math.max(parseInt(workMinInput.value, 10) || 25, 1);
        phaseRemaining = workMin * 60;
        showToast('Break over — back to it!');
      }
    }
    updateDisplay();
  }

  function startLocalTicking() {
    clearInterval(intervalId);
    intervalId = setInterval(tick, 1000);
  }

  function setRunningControls(running) {
    pauseBtn.style.display = running ? 'inline-flex' : 'none';
    resumeBtn.style.display = running ? 'none' : 'inline-flex';
  }

  function showTimerPanel(subjectLabel, chapterLabel) {
    timerMeta.textContent = chapterLabel ? `${subjectLabel} — ${chapterLabel}` : subjectLabel;
    setupPanel.style.display = 'none';
    timerPanel.style.display = 'block';
  }

  function resetToSetup() {
    clearInterval(intervalId);
    setupPanel.style.display = 'block';
    timerPanel.style.display = 'none';
    setRunningControls(true);
  }

  async function postJSON(url, body) {
    try {
      const r = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body || {}),
      });
      return await r.json();
    } catch (e) {
      return { ok: false, error: 'network' };
    }
  }

  // ------------------------------------------------------------------
  // Resume an in-progress session on page load (this is what makes it
  // survive navigating away, refreshing, or closing the tab -- the
  // server already reconciled elapsed/phase for us).
  // ------------------------------------------------------------------
  const active = window.__ACTIVE_SESSION__;
  if (active) {
    mode = active.mode;
    phase = active.phase;
    workSeconds = active.total_work_seconds;
    phaseRemaining = active.remaining_in_phase != null ? active.remaining_in_phase : 0;

    modeButtons.forEach(b => b.classList.toggle('active', b.dataset.mode === mode));
    pomodoroFields.style.display = mode === 'pomodoro' ? 'flex' : 'none';
    if (active.work_minutes) workMinInput.value = active.work_minutes;
    if (active.break_minutes) breakMinInput.value = active.break_minutes;

    showTimerPanel(active.subject_name || 'No subject', active.chapter_name);
    updateDisplay();
    setRunningControls(active.running);
    if (active.running) startLocalTicking();
  }

  modeButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      modeButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      mode = btn.dataset.mode;
      pomodoroFields.style.display = mode === 'pomodoro' ? 'flex' : 'none';
    });
  });

  startBtn.addEventListener('click', async () => {
    if (!subjectSelect.value) {
      showToast('Pick a subject to study first.');
      return;
    }
    const workMin = Math.max(parseInt(workMinInput.value, 10) || 25, 1);
    const breakMin = Math.max(parseInt(breakMinInput.value, 10) || 5, 1);

    startBtn.disabled = true;
    const res = await postJSON('/study-sessions/start', {
      subject_id: subjectSelect.value,
      chapter_name: chapterInput.value.trim(),
      mode: mode,
      work_minutes: workMin,
      break_minutes: breakMin,
    });
    startBtn.disabled = false;

    if (!res.ok) {
      showToast(res.error || 'Could not start the session.');
      return;
    }

    workSeconds = 0;
    phase = 'work';
    phaseRemaining = mode === 'pomodoro' ? workMin * 60 : 0;

    const subjectLabel = subjectSelect.options[subjectSelect.selectedIndex].text;
    showTimerPanel(subjectLabel, chapterInput.value.trim());
    updateDisplay();
    setRunningControls(true);
    startLocalTicking();
  });

  pauseBtn.addEventListener('click', async () => {
    clearInterval(intervalId);
    setRunningControls(false);
    await postJSON('/study-sessions/pause');
  });

  resumeBtn.addEventListener('click', async () => {
    setRunningControls(true);
    startLocalTicking();
    await postJSON('/study-sessions/resume');
  });

  cancelBtn.addEventListener('click', async () => {
    resetToSetup();
    await postJSON('/study-sessions/cancel');
  });

  finishBtn.addEventListener('click', () => {
    clearInterval(intervalId);
    if (workSeconds < 1) {
      showToast('No study time was recorded.');
      resetToSetup();
      return;
    }

    finishBtn.disabled = true;
    fetch('/study-sessions/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        subject_id: subjectSelect.value || (active ? active.subject_id : null),
        chapter_name: chapterInput.value.trim(),
        mode: mode,
        planned_minutes: mode === 'pomodoro' ? (parseInt(workMinInput.value, 10) || null) : null,
        duration_seconds: workSeconds,
      }),
    })
      .then(r => r.json())
      .then(data => {
        finishBtn.disabled = false;
        if (data.ok) {
          showToast('Session saved — nice work! 🎉');
          setTimeout(() => window.location.reload(), 900);
        } else {
          showToast(data.error || 'Could not save that session.');
          resetToSetup();
        }
      })
      .catch(() => {
        finishBtn.disabled = false;
        showToast('Could not save that session — check your connection.');
      });
  });
})();
"""


DASHBOARD_JS = r"""
function showToast(msg, duration = 2400) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(showToast._t);
  showToast._t = setTimeout(() => toast.classList.remove('show'), duration);
}

const sidebar = document.getElementById('appSidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
if (sidebarToggle) {
  sidebarToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
}

const panelTitle = document.getElementById('panelTitle');
const panelSubtitle = document.getElementById('panelSubtitle');
const panelNote = document.getElementById('panelNote');
const navItems = document.querySelectorAll('.app-nav-item[data-item]');

const panelCopy = {
  Dashboard: `Good morning, ${window.__USERNAME__ || 'Student'}! 👋`,
  Chapters: "Track chapter-by-chapter syllabus completion.",
  Tests: "Log scores and watch your average trend upward.",
  Assignments: "Keep every deadline in one tidy list.",
  Attendance: "Automatic attendance percentage, always up to date.",
  "Study Sessions": "Every focused session, timed and logged.",
  Goals: "Set targets and keep your streak alive.",
  Notes: "Your notes, searchable and synced.",
  Calendar: "See exams, assignments, and sessions in one view.",
  Settings: "Personalize your StudySmart experience.",
};

navItems.forEach(btn => {
  btn.addEventListener('click', () => {
    navItems.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const item = btn.dataset.item;
    panelTitle.textContent = item;
    panelSubtitle.textContent = panelCopy[item] || '';
    if (item === 'Dashboard') {
      panelNote.textContent = 'Select an item from the sidebar to preview it — this demo focuses on the dashboard overview.';
    } else {
      panelNote.textContent = `This is a demo preview of the ${item} panel — plug in your own data model to make it fully functional.`;
      showToast(`Switched to ${item}`);
    }
  });
});

const rangeBtns = document.querySelectorAll('.range-btn');
const statHours = document.getElementById('statHours');
const statTests = document.getElementById('statTests');
const statScore = document.getElementById('statScore');
const statStreak = document.getElementById('statStreak');

const rangeData = {
  week: {
    hours: window.__STAT_HOURS__ || '0h 0m',
    tests: window.__STAT_SESSIONS__ ?? '0',
    score: '82%',
    streak: window.__STAT_STREAK__ || '0 Days',
    bars: window.__WEEK_HOURS__ || [0,0,0,0,0,0,0],
  },
  // Monthly rollups aren't tracked yet — this stays demo data until a
  // month-over-month query is added.
  month: { hours: '72h 10m', tests: '21', score: '85%', streak: '12 Days', bars: [14, 16, 15, 18, 17, 20, 19] },
};

rangeBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    rangeBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const range = btn.dataset.range;
    const d = rangeData[range];
    statHours.textContent = d.hours;
    statTests.textContent = d.tests;
    statScore.textContent = d.score;
    statStreak.textContent = d.streak;
    drawBarChart(d.bars);
    showToast(range === 'week' ? 'Showing this week' : 'Showing this month');
  });
});

function drawBarChart(values) {
  const svg = document.getElementById('barChart');
  if (!svg) return;
  svg.querySelectorAll('.bar').forEach(b => b.remove());
  const max = Math.max(...values, 1);
  const chartHeight = 170;
  const baseline = 200;
  values.forEach((v, i) => {
    const barHeight = (v / max) * chartHeight;
    const x = 12 + i * 68;
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('class', 'bar');
    rect.setAttribute('x', x);
    rect.setAttribute('width', 34);
    rect.setAttribute('rx', 6);
    rect.setAttribute('y', baseline);
    rect.setAttribute('height', 0);
    svg.appendChild(rect);
    requestAnimationFrame(() => {
      rect.style.transition = 'y .5s ease, height .5s ease';
      rect.setAttribute('y', baseline - barHeight);
      rect.setAttribute('height', barHeight);
    });
  });
}
drawBarChart(window.__WEEK_HOURS__ || [2.5,4,3,5.5,4.5,6.5,5]);

document.querySelectorAll('[data-toast]').forEach(btn => {
  btn.addEventListener('click', () => showToast(btn.dataset.toast));
});
"""