import requests
from django.shortcuts import render
from django.http import HttpResponse
import base64
from django.views.decorators.csrf import csrf_exempt
import json
import cv2
import numpy as np


@csrf_exempt
def home(request):
    exist = 0
    if request.method == 'POST':
        try:
            image_data = request.body
            image_obj = json.loads(image_data)
            image = image_obj['image']
            one_img_bytes = bytes(image['img']['data']['data'])
            one_img_data_uri = base64.b64encode(one_img_bytes).decode('utf-8')
            image1_bytes = base64.b64decode(one_img_data_uri)
            image1_array = np.frombuffer(image1_bytes, dtype=np.uint8)
            image1 = cv2.imdecode(image1_array, cv2.IMREAD_COLOR)

            response = requests.get('http://localhost:5000/Posts/getImages')
            images = response.json()

            imagesTab = []
            for i in range(len(images)):
                img_bytes = bytes(images[i]['img']['data']['data'])
                img_data_uri = base64.b64encode(img_bytes).decode('utf-8')
                imagesTab.append(img_data_uri)

            for image in imagesTab:
                image_bytes = base64.b64decode(image)
                image_array = np.frombuffer(image_bytes, dtype=np.uint8)
                image2 = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                if image1.shape != image2.shape:
                    height = min(image1.shape[0], image2.shape[0])
                    width = min(image1.shape[1], image2.shape[1])
                    image1_resized = cv2.resize(image1, (width, height))
                    image2_resized = cv2.resize(image2, (width, height))
                else:
                    image1_resized = image1
                    image2_resized = image2
                diff = cv2.absdiff(image1_resized, image2_resized)
                diff_mean = np.mean(diff)
                if diff_mean <= 0.0:
                    exist += 1
        except Exception as e:
            print(e)
            return HttpResponse('Error')

        return HttpResponse(exist)
    if request.method == 'GET':
        response = requests.get('http://localhost:5000/Posts/getImages')
        images = response.json()
        imagesTab = []
        for i in range(len(images)):
            img_bytes = bytes(images[i]['img']['data']['data'])
            img_data_uri = base64.b64encode(img_bytes).decode('utf-8')
            imagesTab.append(img_data_uri)
        context = {
            'images': imagesTab
        }
        return render(request, 'home.html', context)
