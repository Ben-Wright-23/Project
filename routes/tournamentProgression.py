from flask import Blueprint,render_template, session, request,redirect
from database import DatabaseHandler


fixturesPageBlueprint = Blueprint("fixturesPage",__name__)
#create a flask blueprint for the function to load the fixtures page
liveBracketViewPageBlueprint = Blueprint("liveBracketViewPage",__name__)
#create a flask blueprint for the function to load the live bracket view page
scoresInputPageBlueprint = Blueprint("scoresInputPage",__name__)
#create a flask blueprint for the function to load the scores input page
fixtureInfoInputBlueprint = Blueprint("fixtureInfoInput",__name__)


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

    return render_template("fixtures.html", tournaments = brackets)
    #loads the fixtures page

@scoresInputPageBlueprint.route("/scoresInputPage")
#creates the route for the scoresInputPage blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def scoresInputPage():
    #defines scoresInputPage function for the scoresInputPage blueprint
    return render_template("scoresInput.html")
    #loads the scores input page

@fixtureInfoInputBlueprint.route("/fixtureInfoInput")
def fixtureInfoInput():
    db = DatabaseHandler("appData.db")
    startTime = request.form["startTime"]
    matchDuration = request.form["matchDuration"]
    breakLength = request.form["breakLength"]
    db.addFixtureInfo(startTime, matchDuration, breakLength, session["Tournament"])
    return redirect("/fixturesPage")