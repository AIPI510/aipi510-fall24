import nltk 
from nltk.corpus import inaugural
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.tokenize import word_tokenize
import pandas as pd

nltk.download('inaugural')
nltk.download('punkt')  # For tokenizing
nltk.download('punkt_tab')  #For tokenizing
nltk.download('stopwords') # For removing stopwords

def load_file_ids():
    '''
    Loads the file IDs for the dataset

    Returns:
        - file IDs that contain the speeches
    '''
    # Load the file IDs (each file represents an inaugural speech)
    return inaugural.fileids()

def get_stop_words():
    '''
    Gets the set of stop words for the English language

    Returns:
        - The set of stop words in English
    '''
    stop_words = set(stopwords.words("english"))
    return stop_words
    
def extract_features(text, stop_words):
    '''
    Tokenizes a text, removes the stop words and retrieves the frequency distribution to extract features

    Input:
        - text (str): the text for which to begin feature extraction
        - stop_words (set): the set of stop words in English

    Returns:
        - A dictionary containing the length of the list of words in the text, the number of unique words in the text,
        the 5 most common words in the text, and the percentage of unique words in the speech
    '''
    # Tokenize the text
    words = word_tokenize(text.lower())
    # Remove stopwords and non-alphabetic words
    words = [word for word in words if word.isalpha() and word not in stop_words]
    
    # Get word frequency distribution
    word_freq = FreqDist(words)
    
    # Return features
    return {
        "num_words": len(words),
        "num_unique_words": len(set(words)),
        "most_common_words": word_freq.most_common(5),
        "pct_unique_words": "{:.2f}".format((len(set(words))/len(words)) * 100)
    }

def create_df(file_ids, stop_words):
    '''
    Extracts features for every text in a list of file IDs and creates a dataframe of those features

    Input:
        - file_ids (list): a list of file IDs
        - stop_words (set): a set of stop words in English

    Returns:
        - df (pd.Dataframe): A dataframe consisting of the extracted features from the file IDs
    '''
    # Create an empty list to store features for each speech
    data = []

    # Loop through each speech and extract features
    for file_id in file_ids:
        speech_text = inaugural.raw(file_id)
        features = extract_features(speech_text, stop_words)
        features["speech_text"] = speech_text
        data.append(features)

    # Convert the list of feature dictionaries into a DataFrame
    df = pd.DataFrame(data)
    return df

def main():
    file_ids = load_file_ids()
    stop_words = get_stop_words()
    df = create_df(file_ids, stop_words)
    print(df.head(10))

if __name__ == "__main__":
    main()
