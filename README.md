# Inventory-Management-System
Inventory Management System using sqlite3 and tkinter module

![image](https://github.com/owenlim225/Inventory-Management-System/assets/87555304/83b82a6d-7ccc-42e8-ae7e-d8a6470bbe29)


You are assigned to develop a simple inventory management system using SQLite and Python for a small retail store. The system should allow users to perform basic inventory management tasks, including adding new products, viewing existing products, updating product information, and removing products from the inventory.

Design and implement a Python script to accomplish the following tasks:

Create a SQLite database named "inventory.db" if it does not already exist.
Create a table named "products" with the following columns:
ID (INTEGER, PRIMARY KEY)
Name (TEXT)
Price (REAL)
Quantity (INTEGER)
Implement a menu-driven interface that allows users to:
Add a new product by entering its name, price, and quantity.
View all existing products stored in the inventory, including their ID, name, price, and quantity.
Update the details of an existing product by searching for its ID and providing new information.
Remove a product from the inventory by searching for its ID and confirming removal.
Exit the application.
Ensure error handling for invalid inputs and proper closing of the database connection.
