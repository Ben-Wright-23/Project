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
#create a flask blueprint for the function to load generate the unique view code and add it to the database
myTournamentsPageBlueprint = Blueprint("myTournamentsPage",__name__)
tournamentDashboardRedirectBlueprint = Blueprint("tournamentDashboardRedirect",__name__)
deleteTournamentBlueprint = Blueprint("deleteTournament",__name__)
teamsInputRedirectBlueprint = Blueprint("teamsInputRedirect",__name__)
bracketViewRedirectBlueprint = Blueprint("bracketViewRedirect",__name__)

@creationFormBlueprint.route("/creationForm")
def creationForm():
    session["teamInputError"] = ""
    session["teamDeletionError"] = ""
    session["viewCodeInputError"] = ""
    #clears the view code input errors session so it does not remain present when returning to the user's dashboard
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
    session["Viewing"] = False
    #sets the viewing session to false so when the tournament dashboard is loaded from the bracketView page when a tournament is being created,
    #all functions are displayed as it is the tournament organiser accessing the tournament
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
    results = db.getTournamentFields(session["Tournament"])
    brackets = (results[4])
    brackets = eval(brackets)
    return brackets

@tournamentDashboardBlueprint.route("/tournamentDashboard")
def tournamentDashboard():
    session["FixtureInfoInputError"] = ""
    #defines the FixtureInfoInputError session or clears the session containing errors with fixture information inputs so they are not already present from other tournaments when the fixture information input page is loaded
    session["scoreInputError"] = ""
    #defines the scoreInputError session or clears the session containing errors with score inputs,
    #so they are not already present from other tournaments when the scores input page is loaded
    session["viewCodeInputError"] = ""
    #clears the view code input errors session so it does not remain present when returning to the user's dashboard
    db = DatabaseHandler("appData.db")
    db.updateActiveTrue(session["Tournament"])
    results = db.getTournamentFields(session["Tournament"])
    #retrieves all the fields for the current tournament and sets the list retrieved to be results
    viewCode = results[5]
    #sets viewCode to be the sixth item in the list of current tournament fields as this represents the view code
    viewCode = eval(viewCode)
    #turns the view code back to its origional string form
    if results[6] != None:
        #if the seventh item of results is not None, this signifies the fixture information for the tournament has already been inputted
        fixturesInfoInputted="True"
        #sets fixturesInfoInputted to be True to signify the fixture information for the tournament has already been inputted so the fixtures page should be loaded if the Fixtures button is pressed on the tournament dashboard
    else:
        #if the seventh item of results is None, this signifies the fixture information for the tournament has not already been inputted
        fixturesInfoInputted="False"
        #sets fixturesInfoInputted to be False to signify the fixture information for the tournament has not already been inputted so the fixture info input page should be loaded if the Fixtures button is pressed on the tournament dashboard
    matchScores = results[9]
    #sets brackets to be the fith value from the fields list as this represents that tournament's brackets
    matchScores = eval(matchScores)
    #turns the brackets back to their origional dictionary form
    numTeams = int(results[2])
    #sets numTeams to be the integer version of the third item in results, which represents the current tournament's number of teams
    numRounds = int(math.log2(numTeams))
    #the number of rounds for the tournament is log2 of the number of teams in the tournament
    return render_template("tournamentDashboard.html", viewCode = viewCode, fixturesInfoInputted= fixturesInfoInputted, matchScores = matchScores, numberOfRounds = numRounds)
    #loads the tournamentDashboard html page with the view code for the tournament from the database passed with it to be displayed
    #also passes in whether the fixture information has been inputted yet so the program can choose whether the fixture info input page should be loaded or the fixtures page should be loaded when the Fixtures button is pressed
    #also passes in the matchScores dictionary and number of rounds to be used to determine whether the end tournament button should be disabled or enabled


@generateViewCodeBlueprint.route("/generateViewCode")
#creates the route for the generateViewCode blueprint, allowing it to be accessed easily.
def generateViewCode():
    #defines generateViewCode function for the generateViewCode blueprint
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    results = "notnone"
    #sets the results local variable to be a value that is not None so the while loop begins 
    while results != None:
        #If the return from the database check for the new view code is not None, this means the view code is already being used in the database for a different tournament. 
        #This means a new view code should be generated and checked for in the database so the while loop should continue
        viewCode = str(random.randint(100000,999999))
        #generates a random 6 digit number, makes it a string and assigns it to the variable viewCode
        results = db.checkViewCodes(viewCode)
        #assigns the return from the checkViewCodes database function when this 6 digit string is checked for and assigns it to the results variable
        

    db.addViewCode(viewCode, session["Tournament"])
    #Once a unique view code is generated, this line calls the database function to add it to the database, assigning it to the current tournament

    return redirect ("/tournamentDashboard")
    # redirect the user to the tournament dashboard page once the view code for the tournament has been added to the database
    
@myTournamentsPageBlueprint.route("/myTournamentsPage")
#creates the route for the myTournamentsPage blueprint, allowing it to be accessed easily.
def myTournamentsPage():
    #defines myTournamentsPage function for the myTournamentsPage blueprint
    session["viewCodeInputError"] = ""
    #clears the view code input errors session so it does not remain present when returning to the user's dashboard
    session["Viewing"] = False
    #sets the viewing session to false so if a tournament dashboard is loaded from the myTournaments page, 
    #all functions are displayed as it is the tournament organiser accessing the tournament
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    results = db.getTournaments(session["currentUser"])
    #sets results to be all of the current user's tournaments, including all the fields in each tournament, formatted as lists within a list
    return render_template("myTournaments.html", tournaments = results)
    #loads the my tournaments html page, with all the current user's tournaements passed in as "tournaments" so they and the fields within them can be displayed

