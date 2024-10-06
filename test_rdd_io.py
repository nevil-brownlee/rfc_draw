# 1631, Mon 27 MAy 2024 (NZST)
# 1708, Sat 28 Oct 2023 (NZDT)
#
# Test rdd_io.py
#
# Copyright 2024, Nevil Brownlee, Taupo NZ

import sys, re, math, svgwrite
import rdd_io

class svg_drawing:
    def __init__(self, sys_argv):
        rdd_fn = None
        print("Startup: sys_argv >%s<" % sys_argv)
        if len(sys_argv) == 1:  # sys_argv[0] = name of program 
            print("No .rdd file specified ???")
            from tkinter.filedialog import askopenfilename
            rdd_fn = (askopenfilename(title="Select .rdd source file"))
        # python3 test_rdd_io.py  save-h1r1.rdd     -> no border
        # python3 test_rdd_io.py  save-h1r1.rdd -b  -> 3 px border
        # python3 test_rdd_io.py  save-h1r1.rdd -b5 -> 5 px border

        self.border_width = 0
        if not rdd_fn:
            rdd_fn = sys_argv[1]
        if len(sys_argv) >= 3:  # We have a second argument
            arg2 = sys_argv[2]
            print("*** arg2 %s" % arg2)
            if len(arg2) >= 2:
                if arg2[0:2] == "-b":  # First two chars
                    self.border_width = 3
                    if len(arg2) > 2:
                        self.border_width = int(arg2[2:])
                    print("svg border width %d px" % self.border_width)
                else:
                    print("Unrecognised option %s" % arg2)
                    exit()
        print("$$$ rdd_fn %s, border_width %d" % (rdd_fn, self.border_width))


        #self.rdd_i = rdd_io.rdd_rw(rdd_fn, self.border_width)
        self.rdd_i = rdd_io.rdd_rw(rdd_fn, sys.argv[1:])
        self.di = self.rdd_i.read_from_rdd()  # {} Info about this Drawing
        # self.di contains:
        #   "r_width", "r_height",  # root window size
        #   "d_width", "d_height",  # drawing Canvas size
        #   "f_width", "f_height",  # font size (px)
        #   "min_x", "max_x", "min_y", "max_y"  # extrema of objects in drawing
        
        rdd_name = rdd_fn.split(".")
        #print("$ $ $ $ self.dwg created len(objects) = %d" % \
        #    len(self.rdd_i.objects))

        #self.text_attributes = ("font-family:monospace, font-size:%d, " +
           #"font-weight:bold; white-space:pre") % self.di["f_height"]
           # pre => display text as given (don't condense spaces!)
           #   NOT allowed for rfc7996 svg !
           # We use find_words instead,
           #   draw_text() writes each word in it's correct position
        # Other fonts tested:  droidsansmono, nimbusmono, Consolas
        self.al = 6  # Arrow length (= length of lines forming arrow)
        self.arad = math.radians(20)  # Arrow angle in radians
        self.a_offset = self.al*math.sin(self.arad)
        self.a_len = self.al*math.cos(self.arad)

        self.min_x = self.di["min_x"]-self.border_width
        self.min_y = self.di["min_y"]-self.border_width
        x_size = self.di["max_x"]-self.di["min_x"]+1 + 2*self.border_width
        y_size = self.di["max_y"]-self.di["min_y"]+1 + 2*self.border_width
        print("svg drawing size %d x %d, border_width %d" % (
            x_size, y_size, self.border_width))
        self.dwg = svgwrite.Drawing(filename=rdd_name[0]+".svg",
            profile='tiny', version='1.2',
            size=(x_size,y_size))

        self.draw_objects("text")
        self.draw_objects("line")
        self.draw_objects("n_rect")

        self.draw_frame(0,0, x_size-1,y_size-1)  # 1:1 scaling (sets viewbox)
        
    def arrow_points(self, a_coords):
        sx,sy, ex,ey = a_coords
        #print("starting arrow_points: %d,%d, %d,%d" % (sx,sy, ex,ey))
        if ey == sy:
            if ex > sx:  # Right
                cx = int(sx+(ex-sx)/2 + self.a_len/2);  cy = sy
                return [[int(cx-self.a_len),int(cy+self.a_offset)], [cx,cy], 
                        [int(cx-self.a_len),int(cy-self.a_offset)]]
            elif ex < sx:  # Left
                cx = int(ex+(sx-ex)/2 - self.a_len/2);  cy = sy
                return [[int(cx+self.a_len),int(cy+self.a_offset)], [cx,cy], 
                        [int(cx+self.a_len),int(cy-self.a_offset)]]
        else:
            if ey > sy:  # Down
                cx = sx;  cy = int(sy+(ey-sy)/2 + self.a_len/2)
                return [[int(sx-self.a_offset),int(cy-self.a_len)], [cx,cy],
                        [int(sx+self.a_offset),int(cy-self.a_len)]]
            else:  # up
                cx = sx;  cy = int(sy+(ey-sy)/2 - self.a_len/2)
                return [[int(sx-self.a_offset),int(cy+self.a_len)], [cx,cy], 
                        [int(sx+self.a_offset),int(cy+self.a_len)]]
    
    def draw_se_bar(self, x, y):
        ht = 7;  sp = 5;  w = 2
        ty = y+ht;  by = y-ht
        self.dwg.add(svgwrite.shapes.Line(
            start=(x,ty+3), end=(x,by+3),
            stroke="black", stroke_width=w, fill="none"))

    def draw_se_bars(self, coords):
        sx,sy = coords[0:2];  ex,ey = coords[-2:]
        gap = 5
        self.draw_se_bar(sx+2, sy)  # Start E mark
        self.draw_se_bar(sx+2-gap, sy)
        self.draw_se_bar(ex+2, ey)  # End E mark
        self.draw_se_bar(ex+2+gap, ey)
        
    def draw_line(self, coords, text):
        # text chars: one or more of a/n, e
        points = []
        for p in range(0, len(coords), 2):  # Centre inside borders
            x = self.border_width+coords[p]
            y = self.border_width+coords[p+1]
            points.append([x,y])
        #print("line points = %s" % points)
        
        self.dwg.add(svgwrite.shapes.Polyline(points,  # Draw the line
            stroke="black", stroke_width=1, fill="none"))

        if "a" in text:  # Draw line's arrowheads
            for n in range(0, len(points)-1):
                seg = points[n]+points[n+1]
                a_coords = self.arrow_points(seg)
                self.dwg.add(svgwrite.shapes.Polyline(a_coords,
                    stroke="black", stroke_width=1, fill="none"))
        if "e" in text:  # Draw Syntax End markers
            self.draw_se_bars(coords)
                
    def find_words(self, s):
        words = s.split()
        wx = []  # Start indeces of words
        in_word = False
        for j in range(0,len(s)):
            if not in_word:
                if s[j] != " ":
                    wx.append(j)
                    in_word = True;
            else:
                if s[j] == " ":
                    in_word = False
        return words, wx

    def draw_text(self, coords, text):
        # drawn with anchor=tk.CENTER, coords are text's centre point <<<
        lines = text.split("\n")
        if len(lines) == 1:
            half_nl = 0  # Only one line
        else:
            half_nl = len(lines)/2.0*self.di["f_height"]
        #print("@ half_nl = %s" % half_nl)
        cx = coords[0];   ly = coords[1]-half_nl  # Line y coord
        for text in lines:
            chars = len(text);  px = chars*self.di["f_width"]
            x = cx - int(px/2.0)
            words, wx = self.find_words(text)
            for j in range(len(wx)):
                self.dwg.add(svgwrite.text.Text(
                    words[j], insert=(x+wx[j]*self.di["f_width"],int(ly)),
                    font_family="monospace",font_weight="bold",
                    font_size=self.di["f_height"]))
            ly += self.di["f_height"]

    def draw_n_rect(self, coords, n_r_text):
        # coords = centre point for displayed text
        self.dwg.add(svgwrite.shapes.Rect(
            insert=(coords[0], coords[1]),  # upper left
            size=(coords[2]-coords[0], coords[3]-coords[1]),
            stroke="black", fill="white", stroke_width=1))
        cx = (coords[0]+coords[2])/2.0
        cy = (coords[1]+coords[3])/2.0
        #print("_rect coords %s, cx %d, cy %d" % (coords, cx,cy))
        #print("text >%s<, cx %d, cy %d" % (n_r_text, cx, cy))
        self.draw_text([cx, cy-2+self.di["f_height"] /2.0], n_r_text)
        
    def draw_frame(self, min_x,min_y, height,width):
        #print("draw_frame: %d,%d h %d, w %d" % (min_x,min_y, height,width))
        self.dwg.viewbox(min_x,min_y, height,width)
        self.dwg.save()

    def adj_coords(self, coords):
        a_coords = []
        for x in range(0,len(coords),2):
            a_coords.append(coords[x]-self.min_x)    
            a_coords.append(coords[x+1]-self.min_y)
        return a_coords

    def draw_objects(self, which):
        n_lines = n_n_rects = n_texts = 0
        for obj in self.rdd_i.objects:
            #print("++ obj >%s<" % obj)
            if obj.type == which:
                if obj.type == "line":
                    self.draw_line(self.adj_coords(self.obj.i_coords),
                        obj.i_text)
                    n_lines += 1
                elif obj.type == "n_rect":
                    #print(">> n_rect coords %s, text >%s<" % (
                    #    obj.i_coords, obj.i_text))
                    self.draw_n_rect(self.adj_coords(obj.i_coords),
                        obj.i_text)
                    n_n_rects += 1
                elif obj.type == "text":
                    #print("|%s|" % obj)
                    self.draw_text(self.adj_coords(obj.i_coords), obj.i_text)
                    n_texts += 1
        print("=== %d lines, %d n_rects and %d texts drawn" % (
            n_lines, n_n_rects, n_texts))
                

if __name__ == "__main__":
    svg_drawing(sys.argv)
