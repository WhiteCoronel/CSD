from steam.client import SteamClient
from steam.client.cdn import CDNClient
import os
import time
import ast

client = SteamClient()
cdn = CDNClient(client)

def login():
    """Handle user login, including anonymous login."""
    username = input("Username (Leave empty for Anonymous logging): ")
    if username:
        password = input("Password: ")
        TwoFA = input("2FA/Steam Guard Code: ")
        client.login(username, password, two_factor_code=TwoFA)
        if client.logged_on:
            print(f'User {username.capitalize()} has been logged on successfully')
            password = 'You saw nothing'
    else:
        client.anonymous_login()
        if client.logged_on:
            print('Anonymous logging successful')

def find_csdg():
    """Find the first .csdg file in the current directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for dirs_path, dirs_names, filenames in os.walk(current_dir):
        for filename in filenames:
            if filename.lower().endswith('.csdg'):
                return filename
    return None

def load_from_csdg(csdg):
    """Load data from a .csdg file."""
    global app_id, depot_id, manifest_id, depot_key, manifest
    with open(csdg) as csdg_file:
        app_id = int(csdg_file.readline())
        depot_id = int(csdg_file.readline())
        manifest_id = int(csdg_file.readline())
        depot_key = bytes.fromhex(csdg_file.readline().strip())
        manifest = ast.literal_eval(csdg_file.readline())
        cdn.manifests[(app_id, depot_id, manifest_id)] = cdn.DepotManifestClass(cdn, app_id, manifest)

def make_csdg(app_id, depot_id, manifest_id, depot_key, manifest_request_code=0):
    """Create a .csdg file with the provided data."""
    resp = cdn.cdn_cmd('depot', f'{depot_id}/manifest/{manifest_id}/5/{manifest_request_code}')
    depot_key_hex = depot_key.hex()
    if resp.ok:
        with open(f'{app_id}_{depot_id}_{manifest_id}.csdg', 'w') as file:
            file.write(f'{app_id}\n')
            file.write(f'{depot_id}\n')
            file.write(f'{manifest_id}\n')
            file.write(f'{depot_key_hex}\n')
            file.write(str(resp.content))

def add_csdg_data_to_client():
    """Add .csdg data to the CDN client."""
    global app_id, depot_id, manifest_id, depot_key, manifest
    cdn.depot_keys[depot_id] = depot_key
    cdn.manifests[(app_id, depot_id, manifest_id)] = cdn.DepotManifestClass(cdn, app_id, manifest)
    manifest = cdn.get_manifest(app_id, depot_id, manifest_id)

def download_game():
    """Download game files based on the manifest."""
    global app_id, depot_id, manifest_id, depot_key
    try:
        manifest = cdn.get_manifest(app_id, depot_id, manifest_id)
        manifest.decrypt_filenames(depot_key)
        if not manifest:
            print("Failed to retrieve the manifest.")
            return
        files = list(manifest.iter_files())
        print(f"Number of files to download: {len(files)}")
        print("You might see permission errors; if they occur while making a directory/folder, there is nothing to worry about")
        input("Press enter to start downloading files...")
        for file in files:
            print(f"Downloading {file.filename}...")
            try:
                content = file.readlines()
                dir_path = os.path.dirname(f"{app_id}/{file.filename}")
                os.makedirs(dir_path, exist_ok=True)
                file_path = f'{app_id}/{file.filename}'
                with open(file_path, 'wb') as file_out:
                    for chunk in content:
                        file_out.write(chunk)
                print(f"File {file.filename} saved successfully.")
            except PermissionError as e:
                print(f"Permission error while saving file {file.filename}: {e}")
            except Exception as e:
                print(f"Unexpected error while saving file {file.filename}: {e}")
        print('Game Downloaded!')
        input('Press any key to continue')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

app_id = 'LOAD .CSDG!'
depot_id = 'LOAD .CSDG!'
manifest_id = 'LOAD .CSDG!'
depot_key = 'LOAD .CSDG!'
manifest = 'LOAD .CSDG!'

def TUI():
    """Terminal User Interface for the application."""
    global app_id, depot_id, manifest_id, depot_key, manifest, csdg
    csdg = None

    print("!!! WARNING !!!")
    print("THIS PoC HAS ZERO ERROR HANDLING APART FROM THE FILE SAVING PART")
    print("BE EXTRA CAREFUL WHILE FILLING THE INFORMATION TO AVOID HAVING TO DO EVERYTHING AGAIN")
    print("!!! ENSURE YOU ARE RUNNING THE SCRIPT FROM INSIDE CSD OTHERWISE YOU WILL FIND ERRORS WHILE LOADING OR MAKING FILES !!!")
    print("!!! WHILE I HAVE DONE MY BEST TO ENSURE YOUR SECURITY, ONLY LOAD .csdg's FROM TRUSTED SOURCES !!!")
    time.sleep(5)

    while True:
        csdg_found = csdg is not None
        print(f"""
