# NotesToLatex
*(unfinished)*

Turn a photo of handwritten notes into LaTeX.

The only working piece right now is **TableToLatex** - point it at a photo of a hand-drawn table and it'll return out a `\begin{tabular}` block. Full page parsing is the eventual goal.


# Examples
| Output \| Input |
|-------|
![Example 2](tableToTable/examples/example2)
![Example 3](tableToTable/examples/example3)
![Example 4](tableToTable/examples/example4)

I used a pretrained OCR model for text recognition (terrible results, but just a placeholder — my main focus was the table backbone). If I were to continue this project I would certainly train a better one myself.

# Pipeline

**Raw image:**

![Raw Image](tableToTable/examples/plain.png)

1. **Gaussian blur** - smooths before thresholding
```python
blurred = cv2.GaussianBlur(image, (5, 5), 2)
```
![Blurred Image](tableToTable/examples/blur.png)

2. **Adaptive threshold** - black and white, handles uneven lighting
```python
threshold = cv2.adaptiveThreshold(median, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 3)
```
![Thresholded Image](tableToTable/examples/threshold1.png)

3. **Dilation** - thickens lines to close any gaps in the table border
```python
dilated = cv2.dilate(threshold, kernelD, iterations=1)
```
![Dilated Image](tableToTable/examples/thicken.png)

4. **Erosion** - strips leftover noise
```python
eroded = cv2.erode(dilated, kernelE, iterations=1)
```
![Eroded Image](tableToTable/examples/denoise.png)

5. **Invert** - HoughLinesP wants white-on-black

![Inverted Image](tableToTable/examples/invert.png)

6. **Hough line detection** - finds line segments
```python
lines = cv2.HoughLinesP(processed,
                        1,
                        np.pi / 180,
                        threshold,
                        minLineLength=minLineLength,
                        maxLineGap=1)
```
![Detected Lines](tableToTable/examples/image.png)

7. **Line filtering** - keeps only horizontal/vertical, drops the rest

![Filtered Lines](tableToTable/examples/hozandvert.png)

8. **Table construction** - finds intersections, infers cells

![Full Table](tableToTable/examples/full_table.png)

9. **OCR + output** - reads each cell, assembles the LaTeX
```latex
\documentclass{article}
\usepackage{multirow}
\usepackage{booktabs}
\begin{document}
\begin{table}[h]
\centering
\begin{tabular}{|l|l|}
\hline
\verb|street ,|&\verb|" Mexico|\\
\hline
\verb|Because it|&\verb|forces in the|\\
\hline
\verb|Texas State|&\verb|2 October 1987|\\
\hline
\end{tabular}
\end{table}
\end{document}
```
The OCR is bad, I'm using a pretrained model as a placeholder. That was never the point; I wanted to get the table structure right first. I'd train something better if I continued it.


## Setup
Requires Python 3.
```bash
git clone https://github.com/toby-brett/NotesToLatex.git
pip install -r requirements.txt
cd NotesToLatex/tableToTable
python main.py --image your_image.png
```
Built with [OpenCV](https://opencv.org/) and [Tesseract](https://github.com/tesseract-ocr/tesseract).

