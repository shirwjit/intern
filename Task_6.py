import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Database setup
def create_database():
    conn = sqlite3.connect('billing_software.db')
    cursor = conn.cursor()

    # Drop the Products table if it exists and recreate it
    cursor.execute('DROP TABLE IF EXISTS Products')
    cursor.execute('''
    CREATE TABLE Products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        customer_address TEXT,
        phone_number TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        total_amount REAL,
        transaction_date TEXT,
        FOREIGN KEY (customer_id) REFERENCES Customers (customer_id),
        FOREIGN KEY (product_id) REFERENCES Products (product_id)
    )
    ''')

    conn.commit()
    conn.close()

# Functions to interact with the database
def add_product(name, price, stock):
    conn = sqlite3.connect('billing_software.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Products (product_name, price, stock)
    VALUES (?, ?, ?)
    ''', (name, price, stock))
    conn.commit()
    conn.close()

def add_customer(name, address, phone):
    conn = sqlite3.connect('billing_software.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Customers (customer_name, customer_address, phone_number)
    VALUES (?, ?, ?)
    ''', (name, address, phone))
    conn.commit()
    conn.close()

def add_transaction(customer_id, product_id, quantity, total_amount):
    from datetime import datetime
    conn = sqlite3.connect('billing_software.db')
    cursor = conn.cursor()

    # Update stock
    cursor.execute('''
    UPDATE Products
    SET stock = stock - ?
    WHERE product_id = ?
    ''', (quantity, product_id))

    # Add transaction
    cursor.execute('''
    INSERT INTO Transactions (customer_id, product_id, quantity, total_amount, transaction_date)
    VALUES (?, ?, ?, ?, ?)
    ''', (customer_id, product_id, quantity, total_amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()

# GUI setup
def setup_gui():
    def add_product_action():
        name = product_name_entry.get()
        price = float(price_entry.get())
        stock = int(stock_entry.get())
        add_product(name, price, stock)
        messagebox.showinfo("Success", "Product added successfully!")
    def add_customer_action():
        name = customer_name_entry.get()
        address = address_entry.get()
        phone = phone_entry.get()
        add_customer(name, address, phone)
        messagebox.showinfo("Success", "Customer added successfully!")
    def generate_invoice_action():
        customer_id = int(invoice_customer_id_entry.get())
        product_id = int(invoice_product_id_entry.get())
        quantity = int(invoice_quantity_entry.get())
        conn = sqlite3.connect('billing_software.db')
        cursor = conn.cursor()
        # Check product stock
        cursor.execute('SELECT price, stock FROM Products WHERE product_id = ?', (product_id,))
        result = cursor.fetchone()
        if result:
            price, stock = result
            if quantity <= stock:
                total_amount = price * quantity
                add_transaction(customer_id, product_id, quantity, total_amount)
                messagebox.showinfo("Success", f"Invoice generated. Total Amount: {total_amount:.2f}")
            else:
                messagebox.showerror("Error", "Insufficient stock.")
        else:
            messagebox.showerror("Error", "Product ID not found.")

        conn.close()
    root = tk.Tk()
    root.title("Billing Software")

    # Create Tab Control
    tab_control = ttk.Notebook(root)

    # Create tabs
    product_tab = ttk.Frame(tab_control)
    customer_tab = ttk.Frame(tab_control)
    invoice_tab = ttk.Frame(tab_control)

    tab_control.add(product_tab, text='Product Entry')
    tab_control.add(customer_tab, text='Customer Details')
    tab_control.add(invoice_tab, text='Generate Invoice')

    tab_control.pack(expand=1, fill='both')

    # Product Entry Form
    tk.Label(product_tab, text='Product Name:').grid(row=0, column=0, padx=10, pady=10)
    product_name_entry = tk.Entry(product_tab)
    product_name_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(product_tab, text='Price:').grid(row=1, column=0, padx=10, pady=10)
    price_entry = tk.Entry(product_tab)
    price_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(product_tab, text='Stock:').grid(row=2, column=0, padx=10, pady=10)
    stock_entry = tk.Entry(product_tab)
    stock_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Button(product_tab, text='Add Product', command=add_product_action).grid(row=3, column=1, padx=10, pady=10)

    # Customer Entry Form
    tk.Label(customer_tab, text='Customer Name:').grid(row=0, column=0, padx=10, pady=10)
    customer_name_entry = tk.Entry(customer_tab)
    customer_name_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(customer_tab, text='Address:').grid(row=1, column=0, padx=10, pady=10)
    address_entry = tk.Entry(customer_tab)
    address_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(customer_tab, text='Phone Number:').grid(row=2, column=0, padx=10, pady=10)
    phone_entry = tk.Entry(customer_tab)
    phone_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Button(customer_tab, text='Add Customer', command=add_customer_action).grid(row=3, column=1, padx=10, pady=10)

    # Invoice Generation Form
    tk.Label(invoice_tab, text='Customer ID:').grid(row=0, column=0, padx=10, pady=10)
    invoice_customer_id_entry = tk.Entry(invoice_tab)
    invoice_customer_id_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(invoice_tab, text='Product ID:').grid(row=1, column=0, padx=10, pady=10)
    invoice_product_id_entry = tk.Entry(invoice_tab)
    invoice_product_id_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(invoice_tab, text='Quantity:').grid(row=2, column=0, padx=10, pady=10)
    invoice_quantity_entry = tk.Entry(invoice_tab)
    invoice_quantity_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Button(invoice_tab, text='Generate Invoice', command=generate_invoice_action).grid(row=3, column=1, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_database()
    setup_gui()
