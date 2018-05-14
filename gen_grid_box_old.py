import sys
import math

# Check that the right number of arguments were passed in.
if len(sys.argv) != 7:
  print(("Usage: 'python gen_grid_box.py [W] [L] [H] [C] [R] [T]'\n"
         "  [W] = Interior width (x-axis) of one cell, in mm\n"
         "  [L] = Interior length (y-axis) of one cell, in mm\n"
         "  [H] = Interior height/depth of one cell, in mm\n"
         "  [C] = Number of grid columns\n"
         "  [R] = Number of grid rows\n"
         "  [T] = Thickness of the material\n"))
  sys.exit(1)

# Record the desired values.
cell_w = float(sys.argv[1])
cell_l = float(sys.argv[2])
cell_h = float(sys.argv[3])
grid_w = int(sys.argv[4])
grid_l = int(sys.argv[5])
gaps_t = float(sys.argv[6])
# Adjust to the laser's cut thickness
# TODO: Use this value.
laser_kerf = 0.3

# Calculate the total size of the box.
box_w = gaps_t + grid_w * (cell_w + gaps_t)
box_l = gaps_t + grid_l * (cell_l + gaps_t)
box_h = gaps_t + cell_h
# Find a decent size for each crenellation.
max_cren    = 15.0
num_crens_x = int(math.ceil(float(box_w) / max_cren))
num_crens_y = int(math.ceil(float(box_l) / max_cren))
# Ensure odd numbers >= 3.
if (num_crens_x % 2 == 0):
  num_crens_x += 1
if (num_crens_x < 3):
  num_crens_x = 3
if (num_crens_y % 2 == 0):
  num_crens_y += 1
if (num_crens_y < 3):
  num_crens_y = 3
# Record X/Y crenellation sizes.
cren_w = box_w / num_crens_x;
cren_l = box_l / num_crens_y;

# Define a base filename based on rounded dimensions.
base_filename = "gridbox_%dx%d_%dx%d_%dT"%(int(cell_w), int(cell_l), grid_w, grid_l, int(gaps_t))

# Draw the 'box base' file.
base_svg = open("%s_base.svg"%base_filename, 'w')
# Write the SVG file declaration, to span the full W/H.
base_svg.write(("<svg width=\"%.2fmm\" height=\"%.2fmm\" "
                "viewBox=\"0 0 %.2f %.2f\" "
                "xmlns=\"http://www.w3.org/2000/svg\">\n"
                %(box_w, box_l, box_w, box_l)))
# Draw a 'group' tag to style the following shapes.
base_svg.write(("  <g id=\"outlines\" "
                "fill=\"none\" stroke=\"black\" "
                "stroke-width=\"0.1\" stroke-linejoing=\"miter\">\n"))

# Draw a path to outline the base of the box.
base_svg.write("    <path d=\"M0,0 ")
# Top-Left -> Top-Right
c_sign = ""
for i in range(0, num_crens_x-1):
  base_svg.write("h%.2f v%s%.2f "%(cren_w, c_sign, gaps_t))
  if c_sign == "":
    c_sign = "-"
  else:
    c_sign = ""
base_svg.write("h%.2f "%cren_w)
# Top-Right -> Bottom-Right
c_sign = "-"
for i in range(0, num_crens_y-1):
  base_svg.write("v%.2f h%s%.2f "%(cren_l, c_sign, gaps_t))
  if c_sign == "":
    c_sign = "-"
  else:
    c_sign = ""
base_svg.write("v%.2f "%cren_l)
# Bottom-Right -> Bottom-Left
c_sign = "-"
for i in range(0, num_crens_x-1):
  base_svg.write("h-%.2f v%s%.2f "%(cren_w, c_sign, gaps_t))
  if c_sign == "":
    c_sign = "-"
  else:
    c_sign = ""
base_svg.write("h-%.2f "%cren_w)
# Bottom-Left -> Top-Left
c_sign = ""
for i in range(0, num_crens_y-1):
  base_svg.write("v-%.2f h%s%.2f "%(cren_l, c_sign, gaps_t))
  if c_sign == "":
    c_sign = "-"
  else:
    c_sign = ""
base_svg.write("v-%.2f "%cren_l)
base_svg.write("Z\" />\n")

