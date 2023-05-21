from flask import Flask, request
import mysql.connector, os

# local
from database.mysqlapi import MySQL

app = Flask(__name__)

def register_api(app, database, server):
    if server == "mysql":
        mysqlapi = MySQL.as_view("mysql", mysql.connector.connect(**database), app)
        app.add_url_rule(f"/api/mysql", view_func=mysqlapi)

def run():
    # get config
    app.config.from_object(os.environ.get("APP_CONFIG_FILE"))

    # connect to database server
    register_api(app, app.config["DATABASE"]["DATA"], app.config['DATABASE']["SERVER"])

    # run web
    app.run(debug=app.config['DEBUG'])