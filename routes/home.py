from flask import Blueprint,render_template,session

homeBlueprint = Blueprint("home",__name__)

@homeBlueprint.route("/")
def home():
    session["viewCodeInputError"] = ""
    session["errorMessage"] = ""
    return render_template("index.html")
