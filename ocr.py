#!/usr/bin/env python
import requests
import time

subscription_key = "e4f9a2574d75482597cd04bb93cfb3e0"
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
ocr_url = vision_base_url + "ocr"
text_recognition_url = vision_base_url + "RecognizeText"

image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Cursive_Writing_on_Notebook_paper.jpg/800px-Cursive_Writing_on_Notebook_paper.jpg"

image_path = "testImages/backlog.jpg"
image_data = open(image_path, 'rb').read()

headers    = {
    'Ocp-Apim-Subscription-Key': subscription_key, 
    "Content-Type": "application/octet-stream"
}
params   = {'language': 'unk', 'detectOrientation ': 'true'}
data = {'url': image_url}
#files = {'file': open('testImages/backlog.jpg', 'rb')}
response = requests.post(ocr_url, headers=headers, params=params, data=image_data)
response.raise_for_status()
print(response.json())

print("Text recognition post")

params = {'handwriting': True}
response = requests.post(text_recognition_url, headers=headers, params=params, data=image_data)
response.raise_for_status()
print(response.json())
operation_url = response.headers["Operation-Location"]
print(operation_url)
analysis = {}
while not "recognitionResult" in analysis:
    response_final = requests.get(operation_url, headers=headers)
    analysis = response_final.json()
    time.sleep(1)
print(analysis)

#analysis = response.json()
#print(analysis)

#line_infos = [region["lines"] for region in analysis["regions"]]
#word_infos = []
#for line in line_infos:
#    for word_metadata in line:
#        for word_info in word_metadata["words"]:
#            word_infos.append(word_info)
#
#print(word_infos)
