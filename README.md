# CMPT353Project

 ## Group project for CMPT353 E100 Spring 2024  
 Group Members: Xiao Le Li, Lavika Singh, Wai Lee Tai 

## Project Overview :
This project aims to develop a machine learning model to detect Twitter bots. It involves collecting Twitter data, preprocessing, and feature engineering to create a dataset, and then training and evaluating machine learning models to classify accounts as bots or humans.

## Dependencies : 
Dependencies
pandas
numpy
scikit-learn
matplotlib

## Data Collection and Preprocessing
The dataset used in this project consists of tweet data collected from Twitter. The raw data is processed to extract relevant features such as tweet content, retweet count, like count, and user information. The data is then aggregated to create a comprehensive dataset for each Twitter account.

## Project Codes Description :  

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
