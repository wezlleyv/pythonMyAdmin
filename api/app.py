from flask import Flask
import mysql.connector, os
import psycopg2

# local
from api.database.mysqlapi import MySQL
from api.database.postgresqlapi import PostgreSQL
from api.application.routes import interface_user_manager


application = Flask(__name__,
            static_url_path="",
            static_folder="static")

def register_api(application, database, server):
    if server == "mysql":
        mysqlapi = MySQL.as_view("mysql", mysql.connector.connect(**database), application)
        application.add_url_rule(f"/api/mysql", view_func=mysqlapi)

    elif server == "postgresql":
        postgreapi = PostgreSQL.as_view("postgresql", psycopg2.connect(**database), application)
        application.add_url_rule(f"/api/psql", view_func=postgreapi)


def run():
    # get config
    application.config.from_object(os.environ.get("APP_CONFIG_FILE"))

    # connect to database server
    register_api(application,
                 application.config["DATABASE"]["DATA"],
                 application.config['DATABASE']["SERVER"])

    interface_user_manager(application)

    # run web
    application.run(debug=application.config['DEBUG'])