# Sakia Team Assignment 7

Team members: Iara Ravagni & Sakshee Patil

This repository puts together a code demo for a python feature engineering for the packages Gensim and NLTK. It covers preprocessing, word embeddings with Word2Vec, document-term weighting with TF-IDF, document similarity calculations, and topic modeling using LDA. Additionally, a test function verifies key functionality.

## Requirements: 
Before starting, install the requirements listed on the file requirements.txt plus `gensim`, `nltk` and `pytest`.

## Usage:
Run the code using 

```bash
python gensim-demo-sakia.py
```

The expected output includes:

1. Preprocessed sample document text.
2. Word2Vec similarity scores for selected words.
3. TF-IDF weights for the first document.
4. Document similarity scores.
5. Extracted topics and their representative words.

## Testing

The file contains test functions for each feature to verify the correct output. The tests can be run using the following code:

```bash
pytest gensim-demo-sakia.py    
```

