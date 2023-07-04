from flask import Flask, request, jsonify

app = Flask(__name__)

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database = "pythonstudentcrud"
)

print(mydb)

# reference point to interact with mysql database
mycursor = mydb.cursor()


@app.route('/')
def hello_world():
    return 'This is my first API call!'

@app.route('/api/v1/student', methods=["POST"])
def createstudent():
     # getting input data in json format from user and storing it in dict format
     input_json = request.get_json(force=True)
     sql = "INSERT INTO students (Name, Age, RollNo, City) VALUES (%s, %s, %s, %s)"
     val = (input_json['Name'], input_json['Age'], input_json['RollNo'], input_json['City'])
     mycursor.execute(sql,val)
     mydb.commit()
     dictToReturn = { "succcess" : True ,
                      "id" : mycursor.lastrowid
                      }
     # returning the data in json format
     return jsonify(dictToReturn)


@app.route('/api/v1/student/roll', methods=["GET"])
def findByRoll():
    # getting input data from query params from user and storing it in dict format
    args = request.args
    print(args)
    sql = "SELECT Studentid, Name, Age, City from students where rollno = %s "
    # adr = (args.get('roll'),)
    #         OR
    val = (args['roll'], )
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    student_data = { 'student_id' : myresult[0],
                     'name' : myresult[1],
                     'age' : myresult[2],
                     'city' : myresult[3] }

    response = { 'success' : True,
                 'data' : student_data }
    return jsonify(response)



@app.route('/api/v1/student/roll', methods=["DELETE"])
def deleteByRoll():
    args = request.args
    print(args)
    sql = "DELETE FROM students WHERE rollno =  %s"
    adr = (args.get('roll'), )
    mycursor.execute(sql, adr)
    mydb.commit()
    response = { 'success' : True }
    return jsonify(response)


@app.route('/api/v1/student/studentid', methods=["GET"])
def findByStudentId():
    args = request.args
    print(args)
    sql = "SELECT Name, Age, RollNo, City from students where studentid = %s "
    adr = (args.get('studentid'), )
    print(type(adr))
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchone()
    student_data = { 'name' : myresult[0],
                     'age' : myresult[1],
                     'roll_no' : myresult[2],
                     'city' : myresult[3] }
    response = { 'success' : True,
                 'data' : student_data
                 }
    return jsonify(response)

@app.route('/api/v1/student/studentid', methods=["DELETE"])
def deleteByStudentId():
    args = request.args
    print(args)
    sql = "DELETE FROM students WHERE studentid =  %s"
    adr = (args.get('studentid'), )
    mycursor.execute(sql, adr)
    mydb.commit()
    response = { 'success' : True }
    return jsonify(response)

@app.route('/api/v1/student/getall', methods=["GET"])
def findAll():
    mycursor.execute("SELECT * FROM students")
    myresult = mycursor.fetchall()
    print(myresult)
    all_students = []
    for x in myresult:
        dict = {
            "student_id" : x[0],
            "name" : x[1],
            "age" : x[2],
            "roll_no" : x[3],
            "city" : x[4]
        }
        all_students.append(dict)
        print(x)
    print(all_students)
    response = {
        'success' : True,
        'data' : all_students
    }
    return jsonify(response)

@app.route('/api/v1/student/update', methods=["PUT"])
def updatestudent():
     input_json = request.get_json(force=True)
     args = request.args
     val_list = []
     # fetching roll no from query parameters
     roll = args['roll']
     sql = "update students set "
     if 'name' in input_json.keys():
         sql = sql + "name = %s,"
         val_list.append(input_json['name'])
     if 'age' in input_json.keys():
         sql = sql + " age = %s,"
         val_list.append(input_json['age'])
     if 'city' in input_json.keys():
         sql = sql + " city = %s,"
         val_list.append(input_json['city'])
     sql = sql.rstrip(',')
     sql = sql + " where rollno = %s"
     print(sql)
     val_list.append(roll)
     val_tuple = tuple(val_list)
     mycursor.execute(sql,val_tuple)
     mydb.commit()
     dictToReturn = { "succcess" : True }
     return jsonify(dictToReturn)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)








