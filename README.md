1144, Fri  6 Jun 2025 (NZST)
1545, Sun 27 Apr 2025 (NZST)

# === rfc-draw Manual, version 3 ===

## *Getting started:*

rfc_draw is written in python3, it's license is GPL v3.0.

It uses the following python modules:
os. path, re, math, sys, time, datetime, threading, tkinter, pygame,
termios (for POSIX) or msvcrt (for Windows).
  rfc_draw wil install all these for you on startup, or
you can install them using pip (latest version),
e.g. pip3 install path

Install rfc-draw in a new folder, e.g. ~/rfc-draw.
In a terminal window, enter python3 rfc-draw.py my-drawing.rdd
*my-drawing* specifies the file that rfc-draw should write as a
record of your drawing;
after that the same command will restore that drawing to your screen.
If you don't specify a drawing file, rfc-draw will use it's default,
i.e. save-file.rdd

rfc-draw displays a single tkinter window; at the top is a white space
to draw on, below that are a set of grey (on yellow) **Mode** buttons, and a
white **Message** area.
You can resize the window by dragging (using b1, your Left mouse button)
on any of it's edges.

The **Mode** buttons tell rfc-draw what kind of objects you're currently
working on.  The modes are:

1. _Rectangle:_
   Lets you draw, resize and move rectangle objects.
   An rfc-draw Rectangle has a Text (initially just "+") at it's centre.

2. _Line:_
   Lets you draw lines as a sequence of line segments,
   with a direction arrow on each.

3. _Text:_
   Puts a text on screen, and allows you to edit and move it.
   Multi-line texts are drawn with the lines centred.

4. _Header:_
   Introduced in version 3.
   Lets you draw Header diagrams.

5. _Save:_
   Lets you write an rdd file. That saves your drawing,
but allows you to continue.
   You can edit the filename as you would a text (see below)

**Layers:**

rfc_draw (and SVG) draw their objects in successive *layers.*
Layer 1 (the lowest) contains all your lines, and is drawn first.
Layer 2 is then drawn over layer 1, it contains your rectangles.
&nbsp;&nbsp;&nbsp;This means that ends of your lines don't need to meet exactly
at rectangle edges,
&nbsp;it's easier to draw them with ends a little inside rectangles!
Layer 3 (the highest) contains your texts and headers.

When your drawing is complete, exit rfc-draw's main window (by clicking on
it's 'close' button).
rfc-draw will ask you "Save drawing as my-drawing.rdd*?"
Respond by clicking the main window's Yes or No button.

In any mode:

* The Message area displays error messages (in red),
warnings (in blue), and information messages (in black).
You can clear the Message area by pressing the Pg Dn key.

* You can *edit a text* by clicking it with b3, your Right mouse button;
that will display the text in a separate Edit Window.
You can Backspace (erasing characters), or type in new text.
* 'Command' keys perform the following actions:  
    _Home_&ensp;&ensp;&ensp;moves the edit cursor to the text's start  
    _End_&ensp;&ensp;&ensp;moves the cursor to the text's end  
    _Return_&ensp;&ensp;&ensp;starts a new line  
  
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;Esc;&ensp;puts the edited text back, and
closes the Edit Window

*Deleting objects* from your drawing:

&nbsp;Don't click on the object to select it,
that would start drawing a new object!

&nbsp;The Delete key will delete the object under (closest to) the mouse pointer.  
&nbsp;The Insert key will recover (a sequence of) recently-deleted objects.

**Rectangles:**

Press b1 down to start your rectangle, then drag it down and to the right;
that will draw a rectangle, with a text (just"+") at it's centre.

You can resize the rectangle by clicking near one of it's corners
(to expand or shrink the rectangle), or near one of it's sides
(to expand or shrink it in the direction you move that side).

You can edit the Rectangle's text by clicking on it with b3, as explained
in *edit a text* above.

**Lines:**

Lines are drawn horizontal or vertical. Press b1 down to start your line,
then drag it right, left, up or down to make your line's first *segment.*
After a first segment, add your next segment (in a different direction)
by drawing from near your last segment's end.

A line can be modified in various ways, as follows:  
&nbsp;- Dragging from middle of a segment expands/shrinks the line in the drag direction.  
&nbsp;- Dragging from start or end of line extends that segment of the line.  
&nbsp;- Dragging from any corner moves the whole line.  
&nbsp;- Dragging a single-segment line from it's middle moves it,  
&nbsp;&nbsp;&nbsp;&nbsp;dragging it from just outside an end extends it.  

**Keyboard Actions:**

In any mode:
&nbsp; key&nbsp;**c**&nbsp;to copy an rfc-draw object

In Line mode:

