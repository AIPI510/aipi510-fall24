# This is the code for TA7 - Feature Engineering
# by TEAM XKJX
# Team Members: Xiaoquan Kong, Jinglong Xiong
#
# Install the required libraries by running the following commands:
# pip install -q nltk scikit-learn pytest
#
# How to run this code:
# python ta7-XKJX-nltk-demo.py
#
# How to test this code:
# pytest ta7-XKJX-nltk-demo.py


# Import required libraries
import nltk
from nltk.corpus import movie_reviews
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer


# Download required NLTK datasets
nltk.download("movie_reviews")
nltk.download("punkt_tab")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("averaged_perceptron_tagger_eng")


# following are feature extraction functions
def load_movie_reviews():
    return [" ".join(movie_reviews.words(fileid)) for fileid in movie_reviews.fileids()]


def tokenize_text(text):
    return word_tokenize(text)


def stem_words(words):
    ps = PorterStemmer()
    return [ps.stem(word) for word in words]


def pos_tagging(words):
    return pos_tag(words)


def tfidf_features(texts):
    vectorizer = TfidfVectorizer(max_features=10)
    tfidf_matrix = vectorizer.fit_transform(texts)
    return tfidf_matrix.toarray(), vectorizer.get_feature_names_out()


# Main feature engineering process
def feature_engineering_pipeline():
    texts = load_movie_reviews()
    first_text = texts[0]

    # Tokenization
    tokens = tokenize_text(first_text)

    # Stemming
    stems = stem_words(tokens)

    # POS Tagging
    pos_tags = pos_tagging(tokens)

    # TF-IDF Vectorization
    tfidf_matrix, feature_names = tfidf_features(
        texts[:100]
    )  # Use only a subset to save time

    return {
        "tokens": tokens,
        "stems": stems,
        "pos_tags": pos_tags,
        "tfidf_matrix": tfidf_matrix,
        "feature_names": feature_names,
    }


# following are unit tests
def test_load_movie_reviews():
    texts = load_movie_reviews()
    assert len(texts) > 0, "No texts were loaded from movie_reviews dataset."
    assert isinstance(texts[0], str), "Loaded texts should be strings."


def test_tokenize_text():
    text = "This is a test sentence."
    tokens = tokenize_text(text)
    assert tokens == [
        "This",
        "is",
        "a",
        "test",
        "sentence",
        ".",
    ], "Tokenization failed."


def test_stem_words():
    words = ["running", "jumps", "easily"]
    stems = stem_words(words)
    assert stems == ["run", "jump", "easili"], "Stemming is not working as expected."


def test_pos_tagging():
    words = ["This", "is", "a", "test"]
    pos_tags = pos_tagging(words)
    assert pos_tags[0] == ("This", "DT"), "POS tagging failed for first word."
    assert len(pos_tags) == len(words), "POS tagging output length mismatch."


def test_tfidf_features():
    texts = ["This is a test document.", "This document is a second test document."]
    tfidf_matrix, feature_names = tfidf_features(texts)
    assert (
        tfidf_matrix.shape[0] == 2
    ), "TF-IDF matrix should have 2 rows for 2 documents."
    assert len(feature_names) == 5, "TF-IDF feature count mismatch with max_features."


# Run the pipeline and print results
if __name__ == "__main__":
    features = feature_engineering_pipeline()
    print("Feature Engineering Pipeline Results:")
    print("Tokens:", features["tokens"][:10])
    print("Stems:", features["stems"][:10])
    print("POS Tags:", features["pos_tags"][:10])
    print("TF-IDF Feature Names:", features["feature_names"])
