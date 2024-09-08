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
import datetime

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
        
    def logout(self):
        try:
            self.client.logout()
            self.logged = False
            self.login_type = 'Not Logged'
            if self.client.logged_on:
                return False
            return True
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

    def get_manifest_content(self, app_id: int, depot_id: int, manifest_id: int) -> Union[str, Exception]:
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
        
    def get_app_depot_info(self, app_id):
        try:
            info = self.cdn.get_app_depot_info(app_id)
            return info
        except Exception as e:
            return e

# Steamworks Common Redistributables list and names since they dont work like normal apps
CSR = [
        228981, 228982, 228983, 228984, 228985, 228986, 228987,
        228988, 228989, 228990, 229000, 229001, 229002, 229003,
        229004, 229005, 229006, 229007, 229010, 229011, 229012,
        229020, 229030, 229031, 229032, 229033
    ]

def GetCSRName(CSR: int) -> str:
    if CSR == 228981:
        return 'Windows VC 2005 Redist'
    elif CSR == 228982:
        return 'Windows VC 2008 Redist'
    elif CSR == 228983:
        return 'Windows VC 2010 Redist'
    elif CSR == 228984:
        return 'Windows VC 2012 Redist'
    elif CSR == 228985:
        return 'Windows VC 2013 Redist'
    elif CSR == 228986:
        return 'Windows VC 2015 Redist'
    elif CSR == 228987:
        return 'Windows VC 2017 Redist'
    elif CSR == 228988:
        return 'Windows VC 2019 Redist'
    elif CSR == 228989:
        return 'Windows VC 2022 Redist'
    elif CSR == 228990:
        return 'Windows DirectX Jun 2010 Redist'
    elif CSR == 229000:
        return 'Windows .NET 3.5 Redist'
    elif CSR == 229001:
        return 'Windows .NET 3.5 Client Profile Redist'
    elif CSR == 229002:
        return 'Windows .NET 4.0 Redist'
    elif CSR == 229003:
        return 'Windows .NET 4.0 Client Profile Redist'
    elif CSR == 229004:
        return 'Windows .NET 4.5.2 Redist'
    elif CSR == 229005:
        return 'Windows .NET 4.6 Redist'
    elif CSR == 229006:
        return 'Windows .NET 4.7 Redist'
    elif CSR == 229007:
        return 'Windows .NET 4.8 Redist'
    elif CSR == 229010:
        return 'Windows XNA 3.0 Redist'
    elif CSR == 229011:
        return 'Windows XNA 3.1 Redist'
    elif CSR == 229012:
        return 'Windows XNA 4.0 Redist'
    elif CSR == 229020:
        return 'Windows OpenAL 2.0.7.0 Redist'
    elif CSR == 229030:
        return 'Windows PhysX System Software 8.09.04'
    elif CSR == 229031:
        return 'Windows PhysX System Software 9.12.1031'
    elif CSR == 229032:
        return 'Windows PhysX System Software 9.13.1220'
    elif CSR == 229033:
        return 'Windows PhysX System Software 9.14.0702'
    else:
        return 'Unknown CSR'

def log_debug_print(content, do):
    if do:
        print(content)

def dump(dump):
    if type(dump) == dict:
        with open('Logs/dump.json', 'w') as file:
            json.dump(dump, file, indent=6)
    else:
        with open('Logs/dump.dump', 'w') as file:
            file.write(str(dump))


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

    # Get application info
    log_debug_print(f'Getting Information for {app_id}', debug_print)
        
    data = csd.get_app_info(app_id)
    app_data = data['apps'].get(app_id, {})
    log_debug_print(f'Got Information', debug_print)

    log_debug_print(f'Setting Base Information', debug_print)
    csdg = {}
    csdg['loginType'] = csd.login_type
    csdg['date'] = str(datetime.date.today())
    csdg['appID'] = app_id
    csdg['name'] = app_data['common']['name']
    csdg['oslist']= app_data['common']['oslist']
    csdg['osarch'] = app_data['common']['osarch']
    csdg['depots'] = {}
    log_debug_print(f'Set Base Information', debug_print)

    for depot_id, depot_info in app_data['depots'].items():
        if not depot_id.isdigit():
            log_debug_print(f"Depot '{depot_id}' is not a number, skipped...", debug_print)
            continue

        depot_id = int(depot_id)

        config = depot_info.get('config', {})
        manifests = depot_info.get('manifests', {})
        log_debug_print(f"Getting Name...", debug_print)
        name = csd.get_app_info(depot_id).get('apps', {}).get(depot_id, {}).get('common', {}).get('name', 'no_name')

        if depot_id in CSR:
            log_debug_print(f'Depot is a Steamworks Common Redistributable', debug_print)
            csdg['depots'][depot_id] = {
                "name": GetCSRName(depot_id),
                "config":{
                "osarch": config.get('osarch', '0'),
                "oslist": config.get('oslist', 'universal'),
                "optionaldlc": config.get('optionaldlc', 'no'),
                "CSR": True
                }
            }
            continue
        else:
            log_debug_print(f'Depot {depot_id} qualifies for storage', debug_print)
            content = str(csd.get_manifest_content(app_id, depot_id, int(manifests.get('public', {}).get('gid', '0'))))
            key = str(csd.get_depot_key(app_id, depot_id))
            csdg['depots'][depot_id] = {
                "name": name,
                "key": key,
                "config":{
                    "osarch": config.get('osarch', '0'),
                    "oslist": config.get('oslist', 'universal'),
                    "optionaldlc": config.get('optionaldlc', 'no'),
                    "CSR": False
                },
                "manifests": {
                    "public": {
                        "download": int(manifests.get('public', {}).get('download', '0')),
                        "gid": int(manifests.get('public', {}).get('gid', '0')),
                        "size": int(manifests.get('public', {}).get('size', '0')),
                        "content": content
                    }
                }
            }

    with open(f'CSDG/{app_id}.csdg', 'w') as file:
        json.dump(csdg, file, indent=6)
