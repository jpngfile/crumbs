#!/usr/bin/env python
import requests
import time

subscription_key = "e4f9a2574d75482597cd04bb93cfb3e0"
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
text_recognition_url = vision_base_url + "recognizeText"

image_path = "testImages/scrumboard.jpg"
image_data = open(image_path, 'rb').read()

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
