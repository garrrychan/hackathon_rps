from collections import Counter

def emoji_to_text(emoji):
    '''Convert emoji input to text'''
    lookup = {'🤘': 'rock', "📝": 'paper', '✂️': 'scissors'}
    return lookup.get(emoji)

def evaluate(player, computer):
    '''Evaluate winner'''
    outcomes = {
        ('rock', 'scissors'): 'win',
        ('rock', 'paper'): 'lose',
        ('paper', 'rock'): 'win',
        ('paper', 'scissors'): 'lose',
        ('scissors', 'rock'): 'lose',
        ('scissors', 'paper'): 'win'
    }
    if player == computer:
        return 'tie'
    return outcomes[player, computer]

def win_rate_fn(results):
    '''Calculate win rate'''
    try:
        return Counter(results)["win"]/(Counter(results)["win"]+Counter(results)["lose"])
    except:
         return 0.0

def beat(prediction):
    '''Have bot throw opposite of prediction'''
    if prediction == "paper":
        throw = "scissors"
    if prediction == "rock":
        throw = "paper"
    if prediction == "scissors":
        throw = "rock"
    return throw

start = 0
game_history = { "outcome": [], "next_play": []}
def log_game(game):
    '''Keep track of game history. We don't know the next_play
    until following round'''
    global start
    # first throw, next play is "None", since we don't know yet
    if start == 0:
        game_history["outcome"].append(game["player"]+game["bot"])
        game_history["next_play"].append("None")
        start += 1
        return game_history
    game_history["outcome"].append(game["player"]+game["bot"])
    game_history["next_play"].append(game["player"])
    return game_history
