from flask import Blueprint,render_template

creationFormBlueprint = Blueprint("creationForm",__name__)

@creationFormBlueprint.route("/creationForm")
def creationForm():
    return render_template("creationForm.html")