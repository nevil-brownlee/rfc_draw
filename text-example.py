import svgwrite

svg_document = svgwrite.Drawing(filename = "test-svgwrite.svg",
                                size = (250, 100),  # (white) svg drawing space
                                font_family="monospace", font_size='17')

svg_document.add(svg_document.rect(insert = (20, 20),  # px
                                   size = (200, 50),
                                   stroke_width = "1",
                                   stroke = "blue", fill="lightpink"))
                                   #fill = "rgb(255,255,0)"))

svg_document.add(svg_document.text("0                   1                   2",
                                   insert = (0,'17')))
svg_document.add(svg_document.text("0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0",
                                   insert = (0,'36')))
svg_document.add(svg_document.text("Segment List[n] (128-bit IPv6 address)",
                                   insert = (0,'53')))
print(svg_document.tostring())

svg_document.save()