Proof of Concept
Coronel Steam Downloader
CSDG File found: {csdg_found}
Current AppID: {app_id}
Logged in: {client.logged_on}

1. Logging (Do this first, Non-Anonymous login requires 2FA/Steam Guard Code)
2. Logout (If you want to change account)
3. Find csdg (Can make CSDG File found True)
4. Load .csdg (Requires 'CSDG File found' to be True)
5. Make .csdg (Requires Logging with an account that owns the game)
6. Download game
7. FAQ 
8. Exit (You dont need to download the game to save the .csdg)
                """)
        selection = int(input('Selection (number): '))

        if selection == 1:
            login()
        elif selection == 2:
            client.logout()
        elif selection == 3:
            csdg = find_csdg()
            print(csdg)
            input('Press any key to continue')   
        elif selection == 4:
            if csdg_found:
                load_from_csdg(csdg)
                add_csdg_data_to_client()
            else:
                print('Option not Available at the moment')
                input('Press any key to continue')
        elif selection == 5:
            if client.logged_on:
                print("This function assumes you are logged with an account that owns the game")
                print("Use SteamDB to avoid errors")
                app_id = int(input("AppID: "))
                depot_id = int(input("DepotID: "))
                manifest_id = int(input("ManifestID: "))
                depot_key = cdn.get_depot_key(app_id, depot_id)
                code = cdn.get_manifest_request_code(app_id, depot_id, manifest_id)
                make_csdg(app_id, depot_id, manifest_id, depot_key, code)
                print('Made .csdg!')
                input('Press any key to continue')
        elif selection == 6:
            download_game()
        elif selection == 7:
            os.system('cls')
            print("""
FAQ:

Q: I dont have a .csdg but I have an account that owns the game and I want to make one.
A: Perfect! First log in using option 1, then head to 5 where you need to fill everything using SteamDB.
   Your .csdg should appear now in the same folder the script is.
   
Q: I have a .csdg and I want to download the game
A: Perfect! First log in using option 1, then head to 3 to make the script find it, then 4 to make it load it.
   then press 7 to download the game! It will be located in a folder with the same AppID you see in the 'Current AppID:'
   Section of the main menu.
   This does not require an account that owns the game.
   
Q: I have both a .csdg and a account that owns the game.
A: You should use steam to download it to be honest.

Q: I downloaded the game, but it doesn't run.
A: Taking away the obvious, if you didn't download it completely or if it showed an error at the moment of writing a file then it is incomplete.
A: Some Steam Games require multiple Depots to run, check SteamDB to see which depots you have to download to run the game.
A: Each Depot requires its own DepotKey and Manifest, which means its own .csdg.
   The current version of the script is more focused on single-depot games, but this will change in the future.
   
Q: I downloaded a game with DRM and it doesn't run.
A: This is not a steam alternative, it will still require Steam to run.

Q: Any test .csdg?
A: In the Releases page there should be a 480_481_3183503801510301321.csdg, this is steam test game 'SpaceWar', you can go ahead and download it
   since it is free and it is already on your steam account.

Q: I need more

 assistance/help with the project.
A: Sure! I am on reddit as u/whitecoronel so shot me a DM!

""")
            input("I finished reading the FAQ (Press Enter)")
        elif selection == 8:
            exit()
        os.system('cls')

TUI()