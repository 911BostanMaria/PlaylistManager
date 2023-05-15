import request
from django.contrib.sites import requests

response = requests.get('http://127.0.0.1:8000/Songs')
print(response.json())
