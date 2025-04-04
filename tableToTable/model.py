import PIL.ImageShow
from PIL import Image
import cv2
import easyocr
import numpy as np

def predict(image):

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)
    numpy_image = np.array(pil_image)

    reader = easyocr.Reader(['en'])  # You can specify multiple languages like ['en', 'fr']
    result = reader.readtext(numpy_image)

    for detection in result:
        return detection[1]
