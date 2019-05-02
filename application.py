'''
in anaconda terminal
$ set FLASK_APP=application.py
$ set FLASK_DEBUG=1
$ python -m flask run
'''

import helpers
from flask import Flask, session,render_template,request,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

DB_URL = "postgres://rxyenuwkgfbagh:ffca4aadd434b6c6a113ce84d7799c18da27"
DB_URL += "abaff6cb7221be8a1305dfd8b28c@ec2-54-197-239-115.compute-1.amazonaws.com:"
DB_URL += "5432/d5aba9o0q74a0v"
# Set up database
engine = create_engine(DB_URL)
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    url = url_for('home')
    return render_template("login.html",url = url)

@app.route('/home',methods = ["POST"])
def home():
    
    username = request.form.get("user_name")
    password  = request.form.get("password")
    user = helpers.authenticate(db,username,password)
    
    if user == None:
        return "<h1>Error:Failed To Authenticate<h1>"
    else:
        return "you have just logged in " + username
        
    

@app.route('/create_account')
def create_account():
    onSubmitUrl = url_for('home_register')
    return  render_template("registration.html",url=onSubmitUrl)

#
@app.route('/home_registered',methods = ["POST"])
def home_register():
    return "you have registered"













