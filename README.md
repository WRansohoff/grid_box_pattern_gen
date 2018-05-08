# Overview

This is a script to generate .SVG files for 'grid boxes'; I've used these patterns for a few things in sizes ranging from part trays to battery cases, so it seems like a good thing to try automating.

Start with a simple concept; given an interior width/height of each 'grid cell', the number of rows and columns in the grid, and the thickness of the walls, generate a pattern for the pieces needed to assemble the box.

Currently, millimeters are the only allowed units.

Example command; a box sized to 2x AAA batteries with spring contacts, made out of 3mm-thick material:

python gen\_grid\_box.py 48.0 12.0 1 2 3.0

Currently incomplete; it generates a 'base' pattern, but no walls/dividers. I'll probably need to make it accept a wall height, too...
