# ============================================================
# EDUPRO
# INSTRUCTOR PERFORMANCE & COURSE QUALITY EVALUATION
# Complete Streamlit Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EduPro | Instructor Intelligence",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

EXCEL_PATH = DATA_DIR / "EduPro Online Platform (2).xlsx"

INSTRUCTOR_PATH = DATA_DIR / "instructor_metrics.csv"
EXPERTISE_PATH = DATA_DIR / "expertise_analysis.csv"
CATEGORY_PATH = DATA_DIR / "category_quality.csv"
LEVEL_PATH = DATA_DIR / "level_quality.csv"
COURSE_PATH = DATA_DIR / "course_performance.csv"
SUMMARY_PATH = DATA_DIR / "eda_summary.csv"


# ============================================================
# THEME TOKENS — "The Faculty Ledger"
# ============================================================
# A registrar's gradebook, reimagined as a dashboard: cool
# graph-paper background, ink-navy text, a red grading-pen
# accent for attention and a brass-stamp accent for honors.
# Newsreader (a book-serif) carries headlines, IBM Plex Mono
# carries every number (ledger figures), Public Sans carries
# body copy and UI chrome.

INK = "#1D2A44"
INK_SOFT = "#48557A"
PEN = "#B23A2E"
PEN_SOFT = "#F5E2DE"
BRASS = "#A9832F"
BRASS_SOFT = "#F1E8CF"
BG = "#EAEDF0"
SURFACE = "#FFFFFF"
BORDER = "#D2D8DE"
MUTED = "#5C6B82"

CHART_PALETTE = [INK, PEN, BRASS, "#7C88A8", "#D97F72", "#C7AD68"]

CUSTOM_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,500;0,600;1,400;1,500&family=IBM+Plex+Mono:wght@400;500;600&family=Public+Sans:wght@400;500;600;700&display=swap');

html {{ scroll-behavior: smooth; }}

html, body, [class*="css"], .stMarkdown, .stText {{
    font-family: 'Public Sans', sans-serif;
    color: {INK};
}}

.stApp {{
    background-color: {BG};
    background-image:
        linear-gradient(rgba(29,42,68,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(29,42,68,0.05) 1px, transparent 1px);
    background-size: 28px 28px;
}}

.block-container {{
    padding-top: 1.6rem;
    padding-bottom: 3rem;
    max-width: 1420px;
}}

h1, h2, h3 {{
    font-family: 'Newsreader', serif;
    color: {INK};
}}

code, .stCode, [data-testid="stMetricValue"] {{
    font-family: 'IBM Plex Mono', monospace !important;
}}

/* ---------- One orchestrated motion: the stamp ---------- */
@keyframes stampSlam {{
    0%   {{ opacity: 0; transform: rotate(-14deg) scale(2.1); }}
    55%  {{ opacity: 1; transform: rotate(-7deg) scale(0.94); }}
    75%  {{ opacity: 1; transform: rotate(-8deg) scale(1.04); }}
    100% {{ opacity: 1; transform: rotate(-7deg) scale(1); }}
}}
@keyframes ruleDraw {{
    from {{ width: 0; }}
    to   {{ width: 100%; }}
}}
@keyframes pulseDot {{
    0%   {{ box-shadow: 0 0 0 0 rgba(178,58,46,0.55); }}
    70%  {{ box-shadow: 0 0 0 7px rgba(178,58,46,0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(178,58,46,0); }}
}}

/* ---------- Sidebar: the ledger spine ---------- */
[data-testid="stSidebar"] {{
    background: {INK};
    border-right: 3px double {BRASS};
}}
[data-testid="stSidebar"] * {{
    color: #E4E7EF !important;
    font-family: 'Public Sans', sans-serif;
}}
[data-testid="stSidebar"] h1 {{
    font-family: 'Newsreader', serif;
    font-style: italic;
    font-weight: 500;
    border-bottom: 1px solid rgba(255,255,255,0.18);
    padding-bottom: 12px;
}}
[data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,0.16); }}

/* Nav rendered as filing tabs */
[data-testid="stSidebar"] div[role="radiogroup"] label {{
    background-color: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.12);
    border-left: 3px solid transparent;
    border-radius: 0 4px 4px 0;
    padding: 8px 12px;
    margin-bottom: 6px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.88rem;
    transition: border-left-color 0.15s ease, background-color 0.15s ease;
}}
[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
    background-color: rgba(169,131,47,0.18);
    border-left-color: {BRASS};
}}
[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {{
    background-color: rgba(178,58,46,0.22);
    border-left-color: {PEN};
}}

.status-pill {{
    display: flex;
    align-items: center;
    gap: 8px;
    background-color: rgba(178,58,46,0.14);
    border: 1px solid rgba(178,58,46,0.4);
    border-radius: 4px;
    padding: 8px 12px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    color: #F0D9D5 !important;
}}
.status-dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background-color: {PEN};
    animation: pulseDot 1.9s infinite;
    flex-shrink: 0;
}}

/* ---------- Hero: the open ledger header ---------- */
.edu-hero {{
    background-color: {SURFACE};
    border-top: 3px double {INK};
    border-bottom: 1px solid {BORDER};
    padding: 30px 4px 22px 4px;
    margin-bottom: 26px;
}}
.edu-hero h1 {{
    font-size: 2.3rem;
    font-style: italic;
    font-weight: 500;
    margin: 0 0 6px 0;
    color: {INK};
}}
.edu-hero p {{
    color: {MUTED};
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.92rem;
    letter-spacing: 0.01em;
    margin: 0;
}}

/* ---------- Rubber stamp ---------- */
.stamp {{
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: {PEN};
    border: 2.5px solid {PEN};
    border-radius: 5px;
    padding: 7px 16px;
    margin: 4px 0 16px 0;
    transform: rotate(-7deg);
    animation: stampSlam 0.5s cubic-bezier(.36,1.4,.4,1) both;
}}

/* ---------- Page title ---------- */
.page-title {{
    font-family: 'Newsreader', serif;
    font-size: 1.8rem;
    font-weight: 600;
    color: {INK};
    margin-bottom: 0.1rem;
}}
.page-subtitle {{
    color: {MUTED};
    font-size: 0.98rem;
    margin-bottom: 1.3rem;
    border-bottom: 1px solid {BORDER};
    padding-bottom: 12px;
}}

