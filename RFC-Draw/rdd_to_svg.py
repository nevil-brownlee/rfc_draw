# 1549, Tue  7 Nov 2023 (NZDT)
#
# rdd-to-svg.py: Convert an rfc-draw .rdd file to an svg image;
#   that svg image >>> conforms to RFC 7996 requirements <<<
#
# Copyright 2024, Nevil Brownlee, Taupo NZ

import sys, re, os, math, svgwrite
import rdd_io, rdd_globals, rfc_draw_globals_class as rgdc

class svg_drawing:
    def __init__(self, sys_argv):
        print("===> rdd_to_svg.py: sys_argv %s" % sys_argv)
        rg = rdd_globals.gv
        self.bw = rg.svg_def_b_w  # Default border width
        if len(sys_argv) == 1:  # sys_argv[0] = name of program 
            print("No .rdd file specified ???")
            from tkinter.filedialog import askopenfilename
            self.rdd_fn = (askopenfilename(title="Select .rdd source file"))
        elif len(sys_argv) >= 2:
            self.rdd_fn = sys_argv[1]
        elif len(sys_argv) >= 3:
            self.bw = int(sys_argv[2])
        print("self.rdd_fn %s,  border_width %s" % (self.rdd_fn, self.bw))
        self.rdd_i = rdd_io.rdd_rw(sys_argv, self.bw) 
        print("rddi >%s< (%s)" % (self.rdd_i, type(self.rdd_i)))
        self.rdd_fn = self.rdd_i.rdd_fn
        #;  self.border_width = self.rddi.border_width
        self.objects, self.di = self.rdd_i.read_from_rdd()
        #self.rdd_i.dump_objects("read in by rdd_io")
        self.debug = False   # svg colour always black
                             # True uses hd_colours to show row is which!
        
        # self.di contains:
        #   "f_width", "f_height",  # font size (px)
        #   "min_x", "max_x", "min_y", "max_y"  # extrema of objects in drawing
        
        rdd_name = self.rdd_fn.split(".")
        #print("$ $ $ $ self.dwg created len(objects) = %d" % len(self.objects))

        #self.text_attributes = ("font-family:monospace, font-weight:normal " +
        #   #"font-weight:normal; white-space:pre") % self.di["f_height"])
        #                        "font-size:%d, " % self.di["f_height"])
        #print("text_attributes >%s<" % self.text_attributes)
           # pre => display text as given (don't condense spaces!)
           #   NOT allowed for rfc7996 svg !
           # We use find_words instead,
           #   draw_text() writes each word in it's correct position
        # Other fonts tested:  droidsansmono, nimbusmono, Consolas
        
        self.al = 6  # Arrow length (= length of lines forming arrow)
        self.arad = math.radians(20)  # Arrow angle in radians
        self.a_offset = self.al*math.sin(self.arad)
        self.a_len = self.al*math.cos(self.arad)

        self.min_x = self.di["min_x"]  #-self.border_width
        self.min_y = self.di["min_y"]  #-self.border_width
        self.max_x = self.di["max_x"]  #-self.border_width
        self.max_y = self.di["max_y"]  #-self.border_width
        x_size = self.max_x-self.min_x + 2*self.bw
        y_size = self.max_y-self.min_y + 2*self.bw
        print("svg drawing size %d x %d, border_width %d" % (
            x_size, y_size, self.bw))
        self.filename = rdd_name[0]+".svg"
        print("@@@ svg size = (%d, %d)" % (x_size,y_size))
        self.f_height = self.di["f_height"] - 3  # 17 is too big
        self.dr_calls = 0
        self.f_width = self.di["f_width"]
        self.tic_width = 2

        self.hd_colours = ["black", "brown", "red", "darkorange", # 0,1,2,3
            "gold", "green", "darkblue", "darkviolet", "dimgray", "darkorange"]
        #      4       5        6            7           8            9

        self.dwg = svgwrite.drawing.Drawing(filename=self.filename,
            font_family="monospace",font_size=int(self.f_height),
            font_weight="normal",
            ##width=x_size, height=y_size,
            profile='basic', version='1.2',  # tiny -> basic,  1 Jan 2025
            size=(x_size,y_size))

        self.dr_calls = 0
        self.draw_objects("line")    # layer 1
        self.draw_objects("n_rect")  # layer 2
        self.draw_objects("text")    # layer 3
        self.draw_objects("header")  # Components of rfc-draw Headers
        self.draw_objects("row")     #   all layer 3
        self.draw_objects("field")

        self.draw_frame(0,0, x_size,y_size)  # 1:1 scaling
        self.dwg.save()
        self.strip_qxml(self.filename)

    def r_colour(self, r_nbr):
        if self.debug:
            return self.hd_colours[abs(r_nbr)%len(self.hd_colours)]
        else:
            return "black"
        
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
        
    def draw_line(self, coords, text, r_nbr):
        print("draw_line, r_nbr %d, text >%s<" % (r_nbr, text))
        # text chars: one or more of a/n, e
        points = []
        for p in range(0, len(coords), 2):  # Centre inside borders
            x,y = coords[p],coords[p+1]
            points.append([x,y])
        print("line points = %s" % points)

        self.dwg.add(svgwrite.shapes.Polyline(points,  # Draw the line
            ##stroke="green", stroke_width=1, fill="none"))
            stroke=self.r_colour(abs(r_nbr)), stroke_width=1, fill="none"))

        if "a" in text:  # Draw line's arrowheads
            for n in range(0, len(points)-1):
                seg = points[n]+points[n+1]
                a_coords = self.arrow_points(seg)
                print("a_coords %s" % a_coords)
                self.dwg.add(svgwrite.shapes.Polyline(a_coords,
                stroke=self.r_colour(abs(r_nbr)), stroke_width=1, fill="none"))

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

    def draw_text(self, coords, r_nbr, text):
        # svg uses (x,y) to specify text em's bottom-left corner
        mx_w = 0  # Max line length in text
        lines = text.split("\n")
        for line in lines:
            if len(line) > mx_w:
                mx_w = len(line)
        half_nl = int(len(lines)*self.f_height/2.0)
        print("@ half_nl = %s, r_nbr %d" % (half_nl, r_nbr))
        if len(coords) == 4:  #  field object
            x0,y0, x1,y1 = coords # map(field's parent row coords)
            print("text coords x0,y0 %d,%d, x1,y1 %d,%d" % (x0,y0, x1,y1))
            cx = round((x0+x1)/2.0)
            cy = round((y0+y1)/2.0)
            ###ly = cy + round(self.f_height/4.0)   # First line's y coord
            if r_nbr == 1:  # col_nbrs row
                ly = cy
            else:
                ly = cy + round(self.f_height/4.0)   # First line's y coord
                
        else:  # Plain text (rather than text in draw_field)
            x0,y0 = coords  # text centre x,y
            print("~~~>>> plain text x0,y0 %s,%s" % (x0,y0))
            ##cx = x0+round(mx_w*self.f_width/2.0)
            cx = x0
            #ly = y0+self.f_height - round(self.f_height*0.75)
            ly = y0 + round(self.f_height/4.0)
            print("text coords x0,y0 %d,%d" % (x0,y0))
                
        print("f_width = %d, coords = %s" % (self.f_width, coords))
        lines = text.split("\n")
        if len(lines) == 1:
            half_nl = 0  # Only one line
            #ly += round(self.f_height*1.2)
        else:
            half_nl = int(self.f_height*len(lines)/2.0)
            ly = ly - half_nl + round(self.f_height)
            ##ly = ly - half_nl + round(self.f_height*1.5)
            if len(lines) == 1:
                ly += round(self.f_height/2.0)
            # multi-line in n-rects OK
            # without above  line, only singe-line text in n-rects is OK
        print("@ half_nl = %s" % half_nl)
        print("f_width = %d, coords = %s" % (self.f_width, coords))
        for text in lines:
            chars = len(text);  px = mx_w*self.f_width
            x = cx-round(px/2.0)  # x = left edge of text
            #x = x0  # x = left edge of text

            print("chars %d, x,y %d,%d" % (chars, x,ly))
            words, wx = self.find_words(text)
            print("words %s" % words)
            print("   wx %s" % wx)
            wxp = [] 
            for i in range(0,len(wx)):
                wxp.append(int(wx[i]*self.f_width))

            print("=-=-= words %s" % words)
            print("-=-=-   wxp %s" % wxp)
            # write line's text to svg
            if text.count(' ') > 4:
                for j in range(len(wx)):  # Use words and wxp to specify x coord
                                          # Works well for "1 2 3 4 5 6"
                                          # but not for "Destination Port"
                    self.dwg.add(svgwrite.text.Text(
                        words[j], insert=(x+wxp[j],ly),
                        stroke=self.r_colour(r_nbr)))
                        ##font_family="monospace",font_weight="normal",
                        ##font_size=f_height))
            else:  # Just write whole string
                   # Works well for texts with fewer spaces

                print("===> r_nbr %d, colour %s" % (
                    r_nbr, self.r_colour(r_nbr)))
                self.dwg.add(svgwrite.text.Text(
                    text, insert=(x,ly),
                    stroke=self.r_colour(r_nbr)))
                ##font_family="monospace",font_weight="normal",
                ##font_size=f_height))                   
            ly += self.f_height

    def draw_header (self, id, coords, text, parent_id, v1, v2):
        tlc, tlr = self.map(coords[0], coords[1])  # Top left col,row
        trc, trr = self.map(coords[2], coords[1])  # Top right col,row
        # Nothing drawn for header
        return

    def draw_row(self, id, coords, text, parent_id, v1, v2):
        print("draw_row: r_nbr %d, coords %s, len(text) %d, text %s" % (
            v1, coords, len(text), text))
        self.dr_calls += 1
        r_nbr = v1
        print("??? dr_calls %d, r_nbr %d"  % (self.dr_calls,r_nbr))
        vbl_len_row = v2 < 0;  r_lines = abs(v2)
        rx0,ry0 = self.map(coords[0], coords[1])  # Top left x,y
        rx1,ry1 = self.map(coords[2], coords[3])  # Bottom right x,y
        r_width = rx1-rx0
        print("draw_row: r_nbr %d, vbl_len %s, coords %d,%d, %d,%d, r_width %d" % (
            r_nbr, vbl_len_row, rx0,ry0, rx1,ry1, r_width))
        self.last_row_nbr = r_nbr
        if r_nbr < self.last_row_nbr:
            print("r_nbr < last_row_nbr")
            k = r_nbr/0  # Something unexpected occurred!
        #self.last_ri_len = len(self.row_info)
        #self.row_info.append(self.r_info(r_nbr, coords[1],coords[3]))
        #print("=== appended row %d, len(row_info) %d" % (r_nbr, len(self.row_info)))
        
        print("draw_row: calling draw_line, r_nbr %d coords %s" % (r_nbr, coords))
        if r_nbr == 1:  # Header row
            #print("row %d, s_rnbr >%s<" % (v1, s_rnbr))
            self.draw_line([rx0,ry1, rx1,ry1], "x", 6)  # darkblue
        elif vbl_len_row:
            rh = r_lines*self.f_height
            rh2 = round(rh/2.0);  rh4 = round(rh/4.0); 
            self.draw_line([rx0,ry0, rx0,ry0+rh2], "x", r_nbr)
            self.draw_line([rx0,ry1-rh4, rx0,ry1,
                            rx1,ry1, rx1,ry1-rh2], "x", r_nbr)
            self.draw_line([rx1,ry0, rx1,ry0+rh4], "x", r_nbr)
        else:                     
            #self.draw_line([rx0,ry0, rx0,ry1, rx1,ry1, rx1,ry0], "x", r_nbr)
            self.draw_line([rx0,ry0, rx0,ry1, rx1,ry1, rx1,ry0], "x", 5) # green
        self.draw_tics(rx0,ry0, rx1,ry1)
            
    def draw_n_rect(self, coords, n_r_text):
        # coords = centre point for displayed text
        #@??self.dwg.add(self.dwg.rect(
        self.dwg.add(svgwrite.shapes.Rect(
            insert=(coords[0], coords[1]),  # upper left
            size=(coords[2]-coords[0], coords[3]-coords[1]),
            stroke="black", fill="white", stroke_width=1))
        cx = (coords[0]+coords[2])/2.0
        cy = (coords[1]+coords[3])/2.0
        print("_rect coords %s, cx %d, cy %d" % (coords, cx,cy))
        print("nr text >%s<, cx %d, cy %d" % (n_r_text, cx, cy))
        #self.draw_text([cx, cy-2+self.di["f_height"]/2.0], 0, n_r_text)
        # works for text, but too low for n_rect
        self.draw_text([cx, (cy-self.di["f_height"]/2.0)], 0, n_r_text)
        #self.draw_text([cx, (cy-self.di["f_height"]/2.0)], 0, n_r_text)
    
    def draw_tics(self, x0,y0, x1,y1): # x0-x1, y1 = bottomn of header field
        for col in range(0,31):  # Draw column tics
            tx = x0 + self.f_width + (col+1)*self.f_width*2
            tic_width = self.tic_width
            if col%4 == 3:  # Wider ticks every 4th
                tic_width += 1
            self.dwg.add(svgwrite.shapes.Line(
                start=(tx,y1-3), end=(tx,y1), stroke="black", 
                stroke_width=tic_width))
            ##print("tic col %d" % col)
        
    def draw_field(self, id, coords, i_text, parent_id, f_col, width):
        r_obj = self.objects[parent_id]  # Parent Row
        print("draw_field: r_obj %s, coords >%s<" % (r_obj, coords))
        r_nbr = r_obj.v1
        x0,y0 = self.map(coords[0], coords[1])  # Top left x,y
        x1,y1 = self.map(coords[2], coords[3])  # Bottom right x,y
        print("field r_nbr %d: coords x0,y0 %d,%d, x1,y1 %d,%d" % (
            r_nbr, x0,y0, x1,y1))
        
        #self.dwg.add(svgwrite.shapes.Rect(
        #    insert=(x0, y0),  # upper left corner
        #    size=(x1-x0, y1-y0),
        #    stroke=self.r_colour(r_nbr), fill="white", stroke_width=1))

        if f_col != 0:
            #x = coords[0] + f_col*self.f_width
            # Draw line at left of field
            self.draw_line([x0-1,y0-1,x0-1, y1+2], "-", r_nbr)

        #cx = round((x0+x1)/2.0)  # Field's centre is [cx,cy]
        #cy = round((y0+y1)/2.0)
        r_lines = r_obj.v2
        self.vbl_len_row = r_lines < 0
        print(">>> draw_field: row %d: vbl_len %s, %d lines, x0,y0 %d,%d f_col %d, width %d" % (
            r_obj.v1, self.vbl_len_row, r_lines, x0,y0, f_col, width))

        #if r_nbr != 1:
        #ry1 = y1+self.f_height*2
        t_coords = [x0,y0, x1,y1]
        self.draw_text(t_coords, r_nbr, i_text)
        
    def draw_frame(self, min_x,min_y, height,width):
        #print("draw_frame: %d,%d h %d, w %d" % (min_x,min_y, height,width))
        smin_x = str(min_x)+" "
        smin_y = str(min_y)+" "
        sheight = str(height)+" "
        self.dwg.viewbox(smin_x,smin_y, sheight,width)
        #self.dwg.viewbox(min_x,min_y, height,width)
        self.dwg.save()

    def adj_coords(self, coords):
        a_coords = []
        for x in range(0,len(coords),2):
            a_coords.append(coords[x]-self.min_x)    
            a_coords.append(coords[x+1]-self.min_y)
        return a_coords

    def draw_objects(self, which):
        self.d_lines = self.d_n_rects = self.d_texts = 0
        self.d_headers = self.d_rows = self.d_fields = 0
        for obj in self.objects:
            #print("++ obj >%s<" % obj)
            if obj.type == which:
                if obj.type == "line":
                    print(">> line coords %s, text >%s<" % (
                    obj.i_coords, obj.i_text))
                    self.draw_line(self.adj_coords(obj.i_coords),
                                   obj.i_text, 0)  # r_nbr
                    self.d_lines += 1
                elif obj.type == "n_rect":
                    #print(">> n_rect coords %s, text >%s<" % (
                    #    obj.i_coords, obj.i_text))
                    self.draw_n_rect(self.adj_coords(obj.i_coords),
                        obj.i_text)
                    self.d_n_rects += 1
                elif obj.type == "text":
                    print("|%s|" % obj)
                    cx,cy = self.map(obj.i_coords[0],obj.i_coords[1])
                    self.draw_text([cx,cy], 0, obj.i_text)
                    self.d_texts += 1
                elif obj.type == "header":
                    #self.draw_header(obj.id, obj.i_coords, obj.i_text)
                    # Nothing drawn for a header
                    self.d_headers += 1
                elif obj.type == "row":
                    print("About to call draw_row()")
                    print("  max_x %d, coords %s" % (self.di["max_x"], obj.i_coords))
                    self.draw_row(obj.id, obj.i_coords, obj.i_text,
                        obj.parent_id, obj.v1, obj.v2)
                    self.d_rows += 1
                elif obj.type == "field":
                    print(">> field: coords %s, text >%s<" % (
                        obj.i_coords, obj.i_text))
                    x0,y0 = self.map(obj.i_coords[0], obj.i_coords[1])
                    x1,y1 = self.map(obj.i_coords[2], obj.i_coords[3])
                    print("** field x0,y0 %d,%d" % (x0,y0))
                    print("  max_x %d, coords %s" % (self.di["max_x"], obj.i_coords))
                    self.draw_field(obj.id, obj.i_coords, obj.i_text,
                        obj.parent_id, obj.v1, obj.v2)
                    self.d_fields += 1
                                
        print("=== %d lines, %d n_rects, %d texts, %d headers, %d rows, %d fields drawn" % (
            self.d_lines, self.d_n_rects, self.d_texts,
            self.d_headers, self.d_rows, self.d_fields))

        o_fn = "stripped.svg"
        
    def strip_qxml(self, fn):  # "quoted" xml
        full_fn = "full_"+fn
        os.rename(fn, full_fn)
        f = open(full_fn, "r")     
        of = open(fn, "w")
        for line in f:
            ds = line.rstrip('\n')
            if ds == '<?xml version="1.0" encoding="utf-8" ?>':
                print("xml header removed")
            else:
                of.write(ds+'\n')
        of.close()
        f.close()
        
if __name__ == "__main__":
    svg_drawing(sys.argv)
