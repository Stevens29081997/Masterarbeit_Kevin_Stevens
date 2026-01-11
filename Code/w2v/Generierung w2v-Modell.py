import gensim
import os
from os.path import join
from typing import *

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s' , level=logging.INFO)

# Import corpus from already lemmatized files
corpus: Dict[str, str] = {}

for partei in os.listdir("data/"):
    partei_path = join("data", partei)

    # Ignore the folder "raw_programme" like before in the BoW script
    if partei == "raw_programme":
        continue

    lemm_folder = join(partei_path, "Lemmatisiert")
    lemm_file = join(lemm_folder, f"{partei}_lemmatisiert.txt")

    if os.path.exists(lemm_file):
        with open(lemm_file, "r", encoding="utf-8") as f:
            corpus[partei] = f.read()
    else:
        print(f"Warnung: Lemmatisierte Datei fehlt für Partei '{partei}' → {lemm_file}")

print("Parteien im Korpus:", corpus.keys())

# Word2Vec requires a list of tokens per sentence
# Since the corpora are already lemmatized and cleaned up, a simple split is sufficient
sentences: List[List[str]] = []

for partei, text in corpus.items():
    # Simple tokenizer (no further preprocessing)
    tokens = text.split()
    sentences.append(tokens)

# Building the model
model = gensim.models.Word2Vec(
    sentences, # List of tokenized sentences
    min_count=1, # Ignore all words with total frequency lower than this
    workers=6, # Number of CPU cores
    vector_size=50, # Embedding size
    window=5, # Context window: Maximum distance between current and predicted word
    epochs=10 # Number of iterations over the text corpus
)

# Saving the complete word2vec model
model.save("word2vec_parteien.model")

# Export the model to txt format
from gensim.models import Word2Vec

model = Word2Vec.load("word2vec_parteien.model")
model.wv.save_word2vec_format("word2vec_parteien.txt", binary=False)
