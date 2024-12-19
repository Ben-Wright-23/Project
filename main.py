#Imports#############################################
from flask import Flask, render_template, request, redirect
from database import DatabaseHandler
from routes.home import homeBlueprint
from routes.tournamentCreation import creationFormBlueprint
from routes.dashboardRoute import dashboardBlueprint
from routes.userManagement import signupBlueprint, createUserBlueprint, authenticateUserBlueprint,logoutBlueprint, deleteUserBlueprint, deleteAccountBlueprint
#####################################################

app = Flask(__name__)
app.config["SECRET_KEY"] = "THISISABADKEY"
db = DatabaseHandler("appData.db")
# db.createTables()
db.createTournamentTables()
# db.dropUsers()




#Routing#############################################
app.register_blueprint(homeBlueprint)
app.register_blueprint(signupBlueprint)
app.register_blueprint(createUserBlueprint)
app.register_blueprint(authenticateUserBlueprint)
app.register_blueprint(dashboardBlueprint)
app.register_blueprint(logoutBlueprint)
app.register_blueprint(deleteUserBlueprint)
app.register_blueprint(deleteAccountBlueprint)
app.register_blueprint(creationFormBlueprint)

######################################################
app.run(debug = True)








