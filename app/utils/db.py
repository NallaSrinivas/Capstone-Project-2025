import sqlite3

def check_data_in_db():
    with sqlite3.connect("skillforge.db") as connection: # change to your db file
        cursor = connection.cursor()
        result = cursor.execute(
            "select app_name, session_id, author, content from events"
        )
        print([_[0]+"\n" for _ in result.description])
        for each in result.fetchall():
            print("\n",each)


check_data_in_db()