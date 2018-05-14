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

# Calculate the total size of the box.
box_w = gaps_t + grid_w * (cell_w + gaps_t)
box_l = gaps_t + grid_l * (cell_l + gaps_t)
box_h = gaps_t + cell_h
# Find a decent size for each crenellation.
max_cren    = 15.0
num_crens_x = int(math.ceil(float(box_w) / max_cren))
num_crens_y = int(math.ceil(float(box_l) / max_cren))
num_crens_v = int(math.ceil(float(cell_l) / max_cren))
# Ensure odd numbers >= 3.
if (num_crens_x % 2 == 0):
  num_crens_x += 1
if (num_crens_x < 3):
  num_crens_x = 3
if (num_crens_y % 2 == 0):
  num_crens_y += 1
if (num_crens_y < 3):
  num_crens_y = 3
if (num_crens_v % 2 == 0):
  num_crens_v += 1
if (num_crens_v < 3):
  num_crens_v = 3
# Record X/Y crenellation sizes.
cren_w = box_w / num_crens_x;
cren_l = box_l / num_crens_y;
# Find the number/size of crenellations for the small
# vertical single-cell dividers.
cren_v = cell_l / num_crens_v

# Find the total dimensions of the packed file.
# Basically, draw the base and its four walls interlocking,
# and then place the remaining grid dividers above those.
svg_w = box_w + (box_h * 2) - (gaps_t * 2)
svg_h = box_l + (box_h * 2) - (gaps_t * 2)
total_v_divs = (grid_w - 1) * grid_l
svg_h = svg_h + max(box_h * (grid_l - 1), total_v_divs * cell_l - box_h)

print(("Designing a box with dimensions:\n"
       "  Outer size: (%.2f x %.2f)\n"
       "  %.2fmm tall\n"
       "  %d X-axis crenellations, %.2fmm long\n"
       "  %d Y-axis crenellations, %.2fmm long\n"
       "  %d single-column crenellations, %.2fmm long\n"
       "  %d horizontal walls/divider[s], %.2fmm long\n"
       "  2 vertical dividers, %.2fmm long\n"
       "  %d vertical dividers, %.2fmm long\n"
       "  Total SVG size: %.2f x %.2f mm\n"
       %(box_w, box_l, box_h,
         num_crens_x, cren_w,
         num_crens_y, cren_l,
         num_crens_v, cren_v,
         grid_l+1, cell_w, box_l, grid_w, cell_l,
         svg_w, svg_h)))

# Define a base filename based on rounded dimensions.
base_filename = ("gridbox_%dx%dx%d_%dx%d_%dT"
                 %(int(cell_w), int(cell_l), int(cell_h),
                  grid_w, grid_l, int(gaps_t)))
# Open the SVG file.
svg = open("%s.svg"%base_filename, 'w')
# Write the SVG file declaration, to span the full W/H.
svg.write(("<svg width=\"%.2fmm\" height=\"%.2fmm\" "
           "viewBox=\"0 0 %.2f %.2f\" "
           "xmlns=\"http://www.w3.org/2000/svg\">\n"
           %(svg_w, svg_h, svg_w, svg_h)))
# Draw a 'group' tag to style the following shapes.
svg.write(("  <g id=\"outlines\" "
           "fill=\"none\" stroke=\"black\" "
           "stroke-width=\"0.1\" stroke-linejoing=\"miter\">\n"))

# Draw the 'Grid Box' pattern.
# 1. Draw the 'Base' outline, and its notches for the
#    horizontal/vertical divider columns.
# Draw a path to outline the base of the box.
base_x = cell_h
base_y = (svg_h - (box_l + (cell_h)))
svg.write("    <path d=\"M%.2f,%.2f "%(base_x, base_y))
# Top-Left -> Top-Right
c_sign = ""
for i in range(0, num_crens_x-1):
  svg.write("h%.2f v%s%.2f "%(cren_w, c_sign, gaps_t))
  if c_sign == "":
    c_sign = "-"
  else:
    c_sign = ""
svg.write("h%.2f "%cren_w)
# Top-Right -> Bottom-Right
c_sign = "-"
for i in range(0, num_crens_y-1):
  svg.write("v%.2f h%s%.2f "%(cren_l, c_sign, gaps_t))
  if c_sign == "":
    c_sign = "-"
  else:
    c_sign = ""
svg.write("v%.2f "%cren_l)
# Bottom-Right -> Bottom-Left
c_sign = "-"
for i in range(0, num_crens_x-1):
  svg.write("h-%.2f v%s%.2f "%(cren_w, c_sign, gaps_t))
  if c_sign == "":
    c_sign = "-"
  else:
    c_sign = ""
svg.write("h-%.2f "%cren_w)
# Bottom-Left -> Top-Left
c_sign = ""
for i in range(0, num_crens_y-1):
  svg.write("v-%.2f h%s%.2f "%(cren_l, c_sign, gaps_t))
  if c_sign == "":
    c_sign = "-"
  else:
    c_sign = ""
svg.write("v-%.2f "%cren_l)
svg.write("Z\" />\n")
# Draw dividers.
# Vertical grid column dividers.
for i in range(1, grid_w):
  for k in range(0, grid_l):
    for j in range(0, num_crens_v-1):
      if (j % 2 != 0):
        svg.write(("<rect x=\"%.2f\" y=\"%.2f\" "
                   "width=\"%.2f\" height=\"%.2f\" />\n")
                   %(base_x + gaps_t + (cell_w * i),
                     base_y + gaps_t + (cren_v * j) + (cell_l + gaps_t) * k,
                     gaps_t, cren_v))
