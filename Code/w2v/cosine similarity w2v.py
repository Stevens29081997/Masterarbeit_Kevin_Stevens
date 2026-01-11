from gensim.models import KeyedVectors

# Load Word2Vec model (text format or binary format)
model = KeyedVectors.load_word2vec_format(
    "word2vec_parteien.txt", # or the .model file in binary format
    binary=False
)

# Load lemmatized text files
import os
from os.path import join

corpus = {}

for partei in os.listdir("data/"):
    if partei == "raw_programme":
        continue
    
    lemm_file = join("data", partei, "Lemmatisiert", f"{partei}_lemmatisiert.txt")
    
    if os.path.exists(lemm_file):
        with open(lemm_file, "r", encoding="utf-8") as f:
            corpus[partei] = f.read().split()

# Generate text embedding (document vector)
# Simple averaging of all word vectors
import numpy as np

def text_vector(tokens, model):
    vectors = []
    for token in tokens:
        if token in model.key_to_index:
            vectors.append(model[token])
    if len(vectors) == 0:
        return np.zeros(model.vector_size)
    return np.mean(vectors, axis=0)

# Example: Generate vectors for CDU & SPD
vec_cdu = text_vector(corpus["CDU"], model)
vec_spd = text_vector(corpus["SPD"], model)

# Calculate cosine similarity
from numpy.linalg import norm

def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

# Example: Similarity between the CDU and SPD
similarity = cosine_similarity(vec_cdu, vec_spd)
print("Ähnlichkeit zwischen CDU & SPD:", similarity)

# Calculate cosine similarity for all parties simultaneously
parties = list(corpus.keys())

doc_vectors = {p: text_vector(corpus[p], model) for p in parties}

# Calculate matrix
sim_matrix = {}

for p1 in parties:
    sim_matrix[p1] = {}
    for p2 in parties:
        sim_matrix[p1][p2] = cosine_similarity(doc_vectors[p1], doc_vectors[p2])

# Output
import pandas as pd
df = pd.DataFrame(sim_matrix)
print("\nÄhnlichkeitswerte aller Parteien mit Cosine Similarity:\n")
print(df)

# Most similar party pairs in descending order
similarities = []

for p1 in parties:
    for p2 in parties:
        if p1 < p2:  # Prevents duplicate pairs such as (CDU, SPD) and (SPD, CDU)
            sim_value = float(sim_matrix[p1][p2])
            similarities.append((p1, p2, sim_value))

# Sort by similarity in descending order
similarities_sorted = sorted(similarities, key=lambda x: x[2], reverse=True)

print("\nTop-Ähnlichkeiten zwischen Parteien (absteigend):\n")
for p1, p2, value in similarities_sorted:
    print(f"{p1} – {p2}: {value:.4f}")
