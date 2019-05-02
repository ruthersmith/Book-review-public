# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 16:08:03 2019

@author: bercy
"""

def authenticate(db,username,password):
    #what will be returned
    auth_result = None
    #where we store the result of the query
    rows =  []
    sql = "SELECT user_id FROM users where user_name = :username and password = :password"
    result =  db.execute(sql,{"username":username, "password":password})
    for row in result:
        rows.append(row)
    
    if len(rows) == 1:
        auth_result = rows[0][0]
        
    return auth_result


def registerUser(db,request):
     FirstName = request.form.get("first_name")
     LastName  = request.form.get("last_name")
     username = request.form.get("user_name")
     password  = request.form.get("password")
     password_confirm  = request.form.get("password_confirm")
     print((FirstName,LastName,username,password,password_confirm))
     
     return "I am trying to register you"