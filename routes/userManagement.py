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

    if password == repassword:
        response = db.createUser(username,password)
        if response==True:
            return redirect("/")
        else:
            return "<h1>Error making account</h1>"
    return "<h1>Passwords dont match</h1>"