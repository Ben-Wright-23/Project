#Imports#############################################
from flask import Flask, render_template, request, redirect
from database import DatabaseHandler
from routes.home import homeBlueprint
from routes.tournamentCreation import creationFormBlueprint, tournamentCreationBlueprint, tournamentDashboardBlueprint, bracketViewBlueprint, teamsInputBlueprint
from routes.dashboardRoute import dashboardBlueprint
from routes.userManagement import signupBlueprint, createUserBlueprint, authenticateUserBlueprint,logoutBlueprint, deleteUserBlueprint, deleteAccountBlueprint
#####################################################

app = Flask(__name__)
app.config["SECRET_KEY"] = "THISISABADKEY"
db = DatabaseHandler("appData.db")
# db.createTables()
# db.createTournamentTables()
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
app.register_blueprint(tournamentCreationBlueprint)
app.register_blueprint(tournamentDashboardBlueprint)
app.register_blueprint(bracketViewBlueprint)
app.register_blueprint(teamsInputBlueprint)

######################################################
app.run(debug = True)



####Notes
#Tournament creation force order. Teams input -> show bracket -> Happy with bracket or manual change? -> 
#-> Start tournament or return to dashboard -> start tournament shows tournament dashboard

#My tournaments relies on boolean value, active if tournament started so cannot be edited, inactive if still creating tournament

#View tournament only works for active tournaments



