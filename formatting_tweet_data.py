import pandas as pd
import numpy as np

tweets = pd.read_csv('concat_tweets.csv', low_memory = False)
#needed for average tweet per day
accounts = pd.read_csv('twitter_human_bots_dataset.csv', low_memory = False)
accounts = accounts.loc[:, accounts.columns.intersection(['id','created_at'])]
#typecast for aggregation
tweets.retweetCount = tweets.retweetCount.astype(np.float64)
tweets.likeCount = tweets.likeCount.astype(np.float64)
tweets.replyCount = tweets.replyCount.astype(np.float64)


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

#Exclude url from raw content
tweets['url_excluded'] = tweets.rawContent.replace(r'http\S+', '', regex=True).replace(r'www\S+', '', regex=True)
#wordcount
tweets['word_count'] = tweets.url_excluded.str.split().apply(len)

#aggregated dataframe
grouped_statistics = pd.DataFrame(columns = ['word_count_mean', 'word_count_max', 'word_count_max', 'word_count_min', 'rt_count_max', 'rt_count_mean', 'like_count_mean', 'like_count_max'])

grouped_data = tweets.groupby(tweets.taken_from)
# things to agg we are grouping on the variable: 'extracted_from':
# average words per tweet
grouped_statistics.word_count_mean = grouped_data.word_count.mean()
# highest words per tweet
grouped_statistics.word_count_max = grouped_data.word_count.max()
# lowest words per tweet
grouped_statistics.word_count_min = grouped_data.word_count.min()
# highest rt count
grouped_statistics.rt_count_max = grouped_data.retweetCount.max()
# average rt count
grouped_statistics.rt_count_mean = grouped_data.retweetCount.mean()
# avg like count
grouped_statistics.like_count_mean = grouped_data.likeCount.mean()
# highest like count
grouped_statistics.like_count_max = grouped_data.likeCount.max()
# average daily tweet num
tweet_count =  grouped_data.id.count()
tweet_count = pd.DataFrame({'id':tweet_count.index, 'count': tweet_count.values})
tweet_count = tweet_count.join(accounts.set_index('id'), on='id')
days = tweets.date.max().replace(tzinfo=None)-pd.to_datetime(tweet_count.created_at)
tweet_count['daily_avg'] = tweet_count['count']/days.dt.days
# average reply count 
grouped_data.replyCount.mean()
# highest reply count
grouped_data.replyCount.max()
# unique reply count
# highest number of hashtags
grouped_data.hashtagCount.max()
# average num of hashtags
grouped_data.hashtagCount.mean()
# average num of links
# average num of photos in tweet
# average num of videos in tweet
# avg num of people mentioned in tweet
# highest num of people mentioned in tweet

#grouped_statistics.to_csv('aggregated_tweet_data.csv')
print(tweets.dtypes)

