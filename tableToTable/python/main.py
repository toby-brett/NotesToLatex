import cv2
from tableHandler import *
from ProcessImage import *
from lineHandler import *
import matplotlib.pyplot as plt
from model import *
from laTeX import *

imageOG = cv2.imread("18.png") # loads origional image in color, for drawing lines and text recog
image = cv2.imread("18.png", cv2.IMREAD_GRAYSCALE) # loads in greyscale (for processing)

width = image.shape[1]
height = image.shape[0]

processed, processedForText = process(image) # processes image (see ProcessImage.py)


averageSize = ((width + height) / 2) # calculates average dimensions for parameters
threshold = int(averageSize / 15) # the number of pixels needed to class as a line (bigger = more selective with line choice)
minLineLength = int(averageSize / 15) # the smallest line allowed (smaller and it will detect more lines)

lines = cv2.HoughLinesP(processed, # the image which lines are being detected from
                        1, # the detail to which the image is searched (granularity of 1 pixel) dont change this works well
                        np.pi / 180, # the detail to which the image is searched (angle of 1 degree)
                        threshold, # above
                        minLineLength=minLineLength, # above
                        maxLineGap=1) # the maximum gap in a line where it is still considered a line (experiment)

extended_lines = [] # list of extended lines (for filtereing)
unextended_lines = [] # list of unextended line (for finding  the start and end points of the line)

filtering = True # turn off if you want to see all the lines before they are filtered

for line in lines: # checks every line detected by houghLinesP (in the form x1, y1, x2, y2)
    extended_lines.append(extend(line[0], width, height)) # extends the lines to the screens max
    unextended_lines.append(line[0]) # not extended (saves for finding endpoints of lines)

unextended_hoz_lines, unextended_vert_lines = getDirection(unextended_lines)
hozLines, vertLines = getDirection(extended_lines) # seperates into horizontal and vertical lines for seperate processing)

if filtering:
    hozLines = filterHorizontalLines(hozLines, unextended_hoz_lines, width, height) # filters lines
    vertLines = filterVerticalLines(vertLines, unextended_vert_lines, width, height, imageOG) # filters lines

vertLinesFiltered = []
hozLinesFiltered = []

for line in hozLines:
    if filtering:
        x1, y1, x2, y2 = getHorizontalLine(line) # from  (x1, y1, x2, y2, minX, maxX) to (x1, y1, x2, y2)
    else:
        x1, y1, x2, y2 = line # never found min and max X so converting is not needed

    hozLinesFiltered.append([x1, y1, x2, y2])
    cv2.line(imageOG, (x1, y1), (x2, y2), (255, 0, 0), 2) # adds each line to the image for visualisation

for line in vertLines: # same thing for vertlines (but with min and max Y)
    if filtering:
        x1, y1, x2, y2 = getVerticalLine(line)
    else:
        x1, y1, x2, y2 = line

    vertLinesFiltered.append([x1, y1, x2, y2])
    cv2.line(imageOG, (x1, y1), (x2, y2), (255, 0, 0), 2)
cv2.imshow('win', imageOG)
cv2.waitKey(0)

hozLinesStraight, vertLinesStraight, hozLinesLong, vertLinesLong = getLines(hozLinesFiltered, vertLinesFiltered, imageOG)
intersections = getIntersections(hozLinesStraight, vertLinesStraight)
cells = getCells(intersections)

textList = []
for row in cells:
    textList.append([])
    for cell in row:
        prediction = predict(cell, processedForText)
        textList[-1].append(prediction)


getFormula(cells, textList)
