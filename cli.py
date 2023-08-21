import pymongo
import bcrypt
from decouple import config
from urllib.parse import urlparse
import getpass

# Setup MongoDB connection
MONGODB_URI = config('MONGODB_URI')
client = pymongo.MongoClient(MONGODB_URI)
db = client.passwords_db
app_users = db.app_users
passwords = db.passwords

current_user_id = None

def register():
    username = input("Enter app username: ")
    password = getpass.getpass("Enter app password: ")

    user = app_users.find_one({"username": username})
    if user:
        print("Error: Username already exists!")
        return
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    app_users.insert_one({"username": username, "password": hashed})
    print("\nRegistration successful!")
    print("Please proceed to login.")

def login():
    global current_user_id

    username = input("\nEnter app username: ")
    password = getpass.getpass("Enter app password: ")

    user = app_users.find_one({"username": username})
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        print("\nInvalid credentials!")
        return

    current_user_id = user['_id']
    print("\nLogged in successfully!")

def add_password():
    platform_link = input("\nEnter platform link (e.g., https://github.com): ")
    platform_name = urlparse(platform_link).netloc.split('.')[0]
    platform_username = input("Enter platform username: ")
    platform_password = getpass.getpass("Enter platform password: ")
    tags = input("Enter comma-separated tags (up to 3): ").split(",")[:3]
    
    passwords.insert_one({
        "platform": platform_name,
        "link": platform_link,
        "username": platform_username,
        "password": platform_password,
        "tags": tags,
        "user_id": current_user_id
    })
    print("\nPassword saved successfully!")

def display_passwords():
    print("\nStored Passwords:")
    for pwd in passwords.find({"user_id": current_user_id}):
        print(f"Platform: {pwd['platform']}, Username: {pwd['username']}, Password: ******, Tags: {', '.join(pwd['tags'])}")

def show_password():
    platform = input("\nEnter the platform name (e.g., github) to retrieve the password: ")
    pwd = passwords.find_one({"user_id": current_user_id, "platform": platform})
    if pwd:
        print(f"Password for {platform}: {pwd['password']}")
    else:
        print(f"No password found for platform: {platform}")

def logout():
    global current_user_id
    current_user_id = None
    print("\nLogged out!")

def main():
    while True:
        print("\n" + "="*30)
        print("     PASSWORD MANAGER CLI     ")
        print("="*30)

        if current_user_id:
            print("\n-- Menu --")
            print("1. Display passwords")
            print("2. Add password")
            print("3. Show password for platform")
            print("4. Logout")
            print("5. Exit")
        else:
            print("\n-- Menu --")
            print("1. Register")
            print("2. Login")
            print("3. Exit")

        choice = input("\nChoose an option: ")
        if current_user_id:
            if choice == "1":
                display_passwords()
            elif choice == "2":
                add_password()
            elif choice == "3":
                show_password()
            elif choice == "4":
                logout()
            elif choice == "5":
                break
            else:
                print("\nInvalid choice. Please choose a valid option.")
        else:
            if choice == "1":
                register()
            elif choice == "2":
                login()
            elif choice == "3":
                break
            else:
                print("\nInvalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
