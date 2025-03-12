from flask import Blueprint,render_template, session, request,redirect
from database import DatabaseHandler

viewTournamentBlueprint = Blueprint("viewTournament",__name__)


@viewTournamentBlueprint.route("/viewTournament", methods = ["POST"])
#creates the route for the viewTournament blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def viewTournament():
    #defines viewTournament function for the viewTournament blueprint
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    enteredViewCode = request.form["enteredViewCode"]
    session["Viewing"] = True
    if db.checkViewCodes(enteredViewCode) == None:
        session["viewCodeInputError"] = "The entered view code does not exist"
        return redirect("/dashboard")
    else:
        session["viewCodeInputError"] = ""
        tournamentName = db.getTournamentName(enteredViewCode)
        session["Tournament"] = tournamentName
        return redirect("/tournamentDashboard")
