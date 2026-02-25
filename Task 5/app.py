from flask import Flask, render_template, request
import os
from ultralytics import YOLO
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'images'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load YOLOv8 model (pre-trained)
model = YOLO('yolov8n.pt')  # smallest model for speed

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        file = request.files["media"]
        if file:
            # Save uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Run YOLO detection
            results = model(file_path)

            # Prepare path to save annotated image
            annotated_path = os.path.join(app.config['UPLOAD_FOLDER'], "detected_" + file.filename)

            # Get annotated image as array and save
            annotated_img = results[0].plot()
            cv2.imwrite(annotated_path, annotated_img)

            result = f"Detection done! Check: {annotated_path}"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)