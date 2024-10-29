# ----------------------------------------------------------------------------

# Meet John and Akhil: rival students but in the same team, who each believe they’re the ultimate text analysts.
# The challenge is to extract the best, most meaningful features from text data.
# They’ve got a collection of comments and reviews to analyze—and now it’s a full-on feature-engineering battle.

import pandas as pd
import numpy as np
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from textblob import TextBlob
import textstat
import unittest
from nltk.tokenize import sent_tokenize
import nltk
import warnings
warnings.filterwarnings("ignore")  

# Both of them start with some basic NLTK setup.
nltk.download('punkt')
nltk.download('stopwords')

# John’s setting up VADER right away, claiming that “all the best insights come from sentiment analysis.”
analyzer = SentimentIntensityAnalyzer()

# Akhil, ever the stylist, insists that stopwords and token complexity are where the real insights lie.
stop_words = set(nltk.corpus.stopwords.words('english'))

def extract_sentiment_features(text):
    """
    John’s prized function: a powerhouse of sentiment-related features.
    He’s banking on these to show that *tone* is what really counts.
    """

    # VADER: scoring positive, neutral, and negative sentiments, plus a compound score.
    sentiment = analyzer.polarity_scores(text)

    # Adding TextBlob for a second layer of sentiment: polarity and subjectivity.
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    return pd.Series({
        "pos_score": sentiment['pos'],
        "neu_score": sentiment['neu'],
        "neg_score": sentiment['neg'],
        "compound_score": sentiment['compound'],
        "polarity": polarity,
        "subjectivity": subjectivity
    })

def extract_complexity_features(text):
    """
    Akhil’s masterpiece: a function dedicated to measuring text complexity and style.
    He claims it’ll make John’s sentiment analysis look basic.
    """

    # Basic length stats—Akhil’s idea of foundational complexity.
    char_count = len(text)
    token_count = len(text.split())

    # Akhil loves sophisticated words, so he adds average word length and unique word count.
    words = text.split()
    avg_word_length = np.mean([len(word) for word in words]) if words else 0
    unique_word_count = len(set(words))

    # Stopword count: Akhil believes that the ratio of common words reveals simplicity vs. sophistication.
    stopword_count = sum(1 for word in words if word.lower() in stop_words)

    return pd.Series({
        "char_count": char_count,
        "token_count": token_count,
        "avg_word_length": avg_word_length,
        "unique_word_count": unique_word_count,
        "stopword_count": stopword_count
    })

def extract_style_features(text):
    """
    Both of them go wild here, adding style-based features like exclamations, questions, and mentions.
    They’re neck and neck on this one, and each swears their features matter more.
    """

    # Exclamations, questions, hashtags, and mentions—each revealing a different style and tone.
    exclamation_count = text.count("!")
    question_count = text.count("?")
    hashtag_count = text.count("#")
    mention_count = text.count("@")

    return pd.Series({
        "exclamation_count": exclamation_count,
        "question_count": question_count,
        "hashtag_count": hashtag_count,
        "mention_count": mention_count
    })

def extract_readability_features(text):
    """
    Akhil’s trump card—readability and complexity scores. “Sentiment is nothing if you can’t read it.”
    John’s rolling his eyes, but Akhil’s convinced he’s about to win this.
    """

    # Flesch Reading Ease: a classic readability score. Higher = easier to read, lower = more complex.
    flesch_reading_ease = textstat.flesch_reading_ease(text)

    # Sentence length is another marker of complexity.
    avg_sentence_length = np.mean([len(sentence.split()) for sentence in sent_tokenize(text)]) if text else 0

    # Syllable count per word is the final blow—harder words usually have more syllables.
    words = text.split()
    syllable_count = textstat.syllable_count(text) / len(words) if words else 0

    return pd.Series({
        "flesch_reading_ease": flesch_reading_ease,
        "avg_sentence_length": avg_sentence_length,
        "syllable_count": syllable_count
    })