# Draw dividers.
for i in range(1, grid_w):
  for j in range(0, num_crens_y-1):
    if (j % 2 != 0):
      base_svg.write(("<rect x=\"%.2f\" y=\"%.2f\" "
                      "width=\"%.2f\" height=\"%.2f\" />")
                      %(gaps_t + (i * cell_w),
                        cren_l * j, gaps_t, cren_l))
for i in range(1, grid_l):
  for j in range(0, num_crens_x-1):
    if (j % 2 != 0):
      base_svg.write(("<rect x=\"%.2f\" y=\"%.2f\" "
                      "width=\"%.2f\" height=\"%.2f\" />")
                      %(cren_w * j, gaps_t + (i * cell_l),
                        cren_w, gaps_t))

# Close the 'group' and SVG tags.
base_svg.write("  </g>\n</svg>\n")
base_svg.close()

# Draw the 'horizontal dividers' file.
horiz_svg = open("%s_horizs.svg"%base_filename, 'w')
# Write the SVG file declaration, to span the full W/H.
horiz_svg.write(("<svg width=\"%.2fmm\" height=\"%.2fmm\" "
                 "viewBox=\"0 0 %.2f %.2f\" "
                 "xmlns=\"http://www.w3.org/2000/svg\">\n"
                 %(box_w - gaps_t * 2, box_h,
                   box_w - gaps_t * 2, box_h)))
# Draw a 'group' tag to style the following shapes.
horiz_svg.write(("  <g id=\"outlines\" "
                 "fill=\"none\" stroke=\"black\" "
                 "stroke-width=\"0.1\" stroke-linejoing=\"miter\">\n"))
# Draw a path to outline a horizontal wall/divider of the box.
# (Flat line across the top and right.)
horiz_svg.write(("    <path d=\"M0,0 h%.2f v%.2f h-%.2f v%.2f "
                 %((box_w - (gaps_t * 2)),
                   (cell_h),
                   (cren_w - gaps_t),
                   (gaps_t))))
# Bottom-Right -> Bottom-Left
c_sign = "-"
for i in range(0, num_crens_x-2):
  horiz_svg.write("h-%.2f v%s%.2f "%(cren_w, c_sign, gaps_t))
  if c_sign == "":
    c_sign = "-"
  else:
    c_sign = ""
horiz_svg.write("h-%.2f "%(cren_w - gaps_t))
horiz_svg.write("L0,0 Z\" />\n")
# Close the 'group' and SVG tags.
horiz_svg.write("  </g>\n</svg>\n")
horiz_svg.close()


# Draw the 'vertical edges' file.
vert_svg = open("%s_verts.svg"%base_filename, 'w')
# Write the SVG file declaration, to span the full W/H.
vert_svg.write(("<svg width=\"%.2fmm\" height=\"%.2fmm\" "
                "viewBox=\"0 0 %.2f %.2f\" "
                "xmlns=\"http://www.w3.org/2000/svg\">\n"
                %(box_h, box_l, box_h, box_l)))
# Draw a 'group' tag to style the following shapes.
vert_svg.write(("  <g id=\"outlines\" "
                "fill=\"none\" stroke=\"black\" "
                "stroke-width=\"0.1\" stroke-linejoing=\"miter\">\n"))
# Draw a path to outline a vertical wall of the box.
# (Flat line across the top.)
vert_svg.write(("    <path d=\"M0,0 h%.2f v%.2f h%.2f "
                %(box_h - gaps_t, cren_l, gaps_t)))
# Top-Right -> Bottom-Right.
c_sign = "-"
for i in range(0, num_crens_y-2):
  vert_svg.write("v%.2f h%s%.2f "%(cren_l, c_sign, gaps_t))
  if c_sign == "":
    c_sign = "-"
  else:
    c_sign = ""
# (Flat lines for the bottom and left edges.)
vert_svg.write("v%.2f h-%.2f "%(cren_l, box_h - gaps_t))
vert_svg.write("L0,0 Z\" />\n")
# Close the 'group' and SVG tags.
vert_svg.write("  </g>\n</svg>\n")
vert_svg.close()

# If necessary, draw a 'vertical dividers' file.
# TODO
