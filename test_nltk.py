import unittest
from nltk_demo import nltk_feature_engineering
import nltk
nltk.download('gutenberg')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

# Finishing the imports
from nltk.corpus import gutenberg
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class TestNLTK(unittest.TestCase):
    def setUp(self):
        self.book = 'shakespeare-hamlet.txt'
        self.tokens = nltk_feature_engineering(self.book)

    def test_tokens(self):
        self.assertTrue(isinstance(self.tokens, list), "Tokens have to be a list")
        self.assertTrue(len(self.tokens) > 0, "Tokens shouldn't be empty")

    def test_alpha(self):
        for token in self.tokens:
            self.assertTrue(token.isalpha(), f"Token should be alphabetical, but {token} is not")

    def test_stop(self):
        stop_words = set(stopwords.words('english'))
        for token in self.tokens:
            self.assertTrue(token.lower() not in stop_words, f"Token shouldn't be a stop word, but {token} is")

    def test_lemma(self):
        lemmatizer = WordNetLemmatizer()
        for token in self.tokens:
            self.assertTrue(token == lemmatizer.lemmatize(token), f"Token should be lemmatized, but {token} is not")


if __name__ == '__main__':
    unittest.main()
        
