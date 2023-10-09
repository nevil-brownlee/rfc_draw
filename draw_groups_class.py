# 1706, Sat  8 Apr 2023 (NZST)
# 1715, Tue 21 Mar 2023 (NZDT)
# 1713, Mon  2 Oct 2023 (NZDT)
#
# draw_groups_class: functions to draw/move/edit group objects
#
# Copyright 2023, Nevil Brownlee, Taupo NZ

import tkinter as tk
#import tkinter.font

import arrow_lines_class as alc   # Draw lines with direction arrows

class draw_groups:  # rectangle+text objects for rfc-draw
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)  # New instance of text_info

    def __init__(self, parent, root, rd_globals):
        super().__init__()
        self.drawing = parent;  self.root = root
        self.rdg = rd_globals
        self.double_click_flag = False
        self.rdg.last_mx = self.rdg.last_my = 0
        #print("draw_groups_class, rdg = %s (%s)" % (self.rdg, type(self.rdg)))
        self.gm_count = 0;
        
    def set_event_handlers(self):
        self.root.bind('<KeyPress-u>',self.on_key_press_repeat) # ungroup
        # Click b1 to make an object
        self.drawing.bind_class('Canvas','<Button-1>', self.dg_b1_click)
        self.drawing.bind_class('Canvas','<Button1-Motion>', self.dg_b1_motion)
        self.drawing.bind_class('Canvas','<ButtonRelease-1>',self.dg_b1_release)
        self.drawing.bind_class('Canvas','<Button-3>',self.dg_b3_click)
        self.drawing.bind_class('Canvas','<Double-3>',self.dg_b3_double)
        print("draw_groups, handlers set <<<<")

    def dg_closest(self, mx,my):
        item = self.drawing.find_closest(mx,my)
        if len(item) == 0:  # Empty tuple
            #print("dg_closest(): empty tuple")
            return None, None
        item_x = item[0]       
        item_type = self.drawing.type(item_x)
        self.rdg.current_object =  self.rdg.objects[item_x]
        #print("CdgD closest(): item_x = tk %s (%s), mx,my %d,%d" % (
        #    item, item_type, mx,my))

        if item_type == "rectangle":
            tags = self.drawing.gettags(item_x)
            #print("=== rectangle === item_x %d, tags %s" % (item_x, tags))
            et = any(item.startswith('edr ') for item in tags)
            if et:
                #print("edr tag >%s<" % et)
                return item, self.rdg.current_object

        cg_obj = self.find_surrounding_group(mx,my)
        if cg_obj:
            #print("Ccg_objD = %s" % cg_obj)
            self.rdg.current_object = cg_obj
            return item, self.rdg.current_object
        if item_type == "group":
            #print("Cdg2D item type %s" % item_type)
            self.rdg.current_object = self.rdg.objects[item_x]
            return item, self.rdg.current_object
        return None, None

    def new_group(self, g_coords):  # Create group >>and draw it<<
        #print("new_group() called")
        g_nbr = self.rdg.new_group_nbr()
        new_g = self.rdg.group(self.rdg, self.drawing, g_nbr, g_coords)
        new_g.tlx = g_coords[0]; new_g.tly = g_coords[1]  # Group's top-left corner
        self.rdg.region = self.rdg.new
        self.rdg.draw_group_edr(new_g)

        group_obj = self.rdg.object(
            new_g.g_rect_id, new_g, "group", g_coords, "g", g_nbr, 0)
        self.rdg.objects[new_g.g_rect_id] = group_obj
        self.rdg.current_object = group_obj
        #print("new_group: objects[new_g.g_rect_id] = %s" %
        #    self.rdg.objects[new_g.g_rect_id])
        # new group, has no members yet!
        
    def find_surrounding_group(self, mx,my):
        #print("find_s_group: current_object: %s" % self.rdg.current_object)
        for j,key in enumerate(self.rdg.objects):
            obj = self.rdg.objects[key]
            #print("=-= key %s, o_type %s" % (key, obj.o_type))
            if obj.o_type == "group":
                #print("=a= key %s,  %s" % (key, obj.object))
                self.rdg.region = self.rdg.where(obj.object, mx,my)
                #print("=b= region %s" % self.rdg.pos[self.rdg.region])
                if self.rdg.region == self.rdg.middle:
                    return obj
        return None

    def extrema(self, obj):  # Extrena for x,y pairs in obj
        xmin = xmax = obj[0];  ymin = ymax = obj[1]
        for j in range(2,len(obj),2):
            x = obj[j];  y = obj[j+1]
            xmin = min(xmin,x);  ymin = min(ymin,y)
            xmax = max(xmax,x);  ymax = max(ymax,y)
        return [xmin,xmax, ymin,ymax]

    def find_objects_bbox(self, obj_list):
        if len(obj_list) == 0:
            pass
            #print("find_bbox: No objects in list");  exit()
        #print("obj_list %s" % obj_list)
        points = []
        for obj in obj_list:
            #print("$$$ obj.o_type %s, obj.key %d" % (obj.o_type, obj.key))
            self.min = self.max = False
            if obj.o_type == "n_rect":
                x0,y0, x1,y1  = obj.object.bbox()
                points.extend(obj.object.bbox())
                #print("n_rect points = %s" % points)
            elif obj.o_type == "line":
                points.extend(self.drawing.coords(obj.key))
                #print("line points = %s" % points)
            elif obj.o_type == "text" and obj.in_n_rect == 0:  # Free-standing
                #print("obj = %s" % obj)
                c_text = self.drawing.itemcget(obj.object, "text")
                h,w = self.rdg.str_h_w(c_text)  # 0.5 of dimensions!
                px_h = h*self.rdg.f_height
                px_w = w*self.rdg.f_width+2  # +2 -> 1 px space each side
                cx, cy = self.drawing.coords(obj.key)
                t_coords = (cx-px_w, cy-px_h, cx+px_w, cy+px_h)
                points.extend(list(t_coords))
                #print("text points = %s" % points)
        x0,x1, y0,y1 = self.extrema(points)
        #print("    extrema %d,%d, %d,%d" % (x0,y0, x1,y1))
        return  x0-2,y0-2, x1+2,y1+2

    def find_group_objects(self, id_list):
        objs_in_group = []
        for id in id_list:
            if id in self.rdg.objects:
                obj = self.rdg.objects[id]
                if (obj.o_type == "n_rect" or obj.o_type == "line" or
                        (obj.o_type == "text" and obj.in_n_rect == 0)):
                    #print("%3d, %s" % (id, self.rdg.obj_to_str(obj)))
                    objs_in_group.append(obj)
        return objs_in_group
    
    def print_group(self, headline, g):
        print("@print_group: %s g_nbr %d, %d members" % (
            headline, g.g_nbr, len(g.g_members)))
        for obj in g.g_members:  # i.e. contained tk objects
            print("object: >%s<" % obj)

    def print_list(self, hdr, ll):
        print("$$$ print_list: %s" % hdr)
        for  e in ll:
            print("   %s" % e)
        print("end of list\n")
    
    def create_group(self, event):  # Create new group
                        # i.e, get set to draw the group's edr using b1
        if self.rdg.n_groups == self.rdg.mx_groups:
            print("\a>>> Can only have at most %d groups!" % \
                  self.rdg.mx_groups)
            return
        self.rdg.n_groups += 1; g_nbr = self.rdg.n_groups
        mx, my = (event.x, event.y)  # Mouse position
        #print("create_group(): g_nbr %d, mx,my = %d,%d" % (g_nbr, mx,my))
        g_coords = [mx,my, mx,my]  # Only draw group's edr in b1_motion!
        #print("g_coords (edr) = %s" % g_coords)
        g_obj = self.rdg.group(self.rdg, self.rdg.drawing, g_nbr, g_coords)

        g_key = "g%d" % g_nbr
        group_obj = self.rdg.object(g_key, g_obj, "group",
            g_coords, "g", g_nbr, 0)
        #print("?:? create_group, g_key %s add to self.objects" % g_key)
        self.rdg.objects[g_key] = group_obj
        self.rdg.current_object = group_obj
        #print("   objects[%s] = %s" % (g_key, self.rdg.objects[g_key]))
        #self.rdg.dump_objects("new_group")
        return group_obj

    def rel_coords(self, edr, s_coords):
        n_points = int(len(rel_coords)/2)
        #print("++ screen_coords: n_points %d, edr %s, s_coords %s" % (
        #    n_points, edr, s_coords))
        ex = edr[0];  ey = edr[1]  # Top-left corner
        rel_coords = []
        for ns in range(0,n_points):
            rel_coords.append(s_coords[ns*2]-ex)    # sx
            rel_coords.append(s_coords[ns*2+1]-ey)  # sy
        return rel_coords

    def edr_to_group(self):  # Creates group from edr
        #self.rdg.dump_objects("=== Starting edr_to_group")
        edr = self.rdg.current_object  # It's an object, o_type "group"
            # already in self.rdg.objects, index tn (n = g_nbr)
        g_nbr = edr.object.g_nbr
        #print("@@@ edr = %s, g_nbr = %d" % (edr, g_nbr))
        eo = edr.object
        #print("    eo  = %s" % eo)
        #print("- - - eo coords ", end="");  print(eo.bbox())
        tags = self.drawing.gettags(eo.g_rect_id)
        #print("tags before = ", end="");  print(tags)
        found_edr_tag = False
        for et in tags:  # eo's tags
            t = et.split()
            #print("et >%s<, t %s" % (et, t))
            if t[0].startswith("edr"):
                found_edr_tag = True
                g_nbr = int(t[1])
                #self.print_list("found edr, t_members", eo.t_members)
                us_coords = [eo.x0,eo.y0, eo.x1,eo.y1]  # Un-shrunk coords
                #print("eo coords: %d,%d, %d,%d" % (eo.x0,eo.y0, eo.x1,eo.y1))
                #self.rdg.dump_objects("--- Find_enclosed")
                id_list = self.drawing.find_enclosed(
                    eo.x0,eo.y0, eo.x1,eo.y1)
                #print("id_list: ", end="");  print(id_list)
                group_objs = self.find_group_objects(id_list)
                x0,y0, x1,y1 = self.find_objects_bbox(group_objs)
                esp = 10  # Edge space (need this much
                    # to select group reliably by clicking in the esp)
                #print("BBB shrink to %d,%d, %d,%d" % (
                #    x0-esp,y0-esp, x1+esp,y1+esp))
                eo.coords(x0-esp,y0-esp, x1+esp,y1+esp)
                     # Shrink edr to surround (with edge margine) it's objects
                eo.group = g_nbr  # eo is now a group
                edr = (x0-esp,y0-esp, x1+esp,y1+esp)

                #print("+ + group_objs = %s" % group_objs)
                for obj in group_objs:  # Add enclosed objects to group
                    #print("   obj.key = %d, o_type %s" % (obj.key, obj.o_type))
                    oo_key = obj.key  # Original object key
                    if obj.o_type == "n_rect":
                        x0,y0, x1,y1  = obj.object.bbox()
                        coords = (x0,y0, x1,y1)
                        nro = obj.object
                        g_object = self.rdg.object(oo_key, nro,
                            obj.o_type, coords, "", g_nbr, 0)
                        #??g_object = obj.object
                        g_tk_id = oo_key
                    elif obj.o_type == "line":
                        a_line = obj.object
                        #a_line.undraw_line() # Not needed
                        coords = a_line.lbd  # screen coords 
                        #a_line.draw_line()
                        g_object = self.rdg.object(oo_key, a_line,
                            obj.o_type, coords, "n", g_nbr, 0)
                        g_tk_id = oo_key ###################
                    elif obj.o_type == "text" and obj.in_n_rect == 0:  # Free
                        coords = self.drawing.coords(obj.key)
                        g_tk_id = oo_key
                        g_object = self.rdg.object(oo_key, obj.object,
                            obj.o_type, coords, "t", g_nbr, 0)
                    else:
                        print("\ae_t_g: bad object type, %s" % obj)
                    r_coords = self.rdg.rel_coords(edr, coords)
                    g = self.rdg.g_member(self.rdg, g_nbr, oo_key,
                        g_tk_id, g_object, r_coords)
                    eo.g_members.append(g)
                # eo's objects are now part of it's template group
        #print("==> edr_to_group")

        if not found_edr_tag:
            print("\a>> The object you b3-double-clicked is not an edr")

    def on_key_press_repeat(self, event):
       self.has_prev_key_press = True
       self.drawing.after(150, self.on_key_press, event)
       #print("on_key_press_repeat >%s<" % repr(event.char))
   
    # IMPORTANT: b1_click sets self.rdg.current_object (which includes it's key)
    #   b1_motion and b1_release all work on rdg.current_object

    def on_key_press(self, event):
        self.has_prev_key_press = False
        key = event.char
        if key == "u":  # Ungroup
            self.drawing.delete(self.rdg.current_object.object.g_rect_id)
                # Undraw group's edr (don't try to re-use it's group nbr!)
            del self.rdg.objects[self.rdg.current_object.key]
                # Remove group object from self.rdg.objects
                
    def dg_b1_click(self, event):
        self.drawing.after(250, self.dg_b1_action, event)
            # Delay to allow for double-click
    def dg_b1_action(self, event):  # B1 (left button) to select an object
        #print("b1_a ", end="")
        mx, my = (event.x, event.y)  # Mouse position
        self.rdg.last_mx = mx;  self.rdg.last_my = my  # Last mouse position
        self.x0 = mx;  self.y0 = my
        #print("# # # dg_b1_click: %s ln_mode, %d,%d, %d objects, %s, %s" % (
        #    self.rdg.ln_mode, mx, my, len(self.rdg.objects), 
        #       event.widget, event.type))
        ##print("@@ current_object >%s<" % self.rdg.current_object)

        item, obj = self.dg_closest(mx,my)  # Closest tk object
        #print("b1_click(): closest returned item %s, obj %s" % (item, obj))
        if not item:  # Empty tuple, nothing drawn yet
            #print("Nothing drawn yet:")
            g = self.new_group([mx,my, mx,my])  # sets current_object
            #print("new g = >%s<" % g)
            self.rdg.region = self.rdg.new  #######
            self.x0 = mx;  self.y0 = my
              # edr coords start with b1_click's self.x0, self.y0,
              #   to make a template, in self.rdg.objects,
              #   and making it self.rdg.current_object
            self.rdg.dump_objects("Closest() returned None")
            ##print("waiting for input . . .");  q = input()
        else:
            item_ix = item[0]
            #print("closest tk object: >%s< (%s)" % (item_ix, obj.o_type))
            if obj.o_type == "group":
                #print("group item-ix %d: " % item_ix)
                g = obj.object  # group
                #print("Clicked near group %d" % g.g_nbr)
                if len(g.g_members) != 0:
                    pass
                    #print("$$$ g: g_nbr %d, g_coords %s, edr_tag %s" % (
                    #    g.g_nbr, g.bbox, g.edr_tag))
                    #print("     g_members: ", end="");  print(g.g_members)
                self.current_object = obj
                #print("Clicked near group %d . . ." % g.g_nbr)
                self.rdg.region = self.rdg.where(g, mx,my)
                #print("&&& where return = %d" % self.rdg.region)
            else:
                ### clicked near something not a group
                #print("About to call find_surrounding_group()")
                obj = self.find_surrounding_group(mx,my)
                if not obj:
                    print("\aNo surrounding group found!")
                    exit()
                #print("Found surrounding group: g_nbr %d" % g.g_nbr)

            g = obj.object
            #??g = self.new_group(event, (mx,my, mx,my))  # sets current_object
            #print("g coords %d,%d, %d,%d" % (
            #    g.x0, g.y0, g.x1, g.y1))
            ##self.rdg.region = self.rdg.where(g, mx,my)
            ##print("&&& where return = %d" % self.rdg.region)
            if self.rdg.region == self.rdg.far:
                self.new_group(g.g_coords)
            #print("@@@ b1_action, region %d" % self.rdg.region)
    """             
    def dg_b1_double_action(self, event):
        if self.double_click_flag:
            #print('double b1 click event')
            self.double_click_flag = False
            print("\ab1_double not implemented (yet) <<<<<<<")
        else:
            self.dg_b1_action(event)
    """
    def dg_b1_motion(self, event):  # Move the current_object
        mx, my = (event.x, event.y)
        ##print("current_object >%s<"% self.rdg.current_object)
        if self.rdg.current_object == None:  # No current_object yet!
            return
        elif self.rdg.current_object.o_type == "group":
            go = self.rdg.current_object.object  # Group object has edr's coords
            #grp_dr_id = g.g_rect_id
            #print("=1= g_nbr %s, regn %s" % (
            #    self.rdg.pos[self.rdg.region], self.rdg.region))
            dx = mx-self.rdg.last_mx;  dy = my-self.rdg.last_my
            #print("$$$ region %d, mx,my %d,%d  deltas %d,%d, current_obj %s" % (
            #    self.rdg.region, mx,my, dx,dy, self.rdg.current_object))
            if self.rdg.region == self.rdg.new: # Drawing the edr, tl to lr
                go.coords(self.x0,self.y0, mx,my)
                #print("go = %s" % go)
            elif self.rdg.region == self.rdg.middle:  # Existing group
                #print("calling go.move(%d,%d)" % (dx,dy))
                go.move(dx,dy)
            else:
                #print("go = %s, region = %d" % (go, self.rdg.region))
                #print("dg b1_m: dx,dy = %d,%d" % (dx,dy))
                g = self.rdg.current_object.object
                nx0,ny0, nx1,ny1 = self.rdg.move_deltas(g.bbox(), dx,dy)
                self.rdg.current_object.object.coords(nx0,ny0, nx1,ny1)

        self.gm_count += 1; #print("gm_count %d" % self.gm_count) ########

        self.rdg.last_mx = mx;  self.rdg.last_my = my  # Last mouse position

    def dg_b1_release(self, event):  # Left button released
        #print("b1_r ", end="")
        t = self.rdg.current_object
        ##ttt = self.rdg.objects[self.rdg.current_object.key]
        #print("b1_rel t %s" % t)
        mx, my = (event.x, event.y)  # Mouse position
        self.rdg.last_mx = mx;  self.rdg.last_my = my  # Last mouse position
        
    def dg_b3_click(self, event):
        self.drawing.after(250, self.dg_b3_action, event)
            # Delay to allow for double-click

    def dg_b3_double(self, event):
        self.double_click_flag = True

    def dg_b3_action(self, event):
        if self.double_click_flag:
            #print('b3_double click event')
            self.double_click_flag = False
            self.edr_to_group()

        else:  # B3 (right button) to edit a Text
            if self.rdg.ln_mode == "group":
                print("\a>> Can't edit Text using b3 in group mode")
            else:
                pass
                #print("?? b3 single-click not used in %s mode" % (
                #    self.rdg.ln_mode))
    """
    def where_am_i(self):
        print("!!!!! message from where_am_i()")
        print("   self.left = %s (%s)" % (self.left, type(self.left)))
        #  self here is self.rdg in rfc_draw_globals_class !
        self.test_fn()  # We can call an outer_block function in draw_globals
    """

if __name__ == "__main__":
    root = tk.Tk()  # Main window
    drawing = tk.Canvas(root, width=600, height=600, bg="white")  # Drawing area
    drawing.pack(padx=10, pady=10)
    dto = draw_text_object(drawing, root)
    root.mainloop() 
