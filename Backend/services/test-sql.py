import mysql.connector as pymysql

def test_sql_connection():
    # Replace with your database connection details
    host = "localhost"
    user = "root"
    password = ""
    database = "hetuvan"

    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print("SQL connection successful!")
        connection.close()
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")

if __name__ == "__main__":
    test_sql_connection()