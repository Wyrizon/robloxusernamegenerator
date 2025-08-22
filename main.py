import requests
import random
import string
from threading import Thread, Lock, Event

WHITE = "\033[97m"
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

letters = string.ascii_letters
digits = string.digits
special = "_"
all_chars = letters + digits + special

NUM_THREADS = 20  # Increase for faster checks

lock = Lock()
found_event = Event()
found_username = None

def generate_username(length):
    first_last = letters + digits
    username = random.choice(first_last)
    for _ in range(length - 2):
        username += random.choice(all_chars)
    username += random.choice(first_last)
    return username

def is_username_available(username):
    try:
        resp = requests.get(
            f'https://auth.roblox.com/v1/usernames/validate?request.username={username}&request.birthday=1337-04-20'
        )
        data = resp.json()
        return data.get('code') == 0
    except:
        return None

def worker(length):
    global found_username
    while not found_event.is_set():
        username = generate_username(length)
        print(f"{WHITE}Trying: {username}{RESET}", end="\r")
        available = is_username_available(username)
        if available is None:
            print(f"{RED}Error checking: {username}{RESET}")
            continue
        if available:
            with lock:
                if not found_event.is_set():
                    found_username = username
                    found_event.set()
                    print(f"\n{GREEN}User not taken: {username}{RESET}")
                    break
        else:
            print(f"{RED}Taken: {username}{RESET}", end="\r")

def run_generator():
    global found_username
    while True:
        while True:
            try:
                length = int(input("Enter username length (4-16): "))
                if length < 4 or length > 16:
                    print("Length must be between 4 and 16.")
                    continue
                break
            except:
                print("Invalid input.")

        threads = []
        for _ in range(NUM_THREADS):
            t = Thread(target=worker, args=(length,))
            t.start()
            threads.append(t)

        found_event.wait()

        for t in threads:
            t.join()

        input("Press Enter to generate another username...")
        found_username = None
        found_event.clear()

if __name__ == "__main__":
    run_generator()
