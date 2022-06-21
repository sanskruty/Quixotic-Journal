import urllib.parse
import requests


def sRhy(word):
    rhy_api = 'https://rhymebrain.com/talk?function=getRhymes&'

    url_rhy = rhy_api + urllib.parse.urlencode({'word':word})

    try:
        json_data_rhy = requests.get(url_rhy).json()
        #json_data_syn = requests.get(url_syn).json()
        #print(json_data_rhy)
        listRhy = []
        for word in json_data_rhy:
            listRhy.append(word['word'])
        return listRhy
        # count =0
        # print("Rhyming words :")
        # for itr_rhy in json_data_rhy:
        #     print("\t"+itr_rhy["word"])
        #     count = count +1
        # print(count)

        # print(json_data_rhy)"
    except:
        return 0


