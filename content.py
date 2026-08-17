"""
StudySmart — static content used to populate the landing page and dashboard.

None of this is user data (that lives in the database) — it's copy and
demo numbers that get plugged into the Jinja templates.
"""

FEATURES = [
    {"emoji": "📖", "color": "green", "title": "Subject & Chapter Tracking",
     "desc": "Organize subjects, track chapters, and monitor syllabus completion with ease."},
    {"emoji": "📊", "color": "purple", "title": "Test Scores & Analytics",
     "desc": "Record test scores and visualize your performance with beautiful graphs."},
    {"emoji": "📅", "color": "blue", "title": "Attendance Tracker",
     "desc": "Track attendance and maintain your overall percentage automatically."},
    {"emoji": "📋", "color": "orange", "title": "Assignment Manager",
     "desc": "Never miss a deadline. Manage assignments and track completion."},
    {"emoji": "🎯", "color": "teal", "title": "Goals & Study Streaks",
     "desc": "Set goals, build streaks, and stay consistent in your study journey."},
    {"emoji": "📔", "color": "pink", "title": "Notes Manager",
     "desc": "Create, organize, and access your notes anytime, anywhere."},
    {"emoji": "🗓", "color": "amber", "title": "Exam Planner",
     "desc": "Plan your exams and get countdowns for important dates."},
    {"emoji": "⏱", "color": "indigo", "title": "Study Session Tracker",
     "desc": "Track study hours, subjects, and boost your productivity."},
    {"emoji": "🏅", "color": "emerald", "title": "Achievements & Badges",
     "desc": "Earn badges and unlock achievements as you reach milestones."},
    {"emoji": "🥧", "color": "sky", "title": "Insights & Reports",
     "desc": "Get detailed insights and export your data as PDF or CSV reports."},
]

WHY_CHOOSE = [
    {"title": "Secure & Private", "desc": "Your data is safe and protected."},
    {"title": "Access Anywhere", "desc": "Use on any device, anytime, anywhere."},
    {"title": "Save Time", "desc": "Everything organized in one dashboard."},
    {"title": "Boost Productivity", "desc": "Stay focused and achieve more."},
    {"title": "Made for Students", "desc": "Designed by students, for students."},
]

TESTIMONIALS = [
    {"name": "Sarah K.", "role": "Class 11 Student", "stars": 4,
     "quote": "StudySmart helped me organize my studies and improve my scores significantly. The dashboard is super easy to use!"},
    {"name": "James P.", "role": "Class 12 Student", "stars": 5,
     "quote": "I love the study streaks and goals feature. It keeps me motivated every day to study consistently."},
    {"name": "Ananya R.", "role": "College Student", "stars": 5,
     "quote": "The analytics and progress tracking are amazing. Now I know exactly where I need to focus more."},
]

WEEK_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
WEEK_HOURS = [2.5, 4, 3, 5.5, 4.5, 6.5, 5]

SIDEBAR_ITEMS = [
    "Dashboard", "Subjects", "Chapters", "Tests", "Assignments",
    "Attendance", "Study Sessions", "Goals", "Notes", "Calendar", "Settings",
]

# Every sidebar label maps to a real Flask endpoint. Every page's sidebar
# loops over SIDEBAR_ITEMS and looks up its endpoint here, so there is one
# place that decides where each nav link goes -- no page can silently fall
# back to a fake, non-navigating button.
SIDEBAR_ENDPOINTS = {
    "Dashboard": "dashboard",
    "Subjects": "subjects",
    "Chapters": "chapters",
    "Tests": "tests",
    "Assignments": "assignments",
    "Attendance": "attendance",
    "Study Sessions": "study_sessions",
    "Goals": "goals",
    "Notes": "notes",
    "Calendar": "calendar_page",
    "Settings": "settings",
}