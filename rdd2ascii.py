# 1503, Mon 30 Oct 2023 (NZDT)
#
# rdd2ascii.py: Convert an rfc-draw .rdd file to an ASCII-ast image;
#
# Copyright 2023, Nevil Brownlee, Taupo NZ

import sys, os.path
import rdd_io

"""
In an rdd file, each group has a g_members list.
Each member also has (in the rdd file) a separate object for each of the
  group's members, so rfc-draw.py can find them when a user clicks on them.
That means rdd-to-svg can just ignore the group objects, their member
  objects will be used to make each member's svg images!
"""
class asc_drawing:
    def __init__(self, sys_argv):
        rdd_fn = None
        if len(sys_argv) == 1:  # sys_argv[0] = name of program 
            print("No .rdd file specified ???")
            from tkinter.filedialog import askopenfilename
            rdd_fn = (askopenfilename(title="Select .rdd source file"))

        # python3 rdd2ascii.py  group-line-test.rdd     -> no border
        # python3 rdd2ascii.py  group-line-test.rdd -b  -> 3 chars/lines border
        # python3 rdd2ascii.py  group-line-test.rdd -b5 -> 5 chars/lines border

        self.border_width = 1  # Default value
        #print("sys_argv >%s<" % sys_argv)
        if not rdd_fn:
            rdd_fn = sys_argv[1]
        if len(sys_argv) >= 3:  # We have a second argument
            arg2 = sys_argv[2]
            if len(arg2) >= 2:
                if arg2[0:2] == "-b":  # First two chars
                    if arg2 == "-b":
                        pass  #print("bw %d" % self.border_width)
                    else:
                        self.border_width = int(arg2[2:])
                    print("svg border width %d px" % self.border_width)
                else:
                    print("Unrecognised option %s" % arg2)
                    exit()

        print("+1+ border_width %d" % self.border_width)
        self.rdd_i = rdd_io.rdd_rw(rdd_fn)
        self.di = self.rdd_i.read_from_rdd()  # {} Info about this Drawing
        # self.di contains:
        #   "r_width", "r_height",  # root window size
        #   "d_width", "d_height",  # drawing Canvas size
        #   "f_width", "f_height",  # font size (px)
        #   "min_x", "max_x", "min_y", "max_y"  # extrema of objects in drawing

        self.f_width = self.di["f_width"];  self.f_height = self.di["f_height"]
        self.min_x = self.di["min_x"];  self.max_x = self.di["max_x"]
        self.min_y = self.di["min_y"];  self.max_y = self.di["max_y"]
        print("min_x %d, max_x %d, min_y %d, max_y %d, border_width %d" %
            (self.min_x, self.max_x, self.min_y, self.max_y ,self.border_width))

        c_min,r_min = self.map(self.min_x,self.min_y)
        c_max,r_max = self.map(self.max_x,self.max_y)
        self.n_chars = c_max-c_min+1 + 2*self.border_width
        self.n_lines = r_max-r_min+1 + 2*self.border_width
        print("c_min %d, c_max %d, n_chars %d, r_min %d, r_max %d, n_lines %d," %
              (c_min, c_max, self.n_chars, r_min, r_max, self.n_lines))
        
        self.lines = [[" " for col in range(self.n_chars)]
                               for row in range(self.n_lines)]
        self.n_n_rect = self.n_line = 0
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.digits = "0123456789ABC"
        self.slc = False  # Set line corner points to show which line it is

        rdd_name = rdd_io.rdd_rw(rdd_fn)
        text_fn = rdd_fn.split(".")[0]+".txt"

        min_x = min_y = 50000;  max_x = max_y = 0
        for obj in self.rdd_i.objects:
            coords = obj.i_coords
            for n in range(0, len(coords), 2):
                x = coords[n];  y = coords[n+1]  # Text centre (tk Canvas units)
                if obj.type == "text":   ##or obj.type == "n_rect":
                    tw2 = round(obj.txt_width*f_width/2)  # tk units
                    #print("$$$ x %d, tw2 %d; -= %d, += %d" % (x,tw2, x-tw2, x+tw2))
                    if x+tw2 > max_x:
                        x += tw2;  max_x = x+tw2
                        #print(">>> text x incr by %d px" % tw2)
                    if x-tw2 < min_x:
                        min_x = x-tw2
                        x -= tw2
                        #print(">>> text x decr by %d px" % tw2)
                        #print("text %d, cx %d,  min_x %d, max_x %d" % (
                        #    obj.id, coords[0], min_x, max_x))
                else:
                    #print("..%2d  x %d, y %d" % (n, x,y))
                    if x < min_x:
                        min_x = x
                    elif x > max_x:
                        max_x = x
                if y < min_y:
                    min_y = y
                elif y > max_y:
                    max_y = y

        print("x %d to %d, y %d to %d" % (min_x,max_x, min_y,max_y))

        self.draw_objects("line")   # layer 1
        self.draw_objects("n_rect") # layer 2
        self.draw_objects("text")   # layer 3

        self.print_lbuf(text_fn)

    def map(self, x, y):  # Map x,y (from rdd) to col,row (in lines 2D array)
        x_sf = 1.0;  y_sf = 1.0
        col = round((x-self.min_x)*x_sf/self.f_width) + self.border_width  # LH
        row = round((y-self.min_y)*y_sf/self.f_height) + self.border_width  # Top
        #print("@map: col %s %s, row %s %s" % (col,type(col), row,type(row)))
        return col, row
        
    def print_lbuf(self, txt_fn):
        print("#### txt_fn >%s<" % txt_fn)
        #afn = self.asc_filename.split("/")[-1]
        # Bug reported: becarpenter, 22 Oct 2023 (NZDT)
        # Will write .txt file to current directory
        asc_file = open(txt_fn, "w")
        for j in range(self.n_lines):
            asc_file.write("%s\n" % ''.join(self.lines[j]))
        asc_file.close()

    def set_char(self, ch, xc,yr):  # Must not overwrite "+"
        ln = self.lines[yr]
        if ln[xc] != "+":
            ln[xc] = ch            
    
    def draw_line(self, coords, text):
        # text chars: one or more of a/n, e
        #print("LLL coords %s" % coords)
        rc_coords = []
        for p in range(0, len(coords), 2):  # Convert to col,row coords
            col,row = self.map(coords[p], coords[p+1])
            rc_coords.append(col)
            rc_coords.append(row)
        #print("rc_coords = %s" % rc_coords)

        self.n_line += 1
        for p in range(0,len(rc_coords)-2,2):  # Draw the line
            #print("p %s" % p)
            #print(">>>>>>>>>>>>>> n_line %d" % self.n_line)
            ch = self.digits[self.n_line]
            x0 = rc_coords[p];  y0 = rc_coords[p+1]  # segment x0,y0 to x1,y1
            x1 = rc_coords[p+2];  y1 = rc_coords[p+3]
            print("x0,y0 = %d,%d, x1,y1 = %d,%d" % (x0,y0, x1,y1))
            #print(">>> p %s, x %s, y %s :: %d lines" % (p,x,y,len(self.lines)))
            if x0 == x1:     # vertical
                if abs(y1-y0)+1 < 3:
                    print("line segment %d [%d,%d, %d,%d] too small to draw" % (
                        (p, x0,y0, x1,y1)))
                    ln = self.lines[y0];  ln[x0] = "?"
                else:
                    cy = round((y0+y1)/2)
                    if y0 < y1:  # down
                        #print("  line down, %d,%d -> %d,%d" % (x0,y0, x1,y1))
                        self.set_char("+", x0,y0)
                        for y in range(y0+1,y1):
                            self.set_char("|", x0,y)
                        self.set_char("+", x0,y1)
                        self.set_char("v", x0,cy)
                    elif y0 > y1:  # up
                        #print("  line up, %d,%d -> %d,%d" % (x0,y0, x1,y1))
                        if self.slc:
                            self.set_char(self.digits[self.n_line], x0,y0)
                        else:
                            self.set_char("+", x0,y0)
                        for y in range(y1,y0):
                            self.set_char("|", x0,y)
                        if self.slc:
                            self.set_char(self.digits[self.n_line], x0,y1)
                        else:
                            self.set_char("+", x0,y1)
                        self.set_char("^", x0,cy)
            elif y0 == y1:   # horizontal
                cx = round((x0+x1)/2); ln = self.lines[y0]
                if x0 < x1:    # right
                    for x in range(x0+1,x1):
                        self.set_char("-", x, y0)
                    self.set_char(">", cx,y0)
                elif x0 > x1:  # left
                    for x in range(x1+1,x0):
                        self.set_char("-", x,y0)
                    self.set_char("<", cx,y0)
        if "e" in text:  # Draw Syntax End markers
            sx,sy = rc_coords[0:2]
            self.set_char(">", sx,sy)  # >> beginning of syntax diagram
            self.set_char(">", sx+1,sy)
            ex,ey = rc_coords[-2:]
            self.set_char(">", ex-1,ey)  # >< end of syntax diagram
            self.set_char("<", ex,ey)

    def draw_text(self, m_key, coords,text):
            # drawn with anchor=tk.CENTER, coords are text's centre point <<<
        #print("@text %d, coords %s" % (m_key, coords))
        txcol, txrow = self.map(coords[0], coords[1])  # text row,col
        #print("text: >%s<, txcol %d, trow %d" % (text, txcol,txrow))
        t_lines = text.split("\n")
        #print("t_lines = >%s<" % t_lines)
        # Find centre of text block
        mx_tlen = 0
        for j in range(len(t_lines)):
            if len(t_lines[j]) > mx_tlen:
                mx_tlen = len(t_lines[j])
        #print("mx_tlen = %d" % mx_tlen)
        tll = txcol-round(mx_tlen/2.0)    # col (leftmost char)
                                          # col txcol = text centre 
        tlend = txcol+round(mx_tlen/2.0)  # col (rightmost char)
        tlr = txrow-round(len(t_lines)/2.0)  # row
        #print("tll-tlend %d - %d, tlr %d" % (tll,tlend, tlr))
        
        for r,text in enumerate(t_lines):  # Centre the text lines
            ln = self.lines[tlr+r]
            tlc = round(txcol-len(text)/2)  # text, leftmost col
            for j in range(len(text)):
                ln[tlc+j] = text[j]

    def draw_text_row(self, text, c, r):
        ln = self.lines[r]
        for j in range(len(text)):
            ln[c+j] = text[j]

    def draw_n_rect(self, id, coords, n_r_text):
        # coords = centre point for displayed text
        tlc, tlr = self.map(coords[0], coords[1])  # Top left col,row
        brc, brr = self.map(coords[2], coords[3])  # Bottom right col, row
        if brc-tlc+1 < 3 or brr-tlr+1 < 3:
            print("rectangle at %d,%d, %d,%d too small to draw" % (
                tlc,tlr, brc,brr))
            print("  Min rectangle size is 3x3 chars <<<")
        #print("n_rect r,c coords: %d,%d to %d,%d" % (tlc,tlr, brc,brr))

        self.n_n_rect += 1
        ch = self.alphabet[self.n_n_rect]
        h_row = "+" + "-"*(brc-tlc-2) + "+"
        #h_row = "+" + ch*(brc-tlc-2) + "+"
        print("h_row %s" % h_row)
        v_row = "|" + " "*(brc-tlc-2) + "|"
        #v_row = ch + " "*(brc-tlc-2) + ch
        print("v_row %s" % v_row)

        self.draw_text_row(h_row, tlc,tlr)
        for j in range(tlr+1, brr):
            self.draw_text_row(v_row, tlc, j)
        self.draw_text_row(h_row, tlc,brr)

        cx = round((coords[0]+coords[2])/2.0)
        cy = round((coords[1]+coords[3])/2.0)
        #print("cx,cy %d,%d, text >%s<" % (cx,cy, n_r_text))
        self.draw_text(id, [cx,cy], n_r_text)
    
    def draw_objects(self, which):
        d_lines = d_rects = d_texts = 0
        for obj in self.rdd_i.objects:
            if obj.type == which:
                if obj.type == "line":
                    self.draw_line(obj.i_coords, obj.i_text)
                    d_lines += 1
                elif obj.type == "n_rect":
                    #print(">> n_rect id %d, coords %s, text >%s<" % (
                    #    obj.id, obj.i_coords, obj.i_text))
                    self.draw_n_rect(obj.id, obj.i_coords, obj.i_text)
                    d_rects += 1
                if obj.type == "text":
                    #print("|%s|" % obj)
                    self.draw_text(obj.id, obj.i_coords, obj.i_text)
                    d_texts += 1
        print("=== %d lines, %d d_rects and %d texts drawn" % (
            d_lines, d_rects, d_texts))


if __name__ == "__main__":
    asc_drawing(sys.argv)
