import requests

response = requests.get('https://w3schools.com/python/demopage.htm')
print(response.text)