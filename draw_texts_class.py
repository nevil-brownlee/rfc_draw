# 1451, Fri  5 Jan 2024 (NZDT)
# 1539, Sat 21 Jan 2023 (NZDT)
# 1648, Tue  6 Dec 2022 (NZDT)
# 1501, Sun 19 Jan 2025 (NZDT)
#
# draw_texts_class: functions to draw/move/edit tkinter text objects
#
# Copyright 2024, Nevil Brownlee, Taupo NZ

import tkinter as tk, sys

import rfc_draw_globals_class as rdgc

class draw_texts:  # text objects for rfc-draw
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)  # New instance of text_info

    def __init__(self, parent, root, rdg):
        super().__init__()
        self.drawing = parent;  self.root = root
        self.rdg = rdg
        #print("dtc: self.rdg >%s<" % self.rdg)
        self.f_font = self.rdg.f_font
        #self.f_font = ('Space Mono', 10) #, 'bold')  # Google, r and i different
        #self.drawing.create_text( [20,20], text="dtc startup",
        #       font=self.f_font, anchor=tk.CENTER, activefill="red")
        #print("   f_font %s" % self.f_font)
        
        self.parent_id = self.v1 = self.v2 = 0
        self.text_id = None

        self.tx_far = 6
        #self.f_font = tkinter.font.Font(  # Initialise class variables
        #    family="TkFixedFont", size=10, weight="normal")
        #self.f_font = "TkFixedFont"  # This works, above version doesn't <<<
        self.f_font = self.rdg.f_font

        ###print("!@!@! dtc: f_font %s" % self.f_font)
        # https://stackoverflow.com/questions/48731746/
        # how-to-set-a-tkinter-widget-to-a-monospaced-platform-independent-font

    def set_event_handlers(self):
        # Click b1 to make a create_text() object
        self.drawing.bind_class('Canvas','<ButtonPress-1>', self.tx_b1_click)
        self.drawing.bind_class('Canvas','<Button1-Motion>',self.tx_b1_motion)
        self.drawing.bind_class('Canvas','<ButtonRelease-1>',self.tx_b1_release)
        
    def restore_object(self, t_coords, t_text, parent_id, v1, v2):
        #print("t_coords %s, t_text %s, parent_id %d, v1 %d, v2 %d" % (
        #    self.t_coords, self.t_text, self.parent_id, self.v1, self.v2))

        print("DTC.restore_object: t_coords %s, t_text >%s<, parent_id %s, v1 %s, v2 %s, self.text_id %s" % (
            t_coords, t_text, parent_id, v1, v2, self.text_id))
        self.text_id = self.rdg.add_to_layer(3, 
            self.drawing.create_text, t_coords, text=t_text,
            anchor=tk.CENTER, activefill="red",
            font=self.f_font)
        print("self.text_id  now %d" % self.text_id)
        text_obj = self.rdg.object(self.text_id, self.text_id,
            "text", t_coords, t_text, parent_id, v1, v2)
        self.rdg.objects[self.text_id] = text_obj
        self.rdg.current_object = text_obj
        #print("new_text: objects %s" % self.rdg.objects)
        return text_obj

    def undraw(self, val):  # For rdgc.on_delete_key()
        if val.key != 0:
            self.rdg.drawing.itemconfigure(val.key, state=tk.HIDDEN)
            ##self.drawing.delete(val.key)

    def redraw(self, val):  # For rdgc.on_delete_key()
        if val.key != 0:
            self.rdg.drawing.itemconfigure(val.key, state=tk.NORMAL)

    def set_background(self, colour):  # Set background colour
        # https://stackoverflow.com/questions/
        #            9408195/python-tkinter-text-background
        i = self.text_id
        r =  self.rdg.drawing.create_rectangle(w.bbox(i),fill=colour)
        self.rdg.drawing.tag_lower(r, i)

    def mk_save_str(self, val):  # Make object's rdd file entry
        #print("@@text@@ text: mk_save_str, val >%s<" % val)
        coords = []
        for c in val.i_coords:
            coords.append(round(c))
        #print("@@    @@ %s" % coords)
        str = self.rdg.drawing.itemcget(val.key, "text")
        str = str.replace("\n", "\\n")  # Escape \n chars
        str = str.replace("\"", "\\\"")  # Escape \" chars
        return "(%s %d) %s \"%s\" %s %s %s" % ("text", val.key,
            coords, str, val.parent_id, val.v1, val.v2)

    def tx_closest(self, mx,my):
        item = self.drawing.find_closest(mx,my) 
        if len(item) == 0:  # Empty tuple
            #print("rdg_closest(0): empty tuple")
            return None, None
        item_id = item[0]
        item_type = self.drawing.type(item_id)
        #print("@@@ tx_closest, item_id %d, type %s" % (item_id, item_type))
        if item_type != "text":
            return None, None
        #print("@=@ tx_closest(1): item %s (%s), mx,my %d,%d" % (
        #    item, item_type, mx,my))
        if item_id in self.rdg.objects:
            obj = self.rdg.objects[item_id]  # item_id is a tkinter object id
            # object (e.g. nro) has: key, obj, obj_ type, in_n_rect
            #print("-> closest %s is in objects, obj >%s<" % (item, obj))
            cx,cy = self.drawing.coords(item_id)  # Centre of text object
            c_text = self.drawing.itemcget(item_id, "text")
            h,w = self.rdg.str_h_w(c_text)  # 0.5 of dimensions!
            px_h = h*self.rdg.f_height;  px_w = w*self.rdg.f_width
            #print("=== mx,my %d,%d  px_w %d, px_h %d" % (mx,my, px_w,px_h))
            ##print(">H< %s" % (abs(mx-cx) > (px_w*2 + self.tx_far)/2))
            ##print(">V< %s" % (abs(my-cy) > (px_h*2 + self.tx_far)/2))
            if ( (abs(mx-cx) > (px_w*2 + self.tx_far)/2) or
                 (abs(my-cy) > (px_h*2 + self.tx_far)/2) ):
                print("\atext is too far away")
                return None, None
            #print("--- close !!!")
            return item, obj
        else:  # Not in objects ??
            #print("@@@ text %d is not in rdg.objects <<<<" % item_id)
            return None, None

    def tx_b1_click(self, event):  # B1 (left button) to create_text()
        mx, my = (event.x, event.y)  # Mouse position
        #print(". . . on_b1_click_t: %d,%d, %s, %s" % (
        #    mx, my, event.widget, event.type))        

        item, obj = self.tx_closest(mx,my)  # Closest tk object
        if item == None:
            print("no tk objects in drawing yet!")
            tx_str = "--" + str(len(self.rdg.objects)+1) + "--"
            self.restore_object([mx, my], tx_str, 0, 0, 0)
        else:
            #print("item = %s, obj = |%s|" % (item, obj))
            item_ix = item[0]
            if obj.o_type == "text":
                print("\aYou clicked near text %d" % item_ix)
                self.rdg.current_object = obj
        self.rdg.last_mx = mx;  self.rdg.last_my = my  # Last mouse position

    def tx_b1_motion(self, event):  # Move the current_obj_id
        mx, my = (event.x, event.y)
        #print("b1_motion: %d,%d" % (mx,my))
        if self.rdg.current_object == None:  # No current_object yet!
            return
        if self.rdg.current_object.o_type == "text":
            self.drawing.move(self.rdg.current_object.key,
                mx-self.rdg.last_mx, my-self.rdg.last_my)
            self.rdg.last_mx = mx;  self.rdg.last_my = my  # Last mouse position

    def tx_b1_release(self, event):  # Left button released
        mx, my = (event.x, event.y)  # Mouse position
        if self.rdg.current_object:
            self.rdg.current_object.i_coords = \
                self.drawing.coords(self.rdg.current_object.key)
            self.rdg.objects[self.rdg.current_object.key] = \
                self.rdg.current_object
        self.rdg.last_mx = mx;  self.rdg.last_my = my

if __name__ == "__main__":
    root = tk.Tk()  # Main window
    drawing = tk.Canvas(root, width=600, height=600, bg="white")  # Drawing area
    drawing.pack(padx=10, pady=10)
    message = tk.Frame(drawing, height=35, width=500, bg="azure") # Message area
    message.place(x=50, y=550)
    message.update()
    drawing.m_text = tk.Text(message, fg="black", bg="azure",
        font=("TkFixedFont"), bd=0, highlightthickness=0)  # No border
    drawing.m_text.place(x=7, y=7)

    rdg = rdgc.rdglob(drawing, root, drawing.m_text)
    dto = draw_texts(drawing, root, rdg)
    dto.set_event_handlers()
    root.mainloop()
