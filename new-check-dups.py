# 1045, Tue  2 Jan 2024 (NZDT)
#
# check-dups.py

import sys

l_dict = {}
f_name = sys.argv[1]
#print("f_name %s" % f_name)

f = open(f_name, "r")
for ln,line in enumerate(f):
    ls = line.strip()
    #print("line %d: >%s< (%d)" % (ln, ls, len(ls)))
    if len(ls) != 0:
        #print("+++ line >%s<" % ls)
        if ls in l_dict:
            if ls != "#" and ls != '"""':
                flag = ""
                if "def " in line:
                    flag = "<<<"
                    print("line %d is also at %d %s" % (ln+1, l_dict[ls], flag))
                    #  ln+1 to match emacs line numbering
            """                                      
            l_dict[ls] = ln+1
            for k,v in l_dict.items():
                #print("k >%s< v >%s<" % (k,v))
                if v == prev_line:
                    print("prev_line >%s< is at %s" % v)

            prev_line = ls
            """
             
"""
Another check woud be to see if lines before/ahead of dup line are also at
the other found point within the file.
We have ln = {line contents}:  ln[line] -> line's nbr in file

We need a low-overhead way to get nth record from file
"""
