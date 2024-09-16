#Imports#############################################
from flask import Flask, render_template


#####################################################

app = Flask(__name__)
app.config["SECRET_KEY"] = "THISISABADKEY"

#Routing#############################################

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup")
def signup():
    return render_template("SignUp.html")



######################################################
app.run(debug = True)