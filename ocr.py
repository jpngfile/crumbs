#!/usr/bin/env python
import requests
import time
import io
import pprint
from PIL import Image

pp = pprint.PrettyPrinter(indent=4)
HEADERS = [u'backlog', u'doing', u'done']
def scaleImage(img_file, maxSize):
    size = maxSize, maxSize
    img = Image.open(img_file)
    img_within_limit = all(dimension < limit for dimension, limit in zip(img.size, size))
    if (not img_within_limit):
        img.thumbnail(size, Image.ANTIALIAS)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    return img_bytes

def getWords(azure_response):
    word_list = []
    for line in azure_response['recognitionResult']['lines']:
        for word in line['words']:
            word_list.append(word)
    return word_list

def getLineOverlap(xCoords1, xCoords2):
    x1, x3 = xCoords1
    x2, x4 = xCoords2
    if (x1 < x2):
        return min(x3 - x2, x4 - x2)
    else:
        return min(x3 - x1, x4 - x1)

def mean(a, b):
    return (a + b) / 2

def getXCoordsFromWord(word):
   box = word[u'boundingBox']
   # 0 and 6 are left x coords
   # 2 and 4 are right x coords
   xLeft = mean(box[0], box[6])
   xRight = mean(box[2], box[4])
   return (xLeft, xRight)

def getHeaderDict(headers):
    headerDict = {}
    for header in headers:
        xCoords = getXCoordsFromWord(header)
        headerDict[header[u'text']] = xCoords
    return headerDict

def getScrumDict(word_list):
    scrum_headers = [word for word in word_list if word[u'text'].lower() in HEADERS]
    task_words = [word for word in word_list if word not in scrum_headers]
    header_dict = getHeaderDict(scrum_headers)
    scrum_dict = {}
    for header in scrum_headers:
        scrum_dict[header[u'text']] = []

    for word in task_words:
        wordXCoords = getXCoordsFromWord(word)
        matching_header,_ = max(header_dict.items(), key=lambda header: getLineOverlap(wordXCoords, header[1]))
        scrum_dict[matching_header].append(word[u'text'])
    return scrum_dict

def getAzureAnalysis(image_data):
    subscription_key = "e4f9a2574d75482597cd04bb93cfb3e0"
    vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
    text_recognition_url = vision_base_url + "recognizeText"
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
    return analysis

def parseAnalysis(analysis):
    word_list = getWords(analysis)
    return getScrumDict(word_list)

def getSampleAnalysis():
    subscription_key = "e4f9a2574d75482597cd04bb93cfb3e0"
    vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
    text_recognition_url = vision_base_url + "recognizeText"

    image_path = "testImages/dummyScrumboard.jpg"
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
    return analysis

def getSampleScrumDict():
    sample_analysis = getSampleAnalysis()
    word_list = getWords(sample_analysis)
    scrum_headers = getScrumDict(word_list)
    return scrum_headers
