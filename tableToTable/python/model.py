import cv2
import cv2
from PIL import Image
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

# Initialize once
#reader = easyocr.Reader(['en'], gpu=False)



def predict(cell, image):
    # Unpack 4 points (x, y) — assuming order: top-left, top-right, bottom-right, bottom-left
    x1, y1, x2, y2, x3, y3, x4, y4 = cell

    # Convert polygon to bounding box (AABB)
    x_coords = [x1, x2, x3, x4]
    y_coords = [y1, y2, y3, y4]
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)

    # Clip to image boundaries
    x_min = max(0, x_min)
    y_min = max(0, y_min)
    x_max = min(image.shape[1], x_max)
    y_max = min(image.shape[0], y_max)

    # Extract chunk
    chunk = image[y_min:y_max, x_min:x_max]

    if chunk.size == 0:
        print(f"Empty chunk for cell: {cell}")
        return ""

    # Convert BGR to RGB
    rgb_chunk = cv2.cvtColor(chunk, cv2.COLOR_BGR2RGB)

    # cv2.imshow("image", rgb_chunk)
    # cv2.waitKey(0)

    pil_img = Image.fromarray(rgb_chunk)

    # 3. Load the processor and model (use 'trocr-base-handwritten' or 'trocr-large-handwritten')
    processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
    model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')

    # 4. Preprocess the image and generate input tensor
    pixel_values = processor(images=pil_img, return_tensors="pt").pixel_values

    # 5. Generate prediction (disable grad + run on GPU if available)
    with torch.no_grad():
        generated_ids = model.generate(pixel_values)

    # 6. Decode the output token IDs to text
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(generated_text)

    return generated_text