# Horizontal grid row dividers.
for i in range(1, grid_l):
  for j in range(0, num_crens_x-1):
    if (j % 2 != 0):
      svg.write(("<rect x=\"%.2f\" y=\"%.2f\" "
                 "width=\"%.2f\" height=\"%.2f\" />\n")
                 %(base_x + (cren_w * j),
                   base_y + (gaps_t + (i * cell_l)),
                   cren_w, gaps_t))

# 2. Draw the 'Vertical Wall' outlines. They will go to the
#    Left/Right of the 'base' outline, interlocking with it.
# 'Left' wall:
# (Flat line across the top.)
svg.write(("    <path d=\"M0,%.2f h%.2f v%.2f h%.2f "
           %(base_y, cell_h, cren_l, gaps_t)))
# Top-Right -> Bottom-Right.
c_sign = "-"
for i in range(0, num_crens_y-2):
  svg.write("v%.2f h%s%.2f "%(cren_l, c_sign, gaps_t))
  if c_sign == "":
    c_sign = "-"
  else:
    c_sign = ""
# (Flat lines for the bottom and left edges.)
svg.write("v%.2f h-%.2f "%(cren_l, cell_h))
svg.write("L0,%.2f Z\" />\n"%base_y)
# 'Right' wall:
# (Flat line across the top, right, and bottom.)
svg.write(("    <path d=\"M%.2f,%.2f h%.2f v%.2f h-%.2f "
           %(base_x + box_w, base_y, cell_h, box_l, cell_h)))
# Bottom-Left -> Top-Left.
c_sign = "-"
for i in range(0, num_crens_y-1):
  svg.write("v-%.2f h%s%.2f "%(cren_l, c_sign, gaps_t))
  if c_sign == "":
    c_sign = "-"
  else:
    c_sign = ""
svg.write("L%.2f,%.2f Z\" />\n"%(base_x + box_w, base_y))

# 3. Draw the 'Horizontal Wall/Divider' outlines.
#    The two walls will go above/below the 'base', interlocking.
#    The remaining dividers will go above and on the left.
# 'Bottom' wall.
svg.write(("    <path d=\"M%.2f,%.2f "
          %(cell_h + gaps_t, svg_h - cell_h)))
svg.write("h%.2f v-%.2f "%(cren_w - gaps_t, gaps_t))
c_sign = ""
# Top-Left -> Top-Right
for i in range(0, num_crens_x-2):
  svg.write("h%.2f v%s%.2f "%(cren_w, c_sign, gaps_t))
  if c_sign == "":
    c_sign = "-"
  else:
    c_sign = ""
# (Flat lines for right/bottom/left.)
svg.write(("h%.2f v%.2f h-%.2f "
           %(cren_w - gaps_t, cell_h,
            box_w - gaps_t * 2)))
svg.write("L%.2f,%.2f Z\" />\n"%(cell_h + gaps_t, svg_h - cell_h))
# 'Top' wall.
# (Flat lines for top/right.)
svg.write(("    <path d=\"M%.2f,%.2f h%.2f v%.2f "
          %(cell_h + gaps_t, svg_h - box_l - cell_h * 2,
            box_w - gaps_t * 2, cell_h)))
# Bottom-Right -> Bottom-Left
svg.write("h-%.2f v%.2f "%(cren_w - gaps_t, gaps_t))
c_sign = "-"
for i in range(0, num_crens_x-2):
  svg.write("h-%.2f v%s%.2f "%(cren_w, c_sign, gaps_t))
  if c_sign == "":
    c_sign = "-"
  else:
    c_sign = ""
svg.write("h-%.2f "%(cren_w - gaps_t))
svg.write(("L%.2f,%.2f Z\" />\n"
           %(cell_h + gaps_t, svg_h - box_l - cell_h * 2)))
# Remaining dividers.
for i in range(0, grid_l - 1):
  # (Flat lines for top/right.)
  div_y = svg_h - box_l - cell_h * 2 - box_h * (i + 1)
  svg.write(("    <path d=\"M%.2f,%.2f h%.2f v%.2f "
            %(cell_h + gaps_t, div_y,
              box_w - gaps_t * 2, cell_h)))
  # Bottom-Right -> Bottom-Left
  svg.write("h-%.2f v%.2f "%(cren_w - gaps_t, gaps_t))
  c_sign = "-"
  for j in range(0, num_crens_x-2):
    svg.write("h-%.2f v%s%.2f "%(cren_w, c_sign, gaps_t))
    if c_sign == "":
      c_sign = "-"
    else:
      c_sign = ""
  svg.write("h-%.2f "%(cren_w - gaps_t))
  svg.write(("L%.2f,%.2f Z\" />\n"
             %(cell_h + gaps_t, div_y)))

# 4. Draw the 'Vertical Divider' outlines. They will go above
#    the top 'horizontal wall' pattern on the right.
#    This isn't an optimized use of space, but it should be
#    decent to start with.
div_x = svg_w - cell_h - gaps_t
for i in range(0, total_v_divs):
  div_y = svg_h - box_l - cell_h - (cell_l * (i + 1))
  svg.write(("    <path d=\"M%.2f,%.2f h%.2f v%.2f h%.2f "
             %(div_x, div_y, cell_h, cren_v, gaps_t)))
  c_sign = "-"
  for j in range(0, num_crens_v-2):
    svg.write("v%.2f h%s%.2f "%(cren_v, c_sign, gaps_t))
    if c_sign == "":
      c_sign = "-"
    else:
      c_sign = ""

  svg.write("v%.2f h-%.2f "%(cren_v, cell_h))
  svg.write("L%.2f,%.2f Z\" />\n"%(div_x, div_y))

# Close the 'group' and SVG tags.
svg.write("  </g>\n</svg>\n")
svg.close()
