# 1529, Thu 26 Oct 2023 (NZDT)
#
# rdd-to-xmlfig.py: Convert an rfc-draw .rdd file to an XML2RFC <figure>:
#   via an svg image that conforms to RFC 7996 requirements
#
# Copyright 2023, Nevil Brownlee, Taupo NZ

import sys, re, math, svgwrite

class xmlfig_drawing:
    def __init__(self, rdd_fn, asc_b_w, svg_b_w):
                               # *b_w may be integer or None
        print("rdd_fn %s, asc %s, svg %s" % (rdd_fn, asc_b_w, svg_b_w))

        rdd_to_ascii = __import__("rdd_to_ascii")
        if asc_b_w:
            ascii_obj = rdd_to_ascii.asc_drawing(["dummy", rdd_fn, asc_b_w])
        else:
            ascii_obj = rdd_to_ascii.asc_drawing(["dummy", rdd_fn])
        print(">>> ascii_obj >%s<" % ascii_obj)
        print("ascii:")
        print("   rdd_fn = %s, border_width %d" % (
            ascii_obj.rdd_fn, ascii_obj.border_width))

        rdd_to_svg = __import__("rdd_to_svg")
        if svg_b_w:
            svg_obj = rdd_to_svg.svg_drawing(["dummy", rdd_fn, svg_b_w])
        else:
            svg_obj = rdd_to_svg.svg_drawing(["dummy", rdd_fn])
        print(">>> svg_obj >%s<" % svg_obj)
        print("svg:")
        print("   rdd_fn = %s, border_width %d" % (
            svg_obj.rdd_fn, svg_obj.border_width))

if __name__ == "__main__":
    asc_b_w = svg_b_w = None  # Use default border widths
    if len(sys.argv) == 1:  # sys_argv[0] = name of program 
        print("No .rdd file specified ???")
        from tkinter.filedialog import askopenfilename
        rdd_fn = (askopenfilename(title="Select .rdd source file"))
    else:
        rdd_fn = sys.argv[1]

    # arg   0       1       2        3
    #  prog_name  rdd_fn  asc_b_w  svg_b_w  # Both b_ws speified
    #  prog_name  rdd_fn  # Use defaults for both

    if len(sys.argv) >= 3:
        if len(sys.argv) < 4:
            print("expected border_widths for both ascii and svg!")
            exit()
        asc_b_w = sys.argv[2]; svg_b_w = sys.argv[3]
    print("++ rdd_name %s, asc_b_w %s, svg_b_w %s" % (
        rdd_fn, asc_b_w, svg_b_w))

    xmlfig_drawing(rdd_fn, asc_b_w, svg_b_w)
    
    rdd_name = rdd_fn.split(".")[0]
    xmlfig_name = rdd_name + ".xml"
    xf = open(xmlfig_name, "w")
    xf.write("<figure anchor=\"TBD\">\n")
    xf.write("  <name>TBD</name>\n")
    xf.write("  <artset>\n")
    xf.write("    <artwork align=\"left\" type=\"ascii-art\">\n")
    xf.write("      <![CDATA[\n")
    xf.write("      <!-- ASCII text goes here -->\n")
    af = open(rdd_name+".txt", "r")  # Copy ascii version
    for line in af:
        xf.write(line)
    af.close()
    xf.write("      ]]>\n")
    xf.write("    </artwork>\n")
    xf.write("    <artwork align=\"center\" type=\"svg\">\n")
    sf = open(rdd_name+".svg", "r")  # Copy ascii version
    for line in sf:
        xf.write(line)
    sf.close()
    xf.write("      </svg>\n")
    xf.write("    </artwork>\n")
    xf.write("  </artset>\n")
    xf.write("</figure>\n")
    xf.close()
