
# Coronel Steam Downloader

Simple tool with basic TUI to save both manifest and depot key for a Steam depot.

## Features

- Loggin with Account and Anonymous (With its limitations).
- Creation of a basic file (.csdg, which is a .txt with different extention) used to storage depot data.
- Basic CDN file saving, allowing you to download the depot without the need to use Steam.
- Basic TUI and FAQ for easier use.
- Resumable Downlaods

## Limitations

- As of the current version (PoC) there is no error handling besides the file saving part, which means any error in the user part while filling information could result in a crash
- No support for games that require multiple depots to work.

## Planned Features

- TUI using Rich library.
- Resumable Downloads.
- Error handling.
- Game data retrival.
- Support for games that require multiple depots.
## FAQ

#### How does it work?

It uses a python module (steam) to interact with Steam.

#### How secure it is?

It uses HTTP/s to do the logging part, and it does not save any logging information, just remember to always log out after finishing.

#### What is a .csdg?

A .txt with different extention, it saves the AppID, DepotID, ManifestID, DepotKey and Manifest. It would look something like this:

- 480 (AppID for Spacewar)
- 481 (DepotID for Spacewar, the other 229006 is an installer for .NET 4.7)
- 410c... (DepotKey for 481)
- 3183503801510301321 (Current ManifestID for 481)
- b'PK\x03\x04... (Manifest with ID 3183503801510301321)

#### Do I need to log in every time to use the .csdg I made?

Nope, just find it, load it, and you can download it.

#### How identifiable is a .csdg?

It uses completely generic data, the same data given to everyone that owns the game.

#### What happens to the DRM if the game haves one?

It is still there, you would still need steam to play the game.

#### It is not downloading the oldest version.

Yep, it will download whatever version the ManifestID is has points to.
This also means that if you want to make a very lightweight 'backup' of the current update that you will be able to download anytime even if the developer doesn't allow downgrading.

#### How do I do x or y.

Option 7 of the script has a tiny FAQ, if you have any more questions reach me out on reddit, username is u/whitecoronel.



## Installation

Basic Installation guide

#### 1. Download and install python

Download and Install python 3.12 using this link:
https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe

#### 2. Install required module

The script requires the module 'steam'. Open a terminal and type the following:

```bash
  pip install steam
```

#### 3. Downloading the script

Check the releases page of this repo, download the lastest

#### 4. Run the script

Easy enough, in the directory you have the script run:

```bash
  python CSD-PoC-Final.py
```
## Demo - Pre-Made .csdg

In the zip file you just unpacked there should be a 480_481....csdg, We are going to download Spacewar to test the script.

### Menu - Overlook

The menu should look something like this:

```bash
Proof of Concept
Coronel Steam Downloader
CSDG File found: False
Current AppID: LOAD .CSDG!
Logged in: False

1. Logging (Do this first, Non-Anonymous login requires 2FA/Steam Guard Code)
2. Logout (If you want to change account)
3. Find csdg (Can make CSDG File found True)
4. Load .csdg (Requires 'CSDG File found' to be True)
5. Make .csdg (Requires Logging with an account that owns the game)
6. Download game (This should be done after 1 and either 2 or 3 depending on what you doing)
7. FAQ
8. Exit (You dont need to download the game to save the .csdg)

Selection (number):
```
We will cover everything needed to download a game/depot in this Demo.
#### 1. Log in Anonymously

Chose option 1 in the main menu and leave the username empty. The Logged In header should change to True like this:
```
Proof of Concept
Coronel Steam Downloader
CSDG File found: False
Current AppID: LOAD .CSDG!
Logged in: True <-----
```
#### 2. 'Find' the .csdg

Option 3 will find a .csdg, it is prints 'None' ensure that the .csdg is on the same folder the script is.
If it prints the .csdg then you did it right and it should look like this:

```
Selection (number): 3
480_481_3183503801510301321.csdg
Press any key to continue
```
If that is the .csdg you are aiming to, then press continue, if not, remove other .csdgs from the folder and try again until it does.

Now, once you are back at the main menu you will see the headers changed again to the following:
```
Proof of Concept
Coronel Steam Downloader
CSDG File found: True <-----
Current AppID: LOAD .CSDG!
Logged in: True
```

#### 3. Load the .csdg

Option 4 will load the .csdg the part above found, the headers will change to the following:
```
Proof of Concept
Coronel Steam Downloader
CSDG File found: True
Current AppID: 480 <----- This will be the AppID of the .csdg you loaded
Logged in: True
```

#### 4. Downloading the Depot/game

Option 6 will display the numbers of files to download and a notice, press enter once you read it.

```
Selection (number): 6
Number of files to download: 8
You might see permission errors; if they occur while making a directory/folder, there is nothing to worry about
Press enter to start downloading files...
```
Ultimately, the console should look like this if you did everything right:

