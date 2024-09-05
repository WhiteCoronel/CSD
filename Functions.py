# Verify that the file isn't run as main
if __name__ == "__main__":
    print(f'{__file__} is not the file that contains the program main loop, check repo...')
    input('Press any key to continue...')
    exit()

import steam.client
import steam.client.cdn
import ast
import json
from typing import Union, Tuple

class CSD:
    """
    A wrapper class for managing SteamClient and CDNClient functionalities.

    Attributes:
        client (steam.client.SteamClient): The Steam client used for login and other interactions.
        cdn (steam.client.cdn.CDNClient): The CDN client for managing content delivery operations.
        logged (bool): Indicates whether the user is logged in.
        login_type (str): Describes the type of login used (Anonymous or Account).
    """

    def __init__(self) -> None:
        """
        Initializes the CSD instance with a Steam client and a CDN client.
        Sets the initial login status to False and the login type to 'Not Logged'.
        """
        self.client = steam.client.SteamClient()
        self.cdn = steam.client.cdn.CDNClient(self.client)
        self.logged: bool = False
        self.login_type: str = 'Not Logged'

    def login_anonymous(self) -> Union[bool, Exception]:
        """
        Attempts to log in anonymously.

        Returns:
            Union[bool, Exception]: True if login is successful, False if not logged in, or an Exception if an error occurs.
        """
        try:
            self.client.anonymous_login()
            if self.client.logged_on:
                self.logged = True
                self.login_type = 'Anonymous'
                return True
            return False
        except Exception as e:
            return e

    def login_cli(self) -> Union[bool, Exception]:
        """
        Attempts to log in using CLI credentials.

        Returns:
            Union[bool, Exception]: True if login is successful, False if not logged in, or an Exception if an error occurs.
        """
        try:
            self.client.cli_login()
            if self.client.logged_on:
                self.logged = True
                self.login_type = 'Account Logging (CLI)'
                return True
            return False
        except Exception as e:
            return e

    def login_web(self) -> Union[bool, Exception]:
        """
        Attempts to log in using a web session.

        Returns:
            Union[bool, Exception]: True if login is successful, False if not logged in, or an Exception if an error occurs.
        """
        try:
            self.client.get_web_session()
            if self.client.logged_on:
                self.logged = True
                self.login_type = 'Account Logging (Web)'
                return True
            return False
        except Exception as e:
            return e

    def add_depot_key(self, depot_id: int, depot_key: str) -> Union[bool, Exception]:
        """
        Adds a depot key to the CDN client's depot key collection.

        Args:
            depot_id (int): The ID of the depot.
            depot_key (str): The depot key in hexadecimal format.

        Returns:
            Union[bool, Exception]: True if the key was added successfully, or an Exception if an error occurs.
        """
        try:
            depot_key_bytes = bytes.fromhex(depot_key)
            self.cdn.depot_keys[depot_id] = depot_key_bytes
            return True
        except Exception as e:
            return e

    def add_manifest(self, app_id: int, depot_id: int, manifest_id: int, manifest: str) -> Union[bool, Exception]:
        """
        Adds a manifest to the CDN client's manifest collection.

        Args:
            app_id (int): The ID of the application.
            depot_id (int): The ID of the depot.
            manifest_id (int): The ID of the manifest.
            manifest (str): The manifest data in string form, to be evaluated safely.

        Returns:
            Union[bool, Exception]: True if the manifest was added successfully, or an Exception if an error occurs.
        """
        try:
            manifest_data = ast.literal_eval(manifest)
            self.cdn.manifests[(app_id, depot_id, manifest_id)] = self.cdn.DepotManifestClass(self.cdn, app_id, manifest_data)
            return True
        except Exception as e:
            return e

    def get_depot_key(self, app_id: int, depot_id: int) -> Union[str, Exception]:
        """
        Retrieves a depot key from the CDN client.

        Args:
            app_id (int): The ID of the application.
            depot_id (int): The ID of the depot.

        Returns:
            Union[str, Exception]: The depot key as a hexadecimal string, or an Exception if an error occurs.
        """
        try:
            depot_key = self.cdn.get_depot_key(app_id, depot_id)
            return depot_key.hex()
        except Exception as e:
            return e

    def get_manifest(self, app_id: int, depot_id: int, manifest_id: int) -> Union[str, Exception]:
        """
        Retrieves a manifest from the CDN.

        Args:
            app_id (int): The ID of the application.
            depot_id (int): The ID of the depot.
            manifest_id (int): The ID of the manifest.

        Returns:
            Union[str, Exception]: The manifest content as a string, or an Exception if an error occurs.
        """
        try:
            code = self.cdn.get_manifest_request_code(app_id, depot_id, manifest_id)
            response = self.cdn.cdn_cmd('depot', f'{depot_id}/manifest/{manifest_id}/5/{code}')
            return str(response.content)
        except Exception as e:
            return e
    
    def get_app_info(self, app_id):
        try:
            info = self.client.get_product_info([app_id])
            return info
        except Exception as e:
            return e

