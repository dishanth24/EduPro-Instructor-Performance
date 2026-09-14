# EduPro – Instructor Performance and Course Quality Evaluation

## 📌 Project Overview

EduPro – Instructor Performance and Course Quality Evaluation is a data analytics project designed to evaluate instructor effectiveness, course quality, teaching experience, expertise areas, and learner enrollment patterns on the EduPro online learning platform.

The project integrates instructor, course, learner, and transaction data to provide a structured framework for understanding instructor performance and course quality.

An interactive Streamlit dashboard is developed to allow users to explore instructor and course performance using filters, KPIs, charts, and analytical insights.

---

## 🎯 Objectives

The main objectives of this project are:

- Analyze the overall distribution of instructor ratings.
- Evaluate the relationship between teaching experience and instructor ratings.
- Analyze the relationship between instructor ratings and course ratings.
- Identify high-performing and low-performing instructors.
- Compare course quality across different categories and levels.
- Analyze instructor performance across different expertise areas.
- Examine the relationship between instructor ratings and enrollment volume.
- Provide interactive analytics through a Streamlit dashboard.
- Generate data-driven insights and recommendations for EduPro stakeholders.

---

## ❓ Problem Statement

EduPro needs a structured and data-driven approach to evaluate instructor effectiveness and course quality.

The platform needs to identify:

- Which instructors consistently deliver high-quality courses?
- Does teaching experience translate into better instructor ratings?
- Is instructor quality related to course quality?
- Which expertise areas consistently perform well?
- Are highly rated instructors associated with higher enrollment?
- How evenly is instructor performance distributed across the platform?

Without systematic analysis, instructor evaluation can remain subjective and fragmented.

This project addresses the problem by integrating instructor, course, learner, and transaction data and transforming it into meaningful performance insights through exploratory data analysis and an interactive dashboard.

---

## 📊 Dataset

The project uses the **EduPro Online Platform** dataset provided in Excel format.

### Dataset Sheets

The workbook contains the following major sheets:

### Users

Contains learner-related information used for platform-level analysis.

### Teachers

| Field | Description |
|---|---|
| TeacherID | Unique identifier for each instructor |
| TeacherName | Name of the instructor |
| Age | Age of the instructor |
| Gender | Gender of the instructor |
| Expertise | Instructor's area of expertise |
| YearsOfExperience | Number of years of teaching experience |
| TeacherRating | Rating assigned to the instructor |

### Courses

| Field | Description |
|---|---|
| CourseID | Unique identifier for each course |
| CourseName | Name of the course |
| CourseCategory | Category of the course |
| CourseLevel | Difficulty level of the course |
| CourseRating | Rating assigned to the course |

### Transactions

Contains transaction/enrollment information connecting learners, instructors, and courses.

The transaction data is used to analyze enrollment volume and instructor influence.

---

## 🔗 Data Integration

The project connects the datasets using `TeacherID` and `CourseID`.

```text
Teachers
    │
    │ TeacherID
    ▼
Transactions
    │
    │ CourseID
    ▼
Courses
