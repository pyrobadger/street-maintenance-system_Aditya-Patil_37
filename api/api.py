from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import cv2
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)
CORS(app) 


model = YOLO(r"D:\yolo_v8_ver2\api\best.pt")  
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    
    results = model(image)

   
    output = []
    for result in results:
        for box in result.boxes:
            output.append({
                'x1': int(box.xyxy[0][0]),
                'y1': int(box.xyxy[0][1]),
                'x2': int(box.xyxy[0][2]),
                'y2': int(box.xyxy[0][3]),
                'confidence': float(box.conf[0]),
                'class': model.names[int(box.cls[0])]
            })

    return jsonify({'detections': output})

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Runs on http://127.0.0.1:5000
