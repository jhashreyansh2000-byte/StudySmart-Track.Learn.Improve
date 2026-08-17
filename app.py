"""
StudySmart — Flask app entry point.

Run:
    pip install flask
    python3 app.py
Then open http://127.0.0.1:5000

The app used to live in one 1200-line file. It's now split by concern:
    database.py   -> SQLite connection + table setup
    content.py    -> static copy/demo data for the landing page & dashboard
    styles.py     -> shared CSS (STYLE_CSS)
    scripts.py    -> client-side JS (MAIN_JS, DASHBOARD_JS)
    templates.py  -> Jinja page templates + the render() helper
    app.py (here) -> Flask app, static asset routes, auth, and page routes
No logic was changed — this file just imports the pieces and wires up routes,
exactly as they were before.
"""

import sqlite3
import json
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, request, redirect, url_for, session, flash, Response, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash

from database import init_db, get_db
from content import FEATURES, WHY_CHOOSE, TESTIMONIALS, SIDEBAR_ITEMS
from styles import STYLE_CSS
from scripts import MAIN_JS, DASHBOARD_JS, STUDY_SESSIONS_JS
from templates import (
    render, INDEX_HTML, LOGIN_HTML, REGISTER_HTML, DASHBOARD_HTML, SUBJECTS_HTML,
    STUDY_SESSIONS_HTML, CHAPTERS_HTML, TESTS_HTML,
    ASSIGNMENTS_HTML, ATTENDANCE_HTML, GOALS_HTML, NOTES_HTML, CALENDAR_HTML, SETTINGS_HTML,
)

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-me"  # replace with a real secret in production

init_db()

# Colors are rotated onto new subjects and match the `.icon-*` classes
# already defined in styles.py, so no new CSS colors are needed.
SUBJECT_COLORS = [
    "purple", "blue", "orange", "teal", "pink",
    "amber", "indigo", "emerald", "sky", "green",
]


# ============================================================
#  STATIC ASSET ROUTES (served from the same file)
# ============================================================

@app.route("/static/style.css")
def static_css():
    return Response(STYLE_CSS, mimetype="text/css")


@app.route("/static/main.js")
def static_main_js():
    return Response(MAIN_JS, mimetype="application/javascript")


@app.route("/static/dashboard.js")
def static_dashboard_js():
    return Response(DASHBOARD_JS, mimetype="application/javascript")


@app.route("/static/study-sessions.js")
def static_study_sessions_js():
    return Response(STUDY_SESSIONS_JS, mimetype="application/javascript")


# ============================================================
#  AUTH HELPER
# ============================================================

def get_week_study_data(username):
    """Trailing 7 days (oldest -> today) of study seconds, from real logged sessions."""
    conn = get_db()
    today = datetime.utcnow().date()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]

    labels, hours = [], []
    for d in days:
        row = conn.execute(
            "SELECT COALESCE(SUM(duration_seconds), 0) AS secs FROM study_sessions "
            "WHERE username = ? AND date(started_at) = ?",
            (username, d.isoformat()),
        ).fetchone()
        labels.append(d.strftime("%a"))
        hours.append(round(row["secs"] / 3600, 2))

    total_sessions = conn.execute(
        "SELECT COUNT(*) AS c FROM study_sessions WHERE username = ?",
        (username,),
    ).fetchone()["c"]
    conn.close()
    return labels, hours, total_sessions


def compute_streak(username):
    """Consecutive days (ending today) with at least one logged session."""
    conn = get_db()
    day = datetime.utcnow().date()
    streak = 0
    while True:
        row = conn.execute(
            "SELECT COALESCE(SUM(duration_seconds), 0) AS secs FROM study_sessions "
            "WHERE username = ? AND date(started_at) = ?",
            (username, day.isoformat()),
        ).fetchone()
        if row["secs"] <= 0:
            break
        streak += 1
        day -= timedelta(days=1)
    conn.close()
    return streak


def format_hours(total_hours):
    h = int(total_hours)
    m = int(round((total_hours - h) * 60))
    if m == 60:
        h, m = h + 1, 0
    return f"{h}h {m}m"


def get_subject_progress(username):
    """Real completion breakdown across the user's subjects (used by the
    dashboard and subjects-page 'Subject Progress' donut). Replaces the old
    hardcoded 75% / 15 / 5 / 5 placeholder with actual counts from the DB."""
    conn = get_db()
    rows = conn.execute(
        "SELECT chapters_total, chapters_done FROM subjects WHERE username = ?",
        (username,),
    ).fetchall()
    conn.close()

    completed = in_progress = not_started = 0
    total_chapters = done_chapters = 0

    for r in rows:
        total_chapters += r["chapters_total"]
        done_chapters += r["chapters_done"]
        if r["chapters_total"] > 0 and r["chapters_done"] >= r["chapters_total"]:
            completed += 1
        elif r["chapters_done"] > 0:
            in_progress += 1
        else:
            not_started += 1

    overall_pct = round((done_chapters / total_chapters) * 100) if total_chapters else 0

    return {
        "total_subjects": len(rows),
        "overall_pct": overall_pct,
        "completed": completed,
        "in_progress": in_progress,
        "not_started": not_started,
    }


