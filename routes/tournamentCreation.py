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



@creationFormBlueprint.route("/creationForm")
def creationForm():
    session["teamDeletionError"] = ""
    session["teamInputError"] = ""
    Error = session.get("tournamentCreationError") if session.get("tournamentCreationError") else ""
    return render_template("creationForm.html", error = Error)


teams = []


@tournamentCreationBlueprint.route("/tournamentCreation", methods = ["POST"])
def tournamentCreation():
    session["Teams"] = ""
    db = DatabaseHandler("appData.db")
    tournamentName = request.form["tournamentName"]
    global numTeams
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
#creates the route for the teamsInputPage blueprint, allowing it to be accessed easily
def teamsInputPage():
    #defines function to load teamsInputPage
    Error = session.get("teamInputError") if session.get("teamInputError") else ""
    DeletionError = session.get("teamDeletionError") if session.get("teamDeletionError") else ""
    #Produces the errors with the team inputting or deleting if there is one
    #if no error for either, no error is passed for that error to the interface
    return render_template("teamsInput.html", error = Error, error2 = DeletionError)
    #loads the creationForm.html page, with the error messages displayed when it is reloaded

@teamsInputBlueprint.route("/teamsInput", methods = ["POST"])
#creates the route for the teamsInput blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def teamsInput():
    #defines teamsInput function  
    if len(teams)<int(numTeams):
        #creates condition to check there is less teams in the list/tournament than the user previously specified was how many teams their tournament would contain
        newTeamName = request.form["teamNames"]
        #takes the entered team name sent from the teamsInput page(the client) to the server, using the form input with id "teamNames".
        # for i in teams:
        #     if newTeamName==i:
        #         session["teamInputError"] = "Teams must have unique name"
        #         session["Teams"] = session["Teams"]
        #         return redirect("/teamsInputPage")
        if newTeamName != "":
            #Checks the user has entered a value for the team name
            teams.append(newTeamName)
            #adds the new team to the list of teams if there is a team name entered
            session["Teams"] = teams
            #update the session for teams to be the new list of teams so it can be displayed to the user in the teamsInput html page
            session["teamInputError"] = ""
            #The team entered is valid so there is no error with the team input
            return redirect("/teamsInputPage")
            #Reloads the teamInput page with the new team added to the list displayed to the user
        else:
            session["teamInputError"] = "Team must have a name"
            #If no name for the team entered, output an error message stating this
            return redirect("/teamsInputPage")
            #Reloads the teamInput page with the error displayed to the user
    else:
        session["teamInputError"] = "Your amount of teams has been reached"
        #If there are as many teams in the list as that the user has said their tournament should contain, the new team is not entered and this error is displayed
        return redirect("/teamsInputPage")
        #Reloads the teamInput page with the error displayed to the user


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

@bracketGenerationBlueprint.route("/bracketGeneration")
def generateBrackets():
    rounds = int(math.log2(numTeams)) #--> 16 : 4
    tournament = {}
    for i in range(rounds):

        numberOfMatches = numTeams // 2
        for i in range(numberOfMatches):
            tournament[i+1] = {"p1":None, "p2":None}
           
        numTeams = numTeams // 2
       
    return tournament
