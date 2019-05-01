# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 16:08:03 2019

@author: bercy
"""

def authenticate(db,username,password):
    result =  db.execute("SELECT * FROM users")
    for row in result:
        #print("username:", row['username'])
        print(row)
    return None