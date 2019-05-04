import random

# Easy - Random Bot
class EpsilonBot:
    def __init__(self):
        self.history = {'player': [], 'bot': []}

    def predict(self):
        y = random.choice(['rock', 'paper', 'scissors'])
        self.history['bot'].append(y)
        return y

    def throw(self, y):
        x = self.predict()
        self.history['player'].append(y)
        return x
