# 1601, Fri  8 Sep 2023 (NZST)
# 1504, Tue 26 Sep 2023 (NZDT)
# 1553, Sat 21 Oct 2023 (NZDT)
#
# rdd-to-ascii.py: Convert an rfc-draw .rdd file to an ASCII ART image;
#
# Copyright 2023, Nevil Brownlee, Taupo NZ

import sys, os.path
import rdd_io

"""
In an rdd file, each group has a g_members list.
Each member also has (n the rdd file) a separate object for each of the
  group's members, so rfc-draw.py can find them when the user clicks on them.
That means rdd-to-ascii can just ignore the group objects, their member
  objects will be used to make each member's ascii images!

python3 rdd-to-ascii.py  group-line-test.rdd     -> no border around image
python3 rdd-to-ascii.py  group-line-test.rdd -b  -> 1 col/row border
python3 rdd-to-ascii.py  group-line-test.rdd -b3 -> 3 col/row border
"""

class asc_drawing:
    def __init__(self, asc_filename, border,
            x_min, x_max, y_min, y_max, font_width, font_height):
        print("asc_filename %s,border %s,font_width %s, font_height %s" % (
            asc_filename, border, font_width, font_height))
        self.asc_filename = asc_filename
        print("x %s - %s, y %s - %s" % (x_min, x_max, y_min, y_max))
        self.border = border
        self.x_min = x_min;  self.y_min = y_min
        self.f_height = font_height
        self.f_width = font_width
        c_min,r_min = self.map(x_min,y_min)
        #print(" >> c_min %s, r_min %s" % (c_min,r_min))
        c_max,r_max = self.map(x_max,y_max)
        #print(" >> c_max %s, r_max %s" % (c_max,r_max))

        self.n_chars = c_max-c_min+1 + 2*self.border
        self.n_lines = r_max-r_min + 1 + 2*self.border
        self.lines = [[" " for col in range(self.n_chars)]
                               for row in range(self.n_lines)]
        self.n_n_rect = self.n_line = 0
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.digits = "0123456789ABC"
        self.slc = False  # Set line corner digits show which line it is

    def map(self, x, y):  # Map x,y (from rdd) to col,row (in lines 2D array)
        x_sf = 1.0;  y_sf = 1.5
        col = round((x-self.x_min)*x_sf/self.f_width) + self.border  # LH
        row = round((y-self.y_min)*y_sf/self.f_height) + self.border  # Top
        #print("@map: col %s %s, row %s %s" % (col,type(col), row,type(row)))
        return col, row
        
    def print_lbuf(self, txt_fn):
        print("#### txt_fn >%s<" % txt_fn)
        #afn = self.asc_filename.split("/")[-1]
        # Bug reported: becarpenter, 22 Oct 2023 (NZDT)
        # Will write .txt file to current directory
        asc_file = open(txt_fn, "w")
        for j in range(self.n_lines):
            asc_file.write("%s \n" % ''.join(self.lines[j]))
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
        self.draw_text(obj.id, [cx,cy], n_r_text)
    
    def draw_objects(self, which):
        d_lines = d_rects = d_texts = 0
        for obj in rdd_i.objects:
            if obj.type == which:
                if obj.type == "line":
                    self.draw_line(obj.i_coords, obj.i_text)
                    d_lines += 1
                elif obj.type == "n_rect":
                    #print(">> n_rect id %d, coords %s, text >%s<" % (
                    #    obj.id, obj.i_coords, obj.i_text))
                    asc_d.draw_n_rect(obj.id, obj.i_coords, obj.i_text)
                    d_rects += 1
                if obj.type == "text":
                    #print("|%s|" % obj)
                    self.draw_text(obj.id, obj.i_coords, obj.i_text)
                    d_texts += 1
        print("=== %d lines, %d d_rects and %d texts drawn" % (
            d_lines, d_rects, d_texts))


if __name__ == "__main__":
    #print("argv >%s<, len(sys.argv) = %d" % (sys.argv, len(sys.argv)))
    rdd_fn = None
    if len(sys.argv) == 1:  # sys.argv[0] = name of program 
        print("No .rdd file specified ???")
        from tkinter.filedialog import askopenfilename
        rdd_fn = (askopenfilename(title="Select .rdd source file"))
    if not rdd_fn:
        rdd_fn = sys.argv[1]
    path, fn = os.path.split(rdd_fn)
    print("file path %s, rdd_fn %s" % (path, fn))

    print("$$$ path >%s<, fn >%s<" % ( path, fn))
    if not fn.endswith(".rdd"):
        print("\ardd filename >%s< didn't end with '.rdd", rdd_fn)
        exit()

    border_width = 1  # Default value (col/row)
    if len(sys.argv) >= 3:  # We have a second argument
        arg2 = sys.argv[2]
        #print("<><> fn %s, arg2 %s" % (fn, arg2))
        if len(arg2) >= 2:
            if arg2[0:2] == "-b":  # First two chars
                if len(arg2) != 2:
                    border_width = int(arg2[2:])
            print("ascii border width %d cols/rows" % border_width)
        else:
            print("Unrecognised option %s" % arg2)
            exit()

    rdd_i = rdd_io.rdd_rw(rdd_fn)
    xr, yr, f_width, f_height, d_width, d_height = rdd_i.read_from_rdd()
    # xr,ry are rfc-draw's 'root' geometry (in px) !!!
    #rdd_i.dump_objects("after read_from_rdd")
    fs = "Screen: xr %d, yr %d | Drawing: width %d, height %d"
    fs += " | Font: width %.2f, height %.2f px"
    print(fs % (xr, yr, d_width, d_height, f_width, f_height))
    print("===================================================")

    txt_fn = path + "/" + fn.replace("rdd","txt")    
    min_x = min_y = 50000;  max_x = max_y = 0
    for obj in rdd_i.objects:
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

    asc_d = asc_drawing(path+".txt", border_width,
        min_x,max_x, min_y,max_y, rdd_i.f_width, rdd_i.f_height)

    asc_d.draw_objects("line")   # layer 1
    asc_d.draw_objects("n_rect") # layer 2
    asc_d.draw_objects("text")   # layer 3

    asc_d.print_lbuf(txt_fn)

    ##svg_d.draw_frame(min_x,min_y, max_x-min_x, max_y)  # 1:1 scaling
    #svg_d.draw_frame(0,0, rdd_i.xr,rdd_i.yr)  # 1:1 scaling
    #self.svg_d.draw_frame(min_x-6,min_y-6,
    #    (max_x-min_x)*2+6, (max_y-min_y)*2+18)
    #       #  drawing in top left quarter of image
