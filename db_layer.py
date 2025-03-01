import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from config import Config
DB_CONFIG = {
    'dbname': Config.dbname,
    'user': Config.user,   
    'password': Config.password,
    'host': Config.host,
    'port': Config.port
}

@contextmanager
def get_db_connection():
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()  
    except Exception as e:
        connection.rollback() 
        print(f"Error in transaction: {e}")
    finally:
        cursor.close()
        connection.close()
def insert_product_details(serial_number, product_name, input_image_urls,request_id,output_image_urls):
    try:
        # Use the context manager to handle the DB connection
        with get_db_connection() as cursor:
            cursor.execute(
                "INSERT INTO product_images (serial_number, product_name, input_image_urls,request_id,output_image_urls) "
                "VALUES (%s, %s, %s,%s,%s)",
                (serial_number, product_name, input_image_urls,request_id,output_image_urls)
            )
    except Exception as e:
        print(f"Error inserting data into the database: {e}")
        return False
    return True


def get_product_by_requestId(request_id: str):
    try:
        with get_db_connection() as cursor:
            cursor.execute("SELECT serial_number, request_id, product_name, input_image_urls,output_image_urls FROM product_images WHERE request_id = %s", (request_id,))
            return cursor.fetchall() 
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def insert_request_status(request_id: str, request_status: str):
    try:
        with get_db_connection() as cursor:
            cursor.execute(
                "INSERT INTO request_details (request_id, request_status) "
                "VALUES (%s, %s)",
                (request_id, request_status)
            )
    except Exception as e:
        print(f"Error inserting data into the database: {e}")
        return False
    return True

def get_request_status(request_id: str):
    try:
        with get_db_connection() as cursor:
            cursor.execute("SELECT request_status FROM request_details WHERE request_id = %s", (request_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None 
    except Exception as e:
        print(f"Error fetching request status: {e}")
        return None


def update_request_status(request_id: str, new_request_status: str):
    try:
        with get_db_connection() as cursor:
            cursor.execute(
                "UPDATE request_details SET request_status = %s WHERE request_id = %s",
                (new_request_status, request_id)
            )
            if cursor.rowcount > 0:
                print(f"Request status for {request_id} updated to {new_request_status}.")
                return True
            else:
                print(f"No request found with request_id {request_id}.")
                return False
    except Exception as e:
        print(f"Error updating request status: {e}")
        return False