# Now they’re both dabbling in TF-IDF, each claiming it’ll boost their insights. Akhil’s aiming for word uniqueness,
# and John’s just glad it sounds intense.
def extract_tfidf_features(text, top_n=5):
    """
    TF-IDF—Akhil’s pick for understanding which words are unique and important.
    John agrees, but he’s hoping his sentiment still shines.
    """

    # Vectorizing the text data with TF-IDF to see which words matter most.
    vectorizer = TfidfVectorizer(max_features=top_n)
    tfidf_matrix = vectorizer.fit_transform([text])
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

    return tfidf_df.iloc[0]  # Return as a single row Series

def add_ngrams_features(df, text_column, ngram_range=(2, 3), top_n=5):
    """
    Phrases or “n-grams”—John and Akhil’s shared feature, though each thinks they’ll use it better.
    This grabs common bigrams and trigrams to capture context.
    """

    # Vectorizing to extract top n-grams
    vectorizer = CountVectorizer(ngram_range=ngram_range)
    ngrams_matrix = vectorizer.fit_transform(df[text_column])
    ngrams_df = pd.DataFrame(ngrams_matrix.toarray(), columns=vectorizer.get_feature_names_out())
    return pd.concat([df, ngrams_df.iloc[:, :top_n]], axis=1)

# Here’s their sample text—just a few random reviews. John and Akhil are each convinced their features will be the best.
texts = [
    "I absolutely love this! It's amazing!",
    "I'm not sure what I think about this product.",
    "This is the worst experience I've ever had.",
    "Totally fantastic and wonderful!",
    "Absolutely terrible, I hated every moment."
]
df = pd.DataFrame(texts, columns=["text"])

# Here they go, running their feature extractors one by one and merging all features.
df = df.join(df["text"].apply(extract_sentiment_features))
df = df.join(df["text"].apply(extract_complexity_features))
df = df.join(df["text"].apply(extract_style_features))
df = df.join(df["text"].apply(extract_readability_features))

# TF-IDF features for the top 5 most “unique” words, added as individual columns.
df_tfidf = df["text"].apply(lambda x: extract_tfidf_features(x, top_n=5))
df_tfidf.columns = [f"tfidf_{col}" for col in df_tfidf.columns]  # Rename for clarity
df = pd.concat([df, df_tfidf], axis=1)

# And finally, Akhil’s n-gram features. John admits they’re interesting.
df = add_ngrams_features(df, "text", ngram_range=(2, 3), top_n=5)

print("---------------------------------------------")

# The final output—packed with more features than either of them ever dreamed.
print("\nExtracted Features with VADER Sentiment Scores, Readability, Complexity, and TF-IDF:")
print(df)

# ----------------------------------------------------------------------------

# -------- Unit Tests --------
# With both of them claiming victory, it’s time for a quick test run to see if everything works.
class TestVaderSentimentDemo(unittest.TestCase):
    """
    John and Akhil’s showdown: testing each feature extractor to make sure it works without breaking a sweat.
    """

    def test_extract_sentiment_features(self):
        text = "I absolutely love this!"
        features = extract_sentiment_features(text)
        self.assertIn("pos_score", features, "Oops! 'pos_score' feature is missing.")
        self.assertIn("compound_score", features, "Expected 'compound_score' feature is missing.")

    def test_extract_complexity_features(self):
        text = "I absolutely love this!"
        features = extract_complexity_features(text)
        self.assertIn("char_count", features, "Oops! 'char_count' feature is missing.")
        self.assertIn("avg_word_length", features, "Expected 'avg_word_length' feature is missing.")

    def test_extract_style_features(self):
        text = "I absolutely love this!"
        features = extract_style_features(text)
        self.assertIn("exclamation_count", features, "Oops! 'exclamation_count' feature is missing.")

    def test_extract_readability_features(self):
        text = "I absolutely love this!"
        features = extract_readability_features(text)
        self.assertIn("flesch_reading_ease", features, "Oops! 'flesch_reading_ease' feature is missing.")

