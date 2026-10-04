from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import sqlite3
import csv
import io
from jinja2 import ChoiceLoader, FileSystemLoader

app = Flask(__name__)
app.jinja_loader = ChoiceLoader([
    app.jinja_loader,
    FileSystemLoader(app.root_path)
])
app.secret_key = "student-performance-secret-key"

DATABASE = "students.db"

SUBJECTS = [
    "Mathematics",
    "Python",
    "DSA",
    "DBMS",
    "Computer Networks"
]


# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL UNIQUE,
            class_name TEXT NOT NULL,

            maths REAL NOT NULL,
            python REAL NOT NULL,
            dsa REAL NOT NULL,
            dbms REAL NOT NULL,
            networks REAL NOT NULL,

            attendance REAL NOT NULL,

            total REAL NOT NULL,
            percentage REAL NOT NULL,
            grade TEXT NOT NULL,
            performance TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ---------------- CALCULATIONS ----------------

def grade_from_percentage(percentage):

    if percentage >= 90:
        return "A+"

    elif percentage >= 80:
        return "A"

    elif percentage >= 70:
        return "B+"

    elif percentage >= 60:
        return "B"

    elif percentage >= 50:
        return "C"

    elif percentage >= 40:
        return "D"

    else:
        return "F"


def performance_from_percentage(percentage):

    if percentage >= 90:
        return "Excellent"

    elif percentage >= 75:
        return "Good"

    elif percentage >= 60:
        return "Average"

    elif percentage >= 40:
        return "Needs Improvement"

    else:
        return "Poor"


def calculate_result(data):

    maths = float(data["maths"])
    python = float(data["python"])
    dsa = float(data["dsa"])
    dbms = float(data["dbms"])
    networks = float(data["networks"])

    total = maths + python + dsa + dbms + networks

    percentage = total / 5

    grade = grade_from_percentage(percentage)

    performance = performance_from_percentage(percentage)

    return total, percentage, grade, performance


# ---------------- VALIDATION ----------------

def validate_form(form):

    required_fields = [
        "name",
        "roll_no",
        "class_name",
        "maths",
        "python",
        "dsa",
        "dbms",
        "networks",
        "attendance"
    ]

    for field in required_fields:

        if not form.get(field, "").strip():

            return "All fields are required."

    try:

        maths = float(form["maths"])
        python = float(form["python"])
        dsa = float(form["dsa"])
        dbms = float(form["dbms"])
        networks = float(form["networks"])
        attendance = float(form["attendance"])

    except ValueError:

        return "Marks and attendance must be valid numbers."

    values = [
        maths,
        python,
        dsa,
        dbms,
        networks,
        attendance
    ]

    for value in values:

        if value < 0 or value > 100:

            return "Marks and attendance must be between 0 and 100."

    return None


# ---------------- DASHBOARD ----------------

@app.route("/")
def index():

    conn = get_db()

    total_students = conn.execute(
        "SELECT COUNT(*) AS count FROM students"
    ).fetchone()["count"]

    avg_percentage = conn.execute(
        "SELECT COALESCE(AVG(percentage), 0) AS avg FROM students"
    ).fetchone()["avg"]

    avg_attendance = conn.execute(
        "SELECT COALESCE(AVG(attendance), 0) AS avg FROM students"
    ).fetchone()["avg"]

    toppers = conn.execute(
        """
        SELECT *
        FROM students
        ORDER BY percentage DESC
        LIMIT 5
        """
    ).fetchall()

    grade_data = conn.execute(
        """
        SELECT grade, COUNT(*) AS count
        FROM students
        GROUP BY grade
        ORDER BY grade
        """
    ).fetchall()

    subject_columns = {
        "Mathematics": "maths",
        "Python": "python",
        "DSA": "dsa",
        "DBMS": "dbms",
        "Computer Networks": "networks"
    }

    subject_averages = {}

    for subject, column in subject_columns.items():

        row = conn.execute(
            f"""
            SELECT COALESCE(AVG({column}), 0) AS avg
            FROM students
            """
        ).fetchone()

        subject_averages[subject] = round(row["avg"], 2)

    conn.close()

    return render_template(
        "index.html",
        total_students=total_students,
        avg_percentage=round(avg_percentage, 2),
        avg_attendance=round(avg_attendance, 2),
        toppers=toppers,
        grade_data=grade_data,
        subject_averages=subject_averages
    )


# ---------------- VIEW STUDENTS ----------------

@app.route("/students")
def students():

    search = request.args.get("search", "").strip()

    grade = request.args.get("grade", "").strip()

    conn = get_db()

    query = """
        SELECT *
        FROM students
        WHERE 1=1
    """

    parameters = []

    if search:

        query += """
            AND (
                name LIKE ?
                OR roll_no LIKE ?
                OR class_name LIKE ?
            )
        """

        search_value = f"%{search}%"

        parameters.extend([
            search_value,
            search_value,
            search_value
        ])

    if grade:

        query += " AND grade = ?"

        parameters.append(grade)

    query += " ORDER BY id DESC"

    students_data = conn.execute(
        query,
        parameters
    ).fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=students_data,
        search=search,
        selected_grade=grade
    )


# ---------------- ADD STUDENT ----------------

