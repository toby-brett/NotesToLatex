from lineHandler import *
import cv2
import numpy as np

hlines = [[65, 102, 724, 98], [103, 507, 768, 506], [88, 352, 752, 369], [79, 217, 742, 218]]
vlines = [[727, 89, 756, 519], [75, 104, 98, 507], [415, 224, 428, 513]]

def straighten(linesList):

    straightLines = []

    for line in linesList:
        x1, y1, x2, y2 = line

        if x1 == x2:
            straightLines.append([x1, y1, x2, y2])
        else:

            m = (y2 - y1)/(x2 - x1)

            if abs(m) > 1:
                xAvg = (x1 + x2) / 2
                straightLines.append([int(xAvg), y1, int(xAvg), y2])

            else:
                yAvg = (y1 + y2) / 2
                straightLines.append([x1, int(yAvg), x2, int(yAvg)])

    return straightLines

def getLines(hozLines, vertLines, image):

    hozLinesLong = [] # list of extended lines
    vertLinesLong = []

    for line in hozLines:
        hozLinesLong.append(extend(line, image.shape[1], image.shape[0])) # extends the lines
    for line in vertLines:
        vertLinesLong.append(extend(line, image.shape[1], image.shape[0]))

    hozLinesLong = straighten(hozLinesLong) # straightens the long lines
    vertLinesLong = straighten(vertLinesLong)

    hozLinesStraight = straighten(hozLines) # straightens the short lines
    vertLinesStraight = straighten(vertLines)

    for hoz in hozLinesStraight: # iterates through every short horizontal line

        startPoint = hoz[0] # current start
        endPoint = hoz[2] # current end

        newStartPoint = float("inf") # arbitrary and big so it is immediately filtered out
        newEndPoint = float("inf")

        for vertLong in vertLinesLong: # checks all the extended long lines
            if abs(vertLong[0] - startPoint) < abs(startPoint - newStartPoint): # checks if the distance to the new line from the origional point is less than the distance between the newStart and the old start
                newStartPoint = vertLong[0] # sets the short lines new starting point to the intersection
            if abs(vertLong[2] - endPoint) < abs(endPoint - newEndPoint):
                newEndPoint = vertLong[2]

        lineIdx = hozLinesStraight.index(hoz)
        hozLinesStraight[lineIdx][0] = int(np.floor(newStartPoint))
        hozLinesStraight[lineIdx][2] = int(np.floor(newEndPoint))

    for vert in vertLinesStraight:

        startPoint = vert[1]
        endPoint = vert[3]

        newStartPoint = 100000 # arbitrary and big so it is immediately filtered out
        newEndPoint = 100000

        for hozLong in hozLinesLong:
            if abs(hozLong[1] - startPoint) < abs(startPoint - newStartPoint): # checks if the distance to the new line from the origional point is less than the distance between the newStart and the old start
                newStartPoint = hozLong[1]
            if abs(hozLong[3] - endPoint) < abs(endPoint - newEndPoint):
                newEndPoint = hozLong[3]

        lineIdx = vertLinesStraight.index(vert)
        vertLinesStraight[lineIdx][1] = int(np.floor(newStartPoint))
        vertLinesStraight[lineIdx][3] = int(np.floor(newEndPoint))

    for line in hozLinesStraight:
        cv2.line(image, (line[0], int(line[1])), (line[2], int(line[3])), (0, 255, 0), 2)
    for line in vertLinesStraight:
        cv2.line(image, (int(line[0]), line[1]), (int(line[2]), line[3]), (0, 255, 0), 2)

    return hozLinesStraight, vertLinesStraight, hozLinesLong, vertLinesLong

def getTable(lines):

    hozLinesStraight, vertLinesStraight, hozLinesLong, vertLinesLong = lines

    hs = hozLinesStraight # hs = hoz straight
    vs = vertLinesStraight

    rows = []

    for h in range(len(hs) - 1):
        rows.append([])
        for v in range(len(vs) - 1):
            cell = [(vs[v][0], hs[h][1]), (vs[v+1][0], hs[h][1]), (vs[v+1][0], hs[h+1][1]), (vs[v][0], hs[h+1][1])]
            rows[-1].append(cell)

    rows = []
    widths = []
    heights = []

    for v in range(len(vertLinesLong) - 1):
        width = vertLinesLong[v][0] - vertLinesLong[v+1][0]
        widths.append(width)
    for h in range(len(hozLinesLong) - 1):
        height = hozLinesLong[h][1] - hozLinesLong[h+1][1]
        heights.append(height)

    table = []
    for row in rows:
        table.append([])
        i = 0 # resets the width counter
        for cell in row:
            rowWidth = row[1][0] - row[0][0]
            sumWidth = 0
            count = 0
            while rowWidth != sumWidth:
                sumWidth += widths[i]
                i += 1
                count = 0
            table[-1].append([cell, count]) # count is the number of cells the header goes over

    return table

def getIntersections(h_lines, v_lines):

    h_lines = sorted(h_lines, key=lambda x: x[1])
    v_lines = sorted(v_lines, key=lambda x: x[0])

    intersections = []
    for h in h_lines: # h = x1, y1, x2, y2
        intersections.append([]) # new hoz line
        for v in v_lines:
            #print("vertical y = ", v[1], "horizontal y = ", h[1], "vertical x = ", v[0], "horizontal x = ", h[0])
            if abs(v[1] - h[1]) <= 2: # this is where a vertLine hits the middle of a hozLine
            # if the start of v == the y coord of h, then there is an intersection <=4 due to rounding errors
                x = v[0] # starts at v's start X
                y = h[1] # y is where hoz line runs through
                intersections[-1].append((x, y))
            elif abs(h[0] - v[0]) <= 2: # a hozLines hits the middle of a vertLine
                x = v[0]
                y = h[1]
                intersections[-1].append((x, y))
            elif abs(h[2] - v[0]) <= 2: # end of a hozLine hits a vertLine
                x = v[0]
                y = h[1]
                intersections[-1].append((x, y))
            elif abs(v[3] - h[1]) <= 2:
                x = v[0]
                y = h[1]
                intersections[-1].append((x, y))

            elif (v[1] < h[1] < v[3]) and (h[0] < v[0] < h[2]):
                x = v[0]
                y = h[1]
                intersections[-1].append((x, y))
            else:
                continue

    return intersections

def getCells(intersections):

    cellList = []

    for h in range(len(intersections) - 1):
        cellList.append([])
        for i in range(len(intersections[h]) - 1):

            height = intersections[h+1][i][1] - intersections[h][i][1] # height of cell

            x1, y1, x2, y2 = intersections[h][i][0], intersections[h][i][1], intersections[h][i+1][0], intersections[h][i+1][1]
            x3, y3, x4, y4 = x1, y1 + height, x2, y2 + height

            cellList[-1].append([x1, y1, x2, y2, x3, y3, x4, y4])


    return cellList

# imageOG = cv2.imread("13.png")
# lines = getLines(hlines, vlines, imageOG)
# table = getTable(lines)
