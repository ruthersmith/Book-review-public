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

def getBookComment(db,isbn):
    rates = []
    
    sql = "Select user_name,rating,comment from rates "
    sql += "join users using(user_id) where isbn = :isbn"
    result = db.execute(sql,{"isbn":isbn})
    
    for row in result:
        rates.append(row)
    print(rates)
    return rates

def insertRating(db,user,request):
    isbn = request.form.get("isbn")
    comment  = request.form.get("comment")
    rating = request.form.get("rate")
    
    sql = "insert into rates(user_id,isbn,rating,comment) "
    sql += "Values(:user_id,:isbn,:rating,:comment)"
    db.execute(sql,{"user_id":user,"isbn":isbn,"rating":rating,"comment":comment})
    db.commit()
    
def insertReading(db,user_id,request):
    exist = []
    isbn = request.form.get("isbn").strip()
    print(isbn)
    
    #check to see if row exist
    sql = "select * from readinglist where user_id = :user_id and isbn = :isbn"
    result = db.execute(sql,{"user_id":user_id,"isbn":isbn})
    
    for row in result:
        exist.append(row)
    
    #if the len is zero book not yet in readinglist
    if(len(exist) == 0):
        sql = "insert into readinglist(user_id,isbn) Values(:user_id,:isbn)"
        db.execute(sql,{"user_id":user_id,"isbn":isbn})
        db.commit()    
    return True

def getReadingList(db,user_id):
    readingList = []
    sql = "select * from books join readinglist using(isbn) where user_id = :user_id"
    result = db.execute(sql,{"user_id":user_id})
    
    for row in result:
        readingList.append(row)
    
    return readingList
    
def submitComment(db,user_id,request):
    overall_rating = []
    isbn = request.form.get("isbn").strip()
    rate = int(request.form.get("rate"))
    comment = request.form.get("comment")
    
    #insert the comment in rates table
    sql = "insert into rates(user_id,isbn,rating,comment) "
    sql += "Values(:user_id,:isbn,:rate,:comment)"
    db.execute(sql,{"user_id":user_id,"isbn":isbn,"rate":rate,"comment":comment})
    db.commit()
    
    #Get the books overall rating in book table
    sql = "select ratings from books where isbn = :isbn"
    result =  db.execute(sql,{"isbn":isbn})
    
    for row in result:
        overall_rating.append(row)
        
    #update overall rating
    if overall_rating[0][0] ==  "":
        sql = "UPDATE books SET ratings = :rate where isbn = :isbn"
        db.execute(sql,{"rate":rate,"isbn":isbn})
        db.commit()
    else:
        overall_rating = int(overall_rating[0][0])
        overall_rating = int((rate + overall_rating)/2)
        sql = "UPDATE books SET ratings = :rate where isbn = :isbn"
        db.execute(sql,{"rate":overall_rating,"isbn":isbn})
        db.commit()    
    
def getSearchRequest(db,search):
    search_result = []
    sql = "select * from books where title like :begin " 
    sql += "or title like :middle or title like :end "
    
    begining = search + '%'
    middle = '%' + search + '%'
    end = '%' + search 
    
    query_result = db.execute(sql,{"begin":begining,"middle":middle,"end":end})
    
    for row in query_result:
        search_result.append(row)
        
    return search_result

        
    
     
