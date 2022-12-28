import sqlite3
import os
import schedule
import time
import tweepy
import json

from flask import Flask 
from dotenv import load_dotenv, find_dotenv
from jinja2 import Environment, FileSystemLoader
from faker import Faker

app = Flask(__name__)
load_dotenv(find_dotenv())
def get_db():
    db = sqlite3.connect('app.db')
    return db

@app.route('/')
def home():
    """
    This is home page for adding, removing, editting, message that will be broadcasted
    """
    return "Home page"

@app.route('/populate_followers_data')
def populate_followers_data():
    """
    This is for populating user data for development purpose
    """
    db = get_db()
    
    # Initialize tweepy
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)
   
    # Collect all followers into db
    counter = 0
    for follower in api.get_followers():
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

    if counter == 0:
        return "No data inserted"

    return "Populate {} user data success".format(counter)

@app.route('/generate_fake_data')
def generate_fake_data():
    """
    This endpoint is for generating fake data
    """
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
    content = request.form['content']
    activate = 1
    params = [content, activate]
    sql = ''' INSERT INTO messages(content, activate) VALUES(?, ?) '''
    db = get_db()
    cur = db.cursor()
    cur.execute(sql, params)
    return "Store message"

@app.route('/message/<id>', methods = ['POST'])
def edit_message(id):
    """
    This is endpoint editting message
    """
    content = request.form['content']
    return "Edit message"

@app.route('/toggle_message/<id>')
def toggle_message(id):
    """
    This is endpoint for toggling activation of message
    """
    sql = ''' SELECT activate FROM messages WHERE id = ?'''
    params = [id]
    db = get_db()
    cur = db.cursor()
    cur.execute(sql, params)
    row = cur.fetchone()
    activate = row[0]
    toggling_activate ^= 1
    sql = ''' UPDATE message SET activate = ? WHERE id = ?'''
    params = [toggling_activate, id]
    cur.execute(sql, params)
    return "Toggling message"

@app.route('/delete_message/<id>')
def delete_message(id):
    """
    This is endpoint for deletting message
    """
    sql = ''' DELETE FROM message WHERE id = ?'''
    params = [id]
    db = get_db()
    cur = db.cursor()
    cur.execute(sql, params)
    return "Message"
