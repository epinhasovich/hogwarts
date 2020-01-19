from flask import Flask, render_template, request, url_for, send_from_directory
import threading
from datetime import datetime


app = Flask(__name__)

students = [
    {
        "id": 1,
        "first_name": "Eric",
        "last_name": "Pinhasovich",
        "existing_magic_skills": [
                            {"skill": 'Healing', "level": 4},
                            {"skill": 'Animation', "level": 2}
                                ],
        "desired_magic_skills": ["Poison"],
        "courses": "Magic For Day-to-Day Life",
        "created_time": datetime.now(),
        "updated_time": ''
    },
    {
        "id": 2,
        "first_name": "Harry",
        "last_name": "Potter",
        "existing_magic_skills": [
                            {"skill": 'Alchemy', "level": 5},
                            {'skill': 'Invisibility', 'level': 2},
                            {'skill': 'Omnipresent', 'level': 3}
                                 ],
        "desired_magic_skills": ["Poison", "Elemental"],
        "courses": "Dating With Magic",
        "created_time": datetime.now(),
        "updated_time": ''
    },
    {
        "id": 3,
        "first_name": "Hermoine",
        "last_name": "Granger",
        "existing_magic_skills": [
                            {"skill": 'Poison', "level": 4},
                            {'skill': 'Summoning', 'level': 2},
                            {'skill': 'Healing', 'level': 3}
                                 ],
        "desired_magic_skills": ["Invisibility", "Immortality"],
        "courses": "Magic For Medical Professionals",
        "created_time": datetime.now(),
        "updated_time": ''
    },
    {
        "id": 4,
        "first_name": "Draco",
        "last_name": "Malfoy",
        "existing_magic_skills": [
                            {"skill": 'Poison', "level": 4},
                            {'skill': 'Possesion', 'level': 4},
                            {'skill': 'Immortality', 'level': 5}
                                 ],
        "desired_magic_skills": ["Summoning", "Animation", "Healing"],
        "courses": "Alchemy Basics",
        "created_time": datetime.now(),
        "updated_time": ''
    },
    {
        "id": 5,
        "first_name": "Neville",
        "last_name": "Longbottom",
        "existing_magic_skills": [
                            {"skill": 'Invisibility', "level": 1},
                            {'skill': 'Illusion', 'level': 1},
                            {'skill': 'Elemental', 'level': 1}
                                 ],
        "desired_magic_skills": ["Summoning", "Disintegration", "Healing"],
        "courses": "Dating With Magic",
        "created_time": datetime.now(),
        "updated_time": ''
    }
]

magic_skills = ["Alchemy", "Animation", "Conjuror", "Disintegration", "Elemental", "Healing", "Illusion", "Immortality",
                "Invisibility", "Invulnerability", "Necromancer", "Omnipresent", "Omniscient", "Poison", "Possession",
                "Self-detonation", "Summoning", "Water breathing"]


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
        magic_skillz = request.form.getlist('magic_skills[]')
        magic_skillz = [{'skill': skill} for skill in magic_skillz]
        magic_level = request.form.getlist('magic_level[]')
        for i in range(len(magic_skillz)):
            magic_skillz[i]['level'] = magic_level[i]
        return magic_skillz

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
        "desired_magic_skills": wanted_skills(),
        "courses": course_list(),
        "created_time": datetime.now(),
        "updated_time": ''
    }
    students.append(student)
    return render_template("student.html", student=student)


@app.route("/students/<int:id>/edit", methods=['GET', 'POST'])
def edit_student(id):
    student = [student for student in students if student['id'] == id][0]
    if request.method == 'GET':
        return render_template('edit.html', student=student)
    elif request.method == 'POST':
        fname = request.form.get('firstForm')
        lname = request.form.get('lastForm')
        student_wanted_magic_skills = request.form.getlist("wanted_skills[]")
        magic_skillz = request.form.getlist('magic_skills[]')
        magic_skillz = [{'skill': skill} for skill in magic_skillz]
        magic_level = request.form.getlist('magic_level[]')
        for i in range(len(magic_skillz)):
            magic_skillz[i]['level'] = magic_level[i]
        classes = request.form.getlist("classes[]")
        student['first_name'] = fname
        student['last_name'] = lname
        student["existing_magic_skills"] = magic_skillz
        student["desired_magic_skills"] = student_wanted_magic_skills
        student["courses"] = classes
        student['updated_time'] = datetime.now()
        return render_template('student.html', student=student)


@app.route('/skillstats')
def pie_chart():
    data = students
    existing_skills = []
    desired_skills = []
    student_number = len(students)
    student_count = [student_number][0]
    print(student_count)
    student = [student for student in data]
    for skill in student:
        e_skills = skill['existing_magic_skills']
        d_skills = skill['desired_magic_skills']
        for skill in e_skills:
            student_skills = skill['skill']
            existing_skills.append(student_skills)
        for skill in d_skills:
            desired_skills.append(skill)
    existing_list = []
    for skill in magic_skills:
        count = existing_skills.count(skill)
        if count:
            existing_list.append({'y': count, 'label': skill})
    desired_list = []
    for skill in magic_skills:
        count = desired_skills.count(skill)
        if count:
            desired_list.append({'y': count, 'label': skill})
    return render_template('pie-chart.html', data=data, existing_list=existing_list, desired_list=desired_list, student_count=student_count)


# @app.route('/students/<int:id>/delete', methods=['GET'])
# def delete_student(id):
#     student = [student for student in students if student['id'] == id][0]
#     students.remove(student[0])
#     return render_template("students.html", students=students)


if __name__ == "__main__":
    threading.Thread(target=app.run).start()

