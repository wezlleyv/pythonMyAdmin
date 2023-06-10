from flask import request
from flask.views import MethodView



class PostgreSQL(MethodView):
    init_every_request = False

    def __init__(self, server, application):
        self.database = server
        self.app = application

    # GET METHOD

    def get_databases(self):
        cursor = self.database.cursor()
        cursor.execute("SELECT datname FROM pg_database")

        tables = []
        for table in cursor.fetchall():
            tables.append(table)

        return tables
    
    def get_tables(self):
        cursor = self.database.cursor()
        cursor.execute(f"""
        SELECT
            table_schema || '.' || table_name
        FROM
            information_schema.tables
        WHERE
            table_type = 'BASE TABLE'
        AND
            table_schema NOT IN ('pg_catalog', 'information_schema');
        """)

        '''tables = []
        for table in cursor.fetchall():
            tables.append(table)'''

        return cursor.fetchall()

    def get(self):
        option = request.args.get("option")
        
        if option == "get_databases":
            return self.get_databases()
        elif option == "get_tables":
            return self.get_tables()

    # POST METHOD

    def create_databases(self):
        newDatabaseName = request.args.get("database")

        self.database.autocommit = True

        cursor = self.database.cursor()
        cursor.execute(f"CREATE DATABASE {newDatabaseName}")

        return f"Create {newDatabaseName}"

    def create_table(self):
        jsonData = request.get_json()

        databaseName = jsonData["database"]
        newTableName = jsonData["table"]
        columns = jsonData["columns"]

        cache = ""
        for typecolumn in columns:
            cache += f"{typecolumn} "
            cache += " ".join(columns[typecolumn]["type"]) + ","

        querySQL = f"""
        CREATE TABLE {newTableName} (
            {cache[:-1]}
        )
        """


        cursor = self.database.cursor()
        #cursor.execute(f"SET search_path TO {databaseName}")
        #cursor.execute(f"GRANT ALL ON SCHEMA my_custom_schema TO my_user")
        cursor.execute(querySQL)

        return "Create %s" % databaseName

    def post(self):
        option = request.args.get("option")

        if option == "create_database":
            return self.create_databases()
        elif option == "create_table":
            return self.create_table()
