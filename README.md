## RFC-Draw
### A simple drawing package to make SVG and ASCII-art diagrams for RFCs 

RFC-draw is a python tkinter-based drawing system, with three components: 

* _rfc-draw.py_ - interactive drawing program to create on-screen diagrams,   
   &emsp; and save them to rfc-draw-data (.rdd) files  

* _rdd-to-svg.py_ - creates a drawing's SVG file that conforms to the RFC7996 SVG schema  

* _rdd-to-ascii.py_ - creates a drawing's ASCII-art (.txt) file  

rfc-draw.py let's you draw (with your mouse) three kinds of objects, 
in three layers, with restrictions to allow for ASCII-art:  

1. Lines  
   &emsp; Lines have one or more segments; 
   each segment must be either horizontal or vertical. 
 
2. Rectangles  
   &emsp; Rectangles may have line(s) of text at their centre.  
 
3. Text  
   &emsp; A text object has one or more (centred) lines of text.  

To use rfc-draw you'll need to install the following python modules:  
&emsp; tkinter, math, sys, re, os, svgwrite, traceback (for POSIX and windows)  
&emsp; termios (for POSIX) or msvcrt (for Windows)  

You can install all of these by running (in your rfc-draw directory)
  python3 install-modules.py

If that doesn't work, you may need to use a more up-to-date version of pip,  
i.e. one that matches your version of python, for example pip3.10
 
