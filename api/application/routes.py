from flask import render_template
import json


def interface_user_manager(application):
    def mysql_get_database_list():
        client = application.test_client()

        getJsonDatabases = client.get("/api/mysql?option=get_databases")
        jsonDatabases = json.loads(getJsonDatabases.get_data())
        listOfDatabases = [nameOfDatabase['Database'] for nameOfDatabase in jsonDatabases]

        dictionaryTables = {}

        for database in listOfDatabases:
            nameOfDatabase = database
            getJsonTables = client.get(f"/api/mysql?option=get_tables&database={nameOfDatabase}")
            jsonTables = json.loads(getJsonTables.get_data())
            dictionaryTables[nameOfDatabase] = [tables[f"Tables_in_{nameOfDatabase}"] for tables in jsonTables]

        return dictionaryTables

    def mysql_get_values_into_table(database, table):
        client = application.test_client()

        getJsonValues = client.get(f"/api/mysql?option=get_values&database={database}&table={table}")
        jsonValues = json.loads(getJsonValues.get_data())

        return jsonValues

    @application.route("/")
    def home():
        server = ["localhost:336"]
        return render_template("index.html", data=server, databaseList=mysql_get_database_list())

    @application.route("/manage/<database>/<table>")
    def manage_table_search(database, table):
        server = ["localhost:336", database, table]
        searchData = mysql_get_values_into_table(database, table)
        return render_template("index.html", content=searchData, data=server, databaseList=mysql_get_database_list())

    @application.route("/teste")
    def teste():
        return mysql_get_values_into_table("newDB", "Tabelazinha")