import sqlite3

# Establish a connection to the SQLite database
conn = sqlite3.connect('inventory.db')  # This creates a database file if it doesn't exist

# Create a cursor object
cursor = conn.cursor()

# SQL query to create a table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
"""
cursor.execute(create_table_query)

# Function to insert data into the table
def add_item(item_name, quantity, price):
    insert_query = """
    INSERT INTO items (item_name, quantity, price)
    VALUES (?, ?, ?)
    """
    cursor.execute(insert_query, (item_name, quantity, price))
    conn.commit()
    print(f"Item '{item_name}' added successfully!")

# Example of adding an item
item_name = input("Enter item name: ")
quantity = int(input("Enter item quantity: "))
price = float(input("Enter item price: "))

# Add the item to the database
add_item(item_name, quantity, price)

# Close the cursor and connection
cursor.close()
conn.close()
