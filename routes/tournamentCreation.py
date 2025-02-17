from flask import Blueprint,render_template, session, request,redirect
from database import DatabaseHandler
import math
import random 
#import math module so log2 can be performed for number of rounds

creationFormBlueprint = Blueprint("creationForm",__name__)
tournamentCreationBlueprint = Blueprint("tournamentCreation",__name__)
tournamentDashboardBlueprint = Blueprint("tournamentDashboard",__name__)
teamsInputPageBlueprint = Blueprint("teamsInputPage",__name__)
bracketViewBlueprint = Blueprint("bracketView",__name__)
teamsInputBlueprint = Blueprint("teamsInput",__name__)
teamDeletionBlueprint = Blueprint("teamDeletion",__name__)
clearTeamsBlueprint = Blueprint("clearTeams",__name__)
bracketGenerationBlueprint = Blueprint("bracketGeneration",__name__)
bracketDisplayBlueprint = Blueprint("bracketDisplay",__name__)
generateViewCodeBlueprint = Blueprint("generateViewCode",__name__)



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
    if len(teams)< numTeams:
        session["teamInputError"] = "Not enough teams entered" 
        return redirect("/teamsInputPage")
    else:
        generateBrackets()
        return render_template("bracketView.html", brackets = bracketDisplay(), numberOfRounds = int(math.log2(numTeams)))



@bracketGenerationBlueprint.route("/bracketGeneration")
def generateBrackets():
    db = DatabaseHandler("appData.db")
    teamsList=teams
    numberOfTeams = numTeams
    numRounds = int(math.log2(numberOfTeams))
    bracket = {}

    for i in range(numRounds):
        round = {}
        bracket[i+1]= round
        numMatches = numberOfTeams // 2
        for i in range(numMatches):
            round[i+1] = {1:None, 2:None}
            
        numberOfTeams = numberOfTeams // 2

    for i in range (numTeams//2):
        team1 = teamsList.pop(0)
        team2 = teamsList.pop(0)
        bracket[1][i+1][1] = team1
        bracket[1][i+1][2] = team2

    return db.addBrackets(str(bracket), session["Tournament"])

@bracketDisplayBlueprint.route("/bracketDisplay")
def bracketDisplay():
    db = DatabaseHandler("appData.db")
    results = db.getBrackets(session["Tournament"])
    brackets = (results[4])
    brackets = eval(brackets)
    return brackets

@tournamentDashboardBlueprint.route("/tournamentDashboard")
def tournamentDashboard():
    db = DatabaseHandler("appData.db")
    db.updateActiveTrue(session["Tournament"])
    return render_template("tournamentDashboard.html", viewCode = generateViewCode())


@generateViewCodeBlueprint.route("/generateViewCode")
def generateViewCode():
    db = DatabaseHandler("appData.db")
    results = "notnone"
    while results != None:
        viewCode = str(random.randint(100000,999999))
        results = db.getViewCodes(viewCode)
        

    db.addViewCode(viewCode, session["Tournament"])

    return viewCode

    
    

    
