import json
import os
import argparse
from cryptography.fernet import Fernet

# Encryption and Decryption Functions
def generate_key():
    return Fernet.generate_key()

def load_key():
    if not os.path.exists("secret.key"):
        key = generate_key()
        save_key(key)
    return open("secret.key", "rb").read()

def save_key(key):
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def encrypt_message(message):
    key = load_key()
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

# Password Manager Functions
def load_credentials():
    if not os.path.exists("credentials.json"):
        return {}
    with open("credentials.json", "r") as file:
        return json.load(file)

def save_credentials(credentials):
    with open("credentials.json", "w") as file:
        json.dump(credentials, file)

def add_credential(name, username, password):
    credentials = load_credentials()
    encrypted_password = encrypt_message(password).decode()
    credentials[name] = {"username": username, "password": encrypted_password}
    save_credentials(credentials)
    print("Credential added successfully.")

def view_credentials(name):
    credentials = load_credentials()
    if name in credentials:
        user_info = credentials[name]
        decrypted_password = decrypt_message(user_info["password"])
        print(f"Name: {name}")
        print(f"Username: {user_info['username']}")
        print(f"Password: {decrypted_password}")
    else:
        print("Credential not found.")

def edit_credential(name, new_username=None, new_password=None):
    credentials = load_credentials()
    if name in credentials:
        if new_username:
            credentials[name]["username"] = new_username
        if new_password:
            encrypted_password = encrypt_message(new_password).decode()
            credentials[name]["password"] = encrypted_password
        save_credentials(credentials)
        print("Credential updated successfully.")
    else:
        print("Credential not found.")

# Command-Line Interface
def main():
    parser = argparse.ArgumentParser(description="Simple Password Manager")
    parser.add_argument("command", choices=["add", "view", "edit"], help="Command to run")
    parser.add_argument("name", help="Name of the credential")
    parser.add_argument("--username", help="Username for the credential")
    parser.add_argument("--password", help="Password for the credential")
    args = parser.parse_args()

    if args.command == "add":
        if args.username and args.password:
            add_credential(args.name, args.username, args.password)
        else:
            print("Both username and password are required to add a credential.")
    elif args.command == "view":
        view_credentials(args.name)
    elif args.command == "edit":
        edit_credential(args.name, args.username, args.password)

if __name__ == "__main__":
    main()