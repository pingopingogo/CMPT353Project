import pandas as pd

tweet_data = pd.read_csv('aggregated_tweet_data.csv', low_memory = False).set_index('taken_from')
user_data = pd.read_csv('cleaned_user_data.csv').set_index('id')

#cleaning out accounts with missing information
data = user_data.join(tweet_data).dropna()

#removing accounts that only made 1 tweet, not enough info (hourly tweets = inf)
data = data[data['hourly_tweet_mean'] != float('inf')]

def word_count(string):
    return len(string.split())

# add number of words in profile description of account
data['description_word_count'] = data['rawDescription'].apply(word_count)
# username length
data['username_char_count'] = data['username'].apply(len)
# followers vs following ratio
data['following_vs_followers_ratio'] = data['friendsCount']/data['followersCount']
# like vs tweet ratio
data['like_vs_tweet_ratio'] = data['statusesCount']/data['favouritesCount']

# replacing values with inf from columns above (likely if someone has 0 followers, for example)
data = data.replace(float('inf'), 9999).fillna(9999)

# drop irrelevant columns
columns_to_drop = ['displayname', 'rawDescription', 'location', 'username']
data = data.drop(columns_to_drop, axis=1)

data.to_csv('final_data.csv')