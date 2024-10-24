# Import necessary libraries
import gensim.downloader as api 
import gensim
from gensim.models import Word2Vec, LdaModel, TfidfModel
import nltk
nltk.download('punkt')
nltk.download("stopwords")
nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim.corpora import Dictionary

# Helper functions to show gensims feature engineering capabilities
def preprocess_text(text):
    """
    Tokenizes and preprocesses the input text by removing stopwords, punctuation, and lemmatizing words.
    """
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    # Tokenize and clean
    tokens = word_tokenize(text.lower())

    tokens_list = []
    for word in tokens:
        if word.isalpha() and word not in stop_words:
            tokens_list.append(lemmatizer.lemmatize(word))

    return tokens_list

def load_dataset():
    """
    Loading a build-in dataset using gensim downloader API: provides an inbuilt API to download popular text datasets and word embedding models
    """
    # Download and load the 20-newsgroups dataset from Gensim's API
    dataset = api.load('20-newsgroups')

    preprocessed_text = []
    for i, doc in enumerate(dataset):
        preprocessed_text.append(preprocess_text(doc['data']))

        # use the first 10 documents
        if i == 9:
            print(f"Sample Raw Document:\n {doc['data']}")
            break

    return preprocessed_text

def train_word2vec(corpus):
    """
    Trains a Word2Vec model on the provided corpus of tokenized documents.
    """
    model = Word2Vec(corpus, vector_size=100, window=5, min_count=2, workers=4)
    return model


def train_tfidf(corpus):
    """
    Trains a TF-IDF model using the corpus and returns the weighted corpus.
    """
    dictionary = Dictionary(corpus)
    bow_corpus = [dictionary.doc2bow(doc) for doc in corpus]
    tfidf_model = TfidfModel(bow_corpus)
    corpus_tfidf = tfidf_model[bow_corpus]
    
    return tfidf_model, dictionary, corpus_tfidf

def compute_similarity(corpus):
    """
    Computes document similarity using TF-IDF on the given corpus.
    """
    dictionary = Dictionary(corpus)
    bow_corpus = [dictionary.doc2bow(doc) for doc in corpus]
    
    # Train TF-IDF model
    tfidf_model = TfidfModel(bow_corpus)
    tfidf_corpus = tfidf_model[bow_corpus]
    
    # Compute similarity
    index = gensim.similarities.MatrixSimilarity(tfidf_corpus)

    return index, tfidf_corpus

def train_lda_model(corpus, num_topics=5):
    """
    Trains a Latent Dirichlet Allocation topic model to extract topics from the provided corpus.
    """
    dictionary = Dictionary(corpus)
    bow_corpus = [dictionary.doc2bow(doc) for doc in corpus]
    lda_model = LdaModel(bow_corpus, num_topics=num_topics, id2word=dictionary, passes=10)

    return lda_model, dictionary, bow_corpus


# Displaying Feature Engineering Results
if __name__ == '__main__':
    # Load and preprocess the dataset
    corpus = load_dataset()
    print(f"\nPreprocessed {len(corpus)} documents.\n")
    print("*"*100)

    ### Word2Vec Model ###
    print("Training Word2Vec model...")
    w2v_model = train_word2vec(corpus)
    print("\nWord2Vec model trained successfully!")
    
    # Show similar words to 'faith'
    similar_words = w2v_model.wv.most_similar('rule', topn=5)
    print("\nTop 5 words similar to 'rule':")
    for word, similarity in similar_words:
        print(f"{word}: {similarity:.4f}")

    # Word similarity between 'rules' and 'law'
    similarity = w2v_model.wv.similarity('rule', 'law')
    print(f"\nWord similarity between 'rules' and 'law': {similarity:.4f}\n")
    print("*"*100)

    ### TF-IDF Model ###
    print("Training TF-IDF model...")
    tfidf_model, dictionary, corpus_tfidf = train_tfidf(corpus)
    print("\nTF-IDF Weights for first document:")
    
    # Show TF-IDF weights for the first document
    for word_id, weight in corpus_tfidf[0]:
        print(f"{dictionary[word_id]}: {weight:.4f}")

    ### Document Similarity using TF-IDF ###
    print("\nComputing document similarity using TF-IDF...")
    index, tfidf_corpus = compute_similarity(corpus)
    
    # Show similarity between first and second documents
    print(f"\nSimilarity between first and second document: {index[tfidf_corpus[0]][1]:.4f}")
    
    # Query document similarity for the first document
    print("\nDocument Similarity Scores for the first document (compared to others):")
    sims = index[tfidf_corpus[0]]  # Similarity scores
    for i, sim in enumerate(sims):
        print(f"Document {i}: {sim:.4f}")

    print("*"*100)


    ### LDA Model ###
    print("\nTraining LDA model for topic extraction...")
    lda_model, dictionary, bow_corpus = train_lda_model(corpus)
    print("\nExtracted Topics:")
    topics = lda_model.print_topics(num_topics=5, num_words=5)
    for topic in topics:
        print(f"Topic {topic[0]}: {topic[1]}")
