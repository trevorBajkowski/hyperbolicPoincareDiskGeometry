import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
import random
import time
from skimage.io import imread
from skimage.feature import canny
from skimage.util import img_as_ubyte

# #### initiate variables ##### #

x_pts = []
y_pts = []
cur_x = []
cur_y = []
arcs = []

unitCircle = Circle((0, 0), 1, facecolor='none',
                    edgecolor=(0, 0, 0), linewidth=3, alpha=0.8)

fig, ax = plt.subplots(figsize=(7.5, 7.5))
pt_plot = ax.plot([], [], marker='o',
                  linestyle='none', zorder=5)[0]

canvas = ax.get_figure().canvas
placing = False
tempCircle = Circle((0, 0), 1, facecolor='none',
                    edgecolor=(0, 0, 0), linewidth=3, alpha=0.5)


# generates the sample arc after one click is made
# the arc shown will be locked in on the second click
def on_move(event):
    # get the x and y pixel coords
    ax.patches.pop()
    if not ax.patches:
        ax.add_patch(unitCircle)
    m_x, m_y = event.x, event.y
    x2, y2 = ax.transData.inverted().transform([m_x, m_y])
    x1 = cur_x[0]
    y1 = cur_y[0]
    global tempCircle
    x, y, r = find_circle(x1, y1, x2, y2)
    tempCircle = Circle((x, y), r, facecolor='none',
                        edgecolor=(0.8, 0.8, 0), linewidth=3, alpha=0.5)
    theta1 = find_theta(x, y, x1, y1)
    theta2 = find_theta(x, y, x2, y2)
    ratio = find_arc_ratio(theta1, theta2)
    if x1 < 0 and x2 < 0 and np.rad2deg(theta1) > 180 and np.rad2deg(theta2) < 180:
        ratio = 0.1
    if ratio > 0:
        if ratio > 0.5:
            arc = Arc((x, y), r * 2, r * 2, 0, np.rad2deg(theta2), np.rad2deg(theta1))
        else:
            arc = Arc((x, y), r * 2, r * 2, 0, np.rad2deg(theta1), np.rad2deg(theta2))
    else:
        if ratio < 0.5:
            arc = Arc((x, y), r * 2, r * 2, 0, np.rad2deg(theta2), np.rad2deg(theta1))
        else:
            arc = Arc((x, y), r * 2, r * 2, 0, np.rad2deg(theta1), np.rad2deg(theta2))
    ax.add_patch(arc)
    canvas.draw()


# connecting the plot to the above function
onmove = plt.connect('motion_notify_event', on_move)
plt.disconnect(onmove)


# finds the circles defining center and radius given two points
def find_circle(x1, y1, x2, y2):
    x3, y3 = find_circular_inverse(x2, y2)
    m12 = np.reciprocal((y2 - y1) / (x2 - x1)) * -1
    m23 = np.reciprocal((y3 - y2) / (x3 - x2)) * -1
    mid12x = (x2 + x1) / 2
    mid12y = (y2 + y1) / 2
    mid23x = (x3 + x2) / 2
    mid23y = (y3 + y2) / 2
    b12 = mid12y - (m12 * mid12x)
    b23 = mid23y - (m23 * mid23x)
    x = (b23 - b12) / (m12 - m23)  # m12 * x + b12 = m23 * x + b23
    y = (m12 * x) + b12
    r = np.sqrt((x - x1) ** 2 + (y - y1) ** 2)
    return x, y, r


# calculates the inversion of a point relative
# to the unit circle we're using
def find_circular_inverse(x1, y1):
    x = x1 / ((x1 * x1) + (y1 * y1))
    y = y1 / ((x1 * x1) + (y1 * y1))
    return x, y


# gives the positive rotation needed
# to get to certain coordinates of a circle's perimeter
def find_theta(c_x, c_y, x, y):
    theta = np.arctan2(y - c_y, x - c_x)
    if theta < 0:
        theta = (2 * np.pi) + theta
    return theta


# checks if theta is greater than pi
def find_arc_ratio(theta1, theta2):
    center = np.rad2deg(theta2 - theta1)
    return (center/360.0)


