from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file
)

import sqlite3
import csv
import io
import os

from jinja2 import ChoiceLoader, FileSystemLoader


# =========================================================
# APPLICATION CONFIGURATION
# =========================================================

app = Flask(__name__)

app.jinja_loader = ChoiceLoader([
    app.jinja_loader,
    FileSystemLoader(app.root_path)
])

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "student-performance-secret-key"
)

DATABASE = os.path.join(
    app.root_path,
    "students.db"
)


# =========================================================
# CONSTANTS
# =========================================================

SEMESTERS = [
    "Semester 1",
    "Semester 2",
    "Semester 3",
    "Semester 4",
    "Semester 5",
    "Semester 6",
    "Semester 7",
    "Semester 8"
]

DEFAULT_SUBJECTS = [
    "Mathematics",
    "Python",
    "DSA",
    "DBMS",
    "Computer Networks"
]


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


def table_exists(connection, table_name):

    result = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = ?
        """,
        (table_name,)
    ).fetchone()

    return result is not None


# =========================================================
# DATABASE INITIALIZATION + OLD DATABASE MIGRATION
# =========================================================

def init_db():

    connection = get_db()

    # -----------------------------------------------------
    # Check whether old database structure exists
    # -----------------------------------------------------

    if table_exists(connection, "students"):

        columns = [
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(students)"
            ).fetchall()
        ]

        old_database = all(
            column in columns
            for column in [
                "maths",
                "python",
                "dsa",
                "dbms",
                "networks",
                "attendance",
                "total",
                "percentage",
                "grade",
                "performance"
            ]
        )

        if old_database:

            connection.execute(
                """
                ALTER TABLE students
                RENAME TO students_legacy
                """
            )

    # -----------------------------------------------------
    # Students table
    # -----------------------------------------------------

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS students (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            roll_no TEXT NOT NULL UNIQUE,

            class_name TEXT NOT NULL,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # -----------------------------------------------------
    # Academic records table
    # -----------------------------------------------------

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS academic_records (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            student_id INTEGER NOT NULL,

            semester TEXT NOT NULL,

            attendance REAL NOT NULL DEFAULT 0,

            total REAL NOT NULL DEFAULT 0,

            max_total REAL NOT NULL DEFAULT 0,

            percentage REAL NOT NULL DEFAULT 0,

            grade TEXT NOT NULL DEFAULT 'F',

            performance TEXT NOT NULL DEFAULT 'Poor',

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(student_id)
            REFERENCES students(id)
            ON DELETE CASCADE,

            UNIQUE(student_id, semester)
        )
        """
    )

    # -----------------------------------------------------
    # Dynamic subjects table
    # -----------------------------------------------------

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS subjects (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            record_id INTEGER NOT NULL,

            subject_name TEXT NOT NULL,

            marks REAL NOT NULL,

            max_marks REAL NOT NULL,

            FOREIGN KEY(record_id)
            REFERENCES academic_records(id)
            ON DELETE CASCADE
        )
        """
    )

    # -----------------------------------------------------
    # Migrate old database data
    # -----------------------------------------------------

    if table_exists(
        connection,
        "students_legacy"
    ):

        old_students = connection.execute(
            """
            SELECT *
            FROM students_legacy
            """
        ).fetchall()

        for student in old_students:

            connection.execute(
                """
                INSERT OR IGNORE INTO students
                (
                    name,
                    roll_no,
                    class_name,
                    created_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    student["name"],
                    student["roll_no"],
                    student["class_name"],
                    student["created_at"]
                )
            )

            student_id = connection.execute(
                """
                SELECT id
                FROM students
                WHERE roll_no = ?
                """,
                (
                    student["roll_no"],
                )
            ).fetchone()["id"]

            record = connection.execute(
                """
                INSERT INTO academic_records
                (
                    student_id,
                    semester,
                    attendance,
                    total,
                    max_total,
                    percentage,
                    grade,
                    performance
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    student_id,
                    "Semester 1",
                    student["attendance"],
                    student["total"],
                    500,
                    student["percentage"],
                    student["grade"],
                    student["performance"]
                )
            )

            record_id = record.lastrowid

            old_subjects = [
                (
                    "Mathematics",
                    student["maths"]
                ),
                (
                    "Python",
                    student["python"]
                ),
                (
                    "DSA",
                    student["dsa"]
                ),
                (
                    "DBMS",
                    student["dbms"]
                ),
                (
                    "Computer Networks",
                    student["networks"]
                )
            ]

            for subject_name, marks in old_subjects:

                connection.execute(
                    """
                    INSERT INTO subjects
                    (
                        record_id,
                        subject_name,
                        marks,
                        max_marks
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        record_id,
                        subject_name,
                        marks,
                        100
                    )
                )

        connection.execute(
            """
            DROP TABLE students_legacy
            """
        )

    connection.commit()

    connection.close()


