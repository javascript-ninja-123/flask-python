import sqlite3

databse = "data.db"


def connect(database_url):
    connection = None
    try:
        connection = sqlite3.connect(database_url)
        cursor = connection.cursor()

        create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"

        create_table2 = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"

        cursor.execute(create_table)
        cursor.execute(create_table2)

        cursor.execute("INSERT INTO items VALUES ('test', 12.99)")

        connection.commit()

    except:
        print("not good")
    finally:
        if connection:
            connection.close()


connect(databse)
