import tkinter as tk
import sqlite3
from tkinter import font as tkfont

# Create a single database connection at the beginning
db_connection = sqlite3.connect('database1.db') 
db_cursor = db_connection.cursor()

db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS table1 (
        item_id INTEGER PRIMARY KEY,
        item_name TEXT NOT NULL,
        Quantity INTEGER NOT NULL,
        item_price REAL NOT NULL
    )
''')

# Commit the changes
db_connection.commit()

# Create an empty list to store cart items
cart_items = []


def view_items():
    def see_all_items():
        # Code to retrieve and display all items from the database
        db_cursor.execute("SELECT * FROM table1")
        items = db_cursor.fetchall()

        # Display the items
        result_text.delete(1.0, tk.END)  # Clear previous results
        for item in items:
            result_text.insert(tk.END,
                               f"Item ID: {item[0]}\nItem Name: {item[1]}\nQuantity: {item[2]}\nItem Price: {item[3]}\n\n")

    def search_item():
        search_text = search_entry.get().lower()
        db_cursor.execute("SELECT * FROM table1 WHERE item_id = ? OR LOWER(item_name) = ?", (search_text, search_text))
        items = db_cursor.fetchall()

        # Display the search results
        result_text.delete(1.0, tk.END)  # Clear previous results
        for item in items:
            result_text.insert(tk.END,
                                f"Item ID: {item[0]}\nItem Name: {item[1]}\nQuantity: {item[2]}\nItem Price: {item[3]}\n\n")

    # Create the 'view_items' window
    view_items_window = tk.Toplevel(window)
    view_items_window.title("View Items")

    # Set window to full screen
    view_items_window.attributes('-fullscreen', True)

    # Get screen width and height
    screen_width = view_items_window.winfo_screenwidth()
    screen_height = view_items_window.winfo_screenheight()

    # Center the content
    frame = tk.Frame(view_items_window, bg="gray")
    frame.pack(expand=True, fill=tk.BOTH)

    bold_font1 =tkfont.Font(weight="bold", size=40,family="Times New Roman")
    bold_font2 =tkfont.Font(weight="bold", size=16,family="Times New Roman")

    # Create and place widgets in the 'view_items' window
    view_label =tk.Label(frame, text="VIEW ITEM", font=bold_font1, bg="gray",  fg="cyan")
    view_label.pack(pady=40)

    search_label = tk.Label(frame, text="Search:",font=bold_font2, bg="gray", fg="yellow")
    search_label.pack()

    search_entry = tk.Entry(frame,font=bold_font2)
    search_entry.pack(pady=10)

    search_button = tk.Button(frame, text="Search", command=search_item,font=bold_font2, bg='yellow')
    search_button.pack()

    see_all_button = tk.Button(frame, text="See All Items", command=see_all_items,font=bold_font2, bg='yellow')
    see_all_button.pack(pady=20)

    result_text = tk.Text(frame, height=10, width=40,font=bold_font2)
    result_text.pack()

    # Add a back button
    back_button = tk.Button(frame, text="Back to Main Menu", command=view_items_window.destroy,font=bold_font2, bg="red")
    back_button.pack(pady=20)


def add_to_cart():

    def search_item_for_cart():
        search_text = search_entry.get().lower()
        db_cursor.execute("SELECT * FROM table1 WHERE item_id = ? OR item_name = ?", (search_text, search_text))
        item = db_cursor.fetchone()

        if item:
            item_id_label.config(text=f"Item ID: {item[0]}", bg="gray", fg="lightgreen")
            item_name_label.config(text=f"Item Name: {item[1]}", bg="gray", fg="lightgreen")
            item_price_label.config(text=f"Item Price: {item[3]}", bg="gray", fg="lightgreen")

            if item[2] is not None and item[2] > 0:
                item_quantity_label.config(text=f"Available Quantity: {item[2]}", bg="gray", fg="lightgreen")
            else:
                item_quantity_label.config(text="Out of stock", bg="gray", fg="red")
        else:
            # Handle the case when the item is not found
            item_id_label.config(text="Item not found", bg="gray", fg="red")
            item_name_label.config(text="", bg="gray")
            item_price_label.config(text="", bg="gray")
            item_quantity_label.config(text="", bg="gray")

    def add_item_to_cart():
        if item_id_label.cget("text") != "Item not found":
            try:
                item_quantity = int(item_quantity_entry.get())
                item = {
                    "id": item_id_label.cget("text").split(": ")[1],
                    "name": item_name_label.cget("text").split(": ")[1],
                    "price": float(item_price_label.cget("text").split(": ")[1]),
                    "quantity": item_quantity
                }
                cart_items.append(item)

                # Update the cart interface
                cart_result_text.insert(tk.END, f"{item['name']} x{item['quantity']} - Rs{item['price'] * item['quantity']}\n")

                # Clear the search results
                item_id_label.config(text="")
                item_name_label.config(text="")
                item_price_label.config(text="")
                item_quantity_entry.delete(0, tk.END)
            except ValueError:
                # Handle the case when the entered quantity is not a valid integer
                item_id_label.config(text="Invalid quantity", bg="gray", fg="red")
                item_name_label.config(text="")
                item_price_label.config(text="")
        else:
            # Handle the case when the item is not found
            item_id_label.config(text="Item not found", bg="gray", fg="red")
            item_name_label.config(text="")
            item_price_label.config(text="")

    def checkout():
     
        total_cost = 0
        bill_text = "K2R Store's Bill:\n"
        
        bill_text += f"\n{'S.No':<10}{'Item Name':<15}{'Quantity':<0}{'Item Price':>15}{'Total':>10}\n"
        
        for idx, cart_item in enumerate(cart_items, start=1):
            total_cost += cart_item["price"] * cart_item["quantity"]
            item_total = cart_item['price'] * cart_item['quantity']
            bill_text += f"\n{idx:<12}{cart_item['name']:<23}{cart_item['quantity']:<0}{cart_item['price']:>20}{item_total:>17}\n"

            db_cursor.execute("UPDATE table1 SET Quantity = Quantity - ? WHERE item_id = ?",
                              (cart_item["quantity"], cart_item["id"]))

        db_connection.commit()

        bill_text += f"\n{'Total Cost:':<60} Rs.{total_cost}"

        # Additional code for checkout
        checkout_window = tk.Toplevel(window)
        checkout_window.title("Checkout")

        # Set window to full screen
        checkout_window.attributes('-fullscreen', True)

        # Get screen width and height
        screen_width = checkout_window.winfo_screenwidth()
        screen_height = checkout_window.winfo_screenheight()

        # Center the content
        frame = tk.Frame(checkout_window, bg="gray")
        frame.pack(expand=True, fill=tk.BOTH)

        bold_font1 =tkfont.Font(weight="bold", size=16,family="Georgia")
        bold_font =tkfont.Font(weight="bold", size=20, family="Courier New")
        
        checkout_result_label = tk.Label(frame, text=bill_text,font=bold_font,fg="black",bg="gray")
        checkout_result_label.pack(pady=100)

        back_to_menu_button = tk.Button(frame, text="Back to Menu", command=checkout_window.destroy,font=bold_font1, bg='red', fg='black')
        back_to_menu_button.pack(pady=20)

        # Clear the cart_items list after checkout
        cart_items.clear()
        # Clear the cart interface
        cart_result_text.delete(1.0, tk.END)

    # Create the 'add_to_cart' window
    add_to_cart_window = tk.Toplevel(window)
    add_to_cart_window.title("Add to Cart")

    # Set window to full screen
    add_to_cart_window.attributes('-fullscreen', True)

    # Get screen width and height
    screen_width = add_to_cart_window.winfo_screenwidth()
    screen_height = add_to_cart_window.winfo_screenheight()

    # Center the content
    frame = tk.Frame(add_to_cart_window, bg="gray")
    frame.pack(expand=True, fill=tk.BOTH)

    bold_font1 =tkfont.Font(weight="bold", size=40,family="Times New Roman")
    bold_font =tkfont.Font(weight="bold", size=16,family="Times New Roman")

    db_name_label = tk.Label(frame, text="ADD TO CART", font=bold_font1, bg="gray", fg="cyan")
    db_name_label.pack(pady=40)

    # Create and place widgets in the 'add_to_cart' window
    search_label = tk.Label(frame, text="Search:",font=bold_font, bg="gray", fg="yellow")
    search_label.pack()

    search_entry = tk.Entry(frame,font=bold_font)
    search_entry.pack()

    search_button = tk.Button(frame, text="Search", command=search_item_for_cart,font=bold_font, bg="yellow", fg="black")
    search_button.pack(pady=10)

    # Additional widgets for item details
    item_id_label = tk.Label(frame, text="",font=bold_font, bg="gray")
    item_id_label.pack()

    item_name_label = tk.Label(frame, text="",font=bold_font, bg="gray")
    item_name_label.pack()

    item_price_label = tk.Label(frame, text="",font=bold_font, bg="gray")
    item_price_label.pack()

    item_quantity_label = tk.Label(frame, text="Quantity:",font=bold_font, bg="gray", fg="yellow")
    item_quantity_label.pack()

    item_quantity_entry = tk.Entry(frame,font=bold_font)
    item_quantity_entry.pack()

    add_to_cart_button = tk.Button(frame, text="Add to Cart", command=add_item_to_cart,font=bold_font, bg="yellow", fg="black")
    add_to_cart_button.pack(pady=10)

    # Cart interface
    cart_result_text = tk.Text(frame, height=5, width=40,font=bold_font)
    cart_result_text.pack()

    checkout_button = tk.Button(frame, text="Checkout", command=checkout,font=bold_font, bg="yellow", fg="black")
    checkout_button.pack(pady=10)

    # Add a back button
    back_button = tk.Button(frame, text="Back to Main Menu", command=add_to_cart_window.destroy,font=bold_font, bg="red", fg="black")
    back_button.pack(pady=10)


def add_to_db():
    def add_new_item():
        item_id = item_id_entry.get()
        item_name = item_name_entry.get()
        item_quantity = item_quantity_entry.get()
        item_price = item_price_entry.get()

        if item_id and item_name and item_quantity and item_price:
            try:
                # Check if the item already exists in the database
                db_cursor.execute("SELECT * FROM table1 WHERE item_id = ?", (item_id,))
                existing_item = db_cursor.fetchone()

                if existing_item:
                    # Item exists, update the quantity by adding the new quantity
                    new_quantity = existing_item[2] + int(item_quantity)
                    db_cursor.execute("UPDATE table1 SET Quantity = ? WHERE item_id = ?", (new_quantity, item_id))
                else:
                    # Item doesn't exist, insert a new record
                    db_cursor.execute(
                        "INSERT INTO table1 (item_id, item_name, Quantity, item_price) VALUES (?, ?, ?, ?)",
                        (item_id, item_name, item_quantity, item_price))

                db_connection.commit()
                status_label.config(text="Item added or modified in the database", fg="lightgreen")

                # Clear the input fields
                item_id_entry.delete(0, tk.END)
                item_name_entry.delete(0, tk.END)
                item_quantity_entry.delete(0, tk.END)
                item_price_entry.delete(0, tk.END)

            except sqlite3.Error as e:
                status_label.config(text="Error adding or modifying item in the database", fg="red")
        else:
            status_label.config(text="Please fill in all fields", fg="red")

    # Create the 'add_to_db' window
    add_to_db_window = tk.Toplevel(window)
    add_to_db_window.title("Add to Database")

    
    # Set window to full screen
    add_to_db_window.attributes('-fullscreen', True)

    # Get screen width and height
    screen_width = add_to_db_window.winfo_screenwidth()
    screen_height = add_to_db_window.winfo_screenheight()

    # Center the content
    frame = tk.Frame(add_to_db_window, bg="gray")
    frame.pack(expand=True, fill=tk.BOTH)

    bold_font1a =tkfont.Font(weight="bold", size=40,family="Courier New")
    bold_fonta =tkfont.Font( weight="bold",size=16,family="Georgia")

    # Create and place widgets in the 'add_to_db' window
    # Additional widgets for item details
    db_name_label = tk.Label(frame, text="ADD TO STORE", font=bold_font1a, bg="gray", fg="cyan")
    db_name_label.pack(pady=80)
    
    item_id_label = tk.Label(frame, text="Item ID:",font=bold_fonta, fg='yellow', bg='gray')
    item_id_label.pack()

    item_id_entry = tk.Entry(frame, font=bold_fonta)
    item_id_entry.pack(pady=10)

    item_name_label = tk.Label(frame, text="Item Name:",font=bold_fonta, fg='yellow', bg='gray')
    item_name_label.pack()

    item_name_entry = tk.Entry(frame, font=bold_fonta)
    item_name_entry.pack(pady=10)

    item_quantity_label = tk.Label(frame, text="Quantity:",font=bold_fonta, fg='yellow', bg='gray')
    item_quantity_label.pack()

    item_quantity_entry = tk.Entry(frame, font=bold_fonta)
    item_quantity_entry.pack(pady=10)

    item_price_label = tk.Label(frame, text="Item Price:",font=bold_fonta, fg='yellow', bg='gray')
    item_price_label.pack()

    item_price_entry = tk.Entry(frame, font=bold_fonta)
    item_price_entry.pack(pady=10)

    add_to_db_button = tk.Button(frame, text="Add to Database", command=add_new_item, font=bold_fonta, bg='yellow', fg='black')
    add_to_db_button.pack(pady=20)

    status_label = tk.Label(frame, text="", bg='gray', font=bold_fonta)
    status_label.pack(pady=10)

    # Add a back button
    back_button = tk.Button(frame, text="Back to Main Menu", command=add_to_db_window.destroy, font=bold_fonta, bg='red', fg='black')
    back_button.pack()


# Create the main window
window = tk.Tk()
window.title("K2R Store's")
window.configure(bg="gray")

# Set window to full screen
window.attributes('-fullscreen', True)

# Get screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Center the content
frame = tk.Frame(window, bg="gray")
frame.pack(expand=True, fill=tk.BOTH)

bold_font1 =tkfont.Font(weight="bold", size=60, family="Times New Roman")
bold_font =tkfont.Font(weight="bold", size=16,family="Times New Roman")

app_name_label = tk.Label(frame, text="K2R STORE's", font=bold_font1, bg="gray", fg="cyan")
app_name_label.pack(pady=100)


# Create buttons for the menu options
view_items_button = tk.Button(frame, text="View Items", command=view_items,font=bold_font, bg='yellow', fg='black')
view_items_button.pack(pady=20)

add_to_cart_button = tk.Button(frame, text="Add to Cart", command=add_to_cart,font=bold_font, bg='yellow', fg='black')
add_to_cart_button.pack(pady=20)

add_to_db_button = tk.Button(frame, text="Add to Database", command=add_to_db,font=bold_font, bg='yellow', fg='black')
add_to_db_button.pack(pady=20)

exit_button = tk.Button(frame, text="Exit", command=window.destroy,font=bold_font, bg='red', fg='black')
exit_button.pack(pady=20)

# Start the main loop
window.mainloop()

# Close the database connection when the application is done
db_connection.close()
