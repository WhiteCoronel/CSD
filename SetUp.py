# Verify that the file isn't run as main
if __name__ == "__main__":
    print(f'{__file__} is not the file that contains the program main loop, check repo...')
    input('Press any key to continue...')
    exit()

import importlib.util
import subprocess
import sys
import os
from typing import List, Dict

def SetUp_verify_and_install_dependencies(dependencies: List[str]) -> Dict[str, bool]:
    """
    Verifies if the required dependencies are installed, and installs them if they are not.

    Args:
        dependencies (List[str]): A list of dependency names to check and install if missing.

    Returns:
        Dict[str, bool]: A dictionary where the keys are dependency names and the values are booleans
                         indicating whether the dependency is installed (True) or not (False).
    """
    results = {}
    for dep in dependencies:
        spec = importlib.util.find_spec(dep)
        if spec is None:
            results[dep] = False
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
                results[dep] = True
            except subprocess.CalledProcessError:
                pass
        else:
            results[dep] = True
    return results

def SetUp_Directories(directories: List[str]) -> None:
    """
    Sets up the necessary directories from a list if they do not exist.

    Args:
        directories (List[str]): A list of directory paths to create.
    """
    for dir_path in directories:
        try:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        except OSError as e:
            void()

def void():
    void = 'void'
    # Basically a placeholder for when i decide to implement logs