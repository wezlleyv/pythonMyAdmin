from flask import Flask, render_template, send_from_directory
import mysql.connector, os
import psycopg2
import json

# local
from api.database.mysqlapi import MySQL
from api.database.postgresqlapi import PostgreSQL


app = Flask(__name__,
            static_url_path="",
            static_folder="static")

def register_api(application, database, server):
    if server == "mysql":
        mysqlapi = MySQL.as_view("mysql", mysql.connector.connect(**database), application)
        app.add_url_rule(f"/api/mysql", view_func=mysqlapi)

    elif server == "postgresql":
        postgreapi = PostgreSQL.as_view("postgresql", psycopg2.connect(**database), application)
        app.add_url_rule(f"/api/psql", view_func=postgreapi)


def main_routes():
    @app.route("/")
    def home():
        client = app.test_client()

        dictio = client.get("/api/mysql?option=get_databases")
        response = json.loads(dictio.get_data())

        return render_template("index.html", data=response)

def run():
    # get config
    app.config.from_object(os.environ.get("APP_CONFIG_FILE"))

    # connect to database server
    register_api(app, app.config["DATABASE"]["DATA"], app.config['DATABASE']["SERVER"])

    main_routes()

    # run web
    app.run(debug=app.config['DEBUG'])