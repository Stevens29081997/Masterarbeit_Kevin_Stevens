import os
from os.path import join
from typing import *
from collections import defaultdict
import math

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

print("Parteien im Korpus:", corpus.keys())


# Generate tf for all parties
tfs: Dict[str, Dict[str, int]] = {}

for partei, text in corpus.items():
    partei_tf = defaultdict(int)
    for word in text.split():
        w = word.lower()
        partei_tf[w] += 1
    tfs[partei] = partei_tf

# Number of parties = Number of documents
N = len(tfs)

# Compute idf for all terms
all_terms = set(term for tf in tfs.values() for term in tf.keys())

idf = defaultdict(int)

for term in all_terms:
    n = 0
    for partei_tf in tfs.values():
        n += 1 if term in partei_tf.keys() else 0
    idf[term] = math.log(N/n)


tfidfs: Dict[str, Dict[str, float]] = {}

for partei, partei_tf in tfs.items():
    partei_tfidf = {}

    for word, freq in partei_tf.items():

        # Relative Term Frequency (TF)
        rel_tf = freq / max(partei_tf.values())

        # TF-IDF
        partei_tfidf[word] = rel_tf * idf[word]

    tfidfs[partei] = partei_tfidf


# Output: Top 10 words with highest TF–IDF per party
for partei, partei_tfidf in tfidfs.items():
    print(f"\nTop-10 TF-IDF Wörter für {partei}:")

    # Sorting out filter errors in the results
    # Comment this section out to see the original, unfiltered result list
    for filter_error in ['p', 'l', 'wolfgang', 'worauf', 'zudem', 'amerikas', 'amerikanern', 'american', 'saubere', 'june', 'donald', 'muß', 'händeklatschen', 'heiterkeit', 'bravo', 'stürmischer', 'mußte', 'süd', 'willy', '']:
        if partei_tfidf.get(filter_error, None):
            del partei_tfidf[filter_error]

    # Sort in descending order
    sorted_terms = sorted(partei_tfidf.items(), key=lambda x: x[1], reverse=True)

    for i, (w, s) in enumerate(sorted_terms[:10]):
        print(f"{i+1}. {w}: {s:.4f}")
