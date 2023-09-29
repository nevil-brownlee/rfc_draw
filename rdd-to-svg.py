# 1549, Fri  8 Sep 2023 (NZST)
# 1529, Tue 30 May 2023 (NZST)
#
# rdd-to-svg.py: Convert an rfc-draw .rdd file to an svg image;
#   that svg image >>> conforms to RFC 7996 requirements <<<
#
# Copyright 2023, Nevil Brownlee, Taupo NZ

import sys, re, math, svgwrite
import rdd_io

"""
In an rdd file, each group has a g_members list.
Each member also has (in the rdd file) a separate object for each of the
  group's members, so rfc-draw.py can find them when a user clicks on them.
That means rdd-to-svg can just ignore the group objects, their member
  objects will be used to make each member's svg images!
"""

class svg_drawing:
    def __init__(self, svg_filename, x_size, y_size, font_width, font_height):
        self.border = 3;  self.top = 0
        print("svg_drawing: font_width %s, font_height %s" % (
            font_width, font_height))
        self.x_size = x_size;  self.y_size = y_size
        self.f_height = font_height
        self.f_width = font_width
        self.f_size = "%dpx" % font_height
        #self.text_attributes = ("font-family:monospace, font-size:%d, " +
           #"font-weight:bold; white-space:pre") % self.f_height
           # pre => display text as given (don't condense spaces!)
           #   NOT allowed for rfc7996 svg !
           # We use find_words instead,
           #   draw_text() writes each word in it's correct position
        # Other fonts tested:  droidsansmono, nimbusmono        
        self.dwg = svgwrite.Drawing(filename=svg_filename,
            profile='tiny', version='1.2',
            size=(2*self.border+x_size, y_size+2*self.border))
        self.al = 6  # Arrow length (= length of lines forming arrow)
        self.arad = math.radians(20)  # Arrow angle in radians
        self.a_offset = self.al*math.sin(self.arad)
        self.a_len = self.al*math.cos(self.arad)
        
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
            x = self.border+coords[p]
            y = self.border+coords[p+1]
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
        #print("@@@@@ f_height = %d, coords = %s" % (self.f_height, coords))
        lines = text.split("\n")
        if len(lines) == 1:
            half_nl = 0  # Only one line
        else:
            half_nl = len(lines)/2.0*self.f_height
        #print("@ half_nl = %s" % half_nl)
        cx = coords[0];   ly = coords[1]-half_nl  # Line y coord
        for text in lines:
            chars = len(text);  px = chars*self.f_width
            x = cx - int(px/2.0)
            words, wx = self.find_words(text)
            for j in range(len(wx)):
                self.dwg.add(svgwrite.text.Text(
                    words[j], insert=(x+wx[j]*self.f_width,int(ly)),
                    font_family="monospace",font_weight="bold",
                    font_size=self.f_size))
            ly += self.f_height

    def draw_n_rect(self, coords, n_r_text):
        # coords = centre point for displayed text
        self.dwg.add(self.dwg.rect(
            insert=(coords[0], coords[1]),  # upper left
            size=(coords[2]-coords[0], coords[3]-coords[1]),
            stroke="black", fill="white", stroke_width=1))
        cx = (coords[0]+coords[2])/2.0
        cy = (coords[1]+coords[3])/2.0
        #print("_rect coords %s, cx %d, cy %d" % (coords, cx,cy))
        #print("text >%s<, cx %d, cy %d" % (n_r_text, cx, cy))
        self.draw_text([cx, cy-2+self.f_height/2.0], n_r_text)
        
    def draw_frame(self, min_x,min_y, height,width):
        #print("draw_frame: %d,%d h %d, w %d" % (min_x,min_y, height,width))
        self.dwg.viewbox(min_x,min_y, height,width)
        self.dwg.save()

    def draw_objects(self, which):
        n_lines = n_n_rects = n_texts = 0
        for obj in rdd_i.objects:
            if obj.type == which:
                if obj.type == "line":
                    svg_d.draw_line(obj.i_coords, obj.i_text)
                    n_lines += 1
                elif obj.type == "n_rect":
                    #print(">> n_rect coords %s, text >%s<" % (
                    #    obj.i_coords, obj.i_text))
                    svg_d.draw_n_rect(obj.i_coords, obj.i_text)
                    n_n_rects += 1
                elif obj.type == "text":
                    #print("|%s|" % obj)
                    self.draw_text(obj.i_coords, obj.i_text)
                    n_texts += 1
        print("=== %d lines, %d n_rects and %d texts drawn" % (
            n_lines, n_n_rects, n_texts))
                


if __name__ == "__main__":
    #print("argv >%s<, len(sys.argv) = %d" % (sys.argv, len(sys.argv)))
    if len(sys.argv) == 1:  # sys.argv[0] = name of program 
        print("No .rdd file specified ???")
        exit()

    # python3 rdd-to-svg.py  group-line-test.rdd     -> no border around image
    # python3 rdd-to-svg.py  group-line-test.rdd -b  -> 3 px border
    # python3 rdd-to-svg.py  group-line-test.rdd -b5 -> 5 px border
    
    border_width = 3  # Default value
    #print("sys.argv >%s<" % sys.argv)
    rdd_fn = sys.argv[1]
    if len(sys.argv) >= 3:  # We have a second argument
        arg2 = sys.argv[2]
        if len(arg2) >= 2:
            if arg2[0:2] == "-b":  # First two chars
                if arg2 == "-b":
                    pass  #print("bw %d" % border_width)
                else:
                    border_width = int(arg2[2:])
                print("svg border width %d px" % border_width)
            else:
                print("Unrecognised option %s" % arg2)
                exit()
    #print("$$$ rdd_fn %s" % rdd_fn)
    rdd_i = rdd_io.rdd_rw(rdd_fn)
    xr, yr, f_width, f_height, d_width, d_height = rdd_i.read_from_rdd()
    #rdd_i.dump_objects("after read_from_rdd")
    fs = "Screen: xr %d, yr %d | Drawing: width %d, height %d"
    fs += " | Font: width %.2f, height %.2f"
    print(fs % (xr, yr, d_width, d_height, f_width, f_height))

    min_x = min_y = 30000;  max_x = max_y = 0
    for obj in rdd_i.objects:
        coords = obj.i_coords
        for n in range(0, len(coords), 2):
            x = coords[n];  y = coords[n+1]
            if x < min_x:
                min_x = x
            elif x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            elif y > max_y:
                max_y = y
    print("x %d to %d, y %d to %d" % (min_x,max_x, min_y,max_y))

    rdd_name = rdd_fn.split(".")[0]
    svg_d = svg_drawing(rdd_name+".svg",
        rdd_i.xr, rdd_i.yr, rdd_i.f_width, rdd_i.f_height)

    svg_d.draw_objects("text")
    svg_d.draw_objects("line")
    svg_d.draw_objects("n_rect")

    svg_d.draw_frame(0,0, rdd_i.xr,rdd_i.yr)  # 1:1 scaling
