# coding=utf-8
import nltk
from nltk.stem import WordNetLemmatizer

from chatbot import ChatBot

lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import json
import random
from keras.models import load_model

model = load_model('chatbot_Application_model.h5')

intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
labels = pickle.load(open('labels.pkl', 'rb'))


def bank_of_words(s, words, show_details=True):
    bag_of_words = [0 for _ in range(len(words))]
    sent_words = nltk.word_tokenize(s)
    sent_words = [lemmatizer.lemmatize(word.lower()) for word in sent_words]
    for sent in sent_words:
        for i, w in enumerate(words):
            if w == sent:
                bag_of_words[i] = 1
    return np.array(bag_of_words)


def predict_label(s, model):
    # filtering out predictions
    pred = bank_of_words(s, words, show_details=False)
    print("from predict function :",pred)
    response = model.predict(np.array([pred]))[0]
    ERROR_THRESHOLD = 0.25
    final_results = [[i, r] for i, r in enumerate(response) if r > ERROR_THRESHOLD]
    final_results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in final_results:
        return_list.append({"intent": labels[r[0]], "probability": str(r[1])})
    return return_list


def Response(ints, intents_json):
    tags = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tags:
            response = random.choice(i['responses'])
            break
        # else:
        #   response = random.choice(list_of_intents[3]['responses'])
    return response


def chatbot_response(msg):
    ints = predict_label(msg, model)
    response = Response(ints, intents)
    return response


def chat(inp):
    print("عسلامة صديقي ، أنا روبوت نجم نجاوبك على أسئلتك المتعلقة بالستاج ولا بالخدمة")
    while True:
       # inp = input("You: ")
        ai = ChatBot(name="team")
        #inp = ai.speech_to_text()
        if inp.lower() == 'quit':
            break
        response = chatbot_response(inp)
        print("\n BOT: " + response + '\n\n')
        ai.text_to_speech(response)


#chat()
