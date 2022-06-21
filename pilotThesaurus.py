import urllib.parse
import requests

def sThe(word):
    The_api = 'https://dictionaryapi.com/api/v3/references/thesaurus/json/'
    key='?key=e98821b5-afd2-4629-944e-f81a6e560e14'
    theList = []
    # url_The = The_api + urllib.parse.urlencode(word)+key
    url_The = The_api+word+key
    try:
        json_data_The = requests.get(url_The).json()
        """for temp in range(0,10):
            print(json_data_The[temp]["word"])"""
        for i in json_data_The:
            for j in i['meta']['syns']:
                for k in range(0, len(j)):
                    theList.append(j[k])
        return theList
        # print(json_data_The[0]['syns'])
    except:
        return 0