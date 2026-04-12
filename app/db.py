import mysql.connector.pooling
from mysql.connector import Error
import os

_connection_pool = None


def init_connection_pool():
    global _connection_pool
    if _connection_pool is None:
        _connection_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name=os.getenv("POOL_NAME"),
            pool_size=int(os.getenv("POOL_SIZE")),
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("PORT")),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_ROOT_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            autocommit=True
        )

def get_connection():
    if _connection_pool is None:
        raise RuntimeError("Connection pool not initialized")
    return _connection_pool.get_connection()

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_ROOT_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )

        cursor = connection.cursor()
        create_table_query = """
            CREATE TABLE IF NOT EXISTS weapons (
                id INT AUTO_INCREMENT PRIMARY KEY,
                weapon_id VARCHAR(255),
                weapon_name VARCHAR(255),
                weapon_type VARCHAR(255),
                range_km INT,
                weight_kg FLOAT,
                manufacturer VARCHAR(255),
                origin_country VARCHAR(255),
                storage_location VARCHAR(255),
                year_estimated INT,
                risk_level VARCHAR(50)
            )
            """
        cursor.execute(create_table_query)
        connection.commit()
        return connection.close()
    except Error as e:
        print(f"Database connection error: {e}")
        raise

def insert_data_to_db(weapon_list):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO weapons (
                weapon_id, weapon_name, weapon_type, range_km,
                weight_kg, manufacturer, origin_country,
                storage_location, year_estimated,risk_level
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
            """
        values = [
            (
                row["weapon_id"],
                row["weapon_name"],
                row["weapon_type"],
                row["range_km"],
                row["weight_kg"],
                row["manufacturer"],
                row["origin_country"],
                row["storage_location"],
                row["year_estimated"],
                row["risk_level"]
            )
            for row in weapon_list
        ]

        cursor.executemany(query,values)
        conn.commit()
        return {
            "success": True,
            "inserted_rows": cursor.rowcount
        }
    except Error as e:
        if conn:
            conn.rollback()
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        cursor.close()
        conn.close()