def get_session_stats(username):
    """Real totals for the Study Sessions page header cards."""
    conn = get_db()
    totals = conn.execute(
        "SELECT COUNT(*) AS c, COALESCE(SUM(duration_seconds), 0) AS secs "
        "FROM study_sessions WHERE username = ?",
        (username,),
    ).fetchone()
    today = datetime.utcnow().date().isoformat()
    today_row = conn.execute(
        "SELECT COALESCE(SUM(duration_seconds), 0) AS secs FROM study_sessions "
        "WHERE username = ? AND date(started_at) = ?",
        (username, today),
    ).fetchone()
    conn.close()

    return {
        "total_sessions": totals["c"],
        "total_time": format_hours(totals["secs"] / 3600),
        "today_time": format_hours(today_row["secs"] / 3600),
        "streak": compute_streak(username),
    }


def get_theme_for(username):
    conn = get_db()
    row = conn.execute("SELECT theme FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return row["theme"] if row and row["theme"] else "system"


# ============================================================
#  XP / LEVELS
#  100 XP per level (flat). award_xp() is the single place that ever
#  touches users.xp, so level-up detection and the floor-at-zero clamp
#  can't be skipped by a call site forgetting to handle it.
#  Toggle-based actions (chapters/assignments/goals) award XP only on
#  the not-done -> done transition and remove the same amount on the
#  reverse transition, so flipping a checkbox back and forth can't be
#  used to farm infinite XP.
# ============================================================

XP_PER_LEVEL = 100
XP_CHAPTER = 15
XP_ASSIGNMENT = 10
XP_GOAL = 20
XP_TEST = 20
XP_ATTENDANCE = 5
XP_NOTE = 5
XP_EXAM = 5


def get_xp_progress(username):
    conn = get_db()
    row = conn.execute("SELECT xp FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    xp = row["xp"] if row else 0
    return {
        "xp": xp,
        "level": xp // XP_PER_LEVEL + 1,
        "into_level": xp % XP_PER_LEVEL,
        "for_level": XP_PER_LEVEL,
    }


def award_xp(username, delta):
    """Add (positive) or remove (negative) XP for username. Flashes a
    level-up message when a gain crosses a level boundary."""
    if not delta:
        return
    conn = get_db()
    row = conn.execute("SELECT xp FROM users WHERE username = ?", (username,)).fetchone()
    old_xp = row["xp"] if row else 0
    new_xp = max(0, old_xp + delta)
    conn.execute("UPDATE users SET xp = ? WHERE username = ?", (new_xp, username))
    conn.commit()
    conn.close()

    old_level = old_xp // XP_PER_LEVEL + 1
    new_level = new_xp // XP_PER_LEVEL + 1
    if delta > 0 and new_level > old_level:
        flash(f"🎉 Level up! You're now Level {new_level}.", "success")


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "username" not in session:
            flash("Please log in to view your dashboard.", "error")
            return redirect(url_for("login"))
        g.theme = get_theme_for(session["username"])
        return view(*args, **kwargs)
    return wrapped


# ============================================================
#  ROUTES
# ============================================================

@app.route("/")
def home():
    return render(INDEX_HTML, features=FEATURES, why=WHY_CHOOSE, testimonials=TESTIMONIALS)

#-----------------register---------------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        email = request.form.get("email", "").strip() or None

        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect(url_for("register"))
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return redirect(url_for("register"))

        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                (username, generate_password_hash(password), email),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            flash("That username or email is already taken.", "error")
            return redirect(url_for("register"))
        finally:
            conn.close()

        session["username"] = username
        flash("Account created — welcome to StudySmart!", "success")
        return redirect(url_for("dashboard"))

    return render(REGISTER_HTML)

#-----------------login---------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form.get("login", "").strip()
        password = request.form.get("password", "")

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            (identifier, identifier),
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["username"] = user["username"]
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid username/email or password.", "error")
        return redirect(url_for("login"))

    return render(LOGIN_HTML)

# -----------------logout---------------------------

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("You've been logged out.", "success")
    return redirect(url_for("home"))

# -----------------dashboard---------------------------

@app.route("/dashboard")
@login_required
def dashboard():
    week_labels, week_hours, total_sessions = get_week_study_data(session["username"])
    streak = compute_streak(session["username"])

    return render(
        DASHBOARD_HTML,
        sidebar_items=SIDEBAR_ITEMS,
        week_labels=week_labels,
        week_hours=week_hours,
        username=session["username"],
        active_item="Dashboard",
        stat_hours=format_hours(sum(week_hours)),
        stat_sessions=total_sessions,
        stat_streak=f"{streak} Day{'s' if streak != 1 else ''}",
        progress=get_subject_progress(session["username"]),
        xp_info=get_xp_progress(session["username"]),
    )


#-----------------subjects---------------------------

@app.route("/subjects", methods=["GET", "POST"])
@login_required
def subjects():
    if request.method == "POST":
        name = request.form.get("name", "").strip()

        try:
            chapters_total = int(request.form.get("chapters_total", 1))
        except ValueError:
            chapters_total = 1
        if chapters_total < 1:
            chapters_total = 1

        if not name:
            flash("Subject name is required.", "error")
        else:
            conn = get_db()
            count = conn.execute(
                "SELECT COUNT(*) AS c FROM subjects WHERE username = ?",
                (session["username"],),
            ).fetchone()["c"]
            color = SUBJECT_COLORS[count % len(SUBJECT_COLORS)]

            conn.execute(
                "INSERT INTO subjects (username, name, chapters_total, chapters_done, color) "
                "VALUES (?, ?, ?, 0, ?)",
                (session["username"], name, chapters_total, color),
            )
            conn.commit()
            conn.close()
            flash(f"Added {name}.", "success")

        return redirect(url_for("subjects"))

    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM subjects WHERE username = ? ORDER BY id",
        (session["username"],),
    ).fetchall()
    conn.close()

    return render(
        SUBJECTS_HTML,
        subjects=rows,
        sidebar_items=SIDEBAR_ITEMS,
        active_item="Subjects",
        progress=get_subject_progress(session["username"]),
    )


@app.route("/subjects/<int:subject_id>/increment", methods=["POST"])
@login_required
def subject_increment(subject_id):
    adjust_subject_progress(subject_id, 1)
    return redirect(url_for("subjects"))


@app.route("/subjects/<int:subject_id>/decrement", methods=["POST"])
@login_required
def subject_decrement(subject_id):
    adjust_subject_progress(subject_id, -1)
    return redirect(url_for("subjects"))


def adjust_subject_progress(subject_id, delta):
    """Move a subject's chapters_done up or down by delta, staying within 0..chapters_total."""
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM subjects WHERE id = ? AND username = ?",
        (subject_id, session["username"]),
    ).fetchone()

    if row is not None:
        new_done = row["chapters_done"] + delta
        if new_done < 0:
            new_done = 0
        if new_done > row["chapters_total"]:
            new_done = row["chapters_total"]
        conn.execute("UPDATE subjects SET chapters_done = ? WHERE id = ?", (new_done, subject_id))
        conn.commit()

    conn.close()


