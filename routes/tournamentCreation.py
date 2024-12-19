from flask import Blueprint,render_template, session, request,redirect
from database import DatabaseHandler


creationFormBlueprint = Blueprint("creationForm",__name__)
tournamentCreationBlueprint = Blueprint("tournamentCreation",__name__)

@creationFormBlueprint.route("/creationForm")
def creationForm():
    Error = session.get("tournamentCreationError") if session.get("tournamentCreationError") else ""
    return render_template("creationForm.html", error = Error)

@tournamentCreationBlueprint.route("/creationForm")
def tournamentCreation():
    db = DatabaseHandler("appData.db")
    tournamentName = request["tournamentName"]
    numTeams = request["numTeams"]

    if db.createTournament(tournamentName,session["currentUser"],numTeams)==True:
        session["tournamentCreationError"] = ""
        return redirect("/tournamentView")
    elif len(tournamentName)<=4:
        session["tournamentCreationError"] = ""
        return redirect("/creationForm")

