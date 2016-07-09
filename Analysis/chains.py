'''
Combinations of commands
'''

# Time series tf-idf plot
artists = loadAllArtists()
corpi = makeAllDateCorpi(artists)
artlist, yearlist, albumstrings = splitDateCorpi(corpi)
tfidf_vectorizer = TfidfVectorizer(max_df=0.75, max_features=200000,
                                 min_df=0.05, stop_words='english',
                                 use_idf=True, tokenizer=stemmedCorpus, ngram_range=(1,8))
tfidf_matrix = tfidf_vectorizer.fit_transform(albumstrings)
DC3D = reshape3DDateCorpi(artlist,yearlist,tfidf_matrix)
DC3DFlat = np.mean(DC3D,1)
DC3DFlatter = np.mean(DC3DFlat,0)
DC3DSort = DC3DFlat[:,DC3DFlatter.argsort()]
ribbonPlot(DC3DFlat,yearlist)

