# -*- coding: utf-8 -*-
"""
Created on Fri May  3 13:48:41 2019

@author: bercy

files that help take care of admin stuff
"""
import csv

def populateBookTable(db):
    file = open("books.csv")
    reader = csv.reader(file)
    sql = "insert into books(isbn,ratings,title,author,year) "
    sql += "values(:isbn,:title,:author,:year,:ratings)"
    for isbn,title,author,year,ratings in reader:
        db.execute(sql,{"isbn":isbn,"ratings":ratings,"title":title,"author":author,"year":year,})
        print("adding")
    #db.commit()