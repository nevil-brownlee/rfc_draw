# 1451, Fri  5 Jan 2024 (NZDT)
# 1655, Sun  5 Feb 2023 (NZDT)
#
# Draw a line with arrows on each segment
#
# Copyright 2024, Nevil Brownlee, Taupo NZ

import tkinter as tk
import math

import rfc_draw_globals_class as rdgc  # rfc-draw globals and functions
import draw_lines_class as dlc    # Handles line objects

class a_line:  # Draw line with arrows showing direction
    def __init__(self, drawing, coords, rdg):
        print("a_line called, coords %s" % coords)
        self.drawing = drawing  # Set up constants      
        self.rdg = rdg;  self.type = "a_line"
        self.parent_id = 0;  self.v1 = 0;  self.v2 = "0"
        self.arrowheads = True  # Default settings on startup
        self.syntax_end_mark = False

        self.al = 6  # Arrow length (= length of lines forming arrow)
        self.arad = math.radians(20)  # Arrow angle in radians
        self.a_offset = self.al*math.sin(self.arad)
        self.a_len = self.al*math.cos(self.arad)

        self.lbd = coords;  self.lbd_id = 0
        print("a_line: self.lbd = %s (%s)" % (self.lbd, type(self.lbd)))
        self.n_segs = int(len(self.lbd)/2)-1
        self.arrow_ids = [0]*self.n_segs
        self.se_bar_ids = [0]*4

    def mk_save_str(self, val):  # Make object's rdd file entry
        print("-- -- arrow_lines mk_save_str, val %s" % val)
        coords = []
        for c in val.i_coords:  #### Not val.obj.coords
            coords.append(int(float(c)))
        str = ""
        str += ("a" if self.arrowheads else "n")  # None
        str += ("e" if self.syntax_end_mark else "b")  # Bare
        return "(%s %d) %s \"%s\" %d %s %s" % ("line", self.lbd_id,
            self.lbd, str, val.parent_id, val.v1, val.v2)  # Correctd 8 Mar 2024
            #self.lbd, str, self.parent_id, self.v1, self.v2)

    def print_a_line_object(self):
        print("lbd %s, n_segs %d" % (self.lbd, self.n_segs))

    def arrows(self, v):
        self.undraw_arrowheads();  self.arrowheads = v;  self.draw_arrowheads()
        #print("in alc.arrows: self.arrows = %s (%s)" % (
        #    self.arrows, type(self.arrows)))

    def syntax_end(self, v):
        print("syntax_end: v %s, end_mark %s" % (v, self.syntax_end_mark))
        if v == "e":
            if not self.syntax_end_mark:
                self.draw_se_bars()
        elif v == "b":
            if self.syntax_end_mark:
                self.undraw_se_bars()
        
    def set_arrows(self, key):
        #print("alc: key %s" % key)
        if key == "a":
            self.arrows(True)
        elif key == "n":
            self.arrows(False)

    def bbox(self):
        return self.lbd

    def arrow_points(self, a_coords):
        sx,sy, ex,ey = a_coords
        #print("starting arrow_points: %d,%d, %d,%d" % (sx,sy, ex,ey))
        if ey == sy:
            if ex > sx:  # Right
                cx = int(sx+(ex-sx)/2 + self.a_len/2);  cy = sy
                return [int(cx-self.a_len),int(cy+self.a_offset), cx,cy, 
                        int(cx-self.a_len),int(cy-self.a_offset)]
            elif ex < sx:  # Left
                cx = int(ex+(sx-ex)/2 - self.a_len/2);  cy = sy
                return [int(cx+self.a_len),int(cy+self.a_offset), cx,cy, 
                        int(cx+self.a_len),int(cy-self.a_offset)]
        else:
            if ey > sy:  # Down
                cx = sx;  cy = int(sy+(ey-sy)/2 + self.a_len/2)
                return [int(sx-self.a_offset),int(cy-self.a_len), cx,cy,
                        int(sx+self.a_offset),int(cy-self.a_len)]
            else:  # up
                cx = sx;  cy = int(sy+(ey-sy)/2 - self.a_len/2)
                return [int(sx-self.a_offset),int(cy+self.a_len), cx,cy, 
                        int(sx+self.a_offset),int(cy+self.a_len)]
    
    def draw_line(self):
        n_segs = int(len(self.lbd)/2)-1
        if n_segs > self.n_segs:  # Segment(s) added
            self.arrow_ids = self.arrow_ids + [0]*(n_segs-self.n_segs)
        self.n_segs = n_segs
        #print("a_line.draw_line: lbd %s, lbd_id %d, n_segs %d, end_mark %s" % (
        #    self.lbd, self.lbd_id, self.n_segs, self.syntax_end_mark))
        if self.lbd_id == 0:
            self.lbd_id = self.rdg.add_to_layer(1,
                self.drawing.create_line, self.lbd)  #, fill="chartreuse")
            print("draw_line(): self.lbd_id %d" % self.lbd_id)
        else:
            self.rdg.drawing.itemconfigure(self.lbd_id, state=tk.NORMAL)
            self.drawing.coords(self.lbd_id, self.lbd)
        #print("   lbd_id %d, arrow_ids %s" % (
        #    self.lbd_id, self.arrow_ids))

        if self.arrowheads:
            self.draw_arrowheads()
        if self.syntax_end_mark:
            self.draw_se_bars()

        return self.lbd_id

    def draw_arrowheads(self):
        if self.arrowheads:
            for n in range(0, self.n_segs):  # Draw the arrowheads
                seg = self.lbd[n*2:n*2+4]
                a_coords = self.arrow_points(seg)
                if self.arrow_ids[n] == 0:
                    self.arrow_ids[n] = self.rdg.add_to_layer(1,
                        self.drawing.create_line, a_coords)
                else:
                    self.drawing.coords(self.arrow_ids[n], a_coords)
    
    def draw_se_bars(self):
        if not self.syntax_end_mark:
            sx,sy = self.lbd[0:2];  ex,ey = self.lbd[-2:]
            gap = 5
            self.draw_se_bar(0, sx, sy)  # Start E mark
            self.draw_se_bar(1, sx-gap, sy)
            self.draw_se_bar(2, ex, ey)  # End E mark
            self.draw_se_bar(3, ex+gap, ey)
        
    def draw_se_bar(self, n, x, y):
        bar_id = self.se_bar_ids[n]
        ht = 5;  sp = 5;  w = 2
        ty = y+ht;  by = y-ht
        if self.se_bar_ids[n] == 0:
            item_id = self.rdg.add_to_layer(1,
                self.drawing.create_line, [x,ty, x,by], width=w)
            self.se_bar_ids[n] = item_id
        else:
            coords = [x,ty, x,by]
            self.drawing.coords(self.se_bar_ids[n], coords)

    def undraw_se_bars(self):
        if self.syntax_end_mark:
            for n in range(0,4):
                self.rdg.drawing.itemconfigure(
                    self.se_bar_ids[n], state=tk.HIDDEN)
            self.syntax_end_mark = False
    
    def undraw_arrowheads(self):
        if self.arrowheads:
            for n in range(0,self.n_segs):
                self.rdg.drawing.itemconfigure(
                    self.arrow_ids[n], state=tk.HIDDEN)
                ##self.drawing.delete(self.arrow_ids[n])
            self.arrowheads = False
                
    def undraw_line(self):
        self.rdg.drawing.itemconfigure(self.lbd_id, state=tk.HIDDEN)
        ##self.drawing.delete(self.lbd_id)
        #print("*** undraw_line after delete lbd_id (%d)" % self.lbd_id)
        self.undraw_arrowheads()
        if self.syntax_end_mark:
            for n in range(0,4):
                ##self.drawing.delete(self.se_bar_ids[n])
                self.rdg.drawing.itemconfigure(
                    self.se_bar_ids[n], state=tk.HIDDEN)
                self.se_bar_ids[n] = 0
        #print("exiting after undraw_line");  x = input();  exit()
    
    def move(self, dx, dy):
        #print("alc move = = =")
        n_pairs = int(len(self.lbd)/2)
        for n in range(0, n_pairs):  # Move the line
            self.lbd[n*2] += dx
            self.lbd[n*2+1] += dy
        self.drawing.coords(self.lbd_id, self.lbd)

        for n in range(0, self.n_segs):  # Move the arrowheads
            seg = self.lbd[n*2:n*2+4]
            a_coords = self.arrow_points(seg)
            self.drawing.coords(self.arrow_ids[n], a_coords)

        #print("move, self.syntax_end_mark  = %s" % self.syntax_end_mark)
        if self.syntax_end_mark:  # Move the syntax_end bars
            for n in range(0, 4):
                #print("move bar %d = %d" % (n, self.se_bar_ids[n]))
                self.drawing.move(self.se_bar_ids[n], dx,dy)

        return self.lbd

    def extend_line(self, xn,yn):
        self.lbd = self.lbd[0:-2] + [xn,yn]

    def undraw(self, d_obj):  # For rdgc.on_delete_key()
        if self.lbd_id != 0:
            self.rdg.drawing.itemconfigure(self.lbd_id, state=tk.HIDDEN)
            self.undraw_line()
        for n in range(0, self.n_segs):
            self.rdg.drawing.itemconfigure(
                self.arrow_ids[n], state=tk.HIDDEN)

    def redraw(self, d_obj):  # For rdgc.on_insert_key()
        if self.lbd_id != 0:
            self.rdg.drawing.itemconfigure(self.lbd_id, state=tk.NORMAL)
        for n in range(0, self.n_segs):
            self.rdg.drawing.itemconfigure(
                self.arrow_ids[n], state=tk.NORMAL)

    def restore_object(self, l_coords, l_text, parent_id, v1, v2):
        #  line doesn't use parent_id, v1 or v2
        print("ALC.restore_object: l_coords %s, l_text >%s<, parent_id %s, v1 %s, v2 %s" % (
            l_coords, l_text, parent_id, v1, v2))
        print("parent_id %d, v1 %s, v2 %s, rdg %s" % (
            parent_id, v1, v2, self.rdg))

        rst_a_line = a_line(self.drawing, l_coords, self.rdg)
            #parent_id, v1, v2)  # a_line is this class's name !
        print("RO: restore_line: a_line >%s<" % rst_a_line)        
        for c in l_text:
            if c in "na":
                rst_a_line.set_arrows(c)
            elif c in "ub":
                rst_a_line.syntax_end(c)
            print("restore_line: option c = %s" % c)
        rst_a_line.lbd_id = self.draw_line()
        ##??a_line.lbd = l_coords
        print("===>>> arrow_lines:  rst_a_line.lbd_id %s, rst_a_line.lbd %s,rst_a_line %s" % (
            rst_a_line.lbd_id, rst_a_line.lbd, rst_a_line))
        print("   rst_a_line.lbd %s" % rst_a_line.lbd)

        line_obj = rdgc.rdglob.object(rst_a_line.lbd_id,
            rst_a_line, "line", l_coords, l_text, parent_id, v1, v2)
        print(">>> restored line, obj = %s" % line_obj)
        self.rdg.objects[rst_a_line.lbd_id] = line_obj
        self.rdg.current_object = line_obj
        return line_obj

