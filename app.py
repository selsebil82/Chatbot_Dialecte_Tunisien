# imports
import os

from flask import Flask, render_template, request

import ChatBot_Application
from chatbot import ChatBot

app = Flask(__name__)

# def __init__(self):


# create chatbot
# englishBot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
# trainer = ChatterBotCorpusTrainer(englishBot)
# trainer.train("chatterbot.corpus.english") #train the chatter bot for english
# define app routes
i = 0


@app.route("/")
def index():
    global i
    i = 0
    return render_template("index.html")


@app.route("/get")
# function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    response = ChatBot_Application.chatbot_response(userText)
    global i
    i = i + 1
    return [str(response), int(i)]
    # str(englishBot.get_response(userText))


@app.route("/mic")
# function for the bot response
def get_bot_response1():
    userText = request.args.get('msg')
    ai = ChatBot(name="TeamAI")
    inp = ai.speech_to_text()
    return str(inp)


@app.route("/playsound")
# function for the bot response
def get_bot_sound():
    texte = request.args.get('text')
    ai = ChatBot(name="TeamAI")
    ai.text_to_speech(texte)


if __name__ == "__main__":
    app.run(ssl_context='adhoc',port=int(os.getenv('PORT', 4444)))