# when the 'd' key is pressed it will draw einstein
# when the 'c' key is pressed it will clear the plot
def on_space(event):
        if event.key == 'd':
            ax.add_patch(unitCircle)
            arcList = open("einsteinArcs2.txt", "r").read()
            arcList = arcList.replace("(", "")
            arcList = arcList.replace("[", "").replace("]", "").replace(" ", "")
            arcList = arcList.split(") ,")
            componentList = arcList[0].split(",")
            components = len(componentList) / 5
            com = int(components)
            for i in range(0, com - 1):
                print("Drawing arc {}".format(i))
                x = i * 5
                xx = float(componentList[x])
                y = float(componentList[x + 1])
                d = float(componentList[x + 2])
                t1 = float(componentList[x + 3])
                componentList[x + 4] = componentList[x + 4].replace(")", "")
                t2 = float(componentList[x + 4])
                #arcs.append((xx, y, d, t1, t2))
                a = Arc((xx, y), d, d, 0, t1, t2, linewidth=4)
                ax.patches.pop()
                ax.add_patch(a)
                c = Circle((xx,y), d/2, facecolor='none',
                    edgecolor=(random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)),
                           linewidth=3, alpha=0.2)
                ax.add_patch(c)
                canvas.draw()
                plt.pause(0.04)
        ax.patches.pop()
        if event.key == 'c':
            ax.clear()
            ax.add_patch(unitCircle)
            ax.set_xlim([-1, 1])
            ax.set_ylim([-1, 1])
            canvas.draw()


# logic for what happens on a click in the plot
# both for the beginning of an arc and for the
# second placement click of an arc
def on_click(event):
    global placing
    global onmove
    global cur_x
    global cur_y
    m_x, m_y = event.x, event.y
    x, y = ax.transData.inverted().transform([m_x, m_y])
    x_pts.append(x)
    y_pts.append(y)
    cur_x.append(x)
    cur_y.append(y)
    #pt_plot.set_xdata(x_pts)
    #pt_plot.set_ydata(y_pts)
    if placing:
        placing = False
        plt.disconnect(onmove)
        x, y, r = find_circle(cur_x[0], cur_y[0], cur_x[1], cur_y[1])
        theta1 = find_theta(x, y, cur_x[0], cur_y[0])
        theta2 = find_theta(x, y, cur_x[1], cur_y[1])
        ratio = find_arc_ratio(theta1, theta2)
        if cur_x[0] < 0 and cur_x[1] < 0:
            t1 = np.rad2deg(theta1)
            t2 = np.rad2deg(theta2)
            if t1 > 180 and t2 < 180:
                ratio = 0.1
        if ratio > 0:
            if ratio > 0.5:
                # the commented out lines are
                # used if you want to print out your arcs
                # so you can copy them into a text file for drawing

                # a = (x, y, r * 2, np.rad2deg(theta2), np.rad2deg(theta1))
                # arcs.append(a)
                arc = Arc((x, y), r * 2, r * 2, 0, np.rad2deg(theta2), np.rad2deg(theta1))
            else:
                # a = (x, y, r * 2, np.rad2deg(theta1), np.rad2deg(theta2))
                # arcs.append(a)
                arc = Arc((x, y), r * 2, r * 2, 0, np.rad2deg(theta1), np.rad2deg(theta2))
        else:
            if ratio < 0.5:
                # a = (x, y, r * 2, np.rad2deg(theta2), np.rad2deg(theta1))
                # arcs.append(a)
                arc = Arc((x, y), r * 2, r * 2, 0, np.rad2deg(theta2), np.rad2deg(theta1))
            else:
                # a = (x, y, r * 2, np.rad2deg(theta1), np.rad2deg(theta2))
                # arcs.append(a)
                arc = Arc((x, y), r * 2, r * 2, 0, np.rad2deg(theta1), np.rad2deg(theta2))
        ax.add_patch(arc)
        # print(arcs)
        cur_x = []
        cur_y = []
    else:
        onmove = plt.connect('motion_notify_event', on_move)
        placing = True
    canvas.draw()

# connecting the two functions above to the plot
plt.connect('key_press_event', on_space)
plt.connect('button_press_event', on_click)
ax.add_patch(unitCircle)
ax.add_patch(unitCircle)
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
plt.show()

