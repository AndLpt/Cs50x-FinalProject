from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
import helpers



app = Flask(__name__)

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
app.secret_key = 'BAD_SECRET_KEY'
Session(app)


db_users = SQL("sqlite:///users.db")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    else:

        dico = db_users.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        question1 = request.form.get("question1")
        question2 = request.form.get("question2")


        if len(dico) != 0 or not username:
            message = "Enter a valid or different username"
            return render_template ("register.html", message1 = message)


        if not password or password != confirmation:
            message = "Enter a password or passwords don't match"
            return render_template ("register.html", message2 = message)

        if not question1 or  not question2:
            message = "Invalid answer"
            return render_template ("register.html", message3 = message)

        db_users.execute("INSERT INTO users (username, hash, question1, hash1, question2, hash2) VALUES (?,?,?,?,?,?)",
                username, generate_password_hash(password), question1, generate_password_hash(question1), question2, generate_password_hash(question2))

        return redirect("/")


@app.route("/login", methods=["POST", "GET"])
def login():
    session.clear()
    if request.method == "POST":

        if not request.form.get("username"):
            message = "Enter an username"
            return render_template("login.html", message=message)

        if not request.form.get("password"):
            message = "Enter a password"
            return render_template("login.html", message=message)

        dico = db_users.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(dico) != 1 or not check_password_hash(
            dico[0]["hash"], request.form.get("password")
        ):
            message = "Invalid username or password"
            return render_template("login.html", message=message)

        session["id"] = dico[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")



@app.route("/", methods=["POST", "GET"])
@login_required
def index():

    years, liste = helpers.query()

    if request.method == "GET":
        return render_template("index.html", years=years, liste=liste)

    else:
        if request.form.get("year"):
            year = int(request.form.get("year"))
            dico = db_users.execute("SELECT * FROM years WHERE year = ? AND user_id = ?", year, session["id"])

            if request.form.get("action") == "add":
                if len(dico) != 0:
                    flash("year already exists")
                    return redirect ("/")
                db_users.execute("INSERT INTO years (year, user_id) VALUES (?, ?)", year, session["id"])
                return redirect ("/")
            else:
                if len(dico) == 0:
                    flash("year doesn't exists")
                    return redirect ("/")
                else:
                    try:
                        db_users.execute("DELETE FROM exams WHERE year = ? AND user_id = ?", year, session["id"])
                    except:
                        pass

                    db_users.execute("DELETE FROM years WHERE year = ? AND user_id = ?", year, session["id"])
                    db_users.execute("DELETE FROM grades WHERE year = ? AND user_id = ?", year, session["id"])
                    return redirect ("/")
        else:
            flash("Invalid input")
            return redirect("/")



@app.route("/askchange", methods=["POST", "GET"])
def askchange():
    return render_template("passwordchanging.html")


@app.route("/passwordchanging", methods=["POST", "GET"])
def passwordchanging():
    if request.method == "POST":
        try: # this try-except helps us make sure the user is logged in otherwise we can have an error
            if session["id"]:
                years, liste = helpers.query()
                if request.form.get("newpassword").split() and request.form.get("newpassword") == request.form.get("confirmation"):
                    db_users.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(request.form.get("newpassword")), session["id"])
                    return redirect("/")
                else:
                    flash("Passwords don't match or invalid input")
                    return render_template("settings.html", years=years, liste=liste)
        except:

            check = db_users.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
            if len(check) == 0:
                message = "Invalid username"
                return render_template ("passwordchanging.html", message = message)
            else:
                user = check[0]["id"]
                hash1 = db_users.execute("SELECT * FROM users WHERE id = ?", user)[0]["hash1"]
                hash2 = db_users.execute("SELECT * FROM users WHERE id = ?", user)[0]["hash2"]

                if check_password_hash(hash1, request.form.get("question1")) and check_password_hash(hash2, request.form.get("question2")):
                    if not request.form.get("password").strip() or request.form.get("password") != request.form.get("confirmation"): # no blank password allowed
                        message = "Invalid password or passwords don't match"
                        return render_template ("passwordchanging.html", message = message)
                    else:
                        db_users.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(request.form.get("password")), user)
                        return redirect("/login")
                else:
                    message = "Incorrect answers"
                    return render_template ("passwordchanging.html", message = message)
    else:
        return render_template ("passwordchanging.html")



