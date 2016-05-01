__author__ = 'Jonny'
import json
import pattern.vector as vec
import scipy
import json


#Build variables
basedir = "/Users/Jonny/Dropbox/Scripting/RapResults/RapGenius"
indexes_dir = "/Users/Jonny/Dropbox/Scripting/RapResults/indexes/"
results_basedir = "/Users/Jonny/Dropbox/Scripting/RapResults/"
lyrics_dir = "/Users/Jonny/Dropbox/Scripting/RapResults/IndexedLyrics/"
corpus_dir = "/Users/Jonny/Dropbox/Scripting/RapResults/Corpi/"
stop_names_file = "/Users/Jonny/Dropbox/Scripting/RapResults/stop_names"
as_index = "/Users/Jonny/Dropbox/Scripting/RapResults/indexes/ArtistSongID"
sa_index = "/Users/Jonny/Dropbox/Scripting/RapResults/indexes/SongIDArtist"
common_words_file = "/Users/Jonny/Dropbox/Scripting/RapResults/common_words"
assid = json.load(as_index, encoding=object)
assid = artistsongid


rap_exclude_words = ['1','2', '3', 'x2', 'ay', 'hey', 'uhh', '\'mon', 'cuz', 'c', '\'mma', 'kanye', 'west', 'yo', 't', 'oh', 'uh', 'ya', 'yea', 'la', 'gon', 'cause', 'em', 'yeah', '50', 'cent']

def get_only_prolific(thresh):
    proasid = dict()
    keys = list(assid.keys())
    for i in keys:
        xl = list()
        xl.append(assid[i])
        if len(xl) > thresh:
            proasid.update({i:[assid[str(i)]]})
    return proasid



def make_artist_corpus(artist):
    filenames = []
    corpus = corpus_dir + artist
    for vals in asid[artist].values:
        filenames.extend(lyrics_dir + str(vals))
    with open(corpus, 'w') as outfile:
        for fname in filenames

def make_clean_artist_corpus(artist):
    #artist = str(artist)
    artfiles = []
    corpus = corpus_dir + artist
    rap_exclude_words.extend(artist.split)
    #artfiles = (lyrics_dir + r for r in asid[str(artist)])
    #artfiles = [lyrics_dir + str(i) for i in asid[artist]]
    f = open(corpus, 'w')
    artlist = list(asid[str(artist)])
    for aname in artlist:
        aname = lyrics_dir + str(aname)
        g = open(aname, 'r')
        lyrics = g.read()
        lyrics = ' '.join([word for word in text.split() if word not in rap_exclude_words])
        f.write(lyrics)
        g.close()
    f.close()
    #f = open(corpus)
    #cleancorpus = corpus + "_clean"
    #g = open(cleancorpus)
    #for line in f:
    #    for word in rap_exclude_words:
    #        line = line.replace(word, "")
    #    g.write(line)
    #f.close()
    #g.close()

def make_all_clean_artist_corpus():
    #artists = get_artist_names(dir)
    artists = asid.keys
    for n in artists:
        make_clean_artist_corpus(n)



#still need to clean other rapper's verses from the clean corpus


