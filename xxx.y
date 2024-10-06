len(sys.argv) 2, argv >['rfc-draw.py', 'save-qqq.rdd']<
rgdc, self.dhc_tool <draw_headers_class.draw_headers object at 0x7df3d799d120>
about to start, save_file_name save-qqq.rdd
+++ read_from_rdd: new_drawing, fn >save-qqq.rdd<
read_from_rdd: ds >root_geometry 800x600+5+5<
read_from_rdd: ds >drawing_size 784x533<
read_from_rdd: ds >mono_font width 10.333 height 17 pixels<
read_from_rdd: ds >last_mode header<
last_mode found >header<
read_from_rdd: ds >1 (header 1) [171, 161, 695, 323] "H" 0 1 0<
=+-+= ds = 1 (header 1) [171, 161, 695, 323] "H" 0 1 0 f.obj
restore_saved_object: ds >1 (header 1) [171, 161, 695, 323] "H" 0 1 0<
@@@ line = 1 (header 1) [171, 161, 695, 323] "H" 0 1 0 @@@
v2 split ['', '1', 'header', '1', '171, 161, 695, 323', 'H', '0', '1', '0', ''] len 10
fields >>> ['1', 'header', '1', '171, 161, 695, 323', 'H', '0', '1', '0'] <<< len 8
>> fields[6] >1<
restore_saved_object: o_type >header<
!!! class header: rdg <rfc_draw_globals_class.rdglob object at 0x7df3d8220df0> (<class 'rfc_draw_globals_class.rdglob'>)
<> <> h_coords [171, 161, 695, 323]
header __init__: h_nbr >1<, new_drawing False
 | | | self.rows []
 ^ ^ ^ header: h_nbr 1 (<class 'int'>)
class header: rdg.f_font >('Noto Sans Mono', 10)<, h_coords [171, 161, 695, 323], h_nbr 1
!!! !!! h_coords [171, 161, 695, 323]
=========== top line drawn ==========
in time_now: ts 0.000376
ELAPSED 0.000: hdr, top line drawn
!!!!! header: h_nbr 1
&&&  a_obj header: h_nbr 1, len(rows) 0 (<class 'draw_headers_class.draw_headers.header'>)
>< header >< self.rdg.new_drawing False, 0 rows
!!!!! header: h_nbr 1
@@ rso: h_rdo <Key 1, Object header: h_nbr 1, len(rows) 0, Type header, I_coords [171, 161, 695, 161], i_text H, parent_id 0 v1 1, v2 0>
dump_objects -- ---> restore_saved_object --
1 (header 1) [171, 161, 695, 161] "H" 0 1 0
- - dump - -
=== back from restore_object
read_from_rdd: ds >2 (row 2) [171, 161, 695, 210] "R" 1 1 2<
=+-+= ds = 2 (row 2) [171, 161, 695, 210] "R" 1 1 2 f.obj
restore_saved_object: ds >2 (row 2) [171, 161, 695, 210] "R" 1 1 2<
@@@ line = 2 (row 2) [171, 161, 695, 210] "R" 1 1 2 @@@
v2 split ['', '2', 'row', '2', '171, 161, 695, 210', 'R', '1', '1', '2', ''] len 10
fields >>> ['2', 'row', '2', '171, 161, 695, 210', 'R', '1', '1', '2'] <<< len 8
>> fields[6] >1<
restore_saved_object: o_type >row<
$$ $$ restoring row, v2 2 (<class 'int'>)
!!!!! header: h_nbr 1
RRRRR starting class row, h = header: h_nbr 1, len(rows) 0
!!!!! header: h_nbr 1
??? class row, h header: h_nbr 1, len(rows) 0, field<s = []
!!!!! header: h_nbr 1
row: h header: h_nbr 1, len(rows) 0 (<class 'draw_headers_class.draw_headers.header'>)
row header 1, x0,y0, x1,y1 171,161, 695,161
   len(h.rows) = 0
r coords = [171, 161, 695, 210], r_nbr 1
&&&  a_obj row: h_nbr 1, r_nbr 1, (<class 'draw_headers_class.draw_headers.row'>)
!!!!! header: h_nbr 1
@@@ row_obj ><Key 2, Object row: h_nbr 1, r_nbr 1,, Type row, I_coords [171, 161, 695, 210], i_text R, parent_id 1 v1 1, v2 2><, h header: h_nbr 1, len(rows) 0, h.rows >[]<
!!!!! header: h_nbr 1
@@@ appended row 1 to header header: h_nbr 1, len(rows) 1
!!!!! header: h_nbr 1
@+@ row_obj ><Key 2, Object row: h_nbr 1, r_nbr 1,, Type row, I_coords [171, 161, 695, 210], i_text R, parent_id 1 v1 1, v2 2><, h header: h_nbr 1, len(rows) 1, h.rows >[<draw_headers_class.draw_headers.row object at 0x7df3d799cf70>]<
!!!!! header: h_nbr 1
>> draw_tics h header: h_nbr 1, len(rows) 1, len(h.rows) 1, t_r_tag r_1
row_obj <Key 2, Object row: h_nbr 1, r_nbr 1,, Type row, I_coords [171, 161, 695, 210], i_text R, parent_id 1 v1 1, v2 2>
   objects[2] = <Key 2, Object row: h_nbr 1, r_nbr 1,, Type row, I_coords [171, 161, 695, 210], i_text R, parent_id 1 v1 1, v2 2>
   row 1 drawn

