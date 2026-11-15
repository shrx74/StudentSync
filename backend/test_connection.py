from database.connection import Database

try:
    with Database.connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database()")
            result = cursor.fetchone()

            print("Connection successful!")
            print("Database:", result["current_database"])

except Exception as error:
    print("Connection failed:", error)