# =========================================================
# CALCULATION FUNCTIONS
# =========================================================

def grade_from_percentage(percentage):

    if percentage >= 90:
        return "A+"

    if percentage >= 80:
        return "A"

    if percentage >= 70:
        return "B+"

    if percentage >= 60:
        return "B"

    if percentage >= 50:
        return "C"

    if percentage >= 40:
        return "D"

    return "F"


def performance_from_percentage(percentage):

    if percentage >= 90:
        return "Excellent"

    if percentage >= 75:
        return "Good"

    if percentage >= 60:
        return "Average"

    if percentage >= 40:
        return "Needs Improvement"

    return "Poor"


def calculate_result(subjects):

    total_marks = sum(
        subject["marks"]
        for subject in subjects
    )

    maximum_marks = sum(
        subject["max_marks"]
        for subject in subjects
    )

    if maximum_marks == 0:

        percentage = 0

    else:

        percentage = (
            total_marks /
            maximum_marks
        ) * 100

    percentage = round(
        percentage,
        2
    )

    grade = grade_from_percentage(
        percentage
    )

    performance = performance_from_percentage(
        percentage
    )

    return (
        round(total_marks, 2),
        round(maximum_marks, 2),
        percentage,
        grade,
        performance
    )


# =========================================================
# FORM VALIDATION
# =========================================================

def parse_subjects(form):

    names = form.getlist(
        "subject_name[]"
    )

    marks_list = form.getlist(
        "marks[]"
    )

    max_marks_list = form.getlist(
        "max_marks[]"
    )

    if not names:

        raise ValueError(
            "Please add at least one subject."
        )

    if not (
        len(names)
        ==
        len(marks_list)
        ==
        len(max_marks_list)
    ):

        raise ValueError(
            "Invalid subject information."
        )

    subjects = []

    existing_names = set()

    for name, marks, maximum in zip(
        names,
        marks_list,
        max_marks_list
    ):

        name = name.strip()

        if not name:

            raise ValueError(
                "Subject name cannot be empty."
            )

        normalized_name = name.casefold()

        if normalized_name in existing_names:

            raise ValueError(
                f"Duplicate subject: {name}"
            )

        existing_names.add(
            normalized_name
        )

        try:

            marks = float(marks)
            maximum = float(maximum)

        except ValueError:

            raise ValueError(
                f"Marks for {name} must be valid numbers."
            )

        if maximum <= 0:

            raise ValueError(
                f"Maximum marks for {name} "
                "must be greater than zero."
            )

        if marks < 0 or marks > maximum:

            raise ValueError(
                f"Marks for {name} must be "
                f"between 0 and {maximum:g}."
            )

        subjects.append(
            {
                "name": name,
                "marks": marks,
                "max_marks": maximum
            }
        )

    return subjects


def validate_basic_form(form):

    required = [
        "name",
        "roll_no",
        "class_name"
    ]

    for field in required:

        if not form.get(
            field,
            ""
        ).strip():

            return (
                "Name, roll number and "
                "class/course are required."
            )

    semester = semester_from_form(
        form
    )

    if not semester:

        return (
            "Please select or enter a semester."
        )

    try:

        attendance = float(
            form.get(
                "attendance",
                ""
            )
        )

    except ValueError:

        return (
            "Attendance must be a valid number."
        )

    if attendance < 0 or attendance > 100:

        return (
            "Attendance must be between "
            "0 and 100."
        )

    return None


