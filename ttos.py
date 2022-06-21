from gtts import gTTS


def saveAudio(text,name):
    if ( name == " " or name == "" ):
        name="default"
    mytext = text
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    fname = name+".mp3"
    myobj.save(fname)