from nltk.corpus import wordnet as wn
# wd = input('word :')

def sDef(word):
    try:
        defin = wn.synsets(word)
        return defin[0].definition()
    except:
        return 0
# print(sDef(wd))