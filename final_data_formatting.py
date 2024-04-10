import pandas as pd

tweet_data = pd.read_csv('aggregated_tweet_data.csv', low_memory = False).set_index('id')
tweet_data = tweet_data.drop('Unnamed: 0', axis = 1)
user_data = pd.read_csv('cleaned_user_data.csv').set_index('id')

data = user_data.join(tweet_data).dropna()

data.to_csv('final_data.csv')