/* ---------- Section headers: ledger column heads ---------- */
.edu-section {{
    margin: 8px 0 14px 0;
    border-top: 1.5px solid {INK};
    border-bottom: 1px solid {INK};
    padding: 6px 0;
}}
.edu-section h3 {{
    margin: 0;
    font-size: 1.2rem;
    font-weight: 600;
    font-style: italic;
}}

/* ---------- KPI / ledger cards ---------- */
.edu-card {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-bottom: 3px solid {INK};
    border-radius: 3px;
    padding: 13px 15px;
    height: 100%;
}}
.edu-card.pen {{ border-bottom-color: {PEN}; }}
.edu-card.brass {{ border-bottom-color: {BRASS}; }}
.edu-card .label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: {MUTED};
    margin-bottom: 6px;
}}
.edu-card .value {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.4rem;
    font-weight: 600;
    color: {INK};
    line-height: 1.2;
}}
.edu-card .note {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.76rem;
    color: {PEN};
    margin-top: 4px;
}}

/* ---------- Streamlit widgets ---------- */
[data-testid="stMetric"] {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-bottom: 3px solid {INK};
    border-radius: 3px;
    padding: 13px 15px;
}}
[data-testid="stMetricLabel"] {{ color: {MUTED}; font-family: 'IBM Plex Mono', monospace; }}
[data-testid="stMetricValue"] {{ color: {INK}; }}

.stButton > button, .stDownloadButton > button {{
    background-color: {INK};
    color: #FFFFFF;
    border: none;
    border-radius: 3px;
    padding: 0.5rem 1.1rem;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 500;
    font-size: 0.86rem;
}}
.stButton > button:hover, .stDownloadButton > button:hover {{
    background-color: {PEN};
    color: #FFFFFF;
}}

div[data-baseweb="select"] > div {{
    border-radius: 3px;
    border-color: {BORDER};
}}

[data-testid="stDataFrame"] {{
    border: 1px solid {BORDER};
    border-radius: 3px;
    overflow: hidden;
}}

.stAlert {{ border-radius: 3px; }}

hr {{ border-color: {BORDER}; }}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def altair_theme():
    return {
        "config": {
            "background": SURFACE,
            "title": {"font": "Newsreader", "fontSize": 14, "color": INK},
            "mark": {"color": INK},
            "bar": {"cornerRadiusTopLeft": 2, "cornerRadiusTopRight": 2},
            "circle": {"color": PEN},
            "axis": {
                "labelFont": "IBM Plex Mono",
                "titleFont": "Public Sans",
                "labelColor": MUTED,
                "titleColor": INK_SOFT,
                "gridColor": BORDER,
                "domainColor": BORDER,
            },
            "legend": {"labelFont": "IBM Plex Mono", "titleFont": "Public Sans"},
            "range": {"category": CHART_PALETTE, "heatmap": "blues"},
        }
    }


alt.themes.register("edupro_ledger", altair_theme)
alt.themes.enable("edupro_ledger")


