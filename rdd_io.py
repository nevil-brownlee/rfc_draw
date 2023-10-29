# 1621, Sat 28 Oct 2023 (NZST)
# 1107, Wed  6 Sep 2023 (NZST)
# 1455, Wed 31 May 2023 (NZST)
# 1457, Tue 26 Sep 2023 (NZDT)
#
# rdd_rw.py: Read/write *.rdd files
#
# Copyright 2023, Nevil Brownlee, Taupo NZ

import re

class rdd_rw:
    def __init__(self, fn):
        self.rdd_fn = fn
        #print("rdd_fn %s" % self.rdd_fn)
        self.objects = []   # rfc-draw objects
        self.r_obj_keys = {}  # old-key -> new-key for objects read from rdd

        # Patterns for reading the description string for an object
        self.rrd_re = re.compile(
               "(\d+)\s+\((.+)\s+(.+)\)\s+\[(.+)\]\s+\"(.*)\"\s+(\d+)\s+(.)")
        # field   0        1       2          3          4         5      6
        #       objid    type    skey       coords     text      g_nbr   g_type

        self.mbr_re = re.compile(
               "\s+\((.)(.+)\ member\s(.+)\)\s+(.+)\s\[(.+)\]")
        # field       0  1           2        3       4
        #    blanks  id g_nbr       g_key    type    coords
       

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
        def __init__(self, id, type, coords, text, t_width, g_nbr):
            self.id = id
            self.type = type;  self.i_coords = coords
            self.i_text = text;  self.txt_width = t_width
            self.g_nbr = g_nbr; self.g_members = []
            
        def __str__(self):
            return (
                "id %d, type %6s, i_text %s, g_nbr %d, i_coords %s, txt_width %d" % (
                self.id, self.type, self.i_text, self.g_nbr,
                self.i_coords, self.txt_width))

    class g_member:  # Holds group info for a group member obj
        def __init__(self, objects, g_nbr, m_key, g_rel_coords):
            self.objects = objects
            self.g_nbr = g_nbr
            self.m_key = m_key  # member's original objects[] key
            self.g_rel_coords = g_rel_coords
            
        def __str__(self):
            m_type = self.objects[self.m_key].type
            return ("g_nbr %s, m_key %s, m_type %s, rel_coords %s" % (
                self.g_nbr, self.m_key, m_type, self.g_rel_coords))

    def find_group_key(self, g_nbr):
        for val in self.objects:
            if val.type == "group" and val.g_nbr == g_nbr:
                return val.id

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

    def restore_object(self, ds):
        #print("restore_object: ds >%s<" % ds)
        if "member" in ds:
            #print("=== member line >%s<" % ds)
            self.dump_objects(">> 'member' read <<")

            fields = self.mbr_re.search(ds).groups()
            gt = fields[0]  # 'g'
            g_nbr = int(fields[1])  # group (or template number)
            o_key = fields[2]  # member key in objects[]
            m_key = self.r_obj_keys[o_key]
                # member key in new objects[] dict
            m_type = fields[3]  # member type
            mo = self.objects[m_key]
            #print("+++ mo >%s<" % mo)
            i_coords = self.s_to_ilist(fields[4])
            #print("gt %s, g_nbr %d m_key %d, type %s, coords >%s<" %
            #      (gt, g_nbr, m_key, m_type, i_coords))
            g_key = self.find_group_key(g_nbr)-1  # 0-ord for objects[]
            go = self.objects[g_key]
            i_coords = mo.i_coords;  i_text = mo.i_text
            r_coords = self.rel_coords(go. i_coords, i_coords)
            m = self.g_member(self.objects, g_nbr, m_key, r_coords)
            self.objects[g_key].g_members.append(m)
            return m_key, g_key
        else:  # Ordinary object
            #print("== ds %s ==" % ds)
            fields = self.rrd_re.search(ds).groups()
            #print("@@@ rdd_io fields = ", end="");  print(fields)
            obj_id = int(fields[0])  # Ignore line_nbr (field 0)
            obj_type = fields[1]
            s_key = fields[2]  # object's key in save file
            coords = self.s_to_ilist(fields[3])
            text = fields[4].replace("\\n", "\n")
            text = text.replace('\\"', '"')
            g_nbr = int(fields[5])  # Group nbr
            g_type = fields[6]  # Group type
            t_width = 0
            if obj_type == "text":
                t_lines = text.split("\n")
                #print("@@@ t_lines >%s<" % t_lines)
                for l_txt in t_lines:
                    chrs = len(l_txt)
                    if chrs > t_width:
                        t_width = chrs
            obj = self.rdd_obj(obj_id, obj_type, coords, text, t_width, g_nbr)
            #print("=== obj = >%s<" % obj)
            self.objects.append(obj)  # rdd_io objects are in a list 
            new_key = len(self.objects)-1
            self.r_obj_keys[s_key] = new_key
            #print("r_obj_keys = %s" % self.r_obj_keys)
            return new_key, obj

    def dump_objects(self, header):
        #return
        print("dump_objects -- %s --" % header)
        for j, val in enumerate(self.objects):
            print("%4d val >%s<" % (j, val))
            if val.type == "group":
                for g_m in val.g_members:
                    print("  member %s" % g_m)
        print("- - dump - -")  # Trailer line

    
    def read_from_rdd(self):
        f = open(self.rdd_fn, "r")
        self.di = {}
        for line in f:
            #print(">>>%s<" % line)
            if line[0] == "#":  # Ignore comment lines
                continue
            ds = line.rstrip('\n')
            #print("ds >%s<" % ds)
            if ds.find("root_geometry") >= 0:
                la = ds.split(" ");  dims = la[1].split("+")
                xy = dims[0].split("x")
                self.di["r_width"] = int(xy[0])
                self.di["r_height"] = int(xy[1])
                #print("root geometry: x %d, y %d" % (self.xr, self.yr))
            elif ds.find("drawing_size") >= 0:
                la = ds.split(" ")
                la_ds = la[1].split("x")
                self.di["d_width"]  = int(la_ds[0])  # drawing width
                self.di["d_height"] = int(la_ds[1])  # drawing height
                #print("drawing_size %dx%d" % (self.dw,self.dh))
            elif ds.find("mono_font") >= 0:
                la = ds.split(" ")
                #print("mono_font width %.2f, height %.2f pixels" % (
                #    self.f_width, self.f_height))
                self.di["f_width"] = float(la[2])
                self.di["f_height"] = int(la[4])
            else:
                #print("=== ds = %s" % ds)
                o_key, obj = self.restore_object(ds)
                #print("--- o_key %s, obj >%s<" % (o_key, obj))

        min_x = min_y = 50000;  max_x = max_y = 0
        for obj in self.objects:
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
            self.di["min_x"] = min_x;  self.di["max_x"] = max_x
            self.di["min_y"] = min_y;  self.di["max_y"] = max_y
        #print("+++ min_x %d, max_x %d, min_y %d, max_y %d" % (
        #    min_x, max_x, min_y, max_y))
                    
        fs = "Screen: xr %d, yr %d | Drawing: width %d, height %d"
        fs += " | Font: width %.2f, height %.2f"
        print(fs % (self.di["r_width"], self.di["r_height"],
            self.di["d_width"], self.di["d_height"],
            self.di["f_width"], self.di["f_height"]))

        return self.di
