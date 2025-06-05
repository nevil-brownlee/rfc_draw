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
        self.rect_id = None  # id of this n_rect's rectangle

    class n_rect:  # Actual class for an n_rect
        def __init__(self, parent, root, rdg,
                     r_coords, r_text, parent_id, v1, v2):
            super().__init__()
            self.drawing = parent;  self.root = root;  self.rdg = rdg
            self.type = "n_rect"
            self.parent_id = parent_id;  self.v1 = v1;  self.v2 = v2
            self.rdg.region = self.rdg.lr  # Start with cursor at lower right
            self.r_coords = r_coords  # Class variable
            self.x0, self.y0, self.x1, self.y1 = r_coords
            self.text = r_text
            self.rect_id = self.rdg.add_to_layer(2,
                self.drawing.create_rectangle, r_coords, fill="white")
            print("--1-- class n_rect, self.rect_id %d" % self.rect_id)
            self.cx = (self.x0+self.x1)/2;  self.cy = (self.y0+self.y1)/2
            dtc_tool = dtc.draw_texts(self.drawing, self.root, self.rdg)
            self.text_obj = dtc_tool.restore_object(
                [self.cx,self.cy], r_text, self.rect_id, 0, 0)
            # restores the n_rect's text, and puts it into objects[]
            print("+++ n_rect text obj, parent_id %d" % self.rect_id)
            self.text_id = self.text_obj.key  # text after n_rect (it's parent)
            self.obj = self.rdg.object(self.rect_id, self, "n_rect",
                r_coords, r_text, parent_id, v1, v2)
            print("||| self.obj >%s<" % self.obj)
            ##del self.rdg.objects[self.text_id]  # Don't need to keep text obj!
            """
            self.rdg.objects[self.rect_id] = self.obj
            self.rdg.current_obj = self.obj
            print("|2| current_obj >%s<" % self.rdg.current_obj)  # OK here
            self.rdg.dump_objects("n_rect %d created: %s" % (
                self.rect_id, self.obj))
            """
        def coords(self, *args):
            print("--NR.coords, len(args): %d" % len(args))
            #for a in args: 
            #    print("arg: %s" % a)
            #exit()
            if len(args) == 4:
                self.x0, self.y0, self.x1, self.y1 = args
            elif len(args) == 2:
                self.x0, self,y0 = args
                self.x1 = self.x0+10;  self.y1 = self.y1+10
            #print("@@@ n_rect.coords: args ...")
            for arg in args:
                print(arg)
            print("coords set to %d,%d, %d,%d" % (
                self.x0, self.y0, self.x1, self.y1))
            #self.drawing.coords(self.rect_id,  # These 4 lines move the n_rect
            #    self.x0,self.y0, self.x1,self.y1)
            #self.cx = (self.x1+self.x0)/2;  self.cy = (self.y1+self.y0)/2
            #self.drawing.coords(self.text_id, self.cx, self.cy)  # and it's text
            
        def coords(self, x0, y0, x1, y1):  # Set the n_rect's coords
            print("+NR coords(%d,%d, %d,%d)" % (x0, y0, x1, y1))
            self.x0 = x0;  self.y0 = y0;  self.x1 = x1;  self.y1 = y1
            self.drawing.coords(self.rect_id, x0,y0, x1,y1)  # Move the n_rect
            self.cx = (x1+x0)/2;  self.cy = (y1+y0)/2
            self.drawing.coords(self.text_id, self.cx, self.cy)  # And it's text

        def reorg(self, sx, sy):  # Shift the n_rect's top-left corner
            w = self.x1-self.x0;  h = self.y1-self.y0
            self.x0 = sx;  self.y0 = sy;  self.x1 = sx+w;  self.y1 = sy+h

        def bbox(self):  # Gets the current coords
            return self.x0, self.y0, self.x1, self.y1

        #def move(self, dx,dy):  # Move an n_rect
        #    nx0 = self.x0+dx;  ny0 = self.y0+dy 
        #    nx1 = self.x1+dx;  ny1 = self.y1+dy
        #    #print("/// n_rect move %s,%s" % (dx,dy))
        #    self.coords(nx0,ny0, nx1,ny1)  # Also moves cx,cy
                
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

        def mk_save_str(self, val):  # Make object's rdd file entry
            print("@@text@@ text: mk_save_str, val >%s<" % val)
            coords = []
            for c in val.i_coords:
                coords.append(round(c))
                #print("@@    @@ %s" % coords)
                str = self.text
                str = str.replace("\n", "\\n")  # Escape \n chars
                str = str.replace("\"", "\\\"")  # Escape \" chars
            return "(%s %d) %s \"%s\" %s %s %s" % ("n_rect", val.key,
                coords, str, val.parent_id, val.v1, val.v2)
            
    def set_event_handlers(self):
        # Click b1 to make an object
        self.drawing.bind_class('Canvas','<ButtonPress-1>',  self.nr_b1_click)
        self.drawing.bind_class('Canvas','<Button1-Motion>', self.nr_b1_motion)
        self.drawing.bind_class('Canvas','<ButtonRelease-1>',self.nr_b1_release)
        #print(">>> draw_n_rects event handlers set")
        
    def restore_object(self, r_coords, r_text, parent_id, v1, v2):
        # Actual class for an n_rect
        print("r_coords >%s<" % r_coords)  # list
        print("r_text >%s<" % r_text)
        print("parent_id >%s<" % parent_id)
        print("v1 >%s<" % v1)
        print("v2 >%s<" % v2)
        print("$$$ r_coords %s, r_text >%s<, %s, %s,%s" % (
            r_coords, r_text, parent_id, v1,v2))
        self.rdg.rects_drawn += 1
        nro = draw_n_rects.n_rect(self.drawing, self.root, self.rdg,
            r_coords, r_text, parent_id, v1, v2)
        print("--99-- nro = %s" % nro)
        nro_obj = self.rdg.object(nro.rect_id, nro, "n_rect",
            r_coords, r_text, parent_id, v1, v2)
        print("||| nro_obj >%s<" % nro_obj)
        self.rdg.objects[nro.rect_id] = nro_obj
        self.rdg.current_obj = nro_obj
        print("|2| current_obj >%s<" % self.rdg.current_object)
        #self.rdg.dump_objects("n_rect %d created" % nro.rect_id)
        return nro_obj
        
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
        return "NRXXX: self >%s<" % (
            self.text)

    def mk_save_str(self, val):  # Make object's rdd file entry
        print("N_RECT mk_save_str: val %s, val.i_coords %s" % (
            val, val.i_coords))
        nro = self.rdg.objects[val.key].a_obj
        print("->-> nro %s" % nro)
        i_coords = [nro.x0, nro.y0, nro.x1, nro.y1]
        print("nro i_coords %s" % i_coords)  # OK
        d_type = "n_rect";  d_id = val.key
        coords = []
        for c in i_coords:  #### Not val.obj.coords
            coords.append(int(float(c)))
        ##str = self.drawing.itemcget(self.text_id, "text")
        str = val.i_text  # rdg.edit_esc_key updates i_text
        str = str.replace("\"", "\\\"")  # Escape \" chars
        str = str.replace("\n", "\\n")   # Escape \n chars
        #print("n_rect save_str >(%s %d) %s \"%s\" %s %s \"%s\"<" % (
        #    "n_rect", val.key,
        #   coords, str, self.parent_id, self.v1, self.v2))
        return "(%s %d) %s \"%s\" %s %s %s" % ("n_rect", val.key, \
            coords, str, val.parent_id, val.v1, val.v2)
    """
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
    """   
    def nr_closest(self, mx,my):
        item = self.drawing.find_closest(mx,my)
        if len(item) == 0:  # Empty tuple
            print("*** nr_closest(): empty tuple")
            return None, None
        item_ix = item[0]
        print("''nr_closest:: mx,my %d,%d item %d" % (mx,my, item_ix))
        #self.rdg.dump_objects("nr_closest")

        if item_ix in self.rdg.objects.keys():  # It's a known object
            obj = self.rdg.objects[item_ix]
            print("   item_ix %d in objects, obj >%s<" % (item_ix, obj))
            #if obj.o_type == "text":
            #    print(">>>>>>>>> it's a text object")
            #    exit()
        else:
            self.rdg.display_msg(
                "(Unknown object, item_ix %d, tk type %s << %s" % (
                item_ix, type(item), "unknown"))
            obj =  None        
        region = self.rdg.where(obj.a_obj, mx,my)
        item_type = self.drawing.type(item_ix)
        print("*** nr_closest(): item_x = %s (%s), mx,my %d,%d" % (
            item, item_type, mx,my))
        if item_type == "text":  # Is it an n_rect's text?
            obj = self.rdg.objects[item_x]
            print("*** near a text, obj >%s<" % obj)
            exit()       
        elif item_type != "rectangle":
            return None, None
      
        #!self.rdg.dump_objects("in nr_closest()")

        obj = self.rdg.objects[item_ix]  # obj is a tkinter object id
        print("!!! obj %s" % obj)
        if obj:
            self.rdg.current_object = obj
            print("*** nr_closest(): obj >%s<" % obj)
            return item, obj
        else:  # Not in objects, assume it's an arrowhead line
            print("@@@ item_x %d is not in objects <<<<" % item_x)
            return None, None

    # IMPORTANT: b1_click sets self.rdg.current_object (which includes it's key)
    #   b1_motion and b1_release all work on rdg.current_object

    def nr_b1_click(self, event):  # B1 (left button) to select an object
        mx, my = (event.x, event.y)  # Mouse position

        print(". . . nr_b1_click: %s mode, %d,%d, %d objects, %s, %s" % (
            self.rdg.last_mode, mx, my, len(self.rdg.objects), 
               event.widget, event.type))

        item, obj = self.nr_closest(mx,my)  # Closest tk object
        print("nr_b1_click(%d,%d): closest returned item %s, obj %s" % (
            mx,my, item, obj))
        if not item:  # Empty tuple, nothing drawn yet
            self.rdg.rects_drawn += 1
            print("new_rect, n_objs = %d" % len(self.rdg.objects))
            txt = "<%d>" % self.rdg.rects_drawn
            r_coords = [mx,my, mx+5,my+5]
            nro = draw_n_rects.n_rect(self.drawing, self.root, self.rdg,
                r_coords, txt, 0, 0,0)
            print("$ $ $ nro >%s<" % nro)
            self.rdg.current_object = nro.obj
            print("? ? ? nro >%s<" % nro)
            print("self.rdg.current_object %s" % self.rdg.current_object)
            #self.rdg.dump_objects("draw_n_rects")
        else:
            item_ix = item[0]
            print("click >%d<,obj %s  b1<<<<<<<<<<<<" % (item_ix, obj))
            #self.rdg.dump_objects("click >%d< b1" % item_ix)
            if obj.a_obj.type == "n_rect":
                print("item-ix %d: " % item_ix, end="")
                #!obj.a_obj.print_n_rect()
                self.rect_id = obj.a_obj.rect_id
                self.text_id = obj.a_obj.text_id
                print("Clicked near n_rect %d, text_id %d" % (
                    self.rect_id, self.text_id))
            elif obj.o_type == "text" and obj.parent_id != 0:
                obj = self.rdg.objects[obj.parent_id]
                print("Found enclosing n_rect, obj = %s" % nro.obj)
            #print("closest tk object: >%s< (%s)" % (item_ix, obj.o_type))

            coords = self.drawing.coords(item_ix)
            #print("   coords %s" % coords)
            #self.rdg.dump_objects("nr_b1_click()")

            print("+ - nr_b1_click() %d,%d obj %s - +" % (mx,my, obj))
            if obj.o_type == "n_rect":
                self.rdg.current_object = obj
                print("current_obj = %s" % obj)
                self.rdg.region = self.rdg.where(
                    self.rdg.current_object.a_obj, mx,my)
                #?self.rdg.display_where(obj.a_obj, mx,my, region)
                if self.rdg.region == self.rdg.far:  # Start new rectangle
                    self.rdg.rects_drawn += 1
                    txt = "<%d>" % self.rdg.rects_drawn
                    print("-abc- %d rects_drawn, txt %s, mx/my %d,%d" % (
                        self.rdg.rects_drawn, txt, mx,my))
                    coords = [mx,my, mx+5,my+5]
                    nro = draw_n_rects.n_rect(self.drawing, self.root,
                            self.rdg, coords, txt, 0, 0,0)
                    print("<><> nro %s" % nro)
                    self.rdg.current_object = nro.obj
                    print(">>3>> current_object %s" % self.rdg.current_object)
                    #self.restore_object([mx,my, mx,my], txt, 0, 0, 0)
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
        print("++b1_m deltas %d,%d" % (dx,dy))
        if self.rdg.current_object == None:  # No current_object yet!
            return
        if self.rdg.current_object.o_type == "n_rect":
            r_coords = self.rdg.current_object.a_obj.bbox()
            #print("b1_motion, n_rect: %d,%d, r_coords >%s<, region %d" % (
            #    mx,my, r_coords, self.rdg.region))
            x0,y0, x1,y1 = self.rdg.move_deltas(r_coords, dx,dy)
            print("=motion= %d,%d, %d,%d" % (x0,y0, x1,y1))
            self.rdg.current_object.a_obj.coords(
                x0,y0, x1,y1)  # Resize/Move rect + text
            #print("==current_obj %s" %self.rdg.current_object)
            ##self.rdg.current_object.a_obj.i_coords = (x0,y0, x1,y1)
            self.rdg.current_object.i_coords = (x0,y0, x1,y1)
            #print("b1_motion: %d,%d, %d,%d, %d" % (
            #    x0,y0, x1,y1, self.rdg.region))

            self.last_mx = mx;  self.last_my = my  # Last mouse position

    def nr_b1_release(self, event):  # Left button released
        mx, my = (event.x, event.y)  # Mouse position
        print("b1r: current_obj >%s<" % self.rdg.current_object)
        self.rdg.dump_objects("b1_release")

        co_type = self.rdg.current_object.o_type
        if co_type != "text" and co_type != "int":
            x0,y0, x1,y1 = self.rdg.current_object.a_obj.bbox()
            print("b1_release x %d,y %d, %d,%d, %d,%d" % (
                mx,my, x0,y0, x1,y1))  # <-- OK here
        nr_rdo = self.rdg.current_object
        print("   nr_rdo %s" % nr_rdo)
        nr_clo = nr_rdo.a_obj
        print("   nr_clo %s" % nr_clo)
       
        k = nr_rdo.key
        print("... c_o_key = %d" % k)
        self.rdg.objects[k] = nr_rdo
        
        print(">> k %d, objects[k] = %s" % (k, self.rdg.objects[k]))
        print("   nr_clo %s, >coords %s<" % (nr_clo, nr_clo.bbox()))
        self.rdg.objects[k] = nr_rdo
        print("   saved %s" % self.rdg.objects[nr_clo.rect_id])
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
    # rfc_draw globals class
    dno = draw_n_rects(drawing, root, rdg)
    dno.set_event_handlers()

    nro = dno.n_rect(drawing, root, rdg,
                     [100,100, 200,200], "sample", 7, 1, 2)
    print("nro = %s, coords %s" % (nro, nro.coords(6,7,8,9)))
    
    root.mainloop()
