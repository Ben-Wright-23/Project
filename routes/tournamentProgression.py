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
    session["FixtureInfoInputError"] = ""
    db = DatabaseHandler("appData.db")
    results = db.getTournamentFields(session["Tournament"])
    brackets = results[4]
    brackets = eval(brackets)
    roundStartTimes = results[6]
    roundStartTimes = eval(roundStartTimes)
    matchDuration = int(results[7])
    breakLength = int(results[8])
    return render_template("fixtures.html", tournament = brackets, roundStartTimes = roundStartTimes, matchDuration = matchDuration, breakLength = breakLength)
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
    if startTime[:2].isdigit() == False or int(startTime[:2])>23 or startTime[-2:].isdigit() == False or int(startTime[-2:])>59 or str(startTime)[2] != ":" or len(startTime)>5:
        session["FixtureInfoInputError"] = "Entered tournament start time is not in the specified format"
        return redirect("/fixtureInfoInputPage")
    elif matchDuration.isdigit() == False:
        session["FixtureInfoInputError"] = "Entered match duration is not an integer"
        return redirect("/fixtureInfoInputPage")
    elif int(matchDuration) > 150:
        session["FixtureInfoInputError"] = "Entered match duration is too long"
        return redirect("/fixtureInfoInputPage")
    elif int(matchDuration) == 0:
        session["FixtureInfoInputError"] = "Entered match duration is not valid"
        return redirect("/fixtureInfoInputPage")

    else:   
        session["FixtureInfoInputError"] = ""
        addedTimePerRound = int(matchDuration)+int(breakLength)

        userGivenTime = startTime.split(":")
        hours = int(userGivenTime[0])
        mins = int(userGivenTime[1])
        # tournamentStartDateTime = datetime(2000,1,1,hours,mins,0)
        # tournamentStartTime = tournamentStartDateTime.time()
        tournamentStartTime = datetime(hours,mins,0)

        roundStartTimes = []
        roundStartTimes.append(str(tournamentStartTime)[:5])
        # newDateTime = tournamentStartDateTime
        newTime = tournamentStartTime
        for i in range(numRounds-1):
            newTime = newTime + timedelta(minutes=addedTimePerRound)
            # newDateTime = newDateTime + timedelta(minutes=addedTimePerRound)
            # if newDateTime.day == 2:
            #     session["FixtureInfoInputError"] = "Tournament matches must all start on the same day"
            #     return redirect("/fixtureInfoInputPage")
            # newTime = newDateTime.time()
            roundStartTimes.append(str(newTime)[:5])

        db.addFixtureInfo(str(roundStartTimes), matchDuration, breakLength, session["Tournament"])
        return redirect("/fixturesPage")


@fixtureInfoInputPageBlueprint.route("/fixtureInfoInputPage")
def fixtureInfoInputPage():
    return render_template("fixtureInfoInput.html", error = session["FixtureInfoInputError"])