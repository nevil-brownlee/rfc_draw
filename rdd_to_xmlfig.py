# 1529, Thu 26 Oct 2023 (NZDT)
#
# rdd_to_xmlfig.py: Convert an rfc-draw .rdd file to an XML2RFC <figure>:
#   via an svg image that conforms to RFC 7996 requirements
#
# Copyright 2023, Nevil Brownlee, Taupo NZ

import sys, re, math, svgwrite
import debug_print_class as dbpc
dbp = dbpc.dp_env(False)  # debug printing off

class xmlfig_drawing:
    def __init__(self, rdd_fn, asc_b_w, svg_b_w):
                               # *b_w may be integer or None
        dbp.db_print("-4- rdd_fn %s, asc %s, svg %s" % (
            rdd_fn, asc_b_w, svg_b_w))

        rdd_to_ascii = __import__("rdd_to_ascii")
        if asc_b_w:
            ascii_obj = rdd_to_ascii.asc_drawing(["dummy", rdd_fn, asc_b_w])
        else:
            ascii_obj = rdd_to_ascii.asc_drawing(["dummy", rdd_fn])
        dbp.db_print("-1- >>> ascii_obj >%s<" % ascii_obj)
        dbp.db_print("ascii:")
        dbp.db_print("   rdd_fn = %s, border_width %d" % (
            ascii_obj.rdd_fn, ascii_obj.bw))

        rdd_to_svg = __import__("rdd_to_svg")
        if svg_b_w:
            svg_obj = rdd_to_svg.svg_drawing(["dummy", rdd_fn, svg_b_w])
        else:
            svg_obj = rdd_to_svg.svg_drawing(["dummy", rdd_fn])
        dbp.db_print("-2- >>> svg_obj >%s<" % svg_obj)
        dbp.db_print("svg:")
        dbp.db_print("   rdd_fn = %s, border_width %d" % (
            svg_obj.rdd_fn, svg_obj.bw))

if __name__ == "__main__":  # Executing rdd_to_xmlfig.py
    asc_b_w = svg_b_w = None  # Use default border widths
    if len(sys.argv) < 2:  # sys_argv[0] = name of program 
        print("No .rdd file specified ???")
        from tkinter.filedialog import askopenfilename
        rdd_fn = (askopenfilename(title="Select .rdd source file"))
    else:
        print(">>> sys.argv %s" % sys.argv)
        rdd_fn = sys.argv[1]
    print("rdd_fn %s" % rdd_fn)
    ##  >>['rdd_to_xmlfig.py', '-rfc', 'test-rectangle.rdd']<<

    # arg   0       1      2       3        4
    #  prog_name  rdd_fn      # Use defaults for both b_ws, make .xml file
    #  prog_name  rdd_fn asc_b_w  svg_b_w  # Both b_ws specified
    #  prog_name  rdd_fn *rfc # Use defaults for both b_ws, make -rfc.xml file
    #  prog_name  rdd_fn *rfc asc_b_w  svg_b_w  # Ditto
    #               -rfc is an rdd_to_xmlfig (not a python3) option! <<<

    b_ws = [];  rtx_params = sys.argv[1:]
    if len(sys.argv) >= 2:
        #         0              1            2              3    4
        # 'rdd_to_xmlfig.py', '-rfc', 'test-rectangle.rdd', '2', '5']
        # 'rdd_to_xmlfig.py', 'test-rectangle.rdd',  '2',   '5']
        #
        print(">>%s<< rdd_fn %s" % (sys.argv, rdd_fn))

        mk_rfc = False
        if rtx_params[0] == "-rfc":
            rtx_params = rtx_params[1:]
            print("**rtx_params: %s" % rtx_params)
            xmlfig_name = rtx_params[0][0:-4] + "-rfc.xml"
            print("Will generate test rfc: %s" % xmlfig_name)
            mk_rfc = True
        else:
            rdd_fn = rtx_params[0]
            xmlfig_name = rdd_fn[0:-4] + ".xml"
            print("Will generate xml figure: %s" % xmlfig_name)
        dbp.db_print("-0- rtx_params >%s<" % rtx_params)

    print("- - - rdd_fn >%s<, b_ws >%s<, mk_rfc %s" % (rdd_fn, b_ws, mk_rfc))
    dbp.db_print("-1- rtx_params >%s<" % rtx_params)
    if len(rtx_params) >= 3:
        asc_b_w = rtx_params[1]; svg_b_w = rtx_params[2]
        print("++ rdd_name %s, asc_b_w %s, svg_b_w %s" % (
            rdd_fn, asc_b_w, svg_b_w))
    elif len(b_ws) == 2:
        print("expected border_widths for both ascii and svg!")
        exit()
    else:
        print("Using default border_widths for both ascii and svg!")

    xf = open(xmlfig_name, "w")
    dbp.db_print("-2- rdd_fn %s, asc %s, svg %s" % (
        rdd_fn, asc_b_w, svg_b_w))

    rdd_fn = rtx_params[0]
    xmlfig_drawing(rdd_fn, asc_b_w, svg_b_w)
    skel_file = open("xml_fig_skel.xml", "r")
    ln = 0
    for skel_ln in skel_file:
        ln += 1
        #dbp.db_print("+++ %4d %s" % (ln, skel_ln))
        if not ("@@@ xmlfig figure to be tested" in skel_ln):
            xf.write(skel_ln)  # Copy skel line to xmlfig file
        else:
            break

    xf.write("<figure anchor=\"TBD\">\n")
    xf.write("  <name>TBD</name>\n")
    xf.write("  <artset>\n")
    xf.write("    <artwork align=\"left\" type=\"ascii-art\">\n")
    xf.write("      <![CDATA[\n")
    #dbp.db_print("??? rdd_fn >%s<" % rdd_fn)
    af = open(rdd_fn[0:-4]+".txt", "r")  # Copy ascii version
    for line in af:
        xf.write("%s" % line)
    af.close()
    xf.write("      ]]>\n")
    xf.write("    </artwork>\n")
    xf.write("    <artwork align=\"center\" type=\"svg\">\n")
    sf = open(rdd_fn[0:-4]+".svg", "r")  # Copy ascii version
    for line in sf:
        xf.write(line)
    sf.close()
            #xf.write("      </svg>\n")  # The .svg file ends with </svg>
    xf.write("    </artwork>\n")
    xf.write("  </artset>\n")
    xf.write("</figure>\n")
    ###xf.close()

    for skel_ln in skel_file:
        xf.write(skel_ln)  # Copy rest of skel file to xmlfig file
    skel_file.close()


#https://authors.ietf.org/ -> https://author-tools.ietf.org/
