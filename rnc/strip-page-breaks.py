# 1511, Wed 13 Sep 2023 (NZST)
#
# strip-page-breaks.py:
#   Given file SVG-1.2-RFC.rnc, taken from RFC 7996,
#     strip out the 8 lines (3 blank, trailer, ^L, 2 blank) between pages
#
# Copyright 2023, Nevil Brownlee, Taupo NZ

def page_break(ln, lbuf):
    empty_lines = 0
    has_rfc = has_ff = has_page = False
    page_li = -1
    for j in range(0,8):
        ls = lbuf[j]
        if len(ls) == 0:
            empty_lines += 1
        if ls.find("Page") >= 0:
            has_page = True
            page_li = j
        if ls == "\x0c":
            has_ff = True
        if  ls.startswith("RFC 7996"):
            has_rfc = True
        
    #print("%4i  empty %d,  has RFC 7996 %s, has_ff %s, has_page %s" % (
    #    ln, empty_lines, has_rfc, has_ff, has_page))

    return page_li, has_rfc and has_ff and has_page and empty_lines == 5
        # print("@@@@@@@@@@@@@@@@@ page break in lbuf")

f = open("SVG-1.2-RFC.rnc", "r")
tf = open("tweaked.rnc", "w")
lbuf = [" "]*8
ln = 0
li = lines_in_buf = 0  # Start filling buffer
for line in f:
    print("%6i %6i >%s< len %d" % (li, ln, lbuf[li], lines_in_buf))
    if lines_in_buf < 8:  # Filling lbuf
        print("--- filling")
        lbuf[li] = line.rstrip('\n')
        print("lbuf[%d] >%s<" % (li, lbuf[li]))
        li = (li+1)%8;  lines_in_buf += 1
    else:  # Passing lines through lbuf
        pg_li, pb = page_break(ln, lbuf)
        if pb:
            print("========= page break, pg_li %i ===========" % pg_li)
            li = lines_in_buf = 0  # Discard page-break lines
            lbuf[li] = line.rstrip('\n')
            print("lbuf[%d] >%s<" % (li, lbuf[li]))
            li = (li+1)%8;  lines_in_buf += 1  # Save current line
        elif line.find(" End of SVG 1.2") > 0:
            for j in range(0,8):
                print("j %d >%s<" % (j,lbuf[j]))
            print("li = %d" % li)
            break
        else:
            tf.write(lbuf[li]+"\n")  # Write line about to be replaced
            lbuf[li] = line.rstrip('\n')
            li = (li+1)%8
    ln += 1
    #if ln >= 120:
    #    exit()

while(lines_in_buf != 0):
    tf.write(lbuf[(li) % 8]+"\n")  # Empty lbuf
    li = (li+1)%8
    lines_in_buf -= 1
tf.close()
