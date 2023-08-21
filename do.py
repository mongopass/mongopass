import pymongo
import bcrypt
from decouple import config

# Retrieve MongoDB connection from .env file
MONGODB_URI = config('MONGODB_URI')

# MongoDB connection setup
client = pymongo.MongoClient(MONGODB_URI)
db = client.passwords_db
users = db.users

def register(username, password):
    # Check if username already exists
    user = users.find_one({"username": username})
    if user:
        print("Username already exists!")
        return
    
    # Hash the password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Store the hashed password
    users.insert_one({"username": username, "password": hashed})
    print("Registration successful!")

def check_password(username, password):
    user = users.find_one({"username": username})
    if not user:
        print("User not found!")
        return False
    
    # Check the password
    if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        print("Password is correct!")
        return True
    else:
        print("Password is incorrect!")
        return False

# Simple interface
while True:
    choice = input("Do you want to register (r) or check a password (c)? ")
    if choice == 'r':
        username = input("Enter username: ")
        password = input("Enter password: ")
        register(username, password)
    elif choice == 'c':
        username = input("Enter username: ")
        password = input("Enter password: ")
        check_password(username, password)
    else:
        print("Invalid choice!")