key&nbsp;**a**&nbsp;adds direction arrows to a line
&nbsp;&nbsp;**n**&nbsp;removes direction arrows from a line
&nbsp;&nbsp;**f**&nbsp;&nbsp;flips (inverts) a line
&nbsp;&nbsp;**r**&nbsp;&nbsp;reverses (LR to RL) a line
&nbsp;&nbsp;**=**&nbsp;&nbsp;makes both ends of a line have the same height on-screen
&nbsp;&nbsp;**e**&nbsp;&nbsp;sets Syntax End markers on a line
&nbsp;&nbsp;**b**&nbsp;&nbsp;removes Syntax End markers from a line

In Header mode (how to draw a header):

**Headers**

An rfc-draw header consists of a *Header*, with one or more *Rows* below it.
Each *Row* may contain one or more *Fields*, separated by vertical lines.
Every Field contains a Text specifying what information that field contains.

&nbsp;Click b1 to create a *Header*

A *Header* is drawn as a horizontal line, with column numbers (0 to 31)
displayed above it.
You can move a *Header* on-screen by pressing b1 down in it's column numbers;
then dragging b1 will move the whole header, together with it's *Rows*.

Now you can add a *Row* by clicking (about one column's width) below
the *Header's* bottom line.

Clicking just below a header's bottom Row will add another *Row*
Each *Row* has a series of tic marks drawn upward from it's bottom line;
every fourth tic is drawn a little wider to make it easier to select
any required column.

*Rows* are initially drawn with room for one line of text.
You can change a row's number of text lines by clicking b1 between tics
on the row's bottom line, and dragging it down or up one line.

To draw a *Field* within a *Row*, click with b1 on the tic mark to the
left of your Field's first column; this will draw a vertical bar in that
Row, with an initial Text ('X') in the centre of the new field.
Click on b3 (your right mouse button) to edit the Field's text,
and Esc when the text edit is complete.

Note that a field's text may have more than one line; *Rows* are drawn
with room (initially) for one line of text.

If you wish to delete a *Field*, double-click b1 (your left mouse button)
on the bar at the field's left.

You can change a *Field's* position in a *Row* by dragging (with b1)
left or right on the bar at the *Field's* left.
Bar movements such as this are limited to 1 column only; if you need to move it
further, you can do that as a sequence of 1-column moves.

When you have created a drawing, saved as an rdd file, you can convert it
to SVG (python3 rdd_to_svg.py),

&nbsp;python3 rdd_to_svg.py *my-drawing.rdd*  via
&nbsp;&nbsp;Creates an  SVG file,  *my-drawing.svg*

&nbsp;python3 rdd_to_ascii.py *my-drawing.rdd*
&nbsp;&nbsp;Creates an  ASCII-art file,  *my-drawing.txt*

&nbsp; python3 rdd_to_xmlfig.py *my-drawing.rdd*
&nbsp;&nbsp;Creates an svg file and a .txt file for *my-drawing.txt*,
&nbsp;&nbsp; and uses them to create a .xml file (in XML2RFC format)for *my-drawing.txt*,

&nbsp; python3 rdd_to_xmlfig.py  **-rfc**  *my-drawing.rdd*
&nbsp;&nbsp;Creates my-drawing-rfc.xml, an RFC in xml2rfc --v3 format
&nbsp;&nbsp;You can test this using the tools at https://author-tools.ietf.org/

&nbsp;&nbsp;Creates an  SVG file,  *my-drawing.svg*

&nbsp;python3 rdd_to_ascii.py *my-drawing.rdd*
&nbsp;&nbsp;Creates an  ASCII-art file,  *my-drawing.txt*

&nbsp; python3 rdd_to_xmlfig.py *my-drawing.rdd*
&nbsp;&nbsp;Creates an svg file and a .txt file for *my-drawing.txt*,
&emsp and uses them to create a .xml file (in XML2RFC format)for *my-drawing.txt*,

&nbsp; python3 rdd_to_xmlfig.py -rfc *my-drawing.rdd*
&nbsp;&nbsp;Creates my-drawing-rfc.xml, an RFC in xml2rfc --v3 format
&nbsp;&nbsp;You can test this using the tools at https://author-tools.ietf.org/

Blank borders around drawings can be set by the -p*w* option,
*w* units for svg are pixels, for ASCII-art they are chars/lines.

You can check that an svg drawing complies with RFC7996 by using
&nbsp;&nbsp;jing -c SVG-1.2-RFC *my-drawing.svg*

jing may give warning messages (about missing java apps), but
*not* getting any error messages tells you that your SVG drawing complies.

Alternatively, you can check your svg drawing using svg-check
(from https://github.com/ietf-tools/svgcheck).

   ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==