# And they’re off! Testing each feature extraction function to make sure their theories hold water.
if __name__ == '__main__':
    unittest.main(argv=[''], exit=False) 

# ----------------------------------------------------------------------------

# Findings and Discussion:
# With their extracted features in hand, John and Akhil go over the results, debating their insights.
# Here’s what they notice:

# 1. Sentiment Trends:
#    - Comments 0 and 3 have high positive sentiment scores (`pos_score` and `compound_score`), which aligns with the 
#      words they use (“love,” “fantastic,” “wonderful”). It’s clear these are positive reviews.
#    - Comments 2 and 4, on the other hand, are quite negative, with high `neg_score` and negative `compound_score`.
#      This matches their tone, which includes phrases like “worst experience” and “hated every moment.”
#    - Both John and Akhil agree: sentiment features seem reliable and accurately reflect the overall tone.

# 2. Subjectivity Levels:
#    - Akhil is fascinated by the subjectivity scores. Comment 2 has a subjectivity of 1.0, meaning it’s highly opinionated.
#      This makes sense because it’s a personal complaint. Comments with lower subjectivity (like 0.75) seem to have more
#      balanced tones, blending opinion with some descriptive language.
#    - John thinks this feature could help differentiate emotional feedback from more neutral, factual comments.

# 3. Text Complexity and Style:
#    - Akhil points out that comments with higher `token_count` and `avg_word_length` often feel more sophisticated.
#      For example, Comment 3 has a high average word length of 7.25, making it sound more formal.
#    - Interestingly, `unique_word_count` varies significantly; Comment 1 uses a lot of common words and is repetitive,
#      while Comment 3 has high variety, reflecting a richer vocabulary.
#    - `stopword_count` also adds a layer—more stopwords, like in Comment 1, make it feel conversational, whereas fewer 
#      stopwords (like in Comment 3) give it a more polished, intentional tone.

# 4. Punctuation and Style Indicators:
#    - The `exclamation_count` and `question_count` show us that Comment 0 is enthusiastic, using exclamations.
#      Comment 2, with a question mark, has a tone of uncertainty.
#    - `hashtag_count` and `mention_count` could be more useful with social media text; here, they’re mostly 0,
#      indicating that these reviews lack social context but might be relevant if analyzing tweets (Or should we say Xweets) or Instagram posts.

# 5. Readability Insights:
#    - Akhil’s proudest moment: the `flesch_reading_ease` and `syllable_count` scores highlight text readability.
#    - Comment 3, with high syllable count and low Flesch score, is the most complex and formal-sounding review.
#      Meanwhile, Comment 0 is easy to read, making it accessible and upbeat.
#    - `avg_sentence_length` also aligns well with these findings, where shorter sentences are easier to read and more 
#      conversational, as seen in Comment 0.

# 6. TF-IDF and N-Gram Highlights:
#    - TF-IDF scores reveal which words stand out in each comment. For example, Comment 4 ranks high on words like
#      “hated” and “terrible,” which emphasize its negativity.
#    - N-grams add context; for instance, “absolutely love” appears in Comment 0, giving it a positive sentiment boost,
#      while “worst experience” in Comment 2 solidifies its negative tone.
#    - Both John and Akhil agree that TF-IDF and n-grams help capture the specific language that defines each review’s tone.

# Conclusion:
#    - Both John and Akhil are finally on the same page: each feature adds unique insights into the data.
#    - Sentiment and subjectivity reveal tone; text complexity, punctuation, and readability capture style; and TF-IDF 
#      and n-grams spotlight the words and phrases that make each review unique.
#    - This detailed analysis could help predict customer sentiment, identify key themes, and make text more accessible 
#      by targeting readability—all while offering a rich, multi-faceted view of each piece of text.

# ----------------------------------------------------------------------------