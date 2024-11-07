import os
import sys
import json
from seedr import SeedrAPI

CREDENTIALS_FILE = os.path.expanduser("~/.seedr_credentials.json")

def save_credentials(email, password):
    credentials = {"email": email, "password": password}
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file)
    print("Credentials saved successfully.")

def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    return None

def prompt_for_credentials():
    email = input("Enter your Seedr email: ")
    password = input("Enter your Seedr password: ")
    save_credentials(email, password)
    return email, password

def download_and_clear(email, password, torrent_links):
    # Initialize Seedr API client with provided credentials
    seedr = SeedrAPI(email=email, password=password)

    for link in torrent_links:
        # Add torrent to Seedr
        response = seedr.add_torrent(link)
        if response['result']:
            folder_id = response['user_torrent_id']
            print(f"Added torrent: {response['title']}")

            # Get folder info and download files
            folder_info = seedr.get_folder(folder_id)
            for file in folder_info['files']:
                file_url = file['url']
                file_name = file['name']
                print(f"Downloading: {file_name}")
                os.system(f"curl -O {file_url}")

            # Clear the downloaded content from Seedr
            seedr.delete_folder(folder_id)
            print(f"Deleted folder with ID: {folder_id}")
        else:
            print(f"Failed to add torrent: {link}")

def main():
    # Check for the --login flag
    if "--login" in sys.argv:
        email, password = prompt_for_credentials()
        sys.argv.remove("--login")
    else:
        credentials = load_credentials()
        if credentials:
            email = credentials["email"]
            password = credentials["password"]
        else:
            email, password = prompt_for_credentials()

    if len(sys.argv) < 2:
        print("Usage: seedr-download \"magnet_link1\" \"magnet_link2\"")
        return

    torrent_links = sys.argv[1:]
    download_and_clear(email, password, torrent_links)

if __name__ == "__main__":
    main()

