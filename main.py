#Limosnero, Sherwin P.
#J1S

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os.path

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("840x405+0+0")
        self.title("Inventory Management System")
        self.resizable(False, False)
        
        # Title label
        lbl_title = tk.Label(self, bd=15, relief=tk.RIDGE, text="INVENTORY MANAGEMENT SYSTEM", fg="blue", bg="linen", font=("times new roman", 20, "bold"))
        lbl_title.pack(side=tk.TOP, fill=tk.X)
        
        # Treeview widget
        tree_frame = tk.Frame(self, bd=15, relief=tk.RIDGE, width=700, height=500)
        tree_frame.place(x=0, y=65)
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Price", "Quantity"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Quantity", text="Quantity")

        # Center align all columns
        for col in self.tree["columns"]:
            self.tree.column(col, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(expand=True, fill="both", padx=5, pady=5)

        # Main functions
        self.Tree()
        self.Button()
        self.MenuBar()

    def Tree(self):
        # Clear existing data
        self.tree.delete(*self.tree.get_children())

        # Check if the database file exists
        if os.path.isfile('inventory.db'):
            # Retrieve data from the SQLite database and insert it into the Treeview
            conn = sqlite3.connect('inventory.db')
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                                ID INTEGER PRIMARY KEY,
                                Name TEXT NOT NULL,
                                Price REAL NOT NULL,
                                QUANTITY INTEGER NOT NULL)''')
            
            rows = cursor.execute("SELECT * FROM products").fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
            
            # Close the connection
            conn.close()
        else:
            messagebox.showwarning("Database Not Found", "No database file found. Proceeding without database functionality.")
    
    
    #Button widgets below treeview    
    def Button(self):           
        #Button frame for buttons
        button_frame = tk.Frame(self, bd=15, relief=tk.RIDGE, width=700, height=70)
        button_frame.place(x=0, y=335)
        
        #Add a new product by entering its name, price, and quantity.
        btn_add = tk.Button(button_frame, command=self.add, text="Add", fg="white", bg="green", font=("times new roman", 11, "bold"), width=17, height=1, padx=4, pady=6)
        btn_add.grid(row=0, column=0)
        
        #Remove a product from the inventory by searching for its ID and confirming removal.
        btn_remove = tk.Button(button_frame, command=self.remove, text="Remove", bg="red", fg="white", font=("times new roman", 11, "bold"), width=17, height=1, padx=4, pady=6)
        btn_remove.grid(row=0, column=1)
        
        #View all existing products stored in the inventory, including their ID, name, price, and quantity.
        btn_view = tk.Button(button_frame, command=self.view, text="View", fg="white", bg="green", font=("times new roman", 11, "bold"), width=18, height=1, padx=4, pady=6)
        btn_view.grid(row=0, column=2)
        
        #Update the details of an existing product by searching for its ID and providing new information.
        btn_update = tk.Button(button_frame, command=self.update, text="Update", bg="green", fg="white", font=("times new roman", 11, "bold"), width=16, height=1, padx=4, pady=6)
        btn_update.grid(row=0, column=3)
        
        # Exit the application.
        btn_exit = tk.Button(button_frame, command=self.exit_confirmation, text="Exit", bg="red", fg="white", font=("times new roman", 11, "bold"), width=14, height=1, padx=4, pady=6)
        btn_exit.grid(row=0, column=5)
        
        # exit window (x)
        self.protocol("WM_DELETE_WINDOW", self.exit_confirmation)



#Functions for the buttons

    # Add button function
    def add(self):
        # Function to add product to database
        def add_product():
            # Retrieve data from entry fields
            name = name_entry.get()
            price = price_entry.get()
            quantity = quantity_entry.get()
            
            # Check if the name contains only letters or spaces
            if not name.replace(" ", "").isalpha():
                messagebox.showerror("Invalid Input", "Name should contain only letters or spaces.")
                return
            
            # Check if price and quantity contain only numbers
            try:
                price = float(price)
                quantity = int(quantity.replace(",", ""))  # Remove commas before converting to integer
            except ValueError:
                messagebox.showerror("Invalid Input", "Price and Quantity should contain only numbers.")
                return
            
            # Insert data into the database
            conn = sqlite3.connect('inventory.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
            conn.commit()
            conn.close()
            
            # Refresh the Treeview to display the newly added product
            self.Tree()
            # Close the window after adding product
            add_window.destroy()
        
        # Open a new window for adding a product
        add_window = tk.Toplevel(self)
        add_window.geometry("300x200")
        add_window.title("Add Product")
        add_window.resizable(False, False)
        add_window.configure(bd=20, relief=tk.RIDGE)
        
        # Label and entry for Name
        name_label = tk.Label(add_window, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()
        name_entry.config(validate="key", validatecommand=(name_entry.register(lambda char: char.isalpha() or char == ' '), "%S"))  # Validate input to allow only letters or spaces
        
        # Label and entry for Price
        price_label = tk.Label(add_window, text="Price:")
        price_label.pack()
        price_entry = tk.Entry(add_window)
        price_entry.pack()
        price_entry.config(validate="key", validatecommand=(price_entry.register(lambda char: char.isdigit() or char == '.'), "%S"))  # Validate input to allow only numbers and decimal point
        
        # Label and entry for Quantity
        quantity_label = tk.Label(add_window, text="Quantity:")
        quantity_label.pack()
        quantity_entry = tk.Entry(add_window)
        quantity_entry.pack()
        quantity_entry.config(validate="key", validatecommand=(quantity_entry.register(lambda char: char.isdigit() or char == ','), "%S"))  # Validate input to allow only numbers and comma
        
        # Function to insert comma every third digit in quantity
        def insert_commas(char):
            if char.isdigit():
                value = quantity_entry.get().replace(",", "") + char
                value = "{:,}".format(int(value))  # Add commas every third digit
                quantity_entry.delete(0, tk.END)
                quantity_entry.insert(0, value)
            return True
        
        quantity_entry.config(validatecommand=(quantity_entry.register(insert_commas), "%S"))  # Modify the validation command to call insert_commas
        
        # Button to add product
        add_button = tk.Button(add_window, text="Add", command=add_product, bg="green", fg="white", width=10)
        add_button.pack()
        
         
    # View button function    
    def view(self):
        def search_products(keyword):
            def go_back():
                result_window.destroy()
                view_window.deiconify()

            result_window = tk.Toplevel(view_window)
            result_window.title("Search Results")
            result_window.geometry("840x100")
            result_window.resizable(False, False)

            tree = ttk.Treeview(result_window, columns=("ID", "Name", "Price", "Quantity"), show="headings")
            tree.heading("ID", text="ID")
            tree.heading("Name", text="Name")
            tree.heading("Price", text="Price")
            tree.heading("Quantity", text="Quantity")
            
            conn = sqlite3.connect('inventory.db')
            cursor = conn.cursor()

            # Perform search based on the keyword
            cursor.execute("SELECT * FROM products WHERE ID=? OR Name=? OR Price=? OR Quantity=?", (keyword, keyword, keyword, keyword))
            rows = cursor.fetchall()
            if not rows:
                messagebox.showinfo("No Results", "No products found matching the search criteria.")
            else:
                for row in rows:
                    tree.insert("", "end", values=row)

            tree.pack(expand=True, fill="both")

            conn.close()

            back_button = tk.Button(result_window, text="Back to Search", command=go_back)
            back_button.pack(pady=10)

        # Open a new window for viewing products
        view_window = tk.Toplevel(self)
        view_window.geometry("250x250")  # Fixed the typo here
        view_window.title("View Products")
        view_window.resizable(False, False)
        view_window.configure(bd=20, relief=tk.RIDGE)
        
        search_label = tk.Label(view_window, text="Search\n(ID, Name, Price, Quantity):")  # Adjusted the label text
        search_label.pack(pady=10)

        search_entry = tk.Entry(view_window)
        search_entry.pack(pady=5)

        search_button = tk.Button(view_window, text="Search", command=lambda: search_products(search_entry.get()))
        search_button.pack(pady=5)
        
    # Update button function
    def update(self):
        # Open a new window for updating products
        update_window = tk.Toplevel(self)
        update_window.geometry("840x405")
        update_window.title("Update Product")
        update_window.resizable(False, False)
        update_window.configure(bd=20, relief=tk.RIDGE)

        # Function to update product in database
        def update_product():
            # Retrieve data from entry fields
            id_value = id_entry.get()
            name = name_entry.get()
            price = price_entry.get()
            quantity = quantity_entry.get()

            # Update data in the database
            conn = sqlite3.connect('inventory.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE products SET name=?, price=?, quantity=? WHERE id=?", (name, price, quantity, id_value))
            conn.commit()
            conn.close()

            # Refresh the Treeview to display the updated product
            self.Tree()
            # Close the window after updating product
            update_window.destroy()

        # Label and entry for ID
        id_label = tk.Label(update_window, text="ID:")
        id_label.pack()
        id_entry = tk.Entry(update_window)
        id_entry.pack()

        # Label and entry for Name
        name_label = tk.Label(update_window, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(update_window)
        name_entry.pack()

        # Label and entry for Price
        price_label = tk.Label(update_window, text="Price:")
        price_label.pack()
        price_entry = tk.Entry(update_window)
        price_entry.pack()

        # Label and entry for Quantity
        quantity_label = tk.Label(update_window, text="Quantity:")
        quantity_label.pack()
        quantity_entry = tk.Entry(update_window)
        quantity_entry.pack()

        # Button to update product
        update_button = tk.Button(update_window, text="Update", command=update_product, bg="green", fg="white", width=10)
        update_button.pack()

    # Remove button function
    def remove(self):
        # Function to remove product from database
        def remove_product():
            # Retrieve ID from entry field
            id = id_entry.get()
            
            # Remove data from the database
            conn = sqlite3.connect('inventory.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id=?", (id,))
            conn.commit()
            conn.close()
            
            # Refresh the Treeview to reflect the changes
            self.Tree()
            # Close the window after removing product
            remove_window.destroy()
        
        # Open a new window for removing products
        remove_window = tk.Toplevel(self)
        remove_window.geometry("200x100")
        remove_window.title("Remove Product")
        remove_window.resizable(False, False)
        remove_window.configure(bd=20, relief=tk.RIDGE)
        
        # Label and entry for ID
        id_label = tk.Label(remove_window, text="ID:")
        id_label.pack()
        id_entry = tk.Entry(remove_window)
        id_entry.pack()
        
        # Button to remove product
        remove_button = tk.Button(remove_window, text="Remove", command=remove_product, bg="red", fg="white", width=10)
        remove_button.pack()

    def exit_confirmation(self):
        if messagebox.askokcancel("Exit", "Do you really want to exit?"):
            self.destroy()


    # Menu Bar 
    def MenuBar(self):
        menuBar = tk.Menu(self)
        #File
        file_menu = tk.Menu(menuBar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        menuBar.add_cascade(label="File", menu=file_menu)

        #Edit
        edit_menu = tk.Menu(menuBar, tearoff=0)
        edit_menu.add_command(label="Add", command=self.add)
        edit_menu.add_command(label="Remove", command=self.remove)
        edit_menu.add_command(label="View", command=self.view)
        menuBar.add_cascade(label="Update", menu=edit_menu)

        #Help
        Help_menu = tk.Menu(menuBar, tearoff=0)
        Help_menu.add_command(label="About", command=self.show_about)
        menuBar.add_cascade(label="Help", menu=Help_menu)

        #Show Menu in Window
        self.config(menu=menuBar)

    # Open file (database files only)   Dev Note: Experimental, may or may not work
    def open_file(self):
        # Open database file in File Manager
        file_path = filedialog.askopenfilename(filetypes=[("Database files", "*.db")])
        
        # Connect to the selected database file
        if file_path:
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()

            # Check if the 'products' table exists in the database
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
            table_exists = cursor.fetchone()

            if table_exists:
                # Clear the existing Treeview
                self.tree.delete(*self.tree.get_children())
                
                # Retrieve data from the 'products' table and insert it into the Treeview
                cursor.execute("SELECT * FROM products")
                rows = cursor.fetchall()
                for row in rows:
                    self.tree.insert("", "end", values=row)
                
                # Close the database connection
                conn.close()
            else:
                messagebox.showwarning("Table Not Found", "No 'products' table found in the selected database file.")

    # Save file (database files only)   Dev Note: Experimental, may or may not work
    def save_file(self):
        # Save database file settings to File Manager
        file_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("Database files", "*.db")])

        # Copy the current database file to the selected location
        if file_path:
            if os.path.isfile('inventory.db'):
                conn = sqlite3.connect('inventory.db')
                try:
                    conn.backup(file_path)
                    messagebox.showinfo("Save Successful", "Database file saved successfully.")
                except sqlite3.Error as e:
                    messagebox.showerror("Save Error", f"Error saving database file: {str(e)}")
                finally:
                    conn.close()
            else:
                messagebox.showwarning("Database Not Found", "No database file found to save.")

    #Help Menu
    def show_about(self):
        messagebox.showinfo("About", "Inventory Management System v1.0\n\nAuthor: Sherwin P. Limosnero")





if __name__ == "__main__":
    app = Gui()
    app.mainloop()
