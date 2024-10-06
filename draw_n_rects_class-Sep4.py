# 1451, Fri  5 Jan 2024 (NZDT)
# 1621, Thu 26 Jan 2023 (NZDT)
# 1545, Thu  8 Dec 2022 (NZDT)
#
# draw_n_rects_class: functions to draw/move/edit n_rect objects
#
# Copyright 2024, Nevil Brownlee, Taupo NZ

import tkinter as tk
import draw_texts_class as dtc    # Handles text objects
import rfc_draw_globals_class as rdgc

class draw_n_rects:  #  Rectangle with white fill and centred text
    # ??? rdg = None  # Class variable

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)  # New instance

    def __init__(self, parent, root, rdg):
        super().__init__()
        self.drawing = parent;  self.root = root;  self.rdg = rdg
        self.last_mx = self.last_my = None
        self.rect_id = None

    def set_event_handlers(self):
        # Click b1 to make an object
        self.drawing.bind_class('Canvas','<ButtonPress-1>',  self.nr_b1_click)
        self.drawing.bind_class('Canvas','<Button1-Motion>', self.nr_b1_motion)
        self.drawing.bind_class('Canvas','<ButtonRelease-1>',self.nr_b1_release)
        #print(">>> draw_n_rects event handlers set")
        
    def restore_object(self, r_coords, r_text, parent_id, v1, v2):
        self.x0, self.y0, self.x1, self.y1 = r_coords
        self.text = r_text
        print("NR: r_text >%s< self.rect_id %s" % (r_text, self.rect_id))
        print("NR restore_obj, coords %d,%d, %d,%d, text >%s< parent_id %d" % (
             self.x0, self.y0, self.x1, self.y1, self.text, parent_id))
        self.parent_id = parent_id
        self.v1 = v1;  self.v2 = v2
        self.rdg.region = self.rdg.lr  # Start with cursor at lower right
        self.type = "n_rect"
        ##if not self.rect_id:
        self.rect_id = self.rdg.add_to_layer(2,
            self.drawing.create_rectangle, r_coords, fill="white")
        ##else:
        ##    self.rdg.drawing.itemconfigure(self.rect_id, state=tk.NORMAL)
        #print("? ? ? self.rect_id = %d" % self.rect_id)  #  rect_id = 1 here <<
            
        #self.nro = self.rdg.a_obj(self.rect_id, self, "n_rect", 
        #    r_coords, r_text, 0, v1, v2)  # No parent for n_rect's rectangle
        #print("n_rect.nro %s" % self.nro)
        print("++1++ self.rect_id = %d" % self.rect_id)
        nr_obj = self.new_n_rect(self.rect_id, r_coords, r_text,
            0, v1, v2)  # <<<<< n_rect has no parent  1535, Fri 8 Mar
        print(": : : nr_obj %s" % nr_obj)  ### coords OK here
        print("++2++ self.rect_id = %d" % self.rect_id)
        self.rdg.objects[self.rect_id] = nr_obj  # Put n_rect in objects first
        
        self.cx = (self.x0+self.x1)/2;  self.cy = (self.y0+self.y1)/2
        dtc_tool = dtc.draw_texts(self.drawing, self.root, self.rdg)
        self.text_obj = dtc_tool.restore_object(
            [self.cx, self.cy], r_text, self.rect_id, 0, 0)
            # restores the n_rect's text, and puts it into objects[]
        print("+++ n_rect text obj, parent_id %d" % self.rect_id)
        self.text_id = self.text_obj.key  # text after n_rect (it's parent)
        self.rdg.current_object = nr_obj
        
        print("      text id %d, obj %s" % (self.text_id, self.text_obj))
        print("n_rect %d = %s" % (self.rect_id, nr_obj))
        #self.rdg.dump_objects("n_rect restored")  ## parent_id 0 here !!!
        return self.rdg.current_object

    def new_n_rect(self, key, coords, txt, parent_id, v1, v2):
        self.x0, self.y0, self.x1, self.y1 = coords
        self.cx = (self.x0+self.x1)/2;  self.cy = (self.y0+self.y1)/2
        self.text = txt
        #print("NR: text >%s<" % txt)
        #print("NR restore_object, coords %d,%d, %d,%d, text >%s<" % (
        #     self.x0, self.y0, self.x1, self.y1, self.text))
        return self.rdg.object(key, self, "n_rect", coords, txt,
            parent_id, v1, v2)
        
    def undraw(self, d_obj):  # For rdgc.on_delete_key()
        obj = d_obj.a_obj
        if self.rect_id != 0:  # d+_obj not used for n_rects!
            self.rdg.drawing.itemconfigure(obj.rect_id, state=tk.HIDDEN)
            self.rdg.drawing.itemconfigure(obj.text_id, state=tk.HIDDEN)

    def redraw(self, d_obj):  # For rdgc.on_insert_key()
        obj = d_obj.a_obj
        if self.rect_id != 0:  # d_obj not used for n_rects!
            self.rdg.drawing.itemconfigure(obj.rect_id, state=tk.NORMAL)
            self.rdg.drawing.itemconfigure(obj.text_id, state=tk.NORMAL)

    def __str__(self):
        print("draw_n_rects, self x0,y0 %d/%d" % (self.x0,self.y0))
        coords = [self.x0, self.y0, self.x1, self.y1]
        return "NRXXX: coords %s, Text >%s<" % (coords, self.text)

    def mk_save_str(self, val):  # Make object's rdd file entry
        #print("N_RECT mk_save_str: val %s, val.i_coords %s" % (
        #    val, val.i_coords))
        ##nro = self.rdg.objects[val.key].a_obj
        ##print("->-> nro %s" % nro)  # nro never changes !!!
        i_coords = val.i_coords
        #print("self.coords [%d,%d, %d,%d]" % (
        #    self.x0, self.y0, self.x1, self.y1))
        d_type = "n_rect";  d_id = val.key
        coords = []
        for c in val.i_coords:  #### Not val.obj.coords
            coords.append(int(float(c)))
        ##str = self.drawing.itemcget(self.text_id, "text")
        str = val.i_text  # rdg.edit_esc_key updates i_text
        str = str.replace("\"", "\\\"")  # Escape \" chars
        str = str.replace("\n", "\\n")   # Escape \n chars
        #print("n_rect save_str >(%s %d) %s \"%s\" %s %s \"%s\"<" % (
        #    "n_rect", val.key,
        #   coords, str, self.parent_id, self.v1, self.v2))
        return "(%s %d) %s \"%s\" %s %s %s" % ("n_rect", val.key, \
            coords, str, val.parent_id, val.v1, val.v2)  # Corrected 8 Mar 2024
            #coords, str, self.parent_id, self.v1, self.v2)

    def coords(self, x0, y0, x1, y1):  # Set the n_rect's coords
        self.x0 = x0;  self.y0 = y0;  self.x1 = x1;  self.y1 = y1
        self.drawing.coords(self.rect_id, x0,y0, x1,y1)  # Move the n_rect
        self.cx = (x1+x0)/2;  self.cy = (y1+y0)/2
        self.drawing.coords(self.text_id, self.cx, self.cy)  # And it's text

    def reorg(self, sx, sy):  # Shift the n_rect's top-left corner
        w = self.x1-self.x0;  h = self.y1-self.y0
        self.x0 = sx;  self.y0 = sy;  self.x1 = sx+w;  self.y1 = sy+h

    def bbox(self):  # Gets the current coords
        return self.x0, self.y0, self.x1, self.y1

    def move(self, dx,dy):  # Move an n_rect
        nx0 = self.x0+dx;  ny0 = self.y0+dy 
        nx1 = self.x1+dx;  ny1 = self.y1+dy
        #print("/// n_rect move %s,%s" % (dx,dy))
        self.coords(nx0,ny0, nx1,ny1)  # Also moves cx,cy

    def type(self):
        return "n_rect"

    def print_n_rect(self):
        print("coords %d,%d, %d,%d, 'rect %s', 'text %s'" % (
            self.x0, self.y0, self.x1, self.y1, self.rect_id, self.text))

    def delete(self):
        self.rdg.drawing.itemconfigure(self.rect_id, state=tk.HIDDEN)
        ##self.drawing.delete(self.rect_id)
        self.rdg.drawing.itemconfigure(self.text_id, state=tk.HIDDEN)
        ##self.drawing.delete(self.text_id)
   
    def nr_closest(self, mx,my):
        item = self.drawing.find_closest(mx,my)
        if len(item) == 0:  # Empty tuple
            #print("*** nr_closest(): empty tuple")
            return None, None
        item_x = item[0]
        item_type = self.drawing.type(item_x)
        #print("*** nr_closest(): item_x = %s (%s), mx,my %d,%d" % (
        #    item, item_type, mx,my))
        if item_type != "rectangle":
            return None, None

        #self.dump_objects("in  nr_closest()")
 
        obj = self.rdg.objects[item_x]  # item_x is a tkinter object id
        if obj:
            return item, obj
        else:  # Not in objects, assume it's an arrowhead line
            print("@@@ item_x %d is not in objects <<<<" % item_x)
            return None, None

    # IMPORTANT: b1_click sets self.rdg.current_object (which includes it's key)
    #   b1_motion and b1_release all work on rdg.current_object

    def nr_b1_click(self, event):  # B1 (left button) to select an object
        mx, my = (event.x, event.y)  # Mouse position

        #print(". . . nr_b1_click: %s mode, %d,%d, %d objects, %s, %s" % (
        #    self.rdg.ln_mode, mx, my, len(self.rdg.objects), 
        #       event.widget, event.type)) 

        item, obj = self.nr_closest(mx,my)  # Closest tk object
        print("b1_click(): closest returned item %s, obj %s" % (item, obj))
        if not item:  # Empty tuple, nothing drawn yet
            #print("new_rect, n_objs = %d" % len(self.rdg.objects))
            nnn = self.restore_object([mx,my, mx+5,my+5],
                "<+>", 0, 0, 0)  # sets current_object
            #print("self.rdg.current_object %s" % self.rdg.current_object)
            #self.rdg.dump_objects("draw_n_rects")
        else:
            item_ix = item[0]
            if obj.o_type == "n_rect":
                #print("item-ix %d: " % item_ix, end="")
                #obj.a_obj.print_n_rect()
                self.rect_id = obj.a_obj.rect_id
                self.text_id = obj.a_obj.text_id
                print("Clicked near n_rect %d, text_id %d" % (
                    self.rect_id, self.text_id))
            elif obj.o_type == "text" and obj.parent_id != 0:
                obj = self.rdg.objects[obj.parent_id]
                print("Found enclosing n_rect, obj = %s" % obj)
            #print("closest tk object: >%s< (%s)" % (item_ix, obj.o_type))

            coords = self.drawing.coords(item_ix)
            #print("   coords %s" % coords)
            self.rdg.dump_objects("nr_b1_click()")

            #print("- - nr_b1_click() - -")
            if obj.o_type == "n_rect":
                self.rdg.current_object = obj
                #print("current_obj = %s" % obj)
                self.rdg.region = self.rdg.where(
                    self.rdg.current_object.object, mx,my)
                print("+++  %d,%d: self.rdg.region = %d" % (
                    mx,my, self.rdg.region))
                if self.rdg.region == self.rdg.far:  # Start new rectangle
                    self.restore_object([mx,my, mx,my], "-+-", 0, 0, "0")
                        # Changes rdg.current_obj to new rectangle
                else:
                    gt = self.drawing.gettags(item)
                    #print("gt %s (%s)" % (gt, type(gt)))
                    for tag in gt:  # Check its tags
                        if tag.startswith('rect'):
                            #print('  You clicked near {tag}')
                            self.last_tag = tag
            else:
                self.rdg.current_object = obj
                print("\a==> Can't move a '%s' in '%s' mode" % (
                    obj.o_type, self.ln_mode))

        self.last_mx = mx;  self.last_my = my  # Last mouse position
                
    def nr_b1_motion(self, event):  # Move the current_object
        mx, my = (event.x, event.y)
        if self.last_mx:
            dx = mx-self.last_mx;  dy = my-self.last_my
        else:
            dx = dy = 0
        #print("++b1_m deltas %d,%d" % (dx,dy)
        if self.rdg.current_object == None:  # No current_object yet!
            return
        if self.rdg.current_object.o_type == "n_rect":
            #nro = self.rdg.current_object.a_obj
            #print("b1_m: mx %d,%d  x0 %d,%d, x1 %d,%d, dx %d,%d" % (
            #    mx,my, nro.x0,nro.y0, nro.x1,nro.y1, dx,dy))
            r_coords = self.rdg.current_object.a_obj.bbox()
            #print("b1_motion: dr_coords >%s<, region %d" % (
            #    r_coords, self.region))
            x0,y0, x1,y1 = self.rdg.move_deltas(r_coords, dx,dy)
            #print("=== %d,%d, %d,%d" % (x0,y0, x1,y1))
            self.rdg.current_object.a_obj.coords(
                x0,y0, x1,y1)  # Resize/Move rect + text
            self.rdg.current_object.a_obj.i_coords = [x0,y0, x1,y1]
            #print("b1_motion %d,%d, %d,%d" % (x0,y0, x1,y1))
        self.last_mx = mx;  self.last_my = my  # Last mouse position

    def nr_b1_release(self, event):  # Left button released
        mx, my = (event.x, event.y)  # Mouse position
        x0,y0, x1,y1 = self.rdg.current_object.a_obj.bbox()
        ##print("b1_release %d,%d, %d,%d" % (x0,y0, x1,y1))  # <-- OK here
        ##k = self.rdg.current_object.key
        ##print("objects[k] = %s" % self.rdg.objects[k])
        self.rdg.objects[self.rect_id].i_coords = \
            [x0,y0, x1,y1]  # Save it's current coords!
        ##print("   saved %s" % self.rdg.objects[self.rect_id])
        self.last_mx = mx;  self.last_my = my  # Last mouse position

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
    # rfc-draw globals class
    dno = draw_n_rects(drawing, root, rdg)
    dno.set_event_handlers()
    root.mainloop()
