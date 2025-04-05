import cv2
from lineHandler import *
import matplotlib.pyplot as plt
from cellHandler import *

imageOG = cv2.imread("testTable2.png")
image = cv2.imread("testTable2.png", cv2.IMREAD_GRAYSCALE)
blurred = cv2.blur(image, (9, 9))
threshold = cv2.adaptiveThreshold(blurred, 200, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 2)
canny = cv2.Canny(threshold, 150, 200)

width = image.shape[1]
height = image.shape[0]

lines = cv2.HoughLinesP(canny,
                        1,
                        np.pi / 180,
                        70,
                        minLineLength=10,
                        maxLineGap=0)

extended_lines = []

for line in lines:
    extended_lines.append(extend(line[0], width, height))

hozLines, vertLines = getDirection(extended_lines)
hozLines = filterLines(hozLines, "H")
vertLines = filterLines(vertLines, "V")

for line in hozLines:
    x1, y1, x2, y2 = line
    cv2.line(imageOG, (x1, y1), (x2, y2), (255, 0, 0), 2)

for line in vertLines:
    x1, y1, x2, y2 = line
    cv2.line(imageOG, (x1, y1), (x2, y2), (255, 0, 0), 2)

cv2.imshow("image", imageOG)
cv2.waitKey(0)
cv2.destroyAllWindows()

hozLines = sorted(hozLines, key=lambda x: x[1])
vertLines = sorted(vertLines, key=lambda x: x[0])

textList, rows, cols = getCells(vertLines, hozLines, imageOG)
print(textList)

fig, ax = plt.subplots(figsize=(4,2))
ax.axis("tight")
ax.axis("off")

table = ax.table(cellText=textList, loc="center")

cv2.imshow("name3", threshold)
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
