import requests

response = requests.get("http://51.20.122.112:8080")

if (response.status_code):
    print("nginx up!")
else:
    print("nginx is down!")