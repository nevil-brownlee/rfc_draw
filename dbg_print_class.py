# 1509, Sun  2 Feb 2025 (NZDT)
#
# dbg_print_class.py: Debug print utility for rdd_to_* programs
#
# Copyright 2025, Nevil Brownlee, Taupo NZ

class dbp:
    def __init__(self):
        self.debug = False  # global variable

    def db_print(self, txt):
        print("$$$ rdd_io.dbg_print")
        if self.debug:
            print(txt)
