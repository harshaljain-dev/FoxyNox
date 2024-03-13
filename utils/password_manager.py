import json
import cryptography
from cryptography.fernet import Fernet
import os
from getpass import getpass

USERS_FILE = "users.json"
KEY_FILE = "key.txt"  # Choose a suitable file name

def create_key(password):
    # Check if the key file exists
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    else:
        # Generate a new key
        key = Fernet.generate_key()

        # Save the key to the file
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

    return key

def encrypt_password(key, password):
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode()).decode()

    return encrypted_password

def decrypt_password(key, encrypted_password):
    cipher = Fernet(key)
    decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()

    return decrypted_password

def add_password(user_id, key):
    website = input("Enter website: ")
    username = input("Enter username: ")
    password = getpass("Enter password: ")

    # Load existing credentials for the user
    data = load_credentials(user_id)

    # Encrypt the password
    encrypted_password = encrypt_password(key, password)

    # Add the new credentials
    data[website] = {"username": username, "password": encrypted_password}

    # Save the updated credentials with the user's ID
    save_credentials(user_id, data)

    print("Password added successfully!")

def get_password(user_id, key):
    website = input("Enter website: ")

    # Load existing credentials for the user
    data = load_credentials(user_id)

    if website in data:
        # Decrypt the password
        encrypted_password = data[website]["password"]
        decrypted_password = decrypt_password(key, encrypted_password)

        print(f"Password for {website}: {decrypted_password}")
    else:
        print(f"No password found for {website}")

def save_credentials(user_id, data):
    filename = f"{user_id}_passwords.json"
    with open(filename, "w") as file:
        json.dump(data, file)

def load_credentials(user_id):
    filename = f"{user_id}_passwords.json"
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    else:
        return {}
