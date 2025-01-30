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
