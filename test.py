from ultralytics import YOLO
import cv2

# Load vest model
model = YOLO("runs/detect/train5/weights/best.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    results = model(frame)

    best_conf = 0
    best_class = None
    best_box = None

    # Find best detection
    for box in results[0].boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])

        if conf > best_conf:
            best_conf = conf
            best_class = cls
            best_box = box

    # Decision logic
    if best_conf < 0.6:
        status = "No person detected"
        color = (255, 255, 0)

    elif best_class == 0:
        status = "SAFE - VEST DETECTED"
        color = (0, 255, 0)

    elif best_class == 1:
        status = "NO VEST - ACCESS DENIED"
        color = (0, 0, 255)

    # Draw only best box
    annotated = frame.copy()

    if best_box is not None and best_conf >= 0.6:
        x1, y1, x2, y2 = map(int, best_box.xyxy[0])
        label = f"{'vest' if best_class == 0 else 'no-vest'} {best_conf:.2f}"

        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
        cv2.putText(annotated, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    # Show status
    cv2.putText(annotated, status, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("Vest Detection", annotated)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()