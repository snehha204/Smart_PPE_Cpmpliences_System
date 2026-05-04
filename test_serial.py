from ultralytics import YOLO
import cv2
import datetime
import time
import serial

# -------- SERIAL SETUP --------
try:
    stm32 = serial.Serial('/dev/cu.usbserial-0001', 115200, timeout=1)
    time.sleep(2)
    print("✅ STM32 Connected")
except:
    stm32 = None
    print("⚠️ STM32 NOT connected")

# -------- LOAD MODELS --------
helmet_model = YOLO("runs/detect/train8/weights/best.pt")
vest_model = YOLO("runs/detect/train5/weights/best.pt")

cap = cv2.VideoCapture(0)

last_status = None
last_mark_time = 0
COOLDOWN = 10  # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    helmet_results = helmet_model(frame)
    vest_results = vest_model(frame)

    annotated = frame.copy()

    # -------- HELMET DETECTION --------
    helmet_detected = False

    for box in helmet_results[0].boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])

        if conf > 0.6:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = "helmet" if cls == 1 else "head"

            cv2.rectangle(annotated, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(annotated, f"{label} {conf:.2f}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        if conf > 0.6 and cls == 1:
            helmet_detected = True

    # -------- VEST DETECTION --------
    best_conf = 0
    best_class = None
    best_box = None

    for box in vest_results[0].boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])

        if conf > best_conf:
            best_conf = conf
            best_class = cls
            best_box = box

    vest_detected = False

    if best_conf >= 0.6 and best_class == 0:
        vest_detected = True

    if best_box is not None and best_conf >= 0.6:
        x1, y1, x2, y2 = map(int, best_box.xyxy[0])
        label = f"{'vest' if best_class == 0 else 'no-vest'} {best_conf:.2f}"

        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(annotated, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # -------- FINAL DECISION --------
    if helmet_detected and vest_detected:
        status = "FULL PPE - ACCESS GRANTED"
        color = (0, 255, 0)
        current_status = "SAFE"
    else:
        status = "PPE MISSING - ACCESS DENIED"
        color = (0, 0, 255)
        current_status = "UNSAFE"

    # -------- SEND SIGNAL ONLY ON CHANGE --------
    if current_status != last_status:
        if current_status == "SAFE":
            print("🟢 Sending 1 → OPEN GATE")
            if stm32:
                stm32.write(b'1')
        else:
            print("🔴 Sending 0 → CLOSE GATE + BUZZER")
            if stm32:
                stm32.write(b'0')

    # -------- ATTENDANCE --------
    current_time = time.time()

    if current_status == "SAFE" and (current_time - last_mark_time > COOLDOWN):
        print("✅ Attendance Marked")

        with open("attendance.csv", "a") as f:
            now = datetime.datetime.now()
            f.write(f"{now}, ACCESS GRANTED\n")

        last_mark_time = current_time

    last_status = current_status

    # -------- DISPLAY --------
    cv2.putText(annotated, status, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    if current_status == "SAFE":
        cv2.putText(annotated, "GATE: OPEN", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(annotated, "BUZZER: OFF", (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    else:
        cv2.putText(annotated, "GATE: CLOSED", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(annotated, "BUZZER: ON", (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("PPE Detection System", annotated)

    if cv2.waitKey(1) == 27:
        break

# -------- CLEANUP --------
cap.release()
cv2.destroyAllWindows()
if stm32:
    stm32.close()