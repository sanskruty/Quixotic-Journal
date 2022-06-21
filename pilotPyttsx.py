import pyttsx3


def playAudio(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return 1
    except:
        print("no return")
        return 0
#
# # playAudio("Hello")
#     engine = pyttsx3.init()
#     engine.say(text)
#     engine.runAndWait()
#     return 1
