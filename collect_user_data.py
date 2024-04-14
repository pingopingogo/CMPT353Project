
import pandas as pd

data = pd.read_json('data.json', lines = True)
#print(data)

accounts = pd.read_csv('twitter_human_bots_dataset2.csv')

collected_user_info = pd.DataFrame()
collected_user_tweets = pd.DataFrame()

import asyncio
import time
import twscrape
from twscrape import API, gather
from twscrape.logger import set_log_level

async def worker(queue:asyncio.Queue, api:twscrape.API):
    while True:
        query = await queue.get()
        global collected_user_info
        global collected_user_tweets

        try:
           
            # gathering user latest tweets (including replies)
            user_tweets_list = await twscrape.gather(api.user_tweets_and_replies(query, limit=1))
            user_tweets = pd.DataFrame(user_tweets_list)

            # Ensure datetime is in the correct format
            user_tweets['date'] = pd.to_datetime(user_tweets['date'])

            # Extracting time-related features
            user_tweets['time_of_day'] = user_tweets['date'].dt.hour
            user_tweets['day_of_week'] = user_tweets['date'].dt.day_name()
            user_tweets['weekend'] = user_tweets['date'].dt.dayofweek >= 5

            
            user_tweets['taken_from'] = int(query)
            print(user_tweets)
            collected_user_tweets = pd.concat([user_tweets, collected_user_tweets])

            """
            # gathering user info
            user_info_list = await api.user_by_id(query)
            user_info_dict = user_info_list.dict() # convert to dict for pd dataframe
            user_data = pd.DataFrame.from_dict(user_info_dict, orient = 'index').transpose() # convert to a pandas dataframe
            print(user_data)
            collected_user_info = pd.concat([user_data,collected_user_info]) # add onto user info dataframe"""
        except Exception as e:
            print(f"Error on {query} - {type(e)}")
        finally:
            queue.task_done()

async def main():
    
    api = twscrape.API()

    await api.pool.add_account("wt0001119187", "ab123456a", "wwtt2236422@gmail.com", "ab123456a")
    await api.pool.add_account("wt0002149784", "ab123456a", "w.wtt2236422@gmail.com", "ab123456a")
    await api.pool.add_account("wt000314947", "ab123456a", "ww.tt2236422@gmail.com", "ab123456a")
    await api.pool.add_account("wt000448267", "ab123456a", "wwt.t2236422@gmail.com", "ab123456a")
    await api.pool.add_account("wt000581135", "ab123456a", "wwtt.2236422@gmail.com", "ab123456a")
    await api.pool.add_account("wt0006140643", "ab123456a", "wwtt2.236422@gmail.com", "ab123456a")
    await api.pool.add_account("wt00071308", "ab123456a", "wwtt22.36422@gmail.com", "ab123456a")
    await api.pool.add_account("wt0008182714", "ab123456a", "wwtt223.6422@gmail.com", "ab123456a")
    await api.pool.add_account("wt0009162561", "ab123456a", "wwtt2236.422@gmail.com", "ab123456a")
    await api.pool.add_account("wt0000569973", "ab123456a", "wwtt22364.22@gmail.com", "ab123456a")

    await api.pool.login_all()

    queries = accounts['id'][1000:2000]
    queue = asyncio.Queue()

    workers_count = 2
    workers = [asyncio.create_task(worker(queue,api)) for _ in range(workers_count)]
    for q in queries:
        queue.put_nowait(q)

    await queue.join()
    for worker_task in workers:
        worker_task.cancel()

    #print(collected_user_info)
    #collected_user_info.to_csv('collected_user_data.csv2')
    collected_user_tweets.to_csv('collected_user_tweets3.csv')


if __name__ == "__main__":
    asyncio.run(main())

