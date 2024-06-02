import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re

# Create and connect to the SQLite database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Create the students table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        class TEXT NOT NULL,
        stream TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        father_name TEXT NOT NULL,
        mother_name TEXT NOT NULL,
        parent_phone TEXT NOT NULL,
        permanent_address TEXT NOT NULL,
        correspondence_address TEXT NOT NULL
    )
''')
conn.commit()

# Function to validate phone numbers
def validate_phone_number(phone_number):
    return bool(re.fullmatch(r'\+\d{12}', phone_number))

def validate_phone_entry(input):
    return re.fullmatch(r'\+?\d{0,12}', input) is not None

# Function to insert data into the database
def submit_data():
    name = name_entry.get()
    class_ = class_entry.get()
    stream = stream_option.get()
    phone_number = phone_entry.get()
    father_name = father_name_entry.get()
    mother_name = mother_name_entry.get()
    parent_phone = parent_phone_entry.get()
    permanent_address = permanent_address_entry.get()
    correspondence_address = correspondence_address_entry.get()

    if (name and class_ and stream and phone_number and father_name and mother_name and 
        parent_phone and permanent_address and correspondence_address):
        
        if not validate_phone_number(phone_number) or not validate_phone_number(parent_phone):
            messagebox.showwarning("Input Error", "Phone numbers must start with a '+' and be followed by 12 digits.")
            return

        cursor.execute('''
            INSERT INTO students (name, class, stream, phone_number, father_name, mother_name, 
            parent_phone, permanent_address, correspondence_address) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, class_, stream, phone_number, father_name, mother_name, parent_phone,
              permanent_address, correspondence_address))
        conn.commit()
        messagebox.showinfo("Success", "Data inserted successfully")
        clear_fields()
    else:
        messagebox.showwarning("Input Error", "All fields are required")

def clear_fields():
    name_entry.delete(0, tk.END)
    class_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    father_name_entry.delete(0, tk.END)
    mother_name_entry.delete(0, tk.END)
    parent_phone_entry.delete(0, tk.END)
    permanent_address_entry.delete(0, tk.END)
    correspondence_address_entry.delete(0, tk.END)

def search_data():
    parameter = lookup_param.get()
    search_term = search_entry.get()

    if search_term:
        query = ""
        if parameter == "Name":
            query = "SELECT * FROM students WHERE name LIKE ?"
        elif parameter == "ID":
            query = "SELECT * FROM students WHERE id = ?"
        elif parameter == "Class":
            query = "SELECT * FROM students WHERE class LIKE ?"
        elif parameter == "Stream":
            query = "SELECT * FROM students WHERE stream LIKE ?"
        
        cursor.execute(query, (f"%{search_term}%",))
        results = cursor.fetchall()

        if results:
            result_text = "\n".join([f"ID: {row[0]}, Name: {row[1]}, Class: {row[2]}, Stream: {row[3]}, Phone: {row[4]}" for row in results])
            result_label.config(text=result_text)
        else:
            result_label.config(text="No results found")
    else:
        messagebox.showwarning("Input Error", "Search term is required")

# Create the main window
root = tk.Tk()
root.title("Student Form")

# Add some styling
style = ttk.Style()
style.configure('TLabel', font=('Arial', 12))
style.configure('TButton', font=('Arial', 12))
style.configure('TEntry', font=('Arial', 12))

# Create and place the labels and entries for the form
tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=5)
name_entry = ttk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Class").grid(row=1, column=0, padx=10, pady=5)
class_entry = ttk.Entry(root)
class_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Stream").grid(row=2, column=0, padx=10, pady=5)
stream_options = ["Medical", "Non-Medical", "Commerce", "Arts"]
stream_option = tk.StringVar(root)
stream_option.set(stream_options[0])  # Set default value
stream_menu = ttk.OptionMenu(root, stream_option, *stream_options)
stream_menu.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Phone Number").grid(row=3, column=0, padx=10, pady=5)
phone_entry = ttk.Entry(root)
phone_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Father's Name").grid(row=4, column=0, padx=10, pady=5)
father_name_entry = ttk.Entry(root)
father_name_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Mother's Name").grid(row=5, column=0, padx=10, pady=5)
mother_name_entry = ttk.Entry(root)
mother_name_entry.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Parent's Phone").grid(row=6, column=0, padx=10, pady=5)
parent_phone_entry = ttk.Entry(root)
parent_phone_entry.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Permanent Address").grid(row=7, column=0, padx=10, pady=5)
permanent_address_entry = ttk.Entry(root)
permanent_address_entry.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="Correspondence Address").grid(row=8, column=0, padx=10, pady=5)
correspondence_address_entry = ttk.Entry(root)
correspondence_address_entry.grid(row=8, column=1, padx=10, pady=5)

# Register the validation function
validate_command = root.register(validate_phone_entry)

# Apply the validation function to phone entry fields
phone_entry.config(validate="key", validatecommand=(validate_command, "%P"))
parent_phone_entry.config(validate="key", validatecommand=(validate_command, "%P"))

# Create and place the submit button
submit_button = ttk.Button(root, text="Submit", command=submit_data)
submit_button.grid(row=9, column=0, columnspan=2, pady=20)

# Create and place the lookup frame
lookup_frame = ttk.Frame(root)
lookup_frame.grid(row=10, column=0, columnspan=2, pady=20)

lookup_param = tk.StringVar(root)

lookup_menu = ttk.OptionMenu(lookup_frame, lookup_param, "Name", "Class", "Stream")
lookup_menu.pack(side="left", padx=5)

search_entry = ttk.Entry(lookup_frame)
search_entry.pack(side="left", padx=5)

search_button = ttk.Button(lookup_frame, text="Search", command=search_data)
search_button.pack(side="left", padx=5)

# Create and place the result label
result_label = tk.Label(root, text="")
result_label.grid(row=11, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()

# Close the database connection when the application is closed
conn.close()
