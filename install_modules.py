# 1621, Sun  9 Mar 2025 (NZDT)
#
# test-modules.py: Check that all the python modules rfc-draw needs
#   are installed
#
# Copyright 2025, Nevil Brownlee, Taupo NZ

import importlib

all_installed = True
def module_installed(module_name):
    try:
        importlib.import_module(module_name)
        return True
    except:
        all_installed = False
        return False

if not module_installed("sys"):
    print("python 'sys' module not installed, install it as follows:")
    print("    pip3 install sys")
    exit()
import sys

if sys.platform == "win32":
    print("System is Windows")
    if not module_installed("msvcrt"):
        importlib.import_module("msvcrt")
elif sys.platform == "darwin":
    print("System is macOS")
    if not module_installed("termios"):
        importlib.import_module("termios")
elif sys.platform == "linux":
    print("System is Linux")
    if not module_installed("termios"):
        importlib.import_module("termios")

module_names = ["os", "pathlib", "re", "math", "sys", "time",
                "datetime", "threading", "tkinter", "pygame"]


for mn in module_names:
    if not module_installed(mn):
        all_installed = False
        print(">>> %s not installed" % mn)
        importlib.import_module(mn)
