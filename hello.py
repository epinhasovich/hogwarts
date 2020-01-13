from flask import Flask, jsonify, render_template, request
import threading
from datetime import datetime


app = Flask(__name__)

students = [
    {
        "id": 1,
        "First Name": "Eric",
        "Last Name": "Pinhasovich",
        "Existing Magic Skills": "Healing",
        "Desired Magic Skills": "Potions",
        "Courses": "Magic For Day-to-Day Life",
        "Created Time": datetime.now()
    },
    {
        "id": 2,
        "First Name": "Harry",
        "Last Name": "Potter",
        "Existing Magic Skills": ["Alchemy", "Invisibility"],
        "Desired Magic Skills": "Poison",
        "Courses": "Dating With Magic",
        "Created Time": datetime.now()
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
    def add_skills():
        skills = []
        for key, val in request.form.items():
            if key.startswith('skill'):
                skills.append(val)
        return skills

    def wanted_skills():
        wanted = []
        for key, val in request.form.items():
            if key.startswith('wanted'):
                wanted.append(val)
        return wanted

    def course_list():
        courses = []
        for key, val in request.form.items():
            if key.startswith('course'):
                courses.append(val)
        return courses
    student = {
        "id": students[-1]['id'] + 1,
        "First Name": request.form['firstForm'],
        "Last Name": request.form['lastForm'],
        "Existing Magic Skills": add_skills(),
        "Desired Magic Skills": wanted_skills(),
        "Courses": course_list(),
        "Created Time": datetime.now()

    }

    students.append(student)
    return render_template("student.html", student=student)


@app.route("/students/update/<int:id>", methods=['GET'])
def edit_student(id):
    print("Hello!")
    student = [student for student in students if student['id'] == id]
    print("Hello 2!")
    return render_template('edit.html', student=student)


@app.route("/edited/", methods=['POST'])
def update_student(id):
    student = [student for student in students if student['id'] == id]
    student[0]['First Name'] = request.form.get('First Name', student[0]['First Name'])
    return render_template("student.html", student=student[0])


if __name__ == "__main__":
    threading.Thread(target=app.run).start()
