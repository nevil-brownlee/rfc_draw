# 1036, Fri  3 Nov 2023 (NZDT)
#
# rdd_globals: globals for rfc-draaw's rdd-to*.py programs
#
# Copyright 2023, Nevil Brownlee, Taupo NZ

class rdd_globals:
    def __init__(self):
        self.asc_def_b_w = 1  # border_width chars/lines
        self.svg_def_b_w = 3  #              pixels
        self.asc_x_sf = 1.5   # (old) ascii x scale factor
        self.asc_y_sf = 1.0   #
        self.hdr_x_sf = 0.99  # ascii x sf for header/row/field -> n_chars 67
        self.hdr_y_sf = 1.0   # ascii y sf   -> n_lines 7 (for test-h1r2.rdd)
 
gv = rdd_globals()  # rdd global variables
