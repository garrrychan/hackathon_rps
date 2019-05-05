# hackathon_rps
A smart rock paper scissors bot



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