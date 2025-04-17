# 1527, Wed  8 Mar 2023 (NZDT)
# 1659, Sun 16 Oct 2022 (NZDT)
#
# r_buttons_class: Nevil's radio buttons
#
# Copyright 2023, Nevil Brownlee, Taupo NZ

from tkinter import *

def button_press_handler(obj):
    print('empty handler for id={}'. format(obj.the_id))

class r_buttons:
    def __init__(self, the_id, root):
        self.the_id = the_id
        self.root = root
        self.b_current = "rect"

        self.func_on_press = button_press_handler
        #self.func_on_release = default_empty_event_handler

        self.b_frame = Frame(root, bg="yellow")
        self.b_frame.place(x=50, y=5)

        self.b_rect = Button(self.b_frame, text="Rectangle", relief=SUNKEN,
            padx=6, pady=6)
        self.b_rect.grid(row=0, column=0, padx=6, pady=6)
        self.b_rect.configure(command=self.b_rect_pressed)

        self.b_line = Button(self.b_frame, text="Line", padx=6, pady=6)
        self.b_line.grid(row=0, column=1, padx=6, pady=6)
        self.b_line.configure(command=self.b_line_pressed)

        self.b_text = Button(self.b_frame, text="Text", padx=6, pady=6)
        self.b_text.grid(row=0, column=2, padx=6, pady=6)
        self.b_text.configure(command=self.b_text_pressed)

        self.b_header = Button(self.b_frame, text="Header", padx=6, pady=6)
        self.b_header.grid(row=0, column=3, padx=6, pady=6)
        self.b_header.configure(command=self.b_header_pressed)

        self.b_save = Button(self.b_frame, text="Save", padx=6, pady=6)
        self.b_save.grid(row=0, column=4, padx=6, pady=6)
        self.b_save.configure(command=self.b_save_pressed)

        self.ba = {"rect":self.b_rect, "line":self.b_line, "text":self.b_text,
                   "header":self.b_header, "save":self.b_save}

        self.bp = {"rect":self.b_rect_pressed, "line":self.b_line_pressed,
                   "text":self.b_text_pressed,
                   "header":self.b_header_pressed, "save":self.b_save_pressed}

    def b_rect_pressed(self):
        #print("Rectangle pressed, current %s" % self.b_current)
        self.b_rect.configure(relief=SUNKEN)
        self.raise_button(self.b_current)
        self.b_current = "rect"
        self.func_on_press(self)

    def b_line_pressed(self):
        #print("Line pressed, current %s" % self.b_current)
        self.b_line.configure(relief=SUNKEN)
        self.raise_button(self.b_current)
        self.b_current = "line"
        self.func_on_press(self)

    def b_text_pressed(self):
        #print("Text pressed, current %s" % self.b_current)
        self.b_text.configure(relief=SUNKEN)
        self.raise_button(self.b_current)
        self.b_current = "text"
        self.func_on_press(self)

    def b_header_pressed(self):
        #print("Header pressed, current %s" % self.b_current)
        self.b_header.configure(relief=SUNKEN)
        self.raise_button(self.b_current)
        self.b_current = "header"
        self.func_on_press(self)

    def b_save_pressed(self):
        #print("Save pressed, current %s" % self.b_current)
        self.b_save.configure(relief=SUNKEN)
        self.raise_button(self.b_current)
        self.b_current = "save"
        self.func_on_press(self)

    def raise_button(self, b_name):
        #print("b_name >%s<, self.ba = %s" % (b_name, self.ba))
        b = self.ba[b_name]
        #print("raise %s: b = %s (%s)" % (b_name, b, type(b)))
        b.configure(relief=RAISED)

    def trigger_on_press(self):
        self.func_on_press(self)  # Pass 'self' as argument to the function

    def change_current(self, b_name):  # Switch to button b_name
        #print("&&& change_current b_name >%s<" % b_name)
        self.bp[b_name]()

if __name__ == "__main__":
    root = Tk()
    root.geometry("600x600")

    rbc = r_buttons("Test r_buttons_class", root)

    def custom_handler(obj):
        print("custom handler for id %s, b_current %s" % (
            obj.the_id, obj.b_current))
        print("- - - - -")

    rbc.func_on_press = custom_handler

    rbc.b_frame.place(x=200, y=300)  # Position the frame where we want it

    b_names =  ["rect", "text", "line", "header", "save"]
    b = 3

    def change_button():
        global b
        b = (b+1) % 4
        b_name = b_names[b]
        #print("b = %d, %s" % (b, b_name))
        rbc.change_current(b_name)
        Tk().after(2000, change_button)
 
    Tk().after(0, change_button)
    root.mainloop()
