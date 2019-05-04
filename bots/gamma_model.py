from sklearn.pipeline import Pipeline
import pickle
import random
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from utils import beat

# Medium - GammaBot
raw = pd.read_excel('data/Rock_Paper_Scissors_Raw.xlsx')

# keep it small to start
df = raw.head(10000).copy()

# groupby shift to get next throw
df['player_one_throw_next'] = df.groupby('game_id')['player_one_throw'].shift(-1)

# kiss
df = df[['player_one_throw', 'player_two_throw', 'player_one_throw_next']]
df = df.rename(columns={
    'player_one_throw': 'player',
    'player_two_throw': 'computer',
    'player_one_throw_next': 'player_next'
})

# drop out no responses
df = df.replace(0, np.nan).dropna()

# map throws
df = df.replace({1: 'rock', 2: 'paper', 3: 'scissors'})

# reverse out the throw mapper
throw_mapper = LabelEncoder()
throw_mapper.fit(['rock', 'paper', 'scissors'])
throw_mapper.transform(['rock', 'paper', 'scissors'])
df = df.apply(throw_mapper.transform)

# there's 3 classes
# throw_mapper.classes_

# df["player"].value_counts()
# rock 1: 2361
# paper 0: 2141
# scissors 2: 1992

# identify the X and y blocks
target = 'player_next'
y = df[target]
X = df.drop(target, axis=1)

# train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# try to be better than random model 'EpsilonBot'
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
model.score(X_train, y_train)
model.score(X_test, y_test)

print(cross_val_score(model, X_train, y_train, cv=5).mean())
print(cross_val_score(model, X_test, y_test, cv=5).mean())

# grid search over n estimators, max samples
params = {
    'n_estimators': [5, 10, 15],
    'max_depth': [None, 1, 2],
    'min_samples_split': [3, 4, 5]
}

# instantiate
rf_grid_search = GridSearchCV(model, param_grid=params, cv=5)
rf_grid_search.fit(X_train, y_train)

print(rf_grid_search.best_score_)
print(rf_grid_search.best_params_)
print(rf_grid_search.score(X_test,y_test))

# Adjust hyperparameters. However, this didn't improve score, performance trailed off.
model = RandomForestClassifier(random_state=42, min_samples_split= 3, n_estimators= 10)
model.fit(X_train, y_train)

# create a pipeline
pipe = Pipeline([("model", model)])

# serialize our model to a file
pickle.dump(pipe, open("pipe.pkl", "wb"))
