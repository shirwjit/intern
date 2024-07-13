
# SIMPLE CALCULATOR
import tkinter as tk

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")

        self.expression = ""
        self.text_input = tk.StringVar()

        # Setting a light gray background for the calculator
        self.root.configure(bg='light gray')

        # Creating the display for the calculator
        self.display = tk.Entry(root, font=('arial', 20, 'bold'), textvariable=self.text_input, bd=30, insertwidth=4, width=14, borderwidth=4)
        self.display.grid(row=0, column=0, columnspan=4)

        # Defining colors for buttons
        button_colors = {
            'purple': {'bg': '#9c27b0', 'fg': 'white'},
            'blue': {'bg': '#2196f3', 'fg': 'white'},
            'green': {'bg': '#4caf50', 'fg': 'white'},
            'orange': {'bg': '#ff9800', 'fg': 'black'}
        }

        # Creating buttons with different colors
        self.create_buttons(button_colors)

    def create_buttons(self, button_colors):
        buttons = [
            ('7', 'purple'), ('8', 'purple'), ('9', 'purple'), ('/', 'orange'),
            ('4', 'blue'), ('5', 'blue'), ('6', 'blue'), ('*', 'orange'),
            ('1', 'green'), ('2', 'green'), ('3', 'green'), ('-', 'orange'),
            ('0', 'purple'), ('clr', 'purple'), ('=', 'purple'), ('+', 'orange')
        ]

        row_val = 1
        col_val = 0

        for label, color_key in buttons:
            action = lambda x=label: self.click_event(x)
            tk.Button(self.root, text=label, padx=20, pady=20, bd=8,
                      fg=button_colors[color_key]['fg'], bg=button_colors[color_key]['bg'],
                      font=('arial', 20, 'bold'), command=action).grid(row=row_val, column=col_val)

            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

    def click_event(self, key):
        if key == '=':
            try:
                self.expression = str(eval(self.expression))
            except:
                self.expression = "Error"
            self.text_input.set(self.expression)
        elif key == 'clr':
            self.expression = ""
            self.text_input.set("")
        else:
            self.expression += str(key)
            self.text_input.set(self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
