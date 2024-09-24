from flask import Blueprint,render_template


dashboardBlueprint = Blueprint("dashboard",__name__)

@dashboardBlueprint.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")