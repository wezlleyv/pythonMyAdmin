from flask import render_template
import json


def interface_user_manager(application):
    @application.route("/")
    def home():
        client = application.test_client()

        getJsonDatabases = client.get("/api/mysql?option=get_databases")
        jsonDatabases = json.loads(getJsonDatabases.get_data())
        listOfDatabases = [nameOfDatabase['Database'] for nameOfDatabase in jsonDatabases]

        dictionaryTables = {}

        for database in listOfDatabases:
            nameOfDatabase = database
            getJsonTables = client.get(f"/api/mysql?option=get_tables&database={nameOfDatabase}")
            jsonTables = json.loads(getJsonTables.get_data())
            dictionaryTables[nameOfDatabase] = jsonTables

        return render_template("index.html", array_databases=listOfDatabases, d=dictionaryTables)
