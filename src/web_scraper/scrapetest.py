import requests as req
import json

url = "https://anydice.com/calculator_limited.php"

querystring = {}

payload = {
    'program': '''
    output 1d20 > 10 named "attackTest1"
    output 1d20 > 15 named "attackTest2"
    '''
}

headers = {
    ##"cookie": "anydice=e99494286ddf8112367ddc9b39090a9b"
}

response1 = req.post(url, data=payload)

dataDictionary = json.loads(response1.content)

print(dataDictionary["distributions"])

##print(response1.text)