@app.route("/grades", methods=["POST", "GET"])
@login_required
def grades():

    years, liste = helpers.query()
    semester = request.form.get("semester") # here I used post method because by choosing a semester an information is send to the server
    return render_template("grades.html", years=years, semester=semester, liste=liste)


@app.route("/gradeschange", methods=["POST", "GET"])
@login_required
def gradeschange():

    semester = request.form.get("semester")
    years, liste = helpers.query()

    if request.method == "POST":
        course = request.form.get("course").capitalize()
        exam = request.form.get("exam")
        year = request.form.get("year")

        if request.form.get("action") == "add":

            if not request.form.get("course") or not request.form.get("exam") or not request.form.get("rowgrades") or not request.form.get("weigth") or not request.form.get("year"):
                flash("Invalid input")

            else:

                rowgrades = float(request.form.get("rowgrades"))
                weigth = int(request.form.get("weigth"))
                grades = (rowgrades * weigth) / 100

                course_list = db_users.execute("SELECT * FROM grades WHERE course = ? AND user_id = ? AND semester = ? AND year = ?", course, session["id"], semester, year)

                # check if this course has already been added by this user
                if len(course_list) == 0: # if not

                    query = "INSERT INTO grades (user_id, course, exam1, grades1, weigth, year, semester) VALUES (?,?,?,?,?,?,?)"
                    db_users.execute(query, session["id"], course, exam, grades, weigth, year, semester)
                    course_list = db_users.execute("SELECT * FROM grades WHERE course = ? AND user_id = ? AND semester = ? AND year = ?", course, session["id"], semester, year)
                    course_id = course_list[0]["id"]
                    db_users.execute("INSERT INTO exams (course_id, user_id, exam, semester, year, grades, rowgrades) VALUES (?, ?, ?, ?, ?, ?,?)", course_id, session["id"], exam, semester, year, grades, rowgrades)

                else: # if so

                    course_id = course_list[0]["id"]
                    exam_list = db_users.execute("SELECT * FROM exams WHERE course_id = ? AND user_id = ? AND exam = ? AND semester = ? AND year = ?", course_id, session["id"], exam, semester, year)
                    if len(exam_list) == 0: # si période pas encore ajouté pour ce cours
                        db_users.execute("INSERT INTO exams (course_id, user_id, exam, semester, year, grades, rowgrades) VALUES (?, ?, ?, ?, ?, ?, ?)", course_id, session["id"], exam, semester, year, grades, rowgrades)
                        number_exam = db_users.execute("SELECT SUM(value) FROM exams WHERE course_id = ? AND user_id = ? AND semester = ? AND year = ?", course_id, session["id"], semester, year)[0]["SUM(value)"]
                        new_exam = f"exam{number_exam}"
                        new_grades = f"grades{number_exam}"
                        value = db_users.execute(f"SELECT * FROM grades")

                        # check if the column already exists and create it if it doesnt
                        try:
                            key = value[0][new_exam]
                        except:

                            query = f"ALTER TABLE grades ADD COLUMN {new_exam} TEXT DEFAULT NULL"
                            db_users.execute(query)
                            query2 = f"ALTER TABLE grades ADD COLUMN {new_grades} REAL DEFAULT 0.0" # je n'ai pas pu ajouter deux colonnes à la fois
                            db_users.execute(query2)
                            query3 = f"UPDATE grades SET {new_exam} = ?, {new_grades} = ? WHERE course = ? AND user_id = ? AND semester = ? AND year = ?"
                            db_users.execute(query3, exam, grades, course, session["id"], semester, year)

                        # updating the column if it already exists
                        else:
                            query = f"UPDATE grades SET {new_exam} = ?, {new_grades} = ? WHERE course = ? AND user_id = ? AND semester = ? AND year = ?"
                            db_users.execute(query, exam, grades, course, session["id"], semester, year)

                    else: # if exam already added

                        db_users.execute("UPDATE grades SET grades1 = ?, weigth = ? WHERE course = ? AND user_id = ? AND semester = ? AND year = ?", grades, weigth, course, session["id"], semester, year)
                        db_users.execute("UPDATE exams SET grades = ?, rowgrades = ? WHERE course_id = ? AND exam = ? AND user_id = ? AND year = ? AND semester = ?", grades, rowgrades, course_id, exam, session["id"], year, semester)

        else:
            if course and year:

                year = int(year)
                course_list = db_users.execute("SELECT * FROM grades WHERE course = ? AND user_id = ? AND semester = ? AND year = ?", course, session["id"], semester, year)
                if len(course_list) == 0:

                    flash("Invalid input or Course not completed")

                else:
                    course_id = course_list[0]["id"]
                    db_users.execute("DELETE FROM exams WHERE course_id = ? AND year = ? AND semester = ? AND user_id = ?", course_id, year, semester, session["id"]) # delete the table where this value is a foreign key first
                    db_users.execute("DELETE FROM grades WHERE course = ? AND year = ? AND semester = ? AND user_id = ?", course, year, semester, session["id"])

            else:
                flash("Invalid input or Course not completed")


    return render_template("grades.html", years=years, semester=semester, liste=liste) # stay on this page regardless of the method


