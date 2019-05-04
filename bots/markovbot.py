from utils import beat
import numpy as np
import pandas as pd
from collections import Counter

class MarkovBot:
    def __init__(self, transition_prob):
        '''instantiate with given transition prob matrix'''
        self.transition_prob = transition_prob
        self.states = list(transition_prob.keys())

    def next_state(self, current_state):
        '''generate next state with stochastic probabilities'''
        current_options = self.transition_prob[current_state]
        x = np.random.choice(
            list(current_options.keys()),
            p=list(current_options.values()))
        return x

    def predict(self,game):
        '''predict player's throw based on last play'''
        pred = self.next_state(game["player"]+game["bot"])
        return pred

    def throw(self,game):
        '''throw the opposite of player's predicted throw'''
        y = self.predict(game)
        return beat(y)

    def update_transition_matrix(self,game_history):
        '''update transition matrix based on new game_history'''
        # instantiate transition matrix, let's start at ~1/3,
        # so probabilities don't swing too wildly in the beginning
        transition_count = {
        'paperpaper': {'paper': 3,'rock':3,'scissors':3},
        'paperrock': {'paper': 3,'rock':3,'scissors':3},
        'paperscissors': {'paper': 3,'rock':3,'scissors':3},
        'rockpaper': {'paper': 3,'rock':3,'scissors':3},
        'rockrock': {'paper': 3,'rock':3,'scissors':3},
        'rockscissors': {'paper': 3,'rock':3,'scissors':3},
        'scissorspaper': {'paper': 3,'rock':3,'scissors':3},
        'scissorsrock': {'paper': 3,'rock':3,'scissors':3},
        'scissorsscissors': {'paper': 3,'rock':3,'scissors':3}}
        # update transition_count based on new game_history
        for i in self.states:
            for j in ["paper","rock","scissors"]:
                transition_count[i][j] = transition_count[i][j] + Counter(list(zip(game_history["outcome"],game_history["next_play"])))[(i,j)]
        # convert from count to transition probabilities
        df = pd.DataFrame(transition_count)
        for i in list(df.columns):
            df[i] = df[i]/sum(df[i])
        # convert back to dictionary to feed into Markov Chain
        transition_prob = df.to_dict()
        return transition_prob
