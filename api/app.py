from flask import Flask, jsonify, request
import mysql.connector


app = Flask(__name__)
db = mysql.connector.connect(
    host="sql10.freemysqlhosting.net",
    user="sql10617616",
    password="yBdi7EmpE4",
    port="3306",
)

@app.route("/api/databases", methods=['GET'])
def show_databases():
    cursor = db.cursor()
    cursor.execute("SHOW DATABASES")

    return jsonify(cursor.fetchall())

@app.route("/api/tables", methods=['GET'])
def show_tables():
    cursor = db.cursor()
    cursor.execute(f"USE {request.args.get('database')}")
    cursor.execute("SHOW TABLES")

    return jsonify(cursor.fetchall())

@app.route("/api/columns", methods=['GET'])
def show_columns():
    cursor = db.cursor()
    cursor.execute(f"USE {request.args.get('database')}")
    cursor.execute(f"SHOW COLUMNS FROM {request.args.get('table')}")
    
    return jsonify(cursor.fetchone())

if __name__ == '__main__':
    app.run(debug=True)