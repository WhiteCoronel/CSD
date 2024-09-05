from Functions import CSD, auto_make_csdg
import pprint
csd = CSD()

while True:
    command = input('Command: ')
    try:
        eval(command)
    except Exception as e:
        print(f'An error occured while running command: {command}... Error: {e}')

