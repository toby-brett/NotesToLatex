import math

import numpy as np
from sklearn.cluster import OPTICS
import cv2

def extend(line, width, height): # function to extend the lines

    x1, y1, x2, y2 = line # extracts line

    if x1 == x2: # vertical line
        return int(x1), 0, int(x2), height # y is 0 - max, x stays costant

    gradient = (y2 - y1) / (x2 - x1) # wowza

    if gradient == 0:
        return 0, int(y1), width, int(y2) # x is 0 to max, y stats cosntant

    intercept = y1 - (gradient * x1) # from y = mx + c

    # compute intersection points with image boundaries
    x_min = 0 # smallest X can be
    x_max = width # biggest X can be
    y_min = 0 # smallest Y can be
    y_max = height # biggest y can be

    points = [ # posssible points of boundary collision
        (x_min, int(gradient * x_min + intercept)), # hitting left wall
        (x_max, int(gradient * x_max + intercept)), # hitting right wall
        (int((y_min - intercept) / gradient), y_min), # hitting ceiling
        (int((y_max - intercept) / gradient), y_max) # hitting floor
    ]

    valid_points = [ # if the points are within the screen
        (x, y) for x, y in points if 0 <= x <= width and 0 <= y <= height
    ]

    (x1_new, y1_new), (x2_new, y2_new) = valid_points[0], valid_points[1] # takes first 2. (might be 3 or 4 if the line hits corners exctly)
    return x1_new, y1_new, x2_new, y2_new

def filterHorizontalLines(extendedLines, unextendedLines, width, height):

    filteredLines = [] # stores a list of unique lines

    for long_line, short_line in zip(extendedLines, unextendedLines): # cycles through both the long and short lines
        duplicate = False # assumes the line is not a duplicate
        X1, Y1, X2, Y2 = long_line # extracts extended line
        x1s, y1s, x2s, y2s = short_line # extracts short line

        startX = x1s # sets the startX of this line automatically to the short lines start point
        endX = x2s # same for endX

        for lineComparison in filteredLines: # compares to all the filtered lines

            x1, y1, x2, y2, startXComp, endXComp = lineComparison

            # Crossed over horizontally
            if (Y1 < y1 and Y2 > y2) or (Y1 > y1 and Y2 < y2): # if they cross over

                lineComparison[0] = (lineComparison[0] + X1) / 2 # averages their X1
                lineComparison[1] = (lineComparison[1] + Y1) / 2 # averages their Y1
                lineComparison[2] = (lineComparison[2] + X2) / 2 # X2
                lineComparison[3] = (lineComparison[3] + Y2) / 2 # Y2

                # Update start and end X values
                lineComparison[4] = min(lineComparison[4], x1s) # if the current Xmin is bigger than this new lines Xmin, we take the new Xmin
                lineComparison[5] = max(lineComparison[5], x2s) # same for max

                duplicate = True # as they crossed, there is a duplicate
                break # futher checks not needed

            # Close in Y position
            if abs(y1 - Y1) < (height / 15) or abs(y2 - Y2) < (height / 15): # may be parrallel, close but not crossing
                lineComparison[4] = min(lineComparison[4], x1s) # compares minimum vals
                lineComparison[5] = max(lineComparison[5], x2s)

                duplicate = True
                break

        if not duplicate: # if a unique line was found
            filteredLines.append([X1, Y1, X2, Y2, startX, endX]) # adds the long line, plus the short lines restraints to the filtersLines list

    filteredLines = np.array(filteredLines).astype(int).tolist() # ints
    return filteredLines


def filterVerticalLines(extendedLines, unextendedLines, width, height, image): # check comments above but rotate evertything 90 degrees

    filteredLines = []

    for long_line, short_line in zip(extendedLines, unextendedLines):
        duplicate = False
        X1, Y1, X2, Y2 = long_line
        x1s, y1s, x2s, y2s = short_line

        startY = y1s
        endY = y2s

        # cv2.circle(image, (x1s, startY), 2, (255, 255, 0), thickness=2)
        # cv2.circle(image, (x2s, endY), 2, (255, 255, 0), thickness=2)

        for lineComparison in filteredLines:
            x1, y1, x2, y2, startYComp, endYComp = lineComparison

            #  if line crosses over vertically
            if (X1 < x1 and X2 > x2) or (X1 > x1 and X2 < x2):
                # Average the coordinates
                lineComparison[0] = (lineComparison[0] + X1) / 2
                lineComparison[1] = (lineComparison[1] + Y1) / 2
                lineComparison[2] = (lineComparison[2] + X2) / 2
                lineComparison[3] = (lineComparison[3] + Y2) / 2

                # expands Y bounds if needed
                lineComparison[4] = min(lineComparison[4], y1s)
                lineComparison[5] = max(lineComparison[5], y2s)

                duplicate = True
                break

            # check if lines are close horizontally
            if abs(x1 - X1) < (width / 15) or abs(x2 - X2) < (width / 15):
                # expan Y bounds
                lineComparison[4] = min(lineComparison[4], y1s)
                lineComparison[5] = max(lineComparison[5], y2s)

                duplicate = True
                break

        if not duplicate:
            filteredLines.append([X1, Y1, X2, Y2, startY, endY])

    filteredLines = np.array(filteredLines).astype(int).tolist()
    return filteredLines
def getHorizontalLine(line): # gets a line given a extended line and a bounudary

    x1, y1, x2, y2, startX, endX = line
    m = (y2 - y1) / (x2 - x1) # grad
    c = y1 - m * x1 # intercept

    x1 = startX # bounuds X
    y1 = m * startX  +  c
    x2 = endX # bounds X
    y2 = m * endX  +  c

    return int(x1), int(y1), int(x2), int(y2)

def getVerticalLine(line): # same as above

    x1, y1, x2, y2, startY, endY = line

    if x2 == x1:
        return int(x1), startY, int(x2), endY

    m = (y2 - y1) / (x2 - x1)
    c = y1 - m * x1

    y1 = startY
    x1 = (startY - c) / m
    y2 = endY
    x2 = (endY - c) / m

    return int(x1), int(y1), int(x2), int(y2)

def getDirection(lines): # gets direction of  a line

    hozLines = []
    vertLines = []

    for line in lines:

        x1, y1, x2, y2 = line

        if x1 == x2:
            vertLines.append(line)
        else:
            gradient = (y2 - y1) / (x2 - x1)
            if -1 < gradient < 1: # 1 is 45 degrees
                hozLines.append(line)
            else:
                vertLines.append(line)

    return hozLines, vertLines
