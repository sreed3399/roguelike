import numpy as np
import tcod
import sys


def main():
    width = height = 50

    try:
        x, y, c, r = process_cmdline()
    except TypeError as err:
        print(err)
        print(usage())
        sys.exit()

    root = init_root(width, height)

    while not tcod.console_is_window_closed():
        root.clear()
        draw_circle(root, x, y, c, r)

        tcod.console_flush()

        dx, dy, dr = handle_key()
        x += dx
        y += dy
        r += 0 if r+dr < 0 else dr


# Is con garbage collected ?
def draw_circle(dest, x, y, c, r):
    diam = 2*r + 1
    center_x = center_y = r
    min_dist = (r-1)**2 - 1
    max_dist = r**2
    mgrid = np.mgrid[:diam, :diam]
    distance_array = (mgrid[0]-center_x)**2 + (mgrid[1]-center_y)**2

    truth_circle = (min_dist < distance_array)*(distance_array < max_dist)

    con = tcod.console_new(diam, diam)
    con.bg[:] = tcod.black
    con.fg[:] = tcod.white
    con.ch[:] = truth_circle.choose([ord(" "), ord(c)])

    con.blit(dest, x-center_x, y-center_y, 0, 0, diam, diam)


def handle_key():
    x = y = r = 0
    key = tcod.console_wait_for_keypress(True)

    if key.vk == tcod.KEY_ESCAPE:
        raise SystemExit()
    elif key.vk == tcod.KEY_CHAR:
        x += (key.c == ord('l')) - (key.c == ord('h'))
        y += (key.c == ord('j')) - (key.c == ord('k'))
        r += (key.c == ord('y')) - (key.c == ord('n'))
    return x, y, r


def init_root(w, h):
    params = {
        "fontFile": "data/fonts/dejavu10x10_gs_tc.png",
        "flags": tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
    }
    tcod.console_set_custom_font(**params)

    params = {
        "w": w,
        "h": h,
        "title": "Challenge 1: Simple circle",
        "fullscreen": False
    }
    return tcod.console_init_root(**params)


def process_cmdline():
    argv = sys.argv[1:]

    if len(argv) != 4:
        raise TypeError(f"4 arguments expected, given: {len(argv)}")
    type_check = (str.isdigit, str.isdigit, lambda x: len(x) == 1, str.isdigit)

    good_type = [type_check[i](e) for i, e in enumerate(argv)]
    if not all(good_type):
        s = "Bad argument :\n"
        s += "\n".join(f"\tArgument {i+1}, '{argv[i]}' is inappropriate" for i, e in
                       enumerate(good_type) if not e)
        raise TypeError(s)
    x, y, c, r = argv
    x, y, r = map(int, (x, y, r))
    return x, y, c, r


def usage():
    s = "\n".join([
        f"usage : {sys.argv[0]} x y char r",
        f"",
        f"\t(x,y) are the circle coordinates, and must be of type int",
        f"\tchar is the character used to draw the circle and must be 1 char only",
        f"\tr is the radius of the circle, and must be of type int",
        f"",
        f"\tYou can zoom in/out with y/n and move the circle around with hjkl"
    ])
    return s





r=2
x = 25
y = 15
c="Red"
    
diam = 2*r + 1
center_x = center_y = r
min_dist = 0
max_dist = r**2

# Initialize variables for midpoint algorithm
x1 = 0
y1 = r
p = (r - 1)**2 - r

mgrid = np.mgrid[:diam,:diam]
mgrid = np.mgrid[x:x+diam:1, y:y+diam:1]
distance_array = (mgrid[0]-center_x)**2 + (mgrid[1]-center_y)**2

a = x
b = y

        #mgrid = np.mgrid[x:x+4, y:y+4]
        
        

for a in range(x+diam+1):
    for b in range(y+diam+1):
        #console.rgb[a,b] = ord("*"), color.white, color.red
        print (a,b)




# Create mgrid
mgrid = np.mgrid[0:4:1, 0:4:1]

# Separate grids into x and y components
x, y = mgrid



# Reshape x and y to create xy pairs
xy_pairs = np.vstack((x.flatten(), y.flatten())).T





outside = (min_dist <= distance_array)*(distance_array <= max_dist)
inside = (min_dist < distance_array)*(distance_array < max_dist)
#print (outside )

# Filter for outline pixels (using both min and max distance)
#outline_circle = (distance_array == min_dist) | (distance_array == max_dist)

while x1 <= y1:
    pass
    # Update destination with circle pixels (assuming appropriate drawing method)
    #dest[center_x + x1, center_y + y1] = c  # Set pixel in first octant
    #dest[center_x - x1, center_y + y1] = c  # Symmetric point
    #dest[center_x + x1, center_y - y1] = c  # Symmetric point
    #dest[center_x - x1, center_y - y1] = c  # Symmetric point

# Update next point based on decision parameter
if p >= 0:
    y1 -= 1
    p -= 2 * y1
else:
    x1 += 1
    p += 2 * x1 + 1

con = tcod.console_new(diam, diam )
#con.bg[:] = color.black
#con.fg[:] = color.red
#con.ch[:] = outline_circle.choose([ord(" "), ord(c)])





