from SetUp import SetUp_verify_and_install_dependencies, SetUp_Directories
from dev_console import Console as InsecureConsole, SetCSD, CheckCSD, ReloadModules

dependencies = ['steam', 'rich']
directories = ['CSDG', 'Downloads', 'Logs']
SetUp_verify_and_install_dependencies(dependencies)
SetUp_Directories(directories)

InsecureConsole()