# Importing required modules
import tkinter as tk
from tkinter import Entry, Button

# Define the CalculatorApp class
class CalculatorApp:
    def __init__(self, root):
        self.root = root
        #self.root.title("Simple Calculator")  # Set title for Tk window
        self.operator = ""
        self.text_Input = tk.StringVar()
        self.create_widgets()

    def btnClick(self, numbers):
        self.operator = self.operator + str(numbers)
        self.text_Input.set(self.operator)

    def btnClear(self):
        self.operator = ""
        self.text_Input.set("")

    def btnEquals(self):
        try:
            result = str(eval(self.operator))
            self.text_Input.set(result)
            self.operator = ""
        except Exception as e:
            self.text_Input.set("Error")
            self.operator = ""

    def create_button(self, text, row, col, command=None):
        button = Button(self.root, padx=29, pady=5, bd=1, fg="black", font=('Calibri', 16, 'bold'), width=1, text=text,
                        bg="#ffffff", command=command, relief=tk.RIDGE)
        button.grid(row=row, column=col)
        return button

    def create_widgets(self):
        # Entry widget for input
        txtDisplay = Entry(self.root, width=20, bg="white", bd=8, font=('Calibri', 20),
                           justify=tk.RIGHT, textvariable=self.text_Input, relief=tk.FLAT)
        txtDisplay.grid(row=0, column=0, columnspan=4, pady=1)
        txtDisplay.insert(0, "0")

        # Create calculator buttons
        buttons = [
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('+', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('*', 4, 3),
            ('C', 5, 0), ('0', 5, 1), ('=', 5, 2), ('/', 5, 3)
        ]

        for (text, row, col) in buttons:
            if text == 'C':
                self.create_button(text, row, col, command=self.btnClear)
            elif text == '=':
                self.create_button(text, row, col, command=self.btnEquals)
            else:
                self.create_button(text, row, col, command=lambda t=text: self.btnClick(t))

# Main program
if __name__ == "__main__":
    root = tk.Tk()  # Create the Tk root object
    app = CalculatorApp(root)  # Pass the root object to CalculatorApp constructor
    root.mainloop()  # Start the main event loop
