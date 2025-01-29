from flask import Blueprint,render_template, session, request,redirect
from database import DatabaseHandler
import math

creationFormBlueprint = Blueprint("creationForm",__name__)
tournamentCreationBlueprint = Blueprint("tournamentCreation",__name__)
tournamentDashboardBlueprint = Blueprint("tournamentDashboard",__name__)
teamsInputPageBlueprint = Blueprint("teamsInputPage",__name__)
bracketViewBlueprint = Blueprint("bracketView",__name__)
teamsInputBlueprint = Blueprint("teamsInput",__name__)
bracketGenerationBlueprint = Blueprint("bracketGeneration",__name__)

@creationFormBlueprint.route("/creationForm")
def creationForm():
    Error = session.get("tournamentCreationError") if session.get("tournamentCreationError") else ""
    return render_template("creationForm.html", error = Error)

@tournamentCreationBlueprint.route("/tournamentCreation", methods = ["POST"])
def tournamentCreation():
    db = DatabaseHandler("appData.db")
    tournamentName = request.form["tournamentName"]
    numTeams = request.form["numTeams"]
    session["Tournament"] = tournamentName
    if db.createTournament(tournamentName,session["currentUser"],numTeams,None)==True:
        session["tournamentCreationError"] = ""
        return redirect("/teamsInputPage")
    elif len(tournamentName)<=4:
        session["tournamentCreationError"] = "Tournament name too short, must be over 4 characters"
        return redirect("/creationForm")
    elif len(tournamentName)>=30:
        session["tournamentCreationError"] = "Tournament name too long, must be under 30 characters"
        return redirect("/creationForm")
    else:
        session["tournamentCreationError"] = "Tournament name already taken"
        return redirect("/creationForm")
        



@teamsInputPageBlueprint.route("/teamsInputPage")
def teamsInputPage():
    return render_template("teamsInput.html")

teams = []
@teamsInputBlueprint.route("/teamsInput", methods = ["POST"])
def teamsInput():
    newTeamName = request.form["teamNames"]
    teams.append(newTeamName)
    session["Teams"] = teams
    return render_template("teamsInput.html")
    
    
    
@bracketViewBlueprint.route("/bracketView")
def bracketView():
    return render_template("bracketView.html")

@bracketGenerationBlueprint.route("/bracketGeneration")
def generateBrackets(numTeams):
    db = DatabaseHandler("appData.db")
    rounds = int(math.log2(numTeams)) #--> 16 : 4
    tournament = {}
    db.createTournament(session["Tournament"], session["currentUser"],numTeams, rounds)

    for i in range(rounds):

        numberOfMatches = numTeams // 2
        for i in range(numberOfMatches):
            tournament[i+1] = {"p1":None, "p2":None}
           
        numTeams = numTeams // 2
       
    


    return tournament