```
Downloading DejaVuSans.txt...
File DejaVuSans.txt saved successfully.
Downloading sdkencryptedappticket.dll...
File sdkencryptedappticket.dll saved successfully.
Downloading DejaVuSans.ttf...
File DejaVuSans.ttf saved successfully.
Downloading installscript.vdf...
File installscript.vdf saved successfully.
Downloading steam_api.dll...
File steam_api.dll saved successfully.
Downloading SteamworksExample.exe...
File SteamworksExample.exe saved successfully.
Downloading controller.vdf...
File controller.vdf saved successfully.
Downloading D3D9VRDistort.cso...
File D3D9VRDistort.cso saved successfully.
Game Downloaded!
Press any key to continue
```

#### 5. Check the game

If you see the folder with the script inside there will be a new folder with the name '480' in our case, inside it is the game.


## Demo - Making a .csdg

#### 1. Logging with an account that owns the game

Option 1, insert you username and password, the Steam Guard code needs the app, you can find the code in the Shield Section, in the bottom left.
The console headers will change to the following if it was done correctly:
```
Proof of Concept
Coronel Steam Downloader
CSDG File found: False
Current AppID: LOAD .CSDG!
Logged in: True <-----
```

#### 2. Making the .csdg

Because different games use different data, I can't tell you exactly what to do...
But I will use Buckshot Roullete this this example. Using SteamDB.info to fill the data.

Option 5 will require AppID, DepotID and ManifestID, all of them can be found in the steamdb page of the game, in my case Buckshot Roullete has the following:

- AppID: 2835570
- DepotID: 2835572
- ManifestID (Lastest Version as of 9/2/2024): 9096719631701850389

#### But didn't we need the manifest and DepotKey?
Yes, but the script will get them automatically from steam.
#### I own the game but it failed getting the DepotKey
Try again... Sometimes it does that, will be fixed in the next version.

If everything was successful the console will look like this:

```
Selection (number): 5
This function assumes you are logged with an account that owns the game
Use SteamDB to avoid errors
AppID: 2835570
DepotID: 2835572
ManifestID: 9096719631701850389
Made .csdg!
Press any key to continue
```

Your .csdg is on the same folder the script is! You can download it using Demo - Pre-Made .csdg

You need to 'find' the .csdg using Option 3 before you can download the game with your new .csdg, but I recomment you exit it and then log (You can do it Anonymously now since you have the .csdg) and follow the Demo - Pre-Made .csdg part as sometimes the script gets funny after making the .csdg

## Demo - Errors while downloading...

Now, as the warning reads there might be some errors while making directories, they don't matter at all, but here is a console output with some of them for you to compare to yours:

```
Selection (number): 6
Number of files to download: 12
You might see permission errors; if they occur while making a directory/folder, there is nothing to worry about
Press enter to start downloading files...
Downloading Buckshot Roulette_windows\Original Soundtrack\You are an Angel.wav...
File Buckshot Roulette_windows\Original Soundtrack\You are an Angel.wav saved successfully.
Downloading Buckshot Roulette_windows...
Permission error while saving file Buckshot Roulette_windows: [Errno 13] Permission denied: '2835570/Buckshot Roulette_windows' <----- This is a directory, this doesn't matter
Downloading Buckshot Roulette_windows\Original Soundtrack\General Release.wav...
File Buckshot Roulette_windows\Original Soundtrack\General Release.wav saved successfully.
Downloading Buckshot Roulette_windows\Original Soundtrack\70K.wav...
File Buckshot Roulette_windows\Original Soundtrack\70K.wav saved successfully.
Downloading Buckshot Roulette_windows\steam_api64.dll...
File Buckshot Roulette_windows\steam_api64.dll saved successfully.
Downloading Buckshot Roulette_windows\Original Soundtrack\Blank Shell.wav...
File Buckshot Roulette_windows\Original Soundtrack\Blank Shell.wav saved successfully.
Downloading Buckshot Roulette_windows\Original Soundtrack\cover.png...
File Buckshot Roulette_windows\Original Soundtrack\cover.png saved successfully.
Downloading Buckshot Roulette_windows\Original Soundtrack...
Permission error while saving file Buckshot Roulette_windows\Original Soundtrack: [Errno 13] Permission denied: '2835570/Buckshot Roulette_windows\\Original Soundtrack' <----- This is a directory, this doesn't matter
Downloading Buckshot Roulette_windows\Original Soundtrack\Before Every Load.wav...
File Buckshot Roulette_windows\Original Soundtrack\Before Every Load.wav saved successfully.
Downloading Buckshot Roulette_windows\Buckshot Roulette.exe...
File Buckshot Roulette_windows\Buckshot Roulette.exe saved successfully.
Downloading Buckshot Roulette_windows\Original Soundtrack\Socket Calibration.wav...
File Buckshot Roulette_windows\Original Soundtrack\Socket Calibration.wav saved successfully.
Downloading Buckshot Roulette_windows\Original Soundtrack\Monochrome LCD.wav...
File Buckshot Roulette_windows\Original Soundtrack\Monochrome LCD.wav saved successfully.
Game Downloaded!
Press any key to continue
```



## Support

For support, contact me via reddit, u/whitecoronel.


## Contributing

Contributions are always welcome!
Please contact me on reddit (u/whitecoronel) or make a pull request or something.


## License

GNU General Public License v3.0

I dont want close source versions as the whole point of making this script was for it to be 100% open-source, for more information about GNU V3 please check the following website: https://choosealicense.com/licenses/gpl-3.0/

