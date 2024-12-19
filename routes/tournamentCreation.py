from flask import Blueprint,render_template, session, request,redirect
from database import DatabaseHandler


creationFormBlueprint = Blueprint("creationForm",__name__)
tournamentCreationBlueprint = Blueprint("tournamentCreation",__name__)

@creationFormBlueprint.route("/creationForm")
def creationForm():
    Error = session.get("tournamentCreationError") if session.get("tournamentCreationError") else ""
    return render_template("creationForm.html", error = Error)

@tournamentCreationBlueprint.route("/tournamentCreation", methods = ["POST"])
def tournamentCreation():
    db = DatabaseHandler("appData.db")
    tournamentName = request.form["tournamentName"]
    numTeams = request.form["numTeams"]

    if db.createTournament(tournamentName,session["currentUser"],numTeams)==True:
        session["tournamentCreationError"] = ""
        return redirect("/tournamentView")
    elif len(tournamentName)<=4:
        session["tournamentCreationError"] = "Tournament name too short, must be over 4 characters"
        return redirect("/creationForm")
    elif len(tournamentName)>=30:
        session["tournamentCreationError"] = "Tournament name too long, must be under 30 characters"
        return redirect("/creationForm")
    elif numTeams =="":
        session["tournamentCreationError"] = "Enter number of teams"
        return redirect("/creationForm")
    else:
        session["tournamentCreationError"] = "Tournament name already taken"
        return redirect("/creationForm")
        
