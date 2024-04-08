import pandas as pd
data_types = {'0':str,'id':str, 'id_str':str, 'url':str, 'date':str, 'user':str, 'lang':str, 'rawContent':str, 'replyCount':str, 
              'retweetCount':str, 'likeCount':str, 'quoteCount':str, 'conversationIdStr':str, 'conversationId':str, 'hashtags':str,
              'cashtags':str, 'mentioned':str, 'links':str, 'viewCount':str, 'retweetedTweet':str, 'quotedTweet':str, 'place':str, 'coordinates':str}
tweet_data_1 = pd.read_csv('collected_user_tweets1.csv', dtype = data_types)
tweet_data_2 = pd.read_csv('collected_user_tweets2.csv', dtype = data_types)
tweet_data_3 = pd.read_csv('collected_user_tweets3.csv', dtype = data_types)
tweet_data_4 = pd.read_csv('collected_user_tweets4.csv', dtype = data_types)
tweet_data_5 = pd.read_csv('collected_user_tweets5.csv', dtype = data_types)
tweet_data_6 = pd.read_csv('collected_user_tweets6.csv', dtype = data_types)
tweet_data_7 = pd.read_csv('collected_user_tweets7.csv', dtype = data_types)
tweet_data_8 = pd.read_csv('collected_user_tweets8.csv', dtype = data_types)
tweet_data_9 = pd.read_csv('collected_user_tweets9.csv', dtype = data_types)
tweet_data_10 = pd.read_csv('collected_user_tweets10.csv', dtype = data_types)
tweet_data_11 = pd.read_csv('collected_user_tweets11.csv', dtype = data_types)
tweet_data_12 = pd.read_csv('collected_user_tweets12.csv', dtype = data_types)
tweet_data_13 = pd.read_csv('collected_user_tweets13.csv', dtype = data_types)
tweet_data_14 = pd.read_csv('collected_user_tweets14.csv', dtype = data_types)
tweet_data_15 = pd.read_csv('collected_user_tweets15.csv', dtype = data_types)
tweet_data_16 = pd.read_csv('collected_user_tweets16.csv', dtype = data_types)

tweet_data = pd.concat([tweet_data_1,tweet_data_2 ,tweet_data_3,tweet_data_4,tweet_data_5,tweet_data_6,tweet_data_7,tweet_data_8,
                        tweet_data_9,tweet_data_10,tweet_data_11,tweet_data_12,tweet_data_13,tweet_data_14,tweet_data_15,tweet_data_16])

tweet_data = tweet_data[['id', 'date','user','rawContent','replyCount','retweetCount','likeCount','quoteCount','hashtags','mentionedUsers','links','media','taken_from', 'inReplyToTweetId']]

tweet_data.to_csv('concat_tweets.csv')

