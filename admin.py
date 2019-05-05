# -*- coding: utf-8 -*-
"""
Created on Fri May  3 13:48:41 2019

@author: bercy

files that help take care of admin stuff
"""
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DB_URL = "postgres://rxyenuwkgfbagh:ffca4aadd434b6c6a113ce84d7799c18da27"
DB_URL += "abaff6cb7221be8a1305dfd8b28c@ec2-54-197-239-115.compute-1.amazonaws.com:"
DB_URL += "5432/d5aba9o0q74a0v"
# Set up database
engine = create_engine(DB_URL)
db = scoped_session(sessionmaker(bind=engine))

#function that was used to populate the books tables
def populateBookTable():
    file = open("books.csv")
    reader = csv.reader(file)
    sql = "insert into books(isbn,ratings,title,author,year) "
    sql += "values(:isbn,:ratings,:title,:author,:year)"
    for isbn,title,author,year,ratings in reader:
        db.execute(sql,{"isbn":isbn,"ratings":ratings,"title":title,"author":author,"year":year,})
        print("adding")
    db.commit()

    
