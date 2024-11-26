from flask import Blueprint, redirect, render_template, request, session
from database import DatabaseHandler



signupBlueprint = Blueprint("signup",__name__)
createUserBlueprint = Blueprint("createUser",__name__)
authenticateUserBlueprint = Blueprint("authenticateUser",__name__)
logoutBlueprint = Blueprint("logout",__name__)


@logoutBlueprint.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@authenticateUserBlueprint.route("/authenticate", methods = ["post"])
def authenticateUser():
    db = DatabaseHandler("appData.db")
    username = request.form["username"]
    password = request.form["password"]

    if db.authenticateUser(username, password) == True:
        session["currentUser"] = username
        return redirect("/dashboard")
    else:
        return redirect("/")



@signupBlueprint.route("/signup")
def signup():
    return render_template("SignUp.html")


@createUserBlueprint.route("/createUser", methods = ["post"])
def createUser():
    db=DatabaseHandler("appData.db")
    username = request.form["username"]
    password=request.form["password"]
    repassword=request.form["repassword"]
    message=""

    if len(username) >=16:
        message = message + "Username too long, must be less than 16 Characters. "
    if len(username) <= 3:
        message = message + "Username too short, must be more than 3 Characters. "
    if len(password) <= 6:
        message = message + "Password too short, must be more than 6 Characters. "
    if any(char.isdigit() for char in password) == False:
        message = message + "Password does not contain a number. "
    if password != repassword:
        message = message + "Passwords do not match. "


    response = db.createUser(username,password)
    if response==True:
        return redirect("/")
    else:
        return ...

