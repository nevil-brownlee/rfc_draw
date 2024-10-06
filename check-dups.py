# 1045, Tue  2 Jan 2024 (NZDT)
#
# check-dups.py

import sys

l_dict = {}
f_name = sys.argv[1]
#print("f_name %s" % f_name)
prev_line = ""

f = open(f_name, "r")
for ln,line in enumerate(f):
    ls = line.strip()
    if len(ls) != 0:
        #print("+++ line >%s<" % ls)
        if ls in l_dict:
            if not(ls in ["#", '"""', "else:"]): #and \
                    #("if obj_type ==" not in ls) and \
                    #("if obj.o_type ==" not in ls):
                #print("prev_line >%s<" % prev_line)
                flag = ""
                if "def " in line:
                    flag = "<<<"
                print("line %d is also at %d %s" % (ln+1, l_dict[ls], flag))
                    #  ln+1 to match emacs line numbering
                for k,v in l_dict.items():
                #    print("k >%s< v >%s<" % (k,v))
                    if k == prev_line:
                        print("prev+line >%s< is at %s" % v)
                        exit()
        else:
            l_dict[ls] = ln+1
    prev_line = line




