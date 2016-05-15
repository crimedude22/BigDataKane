import nltk
from nltk.tokenize import RegexpTokenizer
import re
import dill as pickle
import os
import matplotlib
import numpy
import matplotlib.pyplot as plt


#Make list of word corpus
def wordCorpus(corpus):
    tokenizer = RegexpTokenizer(r"\w+'\w+|\w+")
    return tokenizer.tokenize(corpus)

# Make wordCorpus for all artist corpi
def makeArtistWordCorpi(corpi):
    # corpi is a dict like the one made by makeAllCorpi
    for i in corpi.keys():
        corpi[i] = wordCorpus(corpi[i])
    return corpi



# Split dict into two lists
def splitCorpiDict(corpi):
    artistnames = list()
    corpitemp = list()
    for i in corpi.keys():
        artistnames.append(i)
        corpitemp.append(corpi[i])
    return artistnames,corpitemp

##Make term frequency matrix, dist matrix and make 2d array
from sklearn.feature_extraction.text import TfidfVectorizer

#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.1, stop_words='english',
                                 use_idf=True, tokenizer=wordCorpus, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(corpitemp) #fit the vectorizer to corpi
terms = tfidf_vectorizer.get_feature_names() #list of terms used in tf-idf matrix
print(tfidf_matrix.shape)

#cosine similarity
from sklearn.metrics.pairwise import cosine_similarity
dist = 1 - cosine_similarity(tfidf_matrix)



##Ward Clustering - Hierarchal dendrogram
from scipy.cluster.hierarchy import ward, dendrogram

linkage_matrix = ward(dist) #define the linkage_matrix using ward clustering pre-computed distances

fig, ax = plt.subplots(figsize=(5, 5)) # set size
ax = dendrogram(linkage_matrix, orientation="right", labels=artistnames);

plt.tick_params(\
    axis= 'x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')

plt.tight_layout() #show plot with tight layout

#uncomment below to save figure
plt.savefig('ward_clusters.png', dpi=200) #save figure as ward_clusters


#YOU SHOULD CALCULATE SENTENCE ENTROPY: TRAIN A CLASSIFIER ON A RAPPER AND THEN SEE IN EACH SONG HOW PREDICTABLE THE NEXT LYRICS ARE