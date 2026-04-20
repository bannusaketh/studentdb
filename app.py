from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def connect_db():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = connect_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        course TEXT,
        phone TEXT
    )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = connect_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    age = request.form["age"]
    course = request.form["course"]
    phone = request.form["phone"]

    conn = connect_db()
    conn.execute(
        "INSERT INTO students(name, age, course, phone) VALUES(?,?,?,?)",
        (name, age, course, phone)
    )
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = connect_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/edit/<int:id>")
def edit(id):
    conn = connect_db()
    student = conn.execute(
        "SELECT * FROM students WHERE id=?", (id,)
    ).fetchone()
    conn.close()
    return render_template("edit.html", student=student)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    name = request.form["name"]
    age = request.form["age"]
    course = request.form["course"]
    phone = request.form["phone"]

    conn = connect_db()
    conn.execute("""
        UPDATE students
        SET name=?, age=?, course=?, phone=?
        WHERE id=?
    """, (name, age, course, phone, id))
    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    create_table()
    app.run(debug=True)