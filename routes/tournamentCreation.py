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
    #defines teamsInput function   for the teams input blueprint
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
            #Update the session for teams to be the new list of teams so it can be displayed to the user in the teamsInput html page
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
#creates the route for the teamDeletion blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def teamDeletion():
    #defines teamsDeletion function for the team deletion blueprint
    toDelete = request.form["teamDeletion"]
    #takes the entered team name to be deleted sent from the teamsInput page(the client) to the server, using the form input with id "teamDeletion".
    for i in teams:
        if i == toDelete:
            #Cycles through every team in the list, checking if it matches the name of the team to be deleted
            teams.remove(toDelete)
            #Removes the entered team name from the teams list and therefore tournament
            session["Teams"] = teams
            #Update the session for teams to be the new list of teams so it can be displayed to the user in the teamsInput html page
            session["teamDeletionError"] = ""
            #The team has been deleted successfully so there is no error with the team deletion
        else:
            session["teamDeletionError"] = "Team not in tournament"
            #If the team name has not been found in the list, the team is not in the tournament so this error is displayed to the user
    
    return redirect("/teamsInputPage")
    #Reloads the teams input page with any errors or changes to the team list

@clearTeamsBlueprint.route("/clearTeams", methods = ["POST"])
#creates the route for the clearTeams blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def clearTeams():
    #defines clearTeams function for the team deletion blueprint
    teams.clear()
    #Clears all teams from the team list
    session["Teams"] = teams
    #Updates the session for teams to be empty, matching the teams list
    return redirect("/teamsInputPage")
    #Reloads the teamsInput page with all teams removed from the list
    
    
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
