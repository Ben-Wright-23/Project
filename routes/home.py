from flask import Blueprint,render_template,session

homeBlueprint = Blueprint("home",__name__)

@homeBlueprint.route("/")
def home():
    session["viewCodeInputError"] = ""
    #clears the view code input errors session so there is no error present when loading the user's dashboard
    session["errorMessage"] = ""
    return render_template("index.html")
