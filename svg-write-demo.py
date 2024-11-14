import svgwrite

dwg = svgwrite.Drawing('svgwrite-example.svg', profile='tiny')

# draw a red box
dwg.add(dwg.rect((10, 10), (300, 200),
    stroke=svgwrite.rgb(10, 10, 16, '%'),
    fill='red')
)

# Draw a small white circle in the top left of box
dwg.add(dwg.circle(center=(25,25),
    r=10,
    stroke=svgwrite.rgb(15, 15, 15, '%'),
    fill='white')
)

# Label this box #1
dwg.add(dwg.text('1',
    insert=(21,30),
    stroke='none',
    fill=svgwrite.rgb(15, 15, 15, '%'),
    font_size='15px',
    font_weight="bold")
)

# Draw some text demonstrating font_size, font_family, font_weight, font_color
dwg.add(dwg.text('ABC',
    insert=(55,125),
    stroke='none',
    fill='#900',
    font_size='90px',
    font_weight="bold",
    font_family="monospace")
)

# Draw some text demonstrating font stroke color
dwg.add(dwg.text('12345',
    insert=(50,180),
    stroke='#500',
    fill='#A90690',
    stroke_width=2,
    font_size='66px',
    font_weight="normal",
    font_family="monospace")
)

# white text over red box
dwg.add(dwg.text('rectangle w/ black stroke & red fill',
    insert=(40, 40),
    fill='white')
)

# draw a nofill box
dwg.add(dwg.rect((10, 220), (300, 190),
    stroke=svgwrite.rgb(10, 10, 16, '%'),
    fill='none')
)

# black text over nofill box
dwg.add(dwg.text('rectangle w/ black stroke & no fill',
    insert=(40, 250),
    fill='black')
)

# Draw a small white circle in the top left of box
dwg.add(dwg.circle(center=(26,235),
    r=10,
    stroke=svgwrite.rgb(15, 15, 15, '%'),
    fill='#eeeeee')
)

# Label this box #2
dwg.add(dwg.text('2',
    insert=(22,240),
    stroke='none',
    fill=svgwrite.rgb(15, 15, 15, '%'),
    font_size='15px',
    font_weight="bold")
)
