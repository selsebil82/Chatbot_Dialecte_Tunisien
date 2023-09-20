# Build the AI
import gtts
import speech_recognition as sr
import pyttsx3

from gtts import gTTS
from playsound import playsound


class ChatBot():
    def __init__(self, name):
        self.text = ""
        print("--- starting up", name, "---")
        self.name = name

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=1)
            print("Say something ...")
            audio = recognizer.listen(mic)
        try:
            self.text = recognizer.recognize_google(audio, language="ar-AR")
            print("me --> ", self.text)
        except:
            self.text = "صوتك مش واضح ... عاود تكلم "
            print("me -->  ERROR")
        return self.text

    def text_to_speech(self, resp):
        # pyttsx3.speak(resp)
        # engine = pyttsx3.init()
        # engine.say(resp)
        # engine.runAndWait()
        tts = gtts.gTTS(resp, lang="ar", slow=False)
        tts.save("hola.mp3")
        playsound("hola.mp3")

def wake_up(self, text):
    return True if self.name in text.lower() else False


# Run the AI
if __name__ == "__main__":
    ai = ChatBot(name="maya")