@app.route("/subjects/<int:subject_id>/delete", methods=["POST"])
@login_required
def subject_delete(subject_id):
    conn = get_db()
    conn.execute(
        "DELETE FROM subjects WHERE id = ? AND username = ?",
        (subject_id, session["username"]),
    )
    conn.commit()
    conn.close()
    flash("Subject removed.", "success")
    return redirect(url_for("subjects"))


@app.route("/subjects/<int:subject_id>/edit", methods=["POST"])
@login_required
def subject_edit(subject_id):

    new_name = request.form.get("name", "").strip()

    if not new_name:
        flash("Subject name cannot be empty.", "error")
        return redirect(url_for("subjects"))

    conn = get_db()

    conn.execute(
        """
        UPDATE subjects
        SET name = ?
        WHERE id = ? AND username = ?
        """,
        (new_name, subject_id, session["username"])
    )

    conn.commit()
    conn.close()

    flash("Subject updated.", "success")

    return redirect(url_for("subjects"))
# ---------------chapters---------------------------

@app.route("/chapters", methods=["GET"])
@login_required
def chapters():
    conn = get_db()
    subjects = conn.execute(
        "SELECT * FROM subjects WHERE username = ? ORDER BY name",
        (session["username"],),
    ).fetchall()
    chapter_rows = conn.execute(
        "SELECT * FROM chapters WHERE username = ? ORDER BY created_at",
        (session["username"],),
    ).fetchall()
    conn.close()

    chapters_by_subject = {}
    for s in subjects:
        items = [c for c in chapter_rows if c["subject_id"] == s["id"]]
        chapters_by_subject[s["id"]] = {
            "chs": items,
            "done": sum(1 for c in items if c["done"]),
            "total": len(items),
        }

    return render(
        CHAPTERS_HTML,
        active_item="Chapters",
        subjects=subjects,
        chapters_by_subject=chapters_by_subject,
    )


@app.route("/chapters/add", methods=["POST"])
@login_required
def chapter_add():
    subject_id = request.form.get("subject_id")
    name = request.form.get("name", "").strip()

    if not name or not subject_id:
        flash("Chapter name is required.", "error")
        return redirect(url_for("chapters"))

    conn = get_db()
    owns = conn.execute(
        "SELECT id FROM subjects WHERE id = ? AND username = ?",
        (subject_id, session["username"]),
    ).fetchone()
    if owns is None:
        conn.close()
        flash("That subject wasn't found.", "error")
        return redirect(url_for("chapters"))

    conn.execute(
        "INSERT INTO chapters (username, subject_id, name, done, created_at) VALUES (?, ?, ?, 0, ?)",
        (session["username"], subject_id, name, datetime.utcnow().isoformat(timespec="seconds")),
    )
    conn.commit()
    conn.close()
    flash(f"Added chapter \u201c{name}\u201d.", "success")
    return redirect(url_for("chapters"))


