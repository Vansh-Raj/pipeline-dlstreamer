# crowd_counter.py (inside /app in container)
import cv2
import numpy as np
from openvino.runtime import Core
from collections import deque

ie = Core()
model = ie.read_model(model="/app/models/person-detection-0200.xml")
compiled_model = ie.compile_model(model=model, device_name="CPU")
input_layer = compiled_model.input(0)
output_layer = compiled_model.output(0)

def draw_boxes(frame, detections, confidence_threshold=0.5):
    h, w = frame.shape[:2]
    count = 0
    for det in detections[0][0]:
        if det[2] > confidence_threshold:
            count += 1
            xmin = int(det[3] * w)
            ymin = int(det[4] * h)
            xmax = int(det[5] * w)
            ymax = int(det[6] * h)
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
    return frame, count

def main():
    cap = cv2.VideoCapture("/app/sample.mp4")  # replace with input if needed
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        input_image = cv2.resize(frame, (256, 256))
        input_image = input_image.transpose((2, 0, 1))[np.newaxis, :]
        result = compiled_model([input_image])[output_layer]
        frame, count = draw_boxes(frame, result)
        cv2.putText(frame, f"People Detected: {count}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
        cv2.imshow("Crowd Detection", frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
