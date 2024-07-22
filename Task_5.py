import tkinter as tk
from tkinter import messagebox, ttk
import requests

# Function to fetch exchange rates
def get_exchange_rate(base_currency, target_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rate = data['rates'].get(target_currency, None)
        return rate
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch exchange rates: {e}")
        return None

# Function to convert currency
def convert_currency(amount, rate):
    return amount * rate

# Function to handle conversion
def convert():
    try:
        amount = float(entry_amount.get())
        target_currency = dropdown_currency.get()
        rate = get_exchange_rate('USD', target_currency)
        if rate is not None:
            converted_amount = convert_currency(amount, rate)
            label_result.config(text=f"Converted Amount: {converted_amount:.2f} {target_currency}")
        else:
            messagebox.showerror("Error", "Failed to fetch exchange rate")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number")

# Function to refresh exchange rates (optional, for future enhancements)
def refresh_rates():
    # Logic to refresh exchange rates can be added here
    pass

# Set up the main application window
root = tk.Tk()
root.title("USD Currency Converter")
root.geometry("400x200")
root.resizable(False, False)

# Styling
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))
style.configure("TEntry", font=("Arial", 12))

frame = ttk.Frame(root, padding="10 10 10 10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Widgets
ttk.Label(frame, text="Amount in USD:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
entry_amount = ttk.Entry(frame, width=15)
entry_amount.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(frame, text="Convert to:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
currencies = ["EUR", "GBP", "JPY", "AUD", "CAD", "INR", "CHF", "CNY"]
dropdown_currency = ttk.Combobox(frame, values=currencies, state="readonly")
dropdown_currency.set(currencies[0])
dropdown_currency.grid(row=1, column=1, padx=10, pady=5)

btn_convert = ttk.Button(frame, text="Convert", command=convert)
btn_convert.grid(row=2, column=0, columnspan=2, pady=10)

label_result = ttk.Label(frame, text="Converted Amount: ")
label_result.grid(row=3, column=0, columnspan=2, pady=5)

# Run the main event loop
root.mainloop()