@app.route("/chapters/<int:chapter_id>/toggle", methods=["POST"])
@login_required
def chapter_toggle(chapter_id):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM chapters WHERE id = ? AND username = ?",
        (chapter_id, session["username"]),
    ).fetchone()
    if row is not None:
        now_done = 0 if row["done"] else 1
        conn.execute("UPDATE chapters SET done = ? WHERE id = ?", (now_done, chapter_id))
        conn.commit()
        conn.close()
        award_xp(session["username"], XP_CHAPTER if now_done else -XP_CHAPTER)
    else:
        conn.close()
    return redirect(url_for("chapters"))


@app.route("/chapters/<int:chapter_id>/delete", methods=["POST"])
@login_required
def chapter_delete(chapter_id):
    conn = get_db()
    conn.execute("DELETE FROM chapters WHERE id = ? AND username = ?", (chapter_id, session["username"]))
    conn.commit()
    conn.close()
    return redirect(url_for("chapters"))


def get_avg_score(username):
    conn = get_db()
    rows = conn.execute(
        "SELECT score, max_score FROM tests WHERE username = ?",
        (username,),
    ).fetchall()
    conn.close()
    if not rows:
        return None
    pcts = [(r["score"] / r["max_score"]) * 100 for r in rows if r["max_score"]]
    return round(sum(pcts) / len(pcts)) if pcts else None


# ---------------tests---------------------------

@app.route("/tests", methods=["GET"])
@login_required
def tests():
    conn = get_db()
    subjects = conn.execute(
        "SELECT * FROM subjects WHERE username = ? ORDER BY name",
        (session["username"],),
    ).fetchall()
    test_rows = conn.execute(
        "SELECT * FROM tests WHERE username = ? ORDER BY test_date DESC, id DESC",
        (session["username"],),
    ).fetchall()
    conn.close()

    avg = get_avg_score(session["username"])

    return render(
        TESTS_HTML,
        active_item="Tests",
        subjects=subjects,
        tests=test_rows,
        avg_score=f"{avg}%" if avg is not None else "—",
        today=datetime.utcnow().date().isoformat(),
    )


@app.route("/tests/add", methods=["POST"])
@login_required
def test_add():
    subject_id = request.form.get("subject_id")
    name = request.form.get("name", "").strip()
    test_date = request.form.get("test_date") or datetime.utcnow().date().isoformat()

    try:
        score = float(request.form.get("score"))
    except (TypeError, ValueError):
        score = None
    try:
        max_score = float(request.form.get("max_score") or 100)
    except (TypeError, ValueError):
        max_score = 100

    if not name or not subject_id or score is None or max_score <= 0:
        flash("Please fill in the test name, subject, and a valid score.", "error")
        return redirect(url_for("tests"))

    conn = get_db()
    srow = conn.execute(
        "SELECT name FROM subjects WHERE id = ? AND username = ?",
        (subject_id, session["username"]),
    ).fetchone()
    if srow is None:
        conn.close()
        flash("That subject wasn't found.", "error")
        return redirect(url_for("tests"))

    conn.execute(
        "INSERT INTO tests (username, subject_id, subject_name, name, score, max_score, test_date) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (session["username"], subject_id, srow["name"], name, score, max_score, test_date),
    )
    conn.commit()
    conn.close()
    flash(f"Logged {name}.", "success")
    award_xp(session["username"], XP_TEST)
    return redirect(url_for("tests"))


@app.route("/tests/<int:test_id>/delete", methods=["POST"])
@login_required
def test_delete(test_id):
    conn = get_db()
    conn.execute("DELETE FROM tests WHERE id = ? AND username = ?", (test_id, session["username"]))
    conn.commit()
    conn.close()
    return redirect(url_for("tests"))


