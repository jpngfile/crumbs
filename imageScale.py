#!/usr/bin/env python
import io
from PIL import Image

def scaleImage(imgFile, maxSize):
    size = maxSize, maxSize
    img = Image.open(imgFile)
    imgWithinLimit = all(dimension < limit for dimension, limit in zip(img.size, size))
    if (not imgWithinLimit):
        print("scaled image")
        img.thumbnail(size, Image.ANTIALIAS)
    imgBytes = io.BytesIO()
    img.save(imgBytes, format="JPEG")
    return imgBytes

image_path = "testImages/bigBacklog.jpg"
result_path = "testImages/result.jpg"

imgFile = open(image_path, 'rb')
data=scaleImage(imgFile, 5200)
with open(result_path, 'wb') as out:
    out.write(data.getvalue())
