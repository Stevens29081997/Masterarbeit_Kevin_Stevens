# Import the regular expressions module to help with text processing
import re  
from collections import (
    defaultdict,
)  
# Data preprocessing
import os
from os.path import join
from typing import *

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy

# Download stopwords and tokenizer if you haven't already
nltk.download("punkt")
nltk.download("stopwords")
nltk.download('punkt_tab')

corpus: Dict[str, str] = {}

for folder in os.listdir("data/"):
    if folder != "raw_programme":
        parteiname: str = folder
        corpus.setdefault(parteiname, "")
        folder = join("data/", folder)

        for subfolder in os.listdir(folder):
            dir = join(folder, subfolder)

            for file in os.listdir(dir):
                if "lemmatisiert" not in file:
                    with open(join(dir, file), 'r') as infile:
                        corpus[parteiname] += infile.read().replace("\n", " ")
                    
print(corpus.keys())

# Get the list of stop words in German
stop_words = set(stopwords.words("german"))
# Get the spacy German language package for lemmatization
lemmatizer = spacy.load("de_core_news_lg")

for partei, sentences in corpus.items():
    # Tokenize
    s = word_tokenize(sentences)
    # Remove stop words from the sentence
    s = [word for word in s if word.lower() not in stop_words]
    # Join the words back into a sentence
    s = " ".join(s)
    # Remove all special characters, numbers etc. with RegEx
    s = re.sub(r"[^a-zA-ZäöüÄÖÜß]", ' ', s)

    # Lemmatize all words
    s = lemmatizer.pipe(s, disable=['tok2vec', 'tagger', 'morphologizer', 'parser', 'senter', 'attribute_ruler', 'ner'])
    s = ''.join([st.text for st in s])

    # Creates a lemmatized file for the data of each party in the "data" folder
    os.makedirs(f"data/{partei}/Lemmatisiert/", exist_ok=True)
    with open(f"data/{partei}/Lemmatisiert/{partei}_lemmatisiert.txt", 'w') as outfile:
        outfile.write(s)

    # Applying BoW on the preprocessed data
    vocab = defaultdict(int)
    for word in s.split():
        vocab.setdefault(word.lower(), 0)
        vocab[word.lower()] += 1
    
    # Display the sorted vocabulary with descending frequency count for the 10 most frequent words
    sorted_vocab = dict(sorted(vocab.items(), key=lambda x: x[1], reverse=True)) 
    print(f"{partei} Wörter mit Frequenzen:", [(c, v) for i, (c, v) in enumerate(sorted_vocab.items()) if i < 10])
