import requests

def autoc(fwd, sl):
    suggList=[]

    text = 'http://localhost:8080/'+fwd+'/'+sl
    # print(text)
    try:
        data = requests.get(text).json()
        if data == {}:
            suggList.append('Decoding JSON has failed')
            suggList.append('suggestions not available')
        else:
            for word in data.keys():
                suggList.append(word)

    except ValueError:
        suggList.append('Decoding JSON has failed')
        suggList.append('suggestions not available')
    return suggList



