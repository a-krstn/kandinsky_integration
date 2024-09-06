from celery import shared_task
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.files import File
import json
import time
import base64
import os

from .models import Article

import requests


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=576):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)


@shared_task
def get_image(article_pk):
    article = get_object_or_404(Article, id=article_pk)
    print(f'Запрос в API: {article.title}')
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', os.getenv('KANDINSKY_API_KEY'), os.getenv('KANDINSKY_SECRET_KEY'))
    model_id = api.get_model()
    print(type(model_id), model_id)
    uuid = api.generate(article.body, model_id)
    print(type(uuid), uuid)
    images = api.check_generation(uuid)
    print(type(images))
    image_base64 = images[0]
    image_data = base64.b64decode(image_base64)

    # with open(f"{settings.MEDIA_URL}image_{article_pk}.jpg", "wb") as file:
    # with open(f"{settings.MEDIA_URL}image_{article_pk}.jpg", "w+") as file:
    # imagead.full_photo.save("NowHiring.jpg", File(open("C:\\NowHiring.jpg", "rb")))
    # File(open(f"image_{article_pk}.jpg", "rb"))

    try:
        with open(f"image_{article_pk}.jpg", "wb") as file:
            file.write(image_data)
            # article.image = file
            # article.save(f"image_{article_pk}.jpg", file)
    except:
        with open(f"image_{article_pk}.jpg", "w+") as file:
            file.write(image_data)
            # article.image = file
    
    article.image.save(f"image_{article_pk}.jpg", File(open(f"image_{article_pk}.jpg", "rb")))

    
