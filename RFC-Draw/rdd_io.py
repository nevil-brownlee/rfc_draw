# 1607, Tue 31 Oct 2023 (NZDT)
# 1107, Wed  6 Sep 2023 (NZST)
# 1455, Wed 31 May 2023 (NZST)
#
# rdd_rw.py: Read/write *.rdd files
#
# Copyright 2025, Nevil Brownlee, Taupo NZT

import re

import debug_print_class as dbpc
dbp = dbpc.dp_env(False)  # debug printing on

class rdd_rw:
    def __init__(self, sys_argv, bw):  # i.e. sys.arg)
        dbp.db_print("starting rdd_io.py - - -")
        self.objects = []   # rfc-draw objects
        self.obj_keys = {}  # old-key -> new-key for objects read from rdd
        self.default_bw = 5  # px
        dbp.db_print("??? sys_argv >%s<, len %d" % (sys_argv, len(sys_argv)))
        
        if len(sys_argv) == 1:
            print("No .rdd file specified ???")
            from tkinter.filedialog import askopenfilename
            self.rdd_fn = (askopenfilename(title="Select .rdd source file"))
        else:
            self.rdd_fn = sys_argv[1]

        # Patterns for reading the description string for an object
        # . matches any character except a newline (\n)

        rere_0_4 = r"(\d+)\s+\((.+)\s+(.+)\)\s+\[(.+)\]\s+\"(.+)\""
            # field   0        1      2          3          4
            #       objid    type    skey       coords     text 
        rere_v1 = rere_0_4 + r"\s+(.+)\s+(.+)\Z"  # \Z = at end-of-string
            # rdd v1:              5      6
            #                     g_nbr   g_type
            #               '0', 'N' or '1'

                                # \S = non-white-space character
        rere_v2 = rere_0_4 + r"\s+(\S+)\s+(\S+)\s+(\S+)(\s.+)?"
     
        #                          5       6       7     8
            #              parent_id,     v1,     v2,    Optional comment
        self.rdd_e_v1 = re.compile(rere_v1)
        self.rdd_e_v2 = re.compile(rere_v2)

        self.border_width = self.default_bw  # Default value
        
        #dbp.db_
        print("rdd_io: sys_argv >%s<" % sys_argv)
        if not self.rdd_fn:
            self.rdd_fn = sys_argv[1]
        if len(sys_argv) >= 3:  # We have a second argument
            ##print("sys_argv >%s<" % sys_argv)
            self.border_width = int(sys_argv[2])
        dbp.db_print("=== rdd_fn %s, bw %s" % (self.rdd_fn, self.border_width))
        #self.objects, self.di = self.read_from_rdd()
        #self.dump_objects("rdd objects loaded from .rdd file")
        
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

    class rdd_obj:
        def __init__(self, id, type, coords, text, parent_id, v1, v2):
            self.id = id
            self.type = type;  self.i_coords = coords
            self.i_text = text;  self.txt_width = len(text)
            self.vbl_len_row = v2 < 0
            self.parent_id = parent_id;  self.v1 = int(v1);  self.v2 = int(v2)
            
        def __str__(self):
            return (
                "id %d, type %6s, i_text %s, i_coords %s, parent_id %d, v1 %d, v2 %d, txt_width %d" % (
                    self.id, self.type, self.i_text, self.i_coords,
                    self.parent_id, self.v1, self.v2, self.txt_width))
    
    def parse_rdd_line(self, line):
        line = line.rstrip()
        dbp.db_print("rdd line = >%s<" % line)
        if self.rdd_e_v2.match(line):  # v2 match (9 fields)
            m = self.rdd_e_v2.split(line)
            dbp.db_print("v2 split %s len %d" % (m, len(m)))
            return m[1:-1]
        else:
            dbp.db_print("v2 match failed")#;  exit()
            if self.rdd_e_v1.match(line):  # v1 match (6 fields)
                m = self.rdd_e_v1.split(line)
                dbp.db_print("v1 split %s len %d" % (m, len(m)))
                return m[1:-1]
            else:
                dbp.db_print("v1 match failed");  exit()
                return None
    """
    def is_number(self, s):
        try:
            v =float(s)
            return True
        except ValueError:
            return False
    """
    def restore_object(self, ln, ds):
        #dbp.db_print("restore_object: ln %d, ds >%s<" % (ln, ds))
        #dbp.db_print("== ds %s ==" % ds)
        fields = self.parse_rdd_line(ds)
        dbp.db_print("fields >>> %s <<< len %d" % (fields, len(fields)))
        obj_id = int(fields[0])  # Ignore line_nbr (field 0)
        o_type = fields[1]
        old_key = int(fields[2])  # object's key in save file
        coords = self.s_to_ilist(fields[3])
        text = fields[4].replace("\\n", "\n")
        fields[4] = fields[4].replace('\\"', '"')
        dbp.db_print("After \\n: fields %s" % fields)
        if fields[5] == 'N':
            dbp.db_print("v1 rdd file <<<")
            parent_id = 0
        else:
            parent_id = int(fields[5])
        #self.dump_objects("in restore_object")
        if parent_id != 0:
            parent_id = int(self.obj_keys[parent_id])
        if fields[6] == "N":  # v1 rdd file
            v1 = v2 = 0
        else:
            dbp.db_print("fields[6] >%s" % fields[6])
            v1 = int(fields[6].strip('"'))  # Remove any surrounding " chars
            if len(fields) == 9:  # v2 match (Optional comment is fields[8])
                v2 = int(fields[7])
                #dbp.db_print("v1 %d, v2 %d" % (v1, v2))
            else:
                dbp.db_print("rdd pattern match failed !!!");  exit()
        
                t_width = 0
                    
        obj = self.rdd_obj(obj_id, o_type, coords, text, parent_id, v1, v2)
        dbp.db_print("=== obj = >%s<" % obj)
        self.objects.append(obj)  # rdd_io objects are in a list 
        new_key = len(self.objects)-1
        self.obj_keys[old_key] = new_key
        dbp.db_print("r_obj_keys = %s" % self.obj_keys)
        return new_key, obj

    def dump_objects(self, header):
        #return
        dbp.db_print("dump_objects -- %s --" % header)
        for j, val in enumerate(self.objects):
            dbp.db_print("%4d val >%s<" % (j, val))
        dbp.db_print("- - dump - -")  # Trailer line

    def extrema(self, obj, x, y):
        if x < self.min_x:
            self.min_x = x
            self.min_x_obj = obj
        elif x > self.max_x:
            self.max_x = x
            self.max_x_obj = obj
        if y < self.min_y:
            self.min_y = y
            self.min_y_obj = obj
        elif y > self.max_y:
            self.max_y = y
            self.max_y_obj = obj
    
    def read_from_rdd(self):
        #dbp.db_
        print("read_from_rdd: self.rdd_fn >%s<" % self.rdd_fn)
        f = open(self.rdd_fn, "r")
        self.di = {}
        ln = -1
        for rdd_ln in f:
            ln += 1
            line = rdd_ln.strip()
            #dbp.db_print("rdd ln %d, len %d, line >%s<" % (ln, len(line),line))
            if len(line) == 0 or line[0] == "#":  # Ignore comment lines
                continue
            ds = line.rstrip('\n')
            #dbp.db_print("ds >%s<" % ds)
            if ds.find("root_geometry") >= 0:
                la = ds.split(" ");  dims = la[1].split("+")
                xy = dims[0].split("x")
                self.di["r_width"] = int(xy[0])
                self.di["r_height"] = int(xy[1])
                #dbp.db_print("root geometry: x %d, y %d" % (self.xr, self.yr))
            elif ds.find("drawing_size") >= 0:
                la = ds.split(" ")
                la_ds = la[1].split("x")
                self.di["d_width"]  = int(la_ds[0])  # drawing width
                self.di["d_height"] = int(la_ds[1])  # drawing height
                #dbp.db_print("drawing_size %dx%d" % (self.dw,self.dh))
            elif ds.find("mono_font") >= 0:
                la = ds.split(" ")
                #dbp.db_print("mono_font width %.2f, height %.2f pixels" % (
                #    self.f_width, self.f_height))
                self.di["f_width"] = float(la[2])
                self.di["f_height"] = float(la[4])
            elif ds.find("last_mode") >= 0: 
                pass  # Used by rfc-draw.py
            else:
                dbp.db_print("=== ds = %s" % ds)
                o_key, obj = self.restore_object(ln, ds)
                ##dbp.db_print("o_key %s, obj %s <<<" % (o_key, obj))

        self.min_x = self.min_y = 50000;  self.max_x = self.max_y = 0
        self.t_min_y = self.t_max_y = self.t_min_x = self.t_max_x = "none"
        bw = self.border_width

        self.dump_objects(">> .rdd file read <<")
        
        for obj in self.objects:
            coords = obj.i_coords
            for n in range(0, len(coords), 2):  # Lines have >1 point
                                                # Text has only 1 (cx,cy)
                x = coords[n];  y = coords[n+1]
                self.extrema(obj, x, y) 
                #dbp.db_print("+-+-+ id %d, %s, Ex:%d-%d, Ey:%d-%d" % (
                #    obj.id, obj.type,
                #    self.min_x, self.max_x, self.min_y, self.max_y))
                if obj.type == "field":  
                    x0,y0, x1,y1 = coords # obj's containing rectangle
                    self.extrema(obj, x0,y0)
                    self.extrema(obj, x1,y1)
                elif obj.type == "text":  # x,y is obj's centre position
                    t_lines = obj.i_text.split("\n")
                    c_width = self.di["f_width"]*0.8
                    dbp.db_print("c_width = %f" % c_width)
                    for l_txt in t_lines:
                        n_chrs = len(l_txt)  # This line's chars
                        #dbp.db_print("$ $ chrs %d, txt >%s<" % (chrs, l_txt))
                        l_txt = l_txt.replace('\\"', '"')
                        htw = round(n_chrs*c_width/2.0)  # half text width
                        dbp.db_print("htw %s, y %s" % (htw,y))
                        dbp.db_print("text line: text >%s< lt2 %d, from %d to %d" % (
                            l_txt, htw, x-htw, x+htw))
                        y += self.di["f_height"]  # 1 line below text
                        self.extrema(obj, x+htw, y)  # right x,y
                        self.extrema(obj, x-htw, y)  # left x,y
                    dbp.db_print("ttt x,y %d,%d, min_y %d, max_y %d" % (
                        x, y, self.max_x, self.max_y))

        self.di["min_x"] = self.min_x;  self.di["max_x"] = self.max_x
        self.di["min_y"] = self.min_y;  self.di["max_y"] = self.max_y

        dbp.db_print("Extrema: min_x %d (%s)" % (self.min_x,self.min_x_obj))
        dbp.db_print("         max_x %d (%s)" % (self.max_x,self.max_x_obj))
        dbp.db_print("         min_y %d (%s)" % (self.min_y,self.min_y_obj))
        dbp.db_print("         max_y %d (%s)" % (self.max_y,self.max_y_obj))
        dbp.db_print("")
           
        fs = "Screen: xr %d, yr %d | Drawing: width %d, height %d"
        fs += " | Font: width %.2f, height %.2f"
        dbp.db_print(fs % (self.di["r_width"], self.di["r_height"],
            self.di["d_width"], self.di["d_height"],
            self.di["f_width"], self.di["f_height"]))

        dbp.db_print("min_x %d, max_x %d,  min_y %d, max_y %d" % (
            self.di["min_x"], self.di["max_x"],
            self.di["min_y"], self.di["max_y"]))

        #self.dump_objects("After loading objects")
        
        return self.objects, self.di
