# 1657, Tue 23 Apr 2024 (NZST)
# 1605, Mon  1 Jan 2024 (NZDT)
# 1613, Sat 21 Oct 2023 (NZDT)
# 1603, Sun  1 Oct 2023 (NZDT)
# 1232, Wed 28 Sep 2022 (NZDT)
#
# rfc-draw: Nevil's tkinter program to draw images for SVG-RFC-1.2 diagrams
#
# Copyright 2024, Nevil Brownlee, Taupo NZ

import sys
from pathlib import Path
from tkinter import *  # Different behaviour than 'import tkinter as tk' !!!
from tkinter.messagebox import askyesno
try:
    posix = True
    import termios  # This is POSIX
except:
    posix = False
    import msvcrt   # This is Windows
    
import r_buttons_class as rbc

import rfc_draw_globals_class as rdgc  # rfc-draw globals and functions

import draw_n_rects_class as drc  # Handles n_rect objects
import draw_lines_class as dlc    # Handles line objects
import draw_texts_class as dtc    # Handles text objects
import draw_headers_class as dhc   # Handles pkt header objects

root = Tk()  # Main window
root.title("RFC-draw")
root.geometry('800x600+5+5')
root.resizable(True, True)

class RFC_Canvas(Canvas):  # Base Class Name
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self,parent, **kwargs)
        #print("RFC_Canvas: kwargs >%s<" % kwargs)
        self.bind("<Configure>", self.on_resize)
        self.w_height = self.winfo_reqheight()
        self.w_width = self.winfo_reqwidth()

    def on_resize(self, event):
        d_canvas.drawing.config(width=event.width-18, height=event.height-69)
        d_canvas.r_buttons.b_frame.place(x=9, y=event.height-52)
        x_empty = event.width-330  # Width of empty space on buttons line
        new_width = int(x_empty*0.92)
        d_canvas.message.config(width=new_width)
        d_canvas.message.place(
            x=event.width-new_width-8, y=event.height-47)

d_canvas = RFC_Canvas(root, width=800, height=600, bg="lightgrey",
    highlightthickness=0)
d_canvas.pack(fill=BOTH, expand=1)

def r_buttons_handler(obj):
    global previous, save_file_name
    #print("@@@ r_buttons_handler: b_current = %s" % obj.b_current)
    if obj.b_current == "rect":
        #print("'rect' pressed")
        rdg.set_mode('rect')
        drc_tool.set_event_handlers()
    elif obj.b_current == "line":
        #print("'line' pressed")
        rdg.set_mode('line')
        dlc_tool.set_event_handlers()
    elif obj.b_current == "text":
        #print("'text' pressed")
        rdg.set_mode('text')
        dtc_tool.set_event_handlers()
    elif obj.b_current == "header":
        #print("'header' pressed")
        rdg.set_mode('header')
        dhc_tool.set_event_handlers()
    elif obj.b_current == "save":
        #print("'save' pressed, previous = %s" % previous)
        rdg.unbind_keys()
        get_save_filename()
        d_canvas.m_text.wait_variable(twv)  # Wait for ESC key
        #print("Save: save_file_name = >%s<" % save_file_name)
        rdg.bind_keys()
        rdg.save_to_rdd(save_file_name)
        d_canvas.r_buttons.change_current(previous)
        rdg.set_mode(previous)
        obj.b_current = previous
    else:
        print("\aUnrecognised button >%s< pressed" % obj.b_current)
    previous = obj.b_current

d_canvas.r_buttons = rbc.r_buttons("r_buttons", d_canvas)
d_canvas.r_buttons.func_on_press = r_buttons_handler
d_canvas.r_buttons.b_frame.place(x=9, y=548)

twv = IntVar()  # tkinter wait.variable() for msg_esc_key
previous = "rect"

def msg_esc_key(event):
    global save_file_name, tkw
    sf_name = d_canvas.m_text.get('1.0','end-1c')
    sfa = sf_name.split(": ")
    save_file_name = sfa[1]
    d_canvas.m_text.delete("1.0","end")
    #print("Esc: save_file_name = >%s<" % save_file_name)
    twv.set(1)

def get_save_filename():
    global save_file_name, tkw
    sf_name = d_canvas.m_text.get(1.0, "end-1c")
    d_canvas.m_text.delete('1.0', END)
    d_canvas.m_text.insert('1.0', "Save to: %s" % save_file_name)
    d_canvas.m_text.focus_set()
    d_canvas.m_text.bind('<Escape>', msg_esc_key)

d_canvas.drawing = Canvas(d_canvas, width=782, height=530,
    bg="white")  # Drawing area
d_canvas.drawing.place(x=8, y=8)

#d_canvas.message = Frame(d_canvas, height=35, width=450,
d_canvas.message = Frame(d_canvas, height=35, width=500,
    bg="azure")  # Message area, dynamically set in on_resize() above

#d_canvas.message.place(x=316, y=552)
d_canvas.message.place(x=255, y=552)
d_canvas.message.update()
#print("message width %d" % d_canvas.message.winfo_width())

d_canvas.m_text = Text(d_canvas.message, fg="black", bg="azure",
    font=("TkFixedFont 12"), bd=0, highlightthickness=0)  # No border
d_canvas.m_text.place(x=7, y=7)

save_file_name = "save-file.rdd"
if not posix:
    from tkinter.filedialog import askopenfilename
    f_name = (askopenfilename(
        title="Select .rdd file; cancel box if none"))
        # cancel returns an empty (0-length)  tuple
    if len(f_name) != 0:
        save_file_name = f_name
else:  # POSIX
    #print("len(sys.argv) %d, argv >%s<" % (len(sys.argv), sys.argv))
    if len(sys.argv) == 2:  # save_file specified
        save_file_name = sys.argv[1]
        if sys.argv[1][-4:] != ".rdd":
            print("\a\aExpected to Save to an .rdd file <<<")

rdg = rdgc.rdglob(d_canvas.drawing, root, d_canvas.m_text)
    # Starts running rfc-draw !!!

dlc_tool = dlc.draw_lines(d_canvas.drawing, root, rdg)
drc_tool = drc.draw_n_rects(d_canvas.drawing, root, rdg)
dtc_tool = dtc.draw_texts(d_canvas.drawing, root, rdg)
dhc_tool = dhc.draw_headers(d_canvas.drawing, root, rdg)

print("about to start, save_file_name %s" % save_file_name)
sfp = Path(save_file_name)
last_mode = "rect"
last_mode = rdg.read_from_rdd(save_file_name)  # Reads the save_file
"""
if sfp.is_file():
    last_mode = rdg.read_from_rdd(save_file_name)
    # Reads the save_file
    ##??dhc.draw_headers.wait_for_input(rdg, "save-file.rdd read <<<")
else:
    print("no file %s" % save_file_name)
"""
rdg.set_mode('rect')  # We start with mode = 'rect'
drc_tool.set_event_handlers()

if last_mode != 'rect':
    #print("about to change_current")
    d_canvas.r_buttons.change_current(last_mode)  # Change mode to last_mode

def on_closing():
    response = askyesno("Save drawing as .rdd?")
    if response:  # True/False
        print("Saving drawing")
        rdg.save_to_rdd(save_file_name)
    else:
        print("Closed without saving as .rdd")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
