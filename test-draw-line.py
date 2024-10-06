# 1610, Tue 23 May 2024 (NZDT)
#
# test-draw-line.py  # Test drawing dashed lines
#
# Copyright 2024, Nevil Brownlee, Taupo NZ

import tkinter as tk, time
import tkinter.font

root = tk.Tk()  # Main window
root.title("RFC-draw")
root.geometry('800x600+5+5')
root.resizable(True, True)

d_canvas = tk.Canvas(root, width=600, height=250, bg="lightgrey",
    highlightthickness=0)
d_canvas.pack(expand=1)

fx_font = "TkFixedFont"  # This works (below) to set canvas.m_text !!!


x0 = 200;  y0 = 50

segments = []
segments.append( [ [200, 50, 250, 50], None] )
segments.append( [ [250, 50, 250, 80], (5,3)] )
segments.append( [ [250, 80, 275, 80], None] )

print("segments %s" % segments)
#text_id = d_canvas.create_line(x0, y0, x0+30, y0)
#time.sleep(3)

for s in segments:
    if s[1]:
        d_canvas.create_line(s[0], dash=s[1])
    else:
        d_canvas.create_line(s[0])

print("waiting for input <<<")
input()
