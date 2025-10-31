import requests
import random
import string
from threading import Thread, Lock, Event

white = "\033[97m"
red = "\033[91m"
green = "\033[92m"
reset = "\033[0m"

letters = string.ascii_letters
digits = string.digits
special = "_"
all_chars = letters + digits + special

num_threads = 20

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
        print(f"{white}Trying: {username}{reset}", end="\r")
        available = is_username_available(username)
        if available is None:
            print(f"{red}Error checking: {username}{reset}")
            continue
        if available:
            with lock:
                if not found_event.is_set():
                    found_username = username
                    found_event.set()
                    print(f"\n{green}User not taken: {username}{reset}")
                    break
        else:
            print(f"{red}Taken: {username}{reset}", end="\r")

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
        for _ in range(num_threads):
            thread = Thread(target=worker, args=(length,))
            thread.start()
            threads.append(thread)

        found_event.wait()

        for thread in threads:
            thread.join()

        input("Press Enter to generate another username...")
        found_username = None
        found_event.clear()

if __name__ == "__main__":
    run_generator()
