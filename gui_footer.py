import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

# Function to create the footer label
def create_footer(window):
    footer_label = Label(window, text="Designed by: Soumya Ranjan Mohanty", font=("Helvetica", 15, "italic"), bg="#e8f5e9", fg="#4caf50")
    footer_label.pack(side=BOTTOM, pady=5)

# Function to verify user credentials using the user_data.db
def verify_login():
    user_id = entry_id.get()
    password = entry_password.get()

    # Connect to the user_data database for login verification
    conn_user = sqlite3.connect('user_data.db')
    cursor_user = conn_user.cursor()

    # Fetch user details from the user_data database
    cursor_user.execute('SELECT * FROM users WHERE id = ? AND password = ?', (user_id, password))
    result = cursor_user.fetchone()

    if result:
        conn_user.close()  # Close the user_data.db connection
        open_success_window()  # If valid credentials, open a success window
    else:
        conn_user.close()  # Close the user_data.db connection
        messagebox.showerror("Login Failed", "Invalid User ID or Password")

# Function to open a success window with additional options
def open_success_window():
    success_window = Toplevel(root)
    success_window.title("Dashboard")
    success_window.geometry("600x400")
    
    # Add background image
    bg_image = Image.open("idk1.png")  # Load .png image
    bg_photo = ImageTk.PhotoImage(bg_image.resize((600, 400)))
    bg_label = Label(success_window, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(relwidth=1, relheight=1)

    Label(success_window, text="Login Successful!", font=("Helvetica", 16), bg="white", fg="black").pack(pady=20)
    
    # Add buttons for the requested functionalities
    Button(success_window, text="Search Items", font=("Helvetica", 12), command=search_items, bg="#007BFF", fg="black").pack(pady=10)
    Button(success_window, text="Update Pricing and Quantity", font=("Helvetica", 12), command=update_pricing_quantity, bg="#28A745", fg="black").pack(pady=10)
    Button(success_window, text="Generate Bill", font=("Helvetica", 12), command=open_generate_bill_window, bg="#FFC107", fg="black").pack(pady=10)
    
    # Add footer
    create_footer(success_window)

# Functionality for searching items from inventory.db
def search_items():
    search_window = Toplevel(root)
    search_window.title("Search Items")
    search_window.geometry("400x300")
    
    # Add background image
    bg_image = Image.open("idk1.png")  # Load .png image
    bg_photo = ImageTk.PhotoImage(bg_image.resize((400, 300)))  # Resize to fit the window
    bg_label = Label(search_window, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
    bg_label.place(relwidth=1, relheight=1)  # Place the image to cover the entire window

    # Label for "Enter Item Name"
    Label(search_window, text="Enter Item Name:", font=("Helvetica", 12), bg="black", fg="white").pack(pady=10)
    search_entry = Entry(search_window, font=("Helvetica", 12), fg="white", bg="black")
    search_entry.pack(pady=10)

    # Function to handle the search operation
    def perform_search():
        item_name = search_entry.get().strip()

        if not item_name:  # Check if the input is empty
            messagebox.showerror("Input Error", "Please enter an item name.")
            return

        # Connect to the inventory database
        conn_inventory = sqlite3.connect('inventory.db')
        cursor_inventory = conn_inventory.cursor()

        # Query the database for the item
        cursor_inventory.execute("SELECT price, quantity FROM items WHERE item_name = ?", (item_name,))
        result = cursor_inventory.fetchone()

        if result:
            price, quantity = result
            if quantity > 0:
                messagebox.showinfo(
                    "Item Found",
                    f"Item: {item_name}\nPrice: ${price:.2f}\nQuantity in stock: {quantity}"
                )
            else:
                messagebox.showwarning("Out of Stock", f"The item '{item_name}' is currently out of stock.")
        else:
            messagebox.showerror("Item Not Found", f"The item '{item_name}' does not exist in the inventory.")

        conn_inventory.close()  # Close the database connection

    # Button to trigger the search operation
    Button(search_window, text="Search", font=("Helvetica", 12), command=perform_search, bg="#007BFF", fg="black").pack(pady=20)

    # Add footer
    create_footer(search_window)

# Placeholder function for updating pricing and quantity (can be expanded)
def update_pricing_quantity():
    messagebox.showinfo("Update Pricing and Quantity", "Update pricing and quantity functionality triggered.")

# Function for updating the price and quantity of an item
def update_pricing_quantity():
    update_window = Toplevel(root)
    update_window.title("Update Pricing and Quantity")
    update_window.geometry("400x300")
    
    # Add background image that resizes dynamically with the window
    bg_image = Image.open("idk1.png")
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(update_window, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(relwidth=1, relheight=1)

    # Entry fields for item name, price, and quantity
    Label(update_window, text="Item Name:", font=("Helvetica", 12), bg="black", fg="white").pack(pady=10)
    item_name_entry = Entry(update_window, font=("Helvetica", 12), fg="black", bg="white")
    item_name_entry.pack(pady=10)

    Label(update_window, text="New Price:", font=("Helvetica", 12), bg="black", fg="white").pack(pady=10)
    price_entry = Entry(update_window, font=("Helvetica", 12), fg="black", bg="white")
    price_entry.pack(pady=10)

    Label(update_window, text="New Quantity:", font=("Helvetica", 12), bg="black", fg="white").pack(pady=10)
    quantity_entry = Entry(update_window, font=("Helvetica", 12), fg="black", bg="white")
    quantity_entry.pack(pady=10)

    # Function to update price and quantity in the database
    def perform_update():
        item_name = item_name_entry.get().strip()
        new_price = price_entry.get().strip()
        new_quantity = quantity_entry.get().strip()

        # Check if fields are empty
        if not item_name or not new_price or not new_quantity:
            messagebox.showerror("Input Error", "All fields are required.")
            return
        
        try:
            # Convert new_price and new_quantity to appropriate types
            new_price = float(new_price)
            new_quantity = int(new_quantity)
            
            # Connect to the inventory database
            conn_inventory = sqlite3.connect('inventory.db')
            cursor_inventory = conn_inventory.cursor()

            # Check if the item exists
            cursor_inventory.execute("SELECT * FROM items WHERE item_name = ?", (item_name,))
            result = cursor_inventory.fetchone()

            if result:
                # Update price and quantity for the item
                cursor_inventory.execute("UPDATE items SET price = ?, quantity = ? WHERE item_name = ?",
                                          (new_price, new_quantity, item_name))
                conn_inventory.commit()  # Commit changes
                messagebox.showinfo("Update Successful", f"Item '{item_name}' updated successfully.")
            else:
                messagebox.showerror("Item Not Found", f"Item '{item_name}' does not exist in the inventory.")

            conn_inventory.close()  # Close the database connection
            
            # Clear the entry fields after successful update
            item_name_entry.delete(0, END)
            price_entry.delete(0, END)
            quantity_entry.delete(0, END)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid price and quantity.")

    # Button to trigger the update operation
    Button(update_window, text="Update", font=("Helvetica", 12), command=perform_update, bg="#007BFF", fg="black").pack(pady=20)

    # Add footer
    create_footer(update_window)

# Function to open the "Generate Bill" window and calculate the total bill from inventory.db
def open_generate_bill_window():
    bill_window = Toplevel(root)
    bill_window.title("Generate Bill")
    bill_window.geometry("500x500")
    
    # Add background image
    bg_image = Image.open("idk1.png")  # Load .png image
    bg_photo = ImageTk.PhotoImage(bg_image.resize((500, 500)))
    bg_label = Label(bill_window, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(relwidth=1, relheight=1)

    Label(bill_window, text="Generate Bill", font=("Helvetica", 16, "bold"), bg="white", fg="black").pack(pady=10)

    # Input fields for bill generation
    Label(bill_window, text="Item Name:", font=("Helvetica", 12), bg="white", fg="black").pack(pady=5)
    item_name_entry = Entry(bill_window, font=("Helvetica", 12), fg="black", bg="white")
    item_name_entry.pack(pady=5)

    Label(bill_window, text="Quantity:", font=("Helvetica", 12), bg="white", fg="black").pack(pady=5)
    quantity_entry = Entry(bill_window, font=("Helvetica", 12), fg="black", bg="white")
    quantity_entry.pack(pady=5)

    # Listbox to display added items
    item_listbox = Listbox(bill_window, font=("Helvetica", 12), width=40, height=10, fg="black", bg="white")
    item_listbox.pack(pady=10)

    # Label to display total bill
    total_label = Label(bill_window, text="Total Bill: $0.00", font=("Helvetica", 14, "bold"), bg="white", fg="black")
    total_label.pack(pady=10)

    # Function to calculate the total bill
    def calculate_total():
        try:
            item_name = item_name_entry.get().strip()
            quantity = int(quantity_entry.get())

            if not item_name or quantity <= 0:
                messagebox.showerror("Invalid Input", "Please enter a valid item name and quantity.")
                return

            # Connect to the inventory database for fetching price
            conn_inventory = sqlite3.connect('inventory.db')
            cursor_inventory = conn_inventory.cursor()

            cursor_inventory.execute("SELECT price FROM items WHERE item_name = ?", (item_name,))
            result = cursor_inventory.fetchone()

            if result:  # If item is found in the database
                price = float(result[0])  # Fetch the price from the result
                total_item_price = quantity * price
                item_listbox.insert(END, f"{item_name} - Quantity: {quantity} - Price: ${total_item_price:.2f}")

                # Calculate total bill from all items in the listbox
                total_amount = 0
                for entry in item_listbox.get(0, END):
                    price_str = entry.split(": $")[-1]
                    total_amount += float(price_str)

                total_label.config(text=f"Total Bill: ${total_amount:.2f}")

                item_name_entry.delete(0, END)
                quantity_entry.delete(0, END)
            else:
                messagebox.showerror("Item Not Found", f"Item '{item_name}' not found in the inventory.")
            
            conn_inventory.close()  # Close the inventory.db connection

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid quantities and prices.")

    Button(bill_window, text="Calculate", font=("Helvetica", 12), command=calculate_total, bg="#007BFF", fg="black").pack(pady=10)
    create_footer(bill_window)
# Main login window
root = Tk()
root.title("Login")
root.geometry("400x300")

# Add background image
bg_image = Image.open("idk1.png")
bg_photo = ImageTk.PhotoImage(bg_image.resize((400, 300)))
bg_label = Label(root, image=bg_photo)
bg_label.image = bg_photo
bg_label.place(relwidth=1, relheight=1)

# User ID and Password Entry fields
Label(root, text="User ID:", font=("Helvetica", 12), bg="black", fg="white").pack(pady=10)
entry_id = Entry(root, font=("Helvetica", 12), fg="black", bg="white")
entry_id.pack(pady=10)

Label(root, text="Password:", font=("Helvetica", 12), bg="black", fg="white").pack(pady=10)
entry_password = Entry(root, font=("Helvetica", 12), show="*", fg="black", bg="white")
entry_password.pack(pady=10)

# Login button
Button(root, text="Login", font=("Helvetica", 12), command=verify_login, bg="#007BFF", fg="black").pack(pady=20)

# Add footer to root window
create_footer(root)

root.mainloop()
