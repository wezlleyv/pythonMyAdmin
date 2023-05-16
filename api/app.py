from flask import Flask, jsonify, request
import mysql.connector, json

app = Flask(__name__)
db = mysql.connector.connect(
    host="0.0.0.0",
    user="root",
    password="root",
    port="3306",
)

@app.route("/api/databases", methods=['GET'])
def show_databases():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SHOW DATABASES")

    response = cursor.fetchall()

    return jsonify(response)

@app.route("/api/tables", methods=['GET'])
def show_tables():
    databaseName = request.args.get('database')

    cursor = db.cursor(dictionary=True)
    cursor.execute(f"USE {databaseName}")
    cursor.execute("SHOW TABLES")

    response = cursor.fetchall()

    return jsonify(response)

@app.route("/api/columns", methods=['GET'])
def show_columns():
    databaseName = request.args.get('database')
    tableName = request.args.get('table')

    cursor = db.cursor(dictionary=True)
    cursor.execute(f"USE {databaseName}")
    cursor.execute(f"SHOW COLUMNS FROM {tableName}")

    response = cursor.fetchall()

    return jsonify(response)

@app.route("/api/createdatabase", methods=['POST'])
def create_database():
    newDatabaseName = request.form.get('database')

    cursor = db.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {newDatabaseName}")

    return f"Create {newDatabaseName}"

@app.route("/api/createtable", methods=['POST'])
def create_table():
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
    jsonData = request.get_json()
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

    cursor = db.cursor()
    cursor.execute(f"USE {databaseName}")
    cursor.execute(querySQL)
    

    return querySQL

@app.route("/api/insert", methods=['GET', 'POST'])
def insert_into():
    database = request.args.get('database')
    table = request.args.get('table')
    client = app.test_client()

    response = client.get(f"/api/columns?database={database}&table={table}")
    response = json.loads(response.get_data())
    
    if request.method == "POST":
        columns = []
        for columnsInFor in range(len(response)):
            columns.append(response[columnsInFor]['Field'])

        jsonData = request.get_json()
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

        cursor = db.cursor()
        cursor.execute(querySQL)

        return f"Finished insert into {table}"


if __name__ == '__main__':
    app.run(debug=True)