@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        error = validate_form(request.form)

        if error:

            flash(error, "danger")

            return render_template(
                "add_student.html",
                student=request.form
            )

        try:

            total, percentage, grade, performance = calculate_result(
                request.form
            )

            conn = get_db()

            conn.execute(
                """
                INSERT INTO students
                (
                    name,
                    roll_no,
                    class_name,
                    maths,
                    python,
                    dsa,
                    dbms,
                    networks,
                    attendance,
                    total,
                    percentage,
                    grade,
                    performance
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,

                (
                    request.form["name"].strip(),
                    request.form["roll_no"].strip(),
                    request.form["class_name"].strip(),

                    float(request.form["maths"]),
                    float(request.form["python"]),
                    float(request.form["dsa"]),
                    float(request.form["dbms"]),
                    float(request.form["networks"]),

                    float(request.form["attendance"]),

                    total,
                    percentage,
                    grade,
                    performance
                )
            )

            conn.commit()

            conn.close()

            flash(
                "Student added successfully.",
                "success"
            )

            return redirect(
                url_for("students")
            )

        except sqlite3.IntegrityError:

            flash(
                "Roll number already exists.",
                "danger"
            )

    return render_template(
        "add_student.html",
        student=None
    )


# ---------------- EDIT STUDENT ----------------

@app.route(
    "/edit/<int:student_id>",
    methods=["GET", "POST"]
)
def edit_student(student_id):

    conn = get_db()

    existing_student = conn.execute(
        """
        SELECT *
        FROM students
        WHERE id = ?
        """,
        (student_id,)
    ).fetchone()

    if existing_student is None:

        conn.close()

        return "Student not found", 404

    if request.method == "POST":

        error = validate_form(request.form)

        if error:

            conn.close()

            flash(
                error,
                "danger"
            )

            return render_template(
                "edit_student.html",
                student=request.form,
                student_id=student_id
            )

        try:

            total, percentage, grade, performance = calculate_result(
                request.form
            )

            conn.execute(
                """
                UPDATE students
                SET
                    name = ?,
                    roll_no = ?,
                    class_name = ?,
                    maths = ?,
                    python = ?,
                    dsa = ?,
                    dbms = ?,
                    networks = ?,
                    attendance = ?,
                    total = ?,
                    percentage = ?,
                    grade = ?,
                    performance = ?

                WHERE id = ?
                """,

                (
                    request.form["name"].strip(),
                    request.form["roll_no"].strip(),
                    request.form["class_name"].strip(),

                    float(request.form["maths"]),
                    float(request.form["python"]),
                    float(request.form["dsa"]),
                    float(request.form["dbms"]),
                    float(request.form["networks"]),

                    float(request.form["attendance"]),

                    total,
                    percentage,
                    grade,
                    performance,

                    student_id
                )
            )

            conn.commit()

            conn.close()

            flash(
                "Student updated successfully.",
                "success"
            )

            return redirect(
                url_for("students")
            )

        except sqlite3.IntegrityError:

            conn.close()

            flash(
                "Roll number already belongs to another student.",
                "danger"
            )

            return render_template(
                "edit_student.html",
                student=request.form,
                student_id=student_id
            )

    conn.close()

    return render_template(
        "edit_student.html",
        student=existing_student,
        student_id=student_id
    )


# ---------------- DELETE STUDENT ----------------

@app.route(
    "/delete/<int:student_id>",
    methods=["POST"]
)
def delete_student(student_id):

    conn = get_db()

    conn.execute(
        """
        DELETE FROM students
        WHERE id = ?
        """,
        (student_id,)
    )

    conn.commit()

    conn.close()

    flash(
        "Student deleted successfully.",
        "success"
    )

    return redirect(
        url_for("students")
    )


# ---------------- STUDENT REPORT ----------------

@app.route("/report/<int:student_id>")
def report(student_id):

    conn = get_db()

    student = conn.execute(
        """
        SELECT *
        FROM students
        WHERE id = ?
        """,
        (student_id,)
    ).fetchone()

    conn.close()

    if student is None:

        return "Student not found", 404

    marks = {

        "Mathematics": student["maths"],

        "Python": student["python"],

        "DSA": student["dsa"],

        "DBMS": student["dbms"],

        "Computer Networks": student["networks"]
    }

    highest_subject = max(
        marks,
        key=marks.get
    )

    lowest_subject = min(
        marks,
        key=marks.get
    )

    return render_template(
        "report.html",
        student=student,
        marks=marks,
        highest_subject=highest_subject,
        lowest_subject=lowest_subject
    )


# ---------------- CSV EXPORT ----------------

@app.route("/export")
def export_csv():

    conn = get_db()

    students_data = conn.execute(
        """
        SELECT *
        FROM students
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Name",
        "Roll No",
        "Class",
        "Mathematics",
        "Python",
        "DSA",
        "DBMS",
        "Computer Networks",
        "Attendance",
        "Total",
        "Percentage",
        "Grade",
        "Performance"
    ])

    for student in students_data:

        writer.writerow([
            student["name"],
            student["roll_no"],
            student["class_name"],
            student["maths"],
            student["python"],
            student["dsa"],
            student["dbms"],
            student["networks"],
            student["attendance"],
            student["total"],
            student["percentage"],
            student["grade"],
            student["performance"]
        ])

    output.seek(0)

    return send_file(
        io.BytesIO(
            output.getvalue().encode("utf-8")
        ),

        mimetype="text/csv",

        as_attachment=True,

        download_name="student_performance.csv"
    )


# ---------------- START APPLICATION ----------------

init_db()


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)