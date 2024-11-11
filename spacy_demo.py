## Team Assignment 7 -- Feature Engineering
## Author: Roxanne Wang & Ruonan Shi
## Date: 26/10/2024
## Package: SpaCy
## GitHub: https://github.com/explosion/spaCy

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import pytest


# Load the spaCy language model.
def load_nlp_model():
    return spacy.load("en_core_web_sm")


# Tokenization, remove stop words, lemmatize.
def preprocess_text(nlp, text):
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    return tokens


# Perform named entity recognition.
def named_entity_recognition(nlp, text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]


# Perform POS tagging.
def part_of_speech_tagging(nlp, text):
    doc = nlp(text)
    return [(token.text, token.pos_) for token in doc]


# Unit Test for SpaCy.
def test_preprocess_text():
    nlp = load_nlp_model()
    text = "Gus Proto is a Python developer currently working for a Fintech company."
    result = preprocess_text(nlp, text)
    assert "gus" in result
    assert "proto" in result
    assert "developer" in result
    assert "is" not in result  # Stop word


def test_named_entity_recognition():
    nlp = load_nlp_model()
    text = "Gus Proto is a Python developer at Fintech Inc. in London."
    result = named_entity_recognition(nlp, text)
    assert ("Gus Proto", "PERSON") in result
    assert ("Fintech Inc.", "ORG") in result
    assert ("London", "GPE") in result


def test_part_of_speech_tagging():
    nlp = load_nlp_model()
    text = "Gus Proto is learning Python."
    result = part_of_speech_tagging(nlp, text)
    assert ("Gus", "PROPN") in result
    assert ("learning", "VERB") in result


if __name__ == "__main__":
    # Load the spaCy model
    nlp = load_nlp_model()

    text = "Gus Proto is a Python developer currently working for a Fintech company in London."

    # Preprocess text.
    print("Preprocessed Tokens:", preprocess_text(nlp, text))

    # Named Entity Recognition.
    print("Named Entities:", named_entity_recognition(nlp, text))

    # POS Tagging.
    print("Part of Speech Tags:", part_of_speech_tagging(nlp, text))

    # Run tests
    import sys
    sys.exit(pytest.main([__file__]))
