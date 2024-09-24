from flask import Blueprint,render_template

homeBlueprint = Blueprint("home",__name__)

@homeBlueprint.route("/")
def home():
    return render_template("index.html")