!!!!! header: h_nbr 1
@@ rso: r_rdo <Key 1, Object header: h_nbr 1, len(rows) 1, Type header, I_coords [171, 161, 695, 161], i_text H, parent_id 0 v1 1, v2 0>
dump_objects -- ---> restore_saved_object --
1 (header 1) [171, 161, 695, 210] "H" 0 1 0
2 (row 2) [171, 161, 695, 210] "R" 1 1 2
- - dump - -
=== back from restore_object
read_from_rdd: ds >3 (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32<
=+-+= ds = 3 (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32 f.obj
restore_saved_object: ds >3 (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32<
@@@ line = 3 (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32 @@@
v2 split ['', '3', 'field', '34', '180, 162, 689, 205', '0                   1                   2                   3  \\n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1', '2', '0', '32', ''] len 10
fields >>> ['3', 'field', '34', '180, 162, 689, 205', '0                   1                   2                   3  \\n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1', '2', '0', '32'] <<< len 8
>> fields[6] >0<
restore_saved_object: o_type >field<
!!!!! header: h_nbr 1
class field: rdg <rfc_draw_globals_class.rdglob object at 0x7df3d8220df0>, h header: h_nbr 1, len(rows) 1, r row: h_nbr 1, r_nbr 1, <><><>
~|~ r.fields: []
||||||||| self.row_id 2 (<class 'int'>)
!!!!! header: h_nbr 1
new field: self.h header: h_nbr 1, len(rows) 1 self.r row: h_nbr 1, r_nbr 1,
!!!!! header: h_nbr 1
||||||||| h_obj <Key 1, Object header: h_nbr 1, len(rows) 1, Type header, I_coords [171, 161, 695, 161], i_text H, parent_id 0 v1 1, v2 0> 
===  r_coords [171, 161, 695, 210]
>.1 field rx1,ry1 695,210 text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
===  f_coords [180, 162, 689, 205]
!!!!! header: h_nbr 1
=== set_cxy: f_clo class field: self.h header: h_nbr 1, len(rows) 1, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 (<class 'draw_headers_class.draw_headers.field'>), self.y0 162, self.y1 205
[[ set_cxy: x0 180, 434, x1 689, text >0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1<
{{ set_cxy: y0 162, 182, y1 205, text >0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1<
>.3 field fcx,fcy 434,182
DTC.restore_object: l_coords (434, 182.0), l_text >0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1<, parent_id 2, v1 0, v2 32, self.text_id None
self.text_id  now 34
&&&  a_obj 34 (<class 'int'>)
>>> 64 field.text_obj <Key 34, Object 34, Type text, I_coords (434, 182.0), i_text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, parent_id 2 v1 0, v2 32>
dump_objects -- >>> text for field created <<< --
1 (header 1) [171, 161, 695, 210] "H" 0 1 0
2 (row 2) [171, 161, 695, 210] "R" 1 1 2
3 (text 34) (434, 182.0) "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
- - dump - -
@ @ @ self.text_id 34
   text >34< cx,cy 434,182
field item's tags: ('h_1', 'r_1', 'c_0')
: : : field self type <class 'draw_headers_class.draw_headers.field'>
!!!!! header: h_nbr 1
&&&  a_obj class field: self.h header: h_nbr 1, len(rows) 1, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 (<class 'draw_headers_class.draw_headers.field'>)
dump_objects -- !!! text 34 changed to field --
1 (header 1) [171, 161, 695, 210] "H" 0 1 0
2 (row 2) [171, 161, 695, 210] "R" 1 1 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 34, Object class field: self.h header: h_nbr 1, len(rows) 1, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, Type field, I_coords (171, 161, 695, 210), i_text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, parent_id 2 v1 0, v2 32>, val.i_coords (171, 161, 695, 210)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 1, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,161, 695,210
[.1 f_clo bbox 180,162, 689,205
field's coords >[180, 162, 689, 205]<
mks field: (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
3 (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
- - dump - -
-->> r.row_id 2, r_nbr 1, fields [<draw_headers_class.draw_headers.field object at 0x7df3d8392320>]
!!!!! header: h_nbr 1
--:: field obj <Key 34, Object class field: self.h header: h_nbr 1, len(rows) 1, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, Type field, I_coords (171, 161, 695, 210), i_text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, parent_id 2 v1 0, v2 32>


dump_objects -- field's text rdo overwritten --
1 (header 1) [171, 161, 695, 210] "H" 0 1 0
2 (row 2) [171, 161, 695, 210] "R" 1 1 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 34, Object class field: self.h header: h_nbr 1, len(rows) 1, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, Type field, I_coords (171, 161, 695, 210), i_text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, parent_id 2 v1 0, v2 32>, val.i_coords (171, 161, 695, 210)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 1, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,161, 695,210
[.1 f_clo bbox 180,162, 689,205
field's coords >[180, 162, 689, 205]<
mks field: (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
3 (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
- - dump - -
!!!!! header: h_nbr 1
field_cls: .h = header: h_nbr 1, len(rows) 1
           .r = row: h_nbr 1, r_nbr 1,
!!!!! header: h_nbr 1
@@ rso: f_rdo <Key 34, Object class field: self.h header: h_nbr 1, len(rows) 1, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, Type field, I_coords (171, 161, 695, 210), i_text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, parent_id 2 v1 0, v2 32>
dump_objects -- ---> restore_saved_object --
1 (header 1) [171, 161, 695, 210] "H" 0 1 0
2 (row 2) [171, 161, 695, 210] "R" 1 1 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 34, Object class field: self.h header: h_nbr 1, len(rows) 1, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, Type field, I_coords (171, 161, 695, 210), i_text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, parent_id 2 v1 0, v2 32>, val.i_coords (171, 161, 695, 210)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 1, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,161, 695,210
[.1 f_clo bbox 180,162, 689,205
field's coords >[180, 162, 689, 205]<
mks field: (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
3 (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
- - dump - -
=== back from restore_object
read_from_rdd: ds >4 (row 35) [171, 210, 695, 259] "R" 1 2 2<
=+-+= ds = 4 (row 35) [171, 210, 695, 259] "R" 1 2 2 f.obj
restore_saved_object: ds >4 (row 35) [171, 210, 695, 259] "R" 1 2 2<
@@@ line = 4 (row 35) [171, 210, 695, 259] "R" 1 2 2 @@@
v2 split ['', '4', 'row', '35', '171, 210, 695, 259', 'R', '1', '2', '2', ''] len 10
fields >>> ['4', 'row', '35', '171, 210, 695, 259', 'R', '1', '2', '2'] <<< len 8
>> fields[6] >2<
restore_saved_object: o_type >row<
$$ $$ restoring row, v2 2 (<class 'int'>)
!!!!! header: h_nbr 1
RRRRR starting class row, h = header: h_nbr 1, len(rows) 1
!!!!! header: h_nbr 1
??? class row, h header: h_nbr 1, len(rows) 1, field<s = []
!!!!! header: h_nbr 1
row: h header: h_nbr 1, len(rows) 1 (<class 'draw_headers_class.draw_headers.header'>)
row header 1, x0,y0, x1,y1 171,161, 695,210
   len(h.rows) = 1
+++ new row at bottom, len(h.rows) 1
bottom row 171,161, 695, 210
r coords = [171, 210, 695, 259], r_nbr 2
&&&  a_obj row: h_nbr 1, r_nbr 2, (<class 'draw_headers_class.draw_headers.row'>)
!!!!! header: h_nbr 1
@@@ row_obj ><Key 35, Object row: h_nbr 1, r_nbr 2,, Type row, I_coords [171, 210, 695, 259], i_text R, parent_id 1 v1 2, v2 2><, h header: h_nbr 1, len(rows) 1, h.rows >[<draw_headers_class.draw_headers.row object at 0x7df3d799cf70>]<
!!!!! header: h_nbr 1
@@@ appended row 2 to header header: h_nbr 1, len(rows) 2
!!!!! header: h_nbr 1
@+@ row_obj ><Key 35, Object row: h_nbr 1, r_nbr 2,, Type row, I_coords [171, 210, 695, 259], i_text R, parent_id 1 v1 2, v2 2><, h header: h_nbr 1, len(rows) 2, h.rows >[<draw_headers_class.draw_headers.row object at 0x7df3d799cf70>, <draw_headers_class.draw_headers.row object at 0x7df3d82211e0>]<
!!!!! header: h_nbr 1
>> draw_tics h header: h_nbr 1, len(rows) 2, len(h.rows) 2, t_r_tag r_2
row_obj <Key 35, Object row: h_nbr 1, r_nbr 2,, Type row, I_coords [171, 210, 695, 259], i_text R, parent_id 1 v1 2, v2 2>
   objects[35] = <Key 35, Object row: h_nbr 1, r_nbr 2,, Type row, I_coords [171, 210, 695, 259], i_text R, parent_id 1 v1 2, v2 2>
   row 2 drawn

!!!!! header: h_nbr 1
@@ rso: r_rdo <Key 1, Object header: h_nbr 1, len(rows) 2, Type header, I_coords [171, 161, 695, 161], i_text H, parent_id 0 v1 1, v2 0>
dump_objects -- ---> restore_saved_object --
1 (header 1) [171, 161, 695, 259] "H" 0 1 0
2 (row 2) [171, 161, 695, 210] "R" 1 1 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 34, Object class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, Type field, I_coords (171, 161, 695, 210), i_text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, parent_id 2 v1 0, v2 32>, val.i_coords (171, 161, 695, 210)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,161, 695,210
[.1 f_clo bbox 180,162, 689,205
field's coords >[180, 162, 689, 205]<
mks field: (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
3 (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
4 (row 35) [171, 210, 695, 259] "R" 1 2 2
- - dump - -
=== back from restore_object
read_from_rdd: ds >5 (field 67) [180, 211, 305, 254] "-2-" 35 0 8<
=+-+= ds = 5 (field 67) [180, 211, 305, 254] "-2-" 35 0 8 f.obj
restore_saved_object: ds >5 (field 67) [180, 211, 305, 254] "-2-" 35 0 8<
@@@ line = 5 (field 67) [180, 211, 305, 254] "-2-" 35 0 8 @@@
v2 split ['', '5', 'field', '67', '180, 211, 305, 254', '-2-', '35', '0', '8', ''] len 10
fields >>> ['5', 'field', '67', '180, 211, 305, 254', '-2-', '35', '0', '8'] <<< len 8
>> fields[6] >0<
restore_saved_object: o_type >field<
!!!!! header: h_nbr 1
class field: rdg <rfc_draw_globals_class.rdglob object at 0x7df3d8220df0>, h header: h_nbr 1, len(rows) 2, r row: h_nbr 1, r_nbr 2, <><><>
~|~ r.fields: []
||||||||| self.row_id 35 (<class 'int'>)
!!!!! header: h_nbr 1
new field: self.h header: h_nbr 1, len(rows) 2 self.r row: h_nbr 1, r_nbr 2,
!!!!! header: h_nbr 1
||||||||| h_obj <Key 1, Object header: h_nbr 1, len(rows) 2, Type header, I_coords [171, 161, 695, 161], i_text H, parent_id 0 v1 1, v2 0> 
===  r_coords [171, 210, 695, 259]
>.1 field rx1,ry1 695,259 text -2-
===  f_coords [180, 211, 305, 254]
!!!!! header: h_nbr 1
=== set_cxy: f_clo class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 2,, self.text -2- (<class 'draw_headers_class.draw_headers.field'>), self.y0 211, self.y1 254
[[ set_cxy: x0 180, 242, x1 305, text >-2-<
{{ set_cxy: y0 211, 231, y1 254, text >-2-<
>.3 field fcx,fcy 242,231
DTC.restore_object: l_coords (242, 231.0), l_text >-2-<, parent_id 35, v1 0, v2 8, self.text_id 34
self.text_id  now 67
&&&  a_obj 67 (<class 'int'>)
>>> 64 field.text_obj <Key 67, Object 67, Type text, I_coords (242, 231.0), i_text -2-, parent_id 35 v1 0, v2 8>
dump_objects -- >>> text for field created <<< --
1 (header 1) [171, 161, 695, 259] "H" 0 1 0
2 (row 2) [171, 161, 695, 210] "R" 1 1 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 34, Object class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, Type field, I_coords (171, 161, 695, 210), i_text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, parent_id 2 v1 0, v2 32>, val.i_coords (171, 161, 695, 210)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,161, 695,210
[.1 f_clo bbox 180,162, 689,205
field's coords >[180, 162, 689, 205]<
mks field: (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
3 (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
4 (row 35) [171, 210, 695, 259] "R" 1 2 2
5 (text 67) (242, 231.0) "-2-" 35 0 8
- - dump - -
@ @ @ self.text_id 67
   text >67< cx,cy 242,231
field item's tags: ('h_1', 'r_2', 'c_0')
: : : field self type <class 'draw_headers_class.draw_headers.field'>
!!!!! header: h_nbr 1
&&&  a_obj class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 2,, self.text -2- (<class 'draw_headers_class.draw_headers.field'>)
dump_objects -- !!! text 67 changed to field --
1 (header 1) [171, 161, 695, 259] "H" 0 1 0
2 (row 2) [171, 161, 695, 210] "R" 1 1 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 34, Object class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, Type field, I_coords (171, 161, 695, 210), i_text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, parent_id 2 v1 0, v2 32>, val.i_coords (171, 161, 695, 210)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,161, 695,210
[.1 f_clo bbox 180,162, 689,205
field's coords >[180, 162, 689, 205]<
mks field: (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
3 (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
4 (row 35) [171, 210, 695, 259] "R" 1 2 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 67, Object class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, Type field, I_coords (171, 210, 695, 259), i_text -2-, parent_id 35 v1 0, v2 8>, val.i_coords (171, 210, 695, 259)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,210, 695,259
[.1 f_clo bbox 180,211, 305,254
field's coords >[180, 211, 305, 254]<
mks field: (field 67) [180, 211, 305, 254] "-2-" 35 0 8
5 (field 67) [180, 211, 305, 254] "-2-" 35 0 8
- - dump - -
-->> r.row_id 35, r_nbr 2, fields [<draw_headers_class.draw_headers.field object at 0x7df3d8220b80>]
!!!!! header: h_nbr 1
--:: field obj <Key 67, Object class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, Type field, I_coords (171, 210, 695, 259), i_text -2-, parent_id 35 v1 0, v2 8>


dump_objects -- field's text rdo overwritten --
1 (header 1) [171, 161, 695, 259] "H" 0 1 0
2 (row 2) [171, 161, 695, 210] "R" 1 1 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 34, Object class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, Type field, I_coords (171, 161, 695, 210), i_text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, parent_id 2 v1 0, v2 32>, val.i_coords (171, 161, 695, 210)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,161, 695,210
[.1 f_clo bbox 180,162, 689,205
field's coords >[180, 162, 689, 205]<
mks field: (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
3 (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
4 (row 35) [171, 210, 695, 259] "R" 1 2 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 67, Object class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, Type field, I_coords (171, 210, 695, 259), i_text -2-, parent_id 35 v1 0, v2 8>, val.i_coords (171, 210, 695, 259)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,210, 695,259
[.1 f_clo bbox 180,211, 305,254
field's coords >[180, 211, 305, 254]<
mks field: (field 67) [180, 211, 305, 254] "-2-" 35 0 8
5 (field 67) [180, 211, 305, 254] "-2-" 35 0 8
- - dump - -
!!!!! header: h_nbr 1
field_cls: .h = header: h_nbr 1, len(rows) 2
           .r = row: h_nbr 1, r_nbr 2,
!!!!! header: h_nbr 1
@@ rso: f_rdo <Key 67, Object class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, Type field, I_coords (171, 210, 695, 259), i_text -2-, parent_id 35 v1 0, v2 8>
dump_objects -- ---> restore_saved_object --
1 (header 1) [171, 161, 695, 259] "H" 0 1 0
2 (row 2) [171, 161, 695, 210] "R" 1 1 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 34, Object class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, Type field, I_coords (171, 161, 695, 210), i_text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, parent_id 2 v1 0, v2 32>, val.i_coords (171, 161, 695, 210)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,161, 695,210
[.1 f_clo bbox 180,162, 689,205
field's coords >[180, 162, 689, 205]<
mks field: (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
3 (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
4 (row 35) [171, 210, 695, 259] "R" 1 2 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 67, Object class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, Type field, I_coords (171, 210, 695, 259), i_text -2-, parent_id 35 v1 0, v2 8>, val.i_coords (171, 210, 695, 259)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 2, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,210, 695,259
[.1 f_clo bbox 180,211, 305,254
field's coords >[180, 211, 305, 254]<
mks field: (field 67) [180, 211, 305, 254] "-2-" 35 0 8
5 (field 67) [180, 211, 305, 254] "-2-" 35 0 8
- - dump - -
=== back from restore_object
read_from_rdd: ds >6 (row 68) [171, 259, 695, 291] "R" 1 3 1<
=+-+= ds = 6 (row 68) [171, 259, 695, 291] "R" 1 3 1 f.obj
restore_saved_object: ds >6 (row 68) [171, 259, 695, 291] "R" 1 3 1<
@@@ line = 6 (row 68) [171, 259, 695, 291] "R" 1 3 1 @@@
v2 split ['', '6', 'row', '68', '171, 259, 695, 291', 'R', '1', '3', '1', ''] len 10
fields >>> ['6', 'row', '68', '171, 259, 695, 291', 'R', '1', '3', '1'] <<< len 8
>> fields[6] >3<
restore_saved_object: o_type >row<
$$ $$ restoring row, v2 1 (<class 'int'>)
!!!!! header: h_nbr 1
RRRRR starting class row, h = header: h_nbr 1, len(rows) 2
!!!!! header: h_nbr 1
??? class row, h header: h_nbr 1, len(rows) 2, field<s = []
!!!!! header: h_nbr 1
row: h header: h_nbr 1, len(rows) 2 (<class 'draw_headers_class.draw_headers.header'>)
row header 1, x0,y0, x1,y1 171,161, 695,259
   len(h.rows) = 2
+++ new row at bottom, len(h.rows) 2
bottom row 171,210, 695, 259
r coords = [171, 259, 695, 291], r_nbr 3
&&&  a_obj row: h_nbr 1, r_nbr 3, (<class 'draw_headers_class.draw_headers.row'>)
!!!!! header: h_nbr 1
@@@ row_obj ><Key 68, Object row: h_nbr 1, r_nbr 3,, Type row, I_coords [171, 259, 695, 291], i_text R, parent_id 1 v1 3, v2 1><, h header: h_nbr 1, len(rows) 2, h.rows >[<draw_headers_class.draw_headers.row object at 0x7df3d799cf70>, <draw_headers_class.draw_headers.row object at 0x7df3d82211e0>]<
!!!!! header: h_nbr 1
@@@ appended row 3 to header header: h_nbr 1, len(rows) 3
!!!!! header: h_nbr 1
@+@ row_obj ><Key 68, Object row: h_nbr 1, r_nbr 3,, Type row, I_coords [171, 259, 695, 291], i_text R, parent_id 1 v1 3, v2 1><, h header: h_nbr 1, len(rows) 3, h.rows >[<draw_headers_class.draw_headers.row object at 0x7df3d799cf70>, <draw_headers_class.draw_headers.row object at 0x7df3d82211e0>, <draw_headers_class.draw_headers.row object at 0x7df3d8221180>]<
!!!!! header: h_nbr 1
>> draw_tics h header: h_nbr 1, len(rows) 3, len(h.rows) 3, t_r_tag r_3
row_obj <Key 68, Object row: h_nbr 1, r_nbr 3,, Type row, I_coords [171, 259, 695, 291], i_text R, parent_id 1 v1 3, v2 1>
   objects[68] = <Key 68, Object row: h_nbr 1, r_nbr 3,, Type row, I_coords [171, 259, 695, 291], i_text R, parent_id 1 v1 3, v2 1>
   row 3 drawn

!!!!! header: h_nbr 1
@@ rso: r_rdo <Key 1, Object header: h_nbr 1, len(rows) 3, Type header, I_coords [171, 161, 695, 161], i_text H, parent_id 0 v1 1, v2 0>
dump_objects -- ---> restore_saved_object --
1 (header 1) [171, 161, 695, 291] "H" 0 1 0
2 (row 2) [171, 161, 695, 210] "R" 1 1 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 34, Object class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, Type field, I_coords (171, 161, 695, 210), i_text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, parent_id 2 v1 0, v2 32>, val.i_coords (171, 161, 695, 210)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,161, 695,210
[.1 f_clo bbox 180,162, 689,205
field's coords >[180, 162, 689, 205]<
mks field: (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
3 (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
4 (row 35) [171, 210, 695, 259] "R" 1 2 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 67, Object class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, Type field, I_coords (171, 210, 695, 259), i_text -2-, parent_id 35 v1 0, v2 8>, val.i_coords (171, 210, 695, 259)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,210, 695,259
[.1 f_clo bbox 180,211, 305,254
field's coords >[180, 211, 305, 254]<
mks field: (field 67) [180, 211, 305, 254] "-2-" 35 0 8
5 (field 67) [180, 211, 305, 254] "-2-" 35 0 8
6 (row 68) [171, 259, 695, 291] "R" 1 3 1
- - dump - -
=== back from restore_object
read_from_rdd: ds >7 (field 100) [180, 260, 481, 286] "-3-" 68 19 32<
=+-+= ds = 7 (field 100) [180, 260, 481, 286] "-3-" 68 19 32 f.obj
restore_saved_object: ds >7 (field 100) [180, 260, 481, 286] "-3-" 68 19 32<
@@@ line = 7 (field 100) [180, 260, 481, 286] "-3-" 68 19 32 @@@
v2 split ['', '7', 'field', '100', '180, 260, 481, 286', '-3-', '68', '19', '32', ''] len 10
fields >>> ['7', 'field', '100', '180, 260, 481, 286', '-3-', '68', '19', '32'] <<< len 8
>> fields[6] >19<
restore_saved_object: o_type >field<
!!!!! header: h_nbr 1
class field: rdg <rfc_draw_globals_class.rdglob object at 0x7df3d8220df0>, h header: h_nbr 1, len(rows) 3, r row: h_nbr 1, r_nbr 3, <><><>
~|~ r.fields: []
||||||||| self.row_id 68 (<class 'int'>)
!!!!! header: h_nbr 1
new field: self.h header: h_nbr 1, len(rows) 3 self.r row: h_nbr 1, r_nbr 3,
!!!!! header: h_nbr 1
||||||||| h_obj <Key 1, Object header: h_nbr 1, len(rows) 3, Type header, I_coords [171, 161, 695, 161], i_text H, parent_id 0 v1 1, v2 0> 
===  r_coords [171, 259, 695, 291]
>.1 field rx1,ry1 695,291 text -3-
===  f_coords [484, 260, 993, 286]
!!!!! header: h_nbr 1
=== set_cxy: f_clo class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 3,, self.text -3- (<class 'draw_headers_class.draw_headers.field'>), self.y0 260, self.y1 286
[[ set_cxy: x0 484, 738, x1 993, text >-3-<
{{ set_cxy: y0 260, 271, y1 286, text >-3-<
>.3 field fcx,fcy 738,271
DTC.restore_object: l_coords (738, 271.5), l_text >-3-<, parent_id 68, v1 19, v2 32, self.text_id 67
self.text_id  now 100
&&&  a_obj 100 (<class 'int'>)
>>> 64 field.text_obj <Key 100, Object 100, Type text, I_coords (738, 271.5), i_text -3-, parent_id 68 v1 19, v2 32>
dump_objects -- >>> text for field created <<< --
1 (header 1) [171, 161, 695, 291] "H" 0 1 0
2 (row 2) [171, 161, 695, 210] "R" 1 1 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 34, Object class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, Type field, I_coords (171, 161, 695, 210), i_text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, parent_id 2 v1 0, v2 32>, val.i_coords (171, 161, 695, 210)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,161, 695,210
[.1 f_clo bbox 180,162, 689,205
field's coords >[180, 162, 689, 205]<
mks field: (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
3 (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
4 (row 35) [171, 210, 695, 259] "R" 1 2 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 67, Object class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, Type field, I_coords (171, 210, 695, 259), i_text -2-, parent_id 35 v1 0, v2 8>, val.i_coords (171, 210, 695, 259)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,210, 695,259
[.1 f_clo bbox 180,211, 305,254
field's coords >[180, 211, 305, 254]<
mks field: (field 67) [180, 211, 305, 254] "-2-" 35 0 8
5 (field 67) [180, 211, 305, 254] "-2-" 35 0 8
6 (row 68) [171, 259, 695, 291] "R" 1 3 1
7 (text 100) (738, 271.5) "-3-" 68 19 32
- - dump - -
@ @ @ self.text_id 100
   text >100< cx,cy 738,271
field item's tags: ('h_1', 'r_3', 'c_19')
: : : field self type <class 'draw_headers_class.draw_headers.field'>
!!!!! header: h_nbr 1
&&&  a_obj class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 3,, self.text -3- (<class 'draw_headers_class.draw_headers.field'>)
dump_objects -- !!! text 100 changed to field --
1 (header 1) [171, 161, 695, 291] "H" 0 1 0
2 (row 2) [171, 161, 695, 210] "R" 1 1 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 34, Object class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, Type field, I_coords (171, 161, 695, 210), i_text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, parent_id 2 v1 0, v2 32>, val.i_coords (171, 161, 695, 210)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,161, 695,210
[.1 f_clo bbox 180,162, 689,205
field's coords >[180, 162, 689, 205]<
mks field: (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
3 (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
4 (row 35) [171, 210, 695, 259] "R" 1 2 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 67, Object class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, Type field, I_coords (171, 210, 695, 259), i_text -2-, parent_id 35 v1 0, v2 8>, val.i_coords (171, 210, 695, 259)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,210, 695,259
[.1 f_clo bbox 180,211, 305,254
field's coords >[180, 211, 305, 254]<
mks field: (field 67) [180, 211, 305, 254] "-2-" 35 0 8
5 (field 67) [180, 211, 305, 254] "-2-" 35 0 8
6 (row 68) [171, 259, 695, 291] "R" 1 3 1
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 100, Object class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 3,, self.text -3-, Type field, I_coords (171, 259, 695, 291), i_text -3-, parent_id 68 v1 19, v2 32>, val.i_coords (171, 259, 695, 291)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 3,, self.text -3-, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,259, 695,291
[.1 f_clo bbox 484,260, 993,286
field's coords >[484, 260, 993, 286]<
mks field: (field 100) [484, 260, 993, 286] "-3-" 68 19 32
7 (field 100) [484, 260, 993, 286] "-3-" 68 19 32
- - dump - -
-->> r.row_id 68, r_nbr 3, fields [<draw_headers_class.draw_headers.field object at 0x7df3d8220af0>]
!!!!! header: h_nbr 1
--:: field obj <Key 100, Object class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 3,, self.text -3-, Type field, I_coords (171, 259, 695, 291), i_text -3-, parent_id 68 v1 19, v2 32>


dump_objects -- field's text rdo overwritten --
1 (header 1) [171, 161, 695, 291] "H" 0 1 0
2 (row 2) [171, 161, 695, 210] "R" 1 1 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 34, Object class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, Type field, I_coords (171, 161, 695, 210), i_text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, parent_id 2 v1 0, v2 32>, val.i_coords (171, 161, 695, 210)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,161, 695,210
[.1 f_clo bbox 180,162, 689,205
field's coords >[180, 162, 689, 205]<
mks field: (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
3 (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
4 (row 35) [171, 210, 695, 259] "R" 1 2 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 67, Object class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, Type field, I_coords (171, 210, 695, 259), i_text -2-, parent_id 35 v1 0, v2 8>, val.i_coords (171, 210, 695, 259)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,210, 695,259
[.1 f_clo bbox 180,211, 305,254
field's coords >[180, 211, 305, 254]<
mks field: (field 67) [180, 211, 305, 254] "-2-" 35 0 8
5 (field 67) [180, 211, 305, 254] "-2-" 35 0 8
6 (row 68) [171, 259, 695, 291] "R" 1 3 1
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 100, Object class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 3,, self.text -3-, Type field, I_coords (171, 259, 695, 291), i_text -3-, parent_id 68 v1 19, v2 32>, val.i_coords (171, 259, 695, 291)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 3,, self.text -3-, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,259, 695,291
[.1 f_clo bbox 484,260, 993,286
field's coords >[484, 260, 993, 286]<
mks field: (field 100) [484, 260, 993, 286] "-3-" 68 19 32
7 (field 100) [484, 260, 993, 286] "-3-" 68 19 32
- - dump - -
!!!!! header: h_nbr 1
field_cls: .h = header: h_nbr 1, len(rows) 3
           .r = row: h_nbr 1, r_nbr 3,
!!!!! header: h_nbr 1
@@ rso: f_rdo <Key 100, Object class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 3,, self.text -3-, Type field, I_coords (171, 259, 695, 291), i_text -3-, parent_id 68 v1 19, v2 32>
dump_objects -- ---> restore_saved_object --
1 (header 1) [171, 161, 695, 291] "H" 0 1 0
2 (row 2) [171, 161, 695, 210] "R" 1 1 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 34, Object class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, Type field, I_coords (171, 161, 695, 210), i_text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, parent_id 2 v1 0, v2 32>, val.i_coords (171, 161, 695, 210)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,161, 695,210
[.1 f_clo bbox 180,162, 689,205
field's coords >[180, 162, 689, 205]<
mks field: (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
3 (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
4 (row 35) [171, 210, 695, 259] "R" 1 2 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 67, Object class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, Type field, I_coords (171, 210, 695, 259), i_text -2-, parent_id 35 v1 0, v2 8>, val.i_coords (171, 210, 695, 259)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,210, 695,259
[.1 f_clo bbox 180,211, 305,254
field's coords >[180, 211, 305, 254]<
mks field: (field 67) [180, 211, 305, 254] "-2-" 35 0 8
5 (field 67) [180, 211, 305, 254] "-2-" 35 0 8
6 (row 68) [171, 259, 695, 291] "R" 1 3 1
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 100, Object class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 3,, self.text -3-, Type field, I_coords (171, 259, 695, 291), i_text -3-, parent_id 68 v1 19, v2 32>, val.i_coords (171, 259, 695, 291)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 3, self.r row: h_nbr 1, r_nbr 3,, self.text -3-, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,259, 695,291
[.1 f_clo bbox 484,260, 993,286
field's coords >[484, 260, 993, 286]<
mks field: (field 100) [484, 260, 993, 286] "-3-" 68 19 32
7 (field 100) [484, 260, 993, 286] "-3-" 68 19 32
- - dump - -
=== back from restore_object
read_from_rdd: ds >8 (row 101) [171, 291, 695, 323] "R" 1 4 1<
=+-+= ds = 8 (row 101) [171, 291, 695, 323] "R" 1 4 1 f.obj
restore_saved_object: ds >8 (row 101) [171, 291, 695, 323] "R" 1 4 1<
@@@ line = 8 (row 101) [171, 291, 695, 323] "R" 1 4 1 @@@
v2 split ['', '8', 'row', '101', '171, 291, 695, 323', 'R', '1', '4', '1', ''] len 10
fields >>> ['8', 'row', '101', '171, 291, 695, 323', 'R', '1', '4', '1'] <<< len 8
>> fields[6] >4<
restore_saved_object: o_type >row<
$$ $$ restoring row, v2 1 (<class 'int'>)
!!!!! header: h_nbr 1
RRRRR starting class row, h = header: h_nbr 1, len(rows) 3
!!!!! header: h_nbr 1
??? class row, h header: h_nbr 1, len(rows) 3, field<s = []
!!!!! header: h_nbr 1
row: h header: h_nbr 1, len(rows) 3 (<class 'draw_headers_class.draw_headers.header'>)
row header 1, x0,y0, x1,y1 171,161, 695,291
   len(h.rows) = 3
+++ new row at bottom, len(h.rows) 3
bottom row 171,259, 695, 291
r coords = [171, 291, 695, 323], r_nbr 4
&&&  a_obj row: h_nbr 1, r_nbr 4, (<class 'draw_headers_class.draw_headers.row'>)
!!!!! header: h_nbr 1
@@@ row_obj ><Key 102, Object row: h_nbr 1, r_nbr 4,, Type row, I_coords [171, 291, 695, 323], i_text R, parent_id 1 v1 4, v2 1><, h header: h_nbr 1, len(rows) 3, h.rows >[<draw_headers_class.draw_headers.row object at 0x7df3d799cf70>, <draw_headers_class.draw_headers.row object at 0x7df3d82211e0>, <draw_headers_class.draw_headers.row object at 0x7df3d8221180>]<
!!!!! header: h_nbr 1
@@@ appended row 4 to header header: h_nbr 1, len(rows) 4
!!!!! header: h_nbr 1
@+@ row_obj ><Key 102, Object row: h_nbr 1, r_nbr 4,, Type row, I_coords [171, 291, 695, 323], i_text R, parent_id 1 v1 4, v2 1><, h header: h_nbr 1, len(rows) 4, h.rows >[<draw_headers_class.draw_headers.row object at 0x7df3d799cf70>, <draw_headers_class.draw_headers.row object at 0x7df3d82211e0>, <draw_headers_class.draw_headers.row object at 0x7df3d8221180>, <draw_headers_class.draw_headers.row object at 0x7df3d8220eb0>]<
!!!!! header: h_nbr 1
>> draw_tics h header: h_nbr 1, len(rows) 4, len(h.rows) 4, t_r_tag r_4
row_obj <Key 102, Object row: h_nbr 1, r_nbr 4,, Type row, I_coords [171, 291, 695, 323], i_text R, parent_id 1 v1 4, v2 1>
   objects[102] = <Key 102, Object row: h_nbr 1, r_nbr 4,, Type row, I_coords [171, 291, 695, 323], i_text R, parent_id 1 v1 4, v2 1>
   row 4 drawn

!!!!! header: h_nbr 1
@@ rso: r_rdo <Key 1, Object header: h_nbr 1, len(rows) 4, Type header, I_coords [171, 161, 695, 161], i_text H, parent_id 0 v1 1, v2 0>
dump_objects -- ---> restore_saved_object --
1 (header 1) [171, 161, 695, 323] "H" 0 1 0
2 (row 2) [171, 161, 695, 210] "R" 1 1 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 34, Object class field: self.h header: h_nbr 1, len(rows) 4, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, Type field, I_coords (171, 161, 695, 210), i_text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, parent_id 2 v1 0, v2 32>, val.i_coords (171, 161, 695, 210)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 4, self.r row: h_nbr 1, r_nbr 1,, self.text 0                   1                   2                   3  
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,161, 695,210
[.1 f_clo bbox 180,162, 689,205
field's coords >[180, 162, 689, 205]<
mks field: (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
3 (field 34) [180, 162, 689, 205] "0                   1                   2                   3  \n0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1" 2 0 32
4 (row 35) [171, 210, 695, 259] "R" 1 2 2
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 67, Object class field: self.h header: h_nbr 1, len(rows) 4, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, Type field, I_coords (171, 210, 695, 259), i_text -2-, parent_id 35 v1 0, v2 8>, val.i_coords (171, 210, 695, 259)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 4, self.r row: h_nbr 1, r_nbr 2,, self.text -2-, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,210, 695,259
[.1 f_clo bbox 180,211, 305,254
field's coords >[180, 211, 305, 254]<
mks field: (field 67) [180, 211, 305, 254] "-2-" 35 0 8
5 (field 67) [180, 211, 305, 254] "-2-" 35 0 8
6 (row 68) [171, 259, 695, 291] "R" 1 3 1
!!!!! header: h_nbr 1
FIELD mk_save_str: val <Key 100, Object class field: self.h header: h_nbr 1, len(rows) 4, self.r row: h_nbr 1, r_nbr 3,, self.text -3-, Type field, I_coords (171, 259, 695, 291), i_text -3-, parent_id 68 v1 19, v2 32>, val.i_coords (171, 259, 695, 291)
!!!!! header: h_nbr 1
mk_s_s: f_clo class field: self.h header: h_nbr 1, len(rows) 4, self.r row: h_nbr 1, r_nbr 3,, self.text -3-, type <class 'draw_headers_class.draw_headers.field'>
@|@|@ i_coords 171,259, 695,291
[.1 f_clo bbox 484,260, 993,286
field's coords >[484, 260, 993, 286]<
mks field: (field 100) [484, 260, 993, 286] "-3-" 68 19 32
7 (field 100) [484, 260, 993, 286] "-3-" 68 19 32
8 (row 102) [171, 291, 695, 323] "R" 1 4 1
- - dump - -
=== back from restore_object
read_from_rdd: ds >9 (field 133) [180, 292, 689, 318] "-4-" 101 0 32<
=+-+= ds = 9 (field 133) [180, 292, 689, 318] "-4-" 101 0 32 f.obj
restore_saved_object: ds >9 (field 133) [180, 292, 689, 318] "-4-" 101 0 32<
@@@ line = 9 (field 133) [180, 292, 689, 318] "-4-" 101 0 32 @@@
v2 split ['', '9', 'field', '133', '180, 292, 689, 318', '-4-', '101', '0', '32', ''] len 10
fields >>> ['9', 'field', '133', '180, 292, 689, 318', '-4-', '101', '0', '32'] <<< len 8
>> fields[6] >0<
restore_saved_object: o_type >field<