def semester_from_form(form):

    semester = form.get(
        "semester",
        ""
    ).strip()

    if semester == "Custom":

        return form.get(
            "custom_semester",
            ""
        ).strip()

    return semester


# =========================================================
# GET ACADEMIC RECORD
# =========================================================

def get_record(
    connection,
    record_id
):

    record = connection.execute(
        """
        SELECT

            ar.*,

            s.name,

            s.roll_no,

            s.class_name,

            s.id AS student_id

        FROM academic_records ar

        JOIN students s
        ON s.id = ar.student_id

        WHERE ar.id = ?

        """,
        (
            record_id,
        )
    ).fetchone()

    if not record:

        return None, []

    subjects = connection.execute(
        """
        SELECT *

        FROM subjects

        WHERE record_id = ?

        ORDER BY id
        """,
        (
            record_id,
        )
    ).fetchall()

    return record, subjects


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/")
def index():

    selected_semester = request.args.get(
        "semester",
        ""
    ).strip()

    connection = get_db()

    where = ""

    parameters = []

    if selected_semester:

        where = """
            WHERE ar.semester = ?
        """

        parameters.append(
            selected_semester
        )

    stats = connection.execute(
        f"""
        SELECT

            COUNT(*) AS records,

            COUNT(
                DISTINCT ar.student_id
            ) AS students,

            COALESCE(
                AVG(ar.percentage),
                0
            ) AS avg_percentage,

            COALESCE(
                AVG(ar.attendance),
                0
            ) AS avg_attendance

        FROM academic_records ar

        {where}
        """,
        parameters
    ).fetchone()

    toppers = connection.execute(
        f"""
        SELECT

            ar.*,

            s.name,

            s.roll_no

        FROM academic_records ar

        JOIN students s
        ON s.id = ar.student_id

        {where}

        ORDER BY ar.percentage DESC

        LIMIT 5
        """,
        parameters
    ).fetchall()

    grades = connection.execute(
        f"""
        SELECT

            ar.grade,

            COUNT(*) AS count

        FROM academic_records ar

        {where}

        GROUP BY ar.grade

        ORDER BY

            CASE ar.grade

                WHEN 'A+' THEN 1
                WHEN 'A' THEN 2
                WHEN 'B+' THEN 3
                WHEN 'B' THEN 4
                WHEN 'C' THEN 5
                WHEN 'D' THEN 6
                ELSE 7

            END
        """,
        parameters
    ).fetchall()

    subject_rows = connection.execute(
        f"""
        SELECT

            sub.subject_name,

            ROUND(
                AVG(
                    sub.marks * 100.0
                    / sub.max_marks
                ),
                2
            ) AS average

        FROM subjects sub

        JOIN academic_records ar
        ON ar.id = sub.record_id

        {where}

        GROUP BY sub.subject_name

        ORDER BY average DESC
        """
        ,
        parameters
    ).fetchall()

    semester_rows = connection.execute(
        """
        SELECT

            semester,

            COUNT(*) AS records,

            ROUND(
                AVG(percentage),
                2
            ) AS average

        FROM academic_records

        GROUP BY semester

        ORDER BY id
        """
    ).fetchall()

    connection.close()

    return render_template(
        "index.html",

        stats=stats,

        toppers=toppers,

        grade_data=grades,

        subject_rows=subject_rows,

        semester_rows=semester_rows,

        semesters=SEMESTERS,

        selected_semester=selected_semester
    )


# =========================================================
# STUDENT / ACADEMIC RECORDS
# =========================================================

