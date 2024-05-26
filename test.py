import tkinter as tk
from tkinter import messagebox
import sqlite3
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

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
        phone_number TEXT NOT NULL
    )
''')
conn.commit()

# Function to insert data into the database
def submit_data():
    name = name_entry.get()
    class_ = class_entry.get()
    stream = stream_entry.get()
    phone_number = phone_entry.get()

    if name and class_ and stream and phone_number:
        cursor.execute('''
            INSERT INTO students (name, class, stream, phone_number) 
            VALUES (?, ?, ?, ?)
        ''', (name, class_, stream, phone_number))
        conn.commit()
        messagebox.showinfo("Success", "Data inserted successfully")
        name_entry.delete(0, tk.END)
        class_entry.delete(0, tk.END)
        stream_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "All fields are required")

# Function to search data in the database
def search_data():
    search_term = search_entry.get()
    search_by = search_option.get()

    if search_term:
        query = ""
        if search_by == "Name":
            query = "SELECT * FROM students WHERE name LIKE ?"
        elif search_by == "ID":
            query = "SELECT * FROM students WHERE id = ?"
        elif search_by == "Class":
            query = "SELECT * FROM students WHERE class LIKE ?"
        
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

# Create and place the labels and entries for the form
tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=10)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Class").grid(row=1, column=0, padx=10, pady=10)
class_entry = tk.Entry(root)
class_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Stream").grid(row=2, column=0, padx=10, pady=10)
stream_entry = tk.Entry(root)
stream_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Phone Number").grid(row=3, column=0, padx=10, pady=10)
phone_entry = tk.Entry(root)
phone_entry.grid(row=3, column=1, padx=10, pady=10)

# Create and place the submit button
submit_button = tk.Button(root, text="Submit", command=submit_data)
submit_button.grid(row=4, column=0, columnspan=2, pady=20)

# Create and place the search entry and options
tk.Label(root, text="Search By").grid(row=5, column=0, padx=10, pady=10)
search_option = tk.StringVar()
search_option.set("Name")
search_menu = tk.OptionMenu(root, search_option, "Name", "ID", "Class")
search_menu.grid(row=5, column=1, padx=10, pady=10)

tk.Label(root, text="Search Term").grid(row=6, column=0, padx=10, pady=10)
search_entry = tk.Entry(root)
search_entry.grid(row=6, column=1, padx=10, pady=10)

search_button = tk.Button(root, text="Search", command=search_data)
search_button.grid(row=7, column=0, columnspan=2, pady=20)

# Create a label to display search results
result_label = tk.Label(root, text="", justify=tk.LEFT)
result_label.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()

# Close the database connection when the application is closed
conn.close()
