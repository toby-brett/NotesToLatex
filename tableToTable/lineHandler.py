import numpy as np

def extend(line, width, height):

    x1, y1, x2, y2 = line

    if x1 == x2: # vertical line
        return int(x1), 0, int(x2), height

    gradient = (y2 - y1) / (x2 - x1)

    if gradient == 0:
        return 0, int(y1), width, int(y2)

    intercept = y1 - (gradient * x1) # from y = mx + c

    # compute intersection points with image boundaries
    x_min = 0
    x_max = width
    y_min = 0
    y_max = height

    points = [ # posssible points of boundary collision
        (x_min, int(gradient * x_min + intercept)),
        (x_max, int(gradient * x_max + intercept)),
        (int((y_min - intercept) / gradient), y_min),
        (int((y_max - intercept) / gradient), y_max) # rearrange y = mx + c
    ]

    valid_points = [
        (x, y) for x, y in points if 0 <= x <= width and 0 <= y <= height
    ]

    if len(valid_points) == 2:
        (x1_new, y1_new), (x2_new, y2_new) = valid_points
        return x1_new, y1_new, x2_new, y2_new

    raise ValueError("More than 2 intersection with screen edges")

def filterLines(lines, vertOrHoz): # all horizontal or vertical

    filteredLines = []

    for line in lines:

        duplicate = False
        X1, Y1, X2, Y2 = line

        for lineComparison in filteredLines:

            x1, y1, x2, y2 = lineComparison

            if (X1 < x1 and X2 > x2) or (X1 > x1 and X2 < x2): # crossed over
                duplicate = True
                continue

            if (Y1 < y1 and Y2 > y2) or (Y1 > y1 and Y2 < y2): # crossed over
                duplicate = True
                continue

            if vertOrHoz == "H":
                if abs(y1 - Y1) < 40 or abs(y2 - Y2) < 40:
                    duplicate = True
                    continue

            else:
                if abs(x1 - X1) < 40 or abs(x2 - X2) < 40:
                    duplicate = True
                    continue

        if not duplicate:
            filteredLines.append(line)

    return filteredLines

def getDirection(lines):

    hozLines = []
    vertLines = []

    for line in lines:

        x1, y1, x2, y2 = line

        if x1 == x2:
            vertLines.append(line)
        else:
            gradient = (y2 - y1) / (x2 - x1)
            if -1 < gradient < 1:
                hozLines.append(line)
            else:
                vertLines.append(line)

    return hozLines, vertLines
