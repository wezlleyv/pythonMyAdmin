from flask import Flask
import mysql.connector, os
from database.mysqlapi import MySQL


app = Flask(__name__)

db = mysql.connector.connect(
    host="0.0.0.0",
    user="root",
    password="root",
    port="3306",
)

def register_api(app):
    mysql = MySQL.as_view("mysql", db, app)
    app.add_url_rule(f"/api/mysql", view_func=mysql)

def run():
    app.config.from_object(os.environ.get("APP_CONFIG_FILE"))
    register_api(app)
    app.run(debug=app.config['DEBUG'])