from flask import Blueprint, redirect, render_template, request, session
from database import DatabaseHandler



signupBlueprint = Blueprint("signup",__name__)
createUserBlueprint = Blueprint("createUser",__name__)
authenticateUserBlueprint = Blueprint("authenticateUser",__name__)
logoutBlueprint = Blueprint("logout",__name__)
deleteUserBlueprint = Blueprint("deleteUser",__name__)
deleteAccountBlueprint = Blueprint("deleteAccount",__name__)


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
    errorMessage = session.get("errorMessage") if session.get("errorMessage") else ""
    
    return render_template("SignUp.html", error = errorMessage)


@createUserBlueprint.route("/createUser", methods = ["post"])
def createUser():
    db=DatabaseHandler("appData.db")
    username = request.form["username"]
    password=request.form["password"]
    repassword=request.form["repassword"]

    response = db.createUser(username,password)
    if response==True:
        session["errorMessage"] = ""
        return redirect("/")
    elif password != repassword:
        session["errorMessage"] = "Passwords do not match"
        return redirect("/signup")
    elif len(username) >=16:
        session["errorMessage"] = "Username too long, must be less than 16 Characters."
        return redirect("/signup")
    elif len(username) <= 3:
        session["errorMessage"] = "Username too short, must be more than 3 Characters. "
        return redirect("/signup")
    elif len(password) <= 6:
        session["errorMessage"] = "Password too short, must be more than 6 Characters. "
        return redirect("/signup")
    elif any(char.isdigit() for char in password) == False:
        session["errorMessage"] = "Password must include number"
        return redirect("/signup")
    else:
        session["errorMessage"] = "This username is taken"
        return redirect("/signup")







# @deleteUserBlueprint.route("/deleteUser", methods = ["get"])
# def deleteUser():
#     db = DatabaseHandler("appData.db")
    
#     if db.deleteUser(session["currentUser"])==True:
#         session["accountDeletionError"] = ""
#         session.clear()
#         return redirect("/")
#     else:
#         session["accountDeletionError"] = "Error deleting Account"
#         return redirect("/dashboard")
    
@deleteUserBlueprint.route("/deleteUser", methods = ["post"])
def deleteUser():
    db = DatabaseHandler("appData.db")
    username = request.form["username"]
    
    if username == session["currentUser"]:
        session["accountDeletionError"] = ""
        db.deleteUser(username)
        return redirect("/")
    else:
        session["accountDeletionError"] = "This is not your username"
        return redirect("/deleteAccount")
        

@deleteAccountBlueprint.route("/deleteAccount")
def deleteAccount():
    session["viewCodeInputError"] = ""
    #clears the view code input errors session so it does not remain present when returning to the user's dashboard
    accountDeletionError = session.get("accountDeletionError") if session.get("accountDeletionError") else ""
    return render_template("deleteAccount.html", error = accountDeletionError)

