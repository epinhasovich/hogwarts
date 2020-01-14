from flask import Flask, jsonify, render_template, request, url_for, send_from_directory
import threading
from datetime import datetime


app = Flask(__name__)

students = [
    {
        "id": 1,
        "first_name": "Eric",
        "last_name": "Pinhasovich",
        "existing_magic_skills": "Healing",
        "Desired Magic Skills": "Potions",
        "Courses": "Magic For Day-to-Day Life",
        "Created Time": datetime.now()
    },
    {
        "id": 2,
        "first_name": "Harry",
        "last_name": "Potter",
        "existing_magic_skills": ["Alchemy", "Invisibility", "Omnipresent"],
        "Desired Magic Skills": ["Poison", "Elemental"],
        "Courses": "Dating With Magic",
        "Created Time": datetime.now()
    },
    {
        "id": 3,
        "first_name": "Hermoine",
        "last_name": "Granger",
        "existing_magic_skills": ["Potions", "Water breathing", "Summoning", "Healing"],
        "Desired Magic Skills": ["Invisibility", "Immortality"],
        "Courses": "Magic For Medical Professionals",
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
        "first_name": request.form['firstForm'],
        "last_name": request.form['lastForm'],
        "existing_magic_skills": add_skills(),
        "Desired Magic Skills": wanted_skills(),
        "Courses": course_list(),
        "Created Time": datetime.now()

    }

    students.append(student)
    return render_template("student.html", student=student)


@app.route("/students/<int:id>/edit", methods=['GET', 'POST'])
def edit_student(id):
    print('1')
    student = [student for student in students if student['id'] == id][0]
    print('2')
    if request.method == 'GET':
        return render_template('edit.html', student=student)
        print('3')
    elif request.method == 'POST':
        print('4')
        fname = request.form.get('firstForm')
        lname = request.form.get('lastForm')
        ems = request.form.get(skills)
        print('5')
        student['first_name'] = fname
        student['last_name'] = lname
        student[skills] = ems
        print('6')
        return render_template('student.html', student=student)

#firstName
# @app.route('/edited')
# def update_student(id):
#     student = [student for student in students if student['id'] == id]
#     student[0]['first_name'] = request.args.get('first_name', student[0]['first_name'])
#     return render_template("student.html", student=student[0])


@app.route('/static/css/<path:path>')
def stylesheets(path):
    return app.send_static_file('css/' + path)


# @app.route('/static/css/<path:path>')
# def stylesheets(path):
#     return send_from_directory('static/css/' + path)


if __name__ == "__main__":
    threading.Thread(target=app.run).start()