def hero(title, subtitle):
    st.markdown(
        f'<div id="top"></div>'
        f'<div class="edu-hero"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def page_header(title, subtitle):
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def section_header(title):
    st.markdown(
        f'<div class="edu-section"><h3>{title}</h3></div>',
        unsafe_allow_html=True,
    )


def kpi_card(label, value, note=None, tone="ink"):
    tone_class = f" {tone}"
    note_html = f'<div class="note">{note}</div>' if note else ""
    st.markdown(
        f'<div class="edu-card{tone_class}">'
        f'<div class="label">{label}</div>'
        f'<div class="value">{value}</div>{note_html}</div>',
        unsafe_allow_html=True,
    )


def kpi_row(items):
    """items: list of dicts with label, value, note (optional), tone (optional)"""
    cols = st.columns(len(items))
    tones = ["ink", "pen", "brass"]
    for i, (col, item) in enumerate(zip(cols, items)):
        with col:
            kpi_card(
                item["label"],
                item["value"],
                item.get("note"),
                item.get("tone", tones[i % 3]),
            )


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_excel_data():

    users = pd.read_excel(
        EXCEL_PATH,
        sheet_name="Users"
    )

    teachers = pd.read_excel(
        EXCEL_PATH,
        sheet_name="Teachers"
    )

    courses = pd.read_excel(
        EXCEL_PATH,
        sheet_name="Courses"
    )

    transactions = pd.read_excel(
        EXCEL_PATH,
        sheet_name="Transactions"
    )

    return users, teachers, courses, transactions


@st.cache_data
def load_analysis_files():

    instructor = pd.read_csv(
        INSTRUCTOR_PATH
    )

    expertise = pd.read_csv(
        EXPERTISE_PATH
    )

    category = pd.read_csv(
        CATEGORY_PATH
    )

    level = pd.read_csv(
        LEVEL_PATH
    )

    course = pd.read_csv(
        COURSE_PATH
    )

    summary = pd.read_csv(
        SUMMARY_PATH
    )

    return (
        instructor,
        expertise,
        category,
        level,
        course,
        summary
    )


# ============================================================
# LOAD DATA WITH FALLBACK
# ============================================================

try:

    users, teachers, courses, transactions = load_excel_data()

except Exception as error:

    st.error(
        "Unable to load the EduPro Excel dataset."
    )

    st.exception(error)

    st.stop()


# ============================================================
# CLEAN RAW DATA
# ============================================================

users = (
    users
    .dropna(how="all")
    .drop_duplicates()
    .copy()
)

teachers = (
    teachers
    .dropna(how="all")
    .drop_duplicates()
    .copy()
)

courses = (
    courses
    .dropna(how="all")
    .drop_duplicates()
    .copy()
)

transactions = (
    transactions
    .dropna(how="all")
    .drop_duplicates()
    .copy()
)


# ============================================================
# NUMERIC CONVERSION
# ============================================================

for column in [
    "Age",
    "YearsOfExperience",
    "TeacherRating"
]:

    if column in teachers.columns:

        teachers[column] = pd.to_numeric(
            teachers[column],
            errors="coerce"
        )


for column in [
    "CoursePrice",
    "CourseDuration",
    "CourseRating"
]:

    if column in courses.columns:

        courses[column] = pd.to_numeric(
            courses[column],
            errors="coerce"
        )


if "Amount" in transactions.columns:

    transactions["Amount"] = pd.to_numeric(
        transactions["Amount"],
        errors="coerce"
    )


if "TransactionDate" in transactions.columns:

    transactions["TransactionDate"] = pd.to_datetime(
        transactions["TransactionDate"],
        errors="coerce"
    )


# ============================================================
# CREATE INTEGRATED DATASET
# ============================================================

teacher_transactions = transactions.merge(
    teachers,
    on="TeacherID",
    how="left"
)

analysis_data = teacher_transactions.merge(
    courses,
    on="CourseID",
    how="left",
    suffixes=("_Teacher", "_Course")
)


# ============================================================
# LOAD EDA OUTPUTS IF AVAILABLE
# ============================================================

try:

    (
        instructor_metrics,
        expertise_analysis,
        category_quality,
        level_quality,
        course_performance,
        eda_summary
    ) = load_analysis_files()

    analysis_files_available = True

except Exception:

    analysis_files_available = False


# ============================================================
# FALLBACK: CALCULATE INSTRUCTOR METRICS
# ============================================================

if not analysis_files_available:

    instructor_metrics = (
        analysis_data
        .groupby(
            [
                "TeacherID",
                "TeacherName",
                "Age",
                "Gender",
                "Expertise",
                "YearsOfExperience",
                "TeacherRating"
            ],
            dropna=False
        )
        .agg(
            TotalEnrollments=(
                "TransactionID",
                "count"
            ),
            CoursesTaught=(
                "CourseID",
                "nunique"
            ),
            AverageCourseRating=(
                "CourseRating",
                "mean"
            ),
            TotalRevenue=(
                "Amount",
                "sum"
            ),
            AverageCoursePrice=(
                "CoursePrice",
                "mean"
            )
        )
        .reset_index()
    )

    rating_std = (
        analysis_data
        .groupby("TeacherID")[
            "CourseRating"
        ]
        .std()
        .fillna(0)
        .reset_index(
            name="RatingStdDev"
        )
    )

    instructor_metrics = instructor_metrics.merge(
        rating_std,
        on="TeacherID",
        how="left"
    )

    max_std = instructor_metrics[
        "RatingStdDev"
    ].max()

    if max_std > 0:

        instructor_metrics[
            "RatingConsistencyIndex"
        ] = (
            1
            -
            instructor_metrics[
                "RatingStdDev"
            ] / max_std
        ) * 100

    else:

        instructor_metrics[
            "RatingConsistencyIndex"
        ] = 100

    max_experience = instructor_metrics[
        "YearsOfExperience"
    ].max()

    if max_experience > 0:

        experience_score = (
            instructor_metrics[
                "YearsOfExperience"
            ] / max_experience
        ) * 100

    else:

        experience_score = 0

    instructor_metrics[
        "ExperienceImpactScore"
    ] = (
        0.5 * experience_score
        +
        0.5 *
        (
            instructor_metrics[
                "TeacherRating"
            ] / 5
        ) * 100
    )

    avg_enrollment = instructor_metrics[
        "TotalEnrollments"
    ].mean()

    if avg_enrollment > 0:

        instructor_metrics[
            "EnrollmentInfluenceRatio"
        ] = (
            instructor_metrics[
                "TotalEnrollments"
            ] / avg_enrollment
        )

    else:

        instructor_metrics[
            "EnrollmentInfluenceRatio"
        ] = 0

    instructor_metrics[
        "OverallScore"
    ] = (

        instructor_metrics[
            "TeacherRating"
        ] / 5 * 30

        +

        instructor_metrics[
            "AverageCourseRating"
        ] / 5 * 30

        +

        instructor_metrics[
            "RatingConsistencyIndex"
        ] / 100 * 20

        +

        instructor_metrics[
            "ExperienceImpactScore"
        ] / 100 * 20
    )

    expertise_analysis = (
        instructor_metrics
        .groupby("Expertise")
        .agg(
            Instructors=(
                "TeacherID",
                "nunique"
            ),
            AverageTeacherRating=(
                "TeacherRating",
                "mean"
            ),
            AverageCourseRating=(
                "AverageCourseRating",
                "mean"
            ),
            AverageExperience=(
                "YearsOfExperience",
                "mean"
            ),
            TotalEnrollments=(
                "TotalEnrollments",
                "sum"
            )
        )
        .reset_index()
    )

    category_quality = (
        analysis_data
        .groupby("CourseCategory")
        .agg(
            AverageCourseRating=(
                "CourseRating",
                "mean"
            ),
            Courses=(
                "CourseID",
                "nunique"
            ),
            Enrollments=(
                "TransactionID",
                "count"
            ),
            AverageCoursePrice=(
                "CoursePrice",
                "mean"
            )
        )
        .reset_index()
    )

    level_quality = (
        analysis_data
        .groupby("CourseLevel")
        .agg(
            AverageCourseRating=(
                "CourseRating",
                "mean"
            ),
            Courses=(
                "CourseID",
                "nunique"
            ),
            Enrollments=(
                "TransactionID",
                "count"
            )
        )
        .reset_index()
    )

    course_performance = (
        analysis_data
        .groupby(
            [
                "CourseID",
                "CourseName",
                "CourseCategory",
                "CourseLevel",
                "TeacherID",
                "TeacherName"
            ]
        )
        .agg(
            CourseRating=(
                "CourseRating",
                "mean"
            ),
            Enrollments=(
                "TransactionID",
                "count"
            ),
            Revenue=(
                "Amount",
                "sum"
            )
        )
        .reset_index()
    )

else:

    # Make sure numeric columns are numeric
    for column in [
        "TeacherRating",
        "AverageCourseRating",
        "TotalEnrollments",
        "CoursesTaught",
        "TotalRevenue",
        "AverageCoursePrice",
        "RatingStdDev",
        "RatingConsistencyIndex",
        "ExperienceImpactScore",
        "EnrollmentInfluenceRatio",
        "OverallScore"
    ]:

        if column in instructor_metrics.columns:

            instructor_metrics[column] = pd.to_numeric(
                instructor_metrics[column],
                errors="coerce"
            )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("# 📖 EduPro")

st.sidebar.caption(
    "Instructor Intelligence Platform"
)

st.sidebar.divider()
st.sidebar.markdown("**Navigation**")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Instructor Performance",
        "Course Quality",
        "Expertise Analysis",
        "Advanced Analytics"
    ],
    label_visibility="collapsed",
)

st.sidebar.divider()
st.sidebar.markdown(
    '<div class="status-pill"><span class="status-dot"></span>Register open — data connected</div>',
    unsafe_allow_html=True,
)

