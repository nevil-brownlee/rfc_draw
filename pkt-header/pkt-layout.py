
import svgwrite  # Modified svgwrite/drawing.py to not set xmlns:ev !!!

class packet_layout:
    def __init__(self, svg_filename, lines, font_size):
        self.border = 2
        self.family = 'sans-serif'
        self.font_height = font_size;  self.font_width = font_size*0.6
        self.xmargin = font_size/10.0  # Margin either side of text
        self.tmargin = self.xmargin*3  # Margin above text
        self.bmargin = self.xmargin*6  # Margin below text
        self.cell_width = 2*self.xmargin + 2*self.font_width  # cols 0..31
        self.cell_height = self.tmargin + self.font_height + self.bmargin
        self.dwg = svgwrite.Drawing(filename=svg_filename,
            profile='tiny', version='1.2',
            size=(32*self.cell_width + 2*self.border,
                (lines+1)*self.cell_height + 2*self.border))

    def col_centre(self, x):
        return self.border + x*self.cell_width + self.cell_width/2.0

    def heading(self):
        hy = self.border + self.tmargin + self.font_height
        for x in range(0,32):
            self.dwg.add(self.dwg.text("%s" % x, font_family=self.family,
                font_size=self.font_height*0.8, text_anchor="middle",
                insert=(self.col_centre(x), hy) ))
        self.top = hy + self.bmargin
        self.last_row = 0

    def field(self, text, row, fcol,lcol, font_size=None):
            # Field test in fcol..lcol of line row
        if font_size == None:
            font_size = self.font_height
        self.bottom = self.top + (row+1)*self.cell_height
        cx = self.col_centre((lcol+fcol)/2.0)
        self.dwg.add(self.dwg.text(text, font_family=self.family,
            font_size=font_size, text_anchor="middle",
            insert=(cx, self.bottom-self.bmargin) ))
        if fcol != 0:
            self.dwg.add(self.dwg.line(
                start=(fcol*self.cell_width+self.border,
                    self.bottom-self.cell_height),
                end=(self.border+fcol*self.cell_width, self.bottom),
                stroke="black", stroke_width=1))
        if row != self.last_row:
            last_bottom = self.bottom-self.cell_height
            self.dwg.add(self.dwg.line(
                start=(self.border, last_bottom),
                end=(self.border+32*self.cell_width, last_bottom),
                stroke="black", stroke_width=1))
        self.last_row = row

    def draw_frame(self):
        self.dwg.add(self.dwg.rect(
            insert=(self.border, self.top),  # upper left
            size=(32*self.cell_width, self.bottom-self.top),
            stroke='black', fill="none", stroke_width=1))

#    def col_markers(self, y):
#        for x in range(0, 32):
#            cc = self.col_centre(x)
#            self.dwg.add(dwg.line(
#               start=(cc, y*self.cell_height),
#               end=(cc, (y+1)*self.cell_height),
#               stroke="black", stroke_width=1))
#        self.dwg.add(dwg.rect(insert=(0,y*self.cell_height),  # upper left
#            size=(32*self.cell_width, self.cell_height),
#            stroke='red', fill="none" ))
#pl.col_markers(1)

pl = packet_layout("tcp-header.svg", 7, 20)  # 7 lines, Font height 20px

pl.heading()  # Column numbers

pl.field("Source Port", 0, 0,15)  # Name, row, from, to
pl.field("Destination Port", 0, 16,31)
pl.field("Sequence Number", 1, 0,31)
pl.field("Acknowledgement Number", 2, 0,31)
pl.field("Data Offset", 3, 0,3)
pl.field("Reserved", 3, 4,9)
pl.field("Urg", 3, 10,10, 14)  # 14ps font to make the flags fit
pl.field("Ack", 3, 11,11, 14)
pl.field("Psh", 3, 12,12, 14)
pl.field("Rst", 3, 13,13, 14)
pl.field("Syn", 3, 14,14, 14)
pl.field("Fin", 3, 15,15, 14)
pl.field("Window", 3, 16,31)
pl.field("Checksum", 4, 0,15)
pl.field("Urgent Pointer", 4, 16,31)
pl.field("Options", 5, 0,23)
pl.field("Padding", 5, 24,31)
pl.field("Data", 6, 0,31)

pl.draw_frame()  # Finish the surrounding frame


'''
    0                   1                   2                   3   
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |          Source Port          |       Destination Port        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                        Sequence Number                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Acknowledgment Number                      |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  Data |           |U|A|P|R|S|F|                               |
   | Offset| Reserved  |R|C|S|S|Y|I|            Window             |
   |       |           |G|K|H|T|N|N|                               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |           Checksum            |         Urgent Pointer        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Options                    |    Padding    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                             data                              |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

                            TCP Header Format
From RFC 793

dwg.add(dwg.rect(insert = (0, 0),
                                   size = ("200px", "100px"),
                                   stroke_width = "1",
                                   stroke = "black",
                                   fill = "rgb(255,255,0)"))

dwg.add(dwg.text("Hello World",
                                   insert = (210, 110)))
'''

#print(pl.dwg.tostring())

pl.dwg.save()

