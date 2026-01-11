from gensim.models import Word2Vec

# Load the model
model = Word2Vec.load("word2vec_parteien.model")

# Print the 20 most frequent words in the word2vec model
print("\nDie 20 häufigsten Wörter im word2vec-Modell:")
print(model.wv.index_to_key[:20])

# Exploring the model: Getting the vector of a specific word
print("\nVektor des Wortes 'deutschland':")
print(model.wv['deutschland'])
print("\nVektor des Wortes 'europa':")
print(model.wv['europa'])
print("\nVektor des Wortes 'sozial':")
print(model.wv['sozial'])

# Finding the top 10 most similar words
print("\nDie 10 ähnlichsten Wörter zu 'deutschland':")
print(model.wv.most_similar('deutschland'))
print("\nDie 10 ähnlichsten Wörter zu 'europa':")
print(model.wv.most_similar('europa'))
print("\nDie 10 ähnlichsten Wörter zu 'sozial':")
print(model.wv.most_similar("sozial", topn=10))
