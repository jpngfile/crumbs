#!/usr/bin/env python
import requests
import time
import io
from PIL import Image

def scaleImage(img_file, maxSize):
    size = maxSize, maxSize
    img = Image.open(img_file)
    img_within_limit = all(dimension < limit for dimension, limit in zip(img.size, size))
    if (not img_within_limit):
        img.thumbnail(size, Image.ANTIALIAS)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    return img_bytes

subscription_key = "e4f9a2574d75482597cd04bb93cfb3e0"
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
text_recognition_url = vision_base_url + "recognizeText"

image_path = "testImages/bigScrumboard.jpg"
image_file = open(image_path, 'rb')
image_data = scaleImage(image_file, 3200).getvalue()

headers    = {
    'Ocp-Apim-Subscription-Key': subscription_key, 
    "Content-Type": "application/octet-stream"
}
params = {'handwriting': True}
response = requests.post(text_recognition_url, headers=headers, params=params, data=image_data)
response.raise_for_status()
operation_url = response.headers["Operation-Location"]
print(operation_url)

analysis = {}
while not "recognitionResult" in analysis:
    response_final = requests.get(operation_url, headers=headers)
    analysis = response_final.json()
    time.sleep(1)
print(analysis)
