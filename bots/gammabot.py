import pickle
import random
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from utils import beat

### medium "Gamma" bot ####

class GammaBot:
    def __init__(self):
        options = ['rock', 'paper', 'scissors']
        player = np.random.choice(options)
        computer = np.random.choice(options)
        # spoof first throw randomly so I can predict
        # Ignore after since new_data grabs last data point only
        self.history = {'player': [player], 'bot': [computer]}

    def predict(self):
        # mapper function
        throw_mapper = LabelEncoder()
        throw_mapper.fit(['rock', 'paper', 'scissors'])
        # loading a random forest model from pickled file
        pipe = pickle.load(open("pipe.pkl", "rb"))
        # new piece of data from history
        new_data = pd.DataFrame([{'player': self.history["player"][-1],'computer': self.history["bot"][-1]}])
        # predict your throw
        # apply transform to data, and then predict with final estimator
        pred = throw_mapper.inverse_transform(pipe.predict(new_data.apply(throw_mapper.transform)))[0]
        # y is bot throw
        y = beat(pred)
        # append bot throw to history
        self.history['bot'].append(y)
        return y

    def throw(self, y):
        x = self.predict()
        # append player's throw to history
        self.history['player'].append(y)
        # return what I should throw
        return x
