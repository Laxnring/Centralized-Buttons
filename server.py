from flask import Flask
from flask import request
import sqlite3
from datetime import datetime
import traceback

conn = None

def check_connection(conn):
    try:
        conn.cursor()
    except:
        conn = sqlite3.connect('./instances.db')
    return conn


def increase_counter(conn, id_):
    conn = check_connection(conn)
    c = conn.cursor()

    if not c.execute(f"SELECT COUNT(*) FROM objects where id = {id_}").fetchone()[0]:
        c.execute(f"INSERT INTO locations (id, location) values ({id_}, {-1})")

    location = c.execute(f"SELECT location from locations where id == {id_} limit 1").fetchone()[0]
    c.execute(f"INSERT INTO objects (id, location, date) values ({id_}, {location}, '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')")
    conn.commit()

def change_location(conn, id_, location):
    conn = check_connection(conn)
    c = conn.cursor()

    if not c.execute(f"SELECT COUNT(*) FROM objects where id = {id_}"):
        c.execute(f"INSERT INTO locations (id, location) values ({id_}, {location}")

    c.execute(f"UPDATE SET id = {id_}, location = {location} where id = {id_}")
    conn.commit()

    

app = Flask(__name__)

@app.route('/counter')
def counter():
    try:
        increase_counter(conn, request.args.get('id'))
    except Exception as e:
        return str(traceback.print_exc())
    return "OK"

@app.route('/changelocation')
def change_loc():
    change_location(conn, request.args.get('id'), request.args.get('location'))
    return f"LOC: {request.args.get('location')}"