st.sidebar.divider()

st.sidebar.subheader("Filters")


# ============================================================
# SIDEBAR FILTERS
# ============================================================

expertise_options = sorted(
    teachers[
        "Expertise"
    ]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_expertise = st.sidebar.multiselect(
    "Instructor Expertise",
    expertise_options,
    default=expertise_options
)


category_options = sorted(
    courses[
        "CourseCategory"
    ]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_categories = st.sidebar.multiselect(
    "Course Category",
    category_options,
    default=category_options
)


level_options = sorted(
    courses[
        "CourseLevel"
    ]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_levels = st.sidebar.multiselect(
    "Course Level",
    level_options,
    default=level_options
)


min_teacher_rating = float(
    teachers["TeacherRating"].min()
)

max_teacher_rating = float(
    teachers["TeacherRating"].max()
)

rating_filter = st.sidebar.slider(
    "Teacher Rating",
    min_value=float(
        np.floor(min_teacher_rating * 10) / 10
    ),
    max_value=float(
        np.ceil(max_teacher_rating * 10) / 10
    ),
    value=(
        float(
            np.floor(min_teacher_rating * 10) / 10
        ),
        float(
            np.ceil(max_teacher_rating * 10) / 10
        )
    ),
    step=0.1
)

st.sidebar.divider()
st.sidebar.caption("EduPro Instructor Intelligence")
st.sidebar.caption("Instructor Performance & Course Quality Evaluation")
st.sidebar.caption("Built with Python + Pandas + Altair + Streamlit")


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_teachers = teachers[
    teachers["Expertise"].isin(
        selected_expertise
    )
    &
    teachers["TeacherRating"].between(
        rating_filter[0],
        rating_filter[1]
    )
].copy()


filtered_teacher_ids = filtered_teachers[
    "TeacherID"
].tolist()


filtered_analysis = analysis_data[
    analysis_data["TeacherID"].isin(
        filtered_teacher_ids
    )
    &
    analysis_data["CourseCategory"].isin(
        selected_categories
    )
    &
    analysis_data["CourseLevel"].isin(
        selected_levels
    )
].copy()


filtered_instructors = instructor_metrics[
    instructor_metrics["TeacherID"].isin(
        filtered_teacher_ids
    )
].copy()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def correlation_text(value):

    if pd.isna(value):
        return "Not available"

    absolute = abs(value)

    if absolute < 0.20:
        strength = "very weak"

    elif absolute < 0.40:
        strength = "weak"

    elif absolute < 0.60:
        strength = "moderate"

    elif absolute < 0.80:
        strength = "strong"

    else:
        strength = "very strong"

    direction = (
        "positive"
        if value >= 0
        else "negative"
    )

    return (
        f"{strength} {direction} relationship "
        f"({value:.2f})"
    )


def safe_mean(series):

    if len(series) == 0:
        return 0

    return series.mean()


def stamp_badge(text):
    st.markdown(
        f'<div class="stamp">{text}</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# PERSISTENT HERO
# ============================================================

hero(
    "EduPro Instructor Ledger",
    "The faculty register — instructor performance and course quality, entered and evaluated",
)


# ============================================================
# OVERVIEW PAGE
# ============================================================

if page == "Overview":

    page_header("Platform Overview", "A snapshot of learners, instructors, courses and revenue")

    st.info(
        "This ledger tracks instructor effectiveness, "
        "course quality, teaching experience, expertise, "
        "and enrollment impact using EduPro platform data."
    )

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    section_header("Platform Overview")

    kpi_row([
        {"label": "Learners", "value": f"{len(users):,}"},
        {"label": "Instructors", "value": f"{len(teachers):,}"},
        {"label": "Courses", "value": f"{len(courses):,}"},
        {"label": "Transactions", "value": f"{len(transactions):,}"},
        {"label": "Avg Teacher Rating", "value": f"{teachers['TeacherRating'].mean():.2f}"},
    ])

    st.write("")

    # --------------------------------------------------------
    # SECOND KPI ROW
    # --------------------------------------------------------

    kpi_row([
        {"label": "Avg Course Rating", "value": f"{courses['CourseRating'].mean():.2f}"},
        {"label": "Avg Experience", "value": f"{teachers['YearsOfExperience'].mean():.1f} yrs"},
        {"label": "Total Revenue", "value": f"${transactions['Amount'].sum():,.0f}"},
        {"label": "Courses per Instructor", "value": f"{courses.shape[0] / max(len(teachers), 1):.1f}"},
    ])

    # --------------------------------------------------------
    # PROJECT OBJECTIVE
    # --------------------------------------------------------

    st.write("")
    section_header("Project Objective")

    st.write(
        "EduPro requires a structured, data-driven framework "
        "to evaluate instructor effectiveness and course quality. "
        "This system integrates instructor, course, and "
        "transaction data to identify high-performing instructors, "
        "evaluate course quality, study the influence of experience, "
        "and understand the relationship between instructor quality "
        "and learner demand."
    )

    # --------------------------------------------------------
    # QUICK INSIGHTS
    # --------------------------------------------------------

    section_header("Quick Insights")

    top_instructor = (
        instructor_metrics
        .sort_values(
            "OverallScore",
            ascending=False
        )
        .iloc[0]
    )

    top_expertise = (
        expertise_analysis
        .sort_values(
            "AverageTeacherRating",
            ascending=False
        )
        .iloc[0]
    )

    top_category = (
        category_quality
        .sort_values(
            "AverageCourseRating",
            ascending=False
        )
        .iloc[0]
    )

    stamp_badge(f"Honor roll: {top_instructor['TeacherName']}")

    kpi_row([
        {"label": "Top Instructor", "value": top_instructor["TeacherName"], "tone": "ink"},
        {"label": "Top Expertise", "value": top_expertise["Expertise"], "tone": "pen"},
        {"label": "Top Course Category", "value": top_category["CourseCategory"], "tone": "brass"},
    ])

    # --------------------------------------------------------
    # RATING DISTRIBUTION
    # --------------------------------------------------------

    st.write("")
    section_header("Instructor Rating Distribution")

    rating_distribution = (
        teachers[
            "TeacherRating"
        ]
        .round(1)
        .value_counts()
        .sort_index()
        .reset_index()
    )

    rating_distribution.columns = [
        "Rating",
        "Instructors"
    ]

    rating_chart = (
        alt.Chart(rating_distribution)
        .mark_bar(
            cornerRadiusTopLeft=2,
            cornerRadiusTopRight=2
        )
        .encode(
            x=alt.X(
                "Rating:Q",
                title="Teacher Rating"
            ),
            y=alt.Y(
                "Instructors:Q",
                title="Number of Instructors"
            ),
            tooltip=[
                "Rating",
                "Instructors"
            ]
        )
        .properties(
            height=350
        )
    )

    st.altair_chart(
        rating_chart,
        use_container_width=True
    )


# ============================================================
# INSTRUCTOR PERFORMANCE PAGE
# ============================================================

elif page == "Instructor Performance":

    page_header("Instructor Performance", "Evaluate instructor effectiveness, consistency, experience, and enrollment impact")

    # --------------------------------------------------------
    # FILTERED KPIs
    # --------------------------------------------------------

    kpi_row([
        {"label": "Instructors", "value": f"{len(filtered_instructors):,}"},
        {"label": "Avg Teacher Rating", "value": f"{safe_mean(filtered_instructors['TeacherRating']):.2f}"},
        {"label": "Avg Course Rating", "value": f"{safe_mean(filtered_instructors['AverageCourseRating']):.2f}"},
        {"label": "Avg Enrollments", "value": f"{safe_mean(filtered_instructors['TotalEnrollments']):.1f}"},
        {"label": "Avg Experience", "value": f"{safe_mean(filtered_instructors['YearsOfExperience']):.1f} yrs"},
    ])

    # --------------------------------------------------------
    # LEADERBOARD
    # --------------------------------------------------------

    st.write("")
    section_header("Instructor Performance Leaderboard")

    leaderboard = (
        filtered_instructors
        .sort_values(
            "OverallScore",
            ascending=False
        )
        .copy()
    )

    leaderboard_display = leaderboard[
        [
            "TeacherName",
            "Expertise",
            "YearsOfExperience",
            "TeacherRating",
            "AverageCourseRating",
            "TotalEnrollments",
            "RatingConsistencyIndex",
            "OverallScore"
        ]
    ].copy()

    leaderboard_display.columns = [
        "Instructor",
        "Expertise",
        "Experience",
        "Teacher Rating",
        "Course Rating",
        "Enrollments",
        "Consistency Index",
        "Overall Score"
    ]

    leaderboard_display.insert(
        0,
        "Rank",
        range(
            1,
            len(leaderboard_display) + 1
        )
    )

    st.dataframe(
        leaderboard_display,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # EXPERIENCE VS RATING
    # --------------------------------------------------------

    st.write("")
    section_header("Experience vs Instructor Rating")

    experience_data = filtered_teachers[
        [
            "TeacherName",
            "YearsOfExperience",
            "TeacherRating",
            "Expertise"
        ]
    ].dropna()

    experience_corr = (
        experience_data[
            "YearsOfExperience"
        ].corr(
            experience_data[
                "TeacherRating"
            ]
        )
    )

    st.caption(
        "Correlation: "
        + correlation_text(experience_corr)
    )

    experience_chart = (
        alt.Chart(experience_data)
        .mark_circle(
            size=90,
            opacity=0.75
        )
        .encode(
            x=alt.X(
                "YearsOfExperience:Q",
                title="Years of Experience"
            ),
            y=alt.Y(
                "TeacherRating:Q",
                title="Teacher Rating"
            ),
            tooltip=[
                "TeacherName",
                "Expertise",
                "YearsOfExperience",
                "TeacherRating"
            ]
        )
        .properties(
            height=400
        )
        .interactive()
    )

    st.altair_chart(
        experience_chart,
        use_container_width=True
    )


    # --------------------------------------------------------
    # ENROLLMENT IMPACT
    # --------------------------------------------------------

    st.write("")
    section_header("Instructor Enrollment Impact")

    enrollment_data = (
        filtered_instructors[
            [
                "TeacherName",
                "TotalEnrollments",
                "TeacherRating"
            ]
        ]
        .sort_values(
            "TotalEnrollments",
            ascending=False
        )
        .head(15)
    )

    enrollment_chart = (
        alt.Chart(enrollment_data)
        .mark_bar(
            cornerRadiusEnd=2
        )
        .encode(
            x=alt.X(
                "TotalEnrollments:Q",
                title="Total Enrollments"
            ),
            y=alt.Y(
                "TeacherName:N",
                sort="-x",
                title="Instructor"
            ),
            tooltip=[
                "TeacherName",
                "TotalEnrollments",
                "TeacherRating"
            ]
        )
        .properties(
            height=450
        )
    )

    st.altair_chart(
        enrollment_chart,
        use_container_width=True
    )


    # --------------------------------------------------------
    # TOP / LOW PERFORMERS
    # --------------------------------------------------------

    st.write("")
    left, right = st.columns(2)

    with left:

        section_header("Top Performing Instructors")

        st.dataframe(
            leaderboard_display.head(5),
            use_container_width=True,
            hide_index=True
        )

    with right:

        section_header("Instructors Requiring Attention")

        low_performers = (
            filtered_instructors
            .sort_values(
                "OverallScore",
                ascending=True
            )
            .head(5)
        )

        low_display = low_performers[
            [
                "TeacherName",
                "Expertise",
                "TeacherRating",
                "AverageCourseRating",
                "OverallScore"
            ]
        ].copy()

        low_display.columns = [
            "Instructor",
            "Expertise",
            "Teacher Rating",
            "Course Rating",
            "Overall Score"
        ]

        st.dataframe(
            low_display,
            use_container_width=True,
            hide_index=True
        )


    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    st.write("")
    st.download_button(
        "Download Instructor Metrics",
        filtered_instructors.to_csv(
            index=False
        ),
        "instructor_performance.csv",
        "text/csv"
    )


# ============================================================
# COURSE QUALITY PAGE
# ============================================================

elif page == "Course Quality":

    page_header("Course Quality Evaluation", "Evaluate course quality across categories, levels, instructors, and learner demand")

    # --------------------------------------------------------
    # COURSE KPIs
    # --------------------------------------------------------

    filtered_courses = filtered_analysis[
        "CourseID"
    ].nunique()

    filtered_transactions = len(
        filtered_analysis
    )

    avg_course_rating = (
        filtered_analysis[
            "CourseRating"
        ].mean()
        if filtered_transactions > 0
        else 0
    )

    avg_course_price = (
        filtered_analysis[
            "CoursePrice"
        ].mean()
        if filtered_transactions > 0
        else 0
    )

    kpi_row([
        {"label": "Courses in View", "value": f"{filtered_courses:,}"},
        {"label": "Transactions", "value": f"{filtered_transactions:,}"},
        {"label": "Avg Course Rating", "value": f"{avg_course_rating:.2f}"},
        {"label": "Avg Course Price", "value": f"${avg_course_price:,.2f}"},
    ])

    # --------------------------------------------------------
    # CATEGORY QUALITY
    # --------------------------------------------------------

    st.write("")
    section_header("Course Quality by Category")

    category_filtered = (
        filtered_analysis
        .groupby("CourseCategory")
        .agg(
            AverageCourseRating=(
                "CourseRating",
                "mean"
            ),
            Courses=(
                "CourseID",
                "nunique"
            ),
            Enrollments=(
                "TransactionID",
                "count"
            )
        )
        .reset_index()
    )

    category_filtered[
        "AverageCourseRating"
    ] = category_filtered[
        "AverageCourseRating"
    ].round(2)

    category_chart = (
        alt.Chart(category_filtered)
        .mark_bar(
            cornerRadiusTopLeft=2,
            cornerRadiusTopRight=2
        )
        .encode(
            x=alt.X(
                "CourseCategory:N",
                sort="-y",
                title="Course Category"
            ),
            y=alt.Y(
                "AverageCourseRating:Q",
                title="Average Course Rating",
                scale=alt.Scale(
                    domain=[0, 5]
                )
            ),
            tooltip=[
                "CourseCategory",
                "AverageCourseRating",
                "Courses",
                "Enrollments"
            ]
        )
        .properties(
            height=400
        )
    )

    st.altair_chart(
        category_chart,
        use_container_width=True
    )


    # --------------------------------------------------------
    # COURSE LEVEL
    # --------------------------------------------------------

    st.write("")
    section_header("Course Quality by Level")

    level_filtered = (
        filtered_analysis
        .groupby("CourseLevel")
        .agg(
            AverageCourseRating=(
                "CourseRating",
                "mean"
            ),
            Courses=(
                "CourseID",
                "nunique"
            ),
            Enrollments=(
                "TransactionID",
                "count"
            )
        )
        .reset_index()
    )

    level_filtered[
        "AverageCourseRating"
    ] = level_filtered[
        "AverageCourseRating"
    ].round(2)

    level_chart = (
        alt.Chart(level_filtered)
        .mark_bar(
            cornerRadiusTopLeft=2,
            cornerRadiusTopRight=2
        )
        .encode(
            x=alt.X(
                "CourseLevel:N",
                title="Course Level"
            ),
            y=alt.Y(
                "AverageCourseRating:Q",
                title="Average Course Rating",
                scale=alt.Scale(
                    domain=[0, 5]
                )
            ),
            tooltip=[
                "CourseLevel",
                "AverageCourseRating",
                "Courses",
                "Enrollments"
            ]
        )
        .properties(
            height=350
        )
    )

    st.altair_chart(
        level_chart,
        use_container_width=True
    )


    # --------------------------------------------------------
    # CATEGORY × LEVEL HEATMAP
    # --------------------------------------------------------

    st.write("")
    section_header("Course Quality Heatmap")

    heatmap_data = (
        filtered_analysis
        .groupby(
            [
                "CourseCategory",
                "CourseLevel"
            ]
        )
        .agg(
            AverageRating=(
                "CourseRating",
                "mean"
            ),
            Courses=(
                "CourseID",
                "nunique"
            )
        )
        .reset_index()
    )

    heatmap_data[
        "AverageRating"
    ] = heatmap_data[
        "AverageRating"
    ].round(2)

    heatmap = (
        alt.Chart(heatmap_data)
        .mark_rect(
            cornerRadius=2
        )
        .encode(
            x=alt.X(
                "CourseLevel:N",
                title="Course Level"
            ),
            y=alt.Y(
                "CourseCategory:N",
                title="Course Category"
            ),
            color=alt.Color(
                "AverageRating:Q",
                title="Rating",
                scale=alt.Scale(
                    domain=[0, 5],
                    scheme="blues"
                )
            ),
            tooltip=[
                "CourseCategory",
                "CourseLevel",
                "AverageRating",
                "Courses"
            ]
        )
        .properties(
            height=450
        )
    )

    st.altair_chart(
        heatmap,
        use_container_width=True
    )


    # --------------------------------------------------------
    # TOP COURSES
    # --------------------------------------------------------

    st.write("")
    section_header("Highest Rated Courses")

    top_courses = (
        filtered_analysis
        .groupby(
            [
                "CourseID",
                "CourseName",
                "CourseCategory",
                "CourseLevel",
                "TeacherName"
            ]
        )
        .agg(
            CourseRating=(
                "CourseRating",
                "mean"
            ),
            Enrollments=(
                "TransactionID",
                "count"
            ),
            Revenue=(
                "Amount",
                "sum"
            )
        )
        .reset_index()
        .sort_values(
            "CourseRating",
            ascending=False
        )
        .head(10)
    )

    top_courses[
        "CourseRating"
    ] = top_courses[
        "CourseRating"
    ].round(2)

    top_courses[
        "Revenue"
    ] = top_courses[
        "Revenue"
    ].round(2)

    st.dataframe(
        top_courses,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # COURSE PERFORMANCE TABLE
    # --------------------------------------------------------

    st.write("")
    section_header("Complete Course Performance")

    complete_courses = (
        filtered_analysis
        .groupby(
            [
                "CourseID",
                "CourseName",
                "CourseCategory",
                "CourseLevel",
                "TeacherName"
            ]
        )
        .agg(
            CourseRating=(
                "CourseRating",
                "mean"
            ),
            Enrollments=(
                "TransactionID",
                "count"
            ),
            Revenue=(
                "Amount",
                "sum"
            )
        )
        .reset_index()
        .sort_values(
            "CourseRating",
            ascending=False
        )
    )

    st.dataframe(
        complete_courses,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Course Analysis",
        complete_courses.to_csv(
            index=False
        ),
        "course_quality_analysis.csv",
        "text/csv"
    )


# ============================================================
# EXPERTISE ANALYSIS PAGE
# ============================================================

elif page == "Expertise Analysis":

    page_header("Expertise-Based Performance", "Compare instructor quality, experience, course ratings, and learner demand across expertise areas")

    # --------------------------------------------------------
    # EXPERTISE DATA
    # --------------------------------------------------------

    expertise_filtered = (
        filtered_instructors
        .groupby("Expertise")
        .agg(
            Instructors=(
                "TeacherID",
                "nunique"
            ),
            AverageTeacherRating=(
                "TeacherRating",
                "mean"
            ),
            AverageCourseRating=(
                "AverageCourseRating",
                "mean"
            ),
            AverageExperience=(
                "YearsOfExperience",
                "mean"
            ),
            TotalEnrollments=(
                "TotalEnrollments",
                "sum"
            ),
            AverageConsistency=(
                "RatingConsistencyIndex",
                "mean"
            )
        )
        .reset_index()
    )

    expertise_filtered[
        [
            "AverageTeacherRating",
            "AverageCourseRating",
            "AverageExperience",
            "AverageConsistency"
        ]
    ] = expertise_filtered[
        [
            "AverageTeacherRating",
            "AverageCourseRating",
            "AverageExperience",
            "AverageConsistency"
        ]
    ].round(2)


    # --------------------------------------------------------
    # TOP EXPERTISE
    # --------------------------------------------------------

    if len(expertise_filtered) > 0:

        best_expertise = expertise_filtered.sort_values(
            "AverageTeacherRating",
            ascending=False
        ).iloc[0]

        best_course_expertise = expertise_filtered.sort_values(
            "AverageCourseRating",
            ascending=False
        ).iloc[0]

        best_enrollment_expertise = expertise_filtered.sort_values(
            "TotalEnrollments",
            ascending=False
        ).iloc[0]

    else:

        best_expertise = None
        best_course_expertise = None
        best_enrollment_expertise = None


    kpi_items = []

    if best_expertise is not None:
        kpi_items.append({
            "label": "Highest Teacher Rating",
            "value": best_expertise["Expertise"],
            "note": f"Rating: {best_expertise['AverageTeacherRating']:.2f}",
            "tone": "ink",
        })

    if best_course_expertise is not None:
        kpi_items.append({
            "label": "Highest Course Quality",
            "value": best_course_expertise["Expertise"],
            "note": f"Rating: {best_course_expertise['AverageCourseRating']:.2f}",
            "tone": "pen",
        })

    if best_enrollment_expertise is not None:
        kpi_items.append({
            "label": "Highest Enrollment",
            "value": best_enrollment_expertise["Expertise"],
            "note": f"Enrollments: {int(best_enrollment_expertise['TotalEnrollments']):,}",
            "tone": "brass",
        })

    if kpi_items:
        kpi_row(kpi_items)


    # --------------------------------------------------------
    # TEACHER RATING BY EXPERTISE
    # --------------------------------------------------------

    st.write("")
    section_header("Average Teacher Rating by Expertise")

    expertise_rating_chart = (
        alt.Chart(expertise_filtered)
        .mark_bar(
            cornerRadiusTopLeft=2,
            cornerRadiusTopRight=2
        )
        .encode(
            x=alt.X(
                "Expertise:N",
                sort="-y",
                title="Expertise"
            ),
            y=alt.Y(
                "AverageTeacherRating:Q",
                title="Average Teacher Rating",
                scale=alt.Scale(
                    domain=[0, 5]
                )
            ),
            tooltip=[
                "Expertise",
                "Instructors",
                "AverageTeacherRating",
                "AverageExperience",
                "TotalEnrollments"
            ]
        )
        .properties(
            height=400
        )
    )

    st.altair_chart(
        expertise_rating_chart,
        use_container_width=True
    )


    # --------------------------------------------------------
    # TEACHER VS COURSE QUALITY
    # --------------------------------------------------------

    st.write("")
    section_header("Teacher Quality vs Course Quality by Expertise")

    expertise_scatter = (
        alt.Chart(expertise_filtered)
        .mark_circle(
            size=180
        )
        .encode(
            x=alt.X(
                "AverageTeacherRating:Q",
                title="Average Teacher Rating",
                scale=alt.Scale(
                    domain=[0, 5]
                )
            ),
            y=alt.Y(
                "AverageCourseRating:Q",
                title="Average Course Rating",
                scale=alt.Scale(
                    domain=[0, 5]
                )
            ),
            size=alt.Size(
                "TotalEnrollments:Q",
                title="Enrollments"
            ),
            tooltip=[
                "Expertise",
                "AverageTeacherRating",
                "AverageCourseRating",
                "TotalEnrollments"
            ]
        )
        .properties(
            height=450
        )
        .interactive()
    )

    st.altair_chart(
        expertise_scatter,
        use_container_width=True
    )


    # --------------------------------------------------------
    # EXPERTISE TABLE
    # --------------------------------------------------------

    st.write("")
    section_header("Expertise Performance Summary")

    st.dataframe(
        expertise_filtered.sort_values(
            "AverageTeacherRating",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Expertise Analysis",
        expertise_filtered.to_csv(
            index=False
        ),
        "expertise_performance.csv",
        "text/csv"
    )


# ============================================================
# ADVANCED ANALYTICS PAGE
# ============================================================

elif page == "Advanced Analytics":

    page_header("Advanced Analytics", "Relationships, KPIs, consistency, experience impact, and data-driven insights")

    # --------------------------------------------------------
    # CORRELATIONS
    # --------------------------------------------------------

    teacher_rating_experience = teachers[
        [
            "YearsOfExperience",
            "TeacherRating"
        ]
    ].dropna()

    experience_corr = (
        teacher_rating_experience[
            "YearsOfExperience"
        ].corr(
            teacher_rating_experience[
                "TeacherRating"
            ]
        )
    )


    teacher_course = filtered_analysis[
        [
            "TeacherRating",
            "CourseRating"
        ]
    ].dropna()

    teacher_course_corr = (
        teacher_course[
            "TeacherRating"
        ].corr(
            teacher_course[
                "CourseRating"
            ]
        )
    )


    enrollment_corr_data = filtered_instructors[
        [
            "TeacherRating",
            "TotalEnrollments"
        ]
    ].dropna()

    enrollment_corr = (
        enrollment_corr_data[
            "TeacherRating"
        ].corr(
            enrollment_corr_data[
                "TotalEnrollments"
            ]
        )
    )


    section_header("Key Relationships")

    c1, c2, c3 = st.columns(3)

    with c1:
        kpi_card("Experience ↔ Teacher Rating", f"{experience_corr:.2f}", tone="ink")
        st.caption(correlation_text(experience_corr))

    with c2:
        kpi_card("Teacher Rating ↔ Course Rating", f"{teacher_course_corr:.2f}", tone="pen")
        st.caption(correlation_text(teacher_course_corr))

    with c3:
        kpi_card("Teacher Rating ↔ Enrollment", f"{enrollment_corr:.2f}", tone="brass")
        st.caption(correlation_text(enrollment_corr))


    # --------------------------------------------------------
    # KPI FRAMEWORK
    # --------------------------------------------------------

    st.write("")
    section_header("Key Performance Indicators")

    kpi_table = pd.DataFrame({
        "KPI": [
            "Average Teacher Rating",
            "Average Course Rating",
            "Rating Consistency Index",
            "Experience Impact Score",
            "Enrollment Influence Ratio"
        ],
        "Description": [
            "Overall instructor teaching-quality benchmark",
            "Overall course content-quality benchmark",
            "Measures consistency of course ratings",
            "Combines teaching experience and teacher rating",
            "Compares instructor enrollment volume with platform average"
        ],
        "Current Value": [
            teachers[
                "TeacherRating"
            ].mean(),

            courses[
                "CourseRating"
            ].mean(),

            filtered_instructors[
                "RatingConsistencyIndex"
            ].mean(),

            filtered_instructors[
                "ExperienceImpactScore"
            ].mean(),

            filtered_instructors[
                "EnrollmentInfluenceRatio"
            ].mean()
        ]
    })

    kpi_table[
        "Current Value"
    ] = kpi_table[
        "Current Value"
    ].round(2)

    st.dataframe(
        kpi_table,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # CORRELATION MATRIX
    # --------------------------------------------------------

    st.write("")
    section_header("Correlation Matrix")

    correlation_columns = [
        "Age",
        "YearsOfExperience",
        "TeacherRating",
        "CourseRating",
        "CoursePrice",
        "CourseDuration",
        "Amount"
    ]

    correlation_data = filtered_analysis[
        [
            col
            for col in correlation_columns
            if col in filtered_analysis.columns
        ]
    ].copy()

    correlation_matrix = correlation_data.corr(
        numeric_only=True
    )

    if len(correlation_matrix.columns) > 0:

        correlation_long = (
            correlation_matrix
            .reset_index()
            .melt(
                id_vars="index",
                var_name="Variable",
                value_name="Correlation"
            )
        )

        correlation_long = correlation_long.rename(
            columns={
                "index": "Variable1"
            }
        )

        correlation_heatmap = (
            alt.Chart(correlation_long)
            .mark_rect()
            .encode(
                x=alt.X(
                    "Variable:N",
                    title=None
                ),
                y=alt.Y(
                    "Variable1:N",
                    title=None
                ),
                color=alt.Color(
                    "Correlation:Q",
                    title="Correlation",
                    scale=alt.Scale(
                        domain=[-1, 1],
                        scheme="redblue"
                    )
                ),
                tooltip=[
                    "Variable1",
                    "Variable",
                    alt.Tooltip(
                        "Correlation:Q",
                        format=".2f"
                    )
                ]
            )
            .properties(
                height=500
            )
        )

        st.altair_chart(
            correlation_heatmap,
            use_container_width=True
        )


    # --------------------------------------------------------
    # EXPERIENCE GROUP ANALYSIS
    # --------------------------------------------------------

    st.write("")
    section_header("Experience Group Performance")

    experience_df = filtered_teachers.copy()

    experience_df[
        "ExperienceGroup"
    ] = pd.cut(
        experience_df[
            "YearsOfExperience"
        ],
        bins=[
            -1,
            5,
            10,
            20,
            np.inf
        ],
        labels=[
            "0–5 Years",
            "6–10 Years",
            "11–20 Years",
            "20+ Years"
        ]
    )

    experience_groups = (
        experience_df
        .groupby(
            "ExperienceGroup",
            observed=False
        )
        .agg(
            Instructors=(
                "TeacherID",
                "count"
            ),
            AverageRating=(
                "TeacherRating",
                "mean"
            ),
            AverageExperience=(
                "YearsOfExperience",
                "mean"
            )
        )
        .reset_index()
    )

    experience_groups[
        [
            "AverageRating",
            "AverageExperience"
        ]
    ] = experience_groups[
        [
            "AverageRating",
            "AverageExperience"
        ]
    ].round(2)

    st.dataframe(
        experience_groups,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # INSIGHT CARDS
    # --------------------------------------------------------

    st.write("")
    section_header("Data-Driven Insights")

    if len(filtered_instructors) > 0:

        top = filtered_instructors.sort_values(
            "OverallScore",
            ascending=False
        ).iloc[0]

        low = filtered_instructors.sort_values(
            "OverallScore",
            ascending=True
        ).iloc[0]

        highest_enrollment = filtered_instructors.sort_values(
            "TotalEnrollments",
            ascending=False
        ).iloc[0]

        highest_consistency = filtered_instructors.sort_values(
            "RatingConsistencyIndex",
            ascending=False
        ).iloc[0]

        i1, i2 = st.columns(2)

        with i1:

            st.success(
                f"**Top Overall Instructor**\n\n"
                f"{top['TeacherName']} has the highest "
                f"overall performance score of "
                f"**{top['OverallScore']:.2f}**."
            )

            st.info(
                f"**Highest Enrollment**\n\n"
                f"{highest_enrollment['TeacherName']} "
                f"has **{int(highest_enrollment['TotalEnrollments']):,}** "
                f"enrollments."
            )

        with i2:

            st.warning(
                f"**Lowest Overall Score**\n\n"
                f"{low['TeacherName']} has the lowest "
                f"overall score within the selected view."
            )

            st.info(
                f"**Most Consistent Instructor**\n\n"
                f"{highest_consistency['TeacherName']} "
                f"has a consistency index of "
                f"**{highest_consistency['RatingConsistencyIndex']:.2f}**."
            )


    # --------------------------------------------------------
    # DOWNLOAD EDA SUMMARY
    # --------------------------------------------------------

    st.write("")
    section_header("Export Analysis")

    st.download_button(
        "Download EDA Summary",
        eda_summary.to_csv(
            index=False
        ),
        "eda_summary.csv",
        "text/csv"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()
st.caption("EduPro Instructor Ledger • Instructor Performance & Course Quality Evaluation")