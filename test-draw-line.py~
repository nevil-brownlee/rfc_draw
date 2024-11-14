# 1548, Wed 13 Mar 2024 (NZDT)
#
# test-item-creating.py  Try to understand how item ids are created,
#                        when items are deleted and re-created
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
#d_canvas.message = tk.Frame(d_canvas, height=60, width=500,
#    bg="azure")
#d_canvas.message.place(x=50, y=50)
#d_canvas.message.update()

#s =  "123456789012345678901234567890\n"  # \n marks end of line
#s2 = "         0         0         0"

fx_font = "TkFixedFont"  # This works (below) to set canvas.m_text !!!

#d_canvas.m_text = tk.Text(d_canvas.message, fg="black", font=fx_font)
#d_canvas.m_text.place(x=7, y=7)
#d_canvas.m_text.delete('1.0', tk.END)
#d_canvas.m_text.insert('1.0',  s)
#d_canvas.m_text.update()
#d_canvas.m_text.insert('2.0', s2)
#d_canvas.m_text.update()

#print("actual returned %s" % font.actual())
   # > {'family': 'DejaVu Sans', 'size': 12, 'weight': 'normal', ...
   # > Clearly tkinter uses "DejaVu Sans 12" for TkFixedFont!

x0 = 200;  y0 = 50

text_id = d_canvas.create_text([x0, y0], text="abcdefghi")
time.sleep(3)

y0 = 100
d_canvas.coords(text_id, 200,100)



"""
t_ids = [];  l_ids = []

def draw_line(j):
    y = 5+j*20
    text_id = d_canvas.create_text([10, y], text="%3d" % j)
    t_ids.append(text_id)
    line_id = d_canvas.create_line([40, y, 300, y], width=3)
    l_ids.append(line_id)
    print("j %d, text id %d, line id %d" % (j, text_id, line_id))
       
for j in range(0,19):
    draw_line(j)

for j in range(20,39):
    draw_line(j)
    
for j in range(0,19):
    d_canvas.destroy(t_ids[j]);  d_canvas.destroy(l_ids[j])

for j in range(0,19):
    draw_line(j)

# Looks as though item ids just keep incrementing :-)

s_width = font.measure(s[0:-2])  # tk units, int
s_height = font.metrics("linespace")  # tk units, int

#print("width %s, len %s %s, size %s, height %s" % (
#    s_width, len(s)-1, type(s_width), s_size, s_height))
print("len %s, width %s (%s), height %s" % (
    len(s)-1, s_width, type(s_width), s_height))

c_width = float(s_width)/(len(s)-1)
print("s1 c_width %.3f %s" % (c_width, type(c_width)))
c_width = float(s_width)/(len(s2))
print("s2 c_width %.3f %s" % (c_width, type(c_width)))
"""

print("waiting for input <<<")
input()
