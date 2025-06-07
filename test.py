import cv2
import numpy as np
import time

# Initialize webcam
cap = cv2.VideoCapture(0)  # 0 for default webcam
if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

# Create blank image for grade output window
grade_window = np.zeros((100, 300, 3), dtype=np.uint8)  # 300x100 black image

def detect_color(frame):
    # Convert to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Define ROI (Region of Interest) - adjust coordinates based on your setup
    x, y, w, h = 200, 150, 200, 100  # Example: center of 640x480 frame
    roi = rgb[y:y+h, x:x+w]

    # Calculate average RGB values
    avg_color = np.mean(roi, axis=(0, 1))
    r, g, b = avg_color

    # Color classification (adjust thresholds based on testing)
    if 20 <= r <= 50 and 10 <= g <= 40 and 10 <= b <= 30:
        grade = 'A'  # Dark brown (Grade A)
    elif 60 <= r <= 100 and 30 <= g <= 60 and 20 <= b <= 40:
        grade = 'B'  # Reddish-brown (Grade B)
    else:
        grade = 'Cuts'  # Beans not matching Grade A or B

    return grade, (r, g, b)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame")
        break

    # Detect color
    grade, avg_rgb = detect_color(frame)

    # Output grade and RGB values to console
    print(f"Grade: {grade}, Average RGB: ({avg_rgb[0]:.1f}, {avg_rgb[1]:.1f}, {avg_rgb[2]:.1f})")

    # Draw ROI rectangle and grade on main video frame
    x, y, w, h = 200, 150, 200, 100
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(frame, f"Grade: {grade}", (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Update grade window
    grade_window.fill(0)  # Clear to black
    cv2.putText(grade_window, f"Grade: {grade}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

    # Display both windows
    cv2.imshow('Vanilla Bean Color Detection', frame)
    cv2.imshow('Grade Output', grade_window)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Delay to simulate bean processing (adjust based on conveyor speed)
    time.sleep(0.5)

# Cleanup
cap.release()
cv2.destroyAllWindows()