def reconcile_active_session(row):
    """Given an active_sessions DB row, compute where the timer should be
    RIGHT NOW -- simulating forward through however many pomodoro work/break
    phase changes happened while the page was closed or on another tab.
    This is what lets the timer be accurate again after leaving for an hour,
    not just surviving a single page navigation."""
    mode = row["mode"]
    phase = row["phase"]
    accumulated_work = row["accumulated_work_seconds"]
    phase_elapsed = row["phase_elapsed_seconds"]

    if row["running"] and row["run_started_at"]:
        run_started = datetime.fromisoformat(row["run_started_at"])
        phase_elapsed += max(0, (datetime.utcnow() - run_started).total_seconds())

    if mode == "pomodoro":
        work_secs = max(1, int(row["work_minutes"] or 25)) * 60
        break_secs = max(1, int(row["break_minutes"] or 5)) * 60
        guard = 0  # bounded so a session left running for days can't loop forever
        while guard < 100000:
            duration = work_secs if phase == "work" else break_secs
            if phase_elapsed < duration:
                break
            if phase == "work":
                accumulated_work += work_secs
            phase_elapsed -= duration
            phase = "break" if phase == "work" else "work"
            guard += 1
        total_work = accumulated_work + (phase_elapsed if phase == "work" else 0)
        remaining_in_phase = (work_secs if phase == "work" else break_secs) - phase_elapsed
    else:
        total_work = accumulated_work + phase_elapsed
        remaining_in_phase = None

    return {
        "phase": phase,
        "phase_elapsed_seconds": int(phase_elapsed),
        "remaining_in_phase": int(remaining_in_phase) if remaining_in_phase is not None else None,
        "accumulated_work_seconds": int(accumulated_work),
        "total_work_seconds": int(total_work),
    }


# ---------------study sessions---------------------------

@app.route("/study-sessions", methods=["GET"])
@login_required
def study_sessions():
    conn = get_db()
    subjects = conn.execute(
        "SELECT * FROM subjects WHERE username = ? ORDER BY name",
        (session["username"],),
    ).fetchall()
    recent_sessions = conn.execute(
        "SELECT * FROM study_sessions WHERE username = ? ORDER BY started_at DESC LIMIT 10",
        (session["username"],),
    ).fetchall()
    active_row = conn.execute(
        "SELECT * FROM active_sessions WHERE username = ?", (session["username"],)
    ).fetchone()
    conn.close()

    active_session = None
    if active_row is not None:
        resolved = reconcile_active_session(active_row)
        active_session = {
            "subject_id": active_row["subject_id"],
            "subject_name": active_row["subject_name"],
            "chapter_name": active_row["chapter_name"],
            "mode": active_row["mode"],
            "work_minutes": active_row["work_minutes"],
            "break_minutes": active_row["break_minutes"],
            "running": bool(active_row["running"]),
            **resolved,
        }

    return render(
        STUDY_SESSIONS_HTML,
        active_item="Study Sessions",
        subjects=subjects,
        recent_sessions=recent_sessions,
        session_stats=get_session_stats(session["username"]),
        active_session_json=json.dumps(active_session),
    )


@app.route("/study-sessions/start", methods=["POST"])
@login_required
def study_sessions_start():
    data = request.get_json(silent=True) or {}
    mode = data.get("mode") if data.get("mode") in ("pomodoro", "stopwatch") else "stopwatch"
    chapter_name = (data.get("chapter_name") or "").strip() or None
    subject_id = data.get("subject_id") or None

    try:
        work_minutes = max(1, int(data.get("work_minutes") or 25))
    except (TypeError, ValueError):
        work_minutes = 25
    try:
        break_minutes = max(1, int(data.get("break_minutes") or 5))
    except (TypeError, ValueError):
        break_minutes = 5

    conn = get_db()
    subject_name = None
    if subject_id:
        srow = conn.execute(
            "SELECT name FROM subjects WHERE id = ? AND username = ?",
            (subject_id, session["username"]),
        ).fetchone()
        if srow is None:
            conn.close()
            return jsonify(ok=False, error="That subject wasn't found."), 400
        subject_name = srow["name"]
    else:
        subject_id = None

    conn.execute("DELETE FROM active_sessions WHERE username = ?", (session["username"],))
    conn.execute(
        """INSERT INTO active_sessions
           (username, subject_id, subject_name, chapter_name, mode, work_minutes, break_minutes,
            phase, phase_elapsed_seconds, accumulated_work_seconds, running, run_started_at, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, 'work', 0, 0, 1, ?, ?)""",
        (
            session["username"], subject_id, subject_name, chapter_name, mode, work_minutes, break_minutes,
            datetime.utcnow().isoformat(timespec="seconds"), datetime.utcnow().isoformat(timespec="seconds"),
        ),
    )
    conn.commit()
    conn.close()
    return jsonify(ok=True)


@app.route("/study-sessions/pause", methods=["POST"])
@login_required
def study_sessions_pause():
    conn = get_db()
    row = conn.execute("SELECT * FROM active_sessions WHERE username = ?", (session["username"],)).fetchone()
    if row is None:
        conn.close()
        return jsonify(ok=False, error="No active session."), 404
    resolved = reconcile_active_session(row)
    conn.execute(
        """UPDATE active_sessions SET phase = ?, phase_elapsed_seconds = ?, accumulated_work_seconds = ?,
           running = 0, run_started_at = NULL WHERE username = ?""",
        (resolved["phase"], resolved["phase_elapsed_seconds"], resolved["accumulated_work_seconds"], session["username"]),
    )
    conn.commit()
    conn.close()
    return jsonify(ok=True)