@tournamentDashboardRedirectBlueprint.route("/tournamentDashboardRedirect", methods = ["POST"])
#creates the route for the tournamentDashboardRedirect blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def tournamentDashboardRedirect():
    #defines tournamentDashboardRedirect function for the tournamentDashboardRedirect blueprint
    session["viewCodeInputError"] = ""
    #clears the view code input errors session so it does not remain present when returning to the user's dashboard
    session["FixtureInfoInputError"] = ""
    #defines the FixtureInfoInputError session or clears the session containing errors with fixture information inputs so they are not already present from other tournaments when the fixture information input page is loaded
    session["scoreInputError"] = ""
    #defines the scoreInputError session or clears the session containing errors with score inputs,
    #so they are not already present from other tournaments when the scores input page is loaded
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    session["Tournament"] = request.form["tournamentName"]
    #sets the Tournament session to be the tournament name value of the tournament that has been clicked on on the myTournaments html page
    results = db.getTournamentFields(session["Tournament"])
    #sets results to be the list of all fields for the tournament with the name of the value in the tournament session
    viewCode = results[5]
    #sets viewCode to be the sixth item from this list as represents the tournament's view code
    viewCode = eval(viewCode)
    #turns the view code back to its origional string form
    if results[6] != None:
        #if the seventh item of results is not None, this signifies the fixture information for the tournament has already been inputted 
        fixturesInfoInputted="True"
        #sets fixturesInfoInputted to be True to signify the fixture information for the tournament has already been inputted so the fixtures page should be loaded if the Fixtures button is pressed on the tournament dashboard
    else:
        #if the seventh item of results is None, this signifies the fixture information for the tournament has not already been inputted
        fixturesInfoInputted="False"
        #sets fixturesInfoInputted to be False to signify the fixture information for the tournament has not already been inputted so the fixture info input page should be loaded if the Fixtures button is pressed on the tournament dashboard
    matchScores = results[9]
    #sets brackets to be the fith value from the fields list as this represents that tournament's brackets
    matchScores = eval(matchScores)
    #turns the brackets back to their origional dictionary form
    numTeams = int(results[2])
    #sets numTeams to be the integer version of the third item in results, which represents the current tournament's number of teams
    numRounds = int(math.log2(numTeams))
    #the number of rounds for the tournament is log2 of the number of teams in the tournament
    return render_template("tournamentDashboard.html", viewCode = viewCode, fixturesInfoInputted = fixturesInfoInputted, matchScores = matchScores, numberOfRounds = numRounds)
    #loads the tournament dashboard, with the specific tournament's view code passed in as viewCode so it can be displayed
    #also passes in whether the fixture information has been inputted yet so the program can choose whether the fixture info input page should be loaded or the fixtures page should be loaded when the Fixtures button is pressed
    #also passes in the matchScores dictionary and number of rounds to be used to determine whether the end tournament button should be disabled or enabled

@deleteTournamentBlueprint.route("/deleteTournament", methods = ["POST"])
#creates the route for the deleteTournament blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def deleteTournament():
    #defines deleteTournament function for the deleteTournament blueprint
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    tournamentToDelete = request.form["deleteTournament"]
    #set tournamentToDelete to be the tournament name of the tournament the "delete tournament" button was selected on on the my tournaments page
    db.deleteTournament(tournamentToDelete)
    #delete the tournament with this tournament name from the database
    return redirect("/myTournamentsPage")
    #redirect the user to the function to load the my tournaments page so it reloads without this tournament present

@teamsInputRedirectBlueprint.route("/teamsInputRedirect", methods = ["POST"])
#creates the route for the teamsInputRedirect blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def teamsInputRedirect():
    #defines teamsInputRedirect function for the teamsInputRedirect blueprint
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    session["Teams"] = ""
    #clears the teams session so the teams input page appears blank
    teams.clear()
    #clears the teams list so the teams input page appears blank
    session["teamDeletionError"] = ""
    #clears the team deletion error session so the teams input page appears blank
    session["teamInputError"] = "" 
    #clears the team input error session so the teams input page appears blank
    session["Tournament"] = request.form["tournamentName"]
    #sets the Tournament session to be the tournament name value of the tournament that has been clicked on on the myTournaments html page

    results = db.getTournamentFields(session["Tournament"])
    global numTeams
    numTeams = results[2]
    numTeams = int(numTeams)

    return redirect("/teamsInputPage")
    #redirects the user to the function to load the teams input page

@bracketViewRedirectBlueprint.route("/bracketViewRedirect", methods = ["POST"])
#creates the route for the bracketViewRedirect blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def bracketViewRedirect():
    #defines bracketViewRedirect function for the bracketViewRedirect blueprint
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    session["Tournament"] = request.form["tournamentName"]
    #sets the Tournament session to be the tournament name value of the tournament that has been clicked on on the myTournaments html page
    results = db.getTournamentFields(session["Tournament"])
    #sets results to be the list of fields from the database for the tournament with the tournament name of the value in the tournament session

    global numTeams

    numTeams = results[2]
    #sets numTeams to be the third value from the fields list as this represents that tournament's number of teams
    numTeams = int(numTeams)
    #turns the number of teams value from the database back to its integer form
    brackets = results[4]
    #sets brackets to be the fith value from the fields list as this represents that tournament's brackets
    brackets = eval(brackets)
    #turns the brackets back to their origional dictionary form
    return render_template("bracketView.html", brackets = brackets, numberOfRounds = int(math.log2(numTeams)))
    #loads the bracket view html page with the brackets for the tournament selected and number of rounds, which is derrived from the number of teams of the selected tournament, passed in with the page