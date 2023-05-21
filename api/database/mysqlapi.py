from flask import request, jsonify
from flask.views import MethodView
import json


class MySQL(MethodView):
    init_every_request = False

    def __init__(self, server, application):
        self.database = server
        self.app = application
    
    # GET method

    def get_databases(self):
        cursor = self.database.cursor(dictionary=True)
        cursor.execute("SHOW DATABASES")

        response = cursor.fetchall()

        return jsonify(response)

    def get_tables(self, database):
        databaseName = database

        cursor = self.database.cursor(dictionary=True)
        cursor.execute(f"USE {databaseName}")
        cursor.execute("SHOW TABLES")

        response = cursor.fetchall()

        return jsonify(response)

    def get_columns(self, database, table):
        databaseName = database
        tableName = table

        cursor = self.database.cursor(dictionary=True)
        cursor.execute(f"USE {databaseName}")
        cursor.execute(f"SHOW COLUMNS FROM {tableName}")

        response = cursor.fetchall()

        return jsonify(response)

    def get(self):
        requestGet = request.args
        option = request.args.get("option")

        if option == "get_databases":
            return self.get_databases()
        elif option == "get_tables":
            return self.get_tables(requestGet.get("database"))
        elif option == "get_columns":
            return self.get_columns(requestGet.get("database"), requestGet.get("table"))
    
    # POST method

    def create_databases(self, database):
        newDatabaseName = database

        cursor = self.database.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {newDatabaseName}")

        return f"Create {newDatabaseName}"
    
    def create_table(self, jsonData):
        ''' Estructure SQL create JSON table
        {
            "database": "Name of database",
            "table": "Name of table for create",
            "columns": {
                "name of columns": {
                    "type": ["varchar(100)", ...]
                }
            }
        }
        '''
        databaseName = jsonData["database"]
        newTableName = jsonData["table"]
        tableColumns = jsonData["columns"]

        cache = ""

        for objType in tableColumns:
            cache += objType + " "
            cache += " ".join(tableColumns[objType]["type"]) + ","


        querySQL = f'''
        CREATE TABLE {newTableName} (
            {cache[:-1]}
        )
        '''

        cursor = self.database.cursor()
        cursor.execute(f"USE {databaseName}")
        cursor.execute(querySQL)
        

        return f"Create {newTableName}"

    def create_values(self, jsonData, database, table):
        client = self.app.test_client()

        response = client.get(f"/api/mysql?option=get_columns&database={database}&table={table}")
        response = json.loads(response.get_data())
        
        
        columns = []
        for columnsInFor in range(len(response)):
            columns.append(response[columnsInFor]['Field'])

        # { "values": [.., .., ..,] } in order
        valuesList = jsonData['values']

        values = []
        for value in valuesList:
            if type(value) == int: pass
            else:
                value = f"'{value}'"
            
            values.append(value)

        valuesQuerySQL = ', '.join(str(value) for value in values)
        columnsQuerySQL = ', '.join(columns)

        querySQL = f"INSERT INTO {table} ({columnsQuerySQL}) VALUES ({valuesQuerySQL})"

        cursor = self.database.cursor()
        cursor.execute(querySQL)

        return f"Finished insert into {table}"

    def execute_query(self, jsonData):
        try:
            query = jsonData['query']
            cursor = self.database.cursor()
            cursor.execute(query)

            return "Sucessfuly"
        except Exception as arr:
            return arr

    def post(self):
        option = request.args.get("option")

        if option == "create_database":
            return self.create_databases(request.args.get("database"))
        elif option == "create_table":
            return self.create_table(request.get_json())
        elif option == "create_values":
            return self.create_values(request.get_json(), request.args.get("database"), request.args.get("table"))
        
        return "Where is the option?"
