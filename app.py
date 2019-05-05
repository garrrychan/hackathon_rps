import random
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
import pickle
from bots.epsilonbot import EpsilonBot
from bots.gammabot import GammaBot
from bots.markovbot import MarkovBot
from collections import Counter
from utils import emoji_to_text, evaluate, win_rate_fn, log_game
from flask import Flask, request, render_template

app = Flask(__name__)
# capture results for win rates
results = []

# home page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/easy', methods=['GET', 'POST'])
def easy():
    game = {}
    bot = EpsilonBot()
    if request.method == 'POST':
        player_throw = emoji_to_text(request.form['player_throw'])
        bot_throw = bot.throw(game)
        result = evaluate(player_throw, bot_throw)
        results.append(result)
        win_rate = win_rate_fn(results)
        game["W"] = Counter(results)["win"]
        game["L"] = Counter(results)["lose"]
        game['result'] = result
        game['player'] = player_throw
        game['bot'] = bot_throw
        game["win_rate"] = round(win_rate*100,2)
    return render_template('easy.html', game=game)

@app.route('/medium', methods=['GET', 'POST'])
def medium():
    game = {}
    bot = GammaBot()
    if request.method == 'POST':
        player_throw = emoji_to_text(request.form['player_throw'])
        bot_throw = bot.throw(player_throw)
        result = evaluate(player_throw, bot_throw)
        results.append(result)
        win_rate = win_rate_fn(results)
        game["W"] = Counter(results)["win"]
        game["L"] = Counter(results)["lose"]
        game['result'] = result
        game['player'] = player_throw
        game['bot'] = bot_throw
        game["win_rate"] = round(win_rate*100,2)
    return render_template('medium.html', game=game)

# game setup for markovbot

# spin up random game 1
options = ['rock', 'paper', 'scissors']
player = np.random.choice(options)
bot = np.random.choice(options)
game = {'W': 0, 'L': 0, 'result': None, 'player': player, 'bot': bot, 'win_rate': 0}

# save the outcomes and play
memory = pd.DataFrame({ "outcome": [], "next_play": []})
memory.to_csv('data/memory.csv', index=False)
del memory

# save the updated transition matrix
memory_transition_prob = pd.DataFrame({
'paperpaper': {'paper': 1/3, 'rock': 1/3,'scissors': 1/3},
'paperrock': {'paper': 1/3, 'rock': 1/3,'scissors': 1/3},
'paperscissors': {'paper': 1/3, 'rock': 1/3,'scissors': 1/3},
'rockpaper': {'paper': 1/3, 'rock': 1/3,'scissors': 1/3},
'rockrock': {'paper': 1/3, 'rock': 1/3,'scissors': 1/3},
'rockscissors': {'paper': 1/3, 'rock': 1/3,'scissors': 1/3},
'scissorspaper': {'paper': 1/3, 'rock': 1/3,'scissors': 1/3},
'scissorsrock': {'paper': 1/3, 'rock': 1/3,'scissors': 1/3},
'scissorsscissors': {'paper': 1/3, 'rock': 1/3,'scissors': 1/3}})
memory_transition_prob.to_csv("data/memory_transition_prob.csv",index=False)
del memory_transition_prob

@app.route('/hard', methods=['GET', 'POST'])
def hard():
    # do not render first dummy game's html
    game_count = 0
    memory_transition_prob = pd.read_csv('data/memory_transition_prob.csv').to_dict()
    # rename 0 to paper, 1 to rock, 2 to scissors
    for i in list(memory_transition_prob.values()):
        i["paper"] = i.pop(0)
        i["rock"] = i.pop(1)
        i["scissors"] = i.pop(2)
    bot = MarkovBot(memory_transition_prob)
    if request.method == 'POST':
        player_throw = emoji_to_text(request.form['player_throw'])
        bot_throw = bot.throw(game)
        result = evaluate(player_throw, bot_throw)
        results.append(result)
        game["W"] = Counter(results)["win"]
        game["L"] = Counter(results)["lose"]
        game['result'] = result
        game['player'] = player_throw
        game['bot'] = bot_throw
        game["win_rate"] = round(win_rate_fn(results)*100,2)
        # load memory of games outcome and next_play
        memory = pd.read_csv('data/memory.csv')
        # update transition matrix for next prediction
        memory_transition_prob = pd.DataFrame(bot.update_transition_matrix(memory))
        # save transition_prob
        memory_transition_prob.to_csv('data/memory_transition_prob.csv',index=False)
        # save memory
        memory = pd.DataFrame(log_game(game))
        memory.to_csv('data/memory.csv',index=False)
        del memory
        del memory_transition_prob
        game_count+= 1
    return render_template('hard.html', game=game, game_count=game_count)

if __name__ == '__main__':
    app.run(debug=True)