@app.route("/students")
def students():

    search = request.args.get(
        "search",
        ""
    ).strip()

    semester = request.args.get(
        "semester",
        ""
    ).strip()

    grade = request.args.get(
        "grade",
        ""
    ).strip()

    connection = get_db()

    query = """
        SELECT

            ar.*,

            s.name,

            s.roll_no,

            s.class_name,

            s.id AS student_id

        FROM academic_records ar

        JOIN students s
        ON s.id = ar.student_id

        WHERE 1 = 1
    """

    parameters = []

    if search:

        query += """
            AND (
                s.name LIKE ?
                OR s.roll_no LIKE ?
                OR s.class_name LIKE ?
            )
        """

        search_value = (
            f"%{search}%"
        )

        parameters.extend(
            [
                search_value,
                search_value,
                search_value
            ]
        )

    if semester:

        query += """
            AND ar.semester = ?
        """

        parameters.append(
            semester
        )

    if grade:

        query += """
            AND ar.grade = ?
        """

        parameters.append(
            grade
        )

    query += """
        ORDER BY ar.id DESC
    """

    records = connection.execute(
        query,
        parameters
    ).fetchall()

    connection.close()

    return render_template(
        "students.html",

        records=records,

        search=search,

        selected_semester=semester,

        selected_grade=grade,

        semesters=SEMESTERS
    )


# =========================================================
# ADD ACADEMIC RECORD
# =========================================================

@app.route(
    "/add",
    methods=["GET", "POST"]
)
def add_student():

    if request.method == "POST":

        error = validate_basic_form(
            request.form
        )

        try:

            subjects = parse_subjects(
                request.form
            )

        except ValueError as exception:

            error = str(exception)

            subjects = []

        if error:

            flash(
                error,
                "danger"
            )

            return render_template(
                "add_student.html",

                form=request.form,

                semesters=SEMESTERS,

                subjects=(
                    subjects
                    or [
                        {
                            "name": "",
                            "marks": "",
                            "max_marks": 100
                        }
                    ]
                )
            )

        semester = semester_from_form(
            request.form
        )

        attendance = float(
            request.form["attendance"]
        )

        (
            total,
            maximum,
            percentage,
            grade,
            performance
        ) = calculate_result(
            subjects
        )

        connection = get_db()

        try:

            existing_student = connection.execute(
                """
                SELECT id

                FROM students

                WHERE roll_no = ?
                """,
                (
                    request.form[
                        "roll_no"
                    ].strip(),
                )
            ).fetchone()

            if existing_student:

                student_id = (
                    existing_student["id"]
                )

                connection.execute(
                    """
                    UPDATE students

                    SET
                        name = ?,
                        class_name = ?

                    WHERE id = ?
                    """,
                    (
                        request.form[
                            "name"
                        ].strip(),

                        request.form[
                            "class_name"
                        ].strip(),

                        student_id
                    )
                )

            else:

                cursor = connection.execute(
                    """
                    INSERT INTO students
                    (
                        name,
                        roll_no,
                        class_name
                    )

                    VALUES (?, ?, ?)
                    """,
                    (
                        request.form[
                            "name"
                        ].strip(),

                        request.form[
                            "roll_no"
                        ].strip(),

                        request.form[
                            "class_name"
                        ].strip()
                    )
                )

                student_id = (
                    cursor.lastrowid
                )

            existing_record = connection.execute(
                """
                SELECT id

                FROM academic_records

                WHERE
                    student_id = ?
                    AND semester = ?
                """,
                (
                    student_id,
                    semester
                )
            ).fetchone()

            if existing_record:

                connection.close()

                flash(
                    f"{semester} already exists "
                    "for this student. "
                    "Please use Edit.",
                    "danger"
                )

                return render_template(
                    "add_student.html",

                    form=request.form,

                    semesters=SEMESTERS,

                    subjects=subjects
                )

            cursor = connection.execute(
                """
                INSERT INTO academic_records
                (
                    student_id,
                    semester,
                    attendance,
                    total,
                    max_total,
                    percentage,
                    grade,
                    performance
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    student_id,
                    semester,
                    attendance,
                    total,
                    maximum,
                    percentage,
                    grade,
                    performance
                )
            )

            record_id = (
                cursor.lastrowid
            )

            for subject in subjects:

                connection.execute(
                    """
                    INSERT INTO subjects
                    (
                        record_id,
                        subject_name,
                        marks,
                        max_marks
                    )

                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        record_id,
                        subject["name"],
                        subject["marks"],
                        subject["max_marks"]
                    )
                )

            connection.commit()

            flash(
                "Academic record added successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "report",
                    record_id=record_id
                )
            )

        except sqlite3.IntegrityError:

            connection.rollback()

            flash(
                "Could not save the record. "
                "The roll number may already exist.",
                "danger"
            )

        finally:

            connection.close()

    return render_template(
        "add_student.html",

        form=None,

        semesters=SEMESTERS,

        subjects=[
            {
                "name": subject,
                "marks": "",
                "max_marks": 100
            }

            for subject in DEFAULT_SUBJECTS
        ]
    )


