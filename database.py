import os
import mysql.connector


def connect_db():
    return mysql.connector.connect(
        host=os.environ.get("MYSQLHOST", "localhost"),
        port=int(os.environ.get("MYSQLPORT", 3306)),
        user=os.environ.get("MYSQLUSER", "root"),
        password=os.environ.get("MYSQLPASSWORD", "sairam123!!!?"),
        database=os.environ.get("MYSQLDATABASE", "lifecraft")
    )


if __name__ == "__main__":
    conn = connect_db()

    if conn.is_connected():
        print("Database connected successfully!")
        conn.close()