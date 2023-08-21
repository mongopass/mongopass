import tkinter as tk
from tkinter import messagebox
import pymongo
import bcrypt
from decouple import config

# Setup MongoDB connection
MONGODB_URI = config('MONGODB_URI')
client = pymongo.MongoClient(MONGODB_URI)
db = client.passwords_db
users = db.users

def register():
    username = entry_username.get()
    password = entry_password.get()

    # Check if username already exists
    user = users.find_one({"username": username})
    if user:
        messagebox.showerror("Error", "Username already exists!")
        return
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users.insert_one({"username": username, "password": hashed})
    messagebox.showinfo("Success", "Registration successful!")

def check_password():
    username = entry_username.get()
    password = entry_password.get()

    user = users.find_one({"username": username})
    if not user:
        messagebox.showerror("Error", "User not found!")
        return
    
    if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        messagebox.showinfo("Success", "Password is correct!")
    else:
        messagebox.showerror("Error", "Password is incorrect!")

# Create the main window
app = tk.Tk()
app.title("MongoDB Password App")

# Add labels and entry fields
tk.Label(app, text="Username").pack(pady=10)
entry_username = tk.Entry(app)
entry_username.pack(pady=5)

tk.Label(app, text="Password").pack(pady=10)
entry_password = tk.Entry(app, show="*")
entry_password.pack(pady=5)

# Add buttons
btn_register = tk.Button(app, text="Register", command=register)
btn_register.pack(pady=10)

btn_check = tk.Button(app, text="Check Password", command=check_password)
btn_check.pack(pady=10)

# Start the GUI loop
app.mainloop()
