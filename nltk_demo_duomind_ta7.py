import nltk
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk import word_tokenize, pos_tag
from nltk.util import ngrams
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
import numpy as np
import os
import time
import pandas as pd

#Ensure required data is downloaded
nltk.download("movie_reviews")
nltk.download("stopwords")
nltk.download("vader_lexicon")
nltk.download("punkt")
nltk.download("punkt_tab")

time.sleep(5)
os.system('cls' if os.name == 'nt' else 'clear')

# Initialize VADER for sentiment analysis
sid = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words("english"))

def load_data():
    sample_review = movie_reviews.raw(movie_reviews.fileids()[0])

    # Tokenize the review
    tokens = word_tokenize(sample_review)

    # Get the sentiment scores
    sentiment_scores = sid.polarity_scores(sample_review)
    positive_score = sentiment_scores['pos']
    negative_score = sentiment_scores['neg']
    neutral_score = sentiment_scores['neu']
    compound_score = sentiment_scores['compound']

    # Subjectivity - Ratio of adjectives and adverbs
    pos_tags = pos_tag(tokens)
    adj_adv_count = sum(1 for word, pos in pos_tags if pos in ['JJ','RB','JJR','JJS','RBR','RBS'])
    subjectivity = adj_adv_count / len(tokens) if tokens else 0

    # Word and Sentence Lengths
    avg_word_length = np.mean([len(word) for word in tokens]) if tokens else 0
    sentence_lengths = [len(sent.split()) for sent in sample_review.split('.')]
    avg_sentence_length = np.mean(sentence_lengths) if sentence_lengths else 0

    # Most Frequent Words (Top-10)
    word_freq = FreqDist(tokens)
    top_10_words = [word for word, freq in word_freq.most_common(10)]

    # Bigram Frequecy
    bigrams = list(ngrams(tokens, 2))
    bigram_freq = Counter(bigrams).most_common(10)

    features = {
        "positive_score": positive_score,
        "negative_score": negative_score,
        "neutral_score": neutral_score,
        "compound_score": compound_score,
        "subjectivity": subjectivity,
        "avg_word_length": avg_word_length,
        "avg_sentence_length": avg_sentence_length,
        "top_10_words": top_10_words,
        "top_10_bigrams": bigram_freq
    }
    
    return sample_review, features

if __name__ == "__main__":

    sample_review, features = load_data()
    print('The First Entry in the "movie_reviews" dataset is, \n')
    print(sample_review)
    print("The Newly Engineered Features For The First Movie Review Are: \n")

    for feature_name, value in features.items():
        print(feature_name,value,'\n')