# =========================================================
# EDIT ACADEMIC RECORD
# =========================================================

@app.route(
    "/edit/<int:record_id>",
    methods=["GET", "POST"]
)
def edit_student(record_id):

    connection = get_db()

    record, old_subjects = get_record(
        connection,
        record_id
    )

    if not record:

        connection.close()

        return (
            "Academic record not found",
            404
        )

    if request.method == "POST":

        error = validate_basic_form(
            request.form
        )

        try:

            subjects = parse_subjects(
                request.form
            )

        except ValueError as exception:

            error = str(exception)

            subjects = []

        if error:

            connection.close()

            flash(
                error,
                "danger"
            )

            return render_template(
                "edit_student.html",

                record=request.form,

                record_id=record_id,

                subjects=(
                    subjects
                    or [
                        {
                            "name": "",
                            "marks": "",
                            "max_marks": 100
                        }
                    ]
                ),

                semesters=SEMESTERS
            )

        semester = semester_from_form(
            request.form
        )

        duplicate = connection.execute(
            """
            SELECT id

            FROM academic_records

            WHERE
                student_id = ?
                AND semester = ?
                AND id <> ?
            """,
            (
                record["student_id"],
                semester,
                record_id
            )
        ).fetchone()

        if duplicate:

            connection.close()

            flash(
                f"{semester} already exists "
                "for this student.",
                "danger"
            )

            return render_template(
                "edit_student.html",

                record=request.form,

                record_id=record_id,

                subjects=subjects,

                semesters=SEMESTERS
            )

        (
            total,
            maximum,
            percentage,
            grade,
            performance
        ) = calculate_result(
            subjects
        )

        try:

            connection.execute(
                """
                UPDATE students

                SET
                    name = ?,
                    roll_no = ?,
                    class_name = ?

                WHERE id = ?
                """,
                (
                    request.form[
                        "name"
                    ].strip(),

                    request.form[
                        "roll_no"
                    ].strip(),

                    request.form[
                        "class_name"
                    ].strip(),

                    record["student_id"]
                )
            )

            connection.execute(
                """
                UPDATE academic_records

                SET
                    semester = ?,
                    attendance = ?,
                    total = ?,
                    max_total = ?,
                    percentage = ?,
                    grade = ?,
                    performance = ?

                WHERE id = ?
                """,
                (
                    semester,

                    float(
                        request.form[
                            "attendance"
                        ]
                    ),

                    total,

                    maximum,

                    percentage,

                    grade,

                    performance,

                    record_id
                )
            )

            connection.execute(
                """
                DELETE FROM subjects

                WHERE record_id = ?
                """,
                (
                    record_id,
                )
            )

            for subject in subjects:

                connection.execute(
                    """
                    INSERT INTO subjects
                    (
                        record_id,
                        subject_name,
                        marks,
                        max_marks
                    )

                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        record_id,
                        subject["name"],
                        subject["marks"],
                        subject["max_marks"]
                    )
                )

            connection.commit()

            flash(
                "Academic record updated successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "report",
                    record_id=record_id
                )
            )

        except sqlite3.IntegrityError:

            connection.rollback()

            flash(
                "Roll number must be unique.",
                "danger"
            )

        finally:

            connection.close()

    else:

        connection.close()

    return render_template(
        "edit_student.html",

        record=record,

        record_id=record_id,

        subjects=old_subjects,

        semesters=SEMESTERS
    )


# =========================================================
# DELETE RECORD
# =========================================================

@app.route(
    "/delete/<int:record_id>",
    methods=["POST"]
)
def delete_student(record_id):

    connection = get_db()

    connection.execute(
        """
        DELETE FROM academic_records

        WHERE id = ?
        """,
        (
            record_id,
        )
    )

    connection.commit()

    connection.close()

    flash(
        "Academic record deleted successfully.",
        "success"
    )

    return redirect(
        url_for("students")
    )


# =========================================================
# DETAILED STUDENT REPORT
# =========================================================

@app.route(
    "/report/<int:record_id>"
)
def report(record_id):

    connection = get_db()

    record, subjects = get_record(
        connection,
        record_id
    )

    if not record:

        connection.close()

        return (
            "Academic record not found",
            404
        )

    highest = None

    lowest = None

    if subjects:

        highest = max(
            subjects,
            key=lambda subject:
                subject["marks"]
                / subject["max_marks"]
        )

        lowest = min(
            subjects,
            key=lambda subject:
                subject["marks"]
                / subject["max_marks"]
        )

    history = connection.execute(
        """
        SELECT

            semester,

            percentage,

            grade

        FROM academic_records

        WHERE student_id = ?

        ORDER BY id
        """,
        (
            record["student_id"],
        )
    ).fetchall()

    connection.close()

    subject_names = [
        subject["subject_name"]
        for subject in subjects
    ]

    subject_percentages = [
        round(
            (
                subject["marks"]
                /
                subject["max_marks"]
            ) * 100,
            2
        )

        for subject in subjects
    ]

    return render_template(
        "report.html",

        record=record,

        subjects=subjects,

        highest=highest,

        lowest=lowest,

        subject_names=subject_names,

        subject_percentages=subject_percentages,

        history=history
    )


# =========================================================
# CSV EXPORT
# =========================================================

@app.route("/export")
def export_csv():

    selected_semester = request.args.get(
        "semester",
        ""
    ).strip()

    connection = get_db()

    query = """
        SELECT

            s.name,

            s.roll_no,

            s.class_name,

            ar.semester,

            ar.attendance,

            ar.total,

            ar.max_total,

            ar.percentage,

            ar.grade,

            ar.performance,

            sub.subject_name,

            sub.marks,

            sub.max_marks

        FROM academic_records ar

        JOIN students s
        ON s.id = ar.student_id

        JOIN subjects sub
        ON sub.record_id = ar.id
    """

    parameters = []

    if selected_semester:

        query += """
            WHERE ar.semester = ?
        """

        parameters.append(
            selected_semester
        )

    query += """
        ORDER BY
            s.name,
            ar.semester,
            sub.id
    """

    rows = connection.execute(
        query,
        parameters
    ).fetchall()

    connection.close()

    output = io.StringIO()

    writer = csv.writer(
        output
    )

    writer.writerow(
        [
            "Name",
            "Roll No",
            "Class/Course",
            "Semester",
            "Attendance",
            "Total Marks",
            "Maximum Marks",
            "Percentage",
            "Grade",
            "Performance",
            "Subject",
            "Marks",
            "Subject Max Marks"
        ]
    )

    for row in rows:

        writer.writerow(
            [
                row["name"],
                row["roll_no"],
                row["class_name"],
                row["semester"],
                row["attendance"],
                row["total"],
                row["max_total"],
                row["percentage"],
                row["grade"],
                row["performance"],
                row["subject_name"],
                row["marks"],
                row["max_marks"]
            ]
        )

    file_data = (
        output
        .getvalue()
        .encode("utf-8-sig")
    )

    return send_file(
        io.BytesIO(file_data),

        mimetype="text/csv",

        as_attachment=True,

        download_name=(
            "student_academic_performance.csv"
        )
    )


# =========================================================
# STARTUP
# =========================================================

init_db()


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )