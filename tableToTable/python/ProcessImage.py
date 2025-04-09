import cv2
import numpy as np
from sympy.integrals.manualintegrate import inverse_trig_rule


def process(image):
    width = image.shape[1]
    height = image.shape[0]

    # Noise Reduction: In addition to your current blurring, consider using a Gaussian or median filter to reduce noise while preserving edges.
    blurred = cv2.GaussianBlur(image, (5, 5), 2)
    median = cv2.medianBlur(blurred, 3)

    threshold = cv2.adaptiveThreshold(median, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 3)

    # Dilation and Erosion: Apply dilation to connect any broken segments of the table lines and erosion afterward to remove minor artifacts. This can help make the lines more continuous before edge detection.
    kernelD = np.ones((2, 2), np.uint8) # bigger means less dialation
    kernelE = np.ones((4, 4), np.uint8) # biger means less erosion
    dilated = cv2.dilate(threshold, kernelD, iterations=1)
    eroded = cv2.erode(dilated, kernelE, iterations=1)

    # Try not using canny edge
    inverted = cv2.bitwise_not(eroded)
    invertedPreserved = inverted

    # Canny Edge Parameters: Adjust the thresholds used in the Canny detector. Sometimes using two sets of thresholds or automatically setting them based on the image histogram can yield better edge maps.
    canny = cv2.Canny(eroded, 150, 200)

    # remove small components (like text)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(inverted, connectivity=8)  # top topleft left bottomleft bottom bottomright right toptight are all considered "touching"
    for i, stat in enumerate(stats):
        x, y, w, h, area = stat
        max_area_considered_text = (width * height) * 0.04 # if it covers more than 4 percent of the image, then it is considered the table
        if area < max_area_considered_text:  # area of blob (text gets removed)
            inverted[labels == i] = 0

    removed_text = inverted


    # cv2.imshow("1", blurred)
    # cv2.imshow("2", median)
    # cv2.imshow("3", threshold)
    # cv2.imshow("4", dilated)
    # cv2.imshow("5", eroded)
    # cv2.imshow("6", invertedPreserved)
    # cv2.imshow("7", removed_text)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return removed_text, eroded
