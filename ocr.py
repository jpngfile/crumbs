#!/usr/bin/env python
import requests

subscription_key = "e4f9a2574d75482597cd04bb93cfb3e0"
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
vision_analyze_url = vision_base_url + "analyze"
ocr_url = vision_base_url + "ocr"

#image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Broadway_and_Times_Square_by_night.jpg/450px-Broadway_and_Times_Square_by_night.jpg"
#image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Atomist_quote_from_Democritus.png/338px-Atomist_quote_from_Democritus.png"


headers  = {'Ocp-Apim-Subscription-Key': subscription_key }
#params   = {'visualFeatures': 'Categories,Description,Color'}
params   = {'language': 'unk', 'detectOrientation ': 'true'}
#data     = {'url': image_url}
files = {'file': open('legendMoviePoster.jpg', 'rb')}
response = requests.post(ocr_url, headers=headers, params=params, files=files)
response.raise_for_status()
analysis = response.json()

print(analysis)
