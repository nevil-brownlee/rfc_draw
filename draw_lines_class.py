# 1545, Fri 30 Jun 2023 (NZST)
# 1654, Tue 17 Jan 2023 (NZDT)
#
# draw_lines_class: functions to draw/move/edit tkinter lines
#
# Copyright 2023, Nevil Brownlee, Taupo NZ

import tkinter as tk
import tkinter.font
import math

import rfc_draw_globals_class as rdgc  # rfc-draw globals and functions
import arrow_lines_class as alc   # Draw lines with direction arrows

class draw_lines:  # line objects for rfc-draw
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)  # New instance of text_info

    def __init__(self, parent, root, rdg):
        super().__init__()
        self.drawing = parent;  self.root = root
        self.rdg = rdg;  self.a_line = alc.a_line

        self.d_step = 12  # Path distances: initial step, deviation,
        self.d_dev =   8  #   used to decide line direction (multiples of 90)
        self.d_far =  10  # Proximity: to decide whether cursor is outside line 

    def set_event_handlers(self):        # Click b1 to make an object
        self.drawing.bind_class('Canvas','<ButtonPress-1>',    self.ln_b1_click)
        self.drawing.bind_class('Canvas','<Button1-Motion>',  self.ln_b1_motion)
        self.drawing.bind_class('Canvas','<ButtonRelease-1>',self.ln_b1_release)

        self.ln_mode = "move"
        print("@@@ event handlers set @@@  mode %s" % self.ln_mode)

    def set_option(self, key):
        self.abd = self.rdg.current_object.object 
        print("set_option: self.abd = %s" % self.abd)
        self.abd.set_option(key)

    def inside_seg(self, x0,y0, mx,my, x1,y1):
        x_in = x0 <= mx and mx <= x1
        y_in = y0 <= my and my <= y1
        print("   x_in %s, y_in %s" % (x_in, y_in))
        return x_in or y_in

    def rel_to_line(self, mx,my, l_coords):  # Where is cursor rel to line?
        n_points = int(len(l_coords)/2)
        #print("rel_to_line: %d,%d, n_points %d, ln_mode %s, l_coords %s" % (
        #    mx,my, n_points, self.ln_mode, l_coords))
        sx = l_coords[0]; sy = l_coords[1]  # Point 0, start of line
        s_dx = abs(mx-sx);  s_dy = abs(my-sy) # Distances to seg start
        if (s_dx <= self.d_dev and s_dy <= self.d_dev):
            #print("Near start of line")
            return 0, 1  # Near start of line
        for ns in range(0,n_points-1):
            seg = l_coords[ns*2:ns*2+4]
            #print("@@@ ns %d, seg %s" % (ns, seg))
            if len(seg) != 4:
                print("Line has only one seg!")
                return 0, 5  # Far from line (?)
            sx = seg[0]; sy = seg[1];   ex = seg[2]; ey = seg[3]
            #print("ns = %d, seg %d,%d, %d,%d" % (ns,  sx,sy, ex,ey))
            s_dx = abs(mx-sx);  s_dy = abs(my-sy) # Distances to seg ends
            e_dx = abs(mx-ex);  e_dy = abs(my-ey)
            #print("mx %d, my %d,  s_dx %d, s_dy %d,  e_dx %d, e_dy %d" % (
            #    mx, my, s_dx, s_dy, e_dx, e_dy))

            if ns == n_points-2:  # Last seg only
                if (s_dy <= self.d_dev and e_dy <= self.d_dev):  # Horizontal
                    if ex > sx and abs(mx-(ex+self.d_far)) <= self.d_dev:
                        #print(">>> outside last rightward seg")
                        self.ln_mode = "mod_end"
                        return ns, 6  # Outside last seg
                    elif ex < sx and abs(mx-(ex-self.d_far)) <= self.d_dev:
                        #print(">>> outside last leftward seg")
                        self.ln_mode = "mod_end"
                        return ns, 6  # Outside last seg
                elif (s_dx <= self.d_dev and e_dx <= self.d_dev):  # Vertical
                    if ey > sy and abs(my-(ey+self.d_far)) <= self.d_dev:
                        #print(">>> outside last downward seg")
                        self.ln_mode = "mod_end"
                        return ns, 6  # Outside last seg
                    elif ey < sy and abs(my-(ey-self.d_far)) <= self.d_dev:
                        #print(">>> outside last upward seg")
                        self.ln_mode = "mod_end"
                        return ns, 6  # Outside last seg

            if (s_dy <= self.d_dev and e_dy <= self.d_dev):
                #print("=> %d,%d is near horiz segment %d" % (mx,my, ns))
                if (e_dx <= self.d_dev and e_dy <= self.d_dev):
                    #print("seg %d, near end" % ns)
                    if ns == n_points-2:  # n_segs = n_points-1
                        return ns, 2  # Near end of line
                    else:
                        return ns, 3  # Seg n, internal junction
                else:
                    #print("seg %d, near middle" % ns)
                    return ns, 4  # Near middle of seg n
            elif (s_dx <= self.d_dev and e_dx <= self.d_dev):
                #print("=> %d,%d is near vert segment %d" % (mx,my, ns))
                if (e_dx <= self.d_dev and e_dy <= self.d_dev):
                    #print("seg %d, near end" % ns)
                    if ns == n_points-2:  # n_segs = n_points-1
                        return ns, 2  # Near end of line
                    else:
                        return ns, 3  # Seg n, internal junction
                else:
                    #print("seg %d, near middle" % ns)
                    return ns, 4  # Near middle of seg n
        return 0, 5  # Far from an (rfc-draw) line
                    
    def ln_closest(self, mx,my):
        item = self.drawing.find_closest(mx,my) 
        if len(item) == 0:  # Empty tuple
            print("ln_closest(0): empty tuple")
            return None, None
        item_id = item[0]
        item_type = self.drawing.type(item_id)
        print("@@@ ln_closest, item_id %d, type %s" % (item_id, item_type))
        if item_type != "line":
            return None, None
        print("@ln@ closest(1): item %s (%s), mx,my %d,%d, ln_mode %s" % (
            item, item_type, mx,my, self.ln_mode))
 
        if item_id in self.rdg.objects:
            obj = self.rdg.objects[item_id]  # item_id is a tkinter object id
            # object (e.g. nro) has: key, obj, obj_ type, in_n_rect
            print("-> closest %s is in objects, obj >%s<" % (item, obj))
            # Now, is mx,my too far from this (closest) line?
            print("ln_closest(2): Nearest line %d, %s, mxy %d,%d" % (
                obj.key, obj.object.lbd, mx,my))
            #self.abd = obj.object 
            #print("   ", end='');  self.abd.print_a_line_object()

            ns, loc = self.rel_to_line(mx,my, obj.object.lbd)
            print("ln_closest(4): ns %d, loc %d, mode %s" % (
                ns, loc, self.ln_mode))
            if loc == 5:  # Far from that line
                return None, None
            else:
                self.ln_mode = "exist_ln"
            self.rdg.current_object = obj
            a_coords = self.rdg.current_object.object.lbd
            print(">> 2 >> a_coords %s, mode %s" % (a_coords, self.ln_mode))
            return item, obj
        else:  # Not in objects, assume it's an arrowhead line
            print("@@@ line %d is not in rdg.objects <<<<" % item_id)
            return None, None

    def start_new_line(self, coords, rdg):
        print("<><><> coords >%s<, rdg >%s<" % (coords, rdg))
        self.lx0 = coords[0];  self.ly0 = coords[1]
        self.abd = alc.a_line(self.drawing, coords, rdg)
        self.lbd_id = 0  # Don't draw it yet!
        #print("start_new_line(): line_id %d, self.abd %s (%s)" % (
        #    self.lbd_id, self.abd, type(self.abd)))
        self.ln_mode = "new_ln"
        self.ln_dir = self.left = self.right = self.up = self.down = False
        ##print(">>> >>> self.abd = %s (%s)" % (self.abd, type(self.abd)))
        return self.abd
        
    def reverse_line(self):
        old_abd = self.rdg.current_object.object###;  lbd = old_abd.lbd
        rev_lbd = []
        for x in range(len(old_abd.lbd)-2,-2,-2):
            rev_lbd.append(old_abd.lbd[x])
            rev_lbd.append(old_abd.lbd[x+1]) 
        old_abd.lbd = rev_lbd
        old_abd.draw_line()
        self.ln_mode = "move"

    def flip_line(self):
        old_abd = self.rdg.current_object.object;  lbd = old_abd.lbd
        bx0,by0, bx1,by1 = self.drawing.bbox(old_abd.lbd_id)
        r_coords = []  # rel to bbox
        for c in range(0,len(lbd),2):
            r_coords.append(lbd[c]-bx0)
            r_coords.append(lbd[c+1]-by0)
        print("r_coords %s" % r_coords)
        f_coords = [];  # Flipped, rel to bbox
        offset = 0;  m_y = by1-by0  # Height of bbox
        for c in range(0,len(lbd),2):
            f_coords.append(r_coords[c]+bx0-offset)
            f_coords.append(m_y-r_coords[c+1]+by0-offset)
        old_abd.lbd = f_coords
        old_abd.draw_line()
        self.ln_mode = "move"

    def equal_end_coords(self):
        old_abd = self.rdg.current_object.object;  lbd = old_abd.lbd
        n_coords = len(lbd)  # 2 coords per point
        if n_coords >= 8:  # Need enough points to even up the first and last
            if lbd[0] == lbd[2]:
                first_dir = "vert"
            elif lbd[1] == lbd[3]:
                first_dir = "horiz"
            if lbd[n_coords-4] == lbd[n_coords-2]:
                last_dir = "vert"
            elif lbd[n_coords-3] == lbd[n_coords-1]:
                last_dir = "horiz"
        if first_dir == last_dir:
            if first_dir == "horiz":
                first_x = lbd[0];  last_x = lbd[n_coords-2]
                av_x = int(first_x+last_x)/2
                lbd[0] = lbd[n_coords-2] = av_x
            elif first_dir == "vert":
                first_y = lbd[1];  last_y = lbd[n_coords-1]
                av_y = int(first_y+last_y)/2
                lbd[1] = lbd[n_coords-1] = av_y
            old_abd.draw_line()                    
        else:
            print(">>First and Last directions differ, can't = this line!")
                
    def arrows_on(self):
        old_abd = self.rdg.current_object.object
        old_abd.arrows_on()

    def no_arrows(self):
        old_abd = self.rdg.current_object.object
        old_abd.no_arrows(self.rdg.current_object)
       
    def syntax_end(self, v):
        print("dlt.syntax_end: on_of %s" % v)
        old_abd = self.rdg.current_object.object
        sx0,sy0, sx1,sy1 = old_abd.lbd[0:4]
        print("syntax_start, start %d,%d, %d,%d" % (sx0,sy0, sx1,sy1))
        ex0,ey0, ex1,ey1 = old_abd.lbd[-4:]
        print("syntax_end, start %d,%d, %d,%d" % (ex0,ey0, ex1,ey1))
        if sy0 != sy1 or ey0 != ey1:
            print(">> line's first and last segments must be horizontal")
            return
        #old_abd.syntax_end(self.rdg.current_object, v)
        old_abd.syntax_end(v)

    def same_dir(self, x2,y2):  # Do last and new segs have same direction?
        x0,y0, x1,y1 = self.abd.lbd[-6:-2]  # Last seg (2 points)
            # One more point added by release after click !!!
        print("same_dir: %d,%d %d,%d %d,%d" % (x0,y0, x1,y1, x2,y2))
        b_horiz = abs(y0-y1) <= self.d_dev and abs(y1-y2) <= self.d_dev
        b_vert = abs(x0-x1) <= self.d_dev and abs(x1-x2) <= self.d_dev
        print("bh %s, bv %s, bh or bv %s" % (
            b_horiz, b_vert, b_horiz or b_vert))
        return b_horiz or b_vert

    def modify_line(self, ns, mx,my):  # Cursor is near segment self.ns
        x0,y0, x1,y1 = self.abd.lbd[ns*2:ns*2+4]
        #print("modify_line, seg %d, %d,%d to %d,%d" % (ns, x0,y0, x1,y1))
        if len(self.abd.lbd) == 4:  # Only one segment
            dx = mx-self.rdg.last_mx;  dy = my-self.rdg.last_my
            if abs(dy) > 0:
                #print("  move up/down")
                self.abd.lbd = [x0,y0+dy, x1,y1+dy]  # Move up/down
            elif abs(dx) > 0:  # Move L/R
                #print("move L/r")
                self.abd.lbd = [x0+dx,y0, x1+dx,y1]  # Move sideways
        else:
            if abs(y0-y1) <= self.d_dev:  # Horizontal
                self.abd.lbd[ns*2:ns*2+4] = [x0,my, x1,my]
            elif abs(x0-x1) <= self.d_dev:  # vertical
                self.abd.lbd[ns*2:ns*2+4] = [mx,y0, mx,y1]

    def modify_end(self, ns, mx,my):  # Cursor is near segment self.ns
        x0,y0, x1,y1 = self.abd.lbd[ns*2:ns*2+4]
        if ns == 0:  # Modify start of first segment
            print("modify_end, seg %d, %d,%d to %d,%d" % (ns, x0,y0, x1,y1))
            if abs(y0-y1) <= self.d_dev:  # Horizontal
                self.abd.lbd[ns*2:ns*2+4] = [mx,y0, x1,y1]
            elif abs(x0-x1) <= self.d_dev:  # vertical
                self.abd.lbd[ns*2:ns*2+4] = [x0,my, x1,y1]
        else:  # Modify end of last segment
            print("modify_end, seg %d, %d,%d to %d,%d" % (ns, x0,y0, x1,y1))
            if abs(y0-y1) <= self.d_dev:  # Horizontal
                self.abd.lbd[ns*2:ns*2+4] = [x0,y0, mx,y1]
            elif abs(x0-x1) <= self.d_dev:  # vertical
                self.abd.lbd[ns*2:ns*2+4] = [x0,y0, x1,my]

    def move_line(self, abd, dx, dy):  # For moving line within a group
        old_lbd = abd.lbd;  new_lbd = []
        for x in range(0, len(old_lbd),2):
            new_lbd.append(old_lbd[x]+dx)
            new_lbd.append(old_lbd[x+1]+dy)
        abd.lbd = new_lbd
        abd.draw_line()

    def reorg_line(self, abd, sx, sy):  # Move line to new start point
        old_lbd = abd.lbd;  new_lbd = []
        dx = sx-old_lbd[0];  dy = sy-old_lbd[1]
        for x in range(0, len(old_lbd),2):
            new_lbd.append(old_lbd[x]+dx)
            new_lbd.append(old_lbd[x+1]+dy)
        abd.lbd = new_lbd
        abd.draw_line()

    def ln_b1_click(self, event):  # b1 (left button)
        print("@ b1_click(--0--): %d objects known" % (len(self.rdg.objects)))
        self.mx, self.my = (event.x, event.y)  # Mouse position
        print("ln_b1_click(0): mx,my = %d,%d ln_mode %s <<<" % (
            self.mx,self.my, self.ln_mode))

        if self.ln_mode == "mod_end":
            print("click(1.5), mode %s" % self.ln_mode)
        else:
            item, obj = self.ln_closest(self.mx,self.my)  # Closest tk object
            if not item:  # Near non-line object, or not near existing line
                item_id = -1
                print("@b1_click(--2--): closest = None (start new line)")
                coords = [self.mx,self.my, self.mx+3,self.my+3]
                self.start_new_line(coords, self.rdg)
                    # Sets self.abd, self.lbd_id  && 1
                    # abd = (a)_line (b)eing (d)rawn
                print("    coords %s" % self.abd.lbd)
                print("b1_click, not item, mode %s" % self.ln_mode)
                self.ln_mode = "new_ln"
            else:
                item_id = item[0]  # Near existing line
                self.abd = obj.object
                self.lbd_id = self.abd.lbd_id
                self.ln_mode = "exist_ln"
                print("b1_click, near a line, mode %s" % self.ln_mode)
            self.ln_dir = self.left = self.right = self.up = self.down = False
            #print("click(2): old_line %s,  up %s, down %s, left %s, right %s" % (
            #    self.old_line, self.up, self.down, self.left, self.right))
        print("click(2.5): item_id %d, ln_mode %s" % (item_id, self.ln_mode))

        a_coords = self.abd.lbd
        print("b1_click(3): lbd %s" % a_coords)
        self.ns, self.loc = self.rel_to_line(self.mx,self.my, a_coords)
        if self.loc == 1 and self.ln_mode != "new_ln":  # Start of line
            self.ln_mode = "mod_end"
            self.modify_end(self.ns, self.mx,self.my)
        if self.loc == 2:  # End of line
            print("b1_click(): At end of line")
            if self.ln_mode == "end_seg":
                self.modify_end(self.ns, self.mx,self.my)
            else:
                self.lx0, self.ly0 = self.abd.lbd[-2:]  # Start new seg
                self.abd.lbd = self.abd.lbd + [self.mx,self.my]
                print("+++ end of line, lbd now = %s" % self.abd.lbd)
                self.ln_mode = "new_ln"
        elif self.loc == 3:  # Internal junction
            self.ln_mode = "move"
        elif self.loc == 4:  # Middle of segment
            print("ln_closest: Near middle of seg %d" % self.ns)
            self.ln_mode = "modify"
        elif self.loc == 5:  # Far from line
            print("ln_closest, far from line %d" % item_id)
            coords = [self.mx,self.my, self.mx+3,self.my+3]
            self.start_new_line(coords)  # Sets self.abd, with abd.lbd_id = 0
            print("+++ far from line, lbd now = %s" % self.abd.lbd)
            self.ln_mode = "new_ln"
        elif self.loc == 6:  # Outside last segment
            if self.ln_mode == "end_seg":
                self.modify_end(self.ns, self.mx,self.my)

        self.rdg.last_mx = self.mx;  self.rdg.last_my = self.my  # Last mouse position
    def ln_b1_motion(self, event):  # Move the current_object
        mx, my = (event.x, event.y)
        print("b1_motion(0): lbd %s, ln_mode %s" % (self.abd.lbd,self.ln_mode))
        if self.ln_mode == "mod_end":
            self.modify_end(self.ns, mx,my)
            self.abd.draw_line()
        elif self.ln_mode == "move":
            self.rdg.current_object.object.move(  # move() is in arrow_lines_class
                mx-self.rdg.last_mx, my-self.rdg.last_my)
        elif self.ln_mode == "new_ln":  # Creating a new line
            print("b1_motion(1), new_ln: lbd %s, mxy %d,%d" % (
                self.abd.lbd, mx,my))
            if not self.ln_dir:  # Just starting a segment
                #print("b1_motion(2), ln_dir F, start seg, lx,y %d,%d" % (
                #    self.lx0, self.ly0))
                dx = mx-self.lx0;  dy = my-self.ly0
                if abs(dx) >= self.d_step or abs(dy) >= self.d_step:
                    self.ln_dir = True
                    print("=== d_step reached, dx %d, dy %d" % (dx,dy))
                    if len(self.abd.lbd) > 4 and self.same_dir(mx,my):
                        print("\a>> Direction must change at a junction!")
                        self.abd.lbd = self.abd.lbd[0:-2]  # Remove new point
                        self.ln_mode = "move"
                    else:
                        self.left = self.right = self.up = self.down = False
                        if abs(dy) <= self.d_dev:  # going left or right
                            if dx < 0:
                                self.left = True
                            else:
                                self.right = True
                        elif abs(dx) <= self.d_dev: # going up or down
                            if dy < 0:
                                self.up = True
                            else:
                                self.down = True
                        print("ln_dir set: up %s, dwn %s, left %s, rght %s" % (
                            self.up, self.down, self.left, self.right))
                        self.ln_mode = "extend"
        elif self.ln_mode == "extend":
            self.x1,self.y1 = mx,my
            if self.left or self.right:
                self.y1 = self.ly0
            elif self.up or self.down:
                self.x1 = self.lx0
            self.abd.extend_line(self.x1,self.y1)
            self.abd.draw_line()  # Sets abd.lbd_id
            if self.lbd_id == 0:
                print("extend: new line started,  lbd_id now %d" % (
                    self.abd.lbd_id))
                self.rdg.dump_objects("extend:new line started")
                self.lbd_id = self.abd.lbd_id  # line id
                line_obj = self.rdg.object(
                    self.lbd_id, self.abd, "line", 0, 0, 0, 0)
                self.rdg.current_object = line_obj
                self.rdg.objects[self.lbd_id] = line_obj
        elif self.ln_mode == "modify":
            self.modify_line(self.ns, mx,my)
            self.abd.draw_line()

        self.rdg.last_mx = mx;  self.rdg.last_my = my  # Last mouse position

    def ln_b1_release(self, event):  # Left button released
        mx, my = (event.x, event.y)  # Mouse position
        mode_before = self.ln_mode
        self.ln_mode = "move"
        #print("b1_release: line now = %s" % self.abd.lbd)
        #print("b1_release() before %s, now %s" % (mode_before, self.ln_mode))
        self.rdg.last_mx = mx;  self.rdg.last_my = my  # Last mouse position
        #print("   last mx,my = %d,%d" % (self.rdg.last_mx, self.rdg.last_my))

if __name__ == "__main__":
    root = tk.Tk()  # Main window
    drawing = tk.Canvas(root, width=600, height=600, bg="white")  # Drawing area
    drawing.pack(padx=10, pady=10)
    root.mainloop()
