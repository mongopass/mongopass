import tkinter as tk
from tkinter import messagebox
import pymongo
import bcrypt
from decouple import config
from urllib.parse import urlparse

# Setup MongoDB connection
MONGODB_URI = config('MONGODB_URI')
client = pymongo.MongoClient(MONGODB_URI)
db = client.passwords_db
app_users = db.app_users
passwords = db.passwords

current_user_id = None

def register():
    global current_user_id

    username = entry_username.get()
    password = entry_password.get()

    user = app_users.find_one({"username": username})
    if user:
        messagebox.showerror("Error", "Username already exists!")
        return
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    inserted = app_users.insert_one({"username": username, "password": hashed})
    current_user_id = inserted.inserted_id
    messagebox.showinfo("Success", "Registration successful!")

def login():
    global current_user_id

    username = entry_username.get()
    password = entry_password.get()

    user = app_users.find_one({"username": username})
    if not user:
        messagebox.showerror("Error", "User not found!")
        return
    
    if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        current_user_id = user['_id']
        messagebox.showinfo("Success", "Logged in successfully!")
    else:
        messagebox.showerror("Error", "Password is incorrect!")

def save_password():
    platform_link = entry_platform.get()
    platform_name = urlparse(platform_link).netloc.split('.')[0]
    username = entry_platform_username.get()
    password = entry_platform_password.get()
    tags = entry_tags.get().split(",")[:3]  # Only get up to 3 tags

    if not current_user_id:
        messagebox.showerror("Error", "Please log in first!")
        return

    passwords.insert_one({
        "platform": platform_name,
        "link": platform_link,
        "username": username,
        "password": password,
        "tags": tags,
        "user_id": current_user_id
    })
    messagebox.showinfo("Success", "Password saved successfully!")

# Create the main window
app = tk.Tk()
app.title("MongoDB Password App")

# User Registration and Login
tk.Label(app, text="App Username").pack(pady=10)
entry_username = tk.Entry(app)
entry_username.pack(pady=5)

tk.Label(app, text="App Password").pack(pady=10)
entry_password = tk.Entry(app, show="*")
entry_password.pack(pady=5)

btn_register = tk.Button(app, text="Register", command=register)
btn_register.pack(pady=10)

btn_login = tk.Button(app, text="Login", command=login)
btn_login.pack(pady=10)

# Save Passwords for Platforms
tk.Label(app, text="Platform Link (e.g., https://github.com)").pack(pady=10)
entry_platform = tk.Entry(app)
entry_platform.pack(pady=5)

tk.Label(app, text="Platform Username").pack(pady=10)
entry_platform_username = tk.Entry(app)
entry_platform_username.pack(pady=5)

tk.Label(app, text="Platform Password").pack(pady=10)
entry_platform_password = tk.Entry(app, show="*")
entry_platform_password.pack(pady=5)

tk.Label(app, text="Tags (comma-separated)").pack(pady=10)
entry_tags = tk.Entry(app)
entry_tags.pack(pady=5)

btn_save_password = tk.Button(app, text="Save Password", command=save_password)
btn_save_password.pack(pady=10)

# Start the GUI loop
app.mainloop()
