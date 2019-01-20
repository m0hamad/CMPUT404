import requests

print(requests.__version__)

print(requests.get('http://www.google.com'))

requests.get('https://raw.githubusercontent.com/m0hamad/CMPUT404/master/lab1.py')