🛡️ Smart PPE Compliance System using YOLO & STM32

📌 Project Overview

This project presents a Smart PPE (Personal Protective Equipment) Compliance System that automatically detects whether a worker is wearing a helmet and safety vest. The system uses Artificial Intelligence (YOLO model) for real-time detection and integrates with an STM32 microcontroller to provide alerts and control access.

⸻

🎯 Objective

* To automate PPE detection in industrial environments
* To reduce human supervision and errors
* To provide real-time alerts and access control

⸻

⚙️ System Architecture
Camera → AI Detection (YOLO) → Decision Logic → STM32 → (LED + Buzzer + Servo)
🧠 Features

* Real-time PPE detection using webcam
* Detects helmet and safety vest
* Serial communication between Python and STM32
* Automated gate control using servo motor
* Buzzer alert for safety violation
* LED indication for system status

⸻

🛠️ Technologies Used

Software:

* Python
* OpenCV
* Ultralytics YOLO
* PySerial

Hardware:

* STM32 Blue Pill
* USB Webcam
* Servo Motor
* Buzzer
* LED
* USB to TTL Converter

⸻

🔧 Working Principle

* Camera captures live video
* YOLO model detects helmet and vest
* System decides SAFE / UNSAFE
* Signal sent to STM32 via serial communication
* STM32 controls:
    * Servo (Gate open/close)
    * Buzzer (Alert)
    * LED (Status indication)
🚀 How to Run

1. Connect webcam and STM32
2. Upload code to STM32 (Arduino IDE)
3. Run Python detection script
4. Ensure correct serial port (/dev/cu.usbserial-XXXX)
5. System will start real-time monitoring

⸻

📸 Project Demo

(Add your images here — hardware setup, detection output, etc.)

⸻

📈 Future Improvements

* Add detection for gloves, shoes, goggles
* Face recognition for worker identification
* Cloud-based monitoring system
* Mobile app integration

⸻

⚠️ Limitations

* Dependent on lighting conditions
* Limited camera coverage
* Accuracy depends on trained model

⸻

👩‍💻 Author

Sneha Pawar ❤️    
