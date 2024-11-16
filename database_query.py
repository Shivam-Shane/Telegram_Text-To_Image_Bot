import sqlite3

# Replace 'your_database.db' with the actual name of your database file
connection = sqlite3.connect('user_conversations.db')
cursor = connection.cursor()

# Example query to fetch all rows from a table
cursor.execute("SELECT * FROM conversations")
rows = cursor.fetchall()
# Print the result
for row in rows:
    print(row)

# Close the connection to the database