def auto_make_csdg(csd, app_id: int, debug_print=False) -> dict:
    """
    Extracts and transforms application data into a structured dictionary.

    Args:
        csd: An object providing methods to get application and depot data.
        app_id: The ID of the application to retrieve and transform data for.
        debug_print: If True, prints debug information.

    Returns:
        A dictionary containing the transformed application data.

    Raises:
        ValueError: If no data is found for the given app_id.
        TypeError: If expected data structures are not dictionaries.
    """
    # List of Steamworks Common Redistributables
    CSR = [
        228981, 228982, 228983, 228984, 228985, 228986, 228987,
        228988, 228989, 228990, 229000, 229001, 229002, 229003,
        229004, 229005, 229006, 229007, 229010, 229011, 229012,
        229020, 229030, 229031, 229032, 229033
    ]

    # Get application info
    if debug_print:
        print("Getting Information...")
        
    data = csd.get_app_info(app_id)
    app_data = data['apps'].get(app_id, {})
    
    if not app_data:
        raise ValueError(f"No data found for app ID {app_id}")

    if debug_print:
        print("Setting Base Information...")
        
    csdg = {
        "appID": app_id,
        "name": app_data['common']['name'],
        "oslist": app_data['common']['oslist'],
        "osarch": app_data['common']['osarch'],
        "depots": {}
    }

    for depot_id_str, depot_info in app_data['depots'].items():
        # Skip non-numeric depot IDs, because they aren't 'depots' for us
        if not depot_id_str.isdigit():
            if debug_print:
                print(f"Depot '{depot_id_str}' is not a number, skipped...")
            continue

        depot_id = int(depot_id_str)

        # Skip Steamworks Common Redistributables
        if depot_id in CSR:
            if debug_print:
                print(f"Depot {depot_id} is a Steamworks Common Redistributable, skipped...")
            continue

        # Retrieve depot configuration and manifests
        config = depot_info.get('config', {})
        manifests = depot_info.get('manifests', {})

        if debug_print:
            print(f"Getting Key for {depot_id}...")
            
        key = str(csd.get_depot_key(app_id, depot_id))
        
        if debug_print:
            print(f"Key: {key}")

        if debug_print:
            print(f"Getting Content for {depot_id}...")
            
        gid = int(manifests.get('public', {}).get('gid', '0'))
        content = str(csd.get_manifest(app_id, depot_id, gid))
        
        if debug_print:
            print(f"Got Content for {depot_id}")

        # Validate data types
        if not isinstance(config, dict):
            raise TypeError(f"Expected dictionary for config but got {type(config).__name__}")

        if not isinstance(manifests, dict):
            raise TypeError(f"Expected dictionary for manifests but got {type(manifests).__name__}")

        if debug_print:
            print(f"Saving data of Depot {depot_id}")

        # Populate csdg dictionary
        csdg["depots"][depot_id] = {
            "key": key,
            "config": {
                "osarch": config.get('osarch', '0'),
                "oslist": config.get('oslist', 'Universal')
            },
            "manifests": {
                "public": {
                    "download": int(manifests.get('public', {}).get('download', '0')),
                    "gid": gid,
                    "size": int(manifests.get('public', {}).get('size', '0')),
                    "content": content
                }
            }
        }

    # Write to file
    with open(f'CSDG/{app_id}.csdg', 'w') as file:
        json.dump(csdg, file, indent=6)

    return True

