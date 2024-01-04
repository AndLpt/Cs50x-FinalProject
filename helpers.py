from functools import wraps
from flask import redirect, render_template, session
from cs50 import SQL


db_users = SQL("sqlite:///users.db")

# I borrowed this function from Cs50x PS9 Finance it is very handy to handle wich page is accessible for logged in users only
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login") # c'est ce helper qui redirige vers page d'acceuil lorsque user pas authentifié
        return f(*args, **kwargs)
    return decorated_function


def query(): # I made this custom function to avoid repetiting the same code over and over

        years = db_users.execute("SELECT year FROM years WHERE user_id = ? ORDER BY year DESC", session["id"])
        query = """
            SELECT grades.course, grades.year, SUM(exams.grades) AS total, GROUP_CONCAT(exams.exam) AS exams, GROUP_CONCAT(exams.grades) AS grades,
            GROUP_CONCAT(exams.rowgrades) as rowgrades
            FROM grades
            JOIN exams ON grades.id = exams.course_id
            WHERE grades.semester = ?
            AND grades.user_id = ?
            GROUP BY grades.course;
            """


        dico_fall = db_users.execute(query, "fall", session["id"])
        for i in range(len(dico_fall)):
            dico_fall[i]["total"] = round(dico_fall[i]["total"], 2)  # make sure the value are rounded before they are displayed to the user

        dico_winter = db_users.execute(query, "winter", session["id"])
        for i in range(len(dico_winter)):
            dico_winter[i]["total"] = round(dico_winter[i]["total"], 2)

        dico_summer = db_users.execute(query, "summer", session["id"])
        for i in range(len(dico_summer)):
            dico_summer[i]["total"] = round(dico_summer[i]["total"], 2)


        liste = [("Fall", dico_fall), ("Winter", dico_winter), ("Summer", dico_summer)]
        return years, liste

