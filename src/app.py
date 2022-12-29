import sqlite3
import os
import schedule
import time
import tweepy
import json

from flask import Flask, request, redirect, flash, session
from flask_session import Session
from dotenv import load_dotenv, find_dotenv
from jinja2 import Environment, FileSystemLoader
from faker import Faker

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
load_dotenv(find_dotenv())
logged_in = "no"
time_started = 0
time_ended = 0
broadcast = 0

def get_session():
    if not session.get("name"):
        return redirect("/login")
    return session.get("name")

def get_db():
    db = sqlite3.connect('app.db')
    return db

def get_env():
    environment = Environment(loader=FileSystemLoader("views/"))
    return environment

def get_tweetapi():
    # Initialize tweepy
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    return api

@app.route('/toggle_broadcast')
def toggle_broadcast():
    global broadcast
    global time_started
    global time_ended

    if not session.get("name"):
        return redirect('/login')

    if broadcast == 0:
        time_started = time.time()
    else:
        time_ended = time.time()

    broadcast ^= 1

    return redirect('/message_page')

@app.route('/login')
def login():
    if session.get("name"):
        return redirect('/message_page')
    environment = get_env()
    template = environment.get_template("login.j2")
    return template.render()

@app.route('/post_login', methods = ["POST"])
def post_login():
    global logged_in
    username = os.getenv("TAD_USER")
    password = os.getenv("TAD_PASS")
    print(username)
    if request.form['username'] == username:
        if request.form['password'] == password:
            logged_in = "yes"
            print("all is ok")
            return redirect('/message_page')
        else:
            print("Wrong password")
            return redirect('/login')
    else:
        print("Wrong Username")
        return redirect('/login')

@app.route('/')
def home():
    """
    This is home page for adding, removing, editting, message that will be broadcasted
    """
    return redirect('/login') 

@app.route('/message_page')
def message_page():
    """
    This is for CRUD message
    """
    print(logged_in)
    if (logged_in == 'no'):
        return redirect('/login')

    environment = get_env()
    db = get_db()
    sql = ''' SELECT * FROM messages '''
    cur = db.cursor()
    cur.execute(sql)
    db.commit()
    messages = cur.fetchall()
    cur.close()

    db = get_db()
    sql = ''' SELECT * FROM followers '''
    cur = db.cursor()
    cur.execute(sql)
    db.commit()
    followers = cur.fetchall()
    cur.close()

    template = environment.get_template('message_page.j2')
    str_time_started = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_started))
    str_time_ended = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_ended))
    if time_started == 0:
        str_time_started = "not started"
    if time_ended == 0:
        str_time_ended = "never stopped"
    return template.render(messages=messages, followers=followers, broadcast=broadcast, time_started=str_time_started, time_ended=str_time_ended)

@app.route('/populate_followers_data')
def populate_followers_data():
    """
    This is for populating user data for development purpose
    """
    if (logged_in == 'no'):
        return redirect('/login')
    db = get_db()

    api = get_tweetapi()

    # Collect all followers into db
    counter = 0
    for follower in api.get_friends():
        cur = db.cursor()
        sql = ''' SELECT * FROM followers WHERE uid = ? '''
        params = [follower.id]
        cur.execute(sql, params)
        if not cur.fetchone():
            sql_insert = ''' INSERT INTO followers(uid, screen_name) VALUES(?, ?) '''
            param_insert = [follower.id, follower.screen_name]
            cur.execute(sql_insert, param_insert)
            counter = counter + 1
        db.commit()
        cur.close()

    return redirect("/message_page")
    if counter == 0:
        return "No data inserted"

    return "Populate {} user data success".format(counter)

@app.route('/generate_fake_data')
def generate_fake_data():
    """
    This endpoint is for generating fake data
    """
    if (logged_in == 'no'):
        return redirect('/login')
    fake = Faker()
    content = fake.text()
    activate = 1
    params = [content, activate]
    sql = ''' INSERT INTO messages(content, activate) VALUES(?, ?) '''
    db = get_db()
    cur = db.cursor()
    cur.execute(sql, params)
    db.commit()
    cur.close()
    return "Success fake data is generated"

@app.route('/get_all_messages')
def get_all_messages():
    """
    This is for getting all messages
    """
    if (logged_in == 'no'):
        return redirect('/login')
    db = get_db()
    sql = ''' SELECT * FROM messages '''
    cur = db.cursor()
    cur.execute(sql)
    db.commit()
    rows = cur.fetchall()
    cur.close()

    return " ".join([str(elem) for elem in rows])
@app.route('/message', methods = ['POST'])
def store_message():
    """
    This is endpoint for adding message
    """
    if (logged_in == 'no'):
        return redirect('/login')
    content = request.form['content']
    activate = 1
    params = [content, activate]
    sql = ''' INSERT INTO messages(content, activate) VALUES(?, ?) '''
    db = get_db()
    cur = db.cursor()
    cur.execute(sql, params)
    db.commit()
    cur.close()
    return redirect("/message_page")

@app.route('/message/<id>', methods = ['POST'])
def edit_message(id):
    """
    This is endpoint editting message
    """
    if (logged_in == 'no'):
        return redirect('/login')
    content = request.form['content']
    params = [content, id]
    db = get_db()
    cur = db.cursor()
    sql = ''' UPDATE messages SET content = ? WHERE id = ?'''
    cur.execute(sql, params)
    db.commit()
    cur.close()

    return redirect("/message_page") 

@app.route('/toggle_message/<id>')
def toggle_message(id):
    """
    This is endpoint for toggling activation of message
    """
    if (logged_in == 'no'):
        return redirect('/login')
    sql = ''' SELECT activate FROM messages WHERE id = ?'''
    params = [id]
    db = get_db()
    cur = db.cursor()
    cur.execute(sql, params)
    row = cur.fetchone()
    print(row)
    activate = row[0]
    activate ^= 1
    print(activate)
    sql = ''' UPDATE messages SET activate = ? WHERE id = ?'''
    params = [activate, id]
    cur.execute(sql, params)
    db.commit()
    cur.close()
    return redirect("/message_page")

@app.route("/send_message/<id>")
def send_message(id):
    """
    This is to send message to your follower
    """
    sql = ''' SELECT * FROM followers WHERE id = ? '''
    params = [id]
    db = get_db()
    cur = db.cursor()
    cur.execute(sql, params)
    follower = cur.fetchone()
    sql = ''' SELECT * FROM messages WHERE activate = 1 '''
    cur.execute(sql)
    messages = cur.fetchall()
    api = get_tweetapi()
    sent = follower[3]
    if sent == 0:
        for message in messages:
            api.send_direct_message(follower[1], message[1])
    sent ^= 1
    params = [sent, id]
    sql = ''' UPDATE followers SET sent = ? WHERE id = ? '''
    cur.execute(sql, params)
    db.commit()
    cur.close()
    return redirect("/message_page")

@app.route('/delete_message/<id>')
def delete_message(id):
    """
    This is endpoint for deletting message
    """
    if (logged_in == 'no'):
        return redirect('/login')
    sql = ''' DELETE FROM messages WHERE id = ?'''
    params = [id]
    db = get_db()
    cur = db.cursor()
    cur.execute(sql, params)
    db.commit()
    cur.close()
    return redirect('/message_page')
