import random
import string
import requests

# Roblox username check API
CHECK_URL = "https://auth.roblox.com/v1/usernames/validate"

# Allowed characters
letters = string.ascii_lowercase
digits = string.digits
special = "_"

# Generate random username
def generate_username(length):
    # First and last char cannot be "_"
    middle_chars = letters + digits + special
    first_last_chars = letters + digits
    
    username = random.choice(first_last_chars)  # first char
    for _ in range(length - 2):
        username += random.choice(middle_chars)
    username += random.choice(first_last_chars)  # last char
    return username

# Check username availability
def is_username_available(username):
    data = {
        "username": username,
        "context": "Signup"
    }
    response = requests.post(CHECK_URL, json=data)
    if response.status_code == 200:
        result = response.json()
        return result.get("code") == 0  # code 0 means available
    return False

def main():
    print("Roblox Username Generator")
    print("Choose an option:")
    print("1. 4-letter usernames")
    print("2. 5-letter usernames")
    
    choice = input("Enter 1 or 2: ")
    if choice == "1":
        length = 4
    elif choice == "2":
        length = 5
    else:
        print("Invalid choice!")
        return
    
    print(f"Generating {length}-letter usernames... Please wait.")
    
    attempts = 0
    while True:
        username = generate_username(length)
        attempts += 1
        if is_username_available(username):
            print(f"\n✅ Available username found: {username}")
            print(f"Attempts: {attempts}")
            break

if __name__ == "__main__":
    main()
