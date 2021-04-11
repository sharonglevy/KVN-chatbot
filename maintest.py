import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import pyodbc
import numpy
import tensorflow
import tflearn
import datetime
from datetime import (date, timedelta)
import time
import time_things as tt
import bot_core as bt

import random
import json
import pickle

with open("intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)


    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn")
except:
    model = tflearn.DNN(net)
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")
    
#---------------------------------------------------------------------------------------------------------------------------------

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)

#---------------------------------------------------------------------------------------------------------------------------------

def predictive_function(inp):
    results = model.predict([bag_of_words(inp, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    response = r"I didn't understand you, try again"
    print(inp, "-", results[results_index], tag)
    if results[results_index] > 0.8:

        for tg in data["intents"]:
            if tg['tag'] == tag:
                    
                if tg['tag'] == "email":
                    responses = tg['responses']
                    response = "email"
                    
                elif tg['tag'] == "number":
                    responses = tg['responses']
                    response = "number"

                elif tg['tag'] == "location":
                    responses = tg['responses']
                    response = "location"

                elif tg['tag'] == "goodbye":
                    responses = tg['responses']
                    response = "goodbye"

                else:
                    responses = tg['responses']
                    response = (random.choice(responses))

    return response

#---------------------------------------------------------------------------------------------------------------------------------

def funcion_fecha(inp):
    print("la dooos!! ")
    print(inp)

    if inp == 'Today' or inp == "today":
        today = tt.get_today()
        today = today.strftime("%m/%d/%Y")
        response = today

    elif inp == 'Tomorrow' or inp == "tomorrow":
        tomorrow = tt.get_tomorrow()
        tomorrow = tomorrow.strftime("%m/%d/%Y")
        response = tomorrow

    elif tt.isDateFormat(inp):
        if tt.is_date_valid(inp):
            response = inp

        else: 
            response = "wrong"
    else:
        response = "Not a valid format"

    return response

#---------------------------------------------------------------------------------------------------------------------------------

def funcion_time_ini(inp, fecha):


    if tt.isTimeFormat(inp):

        if (tt.is_ini_valid(inp, fecha))== True:
            response = inp 
        elif (tt.is_ini_valid(inp, fecha)) == False:
            response = "Can't make a reservation in the past. Try again."

    else:
        response = "Not valid. Try again."



    return response

#---------------------------------------------------------------------------------------------------------------------------------

def funcion_time_fin(inp, time_s):
    print("funcion_time_fin")

    if tt.isTimeFormat(inp):
        print("time format")
        if tt.is_end_valid(inp, time_s):
            print("time end valid")
            response = inp

        else:
            response = "Can't end a meeting before it starts. Try again."

    else:
        response = "Not a valid format. Try again."

    return response

#---------------------------------------------------------------------------------------------------------------------------------
def eid_function(inp):
    response = inp
    return response