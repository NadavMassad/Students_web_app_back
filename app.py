import json
import os
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# list of students
students = []

# write students to json file
def save_to_file():
    json_object = json.dumps(students, indent=4)
    print(json_object)
    with open("students.json", "w") as contact_file:
        contact_file.write(json_object)

# read json file
def load_file():
    global students
    if os.stat('students.json').st_size == 0:
        return []
    else:
        with open("students.json", "r") as contact_file:
            students = json.load(contact_file)
            return students


@app.route('/students/', methods=['GET', 'POST'])
def student_methods():
    if request.method == 'GET':
        load_file()
        return (json.dumps(load_file()))

    if request.method == 'POST':
        request_data = request.get_json()
        sname = request_data['sname']
        email = request_data['email']
        load_file()
        if len(students) == 0:
            student_id = 1
        else:
            last_stud = students[-1]
            last_id = last_stud['student_id']
            print(last_id)
            student_id = last_id + 1

        new_student = {
            "student_id": student_id,
            "sname": sname,
            "email": email,
            "math": 0,
            "english": 0,
            "computers": 0
        }
        
        students.append(new_student)
        save_to_file()
        return new_student

@app.route('/grades/<id>', methods=['PUT'])
def add_grades(id=-1):
    load_file()
    request_data = request.get_json()
    for stud in students:
        if stud['student_id'] == int(id):
            if 'math' in request_data:
                math = request_data['math']
                stud['math'] = math 
                save_to_file()
                return stud
            elif 'english' in request_data:
                english = request_data['english']
                stud['english'] = english
                save_to_file()
                return stud
            elif 'computers' in request_data:
                computers = request_data['computers']
                stud['computers'] = computers
                save_to_file()
                return stud

@app.route('/')
def test():
    return 'Students'


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
