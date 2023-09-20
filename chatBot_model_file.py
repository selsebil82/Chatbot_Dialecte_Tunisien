import nltk  # prétraiter nos données
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
import json
import pickle  # pour enregistrer nos étiquettes et nos mots.
import numpy as np  # convertir nos données sous forme de tableau
from tensorflow import keras
from keras.layers import Dense, Dropout
from keras.models import Sequential, load_mode
from keras.optimizers import SGD
import random  # pour générer des réponses aléatoires en fonction du message de l'utilisateur.

# ------------------------Déclarer des constantes ------------------------------
words = []
labels = []
docs = []
ignore_list = ['?', '!', '.', ':)', ')', ',', '/', '@', '=', '+', '^', '-', '_', '(', '"', '&']
#

# -----------------------Chargement de notre jeu de données---------------------
dataset = open('intents.json').read()
intents = json.loads(dataset)

# nltk.download('punkt')

# -----------------------Prétraiter les données-------------------------------

for intent in intents['intents']:
    for pattern in intent['patterns']:

        # tokenize each word
        word_token = nltk.word_tokenize(pattern)
        words.extend(word_token)

        # add documents in the corpus : ajouter chaque mot dans doc avec le label (tag) qu'il appartient
        docs.append((word_token, intent['tag']))

        # add to our labels list
        if intent['tag'] not in labels:
            labels.append(intent['tag'])
print("chaque mot avec le label : ", docs)
print("list of lables :", labels)

# nltk.download('wordnet')

# ------------------------lemmatize each word, and sort words by removing duplicates-----------------
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_list]
words = sorted(list(set(words)))
print("list of words : ", words)
# sort labels:
labels = sorted(list(set(labels)))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(labels, open('labels.pkl', 'wb'))

# creating our training data
training_data = []
# creating an empty array for our output (with size same as length of labels):
output = [0] * len(labels)

for doc in docs:
    bag_of_words = []
    pattern_words = doc[0]
    # lemmatize pattern words:
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    print("after lemmatization :", pattern_words)
    for w in words:
        if w in pattern_words:
            bag_of_words.append(1)
        else:
            bag_of_words.append(0)

    output_row = list(output)

    output_row[labels.index(doc[1])] = 1

    training_data.append([bag_of_words, output_row])

print("bag of words :", bag_of_words)
print("pattern of words :", pattern_words)

# convert training_data to numpy array and shuffle the data:
random.shuffle(training_data)
training_data = np.array(training_data, dtype=object)
print("training data array :", training_data)

# Now we have to create training list:
x_train = list(training_data[:, 0])
y_train = list(training_data[:, 1])

# Creating Model:

model = Sequential()
model.add(Dense(128, input_shape=(len(x_train[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]), activation='softmax'))

model.summary()

sgd_optimizer = SGD(lr=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd_optimizer, metrics=['accuracy'])

# fit the model 
history = model.fit(np.array(x_train), np.array(y_train), epochs=200, batch_size=5, verbose=1)

model.save('chatbot_Application_model.h5', history)
