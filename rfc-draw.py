# 1232, Wed 28 Sep 2022 (NZDT)
# 1603, Sun  1 Oct 2023 (NZDT)
# 1613, Sat 21 Oct 2023 (NZDT)
#
# rfc-draw: Nevil's tkinter program to draw images for SVG-RFC-1.2 diagrams
#
# Copyright 2023, Nevil Brownlee, Taupo NZ

import sys
from tkinter import *  # Different behaviour than 'import tkinter as tk' !!!
from tkinter.messagebox import askyesno

import r_buttons_class as rbc

import rfc_draw_globals_class as rdgc  # rfc-draw globals and functions

import draw_n_rects_class as drc  # Handles n_rect objects
import draw_lines_class as dlc    # Handles line objects
import draw_texts_class as dtc    # Handles text objects
import draw_groups_class as dgr   # Handles rfc-draw groups

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
    #print("@@@ r_buttons_handler: %s" % obj.b_current)
    global previous, save_file_name
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
    elif obj.b_current == "group":
        #print("'group' pressed")
        rdg.set_mode('group')
        dgr_tool.set_event_handlers()
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

rdg = rdgc.rdglob(d_canvas.drawing, root, d_canvas.m_text)   # rfc-draw globals

if len(sys.argv) == 2:
    save_file_name = sys.argv[1]
    if sys.argv[1][-4:] != ".rdd":
        print("\a\aExpected to Save to an .rdd file <<<")
else:
    save_file_name = None
    from tkinter.filedialog import askopenfilename
    save_file_name = (askopenfilename(title="Select .rdd file; cancel box if none"))
    if not save_file_name:    
        save_file_name = "save-file.rdd"
        rdg.display_msg("No file %s, will write it on closing" % save_file_name,
        "warning")

dlc_tool = dlc.draw_lines(d_canvas.drawing, root, rdg)
    # sets draw_lines ln_b1 handlers

drc_tool = drc.draw_n_rects(d_canvas.drawing, root, rdg)
drc_tool.set_event_handlers()  # We start up in Rectangle mode
rdg.set_mode('rect')
last_mode = "rect"

dtc_tool = dtc.draw_texts(d_canvas.drawing, root, rdg)
    # sets draw_texts tx_b1 handlers

dgr_tool = dgr.draw_groups(d_canvas.drawing, root, rdg)

rdg.read_from_rdd(save_file_name)

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
