import requests

url = "http://localhost:8000/analyze-crop"
files = {"file": ("image.jpg", open("new.jpg", "rb"), "image/jpeg")}
response = requests.post(url, files=files)

print(response.json())