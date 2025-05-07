import torch
import cv2

# Load YOLOv5 model (Nano version for lightweight performance)
model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)

# Start webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO detection
    results = model(frame)

    # Show results
    cv2.imshow('YOLO Webcam', results.render()[0])

    # Press 'p' to exit (as per your preference)
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break

cap.release()
cv2.destroyAllWindows()

