import random
import time
import datetime
import os
import re
import tempfile
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import tkinter.messagebox
from calculator import CalculatorApp

class PlaylandApp:
    def __init__(self, root):
        # Initialize the Playland application with the provided root window.
        self.root = root
        self.setup_gui()

    def setup_gui(self):
        # Define global font styles and background color.
        self.GLOBAL_FONT = ('Calibri', 13, 'bold')
        self.GLOBAL_FONT_LIGHT = ('Calibri', 12)
        self.BACKGROUND_COLOR_RGB = ('#DDDDDD')

        # List to store PhotoImage objects for attractions' images.
        self.image_list = []

        # List of attractions available in the Playland.
        self.attractions = [
            "Ball Pit", "Bondville Fair", "Bug Whirled", "Bumper Cars",
            "Climbing Wall", "Cup", "Dizzy Drop", "Haunted Mansion",
            "Hellevator", "Hells Gate", "Merry Go Round", "Pirate",
            "Roller Coaster", "V Merry Go Round", "W Roller Coaster", "Circus City"
        ]

        # File paths for respective attraction images.
        self.image_paths = [
            'ball pit.gif', 'bondville-fair.gif', 'Bug Whirled.gif', 'Bumper Cars.gif',
            'Climbing Wall.gif', 'cup .gif', 'Dizzy Drop.gif', 'Haunted Mansion .gif',
            'Hellevator.gif', 'Hells Gate.gif', 'Merry-Go-Round.gif', 'Pirate.gif',
            'Roller Coaster.gif', 'V merry go round.gif', 'Wooden Roller Coaster.gif', 'CIRCUS-CITY-PLAYLAND.gif'
        ]

        # Prices of the attractions.
        self.prices = ["$10", "$21", "$17", "$11", "$9", "$26", "$16", "$15", "$28", "$19", "$20", "$20", "$30", "$18", "$25", "$14"]

        # Set the initial size and properties of the root window.
        self.root.geometry("1230x670")
        self.root.resizable(True, True)  # Allowing the window to be resizable
        self.root.title("Vancouver Playland")  # Title of the application window
        self.root.configure(background=self.BACKGROUND_COLOR_RGB)  # Setting background color

        # Frames for receipt, calculator, menu, etc.
        self.receipt_cal_frame = Frame(self.root, bg=self.BACKGROUND_COLOR_RGB, bd=2, relief=FLAT)
        self.receipt_cal_frame.pack(side=RIGHT)

        # Calculator frame and its initialization
        self.calculator_frame = Frame(self.receipt_cal_frame, bg=self.BACKGROUND_COLOR_RGB, bd=0, relief=FLAT)
        self.calculator_frame.pack(side=TOP, padx=0, pady=0)
        self.calculator_app = CalculatorApp(self.calculator_frame)

        # Frames for buttons, receipt, and menu
        self.buttons_frame = Frame(self.receipt_cal_frame, bg=self.BACKGROUND_COLOR_RGB, bd=0, relief=FLAT)
        self.buttons_frame.pack(side=BOTTOM)
        self.receipt_frame = Frame(self.receipt_cal_frame, bg=self.BACKGROUND_COLOR_RGB, bd=0, relief=FLAT)
        self.receipt_frame.pack(side=BOTTOM, fill=BOTH, expand=True, padx=0, pady=0)
        self.menu_frame = Frame(self.root, bg=self.BACKGROUND_COLOR_RGB, bd=0, relief=FLAT)
        self.menu_frame.pack(side=LEFT)

        # Label for the title of the application
        self.title_label = ttk.Label(self.menu_frame, text='Vancouver Playland', style="TLabel",
                                     background=self.BACKGROUND_COLOR_RGB, font=('Calibri', 40, 'bold'))
        self.title_label.pack(side=TOP)

        # Frame for cost information
        self.cost_frame = Frame(self.menu_frame, bg=self.BACKGROUND_COLOR_RGB, bd=0)
        self.cost_frame.pack(side=BOTTOM)

        # Frame for items
        self.ITEMS_FRAME = Frame(self.menu_frame, bg=self.BACKGROUND_COLOR_RGB, bd=0)
        self.ITEMS_FRAME.pack(side=TOP)

        # Variables for cost, receipt, etc.
        self.COST_OF_ITEMS = StringVar()
        self.COST_OF_ITEMS1 = StringVar()
        self.SERVICE_CHARGE = StringVar()
        self.PAID_TAX = StringVar()
        self.SUBTOTAL = StringVar()
        self.TOTAL_COST = StringVar()
        self.RECEIPT_TEXT = StringVar()

        # Lists and dictionaries for checkbox and entry widgets
        self.chk_var = []
        self.entry_var = []
        self.entry_widgets = {}

        # Additional variables for data, receipt reference, item prices, and discount
        self.DATA_OF_ORDER = StringVar(value=time.strftime("%d/%m/%Y"))
        self.RECEIPT_REF = StringVar()
        self.ITEM_PRICES = StringVar()
        self.DISCOUNT = StringVar()

        # Variable for text input and operator
        self.TEXT_INPUT = StringVar()
        self.operator = ""

        # Set the initial date format for the data of the order
        self.DATA_OF_ORDER = StringVar(value=time.strftime("%d/%m/%Y"))

        # Initialize variables for checkbox and entry values
        for _ in range(16):
            self.chk_var.append(IntVar())
            self.entry_var.append(StringVar(value="0"))

        # Create checkboxes, entry widgets, labels, and load images for attractions
        for col in range(4):
            for row in range(4):
                index = row + col * 4

                # Label for attraction name
                ttk.Label(self.ITEMS_FRAME, font=self.GLOBAL_FONT, text=self.attractions[index],
                          background=self.BACKGROUND_COLOR_RGB, foreground="Black").grid(row=row * 3, column=col * 3 + 1, sticky='w', pady=(10, 0))

                # Checkbox for attraction selection
                Checkbutton(self.ITEMS_FRAME, variable=self.chk_var[index], onvalue=1, offvalue=0, font=self.GLOBAL_FONT_LIGHT,
                            bg=self.BACKGROUND_COLOR_RGB, command=lambda idx=index: self.check_attraction(idx)).grid(row=row * 3 + 1, column=col * 3,
                                                                                                                   sticky='ne', padx=(20, 0))

                # Entry for quantity
                txt_entry = Entry(self.ITEMS_FRAME, font=self.GLOBAL_FONT, bd=2, width=3, justify=LEFT, state=DISABLED,
                                  textvariable=self.entry_var[index])
                txt_entry.grid(row=row * 3 + 1, column=col * 3 + 2, sticky='nw')
                self.entry_widgets[f"ITEMS{index}"] = txt_entry

                # Label for quantity
                ttk.Label(self.ITEMS_FRAME, font=self.GLOBAL_FONT_LIGHT, text="Qty", background=self.BACKGROUND_COLOR_RGB, foreground="Black").grid(
                    row=row * 3 + 1, column=col * 3 + 2, sticky='w')

                # Label for price
                ttk.Label(self.ITEMS_FRAME, font=self.GLOBAL_FONT_LIGHT, text=self.prices[index],
                          background=self.BACKGROUND_COLOR_RGB, foreground="Black").grid(row=row * 3 + 1, column=col * 3 + 2, sticky='sw')

                # Load images and display
                img = self.load_image(self.image_paths[index])
                self.image_list.append(img)  # Store reference to PhotoImage object
                ttk.Label(self.ITEMS_FRAME, image=img).grid(row=row * 3 + 1, column=col * 3 + 1, sticky='w')

        # Labels and entry widgets for cost information
        ttk.Label(self.cost_frame, font=self.GLOBAL_FONT, text="Purchased Items\t      ",
                  background=self.BACKGROUND_COLOR_RGB, foreground="Black").grid(row=0, column=0, sticky='w', pady=(20, 0))
        Entry(self.cost_frame, font=self.GLOBAL_FONT, insertwidth=1, background="white", bd=2, justify=RIGHT,
              textvariable=self.ITEM_PRICES).grid(row=0, column=1, pady=(20, 0))

        ttk.Label(self.cost_frame, font=self.GLOBAL_FONT, text="Discounts      ",
                  background=self.BACKGROUND_COLOR_RGB, foreground="Black").grid(row=0, column=3, sticky='w', pady=10)
        Entry(self.cost_frame, font=('Calibri', 14, 'bold'), insertwidth=1, background="white", bd=2, justify=RIGHT,
              textvariable=self.DISCOUNT).grid(row=0, column=4)

        ttk.Label(self.cost_frame, font=self.GLOBAL_FONT, text="Taxes      ",
                  background=self.BACKGROUND_COLOR_RGB, foreground="Black").grid(row=2, column=0, sticky='w', pady=10)
        Entry(self.cost_frame, font=self.GLOBAL_FONT, insertwidth=1, background="white", bd=2, justify=RIGHT,
              textvariable=self.PAID_TAX).grid(row=2, column=1)

        ttk.Label(self.cost_frame, font=self.GLOBAL_FONT, text="Total Cost      ",
                  background=self.BACKGROUND_COLOR_RGB, foreground="Black").grid(row=2, column=3, sticky='w', pady=10)
        Entry(self.cost_frame, font=self.GLOBAL_FONT, insertwidth=1, background="white", bd=2, justify=RIGHT,
              textvariable=self.TOTAL_COST).grid(row=2, column=4)

        # Text widget for receipt
        self.RECEIPT_TEXT = Text(self.receipt_frame, width=37, height=20, bg="white", bd=1, font=('Calibri', 12), relief=RIDGE)
        self.RECEIPT_TEXT.grid(row=0, column=0)

        # Buttons for various actions
        Button(self.buttons_frame, padx=5, pady=1, bd=1, fg="black", font=self.GLOBAL_FONT,
               width=5, height=2, text="Total", bg="#4CAF50", command=self.calculate_item_cost).grid(row=0, column=0)

        Button(self.buttons_frame, padx=7, pady=1, bd=1, fg="black", font=self.GLOBAL_FONT,
               width=5, height=2, text="Receipt", bg="#607D8B", command=self.generate_receipt).grid(row=0, column=1)

        Button(self.buttons_frame, padx=5, pady=1, bd=1, fg="black", font=self.GLOBAL_FONT,
               width=5, height=2, text="Reset", bg="#9E9E9E", command=self.reset_values).grid(row=0, column=3)

        Button(self.buttons_frame, padx=2, pady=1, bd=1, fg="black", font=self.GLOBAL_FONT,
               width=5, height=2, text="Exit", bg="#F44336", command=self.exit_program).grid(row=0, column=4)

        Button(self.buttons_frame, padx=4, pady=1, bd=1, fg="white", font=self.GLOBAL_FONT,
               width=5, height=2, text="Print", bg="#616161", command=self.print_receipt).grid(row=0, column=2)

    def exit_program(self):
        # Display confirmation message before exiting
        confirm_exit = tkinter.messagebox.askyesno("Exit Restaurant system", "Confirm if you want to exit")
        if confirm_exit:
            self.root.destroy()

    def print_receipt(self):
        # Print the receipt file if available, handle errors if any
        try:
            os.startfile("Receipt.txt", "print")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while printing the receipt: {str(e)}")

    def reset_values(self):
        # Reset all values and entry widgets to their initial state
        for var in self.chk_var:
            var.set(0)

        for index in range(16):
            self.entry_widgets[f"ITEMS{index}"].configure(state=NORMAL)
            self.entry_widgets[f"ITEMS{index}"].delete(0, END)
            self.entry_widgets[f"ITEMS{index}"].insert(0, "0")
            self.entry_widgets[f"ITEMS{index}"].configure(state=DISABLED)

        self.RECEIPT_TEXT.delete("1.0", END)
        self.DATA_OF_ORDER.set("")
        self.PAID_TAX.set("")
        self.SUBTOTAL.set("")
        self.TOTAL_COST.set("")
        self.ITEM_PRICES.set("")
        self.DISCOUNT.set("")

    def handle_check_button(self, index, txt_entry):
        # Handle the check button action
        if index.get() == 1:
            txt_entry.configure(state=NORMAL)
            txt_entry.focus()
            txt_entry.delete(0, END)
        else:
            self.entry_widgets[f"ITEMS{index}"].set("0")
            txt_entry.configure(state=DISABLED)

    def calculate_item_cost(self):
        # Calculate the total cost of items and update variables accordingly
        try:
            ITEM_PRICES_total = sum(int(self.entry_var[i].get()) * int(self.prices[i].replace('$', '')) for i in range(16))
            DISCOUNT_amount = ITEM_PRICES_total * 0.009
            tax_amount = ITEM_PRICES_total * 0.14
            total_amount = ITEM_PRICES_total + tax_amount - DISCOUNT_amount

            # Update the ITEM_PRICES, DISCOUNT, PAID_TAX, and TOTAL_COST variables
            self.ITEM_PRICES.set(f"${ITEM_PRICES_total:.2f}")
            self.DISCOUNT.set(f"${DISCOUNT_amount:.2f}")
            self.PAID_TAX.set(f"${tax_amount:.2f}")
            self.TOTAL_COST.set(f"${total_amount:.2f}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while calculating item cost: {str(e)}")

    def generate_receipt(self):
        # Generate and write the receipt data to the file, handle errors if any
        try:
            with open("Receipt.txt", "w") as f:
                self.RECEIPT_TEXT.delete("1.0", END)
                ref_number = random.randint(1000, 2000)
                RECEIPT_REF_str = f"BILL Number: {ref_number}"
                self.RECEIPT_REF.set(RECEIPT_REF_str)

                # Write receipt header to the file and display it in the text widget
                f.write(f'Receipt Ref:\t\t{RECEIPT_REF_str}\t\t{self.DATA_OF_ORDER.get()}\n\n')
                self.RECEIPT_TEXT.insert(END, f'Receipt Ref:\t\t{RECEIPT_REF_str}\n\t\t{self.DATA_OF_ORDER.get()}\n\n')
                self.RECEIPT_TEXT.insert(END, 'Items\t\tNumber of Tickets\n\n')

                # Write item details to the file and display them in the text widget
                for item, qty in zip(self.attractions, self.entry_var):
                    item_str = f"{item}\t\t\t{qty.get()}\n"
                    self.RECEIPT_TEXT.insert(END, item_str)
                    f.write(item_str)

                # Write receipt data (cost, discount, tax, total cost) to the file and display it in the text widget
                receipt_data = [
                    ('Purchased Items', self.ITEM_PRICES),
                    ('DISCOUNT', self.DISCOUNT),
                    ('Tax', self.PAID_TAX),
                    ('Total Cost', self.TOTAL_COST)
                ]

                for label, var in receipt_data:
                    label_str = f'{label} : \t\t{var.get()}\n'
                    self.RECEIPT_TEXT.insert(END, label_str)
                    f.write(label_str)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the receipt: {str(e)}")

    def check_attraction(self, index):
        # Call the handle_check_button function to handle attraction selection
        self.handle_check_button(self.chk_var[index], self.entry_widgets[f"ITEMS{index}"])

    def load_image(self, file_path):
        # Specify the directory where your images are stored
        image_directory = "images"
        # Join the directory path with the file name
        full_path = os.path.join(image_directory, file_path)
        # Return the PhotoImage object created from the specified image file
        return PhotoImage(file=full_path)

# Create the root window and initialize the PlaylandApp
root = Tk()
app = PlaylandApp(root)
# Start the main event loop
root.mainloop()