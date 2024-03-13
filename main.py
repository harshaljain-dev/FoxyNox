import json
import hashlib
import os
from getpass import getpass

from utils.password_manager import add_password, get_password, create_key   
from utils.password_generator import generate_password
from utils.password_strength_checker import check_password_strength
from utils.password_breach_checker import check_password_breach
from utils.common import print_intro

USERS_FILE = "users.json"

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return hashed_password.hex(), salt.hex()

def register_user(user_id, password):
    if not os.path.exists(USERS_FILE):
        users = {}
    else:
        with open(USERS_FILE, "r") as file:
            users = json.load(file)

    hashed_password, salt = hash_password(password)

    users[user_id] = {"password": hashed_password, "salt": salt}

    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

def authenticate_user(user_id, password):
    if not os.path.exists(USERS_FILE):
        return False

    with open(USERS_FILE, "r") as file:
        users = json.load(file)

    if user_id in users:
        hashed_password = users[user_id]["password"]
        salt = bytes.fromhex(users[user_id]["salt"])

        input_hashed_password, _ = hash_password(password, salt)

        if input_hashed_password == hashed_password:
            return True

    return False

def show_menu(user_id, key):
    while True:
        print("1. Add Password")
        print("2. Get Password")
        print("3. Generate Password")
        print("4. Check Password Strength")
        print("5. Check Password Breach")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_password(user_id, key)  # Pass the 'user_id' and 'key' arguments
        elif choice == "2":
            get_password(user_id, key)  # Pass the 'user_id' and 'key' arguments
        elif choice == "3":
            length = int(input("Enter password length: "))
            password = generate_password(length)
            print(f"Generated Password: {password}")
        elif choice == "4":
            password = input("Enter password: ")
            strength = check_password_strength(password)
            print(f"Password Strength: {strength}")
        elif choice == "5":
            password = input("Enter password: ")
            is_breached = check_password_breach(password)
            if is_breached:
                print("Password has been breached!")
            else:
                print("Password is secure!")
        elif choice == "6":
            break
        else:
            print("Invalid choice!")

def main():
    print_intro()

    # Ask if the user is an existing user or a new user
    user_type = input("Are you an existing user? (Y/N): ")

    if user_type.lower() == "y":
        # Existing user login
        user_id = input("Enter user ID: ")
        password = getpass("Enter password: ")

        # Authenticate user
        if authenticate_user(user_id, password):
            print("Authentication successful!\n")
            key = create_key(password)  # Create or load the key
            show_menu(user_id, key)  # Pass the 'user_id' and 'key' to the show_menu function
        else:
            print("Authentication failed. Incorrect user ID or password.")
    elif user_type.lower() == "n":
        # New user registration
        while True:
            user_id = input("Enter a user ID: ")
            password = getpass("Enter a password: ")
            confirm_password = getpass("Confirm password: ")

            if password == confirm_password:
                # Register the new user
                register_user(user_id, password)
                print("Registration successful!\n")
                key = create_key(password)  # Create or load the key
                show_menu(user_id, key)  # Pass the 'user_id' and 'key' to the show_menu function
                break
            else:
                print("Passwords do not match. Please try again.")
    else:
        print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()