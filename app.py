import os
import cv2
from flask import Flask, render_template, request, redirect, send_from_directory
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Mapping label ke warna (BGR format karena OpenCV)
class_colors = {
    "sedan_jeep_wagon": (255, 255, 0),   # Cyan
    "motor": (255, 0, 0),                # Biru
    "angkutan_sedang": (0, 255, 255),    # Kuning
    "tidak_bermotor": (255, 0, 255),     # Ungu
    "bus": (0, 128, 255),                # Oranye
    "mikro_truk": (0, 255, 0),           # Hijau
    "truk_2_sumbu": (0, 0, 255),         # Merah
    "truk_3_sumbu": (203, 192, 255)      # Pink
}

# Load class names
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
vehicle_classes = ["angkutan_sedang", "bus", "mikro_truk", "motor", "sedan_jeep_wagon", "tidak_bermotor", "truk_2_sumbu", "truk_3_sumbu"]

# Load YOLOv4-tiny
net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")
layer_names = net.getUnconnectedOutLayersNames()

def detect_and_count(input_path, output_path):
    conf_threshold = 0.5
    nms_threshold = 0.3

    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'avc1'), fps, (width, height))
    if not out.isOpened():
        print("[ERROR] VideoWriter gagal dibuka.")
        return

    line_y = int(height * 0.75)  # Garis horizontal di 75% tinggi (agak ke bawah)
    total_counts = {cls: 0 for cls in class_colors}
    previous_centers = {}

    frame_id = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_id += 1

        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        outputs = net.forward(layer_names)

        class_ids, confidences, boxes = [], [], []
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > conf_threshold:
                    center_x, center_y, w, h = (detection[0:4] * [width, height, width, height]).astype(int)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
        current_centers = {}

        if indexes is not None:
            for i in indexes.flatten():
                label = str(classes[class_ids[i]])
                if label not in class_colors:
                    continue
                x, y, w, h = boxes[i]
                color = class_colors[label]

                center = (x + w // 2, y + h // 2)
                current_centers[i] = center

                # Tracking sederhana: hitung saat center_y melewati garis
                if i in previous_centers:
                    prev_y = previous_centers[i][1]
                    curr_y = center[1]
                    if prev_y < line_y <= curr_y:
                        total_counts[label] += 1

                # Gambar bounding box dan label
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        previous_centers = current_centers

        # Gambar garis counting
        cv2.line(frame, (0, line_y), (width, line_y), (0, 255, 255), 2)
        y_offset = 30
        for cls, count in total_counts.items():
            cv2.putText(frame, f"{cls}: {count}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, class_colors[cls], 2)
            y_offset += 20

        out.write(frame)

        if os.path.exists(output_path):
            print(f"[INFO] Video berhasil disimpan di: {output_path}")
            print(f"[INFO] Ukuran file: {os.path.getsize(output_path)} bytes")
        else:
            print("[ERROR] File output tidak ditemukan.")

    cap.release()
    out.release()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video = request.files["video"]
        if video:
            path = os.path.join(app.config['UPLOAD_FOLDER'], "input.mp4")
            video.save(path)
            output_path = os.path.join(OUTPUT_FOLDER, "output.mp4")
            detect_and_count(path, output_path)
            return redirect("/result")
    return render_template("index.html")


@app.route("/result")
def result():
    return render_template("result.html")

@app.route('/static/<path:path>')
def send_video(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(debug=True)
