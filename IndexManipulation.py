__author__ = 'Jonny'
import json
import pattern.vector as vec
import scipy

basedir = "/Users/Jonny/Documents/Scripting/RapResults/RapGenius"
indexes_dir = "/Users/Jonny/Documents/Scripting/RapResults/indexes/"
results_basedir = "/Users/Jonny/Documents/Scripting/RapResults/"
lyrics_dir = "/Users/Jonny/Documents/Scripting/RapResults/IndexedLyrics/"
corpus_dir = "/Users/Jonny/Documents/Scripting/RapResults/Corpi/"
stop_names_file = "/Users/Jonny/Documents/Scripting/RapResults/stop_names"
as_index = "/Users/Jonny/Documents/Scripting/RapResults/indexes/ArtistSongID"
sa_index = "/Users/Jonny/Documents/Scripting/RapResults/indexes/SongIDArtist"
common_words_file = "/Users/Jonny/Documents/Scripting/RapResults/common_words"
#asid = json.load(as_index, encoding=object)
asid = artistsongid

rap_exclude_words = ['1','2', '3', 'x2', 'ay', 'hey', 'uhh', '\'mon', 'cuz', 'c', '\'mma', 'kanye', 'west', 'yo', 't', 'oh', 'uh', 'ya', 'yea', 'la', 'gon', 'cause', 'em', 'yeah', '50', 'cent']


def make_artist_corpus(artist)
    filenames = []
    corpus = corpus_dir + artist
    for vals in asid[artist].values:
        filenames.extend(lyrics_dir + str(vals))
    with open(corpus, 'w') as outfile:
        for fname in filenames

def make_clean_artist_corpus(artist):
    artfiles = []
    corpus = corpus_dir + artist
    rap_exclude_words.extend(artist.split)
    #artfiles = (lyrics_dir + r for r in asid[str(artist)])
    #artfiles = [lyrics_dir + str(i) for i in asid[artist]]
    f = open(corpus, 'w')
    for fname in asid[artist]:
        fname = lyrics_dir + str(fname)
        g = open(fname, 'r')
        lyrics = g.read()
        f.write(lyrics)
        g.close()
    f.close()
    rap_exclude_words.extend = get_common_words(common_words_file)
    f = open(corpus)
    cleancorpus = corpus + "_clean"
    g = open(cleancorpus)
    for line in f:
        for word in rap_exclude_words:
            line = line.replace(word, "")
        g.write(line)
    f.close()
    g.close()

def make_all_clean_artist_corpus(dir):
    artists = get_artist_names(dir)
    for n in artists:
        make_clean_artist_corpus(n)



#still need to clean other rapper's versus from the clean corpus


