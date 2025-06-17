'''
1. detection.py (YOLOv8 Vehicle Detection Script)
This script handles vehicle detection using YOLOv8, calls the OCR function from ocr.py to recognize license plates, and sends the violation data to the backend API.
'''
import cv2
import requests
from ultralytics import YOLO
from ocr import recognize_license_plate  # Import OCR function
import time
from bestmodels import *

# Load YOLOv8 model
# model = YOLO('yolov8n.pt')
model = YOLO(r'C:\Users\Aluko Oluwatobi\Downloads\detection\detection\bestmodels\best11n.pt')  # Use the desired YOLOv8 model

# Function to process the video stream
def process_video(video_source='sample_video.mp4'):
# def process_video(video_source=0):
    cap = cv2.VideoCapture(video_source)  # 0 for webcam or video file path

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform vehicle detection
        results = model(frame)
        detections = results[0].boxes  # Get detected boxes

        for detection in detections:
            box = detection.xyxy[0]  # Bounding box coordinates
            conf = detection.conf  # Confidence score
            cls = int(detection.cls)  # Class ID

            if cls == 2:  # Class '2' is typically for 'car' in the COCO dataset
                # Draw bounding box
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Crop the detected vehicle for license plate recognition
                vehicle_image = frame[y1:y2, x1:x2]
                license_plate_text = recognize_license_plate(vehicle_image)

                if license_plate_text:
                    print(f'Detected License Plate: {license_plate_text}')
                    # Placeholder for speed detection (can be enhanced later)
                    speed = 80  # Replace with actual speed detection logic
                    record_violation(license_plate_text, speed)

        cv2.imshow('Vehicle Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to record violations to the backend
def record_violation(license_plate, speed):
    violation_data = {
        'license_plate': license_plate,
        'speed': speed
    }
    try:
        response = requests.post('http://localhost:5000/record_violation', json=violation_data)
        if response.status_code == 200:
            print('Violation recorded successfully.')
        else:
            print(f'Failed to record violation: {response.text}')
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    process_video()  # Start processing the video


# import cv2
# import requests
# from ultralytics import YOLO
# from ocr import recognize_license_plate  # Import OCR function

# # Load YOLOv8 model
# model = YOLO(r'C:\Users\NOCAY\Desktop\latestyolovproject\detection\bestmodels\best11n.pt')  # Use the desired YOLOv8 model

# # Function to process the video stream
# #def process_video(video_source='sample_video.mp4'):
# def process_video(video_source=0):
#     cap = cv2.VideoCapture(video_source)  # 0 for webcam or video file path

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Perform vehicle detection
#         results = model(frame)
#         detections = results[0].boxes  # Get detected boxes

#         # Check if detections exist and are not None
#         if detections is not None:
#             for detection in detections:
#                 box = detection.xyxy[0]  # Bounding box coordinates
#                 conf = detection.conf.item()  # Confidence score
#                 cls = int(detection.cls)  # Class ID
#                 class_name = model.names[cls] if cls in model.names else f"Class {cls}"  # Class name lookup

#                 # Draw bounding box
#                 x1, y1, x2, y2 = map(int, box)
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

#                 # Display class name and confidence score on the frame
#                 label = f"{class_name}: {conf:.2f}"
#                 cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#                 # Crop the detected vehicle for license plate recognition
#                 vehicle_image = frame[y1:y2, x1:x2]
#                 license_plate_text = recognize_license_plate(vehicle_image)

#                 if license_plate_text:
#                     print(f"Detected License Plate: {license_plate_text}")
#                     print(f"Bounding Box: ({x1}, {y1}), ({x2}, {y2})")
#                     print(f"Class Name: {class_name}, Confidence: {conf:.2f}")
#                     # Placeholder for speed detection (can be enhanced later)
#                     speed = 80  # Replace with actual speed detection logic
#                     record_violation(license_plate_text, speed, box, class_name, conf)

#         # Show the processed frame
#         cv2.imshow('Vehicle Detection', frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# # Function to record violations to the backend
# def record_violation(license_plate, speed, box, class_name, confidence):
#     violation_data = {
#         'license_plate': license_plate,
#         'speed': speed,
#         'bounding_box': {
#             'x1': int(box[0]),
#             'y1': int(box[1]),
#             'x2': int(box[2]),
#             'y2': int(box[3])
#         },
#         'class_name': class_name,
#         'confidence': round(confidence, 2)
#     }
#     try:
#         response = requests.post('http://localhost:5000/record_violation', json=violation_data)
#         if response.status_code == 200:
#             print('Violation recorded successfully.')
#         else:
#             print(f'Failed to record violation: {response.text}')
#     except requests.exceptions.RequestException as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     process_video()  # Start processing the video

