import sqlite3

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Create a table if it doesn't already exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Commit changes
conn.commit()

# Function to insert user data
def save_user_data(user_id, username, password):
    cursor.execute('''
    INSERT INTO users (id, username, password)
    VALUES (?, ?, ?)
    ''', (user_id, username, password))
    conn.commit()
    print("User data saved successfully.")

# Take input from the user
user_id = input("Enter User ID (integer): ")
username = input("Enter Username: ")
password = input("Enter Password: ")

# Save user data to the database
try:
    save_user_data(int(user_id), username, password)
except ValueError:
    print("Invalid ID. Please enter an integer value.")
except sqlite3.IntegrityError:
    print("Error: User ID must be unique.")

# Close the connection
conn.close()
