import os
from os.path import join
import pandas as pd
import numpy as np

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from numpy.linalg import norm

# Load lemmatized files from folder structure
corpus = {}

for partei in os.listdir("data/"):
    if partei == "raw_programme":
        continue
    
    lemm_file = join("data", partei, "Lemmatisiert", f"{partei}_lemmatisiert.txt")

    if os.path.exists(lemm_file):
        with open(lemm_file, "r", encoding="utf-8") as f:
            tokens = f.read().split()
            corpus[partei] = tokens


print("Gefundene Parteien:", list(corpus.keys()))

# Create TaggedDocuments for Doc2Vec
documents = []
for party, tokens in corpus.items():
    documents.append(TaggedDocument(words=tokens, tags=[party]))

# Train Doc2Vec model
model = Doc2Vec(
    vector_size=200, # Embedding size, increased dimensions = better distinguishability
    window=10, # Context window: Maximum distance between current and predicted word
    min_count=2, # Ignore all words with total frequency lower than this
    workers=4, # Number of CPU cores
    epochs=40, # Number of iterations over the text corpus
    dm=1,
)

model.build_vocab(documents)
model.train(documents, total_examples=model.corpus_count, epochs=model.epochs)

print("Doc2Vec Modell wurde erfolgreich trainiert.")

# Extract document vectors for each party
doc_vectors = {}
for party in corpus.keys():
    doc_vectors[party] = model.dv[party] # dv = document vectors

# Cosine similarity function
def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

# Calculate similarity matrix
parties = list(doc_vectors.keys())
sim_matrix = {}

for p1 in parties:
    sim_matrix[p1] = {}
    for p2 in parties:
        sim_matrix[p1][p2] = cosine_similarity(doc_vectors[p1], doc_vectors[p2])

# Output as DataFrame
df = pd.DataFrame(sim_matrix)
print("\nCosine Similarity Matrix:\n")
print(df)

# Ranking: Most similar party pairs
similarities = []

for p1 in parties:
    for p2 in parties:
        if p1 < p2: # no duplicates
            similarities.append((p1, p2, sim_matrix[p1][p2]))

similarities_sorted = sorted(similarities, key=lambda x: x[2], reverse=True)

print("\nTop-Ähnlichkeiten zwischen Parteien (absteigend):\n")
for p1, p2, value in similarities_sorted:
    print(f"{p1} – {p2}: {value:.4f}")
