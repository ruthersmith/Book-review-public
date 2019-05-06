# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 16:08:03 2019

@author: bercy
"""

def authenticate(db,request):
    username = request.form.get("user_name")
    password  = request.form.get("password")
    #what will be returned
    auth_result = None
    #where we store the result of the query
    rows =  []
    sql = "SELECT * FROM users where user_name = :username and password = :password"
    result =  db.execute(sql,{"username":username, "password":password})
    for row in result:
        rows.append(row)
    
    if len(rows) == 1:
        auth_result = rows
        
    return auth_result

#function responsible for registering the user
def registerUser(db,request):
     FirstName = request.form.get("first_name")
     LastName  = request.form.get("last_name")
     username = request.form.get("user_name")
     password  = request.form.get("password")
     password_confirm  = request.form.get("password_confirm")
     
     if(password!=password_confirm):
         print("password not a match")
         return False
     else:
         sql = "Insert Into users(user_name,password,first_name,last_name) " 
         sql += "Values(:uname,:psw,:fname,:lname)"
         db.execute(sql,{"uname":username,"psw":password,"fname":FirstName,"lname":LastName})
         db.commit()
         return True

#function resposible for getting the books from the database
def getBooks(db,limit):
    books = []
    sql = "SELECT * FROM books limit " + str(limit)
    result = db.execute(sql)
    for row in result:
        books.append(row)
    books.pop(0)
    return books

#function responsible for getting the book info
def getBookInfo(db,isbn):
    book = []
    sql = "select * from books where isbn = :isbn"
    result = db.execute(sql,{"isbn":isbn})
    for row in result:
        book.append(row)
    
    return book[0]

def insertRating(db,user,request):
    isbn = request.form.get("isbn")
    comment  = request.form.get("comment")
    rating = request.form.get("rate")
    
    sql = "insert into rates(user_id,isbn,rating,comment) "
    sql += "Values(:user_id,:isbn,:rating,:comment)"
    db.execute(sql,{"user_id":user,"isbn":isbn,"rating":rating,"comment":comment})
    db.commit()
    
    


        
    
     
