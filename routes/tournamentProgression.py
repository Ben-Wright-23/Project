from flask import Blueprint,render_template, session, request,redirect
from database import DatabaseHandler


fixturesPageBlueprint = Blueprint("fixturesPage",__name__)
liveBracketViewPageBlueprint = Blueprint("liveBracketViewPage",__name__)
scoresInputPageBlueprint = Blueprint("scoresInputPage",__name__)

@liveBracketViewPageBlueprint.route("/liveBracketViewPage")
def liveBracketViewPage():
    return render_template("liveBracketView.html")

@fixturesPageBlueprint.route("/fixturesPage")
def fixturesPage():
    return render_template("fixtures.html")

@scoresInputPageBlueprint.route("/scoresInputPage")
def scoresInputPage():
    return render_template("scoresInput.html")