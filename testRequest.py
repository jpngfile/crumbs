#!/usr/bin/env python

import requests

crumbs_url = "http://127.0.0.1:5000/"
upload_url = crumbs_url + "api/upload"

image_path = "testImages/dummyScrumboard.jpg"
image_file = open(image_path, 'rb')
files = {'file': image_file}
data={'team': 'cookies'}
response = requests.post(upload_url, data=data, files=files)
response.raise_for_status()
print(response.json())

