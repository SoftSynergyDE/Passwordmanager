import json
import os
import platform
import secrets
import string
import pyperclip
import time
from collections import defaultdict

class PasswordEntry:
    def __init__(self, username, email, password):
        # Initialize a password entry with username, email, and password
        self.username = username
        self.email = email
        self.password = password

    def __str__(self):
        # Define how the password entry is represented as a string
        return f"Username: {self.username}, Email: {self.email}, Password: {self.password}"

    def update(self, username=None, email=None, password=None):
        # Update the password entry with new values if provided
        if username:
            self.username = username
        if email:
            self.email = email
        if password:
            self.password = password

class PasswordManager:
    FILE_NAME = "passwords.json"  # Name of the file where passwords will be stored

    def __init__(self):
        # Upon initialization, load existing passwords from the file
        self.password_store = self.load_passwords()

    @staticmethod
    def clear_console():
        # Clear the console screen based on the operating system
        system_name = platform.system()
        if system_name == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    @staticmethod
    def pause_console():
        # Pause the console until the user presses any key
        input("\nPress any key to continue...")

    def save_passwords(self):
        # Save all password entries to the JSON file
        try:
            with open(self.FILE_NAME, 'w', encoding='utf-8') as file:
                # Convert password entries to dictionaries for JSON serialization
                json.dump(
                    {service: vars(entry) for service, entry in self.password_store.items()},
                    file, ensure_ascii=False, indent=4
                )
            print("Entries saved successfully!")
            time.sleep(1)
        except IOError as e:
            print(f"Error saving entries: {e}")

    def load_passwords(self):
        # Load password entries from the JSON file
        if not os.path.exists(self.FILE_NAME):
            print("No existing file found. Creating a new one.")
            time.sleep(1)
            return {}
        try:
            with open(self.FILE_NAME, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # Reconstruct PasswordEntry objects from loaded data
                return {service: PasswordEntry(**entry) for service, entry in data.items()}
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading entries: {e}")
            time.sleep(1)
            return {}

    def create_password(self):
        # Add a new password entry
        self.clear_console()
        print("Add new password:")
        service = input("Enter the name of the service: ").strip()
        if service in self.password_store:
            print("An entry for this service already exists.")
            time.sleep(2)
            return

        username = input("Enter the username: ").strip()
        email = input("Enter the email address: ").strip()
        password = input("Enter the password: ").strip()

        # Store the new entry in the password store
        self.password_store[service] = PasswordEntry(username, email, password)
        print("Entry saved!")
        time.sleep(2)

    def read_passwords(self):
        # Display all saved password entries
        self.clear_console()
        if not self.password_store:
            print("No saved entries found.")
            time.sleep(2)
            return

        print("Saved entries:")
        for service, entry in self.password_store.items():
            print(f"Service: {service} - {entry}")
        print(f"\nTotal saved passwords: {len(self.password_store)}")
        self.pause_console()

    def view_sorted_by_passwords(self):
        # Display entries grouped and sorted by the password used
        self.clear_console()
        if not self.password_store:
            print("No saved entries available.")
            time.sleep(2)
            return

        password_groups = defaultdict(list)
        # Group services by password
        for service, entry in self.password_store.items():
            password_groups[entry.password].append(service)

        print("Saved entries sorted by passwords (ordered by frequency):")
        # Sort passwords by the number of services using them, in descending order
        sorted_passwords = sorted(password_groups.items(), key=lambda item: len(item[1]), reverse=True)
        for password, services in sorted_passwords:
            print(f"\nPassword: {password} - Count: {len(services)}")
            for service in services:
                entry = self.password_store[service]
                print(f"  Service: {service}")
                print(f"    Username: {entry.username}, Email: {entry.email}")
        self.pause_console()

    def update_password(self):
        # Update an existing password entry
        self.clear_console()
        print("Update password:")
        service = input("Enter the name of the service you want to update: ").strip()
        if service not in self.password_store:
            print("No entry found for this service.")
            time.sleep(2)
            return

        entry = self.password_store[service]
        username = input("Enter the new username (leave empty to keep current): ").strip()
        email = input("Enter the new email address (leave empty to keep current): ").strip()
        password = input("Enter the new password (leave empty to keep current): ").strip()

        # Update the entry with new information if provided
        entry.update(username=username or None, email=email or None, password=password or None)
        print("Entry updated!")
        time.sleep(2)

    def delete_password(self):
        # Remove a password entry from the store
        self.clear_console()
        print("Delete password:")
        service = input("Enter the name of the service you want to delete: ").strip()
        if service in self.password_store:
            del self.password_store[service]
            print("Entry deleted!")
        else:
            print("No entry found for this service.")
        time.sleep(2)

    def generate_random_password(self, length=16):
        # Generate a random secure password and store it
        self.clear_console()
        print("Generate random secure password:")
        service = input("Enter the name of the service: ").strip()
        if service in self.password_store:
            print("An entry for this service already exists.")
            time.sleep(2)
            return

        username = input("Enter the username: ").strip()
        email = input("Enter the email address: ").strip()

        # Create a random password using letters, digits, and punctuation
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(length))

        pyperclip.copy(password)  # Copy the generated password to the clipboard
        print(f"Generated password: {password}")
        print("The password has been copied to the clipboard.")

        # Save the new entry in the password store
        self.password_store[service] = PasswordEntry(username, email, password)
        print("Entry saved!")
        self.pause_console()

    def main(self):
        # Main program loop displaying options to the user
        while True:
            self.clear_console()
            print("Password Manager - Options:")
            print("1. Save new password")
            print("2. Show all passwords")
            print("3. Show passwords sorted by passwords")
            print("4. Update password")
            print("5. Delete password")
            print("6. Generate random secure password")
            print("7. Exit")
            choice = input("Please choose an option: ").strip()

            # Call the appropriate method based on user choice
            if choice == '1':
                self.create_password()
            elif choice == '2':
                self.read_passwords()
            elif choice == '3':
                self.view_sorted_by_passwords()
            elif choice == '4':
                self.update_password()
            elif choice == '5':
                self.delete_password()
            elif choice == '6':
                self.generate_random_password()
            elif choice == '7':
                self.save_passwords()
                print("Program terminated.")
                break
            else:
                print("Invalid option. Please enter a number between 1 and 7.")
                time.sleep(2)

if __name__ == "__main__":
    manager = PasswordManager()
    manager.main()
