from flask import Flask, render_template, request
import pymssql


app = Flask(__name__)


# Azure SQL Database Connection

server = 'studentserver12345.database.windows.net'
database = 'StudentDB'
username = 'shraddha'
password = '#poonam2124'


connection = pymssql.connect(
    'DRIVER={SQL Server};'
    'SERVER='+server+';'
    'DATABASE='+database+';'
    'UID='+username+';'
    'PWD='+password
)



# Home Page

@app.route("/")
def home():

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM StudentRegistration"
    )

    students = cursor.fetchall()

    return render_template(
        "index.html",
        students=students
    )



# Save Student Data

@app.route("/register", methods=["POST"])
def register():

    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    course = request.form["course"]
    city = request.form["city"]


    cursor = connection.cursor()


    cursor.execute(
    """
    INSERT INTO StudentRegistration
    (FullName, Email, Phone, Course, City)
    VALUES (?, ?, ?, ?, ?)
    """,
    (name,email,phone,course,city)
    )


    connection.commit()


    return """
    <h2>Registration Successful!</h2>
    <a href="/">Go Back</a>
    """



if __name__ == "__main__":
    app.run()
