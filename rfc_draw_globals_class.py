# 1055, Wed  6 Sep 2023 (NZST)
# 1600, Tue 25 Jul 2023 (NZST)
# 1411, Sun 22 Jan 2023 (NZDT)
# 1609, Sat  1 Oct 2023 (NZDT)
#
# rfc_draw_globals_class:
#                   contains rfc-draw global data (for event handlers)
#                   and functions for Objects, e.g.
#                      class object (rfc_draw objects)
#                      object dictionary, get_object()
#                      save_to_rdd(), read_from_rdd()
#                      
# Copyright 2023, Nevil Brownlee, Taupo NZ

import os.path, re, sys, termios, traceback
import tkinter as tk

import arrow_lines_class as alc   # Draw lines with direction arrows
import draw_groups_class as dgr   # Handles rfc-draw groups
import draw_lines_class as dlc    # Handles line objects
import draw_n_rects_class as drc  # Handles n_rect objects

class rdglob:  # Global variables for rfc-draw's objects
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)  # New instance of rdglob

    def test_fn(self):
        print("$$$ from rdglob.test_fn")

    def __init__(self, parent, root, m_text):
        super().__init__()
        self.drawing = parent;  self.root = root;  self.m_text = m_text
        self.rdg = self

        #self.f_font = tk.font.Font(  # Initialise class variables
        #    family="TkFixedFont")
        self.f_font = "TkFixedFont"  # This works, above version doesn't <<<
        #self.f_font = "DroidSansMono 12"  # This works too
        #self.f_font = "Consolas 12"  # Should work on Windows 11
        # https://stackoverflow.com/questions/48731746/
        # how-to-set-a-tkinter-widget-to-a-monospaced-platform-independent-font
        self.f_width = self.f_height = None

        self.last_button = "rect"
        self.last_key = ""
        self.ln_mode = "rect"

        self.m_text.tag_config('normal', foreground="black")
        self.m_text.tag_config('warning', foreground="dark orange")
        self.m_text.tag_config('error', foreground="red3")

        # Rect variables
        self.tl   = 0;     self.top = 1;     self.tr = 2  # Mouse regions
        self.left = 3;  self.middle = 4;  self.right = 5
        self.ll   = 6;     self.bot = 7;     self.lr = 8
        self.far  = 9  # Too far away from closest rect
        self.new = 10  # Drawing a new rectangle
        self.region = self.lr  # Region mouse pointer is currently in
        self.pos = ["tl",   "top",  "tr",
                  "left", "middle", "right",
                    "ll", "bottom", "lr",  "too_far", "new"]
        self.res_px = 4  # Nearness margin
        self.far_px = 8  # This far away to start a new rect

        self.objects = {}  # (draw_objects) objects, key (tk object) id
                           #   Text in an n_rect is part of that n_rect
        self.current_object = None  # Key to actual object in self.objects

        self.r_obj_keys = {}  # old-key -> new-key for objects read from rdd
    
        self.deleted_objects = []  # Objects deleted (using Delete key)

        # Patterns for reading the description string for an object
        self.rrd_re = re.compile(
               "(\d+)\s+\((.+)\s+(.+)\)\s+\[(.+)\]\s+\"(.*)\"\s+(\d+)\s+(.)")
        # field   0        1       2          3          4         5      6
        #       objid    type    skey       coords     text      g_nbr   g_type

        self.mbr_re = re.compile(
               "\s+\((.)(.+)\ member\s(.+)\)\s+(.+)\s\[(.+)\]")
        # field       0  1           2        3       4
        #    blanks  id g_nbr       g_key    type    coords
             
        self.last_tag = None  # Tag of last-clicked object
        self._layers = []  # For add_to_layer()

        self.mx_groups = 8
        self.gd_colours = ["tan2", "saddlebrown", "red", "darkorange",
            "gold", "green", "darkblue", "indigo", "darkviolet"]    # Dark
        self.gl_colours = ["tan1", "peru", "tomato", "kakhi", "palegoldenrod",
            "palegreen", "skyblue", "royalblue", "palevioletred"]   # Light
        self.g_colours = self.gd_colours  # For groups 0, 1..8
            # group_nbr == 0 means the object isn't in any group <<
        self.n_groups = 0
        self.g_o_keys = [None]*(self.mx_groups+1)  # Objects in group
 
        self.last_mx = self.last_my = None

        """ 
        self.add_to_layer(3, self.drawing.create_text,
            (300,250), fill="blue", text="H  H  H  H  H")
        self.add_to_layer(3, self.drawing.create_text,
            (300,400), fill="blue", text="HHHHHHHHHHHHHHH")
        # draw a square on layer 2:
        self.add_to_layer(2, self.drawing.create_rectangle,
            (200,200, 500,300), fill="khaki")
        # draw a circle on layer 1:
        self.add_to_layer(1, self.drawing.create_line,
            (100,100, 400,100, 400,400, 400,400, 100,400, 100,100),
            fill="red")
        """

    # Click b3 to edit a text objectg
        self.drawing.bind_class('Canvas','<ButtonPress-3>', self.on_b3_click)

        self.centre_texts = True  # Set by draw_* set_event_handlers()

        self.root.bind("<Delete>", self.on_delete_key)  # Bind to root works
                                             # bind to Canvas *doesn't* work
        self.root.bind("<Insert>", self.on_insert_key)
        self.root.bind("<Next>", self.on_next_key)  # Pg Dn

        self.bind_keys()

    def bind_keys(self):
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            # Clear queued key-presses
        self.root.bind('<KeyPress>', self.on_key_press_repeat)
        self.has_prev_key_press = None
        self.root.bind('<Escape>',self.on_key_press_repeat) # Clear Msg window
        self.root.bind('<KeyPress-c>',self.on_key_press_repeat) # copy
      
    def unbind_keys(self):        # Unbind keys used by
        self.root.unbind('<KeyPress-u>')  # draw_groups_class
        self.root.unbind('<KeyPress-a>')  # draw_lines_class
        self.root.unbind('<KeyPress-n>')
        self.root.unbind('<KeyPress-e>')
        self.root.unbind('<KeyPress-b>')
        self.root.unbind('<KeyPress-f>')
        self.root.unbind('<KeyPress-r>')
        self.root.unbind('<KeyPress-equal>')

    def display_msg(self, text, tag):  # Display text in Message area
        # tags declared above, i.e. 'normal' and 'error'
        if tag == "error":
            print("\a\a")  # BEL
        elif tag == "warning":
            print("\a")
        self.m_text.delete('1.0', tk.END)
        self.m_text.insert('1.0', text, tag)

    def where(self, rdo, x, y):  # Find region of rdo where b1 is pressed
        #print("... ... where: rdo = %s" % rdo)
        #print("   coords %d,%d, %d,%d" % (rdo.x0,rdo.y0, rdo.x1,rdo.y1))
        if y <= rdo.y0 + self.res_px:  # Top row
            if y < rdo.y0 - self.far_px:  # Too high
                return self.far
            if x <= rdo.x0 + self.res_px:
                if x < rdo.x0 - self.far_px:
                    return self.far  # Too far left
                return self.tl
            elif x >= rdo.x1 - self.res_px:
                if x > rdo.x1 + self.far_px:  # Too far right
                    return self.far
                return self.tr
            return self.top
        elif y >= rdo.y1 - self.res_px:  # Bottom row
            if y > rdo.y1 + self.far_px:  # Too low
                return self.far
            if x <= rdo.x0 + self.res_px:
                if x < rdo.x0 - self.far_px:
                    return self.far  # Too far left
                return self.ll
            elif x >= rdo.x1 - self.res_px:
                if x > rdo.x1 + self.far_px:  # Too far right
                    return self.far
                return self.lr
            return self.bot
        else:  # Middle row
            if x <= rdo.x0 + self.res_px:
                if x < rdo.x0 - self.far_px:
                    return self.far  # Too far left
                return self.left
            elif x >= rdo.x1 - self.res_px:
                if x > rdo.x1 + self.far_px:  # Too far right
                    return self.far
                return self.right
            return self.middle

    def move_deltas(self, coords, dx,dy):
        x0,y0, x1,y1 = coords
        #print("move_deltas: %d,%d, %d,%d, delta %d,%d" % (
        #    x0,y0, x1,y1, dx,dy))
        w = self.drawing.winfo_reqwidth()
        h = self.drawing.winfo_reqheight()

        min_px = 5  # Keep at least min_px visible at canvas edges
        if self.region == self.lr:
            if y1+dy+min_px > h: dy = 0 # Stop down
            if x1+dx+min_px > w: dx = 0 # Stop right
            x1 += dx;  y1 += dy
        elif self.region == self.ll:
            if y1+dy+min_px > h: dy = 0 # Stop down
            if x0+dx-min_px < 0: dx = 0 # Stop left
            x0 += dx;  y1 += dy
        elif self.region == self.tl:
            if y0+dy-min_px < 0: dy = 0 # Stop up
            if x0+dx-min_px < 0: dx = 0 # Stop left
            x0 += dx;  y0 += dy
        elif self.region == self.tr:
            if y0+dy-min_px < 0: dy = 0 # Stop up
            if x1+dx+min_px > w: dx = 0 # Stop right
            x1 += dx;  y0 += dy
        elif self.region == self.bot:
            if y1+dy+min_px > h: dy = 0 # Stop down
            y1 += dy
        elif self.region == self.left:
            if x0+dx-min_px < 0: dx = 0 # Stop left
            x0 += dx
        elif self.region == self.top:
            if y0+dy-min_px < 0: dy = 0 # Stop up
            y0 += dy
        elif self.region == self.right:
            if x1+dx+min_px > w: dx = 0 # Stop right
            x1 += dx
        else:  # self.middle
            if x0+dx+min_px > w: dx = 0 # Stop right
            if x1+dx-min_px < 0: dx = 0 # Stop left
            if y0+dy+min_px > h: dy = 0 # Stop down
            if y1+dy-min_px < 0: dy = 0 # Stop up
            x0 += dx;  y0 += dy;  x1 += dx;  y1 += dy
        return x0,y0, x1,y1

    class n_rect:  # Rectangle with white fill and centred text
        def __init__(self, rdg, drawing, r_coords, r_text, g_nbr):
            self.drawing = drawing
            self.f_font = "TkFixedFont"  # See draw_text_class.py for comments!
            self.x0, self.y0, self.x1, self.y1 = r_coords
            #print("create n_rect, coords %d,%d, %d,%d" % (
            #     self.x0, self.y0, self.x1, self.y1))
            rdg.region = rdg.lr  # Start with cursor at lower right
            self.type = "n_rect"
            self.rect_id = rdg.add_to_layer(2,
                self.drawing.create_rectangle, r_coords, fill="white")
            self.cx = (self.x0+self.x1)/2;  self.cy = (self.y0+self.y1)/2
            if len(r_text) != 0:
                self.text_id = rdg.add_to_layer(3,
                    self.drawing.create_text, (self.cx,self.cy),
                        text=r_text, font=self.f_font, activefill="red", 
                        anchor=tk.CENTER)
            self.text = r_text
            self.g_nbr = g_nbr

        def __str__(self):
            return "type %s, text >%s<" % (self.type, self.text)
        
        def coords(self, x0, y0, x1, y1):  # Set the object's coords
            self.x0 = x0;  self.y0 = y0;  self.x1 = x1;  self.y1 = y1
            self.drawing.coords(self.rect_id, x0,y0, x1,y1)  # Move the rect
            self.cx = (x1+x0)/2;  self.cy = (y1+y0)/2
            self.drawing.coords(self.text_id, self.cx, self.cy)  # And it's text

        def reorg(self, sx, sy):  # Shift the object's top-left corner
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
                self.x0, self.y0, self.x1, self.y1, self.rect_id, self.text_id))

        def delete(self):
            self.drawing.delete(self.rect_id)
            self.drawing.delete(self.text_id)

    class g_member:  # Holds group info for a group member obj
        def __init__(self, rdg, g_nbr, oo_key, g_tk_id, g_object, g_rel_coords):
            self.rdg = rdg;  self.g_nbr = g_nbr;
            self.oo_key = oo_key  # member's original objects[] key
            self.g_tk_id = g_tk_id
            self.g_object = g_object  # class object!
            self.rel_coords = g_rel_coords

        def __str__(self):
            return ("<g_nbr %d, g_object %s>" % (self.g_nbr, self.g_object))
            ##return ("<g_nbr %d, g_object %s>" % (self.g_nbr, "GMGM"))

    def draw_group_edr(self, g):
        g.g_rect_id = self.rdg.add_to_layer(1, # Draw it's dashed rectangle
            self.rdg.drawing.create_rectangle, g.g_coords, width=1,
                dash=(8,3), outline=self.rdg.gd_colours[g.g_nbr],
                tags=["edr %d" % g.g_nbr])
                #dash=(8,3), outline="red", tags=["edr %d" % g.g_nbr])

    class group:
        #   Group objects are drawn with pale-colour edr's, o_type 'group'
        #     Their group number is saved
        #     They have their own objects, keeping track of object positions
        #     Their move function must move all their contained objects
        def __init__(self, rdg, drawing, g_nbr, g_coords):
            self.rdg = rdg;  self.drawing = drawing;  self.g_nbr = g_nbr
            self.g_coords = g_coords  # Of group's edr
            self.x0, self.y0, self.x1, self.y1 = self.g_coords
            if not self.x1:
                self.x1 = self.x0;  self.y1 = self.y0
            self.g_rect_id = 0
            self.edr_tag = "edr %d" % g_nbr
            self.zoom = 1.00,
            self.g_members = []
            #print("@1 g_members %s" % self.g_members)

        def __str__(self):
            m_str = ""
            for m in self.g_members:
                m_str += " %s," % m.oo_key
            g_coords = [self.x0, self.y0, self.x1, self.y1]
            return ("<<group %d, g_rect_id %s, g_coords %s, members %s>>" % (
                self.g_nbr, self.g_rect_id, g_coords, m_str))

        def bbox(self):  # Gets the current edr coords
            return self.x0, self.y0, self.x1, self.y1

        def coords(self, x0, y0, x1, y1):  # Set group's coords
            #print("? ? ? group g_rect_id %d" % self.g_rect_id)
            self.x0 = x0;  self.y0 = y0;  self.x1 = x1;  self.y1 = y1
            self.drawing.coords(self.g_rect_id, x0,y0, x1,y1)

        def move(self, dx,dy):  # Move a group
            nx0 = self.x0+dx;  ny0 = self.y0+dy 
            nx1 = self.x1+dx;  ny1 = self.y1+dy
            #print("+77+ dx/dy %d/%d" % (dx,dy))
            #print("current_object >%s<" % self.rdg.current_object)
            self.coords(nx0,ny0, nx1,ny1)  # Move group's edr
            for gm in self.g_members:  # Now move each of the group's objects
                #print("@@ gm >%s<" % gm)
                mo = self.rdg.objects[gm.oo_key]
                #print("   mo = >%s<" % mo)
                if mo.o_type == "text" and mo.in_n_rect == 0:
                    self.drawing.move(mo.key, dx,dy)
                elif mo.o_type == "line":
                    a_line = mo.object
                    a_line.move(dx,dy)
                elif mo.o_type == "n_rect":
                    mo.object.move(dx,dy)

        def delete(self):
            self.drawing.delete(self.g_rect_id)
            #for m in self.g_members:
            #    m_str += " %s," % m.oo_key
 
    def transform_coords(self, del_x,del_y, obj_coords):  # Returns
        # obj_oords with del_x,del_y subtracted from each pair of it's points
        n_points = int(len(obj_coords)/2)
        #print("++ oo_coords: n_points %d, del_x/y %d/%d, obj_coords %s" % (
        #    n_points, del_x,del_y, obj_coords))
        coords = []
        for ns in range(0,n_points):
            coords.append(obj_coords[ns*2]+del_x)
            coords.append(obj_coords[ns*2+1]+del_y)
        #print("== coords >%s<" % coords)
        return coords

    def rel_coords(self, edr, s_coords):  # s to r
        n_points = int(len(s_coords)/2)
        #print("++ rel_coords: n_points %d, edr %s, s_coords %s" % (
        #    n_points, edr, s_coords))
        ex = edr[0];  ey = edr[1]  # Top-left corner
        rel_coords = []
        for ns in range(0,n_points):
            rel_coords.append(s_coords[ns*2]-ex)    # sx
            rel_coords.append(s_coords[ns*2+1]-ey)  # sy
        #print("== rel_coords >%s<" % rel_coords)
        return rel_coords

    def screen_coords(self, edr, rel_coords):  # r to s
        n_points = int(len(rel_coords)/2)
        #print("++ screen_coords: n_points %d, edr %s, rel_coords %s" % (
        #     n_points, edr, rel_coords))
        ex = edr[0];  ey = edr[1]  # Top-left corner
        scr_coords = []
        for ns in range(0,n_points):
            scr_coords.append(ex+rel_coords[ns*2])    # sx
            scr_coords.append(ey+rel_coords[ns*2+1])  # sy
        #print("== scr_coords >%s<" % scr_coords)
        return scr_coords

    class object:  # n_rect/text/line/grp* Objects for rfc-draw
        def __init__(self, key, obj, obj_type, coords, text, group, in_n_rect):
            self.key = key          # key to self.objects
            self.object = obj       # Actual object
            self.o_type = obj_type  # Object type
            self.i_coords = coords  # Initial x,y coords (from rdd)
            self.i_text = text      # Initial text (from rdd)
            self.g_nbr = group      # Group this object is part of
            self.in_n_rect = in_n_rect    # == 0 -> it's just a tk object
                                #  > 0 -> n_rect's key for it's rectangle
                                #         don't write to save-file.rdd
        def __str__(self):
            return "<Key %s, Object %s, Type %s, I_coords %s, G_nbr %d, In_n_rect %s>" % (
                self.key, self.object, self.o_type, self.i_coords, self.g_nbr, self.in_n_rect)

    def set_mode(self, which): # Rect/Text/Line buttons use this
        self.last_button = which  #  ln_mode changes within Line mode
        if self.ln_mode == "group":  # Returning to rect, line or text
            self.drawing.bind_class('Canvas','<Button-3>', self.on_b3_click)
        self.ln_mode = which
        #print("in rdg: self.ln_mode now = %s" % self.ln_mode)
        if which == "line":
            self.ln_mode = "new_ln"

    def obj_to_str(self, val):
        if val.o_type == "n_rect":
            rect_id = val.object.rect_id;  text_id = val.object.text_id
            coords = self.drawing.coords(rect_id)
            str = self.drawing.itemcget(val.object.text_id, "text")
            return "(%s, %d) %s \"%s\"" % ("n_rect", rect_id, coords, str)
        elif val.o_type == "text":
            coords = self.drawing.coords(val.object)
            str = self.drawing.itemcget(val.object, "text")
            return"(%s, %s) %s \"%s\"" % ("text", val.object, coords, str)
        elif val.o_type == "line":
            coords = val.object.lbd
            lbd_id = val.object.lbd_id
            return "(%s %d) %s" % ("a_line", lbd_id, coords)
        elif val.o_type == "group":
            #print("group object >%s<" % val.object)
            g_key = val.key  # key = g1, etc
            coords = val.object.bbox()
            g_nbr = val.object.g_nbr
            #print("@@@ g_key %s, coords %s" % (g_key, coords))
            return "(%s %s) %s" % ("group", g_key, coords)
        return None  # Unknown type
            
    def dump_objects(self, header):
        ###return  # Disable dumps !
        print("dump_objects -- %s --" % header)
        for j,key in enumerate(self.objects):
            val = self.objects[key]
            print("  j %d, val %s" % (j, val))
            o_tags = self.drawing.gettags(val.key)
            s = self.obj_to_str(val)
            if not s:  # Not a known type
                print("%2d (%s) <<< unknown type" % (j, val.o_type))
            else:
                print("%2d %s tags %s" % (j+1, s, o_tags))
                if val.o_type == "group":
                    print("  group %d, o_type %s, <%s>" % (
                        val.object.g_nbr, val.o_type, val.object))
        print("- - dump - -")  # Trailer line
        
    def get_object(self, item_ix):
        #print("get_object: item_ix = %s" % item_ix)
        #self.dump_objects("get_object()")
        #print("objects.keys = %s" % self.objects.keys())
        item_type = self.drawing.type(item_ix);
        if item_ix in self.objects.keys():  # It's a known object
            val = self.objects[item_ix]
            #print("   item_ix %d in objects, val >%s<" % (item_ix, val))
            return val  # rfc-draw object()
        else:
            #self.display_msg("(Unknown object, item_ix %d, tk type %s %s" % (
            #    item_ix, item_type)), "error")
            return None

    # Function to implement stacking order for widgets
    #     https://stackoverflow.com/questions/9576063
    def add_to_layer(self, layer, command, coords, **kwargs):
        layer_tag = "layer %s" % layer
        if layer_tag not in self._layers: self._layers.append(layer_tag)
        tags = kwargs.setdefault("tags", [])
        tags.append(layer_tag)
        item_id = command(coords, **kwargs)
        tags = self.drawing.gettags(item_id)
        #print("add_to_layer %d: tags "% layer, end="");  print(tags)
        self._adjust_layers()
        return item_id

    def _adjust_layers(self):
        for layer in sorted(self._layers):
            self.drawing.lift(layer)

    def restore_rect(self, r_coords, r_text, g_nbr):
        print("restore_rect: r_coords %s, r_text %s, g_nbr %d" % \
            (r_coords, r_text, g_nbr))
        rdo = self.n_rect(self.rdg, self.drawing, r_coords, r_text, g_nbr)
        print("restore_rect: ", end="");  rdo.print_n_rect()
        self.objects[rdo.rect_id] = self.object(rdo.rect_id,
            rdo, "n_rect", r_coords, r_text, g_nbr, 0)  # n_rect obj
        self.objects[rdo.text_id] = self.object(rdo.text_id,
            rdo.text_id, "text", r_coords, r_text, g_nbr, rdo.rect_id) 
            # Entry for n_text allows b3 to edit it
        return rdo.rect_id
        
    def new_text(self, mx, my, t_text, g_nbr):
        text_id = self.add_to_layer(3, 
            #self.drawing.create_text, (mx,my), fill="green", text=t_text,
            self.drawing.create_text, (mx,my), text=t_text,
               font=self.f_font, anchor=tk.CENTER, activefill="red")
        text_obj = self.object(
            text_id, text_id, "text", [mx,my], t_text, g_nbr, 0)
        self.objects[text_id] = text_obj
        self.current_object = text_obj
        return text_obj

    def restore_text(self, r_coords, r_text, g_nbr):
        #print("restore_text: r_coords %s, r_text >%s<, g_nbr %s" % (
        #    r_coords, r_text, g_nbr))
        text_id = self.add_to_layer(3, 
            self.drawing.create_text, r_coords, fill="red", text=r_text,
            font=self.f_font, anchor=tk.CENTER)  #, activefill="red")
        text_obj = self.object(
            text_id, text_id, "text", r_coords, r_text, g_nbr, 0)
        self.objects[text_id] = text_obj
        return text_id

    def delete_text(self, text_id):
        self.drawing.delete(text_id)

    def restore_line(self, l_coords, l_text, g_nbr):
        print("restore_line: l_coords %s, l_text >%s<" % (l_coords, l_text))
        a_line = alc.a_line(self.drawing, l_coords, self)
                                           # rdg is self here!
        #print("restore_line: l_text >%s<" % l_text)        
        for c in l_text:
            if c in "na":
                a_line.set_arrows(c)
            elif c in "ue":
                a_line.syntax_end(c)
            print("restore_line: option c = %s" % c)
        self.lbd_id = a_line.draw_line()
        line_obj = self.object(
            self.lbd_id, a_line, "line", l_coords, l_text, g_nbr, 0)
        #print(">>> restored line, obj = %s" % line_obj)
        self.objects[self.lbd_id] = line_obj
        return self.lbd_id
    
    def new_group_nbr(self):
        self.rdg.n_groups += 1;  g_nbr = self.rdg.n_groups
        if self.rdg.n_groups == self.rdg.mx_groups:
            self.display_msg("Can only have at most %d groups!" % \
                             self.rdg.mx_groups, "error")
        else:
            return g_nbr
                    
    def restore_group(self, g_coords, g_text):
        g_nbr = self.new_group_nbr()
        #print("restore_group: g_coords %s, g_text %s, g_nbr %s" % (
        #    g_coords, g_text, g_nbr))
        g = self.group(self, self.drawing, g_nbr, g_coords)  # New group object
        self.draw_group_edr(g)  # Add (and draw) it's edr
        group_obj = self.object(
            g.g_rect_id, g, "group", g_coords, g_text, g_nbr, 0)
        #print("g_rect_id = %s" % g.g_rect_id)
        self.objects[g.g_rect_id] = group_obj
        return g.g_rect_id
    
    def s_to_stuple(self, t):
        t1 = t.replace("'", "")
        cs = t1.replace('"','')
        return cs
    
    def s_to_ilist(self, t):
        ol = [];  st = t.split(", ")
        for cs in st:
            i_d = cs.split(".")
            ol.append(int(i_d[0]))
        return ol

    def find_group_key(self, g_nbr):
        for item_ix in self.objects.keys():
            val = self.objects[item_ix]
            if val.o_type == "group" and val.object.g_nbr == g_nbr:
                #print("@fgk, val >%s<" % val)
                return val.key

    def restore_object(self, ds):
        #print("restore_object: ds >%s<" % ds)
        if "member" in ds:
            #print("=== member line >%s<" % ds)
            #self.dump_objects(">> 'member' read <<")

            fields = self.mbr_re.search(ds).groups()
            gt = fields[0]  # 'g'
            g_nbr = int(fields[1])  # group (or template number)
            o_key = fields[2]  # member key in objects[]
            m_key = self.r_obj_keys[fields[2]]  # member key in new objects[] dict
            #print("  o_key %s, m_key %s" % (o_key, m_key))

            m_type = fields[3]  # member type
            mo = self.objects[m_key]
            coords = self.s_to_ilist(fields[4])
            #print("gt %s, g_nbr %d m_key %d, type %s, coords >%s<" %
            #      (gt, g_nbr, m_key, m_type, coords))
            g_key = self.find_group_key(g_nbr)
            #print("=== g_key %s" % g_key)
            go = self.objects[g_key]
            #print("group go >%s<" % go)
            i_coords = mo.i_coords;  i_text = mo.i_text
            print("restore group %d member %s" % (g_nbr, mo))
            r_coords = self.rel_coords(go.object.g_coords, i_coords)
            m = self.g_member(self.rdg, g_nbr, m_key, m_key, go, r_coords)
            #print("- - - m = %s" % m)
            self.objects[g_key].object.g_members.append(m)
            return m_key, g_key
        else:  # Ordinary object
            print("Ordinary object == ds %s ==" % ds)
            fields = self.rrd_re.search(ds).groups()
            print("@@@ fields = ", end="");  print(fields)
            print("0: >%s< %s" % (fields[0], type(fields[0])))
            obj_id = int(fields[0])  # Ignore line_nbr (field 0)
            obj_type = fields[1]
            #s_key = int(self.s_to_stuple(fields[2]))  # object's key in save file
            s_key = fields[2]  # object's key in save file
            coords = self.s_to_ilist(fields[3])
            text = fields[4].replace("\\n", "\n")
            text = text.replace('\\"', '"')
            g_nbr = int(fields[5])  # Group nbr
            g_type = fields[6]  # Group type
            if obj_type == "n_rect":
                return s_key, self.restore_rect(coords, text, 0)  # rect_id
            elif obj_type == "text":
                return s_key, self.restore_text(coords, text, 0)  # text_id
            elif obj_type == "line":
                #print("about to call restore_line()")
                return s_key, self.restore_line(coords, text, 0)  # lbd_id
            elif obj_type == "group":
                #self.dump_objects(">group< read from rdd")
                return s_key, self.restore_group(coords, text)    # g_rect_id

    def read_from_rdd(self, fn):
        if not os.path.exists(fn):
            self.display_msg("No file %s, will write it on closing" % fn, \
                "warning")
            self.f_width = 10.333;  self.f_height = 17
            #  10.333 px width, 17 px height work well for TkFixedFont !
        else:
            f = open(fn, "r")
            for line in f:
                if line[0] == "#":  # Ignore comment lines
                    continue
                ds = line.rstrip('\n')
                #print("ds >%s<" % ds)
                #print("r_obj_keys %s <<<" % self.r_obj_keys)
                if ds.find("root_geometry") >= 0:
                    la = ds.split(" ")
                    self.root.geometry(la[1])
                elif ds.find("drawing_size") >= 0:
                    # drawing size is set by rfc-draw.py
                    # It's used by rdd-to-ascii.py
                    #   but not by rfc_draw_globals*.py and draw*.py
                    pass
                elif ds.find("mono_font") >= 0:
                    la = ds.split(" ")
                    self.f_width = float(la[2])
                    self.f_height = int(la[4])
                    #print("mono_font width %d, height %.1f pixels" % (
                    #    self.f_width, self.f_height))
                else:
                    print("=+= ds = %s" % ds)
                    #print("### r_obj_keys %s" % self.r_obj_keys)
                    s_key, tk_id = self.restore_object(ds)
                    self.r_obj_keys[s_key] = tk_id
                    #self.dump_objects("READ_from_rdd")
            self.display_msg("Read from: %s" % fn, 'normal')
        #self.dump_objects("Read all rdd lines")
        #print("r_obj_keys = >%s<" % self.r_obj_keys)

    def obj_to_save_str(self, val):
        ##print("@@ otods: val = %s" % val)
        d_type = None;  g_nbr = 0;  g_type = "N"
        if val.o_type == "n_rect":
            #print("@@@ val.o_type n_rect")
            d_type = "n_rect";  d_id = val.object.rect_id
            coords = self.drawing.coords(val.object.rect_id)
            str = self.drawing.itemcget(val.object.text_id, "text")
        elif val.o_type == "text":
            d_type = "text";  d_id = val.object
            if val.in_n_rect == 0:  # User-created text
                    # != 0 -> part of an n_rect
                coords = self.drawing.coords(val.object)
                str = self.drawing.itemcget(val.object, "text")
                str = str.replace("\"", "\\\"")  # Escape " chars

                #print("-->  d_type %s, d_id %d, coords %s" % (
                #    d_type, d_id, coords))
            else:  # Text in an n_rect
                return None  # Don't try to save it!
        elif val.o_type == "line":
            d_type = "line";  d_id = val.object.lbd_id
            coords = val.object.lbd;  str = ""
            if val.object.arrowheads:
                str += "a"
            if val.object.syntax_end_mark:
                str += "e"
            #print("= = = to_save_str = = = str = >%s<" % str)
            #print("   val.object = %s (%s)" % (val.object, type(val.object)))
        elif val.o_type == "group":
            d_type ="group";  d_id = "g%d" % val.object.g_nbr
            x0,y0, x1,y1 = val.object.bbox()
            coords = [x0,y0, x1,y1];  str = "G"
            g_nbr = val.object.g_nbr;  g_type = val.o_type
            #print("===== d_type %s, d_id %s, coords %s, str <%s>. g_nbr %s, g_type %s" % (
            #    d_type, d_id, coords, str, g_nbr, g_type))            
        if d_type:
            i_coords = []
            for c in coords:
                i_coords.append(int(float(c)))
            return"(%s %s) %s \"%s\" %s %s" % (
                 d_type, d_id, i_coords, str.replace("\n", "\\n"),
                g_nbr, g_type)
        else:
            print("\a>>> obj_to_save_str, unknown object type <<<")
            exit()
        #self.dump_objects("read_from_rdd")
            
    def save_to_rdd(self, save_file_name):  # Write rfc-draw data (.rdd) file
        # Called from 'Save' r_button, and from rfc-draw.on_closing 
        #print("save_to %s, %d objects" % (save_file_name, len(self.objects)))
        self.drawing.update()
        dw = self.drawing.winfo_reqwidth()
        dh = self.drawing.winfo_reqheight()
        s_file = open(save_file_name, "w")
        root_geometry = self.root.geometry()
        s_file.write("root_geometry %s\n" % root_geometry)
        s_file.write("drawing_size %dx%d\n" % (dw,dh))
        s_file.write("mono_font width 10.333 height 17 pixels\n")
        #self.dump_objects("save_to_rdd()")
        #print(" $  $  $  $  $")
        for j,key in enumerate(self.objects.keys()):
            val = self.objects[key]  # Write objects to .rdd first
            ds = self.obj_to_save_str(val)
            #print(" obj %3d: %s" % (j, ds))
            if ds:
                s_file.write("%s %s\n" % (j, ds))

        for j,key in enumerate(self.objects.keys()):
            val = self.objects[key]  # Now write g_members to rdd
            #print("val = %s" % val)
            if val.o_type == "group":
                ds = self.obj_to_save_str(val)
                #print(" obj %3d: %s" % (j, ds))
                #print("Writing group %d members to rdd" % val.object.g_nbr)
                for m in val.object.g_members:
                    #print("!!! g_m m = >%s<" % m)  ### line here
                    mo = self.rdg.objects[m.oo_key]
                    #print("==> mo >%s<" % mo)  ### group here !!!!!!!!
                    if mo.o_type == "line":
                        r_x = int(mo.object.lbd[0]-val.object.x0)
                        r_y = int(mo.object.lbd[1]-val.object.y0)
                    elif mo.o_type == "text":  # It's a tk text object!
                        t_coords = self.drawing.coords(m.oo_key)
                        r_x = int(t_coords[0]-val.object.x0)
                        r_y = int(t_coords[1]-val.object.y0)
                    elif mo.o_type == "n_rect":
                        r_x = int(mo.object.x0-val.object.x0)
                        r_y = int(mo.object.y0-val.object.y0)
                        #print("--> r_x, r_y = %d, %d" % (r_x,r_y))
                    s_file.write("  (g%d member %d) %s %s\n" % (
                        m.g_nbr, m.oo_key, mo.o_type, [r_x,r_y]))
        
        s_file.close()

    def print_g_members(self, go):
        print("ZZZ g_members: go %s" % go)
        for m in go.g_members:
            mo = self.objects[m.oo_key]
            print("==> mo >%s<" % mo)

    def new_g_member_object(self, ncgo, old_gm):
        #print("@@@   ncgo >%s<" % ncgo)  # group object
        #print("@+@ old_gm >%s<" % old_gm)  # old g_member object  #$ members 1
        old_obj = self.objects[old_gm.oo_key]  # g_member's original object
        #print("+++ old_obj >%s<" % old_obj)
        o_text = old_obj.i_text
        edr_coords = ncgo.i_coords
        #print("??? edr_coords >%s<" % edr_coords)
        if old_obj.o_type == "text" and old_obj.in_n_rect == 0:
            #print("new_g_member_object 'text'")
            #print("o_text >%s<, old_obj.i_coords = %s" % (
            #    o_text, old_obj.i_coords))
            oo_coords = (old_obj.i_coords[0], old_obj.i_coords[1])  ## 795
            #print("  edr_coords >%s<" % ncgo.i_coords)  # group edr
            #print("g_rel_coords >%s<" % old_gm.rel_coords)
            #print("   oo_coords >",end="");  print(oo_coords,end=""); print("<")
            del_x = edr_coords[0] +old_gm.rel_coords[0] -oo_coords[0]
            del_y = edr_coords[1] +old_gm.rel_coords[1] -oo_coords[1]
            #           edr            rel to edr       original object
            #print("   del_x/y = %d/%d" % (del_x,del_y))
            s_coords = self.transform_coords(del_x,del_y, oo_coords)
            #print("    s_coords %s, text >%s<" % (
            #    s_coords, old_obj.i_text))  # OK :-)
            text_id = self.add_to_layer(3, self.drawing.create_text,
                (s_coords), text=o_text, font=self.f_font, anchor=tk.CENTER)
            self.objects[text_id] =  self.object(text_id, text_id, "text",
                s_coords, o_text, ncgo.g_nbr, 0)
            return text_id
        elif old_obj.o_type == "line":
            #print("new_g_member_object 'line'")
            #print("    ++%s++" % old_obj)
            #print("old_obj.lbd >%s<" % old_obj.object.lbd)
            o_text = old_obj.i_text
            #print("o_text >%s<, old_obj.i_coords = %s" % (
            #    o_text, old_obj.i_coords))
            del_x = edr_coords[0] +old_gm.rel_coords[0] -old_obj.i_coords[0]
            del_y = edr_coords[1] +old_gm.rel_coords[1] -old_obj.i_coords[1]
            #           edr            rel to edr       original object
            #print("   del_x/y = %d/%d" % (del_x,del_y))
            s_coords = self.transform_coords(del_x,del_y, old_obj.i_coords)
            #print("    s_coords %s, text >%s<" % (
            #    s_coords, old_obj.i_text))  # OK :-)
            line_id = self.restore_line(s_coords, o_text, ncgo.g_nbr)
                # Uses line o_text to set line options
            return line_id
        elif old_obj.o_type == "n_rect":
            #print("new_g_member_object 'n_rect'")
            #print("    ++%s++" % old_obj)
            #print("   rect_id %s, text_id %s" % (  # old_obj is an n_rect object
            #    old_obj.object.rect_id, old_obj.object.text_id))  #$ rct 1 txt 2
            o_text = old_obj.i_text
            #print("o_text >%s<, old_obj.i_coords = %s" % (
            #    o_text, old_obj.i_coords))
            del_x = edr_coords[0] +old_gm.rel_coords[0] -old_obj.i_coords[0]
            del_y = edr_coords[1] +old_gm.rel_coords[1] -old_obj.i_coords[1]
            #           edr            rel to edr       original object
            #print("   del_x/y = %d/%d" % (del_x,del_y))
            s_coords = self.transform_coords(del_x,del_y, old_obj.i_coords)
            #print("    s_coords %s, text >%s<" % (
            #    s_coords, old_obj.i_text))
            rdo = self.restore_rect(s_coords, o_text, ncgo.g_nbr)  # new n_rect
            # Adds new objects[] at rdo.rect_id and rdo.text_id
            #print("^^^ rdo >%s<" % rdo)  #$ nrect 5, text 6
            #self.dump_objects("After new_g_member_object.restore_rect() call")
            return rdo
                                       
    def copy_g_member(self, ncgo, old_gm):
        #print("        ncgo: >%s<" % ncgo)
        #print("      old_gm: >%s<" % old_gm)  #$ old_gm, key 3, g_rect_id 3, members 1
        old_gmo = self.objects[old_gm.oo_key]
        #print("      type %s" % old_gmo.o_type)  #$ type n_rect
        
        #  Make new objects[] entry for this member
        n_obj_key = self.new_g_member_object(ncgo, old_gm)
        if isinstance(n_obj_key, self.n_rect):  #$ it is an n_rect
            #print("      = back from new_g_member =, n_obj_key %s" % n_obj_key)
            #print("      =    rect_id %d, text_id %d <<<<" % (
            #    n_obj_key.rect_id, n_obj_key.text_id))  # 5, 6
            nr_mo = n_obj_key  # It's an n_rect object
            n_gm = self.g_member(self.rdg, ncgo.object.g_nbr,
                nr_mo.rect_id, nr_mo.rect_id,
                self.objects[nr_mo.rect_id], old_gm.rel_coords)
            #self.dump_objects("After making new n_rect g_member")
        else:
            obj =  self.objects[n_obj_key]  # Old object
            n_gm = self.g_member(self.rdg, ncgo.object.g_nbr,
                n_obj_key,  # oo_key
                n_obj_key,  # g_tk_id
                obj,        # g_object
                old_gm.rel_coords)  # g_rel_coords
            #print("**copy_g_member: n_gm = %s" % n_gm)
            edr_coords = self.screen_coords(n_gm.g_object.i_coords,
                old_gm.rel_coords)
            #print("  g_m edr_coords: %s" % edr_coords)
            if obj.o_type == "text":
                pass
                #print("<>copy_g_member: g_tk_id = %d" % n_gm.g_tk_id)
                #if n_gm.g_tk_id == 0:
                    #print("Don't need to draw text here ???")
            elif obj.o_type == "line":
                pass
                #print("  g_m edr_coords: %s" % edr_coords)
                #print("copy_g_member:  line %s" % obj)            
        #print("eee n_gm >%s< end of copy_g_member()" % n_gm)
        return n_gm

    def copy_object(self, obj):
        #print("copy_object: %s" % obj)
        offset = 25;  o_coords = []
        if obj.o_type == "text":
             coords = self.drawing.coords(obj.key)
             for c in coords:
                o_coords.append(c-offset)
             c_text = self.drawing.itemcget(obj.key, "text")
             self.restore_text(o_coords, c_text, 0)
        elif obj.o_type == "line":
            coords = obj.object.bbox()
            for c in coords:
                o_coords.append(c-offset)
            self.restore_line(o_coords, "L", 0)  # coords, text, g_nbr
        elif obj.o_type == "n_rect":
            coords = obj.object.bbox()
            for c in coords:
                o_coords.append(c-offset)
            self.restore_rect(o_coords, obj.object.text, 0)
        elif obj.o_type == "group":
            #print("-0- original object (obj) %s" % obj)
            #self.print_g_members(obj.object)
            coords = obj.object.bbox()
            for c in coords:
                o_coords.append(c-offset)
            #print("-1- copy_ group")
            g_rect_id = self.restore_group(o_coords, "")
                # Makes new group object using next-avail g_nbr, no members yet
            #print("-2- g_rect_id = %d" % g_rect_id)  # group 2's edr
            ncgo = self.objects[g_rect_id]  # Newly Copied Group Object
                #   (obj is the original group object)
            #print("-2.5- ncgo = %s" % ncgo)  #$ ncgo key 4, group 2
            #self.dump_objects("-+- after restore_group")
            
            #print("@4 g_members")
            #print("    g_members |%s|" % obj.object.g_members)
            for ogm in obj.object.g_members:  # Members of original object
                #print("   -3- ogm |%s|" % ogm)  #$ ogm key 3, group 1 , g_rect_id 3
                #  #-2-
                o_key = ogm.oo_key
                obj = self.objects[o_key]
                #print("   -4- obj = %s +%s+" % (o_key, obj))  #$ ogm key 1, n_rect 1
                if o_key in ncgo.object.g_members:
                    print("\a   XXX obj already in g_members XXX")
                else:
                    #if obj.o_type == "n_rect":  #$ it's an n_rect
                    #    print("n_rect in group, %s" % ogm)
                    n_gm = self.copy_g_member(ncgo, ogm) #$ ncgo= new grp's obj
                    #print("   === n_gm = %s" % n_gm)  #$ n_gm key 
                    ncgo.object.g_members.append(n_gm)
                    #print("   === ncgo.object = %s" % ncgo.object)
                    gm_len = len(ncgo.object.g_members)  #$ member 1,should be 5
                    #print(   "=== gm_len %d" % gm_len)
                    if  gm_len > 3:
                        #print("len(g_members) = %d" % gm_len)
                        self.print_g_members(ncgo.object)
            #print("abcd: ncgo = >%s<" % ncgo)
            #print("ncgo.g_members: len %d" % gm_len)
            self.objects[g_rect_id] = ncgo  ############### ????
            #for ogm in ncgo.object.g_members:
            #    print("    %s" % ogm)
            #self.dump_objects("-+- after ncgo completed")

            #self.draw_group(ncgo.object)
            print("= = = = =")
                
            #--1--
            g_key = obj.key
            #print("-4- after restore_group, group >%s<" %
            #      self.objects[g_key].object)
            #print("$$ group now <%s>" % self.objects[g_key].object)
            #self.dump_objects("After restore_group")
            ##exit()
        else:
            print("\aobj >%s< ???" % obj)
            exit()

    def str_h_w(self, str):  # Find height and width of (monospace) str
        if str[-1] == "\n":
            str = str[0:-1]
        lines = str.count("\n")+1
        la = str.split("\n")
        mx_len = 0;  fm = None
        for line in la:
            if len(line) > mx_len:
                mx_len = len(line)
        height = max(1, lines/2);  width = max(1, mx_len/2)
        #print(">%s<" % str)
        #print("h %d, w %d" % (height, width))
        return height, width  # 0.5 of h and w (i.e. centre to edges) !!!
 
    def edit_text_object(self, txt_obj):  # txt_obj is an objects[] entry
        #????self.text_id = txt_obj.object  # rfc-draw text object is it's tk id
        self.text_id = txt_obj.key  # rfc-draw text object is it's tk id
        # Open new window to edit the text, then press Esc
        #   tkinter text object uses Home and End to position cursor!
        #print(">>> edit_text_object: centre_texts = %s" % self.centre_texts)
        self.text_window = tk.Tk()
        self.text_window.title("Edit text object")
        root_geometry = self.root.geometry()
        rg_plus = root_geometry.split("+")
        rg_x = rg_plus[0].split("x")
        #print("root geometry %s x %s at %s,%s" % (
        #    rg_x[0], rg_x[1], rg_plus[1], rg_plus[2]))
        igx = int(rg_x[0]);  igy = int(rg_x[1])
        locx = int(rg_plus[1]);  locy = int(rg_plus[2])
        tw_geometry = "%dx%d+%d+%d" % (igx/2,igy/2, locx+igx+50, locy+igy/5)
        self.text_window.geometry(tw_geometry)

        # User can edit the text in text_window, then press Escape
        # >> Can't use End or Home, tk.Text uses these in tk.Text window <<
        c_text = self.drawing.itemcget(self.text_id, "text")
        # Open new window to edit the text
        self.text_edit = tk.Text(self.text_window,
            bg="white", fg="black", font=self.f_font)
        self.text_edit.pack(fill=tk.BOTH, expand=True)
        self.text_edit.insert('1.0', c_text)
        self.text_edit.focus_set()
        self.text_edit.bind("<Escape>", self.edit_esc_key)

    def rdg_closest(self, mx,my):
        #print("rdg_closest(): mx,my = %d,%d" % (mx,my))
        item = self.drawing.find_closest(mx,my) 
        if len(item) == 0:  # Empty tuple
            #print("rdg_closest(0): empty tuple")
            return None, None
        item_id = item[0]
        item_type = self.drawing.type(item_id)
        print("@@@ rdg_closest, item_id %d, type %s" % (item_id, item_type))
        #print("@ln@ closest(1): item %s (%s), mx,my %d,%d" % (
        #    item, item_type, mx,my))
        if item_id in self.objects:
            obj = self.objects[item_id]  # item_id is a tkinter object id
            # object (e.g. rdo) has: key, obj, obj_ type, in_n_rect
            #print("-> closest %s is in objects, obj >%s<" % (item, obj))
            return item, obj
        else:  # Not in objects ??
            print("\a@@@ item %d is not in rdg.objects <<<<" % item_id)
            return None, None

    def on_key_press_repeat(self, event):
       self.has_prev_key_press = True
       self.drawing.after(150, self.on_key_press, event)
       #print("on_key_press_repeat >%s<" % repr(event.char))
   
    def on_key_press(self, event):
        self.has_prev_key_press = False
        self.last_key = key = event.char
        #print("key_press: %s, current_obj >%s<" % (key, self.current_object))
        if key == "c":  # Copy a tk object
            self.copy_object(self.current_object)
        """
        else:
            #if self.last_button != "line":
            #    print("\a>> Must be in Line mode to flip or reverse object")
            #    return
            self.dlt = dlc.draw_lines(self.drawing,
                self.current_object.object.lbd, self.rdg)
            #abd = alc.a_line(self.drawing,  # Starts a new line, don't use it!
            #    self.current_object.object.lbd, self.rdg)
            abd = self.current_object.object  # Works on current line

            if key == "r":
                self.dlt.reverse_line()  # Arrows in opposite direction
            elif key == "f":
                self.dlt.flip_line()
            elif key == "=":
                self.dlt.equal_end_coords()
            elif key == "e":  # syntax End
                self.dlt.syntax_end(True)
            elif key == "b":  # Bare end
                self.dlt.syntax_end(False)
            elif key == "a":
                abd.set_arrows(key)
            elif key == "n":
                abd.set_arrows(key)
        """
    def on_b3_click(self, event):  # b3 (Right button) to edit a text object
        mx, my = (event.x, event.y)  # Mouse position
        item, obj = self.rdg_closest(mx,my)
        #print(": : : item %s, obj %s" % (item, obj))
        if item:
            item_x = item[0]
            item_type = self.drawing.type(item_x) 
            if item_type != "text":        
                print("\aYour b3 click was not on a text object!")
            else:
                #print("b3_click: obj = %s" % obj)
                self.edit_text_object(obj)

    def justify(self, str, rq_len):
        la = str.split("\n")
        mx_len = 0;  fm = None
        for line in la:
            if len(line) > mx_len:
                mx_len = len(line)
        self.w2 = max(mx_len/2, 1)
        j_text = ""
        for line in la:
            if line[0] != " ":
                pb = max(int(self.w2 - len(line)/2), 0)
                pad = ' '*pb
                j_line = pad+line
            else:  # Don't justify lines starting with blank
                j_line = line
            j_text += j_line+"\n"
        return j_text[0:-1]

    def edit_esc_key(self, event):  # Edit text in pop-up window
        # self.text_edit  is a tk.Text object
        # self.text_id is a create_text object, in objects[] key self.text_id
        new_text = self.text_edit.get('1.0','end-1c')
        print("@@@ new_text >%s<" % new_text)
        
        if self.centre_texts:
            self.h2, self.w2 = self.str_h_w(new_text)
            new_text = self.justify(new_text, self.w2)
            # justify() adds leading spaces to centre all new_text's lines
        #print("new_text = >%s<" % new_text)
        self.text_edit.delete('1.0', 'end')
        self.text_edit.insert('1.0', new_text)

        self.drawing.itemconfigure(self.text_id, text=new_text,
            font=self.f_font)
        # Put edited text back into tk object and it's objects entry
        t_obj = self.objects[self.text_id]
        if t_obj.in_n_rect != 0:  # Text in n_rect
            self.objects[t_obj.in_n_rect].i_text = new_text
        else:
            self.objects[self.text_id].i_text = new_text
        self.text_window.destroy()  # Close the editing window

    def delete_object(self, obj):
        #print("  obj to delete = %s" % obj)
        del self.objects[obj.key]  # Delete object from dictionary
        #print("deleted_objects = >%s<" % self.deleted_objects)
        if obj.o_type == "line":
            obj.object.destroy_line()
        elif obj.o_type == "n_rect":
            obj.object.delete()
        elif obj.o_type == "group":
            obj.object.delete()
        elif obj.o_type == "text":
            self.delete_text(obj.object)  # object is just a text id

    def on_next_key(self, event):  # Pg Dn key pressed
        self.display_msg("", "normal")  # Clear message area

    def on_delete_key(self, event):  # Delete key pressed
        mx, my = (event.x, event.y)  # Mouse position
        #print("on_delete_key(): mx,my = %d,%d" % (mx,mx))
        item_ix, d_obj = self.rdg_closest(mx,my)
        if d_obj:
            #print("about to delete %s" % d_obj)
            #input()
            print("Deleting >%s< (%s)" % (d_obj, d_obj.o_type))
            self.deleted_objects.append(d_obj)
            ##print("deleted_objects >%s<" % self.deleted_objects)
            self.delete_object(d_obj)
        else:
            print("\a    Not in objects ???")

    def on_insert_key(self, event):  # Insert key pressed
        print("len(self.deleted_objects) = %d" % len(self.deleted_objects))
        if len(self.deleted_objects) == 0:
            self.display_msg("No deleted objects", "warning")
        else:
            d_obj = self.deleted_objects.pop()
            print("inserting d_obj = >%s< (%s)" % (d_obj, d_obj.o_type))
            obj_type = d_obj.o_type
            text = d_obj.i_text;  g_nbr = d_obj.g_nbr
            if obj_type == "n_rect":
                x0,y0, x1,y1 = d_obj.object.bbox()
                self.restore_rect([x0,y0, x1,y1], text, g_nbr)
            else:
                coords = d_obj.i_coords
                print("@@@ coords >%s<, text >%s<" % (coords, text))
                if obj_type == "text":
                    self.restore_text(coords, text, g_nbr)
                elif obj_type == "line":
                    self.restore_line(coords, text, g_nbr)
                elif obj_type == "group":
                    self.restore_group(coords, text)

    def dg_b3_click(self, event):
        self.drawing.after(250, self.mouse_action, event)
            # Delay to allow for double-click

    def dg_b3_double(self, event):
        self.double_click_flag = True

    def mouse_action(self, event):
        if self.double_click_flag:
            #print('double mouse click event')
            self.double_click_flag = False
            dgr.draw_groups.edr_to_group(self, event)  # rdg is self here!

        else:  # B3 (right button) to edit a Text
            #print('single mouse click event')
            if self.ln_mode == "group":
                print("\aCan't edit a Text in 'group' mode!")
            else:
                self.on_b3_click(event)
