import requests
# r = requests.post("http://127.0.0.1:5000/connect/", 
#     headers={'Content-Type': 'application/json'}, 
#     data = {"key":"value"})



r = requests.post("http://127.0.0.1:5000/connect/", json={"key":"value"})

