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
teamDeletionBlueprint = Blueprint("teamDeletion",__name__)
clearTeamsBlueprint = Blueprint("clearTeams",__name__)
bracketDisplayBlueprint = Blueprint("bracketDisplay",__name__)



@creationFormBlueprint.route("/creationForm")
def creationForm():
    session["teamInputError"] = ""
    session["teamDeletionError"] = ""
    Error = session.get("tournamentCreationError") if session.get("tournamentCreationError") else ""
    return render_template("creationForm.html", error = Error)
    


teams = []



@tournamentCreationBlueprint.route("/tournamentCreation", methods = ["POST"])
def tournamentCreation():
    session["Teams"] = ""
    teams.clear()
    db = DatabaseHandler("appData.db")
    tournamentName = request.form["tournamentName"]
    global numTeams
    numTeams = request.form["numTeams"]
    numTeams = int(numTeams)
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
    Error = session.get("teamInputError") if session.get("teamInputError") else ""
    DeletionError = session.get("teamDeletionError") if session.get("teamDeletionError") else ""
    return render_template("teamsInput.html", error = Error, error2 = DeletionError)

@teamsInputBlueprint.route("/teamsInput", methods = ["POST"])
def teamsInput():
    if len(teams)<int(numTeams):
        newTeamName = request.form["teamNames"]
        for i in teams:
            if newTeamName==i:
                session["teamInputError"] = "Teams must have unique name"
                session["Teams"] = session["Teams"]
                return redirect("/teamsInputPage")
        if newTeamName != "":
            teams.append(newTeamName)
            session["Teams"] = teams
            session["teamInputError"] = ""
            return redirect("/teamsInputPage")
        else:
            session["teamInputError"] = "Team must have a name"
            return redirect("/teamsInputPage")
    else:
        session["teamInputError"] = "Your amount of teams has been reached"
        return redirect("/teamsInputPage")


@teamDeletionBlueprint.route("/teamDeletion", methods = ["POST"])
def teamDeletion():
    toDelete = request.form["teamDeletion"]
    for i in teams:
        if i == toDelete:
            teams.remove(toDelete)
            session["Teams"] = teams
            session["teamDeletionError"] = ""
        else:
            session["teamDeletionError"] = "Team not in tournament"
    
    return redirect("/teamsInputPage")

@clearTeamsBlueprint.route("/clearTeams", methods = ["POST"])
def clearTeams():
    teams.clear()
    session["Teams"] = teams
    return redirect("/teamsInputPage")

    
    
@bracketViewBlueprint.route("/bracketView")
def bracketView():
    return render_template("bracketView.html")
# , brackets=redirect("/bracketDisplay")),redirect("/bracketGeneration")


@bracketGenerationBlueprint.route("/bracketGeneration")
def generateBrackets():
    db = DatabaseHandler("appData.db")
    global teamsList
    teamsList = teams
    numberOfTeams = numTeams
    numRounds = int(math.log2(numberOfTeams))
    bracket = {}

    for i in range(numRounds):
        round = {}
        bracket[i+1]= round
        numMatches = numberOfTeams // 2
        for i in range(numMatches):
            round[i+1] = {"T1":None, "T2":None}
            
        numberOfTeams = numberOfTeams // 2

    for i in range (numTeams//2):
        team1 = teams.pop(0)
        team2 = teams.pop(0)
        bracket[1][i+1]["T1"] = team1
        bracket[1][i+1]["T2"] = team2

    return db.addBrackets(str(bracket), session["Tournament"])

@bracketDisplayBlueprint.route("/bracketDisplay")
def bracketDisplay():
    db = DatabaseHandler("appData.db")
    brackets = db.getBrackets(session["Tournament"])
    brackets = eval(brackets)

    return brackets


