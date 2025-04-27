# 1409, Sat 16 Mar 2024 (NZDT)  # v2
# 1531, Sat 21 Oct 2023 (NZDT)  # v1
#
# rfc_draw_globals_class:
#                   contains rfc-draw global data (for event handlers)
#                   and functions for Objects, e.g.
#                      class object (rfc_draw objects)
#                      object dictionary, get_object()
#                  
# Copyright 2024, Nevil Brownlee, Taupo NZ

import os.path, re, sys, time, datetime, threading
import faulthandler
import pygame  # playsound doesn't work on nebbiolo, sigh
global posix
try:
    posix = True
    import termios  # This is POSIX
except:
    posix = False
    import msvcrt   # This is Windows

import tkinter as tk


import draw_texts_class as dtc    # Handles text objects
import arrow_lines_class as alc   # Draw lines with direction arrows
import draw_lines_class as dlc    # Handles line objects
import draw_n_rects_class as drc  # Handles n_rect objects
import draw_headers_class as dhc  # Handles rfc-draw headers

class rdglob:  # Global variables for rfc-draw's objects
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)  # New instance of rdglob

    def __init__(self, parent, root, m_text):
        super().__init__()
        self.drawing = parent;  self.root = root;  self.m_text = m_text
        self.rdg = self
        print(">>> m-text = >%s<" % self.m_text)
        
        #self.f_font = tk.font.Font(  # Initialise class variables
        #    family= TkFixedFont)  # This doesn't work, below version does <<<
        self.f_font = "TkFixedFont"  # Looks fine, but a bit too light
        #self.f_font = ('TkFixedFont', 12)  # , 'bold')  # Too tightly spaced
        #self.f_font = ('Courier Prime Code', 10)  # Too tightly spaced
        #self.f_font = ('Monospace Medium', 10) #, 'bold')  # ditto
        #self.f_font = ('Droid Sans Mono', 10) #, 'bold')  # OK
        #self.f_font = ('Nimbus Mono', 10, 'bold') # Google  # Too small
        #self.f_font = ('Noto Sans Mono', 10)  # Google sort of OK
        #self.f_font = ('Space Mono', 10) #, 'bold')  # Google, r,i i different
        #self.f_width = 10.333;  self.f_height = 17  # points on screen
        self.f_width = 8;  self.f_height = 17  # px, from header experiments

        pygame.mixer.init()

        self.new_drawing = False  # True if we have a save_file name
        
        self.last_button = "rect"
        self.last_key = ""
        self.last_mode = "rect"

        self.m_text.tag_configure('normal', foreground="black")
        self.m_text.tag_configure('warning', foreground="deepskyblue2")
        self.m_text.tag_configure('error', foreground="red3")

        self.objects = {}  # (draw_objects) objects, key (tk object) id
                           #   Text in an n_rect is part of that n_rect
        self.current_object = None  # Key to actual object in self.objects

        self.obj_keys = {}  # old-key -> new-key for objects read from rdd
    
        self.deleted_objects = []  # Objects deleted (using Delete key)

        self.rects_drawn = 0

        # Patterns for reading the description string for an object
        #   . matches any character, except a newline (\n)

        rere_0_4 = r"(\d+)\s+\((.+)\s+(.+)\)\s+\[(.+)\]\s+\"(.+)\"" # Raw string
            # field   0        1      2          3          4
            #       objid    type    skey       coords     text 

        rere_v1 = rere_0_4 + r"\s+(\S)\s+([\s\S]+)\Z" # Raw string
        print("*** rere_v1 %s" % rere_v1)
        ###rere_v1 = rere_0_4 + "\s+(.+)\s+(.+)\Z"
            # rdd v1:              5      6
            #                     g_nbr  g_type
            #                   '0  N' or '1 group'

        rere_v2 = rere_0_4 + r"\s+(\S+)\s+(\S+)\s+(\S+)(\s.+)?" # Raw string
            #                      5       6       7      8
            #              parent_id,     v1,     v2    Optional comment
        self.rdd_e_v1 = re.compile(rere_v1)
        self.rdd_e_v2 = re.compile(rere_v2)

        self.last_tag = None  # Tag of last-clicked object
        self._layers = []  # For add_to_layer()

        self.mx_headers = 4
        self.hd_colours = ["tan2", "saddlebrown", "red", "darkorange",
            "gold", "green", "darkblue", "indigo", "darkviolet"]    # Dark
        self.hl_colours = ["tan1", "peru", "tomato", "kakhi", "palegoldenrod",
            "palegreen", "skyblue", "royalblue", "palevioletred"]   # Light
        self.h_colours = self.hd_colours
 
        # n_rect variables
        self.tl   = 0;     self.top = 1;     self.tr = 2  # Mouse regions
        self.left = 3;  self.middle = 4;  self.right = 5
        self.ll   = 6;     self.bot = 7;     self.lr = 8
        self.far  = 9  # Too far away from closest rect
        self.new = 10  # Drawing a new rectangle
        self.region = self.lr  # Region mouse pointer is currently in
        self.pos = ["tl",   "top",  "tr",
                  "left", "middle", "right",
                    "ll", "bottom", "lr",  "far", "new"]
        self.res_px = 5  # Nearness margin ** was 4
        self.far_px = 8  # This far away to start a new rect
        self.hdr_px = 2  # Min up/down change to detect row-bottom dragging
       
    # Click b3 to edit a text object
    
        self.new_ids = {}  # For restore_saved_object
        
        self.drawing.bind_class('Canvas','<ButtonPress-3>', self.on_b3_click)

        self.centre_texts = True  # Set by draw_* set_event_handlers()

        self.root.bind("<Delete>", self.on_delete_key)  # Bind to root works
                                             # bind to Canvas *doesn't* work
        self.root.bind("<Insert>", self.on_insert_key)
        self.root.bind("<Next>", self.on_next_key)  # Pg Dn

        self.bind_keys()

        self.dlc_tool = dlc.draw_lines(self.drawing, self.root, self.rdg)
        self.dtc_tool = dtc.draw_texts(self.drawing, self.root, self.rdg)
        self.drc_tool = drc.draw_n_rects(self.drawing, self.root, self.rdg)
        self.dhc_tool = dhc.draw_headers(self.drawing, self.root, self.rdg)
        print("rgdc, self.dhc_tool %s" % self.dhc_tool)
        #print(">>> m-text = >%s<" % self.m_text)

        self.start_t = datetime.datetime.now()

    def time_now(self, where_from):
        t_now = datetime.datetime.now()
        t_diff = datetime.timedelta.total_seconds(t_now-self.start_t)
        ts = "%s" % t_diff
        print("in time_now: ts %s" % ts)
        pix = ts.index(".") 
        print("ELAPSED %s: %s" % (ts[0:pix+4], where_from))

    def where(self, rdo, x, y):  # Find region of rdo where b1 is pressed
        print("... ... where: rdo = %s, type %s" % (rdo, type(rdo)))
        #print("where:  coords %d,%d, %d,%d" % (rdo.x0,rdo.y0, rdo.x1,rdo.y1))
        if y <= rdo.y0 - self.res_px:  # Top row
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
        elif y >= rdo.y1 + self.res_px:  # Bottom row
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
        """
        def test_fn(self):
            print("$$$ from rdglob.test_fn")
        self.test_v1 = "12345"
        self.test_v2 = "67890"

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

    def bind_keys(self):
        #print("@@@@ posix = %s" % self.posix)
        if posix:
            # Clear queued key-presses on POSIX
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)        
        else:
            # Clear queued key-presses on Windows
            while msvcrt.kbhit():
                msvcrt.getch()
        self.root.bind('<KeyPress>', self.on_key_press_repeat)
        self.has_prev_key_press = None
        self.root.bind('<Escape>', self.on_key_press_repeat) # Clear Msg window
        self.root.bind('<KeyPress-c>',self.on_key_press_repeat) # copy
      
    def unbind_keys(self):        # Unbind keys used by
        print("rdg unbind_keys called <<<")
        self.root.unbind('<KeyPress-c>')  # rdglob.copy
        self.root.unbind('<KeyPress-a>')  # draw_lines_class
        self.root.unbind('<KeyPress-n>')  #        "
        self.root.unbind('<KeyPress-e>')  #        "
        self.root.unbind('<KeyPress-b>')  #        "
        self.root.unbind('<KeyPress-f>')  #        "
        self.root.unbind('<KeyPress-r>')  #        "
        self.root.unbind('<KeyPress-equal>')  #    "
        self.root.unbind('<KeyPress-plus>')
        self.root.unbind('<KeyPress-minus>')

    def big_bell(self):
        pygame.mixer.music.load("BSB-counter-bell.wav")
        pygame.mixer.music.play(loops=0)


    def small_bell(self):
        pygame.mixer.music.load("BSB-small-bell.wav")
        pygame.mixer.music.play(loops=0)
        
        
    def display_msg(self, text, tag):  # Display text in Message area
        # tags are declared above, i.e. 'normal' and 'error'
        print("?=-=-=-=-= starting display_msg(%s), tag %s" % (text, tag))
        self.m_text.delete('1.0', tk.END)
        self.m_text.insert('1.0', text, tag)
        #print("\a")  # BEL without using .wav sound
        if tag == "error":
            self.big_bell()
        elif tag == "warning":
            self.small_bell()

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
        def __init__(self, key, obj, obj_type, coords, text, parent_id, v1, v2):
            #obj_debug = True
            #if obj_debug:
            #    s = "OBJECT: key %s, obj %s, obj_type %s, coords %s, " 
            #    s +="text %s, parent %s, v1 %s, v2 %s"
            #    print(s % (key, obj, obj_type, coords, text, parent_id, v1, v2))
            self.key = key             # 0 key to self.objects
            if not obj:
                print("a_obj = None");  x = 11/0
            self.a_obj = obj           # 1  Actual object
            #    print("a_obj: str() failed") 
            #print("&&&  a_obj %s (%s)" % (obj, type(obj)))
            self.o_type = obj_type     # 2 Object type
            self.i_coords = coords     # 3 Initial x,y coords (from rdd)
            self.i_text = text         # 4 Initial text (from rdd)
            self.parent_id = parent_id # 5 == 0 -> it's just a tk object
                                #  != 0 -> n_rect's key for it's rectangle
                                #         don't write to save-file.rdd
            self.v1 = v1               # 6
            self.v2 = v2               # 7

        def __str__(self):
            s = "<Key %s, Object %s, Type %s, I_coords %s, "
            s += "i_text %s, parent_id %s v1 %s, v2 %s>"
            ##print("@@ object, s >%s<" % s)
            """
            print("self.key %s" % self.key)
            print("self.a_obj ", end="");  print(self.a_obj)
            print("self.o_type %s" % self.o_type)
            print("self.i_coords = ", end="");  print(self.i_coords)
            print("self.i_text %s" % self.i_text)
            print("self.parent_id %s" % self.parent_id)
            print("self.v1 %s" % self.v1)
            print("self.v2 %s" % self.v2)
            #"""
            rs = s % (self.key, self.a_obj, self.o_type, self.i_coords,
                self.i_text, self.parent_id, self.v1, self.v2)
            ##print("->> object str() rs = %s" % rs)
            ##print("type(rs) %s" % type(rs))
            ##exit()
            return rs
            
    def set_mode(self, which): # Rect/Text/Line/Header buttons use this
        self.last_button = which  #  last_mode changes within Line mode
        ##if self.last_mode == "header":  # Returning to rect, line or text
        ##    self.drawing.bind_class('Canvas','<Button-3>', self.on_b3_click)
        self.last_mode = which
        #print("in rdg: self.last_mode now = %s" % self.last_mode)
        if which == "line":
            self.last_mode = "line"

    def obj_to_str(self, val):
        print("??? obj_to_str: val >%s<" % val)
        if val.o_type == "n_rect":
            return val.obj.mk_save_str(val)
        if val.o_type == "text":
            coords = self.drawing.coords(val.obj)
            str = self.drawing.itemcget(val.obj, "text")
            return"(%s, %s) %s \"%s\" 0, 0, 0" % (
                "text", val.obj, coords, str)
        elif val.o_type == "line":
            #coords = val.obj.lbd
            #lbd_id = val.obj.lbd_id
            #return "(%s %d) %s" % ("a_line", lbd_id, coords)
            #print("@@@ line: about to call val.obj.mk_save_str()")
            print("    %s" % val.obj)
            return val.obj.mk_save_str(val)
        elif val.o_type in ["header", "row", "field", "bar"]:
            print("obj_to_str: hdr object >%s<" % val.obj)
            o_ss = val.obj.mk_save_str(val)
            print("%s o_ss >%s<" % (val.o_type, o_ss))
            return o_ss
        else:
            print(">> obj_to_str, val %s" % val)
        return None  # Unknown type
    
    def get_save_string(self, val):  # For object val
        #$print("get_save_string: val %s" % val)
        if val.o_type == "text":
            # Texts use an integer instead of an object!
            ds = self.dtc_tool.mk_save_str(val)
            ##$return ds  #$$s_proc("%d %s" % (j, ds))
        elif val.o_type == "header":
            #$print("?.?.? val >%s<" % val)
            #$if val.o_type != "header":
            #$    print("$$$ val >%s<" % val)
            ds = self.dhc_tool.header.mk_save_str(self, val)
            #$print("***header save_string >%s" % ds)
        elif val.o_type == "row":
            #print("ROW mk_save_string, dhc_tool.row >%s" % self.dhc_tool.row)
            ds = self.dhc_tool.row.mk_save_str(self, val)
            #$print(">?>? ds >%s<" % ds)
        elif val.o_type == "field":
            #$print("&&&& get_save_string, o_type field, val >%s<" % val)
            ds = self.dhc_tool.field.mk_save_str(self, val)
            #$print("&*&* ds >%s<" % ds)
            #4if ds == "no_col_nbrs":
            #4    print("field ds: no_col_nbrs")
        elif val.o_type == "bar":
            ds = self.dhc_tool.bar.mk_save_str(self, val)
        else:
            print("???? val: %s" % val)
            ds = val.a_obj.mk_save_str(val)
            print("   ds: >%s<" % ds)
        #$print("get_save_string >%s<" % ds)
        return ds
    
    def dump_objects(self, heading):
        ###return  # Disable dumps !
        print("dump_objects -- %s --" % heading)
        if len(self.objects) == 0:
            print("!!! self.objects is empty !!!")
            return
        j = 0
        for key in self.objects:
            val = self.objects[key]
            j += 1
            #$print("!@!@ j %d, val %s" % (j, val))
            ds = self.get_save_string(val)
            #$print("%d %s" % (j, ds))
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
        #print(">> add_to_layer(%d, %s, %s  | %s <<" % (
        #    layer, command, coords, kwargs))
        layer_tag = "layer %s" % layer
        if layer_tag not in self._layers: self._layers.append(layer_tag)
        tags = kwargs.setdefault("tags", [])
        #print("ADD_TO_LAYER: tags %s (%s)" % (tags, type(tags)))
        tags.append(layer_tag)
        item_id = command(coords, **kwargs)
        tags = self.drawing.gettags(item_id)
        #print("add_to_layer %d: tags "% layer, end="");  print(tags)
        self._adjust_layers()
        return item_id

    def _adjust_layers(self):
        for layer in sorted(self._layers):
            self.drawing.lift(layer)

    def delete_text(self, text_id):
        self.drawing.delete(text_id)
    
    """
    def mk_visible(self, id, visible):
        if visible:
            self.drawing.itemconfigure(id, state=tk.NORMAL)
        else:
            self.drawing.itemconfigure(id, state=tk.HIDDEN)
    """
    def read_from_rdd(self, fn):
        print("+++ read_from_rdd file >%s<" % fn)
        last_mode = 'rect'
        self.fn = fn
        if not os.path.isfile(fn):  # No save_file
            self.display_msg("New drawing, will write %s on closing" % fn, \
                "normal")
            self.new_drawing = True;
            print("self.rdg.fn >%s<" % self.fn)
        else:  # save_file exists
            if fn == "save-file.rdd":
                self.display_msg("File save-file.rdd exists!", "warning")
            else:
                self.display_msg("Read rdd file %s" % fn, "normal")
            ##  10.333 px width, 17 px height work well for TkFixedFont !
            self.f_width = 10.333;  self.f_height = 17  # From test-font.py
            f = open(fn, "r")
            self.new_drawing = False;    
            for line in f:
                ds = line.rstrip('\n')
                #print("read_from_rdd: ds >%s<" % ds)
                if len(ds) == 0:  # Empty line
                    continue
                if ds[0] == "#":  # Comment line
                    continue
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
                elif ds.find("last_mode") >= 0:
                    la = ds.split(" ")
                    last_mode = la[1]
                    print("last_mode found >%s<" % last_mode)
                else:
                    #  rere_v* patterns expect ds to start with line nbr!
                    #print("=+-+= ds = %s f.obj" % (ds))
                    #print("about to call restore_object(ds)")
                    #  Have to know what type of object it is!
                    self.restore_saved_object(ds)
                        # OK to here
                        #print("=== back from restore_object")
            self.display_msg("Drawing read from: %s" % fn, 'error')
            # Use tag 'error' to make small bell sound here
        self.dump_objects("Read all rdd lines")
        #print("self.obj_keys >%s<" % self.obj_keys)
        #for old, new in self.obj_keys.items():
        #    print("??? old %d -> new %s" % (old, new))
        #print("last_mode %s (%s)" % (last_mode, type(last_mode)))
        return last_mode
        
    def save_to_rdd(self, save_file_name):  # Write rfc-draw data (.rdd) file
        # Called from 'Save' r_button, and from rfc-draw.on_closing 
        print("save_to %s, %d objects" % (save_file_name, len(self.objects)))
        print(r"/\/\/ len(objects) = %d" % len(self.objects))
        self.dump_objects("about to save rdd file")
        self.drawing.update()
        dw = self.drawing.winfo_reqwidth()
        dh = self.drawing.winfo_reqheight()
        s_file = open(save_file_name, "w")
        root_geometry = self.root.geometry()
        s_file.write("root_geometry %s\n" % root_geometry)
        s_file.write("drawing_size %dx%d\n" % (dw,dh))
        s_file.write("mono_font width 8 height 17 pixels\n")
        s_file.write("last_mode %s\n" % self.last_mode)
        self.dump_objects("save_to_rdd()")
        print(" $..$..$")

        j = 0
        for key in self.objects.keys():
            j += 1
            val = self.objects[key]  # Write objects to .rdd first
            # Don't write text with n_rect parent to rdd!
            if val.o_type != "text" or val.parent_id == 0:
                state = self.rdg.drawing.itemcget(key, "state")
                # returns "hidden", rather than tk.HIDDEN !!!
                print(":+0: j %d, key %s, save_to_rdd: val >%s< %s state %s" % (
                    j, key, val, val.i_coords, state))
                if state != "hidden":
                    ds = self.get_save_string(val)
                    if not ds is None:
                        print("$@j %d, ds >%s<" % (j, ds))
                        s_file.write("%d %s\n" % (j, ds))

    def new_text(self, mx, my, t_text, parent_id):
        text_id = self.add_to_layer(3, 
            #self.drawing.create_text, (mx,my), fill="green", text=t_text,
            self.drawing.create_text, (mx,my), text=t_text,
               font=self.f_font, anchor=tk.CENTER, activefill="red")
        text_obj = self.a_obj(
            text_id, text_id, "text", [mx,my], t_text, parent_id, 0)
        self.objects[text_id] = text_obj
        self.current_object = text_obj
        return text_obj

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

    def parse_rdd_line(self, line):
        line = line.rstrip()
        #print("@@@ line = %s @@@" % line)
        if self.rdd_e_v2.match(line):  # v2 match (9 fields)
            m = self.rdd_e_v2.split(line)
            #print("v2 split %s len %d" % (m, len(m)))
            return m[1:-1]
        #else:
        #    print("v2 match failed");  exit()
        elif self.rdd_e_v1.match(line):  # v1 match (6 fields)
            m = self.rdd_e_v1.split(line)
            #print("v1 split %s len %d" % (m, len(m)))
            return m[1:-1]
        else:
            print("v1 match failed")
            print("line >%s<" % line);  exit()
        return None

    def restore_saved_object(self, ds):
        #print("restore_saved_object: ds >%s<" % ds)
        fields = self.parse_rdd_line(ds)
        print("fields >>> %s <<< len %d" % (fields, len(fields)))
        ##print("0: >%s< %s" % (fields[0], type(fields[0])))
        obj_id = int(fields[0])  # Ignore line_nbr (field 0)
        o_type = fields[1]  ## 'n_rect'
        s_key = fields[2]  # object's key in save file
        coords = self.s_to_ilist(fields[3])
        text = fields[4].replace("\\n", "\n")
        #text = text.replace('\\"', '"')
        #print("fields[5] %s" % fields[5])
        parent_id = int(fields[5])
        print("parent_id %s (%s)" % (parent_id, type(parent_id)))
        if parent_id != 0:
            parent_id = int(self.obj_keys[parent_id])
            print("@@ new parent_id %s" % parent_id)
        print(">> fields[6] >%s<" % fields[6])  # v1
        if fields[6] == "N":  # v1 rdd file
            v1 = v2 = 0
        else:
            print("+++>>> fields[6] >%s<" % fields[6])
            v1 = int(fields[6].strip('"'))  # Remove any surrounding " chars
            #print("v1 %s (%s)" % (v1, type(v1)))
            if len(fields) == 9:  # v2 match (Optional comment is fields[8])
                v2 = int(fields[7])
                print("o_type %s, v1 %d, v2 %d" % (fields[1], v1, v2))
            else:
                print("rdd pattern match failed !!!");  exit()
            #print("v2 %s (%s)" % (v2, type(v2)))

        # v1 and v2 are for header, row and field objects
        print("RSO: %s %s %s >%s< %d %d %d" % (
            o_type, s_key, coords, text, parent_id, v1,v2))
        # dhc_tool needs o_type
        #print("restore_saved_object: o_type >%s<" % o_type)
        old_key = int(fields[2])
        if o_type == "line":     # layer 1
            t = self.dlc_tool
            r_obj = t.restore_object(coords, text, parent_id, v1, v2)
            new_key = r_obj.key
        elif o_type == "text":   # layer 3
            t = self.dtc_tool
            r_obj = t.restore_object(coords, text, parent_id, v1, v2)
            new_key = r_obj.key
        elif o_type == "n_rect": # layer 2
            t = self.drc_tool  #  Above three are classes <<<
            r_obj = t.restore_object(coords, text, parent_id, v1, v2)
            new_key = r_obj.key
        elif o_type == "header":  # Nothing drawn for a header
            t = self.dhc_tool
            #print("::: text %s, parent_id %d" % (text, parent_id))
            h_clo = dhc.draw_headers.header(
                self.drawing, self.root, self.rdg, v1, coords, v2)
            if v2 == 1:  # no_col_nbrs
                self.rdg.drawing.itemconfigure(
                    h_clo.hdr_id, state=tk.HIDDEN)  # hdr top (white) line
            dhc.draw_headers.headers.append(h_clo)
            h_key = h_clo.hdr_id
            h_rdo = self.object(h_key, h_clo, "header",
                coords, text, parent_id, v1, v2)
            print("- - - h_rdo >%s<" % h_rdo)
            self.objects[h_key] = h_rdo
            new_key = h_key
            print("@@ rso: h_key %d, h_rdo %s" % (h_key, h_rdo))
            self.rdg.dump_objects("restored header <<<")
        elif o_type == "row":
            h_rdo = self.objects[parent_id]
            print("row's h_rdo %s" % h_rdo)
            h_clo = h_rdo.a_obj
            ##print("+=+= r_clo >%s<" % r_clo)
            h_rdo = self.objects[h_clo.hdr_id] # was .hdr_id
            print("$$ $$ restoring row, v2 %s (%s)" % (v2, type(v2)))
            r_clo = dhc.draw_headers.row(self.drawing, self.rdg, h_clo, v2)
            if v2 < 0:
                r_clo.vbl_len_row = True
            new_key = r_clo.row_id
            ###r_obj = t.restore_object(coords, text, parent_id, v1, v2)
        elif o_type == "field":
            #self.dump_objects("About to restore field <<<")
            r_rdo = self.objects[parent_id] ###.a_obj  # field's row
            #print("r_rdo >%s<" % r_rdo)
            r_clo = r_rdo.a_obj
            h_clo = r_clo.h
            f_clo = dhc.draw_headers.field(self.rdg,
                h_clo, r_clo, text, v1, v2, None)  # f_col, width
            f_rdo = self.objects[f_clo.text_id]
            new_key = f_clo.text_id
            #print("@@ rso: f_rdo %s" % f_rdo)
            ###r_obj = t.restore_object(coords, text, parent_id, v1, v2)
        else:
            print("Unknown object type %s, can't restore it!" % o_type)
            exit()
                
        self.obj_keys[old_key] = new_key
        #print("=+= %s -> %s" % (old_key, new_key))

        #self.dump_objects("---> restore_saved_object")
                
        ##$$print("??? restore_saved_object, t %s" % t)
        #ro_n_rect = t.restore_object(coords, text, parent_id, v1, v2)
        # 4-lines.rdd works without (self,

        ## ##print("? ? ? t = %s (%s)" % (t, type(t)))
        ##r_obj = t.restore_object(coords, text, parent_id, int(v1), int(v2))
        ## print(">>> ro_header %s (%s)" % (r_obj, type(r_obj)))
        
    def copy_object(self, obj):
        #print("copy_object: %s < < <" % obj)
        offset = 25;  o_coords = []
        if obj.o_type == "text":
             coords = self.drawing.coords(obj.key)
             for c in coords:
                o_coords.append(c-offset)
             c_text = self.drawing.itemcget(obj.key, "text")
             self.dtc_tool.restore_object(o_coords, c_text, 0, obj.v1, obj.v2)
        elif obj.o_type == "line":
            coords = obj.a_obj.bbox()
            for c in coords:
                o_coords.append(c-offset)
            self.dlc_tool.restore_object(o_coords,
                "", 0, obj.v1, obj.v2) 
            
        elif obj.o_type == "n_rect":
            coords = obj.a_obj.bbox()
            for c in coords:
                o_coords.append(c-offset)
            self.drc_tool.restore_object(o_coords,
                obj.a_obj.text, 0, obj.v1, obj.v2) 

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
        #@print("@2@ edit_text_obj, self.text_edit %d" % self.text_edit)
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
        #print("@@@ rdg_closest, item_id %d, type %s" % (item_id, item_type))
        #print("@ln@ closest(1): item %s (%s), mx,my %d,%d" % (
        #        item, item_type, mx,my))
        if item_id in self.objects:
            obj = self.objects[item_id]  # item_id is a tkinter object id
            # object (e.g. rdo) has: key, obj, obj_ type, parent_id
            #print("-> closest %s is in objects, obj >%s<" % (item, obj))
            return item, obj
        else:  # Not in objects ??
            #print("\a@@@ item %d is not in rdg.objects <<<<" % item_id)
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
                print("b3_click: obj = %s" % obj)
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
        # self.text_edit is a tk.Text object (i.e. a Text window)
        #   It uses canvas.itemcget(self.text_id)
        # self.text_id   is a create_text object, in objects[self.text_id]
        new_text = self.text_edit.get('1.0','end-1c')
        #print("@@@ new_text >%s<" % new_text)
        #print("    self.text_id >%s<" % self.text_id)
        #@print("@3@ edit_esc_key, txt_obj %s" % txt_obj)
        
        if self.centre_texts:
            self.h2, self.w2 = self.str_h_w(new_text)
            new_text = self.justify(new_text, self.w2)
            # justify() adds leading spaces to centre all new_text's lines
        #print("new_text = >%s<" % new_text)  #@ correct
        self.text_edit.delete('1.0', 'end')
        self.text_edit.insert('1.0', new_text)

        self.drawing.itemconfigure(self.text_id, text=new_text,
            font=self.f_font)
        # Put edited text back into tk object and it's objects entry
        self.objects[self.text_id].i_text = new_text
        t_obj = self.objects[self.text_id]
        print("b3 esc_key: t_obj >%s<" % t_obj)  #@ correct (text)
        if t_obj.parent_id != 0:  # Text inside another object
            if t_obj.o_type == "field":  # Expand text to field width
                lr_len = round((t_obj.v2-len(new_text))/2)
                lr_fill = " "*lr_len
                nt = (lr_fill + new_text + lr_fill + " ")[0:t_obj.v2]
                self.objects[t_obj.parent_id].i_text = new_text
            elif self.objects[t_obj.parent_id].o_type == "n_rect":
                self.objects[t_obj.parent_id].a_obj.text = new_text
                print("parent [%s]" % self.objects[t_obj.parent_id])
                del self.objects[t_obj.key]
                ###t_obj.a_obj.text = integer, i.e, tk item id
                #print("n_rect edited: %s" % t_obj)
                #self.dump_objects("text edited %s" %
                #    self.objects[self.text_id])
        else:
            self.objects[self.text_id].i_text = new_text
            self.dump_objects("After edit text")
            #print("  = = = self.a_objects[self.text_id] >%s<" % self.a_objects[self.text_id])
        self.text_window.destroy()  # Close the editing window
        self.dump_objects(">> Edited text in field <<")

    def on_next_key(self, event):  # Pg Dn key pressed
        self.display_msg("", "normal")  # Clear message area

    def on_delete_key(self, event):  # Delete key pressed
        mx, my = (event.x, event.y)  # Mouse position
        #print("on_delete_key(): mx,my = %d,%d" % (mx,mx))
        item_ix, d_obj = self.rdg_closest(mx,my)
        if d_obj:
            #self.dump_objects("Handling Delete key")
            print("Deleting >%s< (%s) key %s" % (
                d_obj, d_obj.o_type, d_obj.key))
            self.deleted_objects.append(d_obj)
            #print("deleted_objects >%s<" % self.deleted_objects)
            if d_obj.o_type == "n_rect":
                self.drc_tool.undraw(d_obj)
            elif d_obj.o_type == "line":
                a_line = d_obj.a_obj
                a_line.undraw(d_obj)  # a_line already has 'self', avoids
                    # "takes 1 positional argument but 2 were given" error
            elif d_obj.o_type == "text":
                # text objects use Tk id for object and key!
                self.dtc_tool.undraw(d_obj)
            else:  # header/row/field
                hrf = d_obj.a_obj
                hrf.undraw(d_obj)
            ## Undraws the object##, and deletes it from objects dictionary
            ##del self.objects[d_obj.key]  # Delete object from dictionary
            ##self.objects[d_obj.key].deleted = True
            ##print("Deleted %s <<<" % self.objects[d_obj.key])
        else:
            print("\a    Not in objects ???")

    def on_insert_key(self, event):  # Insert key pressed
        print("len(self.deleted_objects) = %d" % len(self.deleted_objects))
        if len(self.deleted_objects) == 0:
            self.display_msg("No deleted objects", "warning")
        else:
            d_obj = self.deleted_objects.pop()
            print("inserting d_obj = >%s< (%s)" % (d_obj, d_obj.o_type))
            o_type = d_obj.o_type
            if d_obj.o_type == "text":
                self.dtc_tool.restore_object(d_obj.i_coords, d_obj.i_text,
                    d_obj.parent_id, d_obj.v1, d_obj.v2)
            #elif o_type == "field" or o_type == "row" or o_type == "field":
            #   d_obj.a_obj.restore_object(d_obj)
            #   #d_obj.a_obj.restore_object(d_obj.i_coords, d_obj.i_text,
            #   #     d_obj.parent_id, d_obj.v1, d_obj.v2, d_obj.a_obj) 
            else:
                #d_obj.a_obj.redraw_object(d_obj.i_coords, d_obj.i_text,
                #    d_obj.parent_id, d_obj.v1, d_obj.v2)
                d_obj.a_obj.redraw(d_obj)

    def dg_b3_click(self, event):
        self.drawing.after(250, self.mouse_action, event)
            # Delay to allow for double-click

    def dg_b3_double(self, event):
        self.double_click_flag = True

    def mouse_action(self, event):
        if self.double_click_flag:
            #print('double mouse click event')
            self.double_click_flag = False
            ##dgr.draw_groups.edr_to_group(self, event)  # rdg is self here!

        else:  # B3 (right button) to edit a Text
            #print('single mouse click event')
            #if self.last_mode == "group":
            #    print("\aCan't edit a Text in 'group' mode!")
           # else:
           self.on_b3_click(event)
