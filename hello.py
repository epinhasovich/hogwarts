from flask import Flask, jsonify, render_template, request
import threading

app = Flask(__name__)

students = [
    {
        "id": 1,
        "First Name": "Eric"
    },
    {
        "id": 2,
        "First Name": "Tomer"
    }
]


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/students", methods=['GET'])
def show():
  return render_template("students.html", students=students)


@app.route("/students/<int:id>", methods=['GET'])
def get_student(id):
    student = [student for student in students if student['id'] == id]
    return render_template("student.html", student=student[0])


@app.route("/students/add", methods=['GET'])
def add_student():
    return render_template('add.html')


@app.route("/added", methods=['POST'])
def create_student():
    student = {
        "id": students[-1]['id'] + 1,
        "First Name": request.form['testForm']
    }

    students.append(student)
    return render_template("student.html", student=student)


if __name__ == "__main__":
  threading.Thread(target=app.run).start()
