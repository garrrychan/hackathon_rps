# hackathon_rps
A smart rock paper scissors bot

Recently, I participated in my first ever hackathon at [Bitmaker General Assembly](https://bitmaker.co/courses/data-science)! To say it was an eye opening experience would be understatement. I had to apply what I've learned so far, by combining concepts from data science and software development. Additionally, it was an exercise to work in pairs, tackle unstructured problems, and think outside the box.

### The challenge

Within a day, I was challenged to create a 'smart' rock, paper and scissors bot that can beat a human over 50 games. This would test my data wrangling, predictive modeling, statistics and web development skills.



**My bot must:** 

* Be built on top of a machine learning algorithm 

* Be able to prove that it's not "peeking" at user input (target leakage)

* Have a flask front-end that can accept user input

* Keep track of wins and losses

  

**Stretch goals:** 

* An ability to switch between different "engines" (naive, random, hard-coded, algorithmic) 
* An ability for your bot to learn from my specific play-style and update turn-over-turn
* Flask that's prettier than just a couple of white input boxes
* Your bot to a hosted website on the internet, somehow, somewhere

------

### Creating my first web app

At this point, I had minimal exposure to web development and databases, so I made the most of my current toolkit. By the end of the hackathon, my teammate and I were nearly there in creating a fully functional app. Over the past week, with the help of my instructor, I refactored and completed my first app. What a feeling!

Tech stack: My web application is written in Python, built on Flask, and hosted on Heroku.

There are 3 difficulties/models for you to play with.

| **1. Easy - Naive random model**                    | The bot throws rock, paper, scissors with 1/3 probability each. You are expected to win about 50% of the time. |
| --------------------------------------------------- | ------------------------------------------------------------ |
| **2. Medium - Deterministic (random forest) model** | The bot is trained on 450K+ previously played games. You are expected win less than 50% of the time. |
| **3. Hard - Stochastic (markov chain) model**       | As you play more, the bot learns your specific playing style and it becomes be harder to win! |

Without further ado, here it is (hosted on Heroku, another milestone!).**https://rps-bot-garry.herokuapp.com/**

Take a break and see if you can beat my bot 😉

---

### Data 

The data is in one Excel file.

* `Rock_Paper_Scissors_Raw.xlsx` - 455180 gamelogs of rock, paper scissors, including:
* `game_round_id.csv` - the game round
* `player_one_throw.csv ` - int of 1, 2 or 3, representing rock, paper or scissors
* `player_two_throw.csv` - int of 1, 2 or 3, representing rock, paper or scissors



Data dictionary:

- `game_id` = a shared url, played between the same two players 
- `game_round_id` = first to 1 win, 3 wins, or 5 wins
- throws: `1` = rock, `2` = paper, `3` = scissors, `0` = no input