@app.route("/study-sessions/resume", methods=["POST"])
@login_required
def study_sessions_resume():
    conn = get_db()
    row = conn.execute("SELECT username FROM active_sessions WHERE username = ?", (session["username"],)).fetchone()
    if row is None:
        conn.close()
        return jsonify(ok=False, error="No active session."), 404
    conn.execute(
        "UPDATE active_sessions SET running = 1, run_started_at = ? WHERE username = ?",
        (datetime.utcnow().isoformat(timespec="seconds"), session["username"]),
    )
    conn.commit()
    conn.close()
    return jsonify(ok=True)


@app.route("/study-sessions/cancel", methods=["POST"])
@login_required
def study_sessions_cancel():
    conn = get_db()
    conn.execute("DELETE FROM active_sessions WHERE username = ?", (session["username"],))
    conn.commit()
    conn.close()
    return jsonify(ok=True)


@app.route("/study-sessions/log", methods=["POST"])
@login_required
def study_sessions_log():
    data = request.get_json(silent=True) or {}

    mode = data.get("mode") if data.get("mode") in ("pomodoro", "stopwatch") else "stopwatch"
    chapter_name = (data.get("chapter_name") or "").strip() or None

    try:
        duration_seconds = int(data.get("duration_seconds") or 0)
    except (TypeError, ValueError):
        duration_seconds = 0
    if duration_seconds < 1:
        return jsonify(ok=False, error="No time was recorded for that session."), 400

    planned_minutes = data.get("planned_minutes")
    try:
        planned_minutes = int(planned_minutes) if planned_minutes not in (None, "") else None
    except (TypeError, ValueError):
        planned_minutes = None

    subject_id = data.get("subject_id")
    subject_name = None

    conn = get_db()
    if subject_id:
        row = conn.execute(
            "SELECT name FROM subjects WHERE id = ? AND username = ?",
            (subject_id, session["username"]),
        ).fetchone()
        if row is None:
            conn.close()
            return jsonify(ok=False, error="That subject wasn't found."), 400
        subject_name = row["name"]
    else:
        subject_id = None

    conn.execute(
        """INSERT INTO study_sessions
           (username, subject_id, subject_name, chapter_name, mode, planned_minutes, duration_seconds, started_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            session["username"], subject_id, subject_name, chapter_name,
            mode, planned_minutes, duration_seconds,
            datetime.utcnow().isoformat(timespec="seconds"),
        ),
    )
    conn.commit()
    conn.close()

    # The session is now permanently logged, so any in-progress timer
    # record for this user is done with -- clear it so a stale "resume"
    # can't reappear on the next visit.
    conn2 = get_db()
    conn2.execute("DELETE FROM active_sessions WHERE username = ?", (session["username"],))
    conn2.commit()
    conn2.close()

    award_xp(session["username"], max(1, duration_seconds // 60))

    return jsonify(ok=True)

#-----------------assignments---------------------------

@app.route("/assignments", methods=["GET"])
@login_required
def assignments():
    conn = get_db()
    subjects = conn.execute(
        "SELECT * FROM subjects WHERE username = ? ORDER BY name",
        (session["username"],),
    ).fetchall()
    rows = conn.execute(
        "SELECT * FROM assignments WHERE username = ? ORDER BY done ASC, (due_date IS NULL), due_date ASC, id DESC",
        (session["username"],),
    ).fetchall()
    conn.close()

    pending = sum(1 for r in rows if not r["done"])

    return render(
        ASSIGNMENTS_HTML,
        active_item="Assignments",
        subjects=subjects,
        assignments=rows,
        pending_count=pending,
        today=datetime.utcnow().date().isoformat(),
    )


@app.route("/assignments/add", methods=["POST"])
@login_required
def assignment_add():
    title = request.form.get("title", "").strip()
    due_date = request.form.get("due_date") or None
    subject_id = request.form.get("subject_id") or None

    if not title:
        flash("Assignment title is required.", "error")
        return redirect(url_for("assignments"))

    conn = get_db()
    subject_name = None
    if subject_id:
        srow = conn.execute(
            "SELECT name FROM subjects WHERE id = ? AND username = ?",
            (subject_id, session["username"]),
        ).fetchone()
        subject_name = srow["name"] if srow else None

    conn.execute(
        "INSERT INTO assignments (username, subject_id, subject_name, title, due_date, done, created_at) "
        "VALUES (?, ?, ?, ?, ?, 0, ?)",
        (session["username"], subject_id, subject_name, title, due_date,
         datetime.utcnow().isoformat(timespec="seconds")),
    )
    conn.commit()
    conn.close()
    flash(f"Added {title}.", "success")
    return redirect(url_for("assignments"))


@app.route("/assignments/<int:assignment_id>/toggle", methods=["POST"])
@login_required
def assignment_toggle(assignment_id):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM assignments WHERE id = ? AND username = ?",
        (assignment_id, session["username"]),
    ).fetchone()
    if row is not None:
        now_done = 0 if row["done"] else 1
        conn.execute("UPDATE assignments SET done = ? WHERE id = ?", (now_done, assignment_id))
        conn.commit()
        conn.close()
        award_xp(session["username"], XP_ASSIGNMENT if now_done else -XP_ASSIGNMENT)
    else:
        conn.close()
    return redirect(url_for("assignments"))


@app.route("/assignments/<int:assignment_id>/delete", methods=["POST"])
@login_required
def assignment_delete(assignment_id):
    conn = get_db()
    conn.execute("DELETE FROM assignments WHERE id = ? AND username = ?", (assignment_id, session["username"]))
    conn.commit()
    conn.close()
    return redirect(url_for("assignments"))


#-----------------attendance---------------------------

@app.route("/attendance", methods=["GET"])
@login_required
def attendance():
    conn = get_db()
    subjects = conn.execute(
        "SELECT * FROM subjects WHERE username = ? ORDER BY name",
        (session["username"],),
    ).fetchall()
    rows = conn.execute(
        "SELECT * FROM attendance WHERE username = ? ORDER BY att_date DESC, id DESC",
        (session["username"],),
    ).fetchall()
    conn.close()

    total = len(rows)
    present = sum(1 for r in rows if r["status"] == "present")
    pct = round((present / total) * 100) if total else None

    return render(
        ATTENDANCE_HTML,
        active_item="Attendance",
        subjects=subjects,
        records=rows,
        pct=f"{pct}%" if pct is not None else "—",
        present_count=present,
        total_count=total,
        today=datetime.utcnow().date().isoformat(),
    )


@app.route("/attendance/add", methods=["POST"])
@login_required
def attendance_add():
    subject_id = request.form.get("subject_id") or None
    att_date = request.form.get("att_date") or datetime.utcnow().date().isoformat()
    status = request.form.get("status") if request.form.get("status") in ("present", "absent") else "present"

    conn = get_db()
    subject_name = None
    if subject_id:
        srow = conn.execute(
            "SELECT name FROM subjects WHERE id = ? AND username = ?",
            (subject_id, session["username"]),
        ).fetchone()
        subject_name = srow["name"] if srow else None

    conn.execute(
        "INSERT INTO attendance (username, subject_id, subject_name, att_date, status) VALUES (?, ?, ?, ?, ?)",
        (session["username"], subject_id, subject_name, att_date, status),
    )
    conn.commit()
    conn.close()
    flash("Attendance recorded.", "success")
    award_xp(session["username"], XP_ATTENDANCE)
    return redirect(url_for("attendance"))


@app.route("/attendance/<int:record_id>/delete", methods=["POST"])
@login_required
def attendance_delete(record_id):
    conn = get_db()
    conn.execute("DELETE FROM attendance WHERE id = ? AND username = ?", (record_id, session["username"]))
    conn.commit()
    conn.close()
    return redirect(url_for("attendance"))


#-----------------goals---------------------------

@app.route("/goals", methods=["GET"])
@login_required
def goals():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM goals WHERE username = ? ORDER BY done ASC, (target_date IS NULL), target_date ASC, id DESC",
        (session["username"],),
    ).fetchall()
    conn.close()

    done_count = sum(1 for r in rows if r["done"])

    return render(
        GOALS_HTML,
        active_item="Goals",
        goals=rows,
        done_count=done_count,
        today=datetime.utcnow().date().isoformat(),
    )


@app.route("/goals/add", methods=["POST"])
@login_required
def goal_add():
    title = request.form.get("title", "").strip()
    target_date = request.form.get("target_date") or None

    if not title:
        flash("Goal text is required.", "error")
        return redirect(url_for("goals"))

    conn = get_db()
    conn.execute(
        "INSERT INTO goals (username, title, target_date, done, created_at) VALUES (?, ?, ?, 0, ?)",
        (session["username"], title, target_date, datetime.utcnow().isoformat(timespec="seconds")),
    )
    conn.commit()
    conn.close()
    flash("Goal added.", "success")
    return redirect(url_for("goals"))


@app.route("/goals/<int:goal_id>/toggle", methods=["POST"])
@login_required
def goal_toggle(goal_id):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM goals WHERE id = ? AND username = ?",
        (goal_id, session["username"]),
    ).fetchone()
    if row is not None:
        now_done = 0 if row["done"] else 1
        conn.execute("UPDATE goals SET done = ? WHERE id = ?", (now_done, goal_id))
        conn.commit()
        conn.close()
        award_xp(session["username"], XP_GOAL if now_done else -XP_GOAL)
    else:
        conn.close()
    return redirect(url_for("goals"))


@app.route("/goals/<int:goal_id>/delete", methods=["POST"])
@login_required
def goal_delete(goal_id):
    conn = get_db()
    conn.execute("DELETE FROM goals WHERE id = ? AND username = ?", (goal_id, session["username"]))
    conn.commit()
    conn.close()
    return redirect(url_for("goals"))


#-----------------notes---------------------------

@app.route("/notes", methods=["GET"])
@login_required
def notes():
    conn = get_db()
    subjects = conn.execute(
        "SELECT * FROM subjects WHERE username = ? ORDER BY name",
        (session["username"],),
    ).fetchall()
    rows = conn.execute(
        "SELECT * FROM notes WHERE username = ? ORDER BY created_at DESC",
        (session["username"],),
    ).fetchall()
    conn.close()

    return render(
        NOTES_HTML,
        active_item="Notes",
        subjects=subjects,
        notes=rows,
    )


@app.route("/notes/add", methods=["POST"])
@login_required
def note_add():
    title = request.form.get("title", "").strip()
    body = request.form.get("body", "").strip() or None
    subject_id = request.form.get("subject_id") or None

    if not title:
        flash("Note title is required.", "error")
        return redirect(url_for("notes"))

    conn = get_db()
    subject_name = None
    if subject_id:
        srow = conn.execute(
            "SELECT name FROM subjects WHERE id = ? AND username = ?",
            (subject_id, session["username"]),
        ).fetchone()
        subject_name = srow["name"] if srow else None

    conn.execute(
        "INSERT INTO notes (username, subject_id, subject_name, title, body, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (session["username"], subject_id, subject_name, title, body,
         datetime.utcnow().isoformat(timespec="seconds")),
    )
    conn.commit()
    conn.close()
    flash("Note saved.", "success")
    award_xp(session["username"], XP_NOTE)
    return redirect(url_for("notes"))


@app.route("/notes/<int:note_id>/delete", methods=["POST"])
@login_required
def note_delete(note_id):
    conn = get_db()
    conn.execute("DELETE FROM notes WHERE id = ? AND username = ?", (note_id, session["username"]))
    conn.commit()
    conn.close()
    return redirect(url_for("notes"))


#-----------------calendar / exam planner---------------------------

@app.route("/calendar", methods=["GET"])
@login_required
def calendar_page():
    conn = get_db()
    subjects = conn.execute(
        "SELECT * FROM subjects WHERE username = ? ORDER BY name",
        (session["username"],),
    ).fetchall()
    rows = conn.execute(
        "SELECT * FROM exams WHERE username = ? ORDER BY exam_date ASC",
        (session["username"],),
    ).fetchall()
    conn.close()

    today = datetime.utcnow().date()
    exams_with_countdown = []
    for r in rows:
        try:
            exam_date = datetime.strptime(r["exam_date"], "%Y-%m-%d").date()
            days_left = (exam_date - today).days
        except ValueError:
            days_left = None
        exams_with_countdown.append({**dict(r), "days_left": days_left})

    return render(
        CALENDAR_HTML,
        active_item="Calendar",
        subjects=subjects,
        exams=exams_with_countdown,
        today=today.isoformat(),
    )


@app.route("/calendar/add", methods=["POST"])
@login_required
def exam_add():
    title = request.form.get("title", "").strip()
    exam_date = request.form.get("exam_date") or ""
    subject_id = request.form.get("subject_id") or None

    if not title or not exam_date:
        flash("Exam title and date are required.", "error")
        return redirect(url_for("calendar_page"))

    conn = get_db()
    subject_name = None
    if subject_id:
        srow = conn.execute(
            "SELECT name FROM subjects WHERE id = ? AND username = ?",
            (subject_id, session["username"]),
        ).fetchone()
        subject_name = srow["name"] if srow else None

    conn.execute(
        "INSERT INTO exams (username, subject_id, subject_name, title, exam_date) VALUES (?, ?, ?, ?, ?)",
        (session["username"], subject_id, subject_name, title, exam_date),
    )
    conn.commit()
    conn.close()
    flash(f"Added {title} to your calendar.", "success")
    award_xp(session["username"], XP_EXAM)
    return redirect(url_for("calendar_page"))


@app.route("/calendar/<int:exam_id>/delete", methods=["POST"])
@login_required
def exam_delete(exam_id):
    conn = get_db()
    conn.execute("DELETE FROM exams WHERE id = ? AND username = ?", (exam_id, session["username"]))
    conn.commit()
    conn.close()
    return redirect(url_for("calendar_page"))


#-----------------settings---------------------------

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    conn = get_db()

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip() or None
        class_name = request.form.get("class_name", "").strip() or None
        avatar = request.form.get("avatar", "").strip() or "🎓"
        theme = request.form.get("theme", "system")
        if theme not in ("light", "dark", "system"):
            theme = "system"

        conn.execute(
            "UPDATE users SET full_name = ?, class_name = ?, avatar = ?, theme = ? WHERE username = ?",
            (full_name, class_name, avatar, theme, session["username"]),
        )
        conn.commit()
        conn.close()
        flash("Settings saved.", "success")
        g.theme = theme  # so the redirect below renders with the new theme, not the stale one
        return redirect(url_for("settings"))

    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (session["username"],)
    ).fetchone()
    conn.close()

    return render(
        SETTINGS_HTML,
        active_item="Settings",
        user=user,
    )


#-----------------run app---------------------------

if __name__ == "__main__":
    app.run(debug=True)