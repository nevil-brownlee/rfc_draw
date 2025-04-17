# 1619, Sat 25 Nov 2023 (NZDT)  >>> may22 <<
# 1432, Mon 11 Nov 2024 (NZDT)
#
# draw_headers_class: functions to draw/move/edit packet headers
#
# Copyright 2024, Nevil Brownlee, Taupo NZ

import tkinter as tk, re, sys, math, time
import rfc_draw_globals_class as rdgc  # rfc-draw globals
import draw_texts_class as dtc    # Handles text objects

import traceback  # For debugging using n_stack (below)

class draw_headers:  # pkt header objects for rfc-draw
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)  # New instance of text_info
    """    
    def n_stack(tb):
        for ln,txt in enumerate(tb):
            print("%3d %s" % (ln,txt[0:-1]))
        print("+ + +")`
    """
    def wait_for_input(self, prompt):
        print("wait_for_input %s ..." % prompt);  q = input()
        print("- - OK - -")
        return

    drawing = root = rdg = None  # Set in __init__ (below)
    
    headers = []  # Header objects, indexed by h_nbr
    n_headers = 0
    hdr_mode = "normal"
    crl_coords = None

    def __init__(self, parent, root, rdg):
        super().__init__()
        self.drawing = parent;  self.root = root;  self.rdg = rdg
        draw_headers.drawing = self.drawing
        draw_headers.rdg = self.rdg
        #print("starting draw_headers_class, rd_globals %s" % self.rdg)
        draw_headers.line_height = rdg.f_height          # 17
        #print("??? line_height %d" % draw_headers.line_height)
        draw_headers.f_font = rdg.f_font
        #print(draw_headers.f_font)
        draw_headers.tic_height = round(self.rdg.f_height/4)  # 4

        self.dtc_tool = dtc.draw_texts(self.drawing, self.root, self.rdg)
        self.double_click_flag = False
        self.move_c_o = None  # Current object being moved
        self.rdg.last_mx = self.rdg.last_my = 0
        self.hm_count = 0;

        #self.adding_row = False  # True while dragging down

    #def undraw_object(self, d_obj):  # For rdgc.on_delete_key()
    #    print("UNDRAW h/r/c object: d_obj %s" % d_obj)
    #    #del self.rdg.objects[d_obj.key]  # Remove obj from dictionary
    #    d_obj.obj.undraw_object(d_obj)

    class header:  # Creates a new Header object
        def __init__(self, drawing, root, rdg, h_nbr, h_coords, v2):
        #   Header objects are drawn with pale-colour edr's, o_type 'header'
        #     Their header number is saved
        #     They have their own objects, keeping track of object positions
        #     Their move function must move all their contained objects
            #print("!!! class header: rdg %s (%s)" % (rdg, type(rdg)))
            self.drawing = drawing;  self.rdg = rdg;  self.root = root
            self.h_nbr = h_nbr
            #print("header __init__: h_nbr >%s<, new_drawing %s, f_font %s" % (
            #    h_nbr, self.rdg.new_drawing, draw_headers.f_font))
            self.rows = []  # Header's n row objects (rows 0 to n-1)
            #print(" | | | self.rows %s" % self.rows)
            #print(" ^ ^ ^ header: h_nbr %s (%s)" % (h_nbr, type(h_nbr)))
            self.row_ids = []  # rows 0 to n-1, i.e. n rows
            #print("class header: f_font >%s<, h_coords %s, h_nbr %s" % (
            #    draw_headers.f_font, h_coords, self.h_nbr))
            self.type = "header"

            self.ch_width = 8  # char width (pixels, from header experiments)
            self.bdr = 6  # L+R border (inside rows)
            self.tic_width = 2
            self.f_lgap =  0  # Field's gap at left of row
            self.r_width = self.bdr + 64*self.ch_width + self.bdr
            self.r_tgap =  15  # Row's gap at top (was 9)
            self.r_bgap =   0  # Row's gap at bottom
            
            #print("<> <> h_coords %s" % h_coords)
            self.x0, self.y0 = h_coords[0:2]  # Top line left
            self.x1 = self.x0+self.r_width;  self.y1 = self.y0  # and right
            self.tl_coords = [self.x0, self.y0, self.x1, self.y1]
            #print("$$$ tl_coords %s" % self.tl_ccoords)
            self.hdr_id = 0  #  top line not drawn
            self.hdr_id = self.rdg.add_to_layer(2, # Draw header top line
                self.drawing.create_line,self.tl_coords,fill="white") # <<<<<
            # We need a hdr_id (tk object) for each header in our drawing,
            #   and the top line is the only such object!
            #print("=========== header %d, top line drawn ==========" %
            #    self.h_nbr)
            #print("header %d,%d, %d, %d" % (
            #    self.x0, self.y0, self.x1, self.y1))
            self.rdg.time_now("hdr %d,top line drawn" % self.hdr_id)
            self.h_tag = "h_%d" % self.h_nbr
            self.drawing.itemconfig(self.hdr_id, tag=self.h_tag)

            ##print("? ? ? header.new self %s (%s)" % (self, type(self)))
            h_rdo = self.rdg.object(  # hdr obj just has it's top line
                self.hdr_id, self, "header", self.tl_coords, "H",
                0, self.h_nbr, v2)  # Parent for rows
            #print("-->> hdr_obj key %d" % self.hdr_id)  # OK, key 1
            ##if self.hdr_id in self.rdg.objects:
            ##    print("*** header object hdr_id %s already in objects[]" %
            ##        self.hdr_id)
            ##    exit()
            self.rdg.objects[self.hdr_id] = h_rdo
            self.rdg.current_object = h_rdo
            #print(">< header >< self.rdg.new_drawing %s, %d rows" % (  #? OK
            #    self.rdg.new_drawing, len(self.rows)))
            #print("?? ?? hdr_id %d, objects[%d] >%s<" % (
            #    h_rdo.key, h_rdo.a_obj.hdr_id, self.rdg.objects[self.hdr_id]))

            if self.rdg.new_drawing: #! and len(self.rows) == 0:
                # Didn't read drawing from save file, need to draw col_nbrs
                self.rdg.time_now("hdr, top line drawn 2")
                self.h = h_rdo.a_obj
                #print("H H H startup self.rdg %s" % self.rdg)
                self.rdg.time_now("hdr, hdr top line drawn")
                self.hr = draw_headers.row(  # Row 1, for col_nbrs
                   self.drawing, self.rdg, self, 2)  # lines
                self.draw_col_nbrs(self.h, self.hr)  # under (white) top line
                # Draw row 1 (header's top row), just tics and col nbrs
                #print("<><> header.new h %s, rdg.new_drawing %s" % (
                #    self, self.rdg.new_drawing))
                #print("header row: hr %s" % self.hr)
                draw_headers.headers.append(self)
                #self.show_draw_headers("new header():")
                self.rdg.dump_objects("col_nbrs drawn, %d rows" % len(
                    self.rows))
            #print("new header, h_nbr %d, %s" % (self.h_nbr, rself))

        def new_header_nbr(self):
            #print("-|-|- new_header_nbr()")
            if draw_headers.n_headers == self.rdg.mx_headers:
                self.display_msg("Can only have at most %d headers!" % \
                                 self.rdg.mx_headers, "error")
            else:
                #print("rdg_new_header_nbr: n_headers %d" % draw_headers.n_headers)
                draw_headers.n_headers += 1
                print("    n_headers now %d" % draw_headers.n_headers)
            return draw_headers.n_headers

        def show_draw_headers(self, id_text):
            print("|| headers: >%s<" % id_text)
            for hn in range(0, len(draw_headers.headers)):
                print("hn %d, header %s" % (hn, draw_headers.headers[hn]))
            print(" ")
                  
        def __str__(self):
            #print("!!!!! header: h_nbr %s" % self.h_nbr)
            return "header: h_nbr %d, len(rows) %d" % (
                self.h_nbr, len(self.rows))
        
        def draw_col_nbrs(self, h, hr):
            #print("= = = starting draw_col_nbrs, h_tag >%s< = = =", h.h_tag)
            #print(">< draw_col_nbrs >< self.rdg.new_drawing %s, %d rows" % (
            #    self.rdg.new_drawing, len(h.rows)))
            #print(". . . h  %s" % h)
            #print(". . . hr %s" % hr)
            col_nbrs = "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1"
            #print("col_nbrs 1: h %s, hr %s" % (h, hr))
            cn_field = draw_headers.field(
                self.rdg, h, hr, col_nbrs, 0, 32, None)
            #print("?+?+? n_field %s (%s)" % (cn_field, type(cn_field)))
            
        def bbox(self):  # Gets the current coords
            return self.x0, self.y0, self.x1, self.y1

        def coords(self, x0, y0, x1, y1):  # Set the header's coords
            self.x0 = x0;  self.y0 = y0;  self.x1 = x1;  self.y1 = y1
            self.drawing.coords(self.hdr_id, x0,y0, x1,y1)  # Move the header
            self.cx = (x1+x0)/2;  self.cy = (y1+y0)/2

        def move(self, ho, dx,dy):  # Move a header (+ it's rows and fields)
            self.drawing.move(ho.h_tag, dx,dy)
            ho.x0 += dx;  ho.x1 += dx
            ho.y0 += dy;  ho.y1 += dy

        def mk_save_str(self, val):  # Make header's rdd file entry
            #$print("$ $ $ header mk_save_str: type(self) = %s" % type(self))
            #$print(" $ $  type(val) %s, val %s" % (type(val), val))
            h_clo = val.a_obj
            if val.o_type != "header":
                print("!=!= header.mk_save_str: val %s" % val)
                x = 123/0
            h_clo = val.a_obj;  d_id = val.key
            
            #4print("header's h >%s< (%s)" % (h_clo, type(h_clo)))
            h_val = self.rdg.objects[val.key]
            #$print("=+=+= h_val >%s<" % h_val)
            hn = h_clo.h_nbr
            #$print("!!! hn = %s" % hn)
            #if h_val.v2 == 1:  ##### v2 was 0 here!
            #    h_state = self.drawing.itemcget(h.hdr_id, 'state')
            #    print("#$#$# h_state >%s<" % h_state)
            #    ######### need a way to remember our b1_double 
            #    val = h_val
            #$print("-+- header, h_val.v2 = %d" % h_val.v2)
            d_type = "header"
            x0,y0, x1,y1 = h_clo.bbox()
            i_coords = [x0,y0, x1,y1];  coords = []
            for c in i_coords:
                coords.append(int(float(c)))
            ds = "(%s %d) %s \"%s\" %s %s %s" % (
                "header", val.key, coords, "H", 0, h_clo.h_nbr, val.v2)
            #$print(" header  ds >%s<" % ds)
            return ds
        # Need to save all the header's rows and fields here !!!!!!!!

        def restore_object(self, h_coords, h_text, parent_id, v1, v2):  # For rdgc.on_insert_key()
            #print("RESTORE header")
            self.type = "header"
            self.x0, self.y0, self.x1, self.y1 = h_coords
            self.text = h_text;  self.hdr_id = parent_id
            self.h_nbr = v1
            h_obj = draw_headers.header(
                draw_headers.drawing, draw_headers.root,
                draw_headers.rdg, self.h_nbr, r_coords)
            #print("+++ h_obj >%s<" % h_obj)
            draw_headers.rdg.current_object = h_obj
            #!!draw_headers.headers.append(h_obj)  # Done in class header()
            #print("restore header, headers %s" % draw_headers.headers)
            self.rdg.n_headers += 1
            
        def undraw(self, d_obj):  # For rdgc.on_delete_key()
            #print("UNDRAW header")
            obj = d_obj.a_obj
            self.rdg.drawing.itemconfigure(obj.h_tag, state=tk.HIDDEN)

        def redraw(self, d_obj):  # For rdgc.on_insert_key()
            #print("REDRAW header")
            obj = d_obj.a_obj
            self.rdg.drawing.itemconfigure(obj.h_tag, state=tk.NORMAL)

    class row:
        def __init__(self, drawing, rdg, h, r_lines):  # h is an h_clo
            # h is this row's parent header, bottom right is h.x1,h.y1
            # Down from rx,ry, across to rx+r_width, back up
            #   with tic-marks at bottom between cols
            self.drawing = drawing;  self.rdg = rdg
            self.h = h;  self.r_lines = r_lines
            self.vbl_len_row = r_lines < 0
            self.r_lines = abs(r_lines)
            print("class row, h %s (%s), r_lines %d, vbl_len_row %s" % (
                h, type(h), self.r_lines, self.vbl_len_row))

            self.hdr_id = h.hdr_id

            print("RRRRR starting class row, h = %s" % h)
            self.tic_ids = [];  self.fields = []
            self.mx_txt_lines = 0  # max nbr of text lines in fields
            #print("??? class row, h %s, fields = %s" % (self.h, self.fields))
            #print("row: h %s (%s)" % (h, type(h)))
            #print("h.line_height %d" % h.line_height)  # = font height
            self.h_tag = h.h_tag
            #if len(h.rows) == 0:  # No rows added yet, add top row
            #    self.x0, self.y0, self.x1, self.y1 = h.tl_coords
            #else:
            #self.x0, self.y0, self.x1, self.y1 = h.bbox()
            self.x0, self.y0, self.x1, self.y1 = h.bbox()
            # Header (and lowest row's) bottom line is x0,y1, x1,y1
            r_width = self.x1-self.x0;  self.x1 = self.x0+r_width
            print("row header %d, n_rows %d, x0,y0, x1,y1 %d,%d, %d,%d" % (
                self.h.h_nbr, len(h.rows), self.x0,self.y0, self.x1,self.y1))

            #print("   types y0 %s, y1 %s" % (type(self.y0), type(self.y1)))
            #print("   height = %d" % (self.y1-self.y0))
            print("   len(h.rows) = %d" % len(h.rows))

            if len(h.rows) == 0:  # No rows added yet, add top row
                # x0,y0, x1,y1 are header's top line ends
                #???self.y0 -= 4  # x0,y0 from self.h  <<<<<<<<<<<<<<<<<<<<<<
                self.h.y1 = self.y1 = self.y0 + \
                    self.row_height(2) - draw_headers.tic_height*2 # ????????
                # self.y0 += draw_headers.tic_height  # ???????????
                #### Tried y0 += *3 and then y0 += *1 ... didn't work
                # Update hdr coords to include (new) lowest row
                self.row_id = h.rdg.add_to_layer(1, # Draw encl (v_^) line
                    h.drawing.create_line,
                    (self.x0,self.y1, self.x1,self.y1), fill="black")
                    #(self.x0,self.y0, self.x0,self.y1,
                    #    self.x1,self.y1, self.x1,self.y0), fill="blue")
                print("row 1: %d,%d, %d, %d" % (
                    self.x0, self.y0, self.x1, self.y1))
                self.r_nbr = 1;  self.r_tag = "r_1"
                #draw_headers.wait_for_input(self, "drawn first |_|")  # OK
            else:  # New row at bottom
                self.r_nbr = len(h.rows)+1  # Can't be 0!
                self.r_tag = "r_"+str(self.r_nbr)  # To find a row
                self.x0,self.y0, self.x1,self.y1 = h.rows[-1].bbox()
                    # get row's x0 and x1
                #print("+++ new row at bottom, len(h.rows) %d" % len(h.rows))
                #print("x0,y0 %d,%d, x1,y1 %d,%d" % (self.x0,self.y0, self.x1,self.y1))
                ##print("bottom row %d,%d, %d, %d" % (
                ##    self.x0,self.y0, self.x1,self.y1))
                self.y0 = self.y1;  # From previous row
                self.h.y1 = self.y1 = self.y0+self.row_height(self.r_lines)
                #print("->-> vbl_len_row %s, h_tag %s" % (
                #    self.vbl_len_row, self.h.h_tag))
                if len(h.rows) == 0:
                    rl_coords = (self.x0,self.y1, self.x1,self.y1)
                    self.row_id = h.rdg.add_to_layer(1, # Draw bottom line
                        h.drawing.create_line, rl_coords)
                else:
                    if not self.vbl_len_row:
                        rl_coords = (self.x0,self.y0, self.x0,self.y1,  # |_|
                            self.x1,self.y1, self.x1,self.y0)
                        self.row_id = h.rdg.add_to_layer(1,
                            h.drawing.create_line, rl_coords)
                        #print("+-1-+ row %d drawn" % self.r_nbr)
                    else:  # vbl_len_row
                        lh = draw_headers.line_height;  lh2 = round(lh/2)
                        rh = self.r_lines*lh
                        rh2 = round(rh/2.0);  rh4 = round(rh/4.0)
                        self.row_id = self.draw_l_seg(self.h.h_tag, self.r_tag,
                            [self.x0,self.y0, self.x0,self.y0+rh2])
                        self.draw_l_seg(self.h.h_tag, self.r_tag,
                            [self.x0,self.y1-rh4, self.x0,self.y1,
                             self.x1,self.y1, self.x1,self.y1-rh2])
                        self.draw_l_seg(self.h.h_tag, self.r_tag,
                            [self.x1,self.y0,self.x1,self.y0+rh4])
                    
            h.row_ids.append(self.row_id)
            self.drawing.itemconfig(self.row_id, tag=self.r_tag)
            self.drawing.addtag_withtag(self.h.h_tag, self.row_id)
            self.drawing.itemconfig(self.r_tag, state=tk.NORMAL)

            ##draw_headers.wait_for_input("row |_| drawn")

            ##self.x1 = self.x0;  self.y1 = new_y1
            self.r_coords = [self.x0,self.y0, self.x1,self.y1]
            #print("r coords = %s, r_nbr %d" % (self.r_coords, self.r_nbr))
            ##print("@@@ h.hdr_id %s" % h.hdr_id)
            row_obj = h.rdg.object(
                self.row_id, self, "row", self.r_coords, "R",
                     h.hdr_id, self.r_nbr, r_lines)  # parent, v1, v2
                     # was h.h_nbr
            #print("@@@ row_obj >%s<, h %s, h.rows >%s<" % (row_obj, h, h.rows))
            h.rows.append(self)  # Append to actual header!
            #print("@@@ appended row %d to header %s; r_nbr %d" % (
            #    len(h.rows), h, self.r_nbr))
            #print("@+@ row_obj >%s<, h %s, h.rows >%s<" % (row_obj, h, h.rows))
            self.h.x1 = self.x1;  self.h.y1 = self.y1
            if self.r_nbr != 1:
                self.draw_tics(self.h)  # tics at h.y1
            ##print("+++ row_obj key %d, r_nbr %d, len(h.rows) %d" % (
            ##      self.row_id, self.r_nbr, len(h.rows)))  ## == 2 here
            if self.row_id in self.rdg.objects:
                print("*** row object row_id (%d) already in objects[]" % self.rcow_id)
                exit()
            self.rdg.objects[self.row_id] = row_obj
            #print("row_obj %s" % row_obj)  #< parent_id 1 (= hdr_id)
            #print("   objects[%d] = %s" % (
            #    self.row_id, h.rdg.objects[self.row_id]))

            #f = self.field(self.rdg, h, row_obj.obj, "field-name", 0, 32, None)
            #print("   row %d drawn\n" % self.r_nbr)

        #def rdr_border(self):  # Redraw row border
        #    print("!!! rdr_border !!!")
        #    self.rdg.drawing.coords(self.row_id, self.x0,self.y0,
        #        self.x0,self.y1, self.x1,self.y1, self.x1,self.y0)

        def __str__(self):
            return "row: h_nbr %d, r_nbr %d," % (
                self.h.h_nbr, self.r_nbr)

        def draw_l_seg(self, h_tag, r_tag, rl_coords):
            self.row_id = self.rdg.add_to_layer(1, # Draw line segment(s)
                self.drawing.create_line, rl_coords)
            self.drawing.itemconfig(self.row_id, tag=h_tag)
            self.drawing.addtag_withtag(r_tag, h_tag)
            return self.row_id

        def row_height(self, r_lines):
            return  self.h.r_tgap + r_lines*draw_headers.line_height + \
               draw_headers.tic_height + self.h.r_bgap  # px

        def bbox(self):  # Get row current coords
            return self.x0, self.y0, self.x1, self.y1

        def draw_tics(self, h):
            t_t_tag = "t_t"  # So we can tell it's a tic!
            t_h_tag = "h_"+str(self.h.h_nbr)
            t_r_tag = "r_"+str(self.r_nbr)  # To find row for a tic
            #print(">> draw_tics h %s, len(h.rows) %d, t_r_tag %s" % (
            #    h, len(h.rows), t_r_tag))
            for col in range(0,31):  # Draw column tics
                cx = self.x0 + h.ch_width + (col+1)*h.ch_width*2
                tic_width = h.tic_width
                if col%4 == 3:  # Wider ticks every 4th
                    tic_width += 1
                tic_id = self.rdg.add_to_layer(1, # Draw a tic
                    self.drawing.create_line, (cx,self.y1-draw_headers.tic_height,
                        cx,self.y1), width=tic_width)
                self.tic_ids.append(tic_id)
                # tic tags
                self.drawing.addtag_withtag(t_t_tag, tic_id)  # It _is_ a tic!
                self.drawing.addtag_withtag(t_h_tag, tic_id)  # Move with header
                self.drawing.addtag_withtag(t_r_tag, tic_id)  # Move with row
                t_c_tag = "c_"+str(col+1)  # col nbr to right of tic
                self.drawing.addtag_withtag(t_c_tag, tic_id)  # Find tic's col
            #self.rdg.drawing.itemconfigure('t_r_tag', state=tk.HIDDEN)

        def delete_bar(self, f_id):
            #print("About to delete bar %s" % f_id)
            rf_rdo = self.rdg.objects[f_id]
            #print("  rf_rdo %s" % rf_rdo)
            rf_clo = rf_rdo.a_obj  # R field's clo
            #print("  rf_clo %s" % rf_clo)
            h = rf_clo.h;  r = rf_clo.r
            
            for j in range(0, len(r.fields)):  # Find R field (has bar) in row
                tf_clo = r.fields[j]  # clo for field being tested
                #print("$$ %d $$, rf_clo %s" % (j, rf_clo))
                if (tf_clo.f_col == rf_clo.f_col and
                        tf_clo.width == rf_clo.width):
                    #print("row's field %d matches !!" % j)
                    #print("Delete bar between %s and %s" % (
                    #    r.fields[j-1].text, r.fields[j].text))
                    new_text = r.fields[j-1].text+" "+ \
                        r.fields[j].text
                    print("new_text >%s<" % new_text)
                    # Delete RH field
                    #print("RH  bar_id %s" % r.fields[j].bar_id)
                    #print("RH text_id %s" % r.fields[j].text_id)

                    old_rh_text_id = r.fields[j].text_id  # Save id for later
                    self.drawing.delete(rf_clo.r.fields[j].bar_id)
                    self.drawing.delete(rf_clo.r.fields[j].text_id)
                    #rf_clo.bar_id = rf_clo.text_id = None
                    
                    old_lf = rf_clo.r.fields[j-1]
                    #print("Old LH field: j %d f_col %d, width %d, text >%s<" % (
                    #    j-1, old_lf.f_col, old_lf.width, old_lf.text))
                    old_rf = rf_clo.r.fields[j]
                    #print("Old RH field: j %d f_col %d, width %d, text >%s<" % (
                    #    j-1, old_rf.f_col, old_rf.width, old_rf.text))
                    # Combine LH and RH fields into new New field
                    r.fields[j-1].text = new_text
                    r.fields[j-1].f_col = r.fields[j-1].f_col
                    r.fields[j-1].width += r.fields[j].width
                    new_lf = r.fields[j-1]
                    #print("new LH field: j %d f_col %d, width %d, text >%s<" % (
                    #    j-1, r.fields[j-1].f_col, r.fields[j-1].width,
                    #    r.fields[j-1].text))
                    #print("new_lf.text_id %s" % r.fields[j-1].text_id)
                    self.rdg.drawing.itemconfig(
                        r.fields[j-1].text_id, text=new_text)
                    old_lf = r.fields[j-1];  lfx0 = old_lf.x0
                    lfy0 = old_lf.y0;  lfy1 = old_lf.y1
                    old_rf = r.fields[j];  rfx1 = old_rf.x1
                    r.fields[j-1].f_cx = round((lfx0+rfx1)/2)
                    r.fields[j-1].f_cy = round((lfy0+lfy1)/2)
                    r.fields[j-1].text = new_text
                    self.rdg.drawing.coords(r.fields[j-1].text_id,
                        r.fields[j-1].f_cx, r.fields[j-1].f_cy)
                    #print("r.fields[j-1] now %s" % r.fields[j-1])

                    rf_clo.r.fields.pop(j)
                    #print("rf_clo.r.fields now %s" % rf_clo.r.fields)
                    del  self.rdg.objects[old_rf.text_id]
                    new_lf_rdo = self.rdg.objects[old_lf.text_id]
                    #print("--1: new_lf_rdo >%s<", new_lf_rdo)
                    new_lf_rdo.object = r.fields[j-1]
                    new_lf_rdo.i_text = new_text
                    #print(">>> new_lf_rdo %s" % new_lf_rdo)
                    self.rdg.objects[old_lf.text_id] = new_lf_rdo
                    break
            return

        def set_mx_txt_lines(self):
            mx_lines = 0
            for f_clo in self.fields:
                f_text = f_clo.text_id
                ttext = self.drawing.itemcget(f_clo.text_id, "text")
                t_lines = len(ttext.splitlines())
                if t_lines > mx_lines:
                    mx_lines = t_lines
            self.mx_txt_lines = mx_lines
        
        def resize_row(self, r_clo, rl_delta):
            draw_headers.row.move_tics(
                self, r_clo.h.h_nbr, r_clo.r_nbr, rl_delta)
            rc = self.drawing.coords(r_clo.row_id)  # 4 points for row's |_|
            #print("RR r_coords old =  %d,%d | %d,%d -- %d,%d, | %d,%d" % (
            #    rc[0],rc[1], rc[2],rc[3], rc[4],rc[5], rc[6],rc[7]))
            if rl_delta < 0:  # Up
                print("^^^ up")
                r_clo.y1 -= draw_headers.line_height
                r_clo.r_lines -= 1
            else: # Down
                print("v down")
                r_clo.y1 += draw_headers.line_height
                r_clo.r_lines += 1
            r_coords = [ rc[0],rc[1], rc[2],r_clo.y1,  # 4 points for row's |_|
                         rc[4],r_clo.y1, rc[6],rc[7] ]
            self.drawing.coords(r_clo.row_id, r_coords)  # Set new coords
            return r_clo  # rclo.y1 has changed!
                        
        def change_row_lines(self, r_rdo, rl_delta):
            # rl_delta = +1/-1 rows delta
            print("change_row_lines: r_rdo %s, rl_delta %s" % (r_rdo, rl_delta))
            r_clo = r_rdo.a_obj
            h = r_clo.h
            #print("hdr %d, row %d has %d lines" % (
            #    h.h_nbr, r_clo.r_nbr, r_clo.r_lines))

            if rl_delta > 0:  # Down (add a line)
                #print("rn range: %d, %d, %d" % (
                #    len(h.rows)-1, r_clo.r_nbr-1, -1))
                for rn in range(len(h.rows), r_clo.r_nbr, -1):
                    clo = h.rows[rn-1]
                    #print("-V- rn %d, y0 %d, y1 %d" % (
                    #    rn, clo.y0, clo.y1))
                    #print("??? rn %d, clo %s" % (rn, clo))
                    self.drawing.move("r_"+str(rn),  # row object's tag
                        0, draw_headers.line_height)
                    #print("=== r_nbr %d, y0 %d, y1 %d" % (
                    #    rn, clo.y0, clo.y1))
                    clo.y0 += draw_headers.line_height
                    clo.y1 += draw_headers.line_height
                    #print("--- r_nbr %d, y0 %d, y1 %d" % (
                    #    rn, clo.y0, clo.y1))
                    h.rows[rn-1] = clo
                r_clo = draw_headers.row.resize_row(self, r_clo, rl_delta)
            else:  # Up  (remove a line)
                draw_headers.row.set_mx_txt_lines(r_clo)
                #print("??? mx_txt_lines = %d" % r_clo.mx_txt_lines)
                if r_clo.r_lines == 1:
                    self.rdg.display_msg(
                        "Row can't have less than one line", "error")
                    return
                r_clo = r_rdo.a_obj
                print("r_clo >%s< rclo.r_mx_txt_lines %d, r_lines %d" % (
                    r_clo, r_clo.mx_txt_lines, r_clo.r_lines))
                if r_clo.r_lines-1 < r_clo.mx_txt_lines:
                    self.rdg.display_msg(
                        "Row contains field(s) with %d lines" %
                        r_clo.mx_txt_lines, "error")
                else:
                    r_clo = draw_headers.row.resize_row(self, r_clo, rl_delta)
                #print("rn range: %d, %d, %d" % (
                #    r_clo.r_nbr, len(h.rows), 1))
                
                    for rn in range(r_clo.r_nbr+1, len(h.rows)+1, 1):
                        clo = h.rows[rn-1]
                        #print("=^= rn %d, y0 %d, y1 %d" % (
                        #    rn, clo.y0, clo.y1))
                        self.drawing.move("r_"+str(rn),
                            0, -draw_headers.line_height)
                        clo.y0 -= draw_headers.line_height
                        clo.y1 -= draw_headers.line_height
                        #print("=*= r_nbr %d, y0 %d, y1 %d" % (
                        #    rn, clo.y0, clo.y1))
                        h.rows[rn-1] = clo

            r_rdo.a_obj = r_clo
            self.rdg.objects[r_rdo.key] = r_rdo  # Update r_rdo in objects[]

            #print("=+=+= r_clo %s (%s)" % (r_clo, type(r_clo)))
            for j in range(0, len(r_clo.fields)):  # Update this row's fields
                fj_clo = r_clo.fields[j]
                #print(">> fj_clo y0,y1 %d,%d" % (fj_clo.y0, fj_clo.y1))
                fj_clo.fj_cx, fj_clo.fj_cy = fj_clo.set_cxy(fj_clo)
                #print(">> fj_cx fj_cy %d,%d" % (fj_clo.fj_cx,fj_clo.fj_cy))
                self.rdg.drawing.coords(
                    fj_clo.text_id, fj_clo.fj_cx, fj_clo.fj_cy)
                r_clo.fields[j] = fj_clo
                if fj_clo.f_col != 0:
                    draw_headers.field.draw_bar(self, fj_clo)
                
                f_rdo = self.rdg.objects[fj_clo.text_id]
                f_rdo.a_obj = fj_clo  # Update f_rdo in objects[]
                self.rdg.objects[fj_clo.text_id] = f_rdo

        def undraw_tics(self, h_nbr, r_nbr):
            h_tag = "h_"+str(h_nbr)
            r_tag = "r_"+str(r_nbr)
            both_tags = h_tag+'&&'+r_tag  # && means AND here!
            self.rdg.drawing.itemconfigure(both_tags, state=tk.HIDDEN)

        def redraw_tics(self, h_nbr, r_nbr):
            h_tag = "h_"+str(h_nbr)
            r_tag = "r_"+str(r_nbr)
            both_tags = h_tag+'&&'+r_tag  # && means AND here!
            self.rdg.drawing.itemconfigure(both_tags, state=tk.NORMAL)

        def move_tics(self, h_nbr, r_nbr, n_lines):
            t_tag = "t_t"  # So we can tell it's a tic!
            h_tag = "h_"+str(h_nbr)
            r_tag = "r_"+str(r_nbr)
            both_tags = t_tag+'&&'+h_tag+'&&'+r_tag  # && means AND here!
            #print("move_tics: both_tags >%s<" % both_tags)
            self.rdg.drawing.move(  # tagorid, dx, dy
                both_tags, 0, n_lines*draw_headers.line_height)
            
        def var_len_row(self, r): 
            self.drawing.delete(r.row_id)
            #print("Mark row %d as variable-length row" % r.r_nbr)
            lh = round(draw_headers.line_height);  lh2 = round(lh/2)
            dls = draw_headers.row.draw_l_seg
            ht = r.h_tag;  rt = r.r_tag
            #print("vlr: ht %s, rt %s" % (ht, rt))
            dls(self, ht, rt, [r.x0,r.y0, r.x0,r.y0+lh])
            dls(self, ht, rt, [r.x0,r.y1-lh2, r.x0,r.y1,
                             r.x1,r.y1, r.x1,r.y1-lh])
            dls(self, ht, rt, [r.x1,r.y0+lh2, r.x1,r.y0])
            self.vbl_len_row = True

        def undraw(self, d_obj):  # For rdgc.on_delete_key()
            #print("UNDRAW row")
            r = d_obj.a_obj;  h = r.h
            if r.r_nbr != len(h.rows):
                self.rdg.display_msg(
                    "May only delete a header's bottom row", "warning")
            else:
                for f_obj in self.fields:
                    f_obj.undraw(f_obj)
                self.undraw_tics(h.h_nbr, r.r_nbr)
                self.rdg.drawing.itemconfigure(r.row_id, state=tk.HIDDEN)
                
        def redraw(self, d_obj):  # For rdgc.on_insert_key()
            #print("REDRAW row")
            r = d_obj.a_obj;  h = r.h
            for f_obj in self.fields:
                f_obj.undraw(f_obj)
            self.redraw_tics(h.h_nbr, r.r_nbr)
            self.rdg.drawing.itemconfigure(r.row_id, state=tk.NORMAL)
                
        def restore_object(self, r_coords, r_text,  # Restore row
                parent_id, v1, v2):  # For rdgc.on_insert_key()
            #print("ROW restore_object: r_coords %s, r_text >%s<, parent_id %s, v1 %s, v2 %s" % (r_coords, r_text, parent_id, v1, v2))
            self.type = "row"
            #self.x0, self.y0, self.x1, self.y1 = r_coords
            self.x0, self.y0 = r_coords
            self.text = r_text;  self.hdr_id = parent_id
            self.r_nbr = int(v1);  self.r_lines = int(v2)
            self.vbl_len_row = False
            #self.rdg.dump_objects("restoring row %d hdr_id %d r_lines %d" % (
            #    self.r_nbr, self.hdr_id, self.r_lines))
            self.h_obj = self.rdg.objects[self.hdr_id]
            #print("+++ row: h_obj >%s<, vbl_len_row %s" % (
            #    self.h_obj, self.vbl_len_row))
            self.h = self.h_obj.a_obj
            r = draw_headers.row(
                self.drawing, self.rdg, self.h, self.r_lines)
            print("+++ row r >%s<" % r)
            if self.r_lines < 0:
                self.r_lines = -self.r_lines;  self.vbl_len_row = True
            r.h_tag = "h_"+str(self.h.h_nbr)
            r.r_tag = "r_"+str(r.r_nbr)
            #print("RESTORE row, self.r_tag >%s<" % self.r_tag)
            if not r.row_id:
                print("restore_object row, row_id=0 !!!");  exit()
            #else:
            #    #both_tags = self.h.h_tag+'&&'+self.r_tag  # && means AND here!
            #    #self.rdg.drawing.itemconfigure(both_tags, state=tk.NORMAL)
            #    self.drawing.itemconfig(self.row_id, tag=self.r_tag)
            #    self.drawing.addtag_withtag(self.h_tag, self.r_tag)

        def mk_save_str(self, val):  # Make row's rdd file entry
            #print("$ r $ ROW mk_save_str: type(self) = %s" % type(self))
            #print(" R R  type(val) %s, val %s" % (type(val), val))
            r = val.a_obj;  d_id = val.key
            #print("$ $ $ row mk_save_str: self.h_nbr %d" % r.h.h_nbr)
            d_type = "row"
            x0,y0, x1,y1 = r.bbox()
            i_coords = [x0,y0, x1,y1];  coords = []
            for c in i_coords:
                coords.append(int(float(c)))
            n_lines = r.r_lines
            if r.vbl_len_row:
                n_lines = -r.r_lines
            #print("+ row + vbl_len_row %s, n_lines %d" % (
            #    r.vbl_len_row, n_lines))
            ds = "(%s %d) %s \"%s\" %s %s %s" % (
                "row", val.key, coords, "R", r.h.hdr_id, r.r_nbr, n_lines)
            #$print("   ds >%s<" % ds)
            return ds

        def clicked_on_tic(self, hn, rn, cn):  # Clicked on a tic (in class row)
            print("row.clicked_on_tic(%s, %s, %s)" % (hn, rn, cn))
            self.rdg.dump_objects("starting clicked_on_tic")
            self.rn = rn;  self.cn = cn
            self.h_nbr_to_fn = {}  # Map h_nbrs to fn
            for hx in range(len(draw_headers.headers)):
                h_clo = draw_headers.headers[hx]
                print("hx %d, hdr %s" % (hx, h_clo))
                h_nbr = h_clo.h_nbr
                print("   header %d, row %d" % (h_nbr, rn-1))
                #print("@$@$: h_nbr %d, hx %d" % (h_nbr, hx))
                self.h_nbr_to_fn[h_nbr] = hx
            #print("***** %s" % self.h_nbr_to_fn)
    
            dhn = self.h_nbr_to_fn[hn]
            #print("hn %s -> dhn %d" % (hn , dhn)) 
            self.h_clo = draw_headers.headers[dhn]
            self.r_clo = self.h_clo.rows[rn-1]
            #print("@#@#@ h %s, r %s" % (self.h_clo, self.r_clo))

            #print("= = = clo.fields %s" % self.r_clo.fields)
            for fn, f in enumerate(self.r_clo.fields):
                if cn >= f.f_col and cn < f.f_col+f.width:
                    c_fn = fn  # divide field c_fn, insert right half after c_fn
                    print("--- divide field %d; f_col %d, width %d" % (
                        c_fn, f.f_col, f.width))
                    lf = self.r_clo.fields[fn]  # Left half
                    lf_rdo = self.rdg.objects[lf.text_id]
                    lf_clo, rf_clo = draw_headers.field.split_field(
                        self, lf_rdo, cn)
                    ## ?? lf_rdo = self.rdg.objects[lf.text_id]
                    print("$$ clicked_on_tic(): r_clo.fields:")
                    for f in self.r_clo.fields:
                        print(" ... %s" % f)
                    #self.rdg.dump_objects("divided a field")
                    break
            #print("tic is in field %d" % c_fn)
            #print("fields now: %s" % self.r_clo.fields)
            #for f in self.r_clo.fields:
            #    print("now     ... %s" % f)

            ##f_rdo = self.rdg.objects[self.text_id]
            for r_clo in self.r_clo.fields[0:-2]:
                #print(">>> r_clo %s" % r_clo)
                #print("    r_clo.text_id = %d" % r_clo.text_id)
                f_rdo = self.rdg.objects[r_clo.text_id]
                #print(">>> f_rdo %s" % f_rdo)

            #self.rdg.dump_objects("After click_on_tic")
            ##draw_headers.wait_for_input(self, "split-field done")           

    class field:
        def __init__(self, rdg, h, r, text, f_col, width, fcolour):
            self.rdg = rdg
            self.h = h;  self.r = r;  self.text = text
            print("*&*&* field; h >%s<, h.h_nbr %d" % (h, h.h_nbr))
            if h.type != "header":
                print(">>>>>>>>>> h.type != header")
            #$print("class field: rdg %s, h %s, r %s <><><>" % (
            #$    self.rdg, self.h, self.r))
            #$print("~|~ r.fields: %s" % self.r.fields)
            self.type = "field"
            self.f_col = f_col;  self.width = width
            row_id = self.r.row_id;  self.r_nbr = self.r.r_nbr
            #$print("||||||||| self.row_id %d (%s)" % (  # << correct here
            #$    self.r.row_id, type(self.r.row_id)))  ##;  exit()
            #$print("new field: self.h %s self.r %s" % (self.h, self.r))
            #$print("   h %s" % h)
            f_h_id= self.h.hdr_id  # field's hdr_id
            h_rdo = self.rdg.objects[f_h_id]
            #$print("||||||||| h_obj %s " % h_rdo)
            #self.rdg.current_object = h_rdo  # To move field's header

            self.r_coords = r.r_coords  # Row coords
            #print("===  r_coords %s" % self.r_coords)
            rx0,ry0, rx1,ry1 = r.r_coords  ####self.r_coords
            #print(">.1 field rx1,ry1 %d,%d text %s" % (rx1,ry1, text))
            #print(">.2 field fcx,fcy %d,%d" % (self.f_cx, self.f_cy))
            ry1 = ry1 - draw_headers.tic_height  # Tics not included in field!
            self.x0 = rx0 + h.ch_width + self.f_col*h.ch_width*2
            self.x1 = self.x0 + self.width*h.ch_width*2 - 1
            self.y0 = ry0+1;  self.y1 = ry1-1  # Avoid row edges and tics
            self.x0 += 1;  self.x1 -= 1  # White edges at field  L and R edges
            # Field bbox includes x coords inside field border,
            #   y coords from top down to top of tics
            self.f_coords = [self.x0,self.y0, self.x1,self.y1]
            #print("===  f_coords %s" % self.f_coords)
            self.f_cx, self.f_cy = self.set_cxy(self)
            #print(">.3 field fcx,fcy %d,%d" % (self.f_cx, self.f_cy))
            self.bar_id = None

            #$print(">.4 class field, text >%s< f_cx,f_cy %s,%s" % (
            #$    self.f_cx, self.f_cy, text))
            centre = [self.f_cx, self.f_cy] 
            self.text_obj = self.rdg.dtc_tool.restore_object(
                centre, text, self.r.row_id,
                self.f_col, self.width)
            # restores the field's text, __and puts it into objects{}__
            #print(">>> 64 field.text_obj %s" % self.text_obj)
            #self.rdg.dump_objects(">>> text for field created <<<")
            self.text_id = self.text_obj.key
            #  Entry for field text allows b3 to edit it
            #print("@ @ @ self.text_id %s" % self.text_id)
            #print("   text >%s< cx,cy %d,%d" % (
            #    self.text_id, self.f_cx,self.f_cy))
            if fcolour:
                rect_id = self.r.drawing.create_rectangle(  # text background
                    self.f_coords, fill=fcolour, outline=fcolour)
                self.rdg.drawing.tag_lower(rect_id,self.text_id)
                
            self.h.drawing.itemconfig(self.text_id, tag=self.h.h_tag)
            self.h.drawing.addtag_withtag(self.r.r_tag, self.text_id)
            c_tag = "c_"+str(self.f_col)
            self.h.drawing.addtag_withtag(c_tag, self.text_id)
            tags = self.h.drawing.gettags(self.text_id)
            #print("field item's tags: ", end="");  print(tags)  # # OK here

            # Change the text_obj to a field_obj !
            #          field's object (f_clo) _is_ a field object
            #                                         V
            #print(": : : field self type %s" % type(self))
            self.f_rdo = self.rdg.object(self.text_id, self, "field",
                self.r.bbox(), text, self.r.row_id,
                self.f_col, self.width)
            self.rdg.objects[self.text_id] = self.f_rdo
            #self.rdg.dump_objects("!! text %d changed to field" % self.text_id)
            
            self.r.fields.append(self)
            print("$$$ text >%s< (%s)" % (text, type(text)))
            txt_lines = self.text.splitlines()
            n_txt_lines = len(txt_lines)
            if n_txt_lines > self.r.mx_txt_lines:
                 self.r.mx_txt_lines = n_txt_lines
            
            #print("-->> r.row_id %d, r_nbr %d, fields %s" % (
            #    (self.r.row_id, self.r.r_nbr, self.r.fields)))
            #print("--:: field obj %s\n\n" % self.f_rdo)
            self.rdg.objects[self.text_id] = self.f_rdo  # Overwrite the text
            #self.rdg.dump_objects("field's text rdo overwritten")
            #print("field_cls: .h = %s" % self.h)
            #print("           .r = %s" % self.r)
            #draw_headers.wait_for_input(self, "Should now have field 34)")

            if self.f_col != 0:  # Draw bar at left
                self.draw_bar(self.f_rdo.a_obj)
                
        def draw_bar(self, f_clo):
            # bar from r.y0 down towards r.y1, to right of f_clo.f_col
            h = f_clo.h;  r = f_clo.r
            rh = r.row_height(r.r_lines)-draw_headers.tic_height
            self.bar_x = r.x0 + h.ch_width + f_clo.f_col*h.ch_width*2
            self.b_coords = [self.bar_x, r.y0, self.bar_x, r.y0+rh]
            bw = h.tic_width-1
            if not f_clo.bar_id:
                f_clo.bar_id = f_clo.r.drawing.create_line(
                    self.b_coords, width=bw)
                self.rdg.drawing.addtag_withtag(h.h_tag, f_clo.bar_id)
                self.rdg.drawing.addtag_withtag(r.r_tag, f_clo.bar_id)
                f_tag = "f_"+str(f_clo.text_id)  # Field's text
                self.rdg.drawing.addtag_withtag(f_tag, f_clo.bar_id)
            else:
                self.rdg.drawing.coords(f_clo.bar_id,
                    self.bar_x, r.y0, self.bar_x, r.y1)
            return f_clo

        def __str__(self):
            return "field str: h %s, r %s, text_id %d, text %s, f_col %s, width %s, fcolour %s" % (
                self.h, self,r, self.textr_id, self,text, self,f_col, self,width, self,fcolour)
       
        def set_cxy(self, f_clo):  # Centre coords for field text
            #print("=== set_cxy: f_clo %s (%s), self.y0 %d, self.y1 %d" % (
            #    f_clo, type(f_clo), self.y0, self.y1))
            #x0,y0, x1,y1 = r.r_coords
            r = f_clo.r;  h = f_clo.h
            txt_top = r.y0 + r.h.r_tgap
            # self.r_lines lines of text
            txt_bot = r.y1 - draw_headers.tic_height - self.h.r_bgap
            txt_bot = r.y0 + r.r_lines*draw_headers.line_height
            f_cy = round(txt_top+txt_bot)/2
            #f_cy = round(f_clo.y0+f_clo.y1)/2
            f_cx = round((f_clo.x0+f_clo.x1)/2) + self.h.f_lgap
            #print("[[ set_cxy: x0 %d, %d, x1 %d, text >%s<" % (
            #    f_clo.x0, f_cx, f_clo.x1, self.text))
            #print("{{ set_cxy: y0 %d, %d, y1 %d, text >%s<" % (
            #    f_clo.y0, f_cy, f_clo.y1, self.text))
            #self.r.drawing.create_text(  # Show where centre of text will be
            #    (self.f_cx,self.f_cy), text="@", fill="red")
            return f_cx, f_cy

        def find_field(self, fs_clo, tf_f_col, tf_width):
            tf_x = -1  # So we can check the target field was found!
            for fx,ft_clo in enumerate(fs_clo.r.fields):
                #print("**** ft_clo %s" % ft_clo)
                if ft_clo.f_col == tf_f_col and \
                       ft_clo.width == tf_width:  # Target field  8, 24  OK
                    tf_obj = ft_clo.text_obj
                    #print("<><><> tf_obj >%s<" % tf_obj)  # Keep this field
                    return fx
            if tf_x < 0:
                print("Couldn't find field in row.fields");  exit()

        def shrink_field(self, fs_rdo, n_width):
            ##fs_obj = self.rdg.objects[fs_rdo.key]
            sf_clo = fs_rdo.a_obj
            #print("@@@ shrink_field: sf_clo %s, sf_clo.width %d, n_width %d" % (
            #    sf_clo, sf_clo.width, n_width))
            sf_clo.x1 = sf_clo.x0 + n_width*sf_clo.h.ch_width*2 - 1
            sf_clo.f_cx, sf_clo.f_cy = sf_clo.set_cxy(sf_clo)
            self.rdg.drawing.coords(sf_clo.text_id, sf_clo.f_cx, sf_clo.f_cy)
            sf_clo.width = n_width
            fs_rdo.a_obj = sf_clo
            self.rdg.objects[fs_rdo.key] = fs_rdo  # Update field object

        def fmt_f_clo(self, l_r, f_clo):
            return "field %s, f_col %d, width %d" % (
                l_r, f_clo.f_col, f_clo.width)
            
        def change_fields_display(self, lf_clo, rf_clo):
            #print("++--++ %s | %s" % (
            #    draw_headers.field.fmt_f_clo(self, "L", lf_clo),
            #    draw_headers.field.fmt_f_clo(self, "R", rf_clo)))
            h = lf_clo.h;  r = lf_clo.r
            rx0,ry0, rx1,ry1 = r.r_coords  # Row coords
            #print("row coords %d,%d, %d,%d" % (rx0,ry0, rx1,ry1))
            
            lf_clo.x0 = rx0 + h.ch_width + lf_clo.f_col*h.ch_width*2
            lf_clo.x1 = lf_clo.x0 + lf_clo.width*h.ch_width*2 - 1
            lf_clo.y0 = ry0+1;  lf_clo.y1 = ry1-1  # Avoid row edges and tics
            lf_clo.x0 += 1;  lf_clo.x1 -= 1  # White edges at field  L,R edges

            rf_clo.x0 = rx0 + h.ch_width + rf_clo.f_col*h.ch_width*2
            rf_clo.x1 = rf_clo.x0 + rf_clo.width*h.ch_width*2 - 1
            rf_clo.y0 = ry0+1;  rf_clo.y1 = ry1-1  # Avoid row edges and tics
            rf_clo.x0 += 1;  rf_clo.x1 -= 1  # White edges at field  L,R edges

            lf_clo.f_cx, lf_clo.f_cy = lf_clo.set_cxy(lf_clo)
            rf_clo.f_cx, rf_clo.f_cy = rf_clo.set_cxy(rf_clo)

            #print("== Left: x0 %d, f_cx %d, x1 %d" % (
            #    lf_clo.x0, lf_clo.f_cx, lf_clo.x1))
            #print("== Rght: x0 %d, f_cx %d, x1 %d" % (
            #    rf_clo.x0, rf_clo.f_cx, rf_clo.x1))
                
            self.rdg.drawing.coords(lf_clo.text_id, lf_clo.f_cx, lf_clo.f_cy)
            self.rdg.drawing.coords(rf_clo.text_id, rf_clo.f_cx, rf_clo.f_cy)
            if rf_clo.f_col != 0:
                rf_clo = draw_headers.field.draw_bar(self, rf_clo)

            lf_rdo = self.rdg.objects[lf_clo.text_id]  # Update lf_rdo
            lf_rdo.a_obj = lf_clo
            self.rdg.objects[lf_rdo.key] = lf_rdo
            rf_rdo = self.rdg.objects[rf_clo.text_id]  # Update rf_rdo
            rf_rdo.a_obj = rf_clo
            self.rdg.objects[rf_rdo.key] = rf_rdo
            return lf_clo, rf_clo
            
        def move_bar(self, f_obj, fx_delta):
            #print("move_bar: fx_delta %d, f_obj %s" % (fx_delta, f_obj))
            f_clo = f_obj.a_obj;  h = f_clo.h
            tf_x = draw_headers.field.find_field(
                self, f_clo, f_clo.f_col, f_clo.width)
            r = f_clo.r
            #print("field's row f_col,width: %d, %d | %d, %d" % (
            #    r.fields[tf_x-1].f_col, r.fields[tf_x-1].width,
            #    r.fields[tf_x].f_col, r.fields[tf_x].width))
            lf_clo = r.fields[tf_x-1]
            rf_clo = r.fields[tf_x]
            #print("f_clo  >%s<" % f_clo)
            #print("rf_clo >%s<" % rf_clo)
            print("lf_clo ==  %s\nrf_clo == %s" % (lf_clo,rf_clo))
            #rint("?=?=? rf_rdo >%s< fx_delta %s" % (rf_rdo, fx_delta))
            if fx_delta > 0:  # Move bar right
                if rf_clo.width == 1:
                    self.rdg.display_msg("Right field too narrow", "warning")
                else:
                    lf_clo.width += 1;  rf_clo.f_col += 1;  rf_clo.width -= 1
                    print("--> move bar right, rf_clo.width %d" % rf_clo.width)
                    lf_clo, rf_clo = draw_headers.field.change_fields_display(
                        self, lf_clo, rf_clo)
            else:  # Move bar left  <<<<<<<<<<<
                if lf_clo.width == 1:
                    self.rdg.display_msg("Left field too narrow", "warning")
                else:
                    lf_clo.width -= 1;  rf_clo.f_col -= 1;  rf_clo.width += 1
                    print("--> move bar left, rf_clo.width %d" % rf_clo.width)
                    lf_clo, rf_clo = draw_headers.field.change_fields_display(
                        self, lf_clo, rf_clo)
            r.fields[tf_x-1] = lf_clo;  r.fields[tf_x] = rf_clo
            
        def split_field(self, fs_rdo, at_col):  # fs = "field to split"
            fs_key = fs_rdo.key;  fs_clo = fs_rdo.a_obj
            print("_+_+_ fs_clo >%s< at_col %d" % (fs_clo, at_col))
            print("!!! fs_rdo text_id >%s< %s" % (fs_clo.text_id, fs_clo.text))
            print("split field %d at col %d" % (fs_key, at_col))
            print("  fs_clo: fs_col %d, width %d, row_id %d" % (  # fc 7, w 24
                fs_clo.f_col, fs_clo.width, fs_clo.r.row_id))  # << added r.
            print("@ ! @ fs_clo.f_rdo %s" % fs_clo.f_rdo) # correct here
            print("fs_clo.f_rdo %s" % fs_clo.f_rdo)
            print("  key %s, object %s" % (fs_clo.f_rdo, fs_clo.f_rdo.a_obj)) 

            #print("row fields: %s" % fs_clo.r.fields)
            tf_f_col = fs_clo.f_col;  tf_width = fs_clo.width
            #print(">> lf f_col %d, width %d" % (tf_f_col, tf_width)) # 7, 24
            tf_x = draw_headers.field.find_field(
                self, fs_clo, tf_f_col, tf_width)
            ft_clo = fs_clo.r.fields[tf_x]
            tf_obj = ft_clo.text_obj
            #ft_clo.undraw(tf_obj)  # Keep target field's text for L
            #   Make new text for R
            #fs_clo.r.fields.pop(fx);  tf_x = fx
            #print("field to be split is %s" % ft_clo)  # OK
            #print("field row now %s" % fs_clo.r.fields)
            
            #print("Target fld split: tf_f_col %d, tf_width %d, at col %d" % (
            #    tf_f_col, tf_width, at_col+1))  # 8, 24, col 20 << Correct
            new_lf_f_col = tf_f_col
            new_lf_width = at_col - new_lf_f_col       #  8, 12 << Correct
            #@@ was at_col+1 !! ??
            print("new_lf f_col %d, width %d" % (new_lf_f_col, new_lf_width))
            
            #lf_clo = draw_headers.field(self.rdg, fs_clo.h, fs_clo.r, "L",
            #            new_lf_f_col, new_lf_width, "lightblue")
            draw_headers.field.shrink_field(self, fs_rdo, new_lf_width)
            lf_clo = fs_rdo.a_obj
            lf_key = lf_clo.text_id
            lf_obj = self.rdg.objects[lf_key]
            lf_obj.a_obj.parent_id = lf_clo.r.row_id
            lf_obj.a_obj.v1 = new_lf_f_col
            self.rdg.objects[lf_key] = lf_obj
            #draw_headers.wait_for_input(self, "L field drawn")  #<< OK to here
            
            new_rf_f_col = new_lf_f_col+new_lf_width
            new_rf_width = tf_width-new_lf_width  #XXXXX
            #print(">> rf f_col %d, width %d" % (new_rf_f_col, new_rf_width))
            #rf_clo = draw_headers.field(self.rdg, fs_clo.h, fs_clo.r, "R",
            #            new_rf_f_col, new_rf_width, "khaki")
            rf_clo = draw_headers.field(self.rdg, fs_clo.h, fs_clo.r, "X",
                         new_rf_f_col, new_rf_width, None)
            #print("! ~ @ rf_clo: >%s<" % rf_clo)

            rf_key = rf_clo.text_id
            rf_obj = self.rdg.objects[rf_key]
            rf_obj.a_obj.parent_id = rf_clo.r.row_id
            rf_obj.a_obj.v1 = new_rf_f_col
            #self.rdg.objects[rf_key] = rf_obj
            ##self.undraw(rf_obj)
            #draw_headers.wait_for_input(self, "R field drawn, rf_key %d" % \
            #                            rf_key)  #<< OK to here
            """
            f_clo = fs_rdo.a_obj
            hn = f_clo.h.h_nbr;  rn = f_clo.r_nbr
            cn = f_clo.f_col+f_clo.width-1
            print(">> split_field: hn %d, rn %d, cn %d" % (hn,rn,cn))
            
            draw_headers.bar(self.drawing, self.rdg, fs_rdo, hn, rn, cn)
            """
            #self.rdg.dump_objects("@ @ @ split_field")
            return lf_clo, rf_clo
            
        def undraw(self, f_rdo):
            #print("FIELD undraw, f_rdo %s, text_id %d" % (
            #    f_rdo, f_rdo.key))
            self.rdg.drawing.itemconfigure(
                f_rdo.a_obj.text_id, state=tk.HIDDEN)
            if self.f_col != 0:  # Undraw bar at left
                self.rdg.drawing.itemconfigure(
                    self.bar_id, state=tk.HIDDEN)

        def redraw(self, f_rdo):
            #print("FIELD redraw, f_rdo %s" % f_rdo)
            self.rdg.drawing.itemconfigure(
                f_rdo.a_obj.text_id, state=tk.NORMAL)
            if self.f_col != 0:  # Redraw bar at left
                self.rdg.drawing.itemconfigure(
                    self.bar_id, state=tk.HIDDEN)

        def __str__(self):
            return "field: self.h %s, self.r %s, self.text %s" % (
                self.h, self.r, self.text)

        def bbox(self):  # Get field's current coords
            return self.x0, self.y0, self.x1, self.y1

        def mk_save_str(self, val):  # Make field's rdd file entry
            #$print("FIELD mk_save_str: val %s, val.i_coords %s" % (
            #$        val, val.i_coords))
            f_clo = val.a_obj;  row = f_clo.r;  hdr = row.h
            #$print("=-= row >%s<, hdr >%s<" % (row, hdr))
            #$print("hdr.hdr_id >%s<" % hdr.hdr_id)
            h_rdo = self.rdg.objects[hdr.hdr_id]
            #$print("--> h_rdo >%s<" % h_rdo)

            if row.r_nbr != 1 or h_rdo.v2 == 0:
                # Not a no_col_nbrs header, normal field
                f_clo = val.a_obj;  d_id = val.key
                fcx0,fcy0, fcx1,fcy1 = f_clo.bbox()
                i_coords = f_clo.bbox();  coords = []
                for c in i_coords:
                    coords.append(int(float(c)))
                sit = str(val.i_text)  # rdg.edit_esc_key updates i_text
                sit = sit.replace('"', '\\"')  # Escape \" chars
                sit = sit.replace("\n", "\\n")   # Escape \n chars
                return "(%s %d) %s \"%s\" %s %s %s" % ("field", val.key, coords,
                    sit, f_clo.r.row_id, f_clo.f_col, f_clo.width)
            else:
                return "no_col_nbrs"
            
        def restore_object(self, r_coords, r_text, 
                parent_id, v1, v2):  # For rdgc.on_insert_key()
            #print("RESTORE field")  # field needs h and r <<<<<<<
            ###  Called from rdglob.restore_saved_object()
            #print("field ro: r_crds %s, r_txt %s, prnt_id %s, v1 %s, v2 %s" % (
            #    r_coords, r_text, parent_id, v1, v2))
            #print("About to restore field obj, h %s, r %s" % (
            #    self.h, self.r))
            #self.rdg.dump_objects("RESTORE field")
            #print("?+?+? field restore_object: self = %s" % self)
            r_rdo = self.rdg.objects[parent_id]  ### #  row 2
            #  <Key 35, Object 35, Type text, I_coords (400, 134),
            #                      i_text 0 ... 0 1, 2  0  32
            #                               row_id = 2
            #print("*** r_rdo = %s" % r_rdo)  # OK
            r_clo = r_rdo.a_obj   # row object            
            #print("*** r_clo %s" % r_clo)
            row_id = parent_id  # field's parent_id            
            r_h_clo = r_clo.h
            #print("*** row's h %s" % r_h_clo)
            f_col = int(v1);  width = int(v2)
            f = draw_headers.field(self.rdg, r_h_clo, r_clo,
                r_text, f_col, width, None)
            #print("R F R F: f_cx %s, f_cy %s" % (f.f_cx, f.f_cy))
            #print("    f.text_id %s" % f.text_id)
            #self.rdg.dump_objects("RESTORE field")
            #print("field f: %s" % f)
            #print("- - - f.text_id %d" % f.text_id)
            #   Entry for field text allows b3 to edit it
            
    def find_closest_rd_obj(self, rdo_type, mx,my):  # rd = rfc_draw
        h_dist = 999999  # distance from centre of header
        fo_type = rdo_type;  o_key = None
        if rdo_type == "text":  # tk item
            fo_type = "field"
        #print("find_closest_rd_obj: fo_type %s" % fo_type)
        for j,key in enumerate(self.rdg.objects):
            obj = self.rdg.objects[key]
            #print("=-= key %s, obj %s, o_key %d" % (key, obj, obj.key))
            if obj.o_type == fo_type:
                #print("=a= key %s,  %s" % (key, obj))
                h_obj = obj;  t_obj = obj.a_obj
                dcx = mx - (t_obj.x0+t_obj.x1)/2
                dcy = my - (t_obj.y0+t_obj.y1)/2
                dist = round(math.sqrt(dcx**2 + dcy**2))
                #print("$  obj %s" % obj)
                #print("@@ type %s, dist %d, key %d" % (
                #    obj.o_type, dist, obj.key))
                if dist < h_dist:
                    h_dist = dist;  h_obj = obj
                    #print("=b= picked key %d, obj.key %d, dist %d" % (
                    #    key, obj.key, dist))
        #print("closest %s obj (h_dist %d) is %s" % (
        #    fo_type, h_dist, h_obj))
        self.rdg.current_object = h_obj
        return h_obj, h_dist
    
    def dh_closest(self, mx,my):
        item = self.drawing.find_closest(mx,my)  # id of closest tk object
        if len(item) == 0:  # Empty tuple
            return None, None
        item_id = item[0]
        #print("dh_closest: item_id %d" % item_id)
        obj = None
        if item_id in self.rdg.objects:
            obj = self.rdg.objects[item_id]
            ##print("  -> -> obj %s" % obj)
        return item_id, obj

    def set_event_handlers(self): 
        # Click b1 to make an object
        self.drawing.bind_class('Canvas','<Button-1>', self.dg_b1_click)
        self.drawing.bind_class('Canvas','<Double-1>',self.dg_b1_double)
        self.drawing.bind_class('Canvas','<Button1-Motion>', self.dg_b1_motion)
        self.drawing.bind_class('Canvas','<ButtonRelease-1>',self.dg_b1_release)

        self.root.bind('<KeyPress-plus>',self.on_key_press_repeat)  # +
        self.root.bind('<KeyPress-minus>',self.on_key_press_repeat) # -
        
        self.root.bind('<KeyPress-a>',self.on_key_press_repeat) #
        #print("draw_headers, handlers set, new_drawing %s <<<<" % \
        #      self.rdg.new_drawing)

    def restore_object(self, obj_type,  # For read_from_rdd()
            obj_id, o_coords, o_text, parent_id, v1, v2):
        #print("--RO-- starting restore_object pid %d, type %s, v1 %d, v2 %d" % (
        #      parent_id, obj_type, v1, v2))
        #@@ self.f_font = self.rdg.f_font
        #print("==>> restore %s, o_coords >%s<" % (obj_type, o_coords))
        if len(o_coords) != 2:  # Top-left corner of **new** header
            self.x0, self.y0, self.x1, self.y1 = o_coords          
        else:
            self.x0, self.y0 = o_coords           
            self.x1 = self.x0;  self.y1 = self.y0

        #self.rdg.dump_objects("restoring %s" % obj_type)
        #draw_headers.wait_for_input(self, "[wfi] restoring a %s" % obj_type)
        if obj_type == "header":
            h = self.header(self.drawing, self.root, self.rdg,
                            v1, o_coords, v2)  # v1=h_nbr, v2=1 -> no_col_nbrs
            #print("restore_object, v1 %s (%s), h %s" % (
            #    v1, type(v1), h))
            h.h_nbr = int(v1)
            #print("... restored header %s" % h)
            #self.rdg.n_headers = max(v1, self.rdg.n_headers)
            draw_headers.headers.append(self)
            #self.rdg.dump_objects("restore header")
        elif obj_type == "row":
            #self.rdg.dump_objects("about to restore row")
            #print(" - - - row's parent_id = %d" % parent_id)
            h_obj = self.rdg.objects[parent_id]  # Row's header object < OK
            #print(" = = = row's h_obj = %s" % h_obj)
            r_nbr = h_obj.v1
            #print("[r0] row key %d, h_obj %s, r_nbr %d" % (
            #    parent_id, h_obj, r_nbr))  ## OK
            r_hdr_id = h_obj.parent_id
            self.r = draw_headers.row(
                self.drawing, self.rdg, h_obj.a_obj, v2)  # n_lines
            #print("[r1] self.r >%s<" % self.r)
            
            rh = self.r.h
            #print("[r1] rh >%s<" % rh)
            #print("... restored row >%s<, r_lines %d" % (
            #    self.r, self.r.r_lines))
        elif obj_type == "field":
            #print("[[ field: parent_id %d, v1 %d, v2 %d" % (
            #    parent_id, v1, v2))
            r_obj = self.rdg.a_objects[parent_id]  # Field's row object
            #print("<<r_obj>> h_obj %s" % r_obj)
            #self.rdg.dump_objects("restoring field 34 <<<")
            h_obj = self.rdg.objects[r_obj.parent_id]  # Row's header object
            #print("<<< h_obj %s" % h_obj)
            f = draw_headers.field(self.rdg, h_obj.a_obj, r_obj.a_obj,
                o_text, v1, v2, None)
            print("=== f >%s<" % f)
    
    def mk_field_str(self, f_str, f_width):  # Add L&R blanks to f_str
        return f_str
        s = f_str
        if len(f_str) < f_width*2:
            s = f_str[0:f_width*2]
        offset = round((f_width*2-len(s))/2)
        return " "*offset + s + " "*offset

    def near_row(self, mx,my, hn,rn):
        print("near_row(): hn %d, rn %d" % (hn,rn))
        print("headers.headers=>%s<" % draw_headers.headers)
        h = draw_headers.headers[hn-1]  # headers[0] is header 1
        r = h.rows[rn-1]
        r_rdo = self.rdg.objects[r.row_id]
        print("near_row hm %d, rn %d, r_obj %s" % (hn,rn, r_rdo))       
        self.rdg.region = self.rdg.where(r_rdo.a_obj, mx,my)
        region = self.rdg.pos[self.rdg.region]
        print("12345 near_row: hn %d, rn %d, region %s" % (hn, rn, region))

        if my > r.y1 and my < r.y1+2*draw_headers.line_height:
            print("Clicked near row %d bottom" % r.r_nbr)
            new_r = draw_headers.row(  # Updates rh.rows !!!
                self.drawing, self.rdg, h, 1)
            print("   len(rows) now %d" % len(h.rows))
            draw_headers.field(
                self.rdg, h, new_r, "-|-", 0, 32, None)
        else:
            h_nbr = draw_headers.header.new_header_nbr(self)
            h_coords = [mx,my]  ##, mx+2,my+2]
            #print(" @ @  self.drawing %s, self.root %s, self.rdg %s" % (
            #    self.drawing, self.root, self.rdg))
            #print("b1 @ @ h_nbr %s, h_coords %s" % (h_nbr, h_coords))
            h = self.header(self.drawing, self.root, self.rdg,
                            h_nbr, h_coords, 0)  # Sets current_object
            #print("b1 + + h >%s<" % h)
            self.rdg.region = self.rdg.new
            self.rdg.dump_objects(">>> New header created")

    def on_key_press_repeat(self, event):
       self.has_prev_key_press = True
       self.drawing.after(150, self.on_key_press, event)
       #print("on_key_press_repeat >%s<" % repr(event.char))
    
    # IMPORTANT: b1_click sets self.rdg.current_object (which includes it's key)
    #   b1_motion and b1_release all work on rdg.current_object

    def on_key_press(self, event):
        self.has_prev_key_press = False
        #key = event.char  # '+' or '-'
        #draw_headers.row.change_row_lines(self, key)
                
    def dg_b1_click(self, event):
        self.drawing.after(250, self.dg_b1_action, event)
        # Delay to allow for double-click

    def dg_b1_double(self, event):
        self.double_click_flag = True

    def dg_b1_action(self, event):  # B1 (left button) to select an object
        mx, my = (event.x, event.y)  # Mouse position
        if self.double_click_flag:
            print('b1_double click event <<<')
            self.double_click_flag = False

            # b1_double processing ...
            self.rdg.last_mx = mx;  self.rdg.last_my = my  # Last mouse position
            item_id, obj = self.dh_closest(mx,my)  # Closest tk object
            print("@@@ obj %s (%s)" % (obj, type(obj)))
            item_type = self.drawing.type(item_id)  # To get tk item id's
            #item_coords = self.drawing.bbox(item_id)  # tuple
            if item_type == "line":
                o_tags = self.drawing.gettags(item_id)
                its_a_tic = its_a_bar = its_a_row = False
                for t in o_tags:
                    if t == "t_t":
                        its_a_tic = True
                    elif t[0:2] == "f_":
                        f_id = int(t[2:])
                        its_a_bar = True
                    elif t[0:2] == "r_":
                        f_id = int(t[2:])
                        its_a_row = True
                if its_a_bar:  # It's a bar, delete it
                    print("B1_DOUBLE: It's a bar, o_tags %s, item_id %d <<<" % (
                        o_tags, item_id))
                    draw_headers.row.delete_bar(self, f_id)
            elif obj.o_type == "field":
                print("$#$#$ field obj >%s<" % obj)
                f_clo = obj.a_obj
                print("b1_double field: h %d, r %d text %s" % (
                    f_clo.h.h_nbr, f_clo.r.r_nbr, f_clo.text))
                if f_clo.h.h_nbr == 1 and f_clo.r.r_nbr == 1:
                    print("f_clo >%s<" % f_clo);
                    fh = f_clo.h;  fr = f_clo.r
                    print("@#@#@ f_clo.h >%s<" % f_clo.h)
                    h_rdo = self.rdg.objects[fh.hdr_id]  # Field's header object
                    h_rdo.v2 = 1  # <-- no_col_nbrs marker
                    print("@$@$$ h_rdo %s" % h_rdo)
                    self.rdg.objects[fh.hdr_id] = h_rdo  # Update h_rdo object
                    print("      h_rdo >%s<" % h_rdo)
                    if f_clo.r.r_nbr == 1:
                        del self.rdg.objects[obj.key]  # Delete field object
                        self.rdg.dump_objects("@@@ b1_double on col_nbrs, delete them @@@")
                    ##h_rdo.a_obj = f_clo
                    print("+++ f_clo >%s<, h_rdo >%s<" % (f_clo, h_rdo))
                    print("--- h_rdo >%s<" % h_rdo)  # h_rdo is a field obj
                    self.rdg.objects[h_rdo.key] = h_rdo
                    print("fh  >%s<\nh_rdo >%s<" % (fh, h_rdo))
                    self.rdg.drawing.itemconfigure(
                        fh.hdr_id, state=tk.HIDDEN)  # hdr top (white) line
                    self.rdg.drawing.itemconfigure(
                        f_clo.text_id, state=tk.HIDDEN)  # col_nbrs (text) field
                        # field (col_nbrs) object deleted above
                    print("*** field's object deleted")
                    #$print("fr >%s<" % fr)
                    
        else:  # (single) b1_action ...
            print('b1 single click event <<<')
            mx, my = (event.x, event.y)  # Mouse position
            self.rdg.last_mx = mx;  self.rdg.last_my = my  # Last mouse position
            self.x0 = mx;  self.y0 = my
            print("# # # dg_b1_click: mode %s, %d,%d, %d objects, %s, %s" % (
                self.rdg.last_mode, mx, my, len(self.rdg.objects), 
                   event.widget, event.type))
            print("-0-0-0-0-")
            print("@@b1 current_object >%s<" % self.rdg.current_object)#? None

            item_id, obj = self.dh_closest(mx,my)  # Closest tk object
            print("\nb1_action: mx,my %d,%d  item_id %s" % (mx,my, item_id))
            print("   obj %s (%s)" % (obj, type(obj)))
            if not item_id:  # Empty tuple, nothing drawn yet
                print("** Nothing drawn yet **")
                print("I I I startup self.rdg %s" % self.rdg)

                h_nbr = draw_headers.header.new_header_nbr(self)  # First header is hdr_1
                h_coords = [mx,my]  ##, mx+2,my+2]
                #print(" @ @  self.drawing %s, self.root %s, self.rdg %s" % (
                #    self.drawing, self.root, self.rdg))
                print("@ @ @ h_nbr %s, h_coords %s" % (h_nbr, h_coords))
                print("b1: nothing drawn, add header")
                h_clo = draw_headers.header(  # Sets current_object
                    self.drawing, self.root, self.rdg, h_nbr, h_coords, 0)
                #                               v2 0 --> draw col_nbrs  |
                print("h_clo >%s<" % h_clo)
                ##self.hr = draw_headers.row(
                ##    self.drawing, self.rdg, h_clo, 2)  # lines
                ##    # Draw row 1 (header's top row), just tics and col nbrs
                ##draw_headers.header.draw_col_nbrs(self, h_clo, self.hr)
                #?print("<><> header: h %s, rdg.new_drawing %s" % h_clo)
                print("<><> header: h %s" % h_clo)
                self.rdg.region = self.rdg.far
                # header coords start with b1_click's self.x0, self.y0,
                #   to draw a header, save it in self.rdg.objects,
                #   and make it self.rdg.current_object
                #r_clo = draw_headers.row(self.drawing, self.rdg, h_clo,  2)
                self.rdg.dump_objects("Header drawn!")  #? OK                
            else:
                print("b1_action: item_id %d" % item_id)
                item_type = self.drawing.type(item_id)  # To get tk item id's
                item_coords = self.drawing.bbox(item_id)  # tuple
                # Display h, r and c (but not layer) tag
                o_tags = self.drawing.gettags(item_id)
                its_a_tic = False
                if o_tags:
                    tags = ""  # Display the item's tags
                    for t in o_tags:
                        if t[0] != "l":  # layer n
                            tags += ", " + t.replace("'","")
                        if t == "t_t":
                             its_a_tic = True
                if obj:
                    d_type = obj.o_type
                else:
                    d_type = "["+item_type+"]"
                msg = "%d,%d   %s   %s" % (mx,my, d_type, tags[2:])
                #print(">>> b1_action: msg >%s<" % msg)
                self.rdg.display_msg(msg, "normal")
                #print(">>>< %s <<<" % msg)
                    # o_types found:  (All but tic have x0,y0,x1,y1)
                    #   header h_1         = top line of header
                    #   row h_1, r_1       = row's |_|
                    #   field h_1          = field     
                    #   tic h_1, r_1, c_13 = [line]   
                # ??? displayed >551,189   [line]   h_1, r_2, c_23<    
                done = False

                #print("<> <> crl_coords %s" % draw_headers.crl_coords)
                if d_type == "[line]":  # Is it a tic?
                    #print("$ $ $ o_tags",end="");  print(o_tags)
                    l_coords = self.drawing.coords(item_id)
                    #print("len(l_coords) = %d" % len(l_coords))
                    f_id = hn = rn = cn = None
                    for t in o_tags:
                        if "c_" in t:
                            cn = int(t[2:])
                        if "r_" in t:
                            rn = int(t[2:])
                        if "h_" in t:
                            hn = int(t[2:])
                        if "f_" in t:
                            f_id = int(t[2:])
                    item_type = self.drawing.type(item_id)  # To get tk item id'
                    print("??? item_type %s" % item_type)
                    
                    if its_a_tic:
                        self.rdg.drawing.itemconfigure(item_id, fill="red")
                        print("clicked on tic: h %s,r %s,c %s" % (hn, rn, cn))
                        draw_headers.row.clicked_on_tic(self, hn, rn, cn)
                        done = True
                    elif f_id:  # It's a bar (i.e. field)
                        print("It's a bar, f_id %d <><>" % f_id)
                        f_rdo = self.rdg.objects[item_id-1]
                        #print("f_rdo = %s" %f_rdo)
                        self.rdg.current_object = f_rdo  # <<< rf_clo 
                        draw_headers.hdr_mode = "move_bar"
                        self.root.config(cursor="sb_h_double_arrow")  # <=>
                        draw_headers.crl_coords = [mx,my]
                        #print("-1- crl_coords and mode move_bar set")
                        done = True
                    elif rn and hn:  # Line, but not tic or bar
                        #print("=== clicked near hn %d, rn %d" % (hn,rn))
                        self.near_row(mx,my, hn,rn)                        
                        
                elif d_type == "field":  # In any row to move hdr + all rows
                    self.rdg.region = self.rdg.where(obj.a_obj, mx,my)
                    region = self.rdg.pos[self.rdg.region]
                    #print("clicked near field, region %s" % region)
                    f_o = obj.a_obj
                    fh = f_o.h;  fr = f_o.r  # field's h, r
                    #print(". , . header fh %s, fr %s, r.r_nbr %d" % (
                    #    fh, fr, fr.r_nbr))
                    h_obj = self.rdg.objects[fh.hdr_id]
                    #?print("field's h_obj %s, region %s" % (h_obj, region))
                    #?if fr.r_nbr == 1:  # b1_click: field in row 1
                    self.rdg.current_object = h_obj  ## Can now move h_obj
                    done = True

                elif d_type == "row":  # Below bottom row to add another row
                    #print("d_type == ROW: mx,my %d,%d, region %s" % (
                    #    mx,my, self.rdg.pos[self.rdg.region]))
                    #print("**** obj >%s<" % obj)
                    self.rdg.region = self.rdg.where(obj.a_obj, mx,my)
                    region = self.rdg.pos[self.rdg.region]
                    r = obj.a_obj;  rh = r.h
                    r_msg = ">>> row %d, region %s <<<" % (r.r_nbr, region)
                    ##self.rdg.display_msg(r_msg, "normal")
                    #print("clicked near row %d, region %s, len(rh.rows) %d" % (
                    #    r.r_nbr, region, len(rh.rows)))
                    #print("   my %d, r.y1 %d" % (my, r.y1))

                    if self.rdg.region == self.rdg.far:
                        print("??? region far, r_nbr %d" % r.r_nbr)
                        print("    r >%s<" % r)
                        print("    r.h %s, r.h.rows %s" % (r.h, r.h.rows))
                        if r.r_nbr == len(rh.rows):
                            self.near_row(mx,my, rh.h_nbr, r.r_nbr)
                    elif self.rdg.region == self.rdg.middle:  # On 
                        self.rdg.current_object = obj
                        draw_headers.hdr_mode = "change_row_lines"
                        self.root.config(cursor="sb_v_double_arrow")  # ^=v
                        draw_headers.crl_coords = [mx,my]
                    elif self.rdg.region == self.rdg.left or \
                             self.rdg.region == self.rdg.right:
                        draw_headers.row.var_len_row(self, r)
                elif not done:
                    print(">>>>> 'far' from row or field <<<<<<")
                    ix0,iy0, ix1,iy1 = item_coords  # bbox for clicked item
                    print("item bbox %d,%d, %d,%d" % (ix0,iy0, ix1,iy1))
                    if my < iy0-12 or my > iy1-12:  # Make new header
                        h_nbr = draw_headers.header.new_header_nbr(self)
                        print("new header, h_nbr %d" % h_nbr)
                        h_coords = [mx,my]  ##, mx+2,my+2]
                        new_h =self.header(self.drawing, self.root, self.rdg,
                            h_nbr, h_coords, 0)  # Draws row 1 <<< :-)
                        self.rdg.dump_objects("New header added <<<<")
          
    def dg_b1_motion(self, event):  # Move the current`_object
        if not self.rdg.current_object:  # No current_object yet!
            return
        mx, my = (event.x, event.y)  # Mouse position
        if draw_headers.hdr_mode == "normal":
            self.move_c_o = self.rdg.current_object  # Header object
            if self.move_c_o and self.move_c_o.o_type == "header":
                move_c_obj = self.move_c_o.a_obj
                dx = mx-self.rdg.last_mx;  dy = my-self.rdg.last_my
                self.header.move(self, self.move_c_o.a_obj, dx,dy)
            elif self.move_c_o and self.move_c_o.o_type == "row":
                r_clo = self.move_c_o.a_obj
                ##print("b1_motion acts on %s" % r_clo)
            self.hm_count += 1; #print("hm_count %d" % self.hm_count)
        elif draw_headers.hdr_mode == "change_row_lines":
            #print("crl")  # Track movement, change row lines here <<<<<<<
            r_obj = self.rdg.current_object  # Row object
            if draw_headers.crl_coords:
                #print("? ? ? crl_coords %s (%s)" % (
                #    draw_headers.crl_coords, 
                #    type(draw_headers.crl_coords[1])))
                if my < draw_headers.crl_coords[1]-1:
                    print("====== up")
                    draw_headers.crl_coords = None  # Only allow 1 row change
                    draw_headers.row.change_row_lines( self, r_obj, -1)  # Up
                elif my > draw_headers.crl_coords[1]+1:
                    print("====== down")
                    draw_headers.crl_coords = None  # Only allow 1 row change
                    draw_headers.row.change_row_lines(self, r_obj, +1)  # Down
        elif draw_headers.hdr_mode == "move_bar":
            #print("mvb")  # Track movement, change bar here <<<<<<<
            if draw_headers.crl_coords:
                #print("crl_coords %s" % draw_headers.crl_coords)
                f_obj = self.rdg.current_object  # Field object
                #print("& & & crl_coords %s (%d,%d), f_obj %s (%s)" % (
                #    draw_headers.crl_coords, mx, my, f_obj, type(f_obj)))
                if mx < draw_headers.crl_coords[0]-1:
                    print("====== left")
                    draw_headers.crl_coords = None  # Only allow 1 bar move
                    draw_headers.field.move_bar( self, f_obj, -1)  # Left
                elif mx > draw_headers.crl_coords[0]+1:
                    print("====== right")
                    draw_headers.crl_coords = None  # Only allow 1 bar move
                    draw_headers.field.move_bar(self, f_obj, +1)  # Right

        self.rdg.last_mx = mx;  self.rdg.last_my = my  # Last mouse position
 
    def dg_b1_release(self, event):  # Left button released
        ##??print("b1_r ", end="")
        #t = self.rdg.current_object
        #    draw_headers.crl_coords, draw_headers.hdr_mode))
        
        self.rdg.current_object = None  # Stop moving it!
        draw_headers.hdr_mode == "normal"
        self.root.config(cursor="")

        mx, my = (event.x, event.y)  # Mouse position
        self.rdg.last_mx = mx;  self.rdg.last_my = my  # Last mouse position

    """
    def dg_b3_click(self, event):
        self.double_b3_click_flag = False
        self.drawing.after(250, self.dg_b3_action, event)
            # Delay to allow for double-click

    def dg_b3_double(self, event):
        self.double_b3_click_flag = True

    def dg_b3_action(self, event):
        if self.double_click_flag:
            #print('b3_double click event')
            self.double_b3_click_flag = False
            print("+ + + + + dbl-b3")
            mx, my = (event.x, event.y)  # Mouse position
            self.rdg.last_mx = mx;  self.rdg.last_my = my  # Last mouse position
            item_id, obj = self.dh_closest(mx,my)  # Closest tk object
            if not item_id:  # Empty tuple, nothing drawn yet
                print("** Nothing drawn yet:")
            else:
    """

    def where_am_i(self):
        print("!!!!! message from where_am_i()")
        print("   self.left = %s (%s)" % (self.left, type(self.left)))
        #  self here is self.rdg in rfc_draw_globals_class !
        self.test_fn()  # We can call an outer_block function in draw_globals

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
    dho = draw_headers(drawing, root, rdg)
    #print("??? dho.rdg %s" % dho.rdg)
    dho.set_event_handlers()
    root.mainloop() 
