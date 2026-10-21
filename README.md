# 🎓 Student Academic Performance Analyzer

**A Web-Based Student Records Management and Academic Performance Analysis System**

The Student Academic Performance Analyzer is a Python-based web application designed to manage student academic records and analyze their performance across multiple subjects. It provides a structured way to store student information, record marks and attendance, calculate academic results, and support performance evaluation.

The project combines web development, database management, and data analysis to demonstrate how technology can simplify academic record management and help identify areas where students may need improvement.

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Objectives](#-objectives)
- [Key Features](#-key-features)
- [Technology Stack](#️-technology-stack)
- [Project Architecture](#️-project-architecture)
- [Project Structure](#-project-structure)
- [Student Information and Academic Data](#-student-information-and-academic-data)
- [Performance Analysis](#-performance-analysis)
- [Database Design](#️-database-design)
- [Installation and Setup](#-installation-and-setup)
- [How to Run the Project](#️-how-to-run-the-project)
- [Application Workflow](#-application-workflow)
- [API and Application Routes](#-api-and-application-routes)
- [Testing and Validation](#-testing-and-validation)
- [Security and Data Integrity](#-security-and-data-integrity)
- [Use Cases](#-use-cases)
- [Limitations](#️-limitations)
- [Future Enhancements](#-future-enhancements)
- [Learning Outcomes](#-learning-outcomes)
- [Author](#-author)
- [License](#-license)

---

## 📖 Project Overview

Educational institutions handle academic information such as student details, subject marks, attendance, grades, and examination results. Managing these records manually can be time-consuming and make it difficult to evaluate academic performance consistently.

The Student Academic Performance Analyzer provides a web-based approach to organizing student records and evaluating academic results.

The application uses **Flask** to handle web requests, **SQLite** to store student information, and Python to process academic data.

The system is designed around five academic subjects:

- Mathematics
- Python Programming
- Data Structures and Algorithms (DSA)
- Database Management Systems (DBMS)
- Computer Networks

It also records student attendance and basic identifying information to support academic evaluation.

### Project Details

| Attribute | Description |
|---|---|
| Project Name | Student Academic Performance Analyzer |
| Project Type | Web Application |
| Domain | Education Technology |
| Backend | Python and Flask |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Primary Purpose | Student record management and academic performance analysis |
| Database File | `students.db` |
| Application Entry Point | `app.py` |

---

## 🎯 Objectives

The primary objectives of this project are:

1. **Digitize student records:** Maintain student information and academic results in a structured database.
2. **Automate calculations:** Calculate total marks, percentages, and grades using program logic.
3. **Analyze academic performance:** Evaluate marks across different subjects.
4. **Track attendance:** Store attendance information alongside academic records.
5. **Improve accessibility:** Provide a web interface for interacting with student data.
6. **Reduce manual effort:** Minimize repetitive calculations and record-management tasks.
7. **Support academic decisions:** Help users identify subjects that may require additional attention.

---

## ✨ Key Features

### 1. Student Record Management

The system is designed to maintain student details, including:

- Student name
- Roll number
- Class or academic group
- Subject-wise marks
- Attendance information

### 2. Academic Marks Management

The application records marks for the following subjects:

- Mathematics
- Python Programming
- Data Structures and Algorithms
- Database Management Systems
- Computer Networks

These marks form the basis for academic calculations and subject-wise performance evaluation.

### 3. Automatic Performance Calculation

The system can process recorded marks to calculate academic results, including:

- Total marks
- Average marks
- Percentage
- Grade, according to the grading rules implemented in the application

The exact grading thresholds depend on the application's implementation.

### 4. Attendance Tracking

Attendance information can be stored with student records and used to review attendance alongside academic performance.

### 5. Database-Driven Application

SQLite provides persistent storage for student records. Data can remain available after the Flask application is stopped and restarted, provided the database file is preserved.

### 6. Web-Based Interface

The frontend uses HTML, CSS, and JavaScript to provide the interface, while Flask processes requests and communicates with the database.

### 7. Academic Performance Evaluation

Recorded marks can be compared across subjects to help identify stronger areas and subjects where further study may be beneficial.

> Feature availability depends on the corresponding implementation in the current source code. Advanced features such as authentication, PDF report generation, live charts, and predictive machine learning are not assumed to be included in the base version.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and academic calculations |
| Flask | Backend web framework |
| SQLite | Persistent student record storage |
| HTML5 | Webpage structure |
| CSS3 | Styling and layout |
| JavaScript | Client-side interactions |
| Jinja2 | Dynamic HTML rendering through Flask |
| Git | Version control |
| GitHub | Source code hosting |

### Why These Technologies?

**Python:** Provides readable code for data processing and academic calculations.

**Flask:** Connects the frontend with backend logic through routes and request handling.

**SQLite:** Offers a lightweight relational database without requiring a separate database server.

**HTML, CSS, and JavaScript:** Form the presentation layer of the web application.

---

## 🏗️ Project Architecture

The application follows a basic three-layer architecture.

```text
┌──────────────────────────────┐
│        Presentation Layer    │
│                              │
│     HTML + CSS + JavaScript  │
│      User Interface          │
└──────────────┬───────────────┘
               │ HTTP Requests
               ▼
┌──────────────────────────────┐
│        Application Layer     │
│                              │
│          Flask + Python      │
│  Validation and Calculations │
│      Academic Processing     │
└──────────────┬───────────────┘
               │ Database Queries
               ▼
┌──────────────────────────────┐
│          Data Layer          │
│                              │
│           SQLite             │
│         students.db          │
│                              │
└──────────────────────────────┘
```

### Architecture Explanation

1. **Presentation layer:** Displays student forms, records, and results.
2. **Application layer:** Receives requests, validates inputs, performs calculations, and coordinates database operations.
3. **Data layer:** Stores student information and academic records in SQLite.

This separation makes the application easier to understand, maintain, and extend.

---

## 📁 Project Structure

The core project is located in:

```text
student_academic_performance_advanced/
│
├── app.py
├── students.db
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add_student.html
│   ├── students.html
│   └── ...
│
├── static/
│   ├── style.css
│   ├── app.js
│   ├── css/
│   └── js/
│
├── requirements.txt
├── README.md
├── .gitignore
└── .venv/
```

**Important:** This is a representative structure. Keep the actual filenames and folders already present in your project; the names of individual templates may differ.

### Important Files and Directories

| File or Directory | Responsibility |
|---|---|
| `app.py` | Flask application, routes, and backend logic |
| `students.db` | SQLite database containing student records |
| `templates/` | HTML templates rendered by Flask |
| `static/` | CSS, JavaScript, and other static assets |
| `requirements.txt` | Python dependencies required by the application |
| `README.md` | Project documentation |
| `.gitignore` | Specifies files Git should ignore |
| `.venv/` | Local Python virtual environment |

The `.venv/` directory should generally remain local and should not be committed to GitHub.

---

## 👨‍🎓 Student Information and Academic Data

Each student record is designed around the following fields:

| Field | Description |
|---|---|
| Name | Student's name |
| Roll Number | Student identification number |
| Class | Student's class or academic group |
| Mathematics | Mathematics marks |
| Python | Python Programming marks |
| DSA | Data Structures and Algorithms marks |
| DBMS | Database Management Systems marks |
| Computer Networks | Computer Networks marks |
| Attendance | Student attendance information |

The exact data types, constraints, and field names should match the database schema implemented in `app.py`.

---

## 📊 Performance Analysis

The recorded academic marks provide the foundation for evaluating student performance.

### 1. Total Marks

For five subjects, the total is calculated as:

\[
T = M_1+M_2+M_3+M_4+M_5
\]

Where \(M_1\) through \(M_5\) represent the marks obtained in each subject.

### 2. Average Marks

\[
\text{Average}=\frac{T}{5}
\]

### 3. Percentage

If each subject has a maximum of 100 marks:

\[
\text{Percentage}=\frac{T}{500}\times100
\]

If the maximum marks differ, the percentage should use the actual total maximum marks.

### 4. Grade Calculation

Grades can be assigned according to predefined percentage ranges. For example, an institution may define its own rules for A, B, C, and other grades.

The grading thresholds must be consistent with the rules implemented in the application and the relevant academic policy.

### 5. Subject-Wise Evaluation

Comparing marks across the five subjects can help identify:

- Subjects in which a student performs relatively well.
- Subjects that may require additional practice.
- Differences between subject-wise results.
- Changes in academic performance over time, if historical records are available.

These calculations are intended to support academic review, not to make definitive judgments about a student's ability.

---

## 🗄️ Database Design

The application uses SQLite for relational data storage.

**Database file:** `students.db`

A student table may contain the following logical fields:

| Column | Purpose |
|---|---|
| `id` | Unique record identifier, if implemented |
| `name` | Student name |
| `roll_no` | Student roll number |
| `class_name` | Class or academic group |
| `maths` | Mathematics marks |
| `python` | Python marks |
| `dsa` | DSA marks |
| `dbms` | DBMS marks |
| `computer_networks` | Computer Networks marks |
| `attendance` | Attendance value |

The names above describe the intended logical schema and should be adjusted to match the actual table definition.

### Database Responsibilities

- Store student records persistently.
- Retrieve records for display.
- Support updates and deletions where implemented.
- Provide data to academic calculations.
- Maintain consistent student information.

SQLite is suitable for a student project because it is lightweight and requires no separate database server.

---

## ⚙️ Installation and Setup

Follow these instructions on Windows using PowerShell.

### Prerequisites

Install the following:

- Python 3
- Visual Studio Code
- Python extension for VS Code
- Git, if you plan to clone or version-control the project

Check the installed Python version:

```powershell
python --version
```

Check pip:

```powershell
python -m pip --version
```

### Step 1: Open the Project Folder

```powershell
cd "C:\Users\ASUS\OneDrive\Attachments\student_academic_performance_advanced"
```

Open the folder in VS Code:

```powershell
code .
```

If the `code` command is unavailable, open VS Code manually and select **File → Open Folder**.

### Step 2: Create a Virtual Environment

If the project already has a working `.venv` folder, you can reuse it.

Otherwise, create one:

```powershell
python -m venv .venv
```

### Step 3: Activate the Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell reports an execution-policy error, use a permitted environment activation method or activate the environment through VS Code's Python interpreter selector.

### Step 4: Install Dependencies

If `requirements.txt` exists:

```powershell
python -m pip install -r requirements.txt
```

If the file is missing, install the known core dependency:

```powershell
python -m pip install Flask
```

SQLite support is included in Python's standard library, so a separate SQLite package is normally unnecessary.

### Step 5: Verify the Project Files

```powershell
Get-ChildItem
```

Confirm that `app.py` exists and that the templates, static assets, and database are in their expected locations.

---

## ▶️ How to Run the Project

Make sure the terminal is inside the project directory and the virtual environment is activated.

Run:

```powershell
python app.py
```

If the application starts successfully, Flask will print a local development URL, typically:

```text
http://127.0.0.1:5000
```

Open that address in your browser.

To stop the development server, press:

```text
Ctrl + C
```

### Troubleshooting

**Problem: `ModuleNotFoundError: No module named 'flask'`**

Install Flask in the currently selected Python environment:

```powershell
python -m pip install Flask
```

**Problem: `TemplateNotFound`**

Check that the required HTML template exists inside the `templates` directory and that its filename matches the name used in `render_template()`.

**Problem: Database errors**

Check that the application is using the intended `students.db` file and that its tables and columns match the SQL queries in the backend.

**Problem: Port 5000 is already in use**

Stop the other application using the port or configure the Flask application to use another available port.

---

## 🔄 Application Workflow

The general workflow of the system is:

1. The user opens the web application.
2. The user enters student details and academic marks.
3. The backend receives and validates the submitted information.
4. Valid records are saved in the SQLite database.
5. The application retrieves student information when required.
6. Python processes the marks to calculate academic results.
7. The results are presented through the web interface.

```text
Start
  |
  v
Open Web Application
  |
  v
Enter Student Information
  |
  v
Validate Input
  |
  +---- Invalid ----> Show Validation Error
  |
  v
Save Student Record
  |
  v
Retrieve Academic Data
  |
  v
Calculate Performance
  |
  v
Display Results
  |
  v
End
```

This flow describes the intended application process; the exact sequence depends on the routes and forms implemented in the current version.

---

## 🌐 API and Application Routes

Flask routes connect browser requests to backend functions.

The application may use routes for:

| Route Purpose | Description |
|---|---|
| Home or dashboard | Displays the main page |
| Add student | Processes new student details |
| Student list | Retrieves and displays records |
| Edit student | Updates a record, if implemented |
| Delete student | Deletes a record, if implemented |
| Performance analysis | Displays calculated academic results |

These are logical route categories, not a verified list of actual endpoint URLs. Refer to the route definitions in `app.py` for the exact paths and HTTP methods.

---

## 🧪 Testing and Validation

The application should be tested with representative student records before being used for real academic data.

### Recommended Test Cases

| Test Case | Expected Behavior |
|---|---|
| Add a valid student | Record is saved successfully |
| Submit a missing name | Validation error is displayed |
| Submit a duplicate roll number | Duplicate is rejected if uniqueness is enforced |
| Enter marks within the permitted range | Values are accepted |
| Enter negative or excessive marks | Invalid values are rejected |
| Calculate percentage | Result matches the calculation formula |
| Retrieve saved records | Correct student information is displayed |
| Restart the application | Saved records remain available |
| Enter invalid attendance | Value is rejected according to the defined rules |

Actual outcomes should be confirmed by running these tests against the application.

---

## 🔐 Security and Data Integrity

For a reliable implementation, consider the following practices:

- Validate all submitted values on the server.
- Use parameterized SQL queries instead of constructing queries from raw user input.
- Apply appropriate database constraints to unique identifiers.
- Keep secret keys and credentials out of source control.
- Use secure session settings if authentication is implemented.
- Avoid exposing sensitive student information publicly.
- Keep backups of important database records.
- Use synthetic student information when sharing screenshots or demonstrations.
- Disable Flask debug mode in production deployments.

**Privacy note:** Student academic information can be sensitive. Access to real records should be limited to authorized users, and any deployed application should use appropriate authentication and access controls.

---

## 🎓 Use Cases

The project can serve as a learning and demonstration application for:

- Students learning Python web development.
- Academic projects involving database management.
- Demonstrations of automated academic calculations.
- Student record-management prototypes.
- Exploring how structured data can support academic analysis.
- Practicing full-stack development fundamentals.

The project is an academic prototype and should not be treated as a certified institutional student information system without further development and validation.

---

## ⚠️ Limitations

The current base project has a defined scope. Depending on its implementation, it may not include:

- User authentication and role-based access.
- Advanced interactive charts.
- PDF or Excel report exports.
- Automatic email notifications.
- Predictive machine-learning models.
- Integration with institutional management systems.
- Multi-user deployment infrastructure.
- Automated historical trend analysis.

These should be considered future enhancements unless they already exist in the source code.

---

## 🚀 Future Enhancements

Potential improvements include:

### 1. Advanced Dashboard

Display student counts, average marks, attendance summaries, and academic performance indicators.

### 2. Interactive Data Visualizations

Add charts to compare subjects, track performance, and present academic statistics.

### 3. Student Performance Prediction

Explore machine-learning models that estimate academic outcomes from suitable historical data. Predictions should be evaluated for accuracy, bias, and limitations before practical use.

### 4. Attendance Analytics

Add attendance summaries and configurable alerts for records that fall below an institution-defined threshold.

### 5. Report Generation

Provide downloadable reports in CSV, Excel, or PDF formats.

### 6. Authentication and Authorization

Introduce secure login and role-based access for authorized staff, teachers, or administrators.

### 7. Improved Database Management

Add stronger validation, database constraints, backup mechanisms, and migration support.

### 8. Deployment

Deploy the application to a suitable hosting platform with production configuration, secure database handling, and appropriate privacy protections.

---

## 📚 Learning Outcomes

This project provides practical experience with:

- Building a web application using Flask.
- Connecting Python applications to SQLite.
- Designing and processing relational records.
- Creating HTML forms and dynamic webpages.
- Implementing input validation.
- Automating academic calculations.
- Organizing backend and frontend code.
- Understanding the relationship between web development and data analysis.
- Using Git and GitHub to manage source code.

---

## 👨‍💻 Author

**Yatharth Jain**

Software Developer | Web Developer | Computer Science Student

GitHub: [yatharthg1727-ctrl](https://github.com/yatharthg1727-ctrl)

Project Repository: [Student Academic Performance Analyzer](https://github.com/yatharthg1727-ctrl/Student-Academic-Performance-Analyzer)

---

## 📄 License

No license has been specified here. If you want others to reuse, modify, or distribute this project, add an appropriate open-source license file, such as the MIT License, after deciding on the intended permissions.

---

⭐ **If you find this project useful, consider starring the repository on GitHub.**

*Built as a practical project to explore web development, database management, and student academic performance analysis.*
