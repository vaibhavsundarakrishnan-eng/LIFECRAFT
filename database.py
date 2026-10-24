
import os
import mysql.connector


def connect_db():

    # Deployed website: connect to Railway using Render variables
    if os.environ.get("MYSQLHOST"):

        return mysql.connector.connect(
            host=os.environ["MYSQLHOST"],
            port=int(os.environ["MYSQLPORT"]),
            user=os.environ["MYSQLUSER"],
            password=os.environ["MYSQLPASSWORD"],
            database=os.environ["MYSQLDATABASE"]
        )

    # Local computer: connect to your local MySQL
    # Local app: use your local MySQL settings
    return mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.environ["LOCAL_MYSQL_PASSWORD"],
    database="lifecraft"
)

if __name__ == "__main__":

    try:
        conn = connect_db()

        if conn.is_connected():
            print("Database connected successfully!")

        conn.close()

    except mysql.connector.Error as err:
        print("Database connection failed:", err)
