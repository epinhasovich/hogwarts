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
        "First Name": "Axel"
    }
]


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/students", methods=['GET'])
def hello():
  return render_template("students.html", students=students)


@app.route("/students/<int:id>", methods=['GET'])
def get_student(id):
    student = [student for student in students if student['id'] == id]
    return jsonify({'student': student[0]})


if __name__ == "__main__":
  threading.Thread(target=app.run).start()
  print("Yay")