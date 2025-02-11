# 1713, Mon 19 Aug 2024 (NZST)
# 1625, Tue 31 Oct 2023 (NZDT)
#
# rdd2ascii.py: Convert an rfc-draw .rdd file to an ASCII .txt image;
#
# Copyright 2023, Nevil Brownlee, Taupo NZ

import sys, os.path
import rdd_io, rdd_globals

import debug_print_class as dbpc
dbp = dbpc.dp_env(False)  # debug printing off

class asc_drawing:
    def draw_objects(self, which):
        for obj in self.objects:
            if obj.type == which:
                if obj.type == "line":
                    print(">> line id %d, coords %s" % (obj.id, obj.i_coords))
                    self.draw_line(obj.i_coords, obj.i_text)
                    self.d_lines += 1
                elif obj.type == "n_rect":
                    print(">> n_rect id %d, coords %s, text >%s<" % (
                        obj.id, obj.i_coords, obj.i_text))
                    self.draw_n_rect(obj.id, obj.i_coords, obj.i_text)
                    self.d_rects += 1
                elif obj.type == "text":
                    #print("|%s|" % obj)
                    self.draw_text(obj.i_coords, obj.i_text)
                    self.d_texts += 1
                elif obj.type == "header":
                    #self.draw_header(obj.id, obj.i_coords, obj.i_text)
                    # Nothing drawn for a header
                    self.d_headers += 1
                elif obj.type == "row":
                    print("About to call draw_row()")
                    print("  max_x %d, coords %s" % (self.max_x, obj.i_coords))
                    self.draw_row(obj.id, obj.i_coords, obj.i_text,
                        obj.parent_id, obj.v1, obj.v2)
                    self.d_rows += 1
                elif obj.type == "field":
                    print(">> field: coords %s, text >%s<" % (
                        obj.i_coords, obj.i_text))
                    print("  max_x %d, coords %s" % (self.max_x, obj.i_coords))
                    self.draw_field(obj.id, obj.i_coords, obj.i_text,
                        obj.parent_id, obj.v1, obj.v2)
                    self.d_fields += 1
                    
        print("=== %d lines, %d n_rects, %d texts, %d headers, %d rows, %d fields drawn" % (
            self.d_lines, self.d_rects, self.d_texts,
            self.d_headers, self.d_rows, self.d_fields))

    def __init__(self, sys_argv):
        self.debug = False  # True to put row numbers at left
        print("===> asc_drawing: sys_argv %s" % sys_argv)
        self.rdd_fn = None
        if len(sys_argv) == 1:  # sys_argv[0] = name of program 
            print("No .rdd file specified ???")
            from tkinter.filedialog import askopenfilename
            self.rdd_fn = (askopenfilename(title="Select .rdd source file"))
        self.rg = rdd_globals.gv
        self.x_sf = self.rg.asc_x_sf;  self.y_sf = self.rg.asc_y_sf
        self.bw = self.rg.asc_def_b_w  # Default border width
        if not self.rdd_fn:
            self.rdd_fn = sys_argv[1]
        if len(sys_argv) >= 3:  # We have a second argument
            self.bw = int(sys_argv[2])  # rows and cols
        print("border-width %d" % self.bw)    

        self.rdd_i = rdd_io.rdd_rw(sys_argv, self.bw)
        print("*** rdd_i >%s<" % self.rdd_i) ## rdd_rw object
        self.objects, self.di = self.rdd_i.read_from_rdd()
        self.rdd_i.dump_objects("read in by rdd_io")

        #print("objects >%s< len %d" % (self.objects, len(self.objects)))
        #print("di >%s<" % self.di)

        rd_headers = rd_rows = rd_fields = rd_lines = rd_rects = rd_texts = 0
        for j, val in enumerate(self.rdd_i.objects):
            if val.type == "line":
                rd_lines += 1
            if val.type == "n_rect":
                rd_rects += 1
            if val.type == "text":
                rd_texts += 1
            if val.type == "header":
                rd_headers += 1
            if val.type == "row":
                rd_rows += 1
            if val.type == "field":
                rd_fields += 1
        print(">> %d lines, %d n_rects, %d text  %d headers, %d rows, %d fields" % (
            rd_lines, rd_rects, rd_texts, rd_headers, rd_rows, rd_fields))

        non_hdr_objs = rd_lines+rd_rects+rd_texts
        hdr_objs = rd_headers+rd_rows+rd_fields
        if hdr_objs == 0:
            print("--> no header objects")
            self.x_sf = self.rg.asc_x_sf;  self.y_sf = self.rg.asc_y_sf
        else:
            if float(non_hdr_objs)/hdr_objs < 0.2:
                print("=== mostly header objects")
                self.x_sf = self.rg.hdr_x_sf;  self.y_sf = self.rg.hdr_y_sf
            else:
                print("--- mostly not header objects")
                self.x_sf = self.rg.asc_x_sf;  self.y_sf = self.rg.asc_y_sf
        
        print("self.rdd_i.di >%s<" % self.rdd_i.di)
        self.f_width = self.di["f_width"];  self.f_height = self.di["f_height"]
        print(">>> f_width %s, f_height %s" % (self.f_width, self.f_height))
        self.min_x = self.di["min_x"];  self.max_x = self.di["max_x"]
        self.min_y = self.di["min_y"];  self.max_y = self.di["max_y"]
        print("min_x %d, max_x %d, min_y %d, max_y %d, border_width %d" %
            (self.min_x, self.max_x, self.min_y, self.max_y, self.bw))

        c_min,r_min = self.map(self.min_x,self.min_y)
        c_max,r_max = self.map(self.max_x,self.max_y)
        self.n_chars = int((c_max-c_min+1)*self.x_sf + 2*self.bw)
        self.n_lines = int((r_max-r_min+1)*self.y_sf + 2*self.bw)
        print("c_min %d,c_max %d, n_chars %d, r_min %d,r_max %d, n_lines %d" %
              (c_min, c_max, self.n_chars, r_min, r_max, self.n_lines))
        
        self.lines = [[" " for col in range(self.n_chars + 1)]
                               for row in range(self.n_lines + 1)]  # 1)]
        self.n_n_rect = self.n_line = 0
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.digits = "0123456789ABC"
        self.slc = False  # Set line corner points to show which line it is

        self.n_header = self.n_row = self.n_field = 0
        self.d_lines = self.d_rects = self.d_texts = \
            self.d_headers = self.d_rows = self.d_fields = 0

        self.txt_row_info = []  # each line has r_nbr, y0, ry0

        self.text_fn = self.rdd_fn.split(".")[0]+".txt"

        min_x = min_y = 50000;  max_x = max_y = 0
        for obj in self.objects:
            coords = obj.i_coords
            for n in range(0, len(coords), 2):
                x = coords[n];  y = coords[n+1]  # Text centre (tk Canvas units)
                if obj.type == "text":   ##or obj.type == "n_rect":
                    tw2 = round(obj.txt_width*self.f_width/2)  # tk units
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
        #?print("@@@@@ >%s<" % self.draw_objects)
        self.draw_objects("line")    # layer 1
        self.draw_objects("n_rect")  # layer 2
        self.draw_objects("text")    # layer 3
        self.draw_objects("header")  # Components of rfc-draw Headers
        self.draw_objects("row")     #   all layer 3
        self.draw_objects("field")

        self.print_lbuf(self.text_fn)
        
        print("=..=..= txt_row_info ... len(selftxt_row_info) %d" % len(self.txt_row_info))
        for n,ri in enumerate(self.txt_row_info):
            print("n %d, ri: %d, %3d,%3d, %3d,%3d" % (n, ri[0], ri[1],ri[2], ri[3],ri[4]))
        print("- - - - - -")
    def r_info(self, r_nbr, y0,y1, ry0,ry1):  # Diagnostic for rows
        return [r_nbr, y0,y1, ry0,ry1]

    def map(self, x, y):  # Map x,y (from rdd) to col,row (in lines 2D array)
        xr = x-self.min_x
        col = round(xr*self.x_sf/self.f_width) + self.bw  # LH, RH
        yr = y-self.min_y
        row = round(yr*self.y_sf/self.f_height)+ self.bw  # Top, Bot

        print("@map: col %s %s, row %s %s" % (col,type(col), row,type(row)))
        return col, row

    def print_lbuf(self, txt_fn):
        #afn = self.asc_filename.split("/")[-1] 
        # Bug reported: becarpenter, 22 Oct 2023 (NZDT)
        #   "Will write .txt file to current directory"
        print("-> -> print_lbuf to %s" % txt_fn)
        bb = " "*self.bw  # Border blank cols
        asc_file = open(txt_fn, "w")
        for r in range(self.bw):
            asc_file.write(" \n")
        for r,val in enumerate(self.lines):
            if r != 0:  # Don't print (empty) top line of row 1 (colnbrs)
                txt_line = ''.join(val)
                t_line = txt_line.rstrip()
                print("len(txt_line) = %d" % len(t_line))
                if self.debug:
                    asc_file.write("%3d %s%s%s\n" % (r, bb,t_line))
                else:
                    asc_file.write("%s%s%s\n" % (bb, t_line, bb))
        for r in range(self.bw):
            asc_file.write(" \n")
        asc_file.close()

    def set_char(self, ch, xc,yr):  # Must not overwrite "+"
        ln = self.lines[yr]
        #if ln[xc] != "+":
        #    ln[xc] = ch
        ln[xc] = ch
    
    def draw_line(self, coords, text):
        # text chars: one or more of a/n, e
        print("LLL draw_line coords %s, text %s" % (coords, text))
        rc_coords = []
        for p in range(0, len(coords), 2):  # Convert to col,row coords
            col,row = self.map(coords[p], coords[p+1])
            rc_coords.append(col)
            rc_coords.append(row)
        print("rc_coords = %s" % rc_coords)

        self.n_line += 1
        for p in range(0,len(rc_coords)-2,2):  # Draw the line
            ch = self.digits[self.n_line]
            x0 = rc_coords[p];  y0 = rc_coords[p+1]  # segment x0,y0 to x1,y1
            x1 = rc_coords[p+2];  y1 = rc_coords[p+3]
            print("line rc0,rl0 = %d,%d, rc1,rl1 = %d,%d" % (x0,y0, x1,y1))
            #print(">>> p %s, x %s, y %s :: %d lines" % (p,x,y,len(self.lines)))
            if x0 == x1:     # vertical
                if abs(y1-y0)+1 < 3:
                    print("line segment %d [%d,%d, %d,%d] too small to draw" % (
                        (p, x0,y0, x1,y1)))
                    ln = self.lines[y0];  ln[x0] = "?"
                else:
                    cy = round((y0+y1)/2)
                    if y0 < y1:  # down
                        print("  line down, %d,%d -> %d,%d" % (x0,y0, x1,y1))
                        self.set_char("+", x0,y0)
                        for y in range(y0+1,y1):
                            print(".|. x0 %d, y=%d" % (x0,y))
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
            self.set_char(">", sx,sy)  # beginning of syntax line
            self.set_char(">", sx+1,sy)
            ex,ey = rc_coords[-2:]
            self.set_char(">", ex-1,ey)  # end of syntax line
            self.set_char("<", ex,ey)

    def draw_text(self, coords, text):
            # drawn with anchor=tk.CENTER, coords are text's centre point <<<
        print("@text %s, coords %s" % (text, coords))
        txcol, txrow = self.map(coords[0], coords[1])  # text row,col
        print("text: >%s<, txcol %d, trow %d" % (text, txcol,txrow))
        #! t_row = 12 # centre line for text
        t_lines = text.split("\n")
        print("t_lines = >%s<" % t_lines)
        # Find centre of text block
        mx_tlen = 0
        for j in range(len(t_lines)):
            if len(t_lines[j]) > mx_tlen:
                mx_tlen = len(t_lines[j])
        print("mx_tlen = %d" % mx_tlen)
        #txcol += 1
                                          # col txcol = text centre 
        tll = txcol-round(mx_tlen/2.0)-1    # col (leftmost char)
        tlend = txcol+round(mx_tlen/2.0)-1  # col (rightmost char)
        tlr = txrow-int(len(t_lines)/2.0)  # middle row
        print("tll %d, tlend %d, tlr %d" % (tll, tlend, tlr))
        
        for r,text in enumerate(t_lines):  # Centre the text lines
            print("?+? tlr %d, r %d" % (tlr, r))
            ln = self.lines[tlr+r]
            tlc = int(txcol-len(text)/2.0)  # text, leftmost col
            print("txt copy loop, len(text) %d, tlc %d" % (len(text), tlc))
            for j in range(len(text)):
                ln[tlc+j] = text[j]
                dbp.db_print("ln >%s<" % text[j])
            dbp.db_print("ln >>%s<<" % ln)

    def draw_field_text(self, text, cx,cy, r_nbr, r_lines):
            # cx,cy are 0-org, r_lines = nbr of lines in field's row
            # drawn with anchor=tk.CENTER, cx,cy are text's centre point <<<
        #print("@text %d, coords %s" % (m_key, coords))
        txcol, txrow = self.map(cx, cy)  # text centre (row,col)
        print("-2-> cx,cy, %d,%d, txcol,txrow %d,%d, r_nbr %d, r_lines %d" % (
            cx,cy, txcol,txrow, r_nbr, r_lines))  # txcol,txrow = 19,12
                                          # Should be 18,12
        t_lines = text.split("\n")   # colnbrs should start at row 1
        print("t_lines = >%s<" % t_lines)
        # Find centre of text block
        mx_tlen = 0
        for j in range(len(t_lines)):
            if len(t_lines[j]) > mx_tlen:
                mx_tlen = len(t_lines[j])
        print("mx_tlen = %d (%s)" % (mx_tlen, type(mx_tlen)))
        print("@@mx_tlen/2.0 = %s" % round(mx_tlen/2.0))

        #rtl = txrow-round(len(t_lines)/2.0)  # field row's top line
        # col txcol = text centre
        txlc = txcol-round(mx_tlen/2.0)  # col (leftmost char)
        txrc = txcol+round(mx_tlen/2.0)  # col (rightmost char)
        print("-3-> txlc %d, txrc %d" % (txlc, txrc))
        
        tlr = txrow  # text's top line
        print("txlc,txrc = %d, %d" % (txlc,txrc))

        print("   txcol, txrow %d, %d" % (txcol, txrow))
        #tlr = max(tlr, ry0)  # Don't go above row ???
        #print("&&& tlr now %d" % tlr)
        for r,text in enumerate(t_lines):  # Centre text lines inside row
            print("??? r %d, txrow+r %d, tlr %d >%s<" % (r, txrow+r, tlr, text))
            #r += self.bw
            if len(t_lines) > r_lines:
                print("field text won't fit into field's row!")
            ln = self.lines[txrow+r]
            tlc = round(txcol-len(text)/2.0)  # text, leftmost col
            print("txt copy loop, len(text) %d, tlc %d" % (len(text), txlc))
            for j in range(len(text)):
                ln[txlc+j] = text[j]

    def find_txt_rows(self, txl, tr,br, r_nbr, r_lines):
        print("ftr: txl %d, tr,br %d,%d, r_nbr %d" % (txl, tr,br, r_nbr))
        if txl > r_lines:
            print("text won't fit into row <<<")
            exit()
        nb_lines = r_lines-txl  # Nbr of blank lines needed around text
        print("ftr> nb_lines = %d" % nb_lines)
        if r_nbr == 1:
            print("TT")
            tr += 1; br -= 1  # colnbrs inside row frame
        else:
        #    print("BB")
            while nb_lines > 0:
                br -= 1
                nb_lines -= 1
                if nb_lines > 0:
                    tr += 1
                    nb_lines -= 1
        print("===> text in rows %d to %d" % (tr,br))
        return tr,br  

    def draw_text_in_row(self, text, fc, tr, br, r_nbr, r_lines):
        # For text centred within row r_nbr
        print("+-+ draw_text_in_row: tr,br %d,%d, r_nbr %d, r_lines %d" % (
            tr,br, r_nbr, r_lines))
        tx_lines = text.split("\n")
        dtr,dbr = self.find_txt_rows(len(tx_lines), tr,br, r_nbr, r_lines)
        print("=== dtr,dbr = %d,%d" % (dtr,dbr))
        print("tx_lines  >%s<" % tx_lines)
        print("=1= len(tx_lines) = %d" % len(tx_lines))
        j = 0
        for ry in range(dtr+1,dbr):
            if j == len(tx_lines):
                break
            print("??? dtr %d, dbr %d, ry %d" % (dtr, dbr, ry))
            ln = self.lines[ry]
            print("--- ry %d, j %d,len(ln) %d ln >%s<" % (ry, j, len(ln), ln))
            tx_ln = tx_lines[j]
            dbp.db_print("len(tx_ln) %d, tx_ln >%s<" % (len(tx_ln), tx_ln))
            for c in range(len(tx_ln)):
                ln[self.bw+fc+c] = tx_ln[c]
            j += 1

    def draw_text_row(self, text, c, r):
        ln = self.lines[r]
        dbp.db_print(
            "$ $ $ draw_text_row: c %d, r %d, len(text) %d" % (c, r, len(text)))
        for j in range(len(text)):
            #print("c %d, j = %d" % (c,j))
            ln[c+j] = text[j]

    def draw_n_rect(self, id, coords, n_r_text):
        # coords = centre point for displayed text
        tlc, tlr = self.map(coords[0], coords[1])  # Top left col,row
        brc, brr = self.map(coords[2], coords[3])  # Bottom right col, row
        if brc-tlc+1 < 3 or brr-tlr+1 < 3:
            print("rectangle at %d,%d, %d,%d too small to draw" % (
                tlc,tlr, brc,brr))
            print("  Min rectangle size is 3x3 chars <<<")
        print("n_rect r,c coords: %d,%d to %d,%d >%s<" % (
            tlc,tlr, brc,brr, n_r_text))
                                    # 1,20 to 31,22
        self.n_n_rect += 1
        ch = self.alphabet[self.n_n_rect]
        h_row = "+" + "-"*(brc-tlc-2) + "+"
        print("h_row %s" % h_row)
        v_row = "|" + " "*(brc-tlc-2) + "|"
        print("v_row %s" % v_row)
        self.draw_text_row(h_row, tlc,tlr)
        for j in range(tlr+1, brr):
            self.draw_text_row(v_row, tlc, j)
        self.draw_text_row(h_row, tlc,brr)
        self.print_lbuf("nr-frame.txt")
        print("+++ tlc %d, tlr %d" % (tlc,tlr))

        cx = round((coords[0]+coords[2])/2.0)
        cy = round((coords[1]+coords[3])/2.0)
        print("cx,cy %d,%d, text >%s<" % (cx,cy, n_r_text))
        self.draw_text([cx,cy], n_r_text)

    def draw_header(self, id, coords, text, parent_id, v1, v2):
        tlc, tlr = self.map(coords[0], coords[1])  # Top left col,row
        trc, trr = self.map(coords[2], coords[1])  # Top right col,row
        # Nothing drawn for header
        return

    def draw_top_line(self, rn, text):
        ln = self.lines[rn]
        for j in range(len(text)):
            ln[self.bw+j] = text[j]        

    def draw_bottom_line(self, row_nbr, bly, text):
        ln = self.lines[bly]
        for j in range(len(text)):
            ln[self.bw+j] = text[j]
        if self.debug:
            rn_s = str(row_nbr)  # Put row nbr in row's bottom line
            for j in range(len(rn_s)):
                ln[self.bw+j] = rn_s[j]

    def draw_row(self, id, coords, text, parent_id, v1, v2):
        print("draw_row: r_nbr %d, coords %s, len(text) %d, text %s" % (
            v1, coords, len(text), text))
        r_nbr = v1
        vbl_len_row =  v2 < 0;  n_lines = abs(v2)
        tlc, tlr = self.map(coords[0], coords[1])  # Top left col,row
        brc, brr = self.map(coords[2], coords[3])  # Bottom right col,row
        r_width = (brc-tlc-1)
        print("draw_row: r_nbr %d, coords %d,%d, %d,%d, r_width %d" % (
            r_nbr, tlc,tlr, brc,brr, r_width))
        #!if r_nbr == 1:
        #!    brr -= 1
        self.last_row_nbr = r_nbr
        if r_nbr < self.last_row_nbr:
            print("r_nbr < last_row_nbr")
            k = r_nbr/0
        self.last_row_nbr = r_nbr
        self.last_ri_len = len(self.txt_row_info)
        self.txt_row_info.append(self.r_info(r_nbr, coords[1],coords[3], tlr,brr))
        print("=== appended row %d, len(txt_row_info) %d" % (r_nbr, len(self.txt_row_info)))

        t_line = "+" + "-+"*32 + " "*self.bw
        if r_nbr == 1:  # Header row
            #print("row %d, s_rnbr >%s<" % (v1, s_rnbr))
            self.draw_bottom_line(r_nbr, brr, t_line)
        else:                       
            #self.draw_top_line(tlr, t_line)
            print("     len h_row %d" % (len(t_line)))
            for j in range(tlr+1, brr):
                self.lines[j][self.bw] = "|"
                self.lines[j][brc-1] = "|"
            self.draw_bottom_line(r_nbr, brr, t_line)

            
    def draw_field(self, id, coords, i_text, parent_id, f_col, width):
        r_obj = self.objects[parent_id]
        ###y0 = coords[1];  y1 = coords[3]
        rc0,rr0 = self.map(r_obj.i_coords[0], r_obj.i_coords[1])  # Field's row
        rc1,rr1 = self.map(r_obj.i_coords[2], r_obj.i_coords[3])
        print("-field's row-> rc0.rr0 %d,%d, rc1,rr1 %d,%d" % (
            rc0,rr0, rc1,rr1))  # rr0 and rr1 are the +_+_+_ lines in .txt <<<
        print("draw_field: r_obj >%s<" % r_obj)
        fc0,fr0 = self.map(coords[0], coords[1])  # Field coords
        fc1,fr1 = self.map(coords[2], coords[3])
        r_nbr = r_obj.v1
        r_lines = abs(r_obj.v2)
        print("fc0,fr0 %d,%d, fc1,fr1 %d,%d, r_lines %d" % (
            fc0,fr0, fc1,fr1, r_lines))
        print("+++>> field from %d,%d down to %d,%d" % (fc0,fr0, fc1,fr1))
        if f_col != 0:
            #x = coords[0] + f_col*self.f_width
            fr = fr0
            for ln in range(0,r_lines):  # Draw line at left of field
                print("@@@ fr0 %s (%s), ln %s (%s)" % (
                    fr0, type(fr0), ln, type(ln)))
                tln = fr0+1+ln+1
                print("$$$ tln %d (%s)" % (ln, type(tln)))
                #ln = self.lines[fr0+1+ln]
                ln = self.lines[fr0+1+ln]
                ln[fc0-1] = "|"  # -1 draws rbar to left of col_nbr digit
        #self.draw_text_in_row(i_text, rc0+1, rr0,rr1, r_nbr, r_lines)

        cx = round((coords[0]+coords[2])/2.0)  # Field's centre is [cx,cy]
        cy = round((coords[1]+coords[3])/2.0)
        print(">>> draw_field: cx,cy %d,%d, f_col %d, width %d" % (
            cx,cy, f_col, width))
        print("-1->   cx,cy -> %s, %s" % (cx,cy))
        if r_nbr == 1:
            cy += self.f_height  # Put colnbrs at bottom of row 1
        n_lines = r_obj.v2
        self.draw_text([cx,cy], i_text)
        #self.draw_field_text(i_text, cx,cy, r_obj.v1, r_obj.v2)

        
if __name__ == "__main__":
    asc_drawing(sys.argv)
