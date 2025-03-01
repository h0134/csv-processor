from flask import Flask
from controller.file_controller import file_controller
import psycopg2


DB_CONFIG = {
    'dbname': 'mydb',
    'user': 'myuser',
    'password': 'mypassword',
    'host': 'localhost',
    'port': '5432'
}
SCHEMA_FILE_PATH = 'schema.sql'

def execute_sql_schema():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        with open(SCHEMA_FILE_PATH, 'r') as file:
            schema_sql = file.read()
        cursor.execute(schema_sql)
        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error executing schema: {e}")

app = Flask(__name__)
app.register_blueprint(file_controller)

if __name__ == "__main__":
    execute_sql_schema()
    app.run(debug=True)
