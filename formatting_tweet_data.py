import pandas as pd
import numpy as np
import json

tweets = pd.read_csv('concat_tweets.csv', low_memory = False)
#needed for average tweet per day
accounts = pd.read_csv('twitter_human_bots_dataset.csv', low_memory = False)
accounts = accounts.loc[:, accounts.columns.intersection(['id','created_at'])]



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


# dropping rows with corrupted data
tweets = tweets.drop(index = [33219,332168])


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

grouped_data = tweets.groupby(tweets.taken_from)
# things to agg we are grouping on the variable: 'extracted_from':
# average words per tweet
grouped_statistics['word_count_mean'] = grouped_data.word_count.mean()
# highest words per tweet
grouped_statistics['word_count_max'] = grouped_data.word_count.max()
# lowest words per tweet
grouped_statistics['word_count_min'] = grouped_data.word_count.min()
# highest rt count
grouped_statistics['rt_count_max'] = grouped_data.retweetCount.max()
# average rt count
grouped_statistics['rt_count_mean'] = grouped_data.retweetCount.mean()
# avg like count
grouped_statistics['like_count_mean'] = grouped_data.likeCount.mean()
# highest like count
grouped_statistics['like_count_max'] = grouped_data.likeCount.max()
# average daily tweet num
tweet_count =  grouped_data.id.count()
tweet_count = pd.DataFrame({'id':tweet_count.index, 'count': tweet_count.values})
tweet_count = tweet_count.join(accounts.set_index('id'), on='id')
days = tweets.date.max().replace(tzinfo=None)-pd.to_datetime(tweet_count.created_at)
tweet_count['daily_avg'] = tweet_count['count']/days.dt.days #join at the end
# average reply count 
grouped_statistics['replyCount_mean'] = grouped_data.replyCount.mean()
# highest reply count
grouped_statistics['replyCount_max'] = grouped_data.replyCount.max()
# unique reply count
# highest number of hashtags
grouped_statistics['hashtagCount_max'] = grouped_data.hashtagCount.max()
# average num of hashtags
grouped_statistics['hashtagCount_mean'] = grouped_data.hashtagCount.mean()
# average num of links
grouped_statistics['links_count_mean'] = grouped_data.links_count.mean()
# average num of photos in tweet
grouped_statistics['photos_count_mean'] = grouped_data.photos_count.mean()
# average num of videos in tweet
grouped_statistics['videos_count_mean'] = grouped_data.videos_count.mean()
# avg num of people mentioned in tweet
grouped_statistics['mentionCount_mean'] = grouped_data.mentionCount.mean()
# highest num of people mentioned in tweet
grouped_statistics['mentionCount_max'] = grouped_data.mentionCount.max()
grouped_statistics.merge(tweet_count, how='left', left_index=True, right_on='id')
#output to csv
grouped_statistics.to_csv('aggregated_tweet_data.csv')
print(tweets.dtypes)

