# Description: This file is used to connect to the database.
import psycopg2
import logging

db = None

def connect():
    global db
    db = psycopg2.connect("dbname=chatapp user=chatapp password=chatapp host=localhost port=5432")
    logging.info("Connected to database")

def init_db():
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS chatrooms (id SERIAL PRIMARY KEY, name VARCHAR(255) UNIQUE NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, message_type VARCHAR(255) NOT NULL, chatroom_id INTEGER NOT NULL REFERENCES chatrooms(id), sender VARCHAR(255) NOT NULL, message VARCHAR(255) NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS chatroom_users (id SERIAL PRIMARY KEY, chatroom_id INTEGER NOT NULL REFERENCES chatrooms(id), username VARCHAR(255) NOT NULL)")
    db.commit()

def get_db():
    if db is None:
        connect()
    return db

def close_db():
    db.close()

def get_cursor():
    return db.cursor()

def commit():
    db.commit()

