import requests

API_URL = "http://127.0.0.1:5000/predict"
image_path = r"D:\yolo_v8_ver2\api\ss.png"  

with open(image_path, "rb") as f:
    response = requests.post(API_URL, files={"file": f})


print(response.json())
