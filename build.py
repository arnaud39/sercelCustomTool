"""setup.py: Used to compile with cx_freeze : python setup.py build -> exe or equivalent for your system"""
__author__ = "Arnaud Petit"

import sys
from cx_Freeze import setup, Executable
import os

if sys.platform == 'win32':
    base = 'Win32GUI'

build_exe_options = {
    'packages': [
        'sys', "os", "selenium", "time", "pyfiglet", "openpyxl", "datetime",
        "queue", "backports", 'tkinter'
    ],
    'includes': [
        'sys', "os", "selenium", "time", "pyfiglet", "openpyxl", "datetime",
        "queue", "backports", 'tkinter'
    ]
}

setup(name="Test Carte",
      version="1.0",
      description="Test Carte par Arnaud",
      options={"build_exe": build_exe_options},
      executables=[Executable("Test_carte.py"),
                   Executable("passExcel.py"),
                   Executable("cli_version.py")])
