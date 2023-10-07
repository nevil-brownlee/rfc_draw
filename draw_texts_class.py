# 1648, Tue  6 Dec 2022 (NZDT)
# 1539, Sat 21 Jan 2023 (NZDT)
#
# draw_texts_class: functions to draw/move/edit tkinter text objects
#
# Copyright 2023, Nevil Brownlee, Taupo NZ

import tkinter as tk
#import tkinter.font

import rfc_draw_globals_class as rdgc

class draw_texts:  # text objects for rfc-draw
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)  # New instance of text_info

    def __init__(self, parent, root, rd_globals):
        super().__init__()
        self.drawing = parent;  self.root = root
        self.rdg = rd_globals

        self.tx_far = 6
        #self.f_font = tkinter.font.Font(  # Initialise class variables
        #    family="TkFixedFont", size=10, weight="normal")
        self.f_font = "TkFixedFont"  # This works, above version doesn't <<<
        #self.f_font = "Courier 10 bold"  # This does too
        # https://stackoverflow.com/questions/48731746/
        # how-to-set-a-tkinter-widget-to-a-monospaced-platform-independent-font

    def set_event_handlers(self):
        # Click b1 to make a create_text() object
        self.drawing.bind_class('Canvas','<ButtonPress-1>', self.tx_b1_click)
        self.drawing.bind_class('Canvas','<Button1-Motion>',self.tx_b1_motion)
        self.drawing.bind_class('Canvas','<ButtonRelease-1>',self.tx_b1_release)

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
            #print("no tk objects in drawing yet!")
            tx_str = "--" + str(len(self.rdg.objects)+1) + "--"
            text_obj = self.rdg.new_text(mx, my, tx_str, 0)
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
        self.drawing.move(self.rdg.current_object.object,
            mx-self.rdg.last_mx, my-self.rdg.last_my)
        self.rdg.last_mx = mx;  self.rdg.last_my = my  # Last mouse position

    def tx_b1_release(self, event):  # Left button released
        mx, my = (event.x, event.y)  # Mouse position
        self.rdg.last_mx = mx;  self.rdg.last_my = my

if __name__ == "__main__":
    root = tk.Tk()  # Main window
    drawing = tk.Canvas(root, width=600, height=600, bg="white")  # Drawing area
    drawing.pack(padx=10, pady=10)
    dto = draw_texts(drawing, root)
    root.mainloop()
    
