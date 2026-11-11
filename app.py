from flask import Flask, render_template, request, redirect
import pymssql

app = Flask(__name__)

# Azure SQL Database Details
server = "studentserver12345.database.windows.net"
database = "StudentDB"
username = "shraddha"
password = "#poonam2124"


def get_connection():
    return pymssql.connect(
        server=server,
        user=username,
        password=password,
        database=database,
        port=1433
    )


@app.route("/")
def home():
    try:
        connection = get_connection()
        cursor = connection.cursor(as_dict=True)

        cursor.execute("SELECT * FROM StudentRegistration")
        students = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template("index.html", students=students)

    except Exception as e:
        return f"<h2>Database Error</h2><pre>{e}</pre>"


@app.route("/register", methods=["POST"])
def register():

    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    course = request.form["course"]
    city = request.form["city"]

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO StudentRegistration
            (FullName, Email, Phone, Course, City)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (name, email, phone, course, city)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/")

    except Exception as e:
        return f"<h2>Insert Error</h2><pre>{e}</pre>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
