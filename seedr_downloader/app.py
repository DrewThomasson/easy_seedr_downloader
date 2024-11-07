import os
import sys
import json
from seedrcc import Login, Seedr

CREDENTIALS_FILE = os.path.expanduser("~/.seedrcc_credentials.json")

def save_credentials(token):
    credentials = {"token": token}
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file)
    print("Token saved successfully.")

def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    return None

def prompt_for_login():
    email = input("Enter your Seedr email: ")
    password = input("Enter your Seedr password: ")
    seedr = Login(email, password)
    response = seedr.authorize()
    if response:
        save_credentials(seedr.token)
        return seedr.token
    else:
        print("Login failed. Please check your credentials.")
        sys.exit(1)

def download_and_clear(token, torrent_links):
    # Initialize Seedr API client with the token
    account = Seedr(token=token)

    for link in torrent_links:
        # Add torrent to Seedr
        response = account.addTorrent(link)
        if response.get('code') == 200:
            folder_id = response['user_torrent_id']
            print(f"Added torrent: {response.get('title')}")

            # List folder contents and download files
            folder_info = account.listContents()
            for file in folder_info.get('files', []):
                file_url = file['url']
                file_name = file['name']
                print(f"Downloading: {file_name}")
                os.system(f"curl -O {file_url}")

            # Clear the downloaded content from Seedr
            account.deleteFolder(folder_id)
            print(f"Deleted folder with ID: {folder_id}")
        else:
            print(f"Failed to add torrent: {link}")

def main():
    # Check for login options
    if "--login" in sys.argv:
        index = sys.argv.index("--login") + 1
        if index < len(sys.argv) and sys.argv[index] == "token":
            # Use the provided token
            token = input("Enter your Seedr token: ")
            save_credentials(token)
            sys.argv.remove("--login")
            sys.argv.remove("token")
        else:
            # Prompt for email and password login
            token = prompt_for_login()
            sys.argv.remove("--login")
    else:
        credentials = load_credentials()
        if credentials:
            token = credentials["token"]
        else:
            token = prompt_for_login()

    if len(sys.argv) < 2:
        print("Usage: seedr-download \"magnet_link1\" \"magnet_link2\"")
        return

    torrent_links = sys.argv[1:]
    download_and_clear(token, torrent_links)

if __name__ == "__main__":
    main()

