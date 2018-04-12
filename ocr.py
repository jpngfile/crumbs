#!/usr/bin/env python
import requests

subscription_key = "e4f9a2574d75482597cd04bb93cfb3e0"
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
ocr_url = vision_base_url + "ocr"

headers  = {'Ocp-Apim-Subscription-Key': subscription_key }
params   = {'language': 'unk', 'detectOrientation ': 'true'}
files = {'file': open('testImages/stopSign.png', 'rb')}
response = requests.post(ocr_url, headers=headers, params=params, files=files)
response.raise_for_status()
analysis = response.json()

line_infos = [region["lines"] for region in analysis["regions"]]
word_infos = []
for line in line_infos:
    for word_metadata in line:
        for word_info in word_metadata["words"]:
            word_infos.append(word_info)

print(word_infos)
