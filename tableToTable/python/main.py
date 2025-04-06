from ProcessImage import *
from lineHandler import *
import matplotlib.pyplot as plt
from cellHandler import *

imageOG = cv2.imread("7.png")
image = cv2.imread("7.png", cv2.IMREAD_GRAYSCALE)
width = image.shape[1]
height = image.shape[0]

processed = process(image)

averageSize = ((width + height) / 2)
threshold = int(averageSize / 5)
minLineLength = int(averageSize / 5)

lines = cv2.HoughLinesP(processed,
                        1,
                        np.pi / 180,
                        threshold,
                        minLineLength=minLineLength,
                        maxLineGap=4)

extended_lines = []

extending = True
filtering = True

for line in lines:
    if extending:
        extended_lines.append(extend(line[0], width, height))
    else:
        extended_lines.append(line[0]) # not extended

hozLines, vertLines = getDirection(extended_lines)
if filtering:
    hozLines = filterLines(hozLines, "H", width, height)
    vertLines = filterLines(vertLines, "V", width, height)

for line in hozLines:
    x1, y1, x2, y2 = line
    cv2.line(imageOG, (x1, y1), (x2, y2), (255, 0, 0), 2)

for line in vertLines:
    x1, y1, x2, y2 = line
    cv2.line(imageOG, (x1, y1), (x2, y2), (255, 0, 0), 2)

hozLines = sorted(hozLines, key=lambda x: x[1])
vertLines = sorted(vertLines, key=lambda x: x[0])

predict = True
if predict:
    textList, rows, cols = getCells(vertLines, hozLines, imageOG)

    fig, ax = plt.subplots(figsize=(4,2))
    ax.axis("tight")
    ax.axis("off")

    table = ax.table(cellText=textList, loc="center")

cv2.imshow("name3", imageOG)

plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()

'''
Morphological Operations:

2. Improve Edge and Line Detection

Dynamic Hough Transform Parameters:

Instead of computing a fixed threshold from the average image dimensions, consider adapting the Hough transform parameters based on the content of the image (for example, using local image statistics).

Tune parameters like the minimum line length and maximum line gap according to the resolution and expected cell size.

Clustering & Merging: Enhance your line merging routine by applying clustering techniques (e.g., using DBSCAN on line parameters) to combine lines that are nearly collinear. This helps in merging duplicate detections and reducing noise.

3. Post-Processing Enhancements
Contour Analysis: Once you have candidate cells, use contour detection to validate and refine the boundaries. This may involve checking for expected aspect ratios or area ranges.

Skew and Perspective Correction: If your images might be rotated or skewed, apply a deskewing step before processing. Correcting perspective can significantly improve the accuracy of line detection.

Refined Filtering: Revisit your filtering criteria in filterLines(). Consider adaptive thresholds based on local line density or a more robust averaging method that accounts for outliers.

4. Explore Alternative or Complementary Approaches
Deep Learning Methods:

Investigate deep learning models (such as CNN-based table detectors) that have been trained on a variety of table structures. These models often generalize better to different document layouts.

Hybrid approaches that combine classical techniques (like Hough transforms) with deep learning for post-processing validation can be effective.

Existing Table Extraction Libraries: Look into libraries like Camelot or Tabula which use robust methods to extract tables. Even if you don’t use them directly, their methodologies might inspire improvements in your algorithm.

5. Testing and Iteration
Diverse Dataset: Test your algorithm on a variety of images with different table formats and qualities. This will help you identify specific scenarios where your current approach fails.

Parameter Optimization: Use cross-validation or grid search on a validation set to automatically tune your parameters for the best performance across diverse conditions.

By combining these strategies, you can create a more robust algorithm that better handles the variations in table layout, noise, and distortions, ultimately leading to a higher detection rate.

These suggestions are based on common practices in image processing and table detection improvements found in community discussions and research on document analysis .
'''
