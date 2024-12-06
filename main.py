#Imports#############################################
from flask import Flask, render_template, request, redirect
from database import DatabaseHandler
from routes.home import homeBlueprint
from routes.userManagement import signupBlueprint, createUserBlueprint, authenticateUserBlueprint,logoutBlueprint, deleteUserBlueprint, dashboardBlueprint, deleteAccountBlueprint
#####################################################

app = Flask(__name__)
app.config["SECRET_KEY"] = "THISISABADKEY"
db = DatabaseHandler("appData.db")
# db.createTables()
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

######################################################
app.run(debug = True)








