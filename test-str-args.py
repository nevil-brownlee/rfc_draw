
s = "<Key %s, Object %s, Type %s, I_coords %s, "
s += "i_text %s, parent_id %s v1 %s, v2 %s>"
print("->> object str() s = %s" % s)
key = "k"
obj = "o"
o_type = "t"
i_coords = "ic"
i_text = "it"
parent_id = "pid"
v1 = "v1"
v2 = "v2"

rs = s % (key, obj, o_type, i_coords, i_text, parent_id, v1, v2)
print("->> object str() rs = %s" % rs)
