#This script demonstrates feature engineering using the NLTK library and text extracted from the U.S. Constitution PDF.
#We will perform tokenization, stopword removal, and word frequency analysis.
#Ysais and I figured this would be pertinent given current events


import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter  # Correct import

# Download necessary resources
nltk.download('stopwords')
nltk.download('punkt')

def extract_text_from_pdf(pdf_file):

    #This function reads and extracts text from a PDF file.


    # Open the PDF file in read-binary mode.
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        # Initialize an empty string to hold the extracted text.
        text = ""

        # Loop through all the pages in the PDF and add the text from each page to our 'text' string.
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()

    # Return the complete extracted text.
    return text


def preprocess_text(text):

   # This function takes the extracted text, splits it into individual words, removes common words (stopwords),
    #and counts how many times each word appears.



    # Split the text into individual words.
    words = word_tokenize(text)

    # Get the list of common English words we want to ignore (stopwords).
    stop_words = set(stopwords.words('english'))

    # Create a new list of words by removing punctuation and stopwords.
    # We also convert each word to lowercase to avoid counting the same word twice (e.g., "The" and "the").
    filtered_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

    # Count how many times each filtered word appears in the text.
    word_frequencies = Counter(filtered_words)

    # Return both the list of important words and the count of how many times each word appears.
    return filtered_words, word_frequencies


def main(pdf_file):
    """
    Main function to extract text, preprocess it, and display the results.

    Args:
        pdf_file (str): The path (location) of the PDF file to process.
    """
    # Extract text from the PDF file provided.
    text = extract_text_from_pdf(pdf_file)

    # Process the extracted text: break it into words, remove common words, and count the remaining words.
    filtered_words, word_frequencies = preprocess_text(text)

    # Print the first 50 filtered words to see what we’re working with.
    print("Filtered Words: ", filtered_words[:50])  # Limit the printout to 50 words for simplicity.

    # Print the 10 most common words and how often they appear.
    print("\nTop 10 Word Frequencies: ", word_frequencies.most_common(10))


# Unit testing using pytest
# These are simple tests to ensure that our functions are working correctly.

def test_extract_text_from_pdf():
    # This test checks that the text extraction function works and returns a string (text) from the PDF.
    text = extract_text_from_pdf('constitution.pdf')
    assert isinstance(text, str), "Extracted text should be a string"
    assert len(text) > 0, "Extracted text should not be empty"


def test_preprocess_text():
    # This test checks that the text preprocessing function works, returning a list of words and a dictionary of frequencies.
    text = extract_text_from_pdf('constitution.pdf')
    filtered_words, word_frequencies = preprocess_text(text)
    assert isinstance(filtered_words, list), "Filtered words should be a list"
    assert isinstance(word_frequencies, dict), "Word frequencies should be a dictionary"


if __name__ == "__main__":
    # Replace 'constitution.pdf' with the path to your PDF file.
    # This is the file we want to analyze.
    main('constitution.pdf')

