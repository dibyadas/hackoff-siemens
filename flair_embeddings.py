# -*- coding: utf-8 -*-
"""flair_embeddings.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Jclgb0I5lX9A7Dh3njqE_Mj4qEgkyvuW
"""

!wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Cell_Phones_and_Accessories_5.json.gz

!python3 -m nltk.downloader stopwords
!python3 -m nltk.downloader universal_tagset
!python3 -m spacy download en # download the english model

!pip install git+https://github.com/boudinfl/pke.git

!pip install flair

from flair.embeddings import WordEmbeddings, FlairEmbeddings, StackedEmbeddings, TransformerWordEmbeddings

# create a StackedEmbedding object that combines glove and forward/backward flair embeddings
stacked_embeddings = StackedEmbeddings([
                                        WordEmbeddings('glove'),
                                        FlairEmbeddings('news-forward-fast'),
                                        FlairEmbeddings('news-backward-fast')
                                       ])

with open('some.txt', 'r') as f:
    s = f.read()

we = {}

from flair.data import Sentence
sentence = Sentence(s)

# just embed a sentence using the StackedEmbedding as you would with any single embedding.
stacked_embeddings.embed(sentence)
# now check out the embedded tokens.
for token in sentence:
    we[token.text] = token.embedding

import pke

# define the valid Part-of-Speeches to occur in the graph
pos = {'NOUN', 'PROPN', 'ADJ'}

# define the grammar for selecting the keyphrase candidates
grammar = "NP: {<ADJ>*<NOUN|PROPN>+}"

# 1. create a PositionRank extractor.
extractor = pke.unsupervised.PositionRank()

# 2. load the content of the document.
extractor.load_document(input='some.txt',
                        language='en',
                        normalization=None)

# 3. select the noun phrases up to 3 words as keyphrase candidates.
extractor.candidate_selection(grammar=grammar,
                              maximum_word_number=3)

# 4. weight the candidates using the sum of their word's scores that are
#    computed using random walk biaised with the position of the words
#    in the document. In the graph, nodes are words (nouns and
#    adjectives only) that are connected if they occur in a window of
#    10 words.
extractor.candidate_weighting(window=10,
                              pos=pos)

# 5. get the 10-highest scored candidates as keyphrases
keyphrases = extractor.get_n_best(n=20)

keyphrases

import torch
def get_mean_emb(phrase):
    ws = phrase.split(" ")
    vect = torch.zeros(list(we.values())[0].numpy().shape)
    c = 1
    for i in ws:
        try:
            vect += we[i]
            c += 1
        except KeyError:
            pass
    return (vect/c).numpy()

from sklearn.cluster import KMeans
import numpy as np
X = np.array([   get_mean_emb(i) for i,j in keyphrases   ])

kmeans = KMeans(n_clusters=8, random_state=0).fit(X)
kmeans.labels_
# kmeans.cluster_centers_

from sklearn.cluster import OPTICS
import numpy as np
X = np.array([   get_mean_emb(i) for i,j in keyphrases   ])
clustering = OPTICS(min_samples=2).fit(X)
clustering.labels_

p = np.array(keyphrases)

for i in range(-1, 10):
    print(p[kmeans.labels_ == i])
    # print(p[clustering.labels_ == i])
    print("  ")









"Over the years, my household has tried multiple Bluetooth solutions for our hands-free communications needs. We\'ve had acceptable results from a solution integrated into GPS...but much of our regular driving doesn\'t include the need to load up a full-size GPS. We\'ve".replace("\'", "'")

myString = ". ".join(df[df['asin'] == df['asin'].unique()[1223]]['reviewText'])
with open('some.txt','w') as f:
    f.write(myString)
myString



import pandas as pd
import gzip

def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield eval(l)

def getDF(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
  return pd.DataFrame.from_dict(df, orient='index')

df = getDF('reviews_Cell_Phones_and_Accessories_5.json.gz')

from flair.data import Sentence
sentence = Sentence("i am using multiple words like this here you can see multiple two times and like also two times")

# just embed a sentence using the StackedEmbedding as you would with any single embedding.
stacked_embeddings.embed(sentence)

# now check out the embedded tokens.
for token in sentence:
    we[token.text] = token.embedding
    print(token)
    print(token.embedding)

