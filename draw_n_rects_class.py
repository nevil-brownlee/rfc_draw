# 1621, Thu 26 Jan 2023 (NZDT)
# 1545, Thu  8 Dec 2022 (NZDT)
#
# draw_n_rects_class: functions to draw/move/edit n_rect objects
#
# Copyright 2023, Nevil Brownlee, Taupo NZ

import tkinter as tk
#import tkinter.font

class draw_n_rects:  # rectangle+text objects for rfc-draw
    # ??? rdg = None  # Class variable

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)  # New instance of text_info

    def __init__(self, parent, root, rd_globals):
        super().__init__()
        self.drawing = parent;  self.root = root
        self.rdg = rd_globals
        self.rdg.region = None
        #self.rdg.display_msg("Starting in Rectangle mode", 'normal')
        #self.rdg.display_msg("Starting in Rectangle mode", 'error')

    def set_event_handlers(self):
        # Click b1 to make an object
        self.drawing.bind_class('Canvas','<ButtonPress-1>',  self.nr_b1_click)
        self.drawing.bind_class('Canvas','<Button1-Motion>', self.nr_b1_motion)
        self.drawing.bind_class('Canvas','<ButtonRelease-1>',self.nr_b1_release)

    def nr_closest(self, mx,my):
        item = self.drawing.find_closest(mx,my)
        if len(item) == 0:  # Empty tuple
            print("rn_closest(): empty tuple")
            return None, None
        item_x = item[0]
        item_type = self.drawing.type(item_x)
        print("@nr@ closest(): item_x = %s (%s), mx,my %d,%d" % (
            item, item_type, mx,my))
        if item_type != "rectangle":
            return None, None

        #self.rdg.dump_objects("in  nr_closest()")
 
        obj = self.rdg.objects[item_x]  # item_x is a tkinter object id
        if obj:  # object (e.g. nro) has: key, obj, obj_ type, in_n_rect
            print("-> closest %s is in objects, obj >%s<" % (item, obj))
            return item, obj
        else:  # Not in objects, assume it's an arrowhead line
            print("@@@ line %d is not in rdg.objects <<<<" % item_x)
            return None, None

    def new_n_rect(self, x0,y0, x1,y1, r_text, g_nbr):
        #self.rdg.dump_objects("new_n_rect start **************")
        if not x1:
            x1 = x0+3; y1 = y0+3
        #print("new_n_rect, %d,%d, %d,%d" % (x0,y0, x1,y1))
        r_coords = (x0,y0, x1,y1)
        #print("new_n_rect, r_coords ", end=""); print(r_coords)
        nro = self.rdg.n_rect(self.rdg, self.drawing, r_coords, r_text, g_nbr)
        #print("new_n_rect: %d,%d, %d,%d" % (nro.x0,nro.x1, nro.x1,nro.y1))

        #print("new_n_rect: nro %s; rect_id %d, text_id %d <<<" % (
        #    nro, nro.rect_id, nro.text_id))
        self.rdg.current_object =  self.rdg.object(
            nro.rect_id, nro, "n_rect", r_coords, r_text, 0, 0)
        self.rdg.objects[nro.rect_id] = self.rdg.current_object
        self.rdg.objects[nro.text_id] = self.rdg.object(
            nro.text_id, nro.text_id, "text", r_coords, r_text, 0, nro.rect_id) 
        #print("new_n_rect: ", end="");  nro.print_n_rect()
        #self.rdg.dump_objects("new_n_rect()")

    # IMPORTANT: b1_click sets self.rdg.current_object (which includes it's key)
    #   b1_motion and b1_release all work on rdg.current_object

    def nr_b1_click(self, event):  # B1 (left button) to select an object
        mx, my = (event.x, event.y)  # Mouse position

        #print(". . . nr_b1_click: %s mode, %d,%d, %d objects, %s, %s" % (
        #    self.rdg.ln_mode, mx, my, len(self.rdg.objects), 
        #       event.widget, event.type)) 

        item, obj = self.nr_closest(mx,my)  # Closest tk object
        #print("b1_click(): closest returned item %s, obj %s" % (item, obj))
        if not item:  # Empty tuple, nothing drawn yet
            #print("new_rect, n_objs = %d" % len(self.rdg.objects))
            self.new_n_rect(mx,my, None,None, " + ", 0)  # sets current_object
            #self.rdg.dump_objects("draw_n_rects")
        else:
            item_ix = item[0]
            if obj.o_type == "n_rect":
                #print("item-ix %d: " % item_ix, end="")
                obj.object.print_n_rect()
                rect_id = obj.object.rect_id
                text_id = obj.object.text_id
                #print("Clicked near n_rect %d, text_id %d" % (
                #    rect_id, text_id))
            elif obj.o_type == "text" and obj.in_n_rect != 0:
                obj = self.objects[obj.in_n_rect]
                #print("Found enclosing n_rect, obj = %s" % obj)

            #print("closest tk object: >%s< (%s)" % (item_ix, obj.o_type))

            coords = self.drawing.coords(item_ix)
            #print("   coords %s" % coords)
            #self.rdg.dump_objects("nr_b1_click()")

            #print("- - nr_b1_click() - -")
            if obj.o_type == "n_rect":
                self.rdg.current_object = obj
                #print("current_obj = %s" % obj)
                self.rdg.region = self.rdg.where(
                    self.rdg.current_object.object, mx,my)
                #print("+++  %d,%d: self.region = %d" % (mx,my, self.rdg.region))

                if self.rdg.region == self.rdg.far:  # Start new rectangle
                    self.new_n_rect(mx,my, mx,my, "-+-")
                        # Changes current_obj to new rectangle
                else:
                    gt = self.drawing.gettags(item)
                    #print("gt %s (%s)" % (gt, type(gt)))
                    for tag in gt:  # Check its tags
                        if tag.startswith('rect'):
                            #print('  You clicked near {tag}')
                            self.rdg.last_tag = tag
            else:
                self.rdg.current_object = obj
                print("\a==> Can't move a '%s' in '%s' mode" % (
                    obj.o_type, self.rdg.ln_mode))

        self.rdg.last_mx = mx;  self.rdg.last_my = my  # Last mouse position
                
    def nr_b1_motion(self, event):  # Move the current_object
        mx, my = (event.x, event.y)
        dx = mx-self.rdg.last_mx;  dy = my-self.rdg.last_my
        #print("++b1_m deltas %d,%d" % (dx,dy))
        if self.rdg.current_object == None:  # No current_object yet!
            return
        if self.rdg.current_object.o_type == "n_rect":
            #nro = self.rdg.current_object.object
            #print("b1_m: mx %d,%d  x0 %d,%d, x1 %d,%d, dx %d,%d" % (
            #    mx,my, nro.x0,nro.y0, nro.x1,nro.y1, dx,dy))
            r_coords = self.rdg.current_object.object.bbox()
            #print("b1_motion: dr_coords >%s<, region %d" % (
            #    r_coords, self.rdg.region))
            x0,y0, x1,y1 = self.rdg.move_deltas(r_coords, dx,dy)
            #print("=== %d,%d, %d,%d" % (x0,y0, x1,y1))
            self.rdg.current_object.object.coords(
                x0,y0, x1,y1)  # Resize/Move rect + text
        self.rdg.last_mx = mx;  self.rdg.last_my = my  # Last mouse position

    def nr_b1_release(self, event):  # Left button released
        mx, my = (event.x, event.y)  # Mouse position
        #print("$$$ current_object = %s" % self.rdg.current_object)
        # >>> if self.rdg.current_object.o_type != "n_rect":
        # >>>    self.rdg.dump_objects("nr_b1_release")
        self.rdg.last_mx = mx;  self.rdg.last_my = my  # Last mouse position

if __name__ == "__main__":
    root = tk.Tk()  # Main window
    drawing = tk.Canvas(root, width=600, height=600, bg="white")  # Drawing area
    drawing.pack(padx=10, pady=10)
    dto = draw_text_object(drawing, root)
    root.mainloop()
