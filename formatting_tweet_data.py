import pandas as pd
import numpy as np

tweets = pd.read_csv('concat_tweets.csv', low_memory = False)

# udf to use, much of the data are strings that are actually lists
def obj_to_list(input):
    if (input == '[]' or input == '0'):
        return([])
    else:
        return(input.split(','))

# returns the num of items in a list to use in apply()
def list_count(input):
    return(len(input))


# dropping rows with corrupted data
tweets = tweets.drop(index = [33219,332168])

# convert tweet date to datetime
tweets['date'] = pd.to_datetime(tweets['date'])

tweets['hashtagCount'] = tweets['hashtags'].fillna('0').astype('string').apply(obj_to_list).apply(list_count)
#tweets = tweets.drop('hashtags')

def is_reply(input):
    if (input == ''):
        return False
    else:
        return True
tweets['isReply'] = tweets['inReplyToTweetId'].apply(is_reply)
# also make something when aggregating for number of unique users replied to, and total number of replies

tweets['mentionCount'] = tweets['mentionedUsers'].fillna('0').apply(obj_to_list).apply(list_count)

# things to agg we are grouping on the variable: 'extracted_from':
# average words per tweet
# highest words per tweet
# lowest words per tweet
# average daily tweet num
# average reply count 
# highest reply count
# unique reply count
# highest number of hashtags
# average num of hashtags
# average num of links
# average num of photos in tweet
# average num of videos in tweet
# highest rt count
# average rt count
# avg num of people mentioned in tweet
# highest num of people mentioned in tweet
# avg like count
# highest like count

print(tweets.dtypes)

