import urllib.parse
import requests


Dict_api = 'https://dictionaryapi.com/api/v3/references/collegiate/json/'
key = '?key=db9d443b-e7b7-40a8-b3aa-9ecc9b46c10c'


word = input("Enter a word : ")

# url_The = The_api + urllib.parse.urlencode(word)+key
url_Dict = Dict_api+word+key
json_data_Dict = requests.get(url_Dict).json()

for word in json_data_Dict[0]["def"]:
    for list in word["sseq"][0]:
        print(list)