"""
Split up old NLTK file. Not organized nor modularized, so definitely shouldn't try to import this one.
Good god what was I doing.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import ward, dendrogram


#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.9, max_features=200000,
                                 min_df=0.1, stop_words='english',
                                 use_idf=True, tokenizer=stemmedCorpus, ngram_range=(1,6))

tfidf_matrix = tfidf_vectorizer.fit_transform(corpil) #fit the vectorizer to corpi
terms = tfidf_vectorizer.get_feature_names() #list of terms used in tf-idf matrix


#cosine similarity

dist = 1 - cosine_similarity(tfidf_matrix)

##Ward Clustering - Hierarchal dendrogram

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

##K-Means Clustering
from sklearn.cluster import KMeans
from sklearn.externals import joblib

nclusters = 6
km = KMeans(n_clusters=nclusters, n_init=30, init='random')
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()
joblib.dump(km,"{}KMClusters{}".format(analdir,time.strftime("_%y%m%d_%H%M")))


#MDS
from sklearn.manifold import MDS
mds = MDS(n_components=2,dissimilarity="precomputed",random_state=1)
pos = mds.fit_transform(dist)
xs,ys = pos[:,0],pos[:,1]

cluster_colors = {0: 'r', 1: 'b', 2: 'g', 3: 'k', 4: 'c', 5: 'm'}
df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=artistnames))
groups = df.groupby('label')

#2d Plot
fig, ax = plt.subplots(figsize=(17, 9)) # set size
ax.margins(0.05) #
for name, group in groups:
    print name
    ax.plot(group.x, group.y, marker='o', linestyle='', ms=12,
            color=cluster_colors[name],
            mec='none')
    ax.set_aspect('auto')
    ax.tick_params(\
        axis= 'x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')
    ax.tick_params(\
        axis= 'y',         # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        left='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelleft='off')


#add label in x,y position with the label as the film title
for i in range(len(df)):
    ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], size=8)



#SpectralEmbedding
from sklearn.manifold import SpectralEmbedding
spe = SpectralEmbedding(n_components=3,affinity="nearest_neighbors")
pos = spe.fit_transform(tfidf_matrix.toarray())
xs,ys,zs = pos[:,0],pos[:,1],pos[:,2]

#3d Plot
cluster_colors = {0: 'r', 1: 'b', 2: 'g', 3: 'k', 4: 'c', 5: 'm'}
df = pd.DataFrame(dict(x=xs, y=ys, z=zs, label=clusters, title=artistnames))
groups = df.groupby('label')


fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
for name, group in groups:
    print name
    ax.scatter(group.x, group.y, group.z, marker='o',
            c=cluster_colors[name])
    ax.set_aspect('auto')
    ax.tick_params(\
        axis= 'x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')
    ax.tick_params(\
        axis= 'y',         # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        left='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelleft='off')


#add label in x,y position with the label as the film title
for i in range(len(df)):
    ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['z'], df.ix[i]['title'], size=8)

ax.legend(numpoints=1)  #show legend with only 1 point

plt.show()

# Decision Tree Classifier
from sklearn import tree
clf = tree.DecisionTreeClassifier
clf = clf.fit()




#YOU SHOULD CALCULATE SENTENCE ENTROPY: TRAIN A CLASSIFIER ON A RAPPER AND THEN SEE IN EACH SONG HOW PREDICTABLE THE NEXT LYRICS ARE