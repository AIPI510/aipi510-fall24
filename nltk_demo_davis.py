# import the nltk module
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

def nltk_feature_engineering(book):
    # based on the book, extract the raw book text
    book_text = gutenberg.raw(book)

    # For ease, we will use the first 1000 characters of the book
    sample_text = book_text[:1000]

    # Step 1: Tokenize the text
    tokens = word_tokenize(sample_text)

    # Step 2: Ensure that the tokens contain only alphabetical characters
    tokens = [token for token in tokens if token.isalpha()]

    # Create a list of stop words 
    stop_words = set(stopwords.words('english'))

    # Step 3: Ensure that the text contains no stop words
    tokens = [token for token in tokens if token.lower() not in stop_words]

    # Initialize the Lemmatizer
    lemmatizer = WordNetLemmatizer()
    
    # Step 4: Lemmatize the tokens
    tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]

    return tokens

def main():
    #We will use moby dick
    tokens = nltk_feature_engineering('melville-moby_dick.txt')
    print(tokens)

if __name__ == "__main__":
    main()
    
