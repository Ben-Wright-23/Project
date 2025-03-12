from flask import Blueprint,render_template, session, request,redirect
from database import DatabaseHandler

viewTournamentBlueprint = Blueprint("viewTournament",__name__)
#create a flask blueprint for the function to handle the view code inputs and either allow the user to view the tournament or display an error


@viewTournamentBlueprint.route("/viewTournament", methods = ["POST"])
#creates the route for the viewTournament blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def viewTournament():
    #defines viewTournament function for the viewTournament blueprint
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    enteredViewCode = request.form["enteredViewCode"]
    #takes the entered view code from the view code input on the dashboard, using the form input with name "enteredViewCode".
    session["Viewing"] = True
    #sets the viewing session to be true, indication the tournament is currently being viewed so access should be restricted
    if db.checkViewCodes(enteredViewCode) == None:
        session["viewCodeInputError"] = "The entered view code does not exist"
        #if the view code is not present in the database, an error is returned to the user stating this
        return redirect("/dashboard")
        #reloads the dashboard page with this error displayed
    else:
        session["viewCodeInputError"] = ""
        #clears the view code input errors session as no error has occured with the view code input
        tournamentName = db.getTournamentName(enteredViewCode)
        #retrieves the tournament name of the tournament that has had its view code entered
        session["Tournament"] = tournamentName
        #sets the tournament session to be the tournament name, so the correct tournament dashboard can be displayed
        return redirect("/tournamentDashboard")
        #loads the restricted tournament dashboard for the tournament that has had its view code entered
