#!/usr/bin/env python
#-*- encoding: utf8 -*-

# Today Quote app

import sys
import os
import sqlite3
from bottle import\
        run, \
        debug, \
        request, \
        static_file, \
        get, \
        post, \
        redirect, \
        HTTPError, \
        template

DBNAME="/home/matael/today_quote/db.sqlite"


#### Generic Views ####

@get('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='/home/matael/today_quote/static')

#### App Views ####

@get('/')
def home():
    """ Home page for a GET request """
    db = sqlite3.connect(DBNAME)
    c = db.cursor()
    c.execute("SELECT * FROM quotes ORDER BY vote_up-vote_down DESC")
    result = c.fetchall()
    db.close()
    return template("templates/home.html", result=result)

@post('/')
def add():
    """ POST processing page """
    if not request.POST:
        redirect("/")

    if request.POST.get("author") and request.POST.get("quote"):
        author = unicode(request.POST.get("author").strip(), 'utf8')
        quote = unicode(request.POST.get("quote").strip(), 'utf8')

        db = sqlite3.connect(DBNAME)
        c = db.cursor()
        c.execute("INSERT INTO quotes (author,quote,vote_up,vote_down) VALUES (?,?,?,?)", (author, quote, 0, 0))
        db.commit()
        db.close()
        redirect("/")

@get("/new")
def new_quote_form():
    """ display the form for adding quote """
    return template("templates/form.html")

@get("/<id:re:\d+>/<do:re:(up)|(down)>")
def upvote(id, do):
    if do=="up":
        request_get = "SELECT vote_up FROM quotes WHERE id LIKE ?"
        request_update = "UPDATE quotes SET vote_up=? WHERE id LIKE ?"
    else:
        request_get = "SELECT vote_down FROM quotes WHERE id LIKE ?"
        request_update = "UPDATE quotes SET vote_down=? WHERE id LIKE ?"
    
    db = sqlite3.connect(DBNAME)
    c = db.cursor()
    c.execute(request_get, [str(id)])
    cur_votes = c.fetchone()
    if not cur_votes:
        db.close()
        raise HTTPError(404)
    else:
        new_votes = str(int(cur_votes[0])+1)
        c.execute(request_update, (new_votes,str(id)))
        db.commit()
        db.close()
        redirect("/")

@get("/api/<object>")
def api(object):
    db = sqlite3.connect(DBNAME)
    c = db.cursor()
    if object=="random":
        c.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1")
    elif object=="top":
        c.execute("SELECT * FROM quotes ORDER BY vote_up-vote_down DESC LIMIT 1")
    if object=="last":
        c.execute("SELECT * FROM quotes ORDER BY id DESC LIMIT 1")
    if object=="all":
        c.execute("SELECT * FROM quotes ORDER BY id")
        result = c.fetchall()
        db.close()
        return {"results":result}
    result = c.fetchone()
    db.close()
    fields = ['id', 'author', 'quote', 'vote_up', 'vote_down']
    return dict(zip(fields,result))



debug(True)
#run(reloader=True)
