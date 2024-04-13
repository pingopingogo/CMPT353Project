# CMPT353Project

## Group project for CMPT353 E100 Spring 2024

Group Members: Xiao Le Li, Lavika Singh, Wai Lee Tai

## Project Codes:

### collect_user_data.py

Required libraries: [pandas](https://pandas.pydata.org/), [twscrape](https://github.com/vladkens/twscrape), asyncio, time  
Requirement: twitter_human_bots_dataset2.csv, data.json in the same directory  
Command to run: python collect_user_data.py  
Output file: collected_user_tweets##.csv  
Description: Collect updated twtter user data and tweet data in twitter_human_bots_dataset2.csv  
Note: This take a long time to run  
<br>

### data_cleaning_tweets.py

Required libraries: [pandas](https://pandas.pydata.org/)  
Requirement: collected_user_tweets1.csv to collected_user_tweets16.csv in the same directory  
Command to run: python data_cleaning_tweets.py  
Description: Clean and concat collected data  
Output file: concat_tweets.csv  
<br>

### formatting_tweet_data.py

Required libraries: [pandas](https://pandas.pydata.org/), [numpy](https://numpy.org/), datetime, json, re  
Requirement: concat_tweets.csv and collected_user_data.csv in the same directory  
Command to run: python formatting_tweet_data.py  
Description: Aggregate tweet data and produced data with features for model training  
Output file: aggregated_tweet_data.csv, cleaned_user_data.csv  
<br>

### final_data_formatting.py

Required libraries: [pandas](https://pandas.pydata.org/)
Requirement: aggregated_tweet_data.csv and cleaned_user_data.csv in the same directory  
Command to run: python final_data_formatting.py  
Description: Aggregate account data, produced data with features and join user data with tweet data for model training  
Output file: aggregated_tweet_data.csv  
<br>

### data_training_different models.py

Required libraries: [pandas](https://pandas.pydata.org/), [sklearn](https://scikit-learn.org/stable/), [matplotlib](https://matplotlib.org/)  
Requirement: final_data.csv in the same directory  
Command to run: python data_training_different models.py  
Description: Use the data with features to train various machine learning model and product comparision graph  
Output file: model_comparison_chart.png, model_comparison_chart_pca.png
<br>

### final_data_formatting.py

Required libraries: [pandas](https://pandas.pydata.org/)
Requirement: aggregated_tweet_data.csv and cleaned_user_data.csv in the same directory  
Command to run: python final_data_formatting.py  
Description: Aggregate account data, produced data with features and join user data with tweet data for model training  
Output file: aggregated_tweet_data.csv  
<br>

### data_training_different models.py

Required libraries: [pandas](https://pandas.pydata.org/), [sklearn](https://scikit-learn.org/stable/), [matplotlib](https://matplotlib.org/)  
Requirement: final_data.csv in the same directory  
Command to run: python data_training_different models.py  
Description: Use the data with features to train various machine learning model and product comparision graph  
Output file: model_comparison_chart.png, model_comparison_chart_pca.png
