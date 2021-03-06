'''
in anaconda terminal
$ set FLASK_APP=application.py
$ set FLASK_DEBUG=1
$ python -m flask run
'''

import helpers
from flask import Flask, session,render_template,request,url_for,redirect
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

    #data to be passed in to the front
    data = {}
    #authentification 
    user_info = helpers.authenticate(db,request)
    user = user_info[0][0]
    #if there were no users found, display error messageS
    if user == None:
        return "<h1>Error:Failed To Authenticate<h1>"
    
    data['user_info'] = user_info[0]
    # list of (isbn,ratings,title,author,year) book info
    data['browse'] = helpers.getBooks(db,limit = 5)
    
    #reading list 
    data['reading_list'] = helpers.getReadingList(db,user)
    #book reviewed
    data['book_reviewed'] = []
    
    session['user_id'] = user
    return render_template("dashboard.html",data=data)
        
    

@app.route('/create_account')
def create_account():
    onSubmitUrl = url_for('home_register')
    return  render_template("registration.html",url=onSubmitUrl)

#
@app.route('/home_registered',methods = ["POST"])
def home_register():
    helpers.registerUser(db,request)
    return "you have registered"

#individual book page route
@app.route('/home/<string:isbn>',methods = ["POST","GET"])
def book(isbn):
    data = {}
    data['book_info'] = helpers.getBookInfo(db,isbn)
    data['book_rates'] = helpers.getBookComment(db,isbn)
    print(data['book_info'])
    return render_template("pages/book_page.html",data=data)

@app.route('/browse')
def browse():
    data = {}
        # list of (isbn,ratings,title,author,year) book info
    data['browse'] = helpers.getBooks(db,limit = 300)
    return render_template("pages/browse_page.html",data=data)

@app.route('/commented',methods = ["POST"])
#when a new comment is submitted  this function is called
def submitComment():
    isbn = request.form.get("isbn")
    helpers.submitComment(db,session['user_id'],request)
    return redirect( url_for('book',isbn = isbn) )

@app.route('/read',methods = ["POST"])
def addReadingList():
    isbn = request.form.get("isbn").strip()
    helpers.insertReading(db,session['user_id'],request)
    return redirect(url_for('book',isbn = isbn))

@app.route('/search')
def search():
    data = {}
    search_request = request.args.get("search").capitalize() 
    data['search_result'] = helpers.getSearchRequest(db,search_request)
    return render_template("search.html",data=data)


