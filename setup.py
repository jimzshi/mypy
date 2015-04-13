#import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], 
                     "excludes": ["tkinter"], 
                    "include_files": [("C:\Python27\Lib\site-packages\selenium\webdriver\\firefox\webdriver.xpi", "./webdriver.xpi"),
                                     ("C:\Python27\Lib\site-packages\selenium\webdriver\\firefox\webdriver_prefs.json", "./webdriver_prefs.json"),
                                     ("C:\\Users\\jzs\\\Documents\\Visual Studio 2013\\Projects\\myrta\\settings.ini", "./settings.ini"),
                                     ("C:\\Users\\jzs\\\Documents\\Visual Studio 2013\\Projects\\myrta\\task.csv", "./task.csv"),
                                     ]
#                       "create_shared_zip": False,
                     }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

setup(  name = "myrta",
        version = "0.1",
        description = "My RTA!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("webdriver.py", base=base)])
