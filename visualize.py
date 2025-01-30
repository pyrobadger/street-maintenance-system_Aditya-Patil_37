import cv2
import matplotlib.pyplot as plt
import json


detection_results = {
    "detections": [
        {"class": "pothole", "confidence": 0.805, "x1": 513, "x2": 684, "y1": 331, "y2": 387},
        {"class": "pothole", "confidence": 0.767, "x1": 608, "x2": 754, "y1": 268, "y2": 305},
        {"class": "pothole", "confidence": 0.765, "x1": 0, "x2": 408, "y1": 160, "y2": 413},
        # Add more detections...
    ]
}


image_path = r"D:\yolo_v8_ver2\api\ss.png"  
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


for detection in detection_results["detections"]:
    x1, y1, x2, y2 = detection["x1"], detection["y1"], detection["x2"], detection["y2"]
    confidence = detection["confidence"]
    
    
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
    
   
    label = f"{detection['class']} {confidence:.2f}"
    cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


plt.figure(figsize=(10, 6))
plt.imshow(image)
plt.axis("off")
plt.show()
