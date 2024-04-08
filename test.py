
import pandas as pd

data = pd.read_json('data.json', lines = True)
#print(data)

accounts = pd.read_csv('/mnt/c/Users/joyli/OneDrive - Simon Fraser University (1sfu)/CMPT/CMPT 353/Project/twitter_human_bots_dataset2.csv')
accounts_cleaned = accounts[['account_type', 'id']]
accounts_bots = accounts_cleaned[accounts_cleaned['account_type'] == 'bot']
accounts_humans = accounts_cleaned[accounts_cleaned['account_type'] == 'human']

# for us to keep the collected user info
collected_user_info = pd.DataFrame()

# for us to keep the updated latest tweets
collected_user_tweets = pd.DataFrame()

import asyncio
import time
import twscrape
from twscrape import API, gather
from twscrape.logger import set_log_level

async def worker(queue:asyncio.Queue, api:twscrape.API):
    while True:
        query = await queue.get()

        try:
            #user_info = await twscrape.gather(api.user_by_id(query, limit=1))
            user_info = await api.user_by_id(query)
            lol = pd.DataFrame(user_info.dict())
            #print(f"{query} - {len(user_info)} - {int(time.time())}")
            print(type(user_info))
            print(lol)
            # do something with tweets here, eg same to file, etc
        except Exception as e:
            print(f"Error on {query} - {type(e)}")
        finally:
            queue.task_done()

async def main():
    
    api = twscrape.API()

    #await api.pool.add_account("pingo_go", "Bumblep_13", "wrenezym@gmail.com", "joyjune13")
    await api.pool.login_all()

    queries = accounts['id']
    queue = asyncio.Queue()

    workers_count = 2
    workers = [asyncio.create_task(worker(queue,api)) for _ in range(workers_count)]
    for q in queries:
        queue.put_nowait(q)

    await queue.join()
    for worker_task in workers:
        worker_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())