@app.route("/results", methods=["POST", "GET"])
@login_required
def results():
    course = request.form.get("question").capitalize()
    years, liste = helpers.query()

    if request.method == "POST":

        query = "SELECT * FROM grades WHERE user_id = ? AND course = ?"
        check = db_users.execute(query, session["id"], course)

        if not course or len(check) == 0:
            print(check)
            flash("Invalid input or course doesnt exist")
            return redirect("/")

        else:

            query2 = """
                SELECT grades.course, grades.semester, grades.year,
                    SUM(exams.grades) AS total
                FROM grades
                JOIN exams ON grades.id = exams.course_id
                WHERE grades.user_id = ? AND grades.course = ?
                GROUP BY grades.course, grades.semester, grades.year;
        """
            course_list = db_users.execute(query2, session["id"], course)
            return render_template("results.html", years=years, liste=liste, course_list=course_list)
    else:

        return redirect("/")

@app.route("/settings", methods=["POST", "GET"])
@login_required
def settings():

    years, liste = helpers.query()
    if request.method == "GET":
        return render_template("settings.html", years=years, liste=liste)

    else:
        if request.form.get("question1") and request.form.get("answer1"):
            hash1 = db_users.execute("SELECT * FROM users WHERE id = ?", session["id"])[0]["hash1"]
            if check_password_hash(hash1, request.form.get("question1")):
                db_users.execute("UPDATE users SET hash1 = ? WHERE id = ?", generate_password_hash(request.form.get("answer1")), session["id"])
                return redirect ("/")
            else:
                flash("Incorrect answer")
                return render_template("settings.html", years=years, liste=liste)


        if request.form.get("question2") and request.form.get("answer2"):
            hash2 = db_users.execute("SELECT * FROM users WHERE id = ?", session["id"])[0]["hash2"]
            if check_password_hash(hash2, request.form.get("question2")):
                db_users.execute("UPDATE users SET hash2 = ? WHERE id = ?", generate_password_hash(request.form.get("answer2")), session["id"])
                return redirect ("/")

        else:
            flash("Invalid input")
            return render_template("settings.html", years=years, liste=liste)



@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")




