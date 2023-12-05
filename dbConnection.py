
import mysql.connector

# Replace these with your MySQL server details
host = "your_host"
user = "your_user"
password = "your_password"
database = "your_database"

# Establish a connection to the MySQL server
try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Naveen19111998',
        database='parking'
    )
    if connection.is_connected():
        print("Connected to MySQL server")

        # Create a cursor object to interact with the database
        mycursor = connection.cursor()

        # Create the 'users' table if it doesn't exist
        mycursor.execute("""CREATE TABLE IF NOT EXISTS users (
                            number_plate VARCHAR(255) PRIMARY KEY,
                            entered_time VARCHAR(255), place varchar(250) , username varchar(250)
                        )""")

        # Commit the changes to the database
        connection.commit()

        print("Table 'users' created successfully.")

    else:
        print("Failed to connect to MySQL server")

except mysql.connector.Error as e:
    print(f"Error: {e}")

