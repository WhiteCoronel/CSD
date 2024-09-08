import Functions
import pprint
import importlib
import os

dump = Functions.dump
CSD = Functions.CSD
auto_make_csdg = Functions.auto_make_csdg
pprint = pprint.pprint

csd_exits = False

def Console():
    while True:
        command = input(f"CSD: {csd_exits} | Command (INSECURE): ")

        if command == 'exit':
            break
        elif command == 'cls':
            os.system('cls')
        else:
            try:
                eval(command)
            except Exception as e:
                print(f'Error while running command: {command} Exeption: {e}')

def ReloadModules():
    importlib.reload(Functions)
    global CSD, auto_make_csdg
    CSD = Functions.CSD
    auto_make_csdg = Functions.auto_make_csdg
    dump = Functions.dump
    print('Remember to use SetCSD to apply changes to update current csd variable with the modified class')
    print('You will have to Re-Log')

def SetCSD():
    try:
        global csd, csd_exits
        csd = CSD()
        csd_exits = True
    except Exception as e:
        print(f'Error setting CSD: {e}')

def CheckCSD():
    global csd_exits
    try:
        csd.logged
        print('CSD exits...')
        csd_exits = True
    except Exception as e:
        csd_exits = False
        print("CSD doesn't exits...")

