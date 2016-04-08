#import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], 
                     "excludes": ["tkinter"], 
                     #"include_files": ["F:\Python27\Lib\site-packages\selenium"]
                    "include_files": [
                        ("C:\\Python34\\Scripts\\chromedriver.exe", "./chromedriver.exe"),
                        ("C:\\Python34\\Scripts\\IEDriverServer.exe", "./IEDriverServer.exe"),
                        #("e:\\home\\jimzs\\workspace\\myrta\\myrta\\settings.ini", "./settings.ini"),
                        #("e:\\home\\jimzs\\workspace\\myrta\\myrta\\task.csv", "./task.csv"),
                        ("e:\\home\\jimzs\\workspace\\myrta\\myrta\\settings2.ini", "./settings2.ini"),
                        ("e:\\home\\jimzs\\workspace\\myrta\\myrta\\candidate.csv", "./candidate.csv"),
                        ]
#                       "create_shared_zip": False,
                     }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

setup(  name = "MyDate",
        version = "0.1",
        description = "My RTA!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("MyrtaDate.py", base=base)])
