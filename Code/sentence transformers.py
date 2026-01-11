from huggingface_hub import configure_http_backend
import matplotlib.pyplot as plt
import numpy as np
import os
from os.path import join
import pandas as pd
import requests
import seaborn as sns
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
import torch
from torchmetrics.functional import pairwise_cosine_similarity as cosine_similarity


# Load the model locally
model = torch.load("models/all_mpnet_base_v2.pt", weights_only=False, map_location=torch.device('cpu'))

# Load aLL combined files for each party
base_dir = "data"
ignore_folder = "raw_programme"

corpus = {}

for partei in os.listdir(base_dir):

    partei_path = join(base_dir, partei)
    if not os.path.isdir(partei_path):
        continue

    # Ignore folder "raw_programme"
    if partei == ignore_folder:
        continue

    combined_path = join(partei_path, "Combined")
    if not os.path.exists(combined_path):
        print(f"⚠ Warnung: Kein Combined-Ordner für {partei}")
        continue

    full_text = ""

    for file in os.listdir(combined_path):
        if file.endswith(".txt"):
            file_path = join(combined_path, file)
            with open(file_path, "r", encoding="utf-8") as f:
                full_text += f.read().replace("\n", " ").strip()

    if full_text.strip() == "":
        print(f"⚠ Warnung: Keine Texte für {partei} gefunden!")
        continue

    corpus[partei] = full_text.strip()
    print(f"✔ Loaded Combined text for {partei}")

print("\nParteien im Korpus:", list(corpus.keys()))

# Embed each party's full combined text
documents = list(corpus.values())

print("\n🔄 Generating embeddings...")
embeddings = model.encode(documents, convert_to_tensor=True)
print("✔ Embeddings shape:", embeddings.shape)

sim = cosine_similarity(embeddings) # embeddings.shape = (N,d), sim.shape = (N,N)
sim += torch.eye(sim.shape[0])
print(sim)

# Visualize the results
sns.heatmap(sim, xticklabels=list(corpus.keys()), yticklabels=list(corpus.keys()), annot=True, cbar=False)
plt.title("Cosine Similarities zwischen allen Parteien", pad=20, fontweight='bold')
plt.savefig("Cosine_Similarities.png")

# Project the 768 embedding dimensions into 2d space
pca = PCA(n_components=2)
embeddings_pca = pca.fit(embeddings.T).components_
e = torch.from_numpy(embeddings_pca)

plt.cla()
for ex, ey in embeddings_pca.T:
    plt.scatter(ex, ey)
plt.legend(labels=list(corpus.keys()))
plt.grid()
plt.title("PCA aller Partei-Embeddings in 2D", pad=20, fontweight='bold')
plt.savefig("PCA_all_embeddings.png")

labels = list(corpus.keys())
labels.remove('GOP')
labels.remove('DEM')
plt.cla()
for i, (ex, ey) in enumerate(embeddings_pca.T):
    if i not in [2,4]:
        plt.scatter(ex, ey)
plt.legend(labels=labels)
plt.grid()
plt.title("PCA der deutschen Partei-Embeddings in 2D", pad=20, fontweight='bold')
plt.savefig("PCA_de_embeddings.png")
