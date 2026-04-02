import logging

from tableHandler import *
from ProcessImage import *
from lineHandler import *
from model import *
from laTeX import *

def show(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

imageOG = cv2.imread("image.png") # loads origional image in color, for drawing lines and text recog
image = cv2.imread("image.png", cv2.IMREAD_GRAYSCALE) # loads in greyscale (for processing)

width = image.shape[1]
height = image.shape[0]

print("Processing image")
processed, processedForText = process(image) # processes image (see ProcessImage.py)
print("done")

averageSize = ((width + height) / 2) # calculates average dimensions for parameters
threshold = int(averageSize / 15) # the number of pixels needed to class as a line (bigger = more selective with line choice)
minLineLength = int(averageSize / 15) # the smallest line allowed (smaller and it will detect more lines)

print("Detecting lines...")
lines = cv2.HoughLinesP(processed, # the image which lines are being detected from
                        1, # the detail to which the image is searched (granularity of 1 pixel) dont change this works well
                        np.pi / 180, # the detail to which the image is searched (angle of 1 degree)
                        threshold, # above
                        minLineLength=minLineLength, # above
                        maxLineGap=1) # the maximum gap in a line where it is still considered a line (experiment)

extended_lines = [] # list of extended lines (for filtereing)
unextended_lines = [] # list of unextended line (for finding  the start and end points of the line)

filtering = True # turn off if you want to see all the lines before they are filtered

if lines is None:
    raise ValueError("No lines detected. Check preprocessing or Hough parameters.")
for i, line in enumerate(lines): # checks every line detected by houghLinesP (in the form x1, y1, x2, y2)
    print(f"Extending lines {i+1}/{len(lines)}...")
    extended_lines.append(extend(line[0], width, height)) # extends the lines to the screens max
    unextended_lines.append(line[0]) # not extended (saves for finding endpoints of lines)

unextended_hoz_lines, unextended_vert_lines = getDirection(unextended_lines)
hozLines, vertLines = getDirection(extended_lines) # seperates into horizontal and vertical lines for seperate processing)

if filtering:
    print("Filtering lines...")
    hozLines = filterHorizontalLines(hozLines, unextended_hoz_lines, width, height) # filters lines
    vertLines = filterVerticalLines(vertLines, unextended_vert_lines, width, height, imageOG) # filters lines

vertLinesFiltered = []
hozLinesFiltered = []

debug = imageOG.copy()
for line in hozLines:
    if filtering:
        x1, y1, x2, y2 = getHorizontalLine(line) # from  (x1, y1, x2, y2, minX, maxX) to (x1, y1, x2, y2)
    else:
        x1, y1, x2, y2 = line # never found min and max X so converting is not needed

    hozLinesFiltered.append([x1, y1, x2, y2])
    cv2.line(debug, (x1, y1), (x2, y2), (255, 0, 0), 2) # adds each line to the image for visualisation
    show("press 0 to continue", debug)

for line in vertLines: # same thing for vertlines (but with min and max Y)
    if filtering:
        x1, y1, x2, y2 = getVerticalLine(line)
    else:
        x1, y1, x2, y2 = line

    vertLinesFiltered.append([x1, y1, x2, y2])
    cv2.line(debug, (x1, y1), (x2, y2), (0, 255, 0), 2)
    show("press 0 to continue", debug)


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
