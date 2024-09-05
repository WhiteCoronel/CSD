# Verify that the file isn't run as main
if __name__ == "__main__":
    print(f'{__file__} is not the file that contains the program main loop, check repo...')
    input('Press any key to continue...')
    exit()