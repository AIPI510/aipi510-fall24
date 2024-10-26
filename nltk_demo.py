import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Downloading vader_lexicon: Contains a list of words and their sentiment scores
nltk.download('vader_lexicon')

def find_sentiment(csv_path):
    tweet_data = pd.read_csv(csv_path)

    # Creating subset with only author_id and content columns
    filtered_df = tweet_data[['author_id', 'content']]

    # Converting all values to string and filling null values with empty string
    filtered_df['content'] = filtered_df['content'].astype(str).fillna('')

    # Initialize sentiment analyzer
    sentiment_analyzer = SentimentIntensityAnalyzer()

    #Lambda function to calculate sentiment score of each tweet
    sentiment = filtered_df['content'].apply(lambda x: sentiment_analyzer.polarity_scores(x))
    sentiment_df = pd.DataFrame(list(sentiment))

    # Check if sentiment score of each tweet is positive, negative or neutral
    sentiment_df['sentiment'] = sentiment_df['compound'].apply(lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'neutral'))
    
    # print count of positive, negative and neutral tweets
    print(sentiment_df['sentiment'].value_counts())

def main():
    csv_path = 'data/Cleaned_ronaldo_tweets.csv'
    find_sentiment(csv_path)

if __name__ == '__main__':
    main()