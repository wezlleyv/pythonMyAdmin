from flask import Flask, jsonify, request
import mysql.connector


app = Flask(__name__)
db = mysql.connector.connect(
    host="0.0.0.0",
    user="root",
    password="root",
    port="3306",
)

@app.route("/api/databases", methods=['GET'])
def show_databases():
    cursor = db.cursor()
    cursor.execute("SHOW DATABASES")

    return jsonify(cursor.fetchall())

@app.route("/api/tables", methods=['GET'])
def show_tables():
    databaseName = request.args.get('database')

    cursor = db.cursor()
    cursor.execute(f"USE {databaseName}")
    cursor.execute("SHOW TABLES")

    return jsonify(cursor.fetchall())

@app.route("/api/columns", methods=['GET'])
def show_columns():
    databaseName = request.args.get('database')
    tableName = request.args.get('table')

    cursor = db.cursor()
    cursor.execute(f"USE {databaseName}")
    cursor.execute(f"SHOW COLUMNS FROM {tableName}")
    
    return jsonify(cursor.fetchone())

@app.route("/api/createdatabase", methods=['GET'])
def create_database():
    newDatabaseName = request.args.get('database')

    cursor = db.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {newDatabaseName}")

    return "Create"


if __name__ == '__main__':
    app.run(debug=True)