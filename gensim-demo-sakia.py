# Gensim downloader API: provides an inbuilt API to download popular text datasets and word embedding models.
import gensim.downloader as api 
import gensim
from gensim.models import Word2Vec, LdaModel, TfidfModel
import nltk
nltk.download('punkt_tab')
nltk.download("stopwords")
nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim.corpora import Dictionary

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

    # comprises approximately 20,000 newsgroup documents across 20 topics, such as sports, politics, and technology.
    dataset = api.load('20-newsgroups')

    preprocessed_text = []
    for i, doc in enumerate(dataset):
        print(doc['data'])
        preprocessed_text.append(preprocess_text(doc['data']))

        # use the first 10 documents
        if i==9:
            break

    return preprocessed_text


def train_word2vec(corpus):
    """
    Trains a Word2Vec model on the provided corpus of tokenized documents.
    """
    model = Word2Vec(corpus, vector_size=100, window=5, min_count=2, workers=4)
    return model


def train_lda_model(corpus, num_topics=5):
    """
    Trains a Latent Dirichlet Allocation topic model to extract topics from the provided corpus.
    """
    dictionary = Dictionary(corpus)
    bow_corpus = [dictionary.doc2bow(doc) for doc in corpus]
    lda_model = LdaModel(bow_corpus, num_topics=num_topics, id2word=dictionary, passes=10)

    return lda_model, dictionary, bow_corpus


def compute_similarity(corpus):
    """
    Computes document similarity using TF-IDF on the given corpus.
    """
    dictionary = Dictionary(corpus)
    bow_corpus = [dictionary.doc2bow(doc) for doc in corpus]
    
    # Train model
    tfidf_model = TfidfModel(bow_corpus)
    tfidf_corpus = tfidf_model[bow_corpus]
    
    # Compute similarity
    index = gensim.similarities.MatrixSimilarity(tfidf_corpus)

    return index, tfidf_corpus


if __name__ == '__main__':
    # Load and preprocess the dataset
    corpus = load_dataset()
    print(f"Preprocessed {len(corpus)} documents.")

    # Train Word2Vec model
    w2v_model = train_word2vec(corpus)
    print("Word2Vec model trained.")
    print("Similar words to 'faith':")
    print(w2v_model.wv.most_similar('faith'))
    
    print("Training LDA model for topic extraction...")
    lda_model, dictionary, bow_corpus = train_lda_model(corpus)
    topics = lda_model.print_topics(num_words=5)

    print("Extracted topics:")
    for topic in topics:
        print(topic)
    
    # Document similarity using TF-IDF
    print("Computing document similarity using TF-IDF...")

    index, tfidf_corpus = compute_similarity(corpus)
    print(f"Similarity between first and second document: {index[tfidf_corpus[0]][1]}")
