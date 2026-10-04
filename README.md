# Student Academic Performance Analyzer - Advanced

A Flask-based academic management system for storing, analyzing and reporting student performance.

## Features

- Student dashboard
- SQLite database
- Add student
- View students
- Edit student
- Delete student
- Search students
- Filter students by grade
- Automatic total calculation
- Automatic percentage calculation
- Automatic grade calculation
- Performance classification
- Attendance monitoring
- Highest subject detection
- Lowest subject detection
- Top performers
- Grade distribution chart
- Subject average chart
- Individual student report
- Print report
- CSV export
- Form validation
- Responsive design

## Project Structure

student_academic_performance_advanced/

├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add_student.html
│   ├── edit_student.html
│   ├── students.html
│   └── report.html
│
└── static/
    └── style.css

## Installation

Open PowerShell inside the project folder.

Create virtual environment:

python -m venv .venv

Activate virtual environment:

.\.venv\Scripts\Activate.ps1

Install Flask:

python -m pip install -r requirements.txt

## Run Project

python app.py

Open browser:

http://127.0.0.1:5000

## Routes

/ 
Dashboard

/students
Student records

/add
Add student

/edit/<id>
Edit student

/report/<id>
Student report

/delete/<id>
Delete student

/export
Export CSV

## Technology Stack

Frontend:
HTML5
CSS3
JavaScript
Chart.js

Backend:
Python
Flask

Database:
SQLite

Export:
CSV

## Database

The application automatically creates:

students.db

The database contains student information, marks, attendance, percentage, grade and performance.

## Architecture

Browser
    |
    v
HTML / CSS / JavaScript
    |
    v
Flask Application
    |
    v
Business Logic
    |
    v
SQLite Database
    |
    v
Reports / Dashboard / CSV Export