import time
from locust import HttpUser, task, between

import http.client
import mimetypes
import requests


class WebsiteUser(HttpUser):
    # random time between 1 and 3 seconds
    waitTime = between(1, 1)

    @task
    def index_page(self):
        # self.client.get(url='/#home')

        url = "http://35.241.233.235/seldon/seldon/mlflow/api/v1.0/predictions?"

        payload = "{\r\n    \"data\":{\r\n        \"names\":[\r\n            \"fixed acidity\",\r\n            \"volatile acidity\",\r\n            \"citric acid\",\r\n            \"residual sugar\",\r\n            \"chlorides\",\r\n            \"free sulfur dioxide\",\r\n            \"total sulfur dioxide\",\r\n            \"density\",\r\n            \"pH\",\r\n            \"sulphates\",\r\n            \"alcohol\"\r\n        ],\r\n        \"ndarray\":[\r\n            [\r\n                7,\r\n                0.27,\r\n                0.36,\r\n                20.7,\r\n                0.045,\r\n                45,\r\n                170,\r\n                1.001,\r\n                3,\r\n                0.45,\r\n                8.8\r\n            ]\r\n        ]\r\n    }\r\n}"
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text.encode('utf8'))

    # @task
    # def index_page(self):
    #    self.client.get(url='/#about')
