import pandas as pd
import numpy as np
import datetime
import json
import re

tweets = pd.read_csv('concat_tweets.csv', low_memory = False)
users = pd.read_csv('collected_user_data.csv').set_index('id')
users = users[['username', 'displayname', 'rawDescription',
                         'followersCount', 'friendsCount', 'statusesCount', 'favouritesCount',
                         'mediaCount', 'blue','created']]
classification_data = pd.read_csv('twitter_human_bots_dataset.csv')[['id', 'account_type']].set_index('id')
users = classification_data.join(users).dropna()

classification_data = classification_data[['account_type']]
users_data = users.drop('created', axis = 1)

users_data.to_csv('cleaned_user_data.csv')
users['created'] = pd.to_datetime(users['created'])

tweets['taken_from'] = tweets['taken_from'].fillna(0).astype(int)


# udf to use, much of the data are strings that are actually lists
def obj_to_list(input):
    if (input == '[]' or input == '0'):
        return([])
    else:
        return(input.split(','))

# returns the num of items in a list to use in apply()
def list_count(input):
    return(len(input))


def parse_json(input):
    try: 
        return json.loads(input)
    except: 
        return ("{[]}")
    
def count_json(input):
    try: 
        return len(parse_json(input))
    except: 
        return 0
    
def count_media(input, field):
    try: 
        return len(parse_json(input)[field])
    except: 
        return 0

def is_retweet(input):
    # regex code to find user id of tweet poster
    match = re.search(r'\d+', str(input['user']))
    # if the user id of tweet poster = id of twitter profile, this is not a retweet
    id_match = int(input['taken_from']) != int(match.group())

    str_match = input['rawContent'].startswith('RT')
    return (id_match or str_match)


# dropping rows with corrupted data
tweets = tweets.drop(index = [33219,332168])


#typecast for aggregation
tweets.retweetCount = tweets.retweetCount.astype(float)
tweets.likeCount = tweets.likeCount.astype(float)
tweets.replyCount = tweets.replyCount.astype(float)


#typecast for aggregation
tweets.retweetCount = tweets.retweetCount.astype(float)
tweets.likeCount = tweets.likeCount.astype(float)
tweets.replyCount = tweets.replyCount.astype(float)

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

# seperate retweets and tweets
tweets['is_retweet'] = tweets.apply(is_retweet, axis = 1)

#replace single quote with double quote to make it proper json object
tweets['media'] = tweets['media'].str.replace("'",'"', regex=False)
tweets['mentionedUsers'] = tweets['mentionedUsers'].str.replace("'",'"', regex=False)
tweets['links'] = tweets['links'].str.replace("'",'"', regex=False)
#replace None with null to make it proper json object
tweets['media'] = tweets['media'].str.replace("None",'null', regex=False)

tweets['photos_count'] = tweets['media'].apply(count_media, field='photos')
tweets['videos_count'] = tweets['media'].apply(count_media, field='videos')
tweets['animated_count'] = tweets['media'].apply(count_media, field='animated')
tweets['mentionCount'] = tweets['mentionedUsers'].apply(count_json)
tweets['links_count'] = tweets['links'].apply(count_json)

#Exclude url from raw content
tweets['url_excluded'] = tweets.rawContent.replace(r'http\S+', '', regex=True).replace(r'www\S+', '', regex=True)
#wordcount
tweets['word_count'] = tweets.url_excluded.str.split().apply(len)

#aggregated dataframe
grouped_statistics = pd.DataFrame()

grouped_data_all_tweets = tweets.groupby(tweets.taken_from)
grouped_data_no_retweets = tweets[tweets['is_retweet'] == False].groupby(tweets.taken_from)

# things to agg we are grouping on the variable: 'taken_from':
# average words per tweet
grouped_statistics['word_count_mean'] = grouped_data_no_retweets.word_count.mean()
# highest words per tweet
grouped_statistics['word_count_max'] = grouped_data_no_retweets.word_count.max()
# lowest words per tweet
grouped_statistics['word_count_min'] = grouped_data_no_retweets.word_count.min()
# highest rt count
grouped_statistics['rt_count_max'] = grouped_data_no_retweets.retweetCount.max()
# average rt count
grouped_statistics['rt_count_mean'] = grouped_data_no_retweets.retweetCount.mean()
# avg like count
grouped_statistics['like_count_mean'] = grouped_data_no_retweets.likeCount.mean()
# highest like count
grouped_statistics['like_count_max'] = grouped_data_no_retweets.likeCount.max()
# average daily tweet num

# average tweets a day
active_days = (grouped_data_all_tweets.date.max() - users['created'])
grouped_statistics['average_tweets_per_day'] = users['statusesCount']/active_days.dt.days
print(grouped_statistics['average_tweets_per_day'])


# average reply count 
grouped_statistics['replyCount_mean'] = grouped_data_no_retweets.replyCount.mean()
# highest reply count
grouped_statistics['replyCount_max'] = grouped_data_no_retweets.replyCount.max()
# unique reply count
grouped_statistics['unique_reply_count'] = grouped_data_no_retweets.replyCount.nunique()
# highest number of hashtags
grouped_statistics['hashtagCount_max'] = grouped_data_all_tweets.hashtagCount.max()
# average num of hashtags
grouped_statistics['hashtagCount_mean'] = grouped_data_all_tweets.hashtagCount.mean()
# average num of links
grouped_statistics['links_count_mean'] = grouped_data_all_tweets.links_count.mean()
# average num of photos in all tweets
grouped_statistics['photos_count_all_mean'] = grouped_data_all_tweets.photos_count.mean()
# average num of photos in original tweets (excluding retweets)
grouped_statistics['photos_count_original_mean'] = grouped_data_no_retweets.photos_count.mean()

# average num of videos in all tweet
grouped_statistics['videos_count_all_mean'] = grouped_data_all_tweets.videos_count.mean()
# average num of videos in original tweets (excluding retweets)
grouped_statistics['videos_count_original_mean'] = grouped_data_no_retweets.videos_count.mean()
# avg num of people mentioned in tweet
grouped_statistics['mentionCount_mean'] = grouped_data_no_retweets.mentionCount.mean()
# highest num of people mentioned in tweet
grouped_statistics['mentionCount_max'] = grouped_data_no_retweets.mentionCount.max()
#output to csv
grouped_statistics.to_csv('aggregated_tweet_data.csv')
print(tweets.dtypes)
