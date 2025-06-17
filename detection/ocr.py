'''
2. ocr.py (License Plate Recognition Script)
This script will handle the Optical Character Recognition (OCR) of license plates using PaddleOCR or any other preferred OCR library.
'''

import cv2
from paddleocr import PaddleOCR

# Load PaddleOCR model
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Function to recognize license plates using PaddleOCR
def recognize_license_plate(vehicle_image):
    # Convert to grayscale for better OCR performance
    gray = cv2.cvtColor(vehicle_image, cv2.COLOR_BGR2GRAY)
    # Run PaddleOCR on the cropped vehicle image
    result = ocr.ocr(gray, cls=True)

    # Assuming license plate is the first detected text
    for line in result[0]:  # The result is a list of detected texts
        if line:  # Check if there is any detected text
            return line[1][0]  # Return the recognized text
    return None
