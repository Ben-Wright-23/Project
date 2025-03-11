from flask import Blueprint,render_template,session


dashboardBlueprint = Blueprint("dashboard",__name__)

@dashboardBlueprint.route("/dashboard")
def dashboard():
    session["accountDeletionError"] = ""
    session["tournamentCreationError"] = ""
    return render_template("dashboard.html", error = session["viewCodeInputError"])
