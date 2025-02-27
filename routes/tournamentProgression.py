from flask import Blueprint,render_template, session, request,redirect
from database import DatabaseHandler
from datetime import datetime,time,timedelta
import math


fixturesPageBlueprint = Blueprint("fixturesPage",__name__)
#create a flask blueprint for the function to load the fixtures page
liveBracketViewPageBlueprint = Blueprint("liveBracketViewPage",__name__)
#create a flask blueprint for the function to load the live bracket view page
scoresInputPageBlueprint = Blueprint("scoresInputPage",__name__)
#create a flask blueprint for the function to load the scores input page
fixtureInfoInputBlueprint = Blueprint("fixtureInfoInput",__name__)
fixtureInfoInputPageBlueprint = Blueprint("fixtureInfoInputPage",__name__)


@liveBracketViewPageBlueprint.route("/liveBracketViewPage")
#creates the route for the liveBracketViewPage blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def liveBracketViewPage():
    #defines liveBracketViewPage function for the liveBracketViewPage blueprint
    return render_template("liveBracketView.html")
    #loads the live bracket view page

@fixturesPageBlueprint.route("/fixturesPage")
#creates the route for the fixturesPage blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def fixturesPage():
    #defines fixturesPage function for the fixturesPage blueprint
    db = DatabaseHandler("appData.db")
    results = db.getTournamentFields(session["Tournament"])
    brackets = results[4]
    brackets = eval(brackets)
    startTime = results[6]
    matchDuration = int(results[7])
    breakLength = int(results[8])
    return render_template("fixtures.html", tournaments = brackets, startTime = startTime, matchDuration = matchDuration, breakLength = breakLength, roundStartTimes = roundStartTimes)
    #loads the fixtures page

@scoresInputPageBlueprint.route("/scoresInputPage")
#creates the route for the scoresInputPage blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def scoresInputPage():
    #defines scoresInputPage function for the scoresInputPage blueprint
    return render_template("scoresInput.html")
    #loads the scores input page

@fixtureInfoInputBlueprint.route("/fixtureInfoInput", methods = ["POST"])
def fixtureInfoInput():
    db = DatabaseHandler("appData.db")
    results = db.getTournamentFields(session["Tournament"])
    numTeams = results[2]
    numTeams = int(numTeams)
    numRounds = int(math.log2(numTeams))
    startTime = request.form["startTime"]
    matchDuration = request.form["matchDuration"]
    breakLength = request.form["breakLength"]
    addedTimePerRound = int(matchDuration)+int(breakLength)
    userGivenTime = startTime.split(":")
    hours = int(userGivenTime[0])
    mins = int(userGivenTime[1])
    tournamentStartTime = time(hours,mins,0)
    roundStartTimes = []
    roundStartTimes.append(str(tournamentStartTime)[:4])
    newTime = tournamentStartTime
    for i in range(numRounds):
        newTime = newTime + timedelta(minutes=float(addedTimePerRound))
        roundStartTimes.append(str(newTime)[:4])

    print(tournamentStartTime, roundStartTimes)
    db.addFixtureInfo(startTime, matchDuration, breakLength, session["Tournament"])
    return redirect("/fixturesPage")

@fixtureInfoInputPageBlueprint.route("/fixtureInfoInputPage")
def fixtureInfoInputPage():
    return render_template("fixtureInfoInput.html")