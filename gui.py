import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import pymongo
import bcrypt
from decouple import config
from urllib.parse import urlparse

MONGODB_URI = config('MONGODB_URI')
client = pymongo.MongoClient(MONGODB_URI)
db = client.passwords_db
app_users = db.app_users
passwords = db.passwords

current_user_id = None

def register():
    username = entry_username.get()
    password = entry_password.get()
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password!")
        return
    if app_users.find_one({"username": username}):
        messagebox.showerror("Error", "Username already exists!")
        return
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    app_users.insert_one({"username": username, "password": hashed})
    messagebox.showinfo("Success", "Registration successful!")

def login(event=None):
    global current_user_id
    username = entry_username.get()
    password = entry_password.get()
    user = app_users.find_one({"username": username})
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        messagebox.showerror("Error", "Invalid credentials!")
        return
    current_user_id = user['_id']
    login_frame.pack_forget()
    password_manager_frame.pack()
    display_passwords()

def add_password():
    show_sidebar()

def display_passwords():
    for record in password_table.get_children():
        password_table.delete(record)
    for pwd in passwords.find({"user_id": current_user_id}):
        password_table.insert("", "end", values=(pwd["platform"], pwd["username"], "******", ",".join(pwd["tags"])), tags=('password', pwd["password"]))

def reveal_password():
    item = password_table.selection()[0]
    password = password_table.item(item, "tags")[1]
    password_table.set(item, "Password", password)

def copy_to_clipboard():
    item = password_table.selection()[0]
    password = password_table.item(item, "tags")[1]
    app.clipboard_clear()
    app.clipboard_append(password)

def show_password(event):
    reveal_password()

def on_right_click(event):
    password_table.selection_set(password_table.identify_row(event.y))
    right_click_menu.post(event.x_root, event.y_root)

def logout():
    global current_user_id
    current_user_id = None
    password_manager_frame.pack_forget()
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    login_frame.pack()

def hide_sidebar():
    sidebar_frame.pack_forget()
    add_button.pack(side="left")

def show_sidebar():
    sidebar_frame.pack(side="right", fill="y")
    add_button.pack_forget()

def save_password():
    platform_link = entry_platform_link.get()
    platform_name = urlparse(platform_link).netloc.split('.')[0]
    platform_username = entry_platform_username.get()
    platform_password = entry_platform_password.get()
    tags = entry_tags.get().split(",")[:3]
    passwords.insert_one({
        "platform": platform_name,
        "link": platform_link,
        "username": platform_username,
        "password": platform_password,
        "tags": tags,
        "user_id": current_user_id
    })
    display_passwords()
    hide_sidebar()

app = tk.Tk()
app.title("Password Manager")
app.geometry("800x400")
app.minsize(800, 400)

login_frame = ttk.Frame(app)
login_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
ttk.Label(login_frame, text="Username").grid(row=0, column=0, pady=5)
entry_username = ttk.Entry(login_frame)
entry_username.grid(row=0, column=1, pady=5, padx=5)
ttk.Label(login_frame, text="Password").grid(row=1, column=0, pady=5)
entry_password = ttk.Entry(login_frame, show="*")
entry_password.grid(row=1, column=1, pady=5, padx=5)
entry_password.bind('<Return>', login)
ttk.Button(login_frame, text="Login", command=login).grid(row=2, column=0, pady=10, padx=5, sticky='e')
ttk.Button(login_frame, text="Sign Up", command=register).grid(row=2, column=1, pady=10, padx=5, sticky='w')

password_manager_frame = ttk.Frame(app)
password_manager_frame.pack(side="left", fill="both", expand=True)

search_bar = ttk.Entry(password_manager_frame)
search_bar.pack(pady=10, fill=tk.X, padx=10)

password_table = ttk.Treeview(password_manager_frame, columns=("Platform", "Username", "Password", "Tags"), show="headings")
password_table.heading("Platform", text="Platform")
password_table.heading("Username", text="Username")
password_table.heading("Password", text="Password")
password_table.heading("Tags", text="Tags")
password_table.bind('<Button-3>', on_right_click)
password_table.bind('<Double-1>', show_password)
password_table.pack(pady=20, fill=tk.BOTH, expand=True, padx=10)

right_click_menu = tk.Menu(app, tearoff=0)
right_click_menu.add_command(label="Reveal", command=reveal_password)
right_click_menu.add_command(label="Copy to Clipboard", command=copy_to_clipboard)

button_frame = ttk.Frame(password_manager_frame)
button_frame.pack(pady=10, fill=tk.X, padx=10)

add_button = ttk.Button(button_frame, text="+", command=show_sidebar)
add_button.pack(side="left")

logout_button = ttk.Button(button_frame, text="Logout", command=logout)
logout_button.pack(side="right")

sidebar_frame = ttk.Frame(password_manager_frame)
ttk.Label(sidebar_frame, text="Platform Link").pack(pady=5, padx=10)
entry_platform_link = ttk.Entry(sidebar_frame)
entry_platform_link.pack(pady=5, padx=10, fill=tk.X)
ttk.Label(sidebar_frame, text="Username").pack(pady=5, padx=10)
entry_platform_username = ttk.Entry(sidebar_frame)
entry_platform_username.pack(pady=5, padx=10, fill=tk.X)
ttk.Label(sidebar_frame, text="Password").pack(pady=5, padx=10)
entry_platform_password = ttk.Entry(sidebar_frame, show="*")
entry_platform_password.pack(pady=5, padx=10, fill=tk.X)
ttk.Label(sidebar_frame, text="Tags (comma-separated)").pack(pady=5, padx=10)
entry_tags = ttk.Entry(sidebar_frame)
entry_tags.pack(pady=5, padx=10, fill=tk.X)
ttk.Button(sidebar_frame, text="Hide", command=hide_sidebar).pack(pady=10, padx=10, side="left")
ttk.Button(sidebar_frame, text="Save", command=save_password).pack(pady=10, padx=10, side="right")

app.mainloop()
