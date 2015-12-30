__author__ = 'Jonny'
#!/usr/bin/python
import pattern.web
import re, sys, os
from operator import itemgetter
from pattern.web import plaintext, DOM
from bs4 import BeautifulSoup
from collections import Counter
import pattern.vector as vec

rap_exclude_words = ['1','2', '3', 'x2', 'ay', 'hey', 'uhh', '\'mon', 'cuz', 'c', '\'mma', 'kanye', 'west', 'yo', 't', 'oh', 'uh', 'ya', 'yea', 'la', 'gon', 'cause', 'em', 'yeah', '50', 'cent']

# ok, just write a thing that opens the directory with all the artists and prints out the directory
# names

basedir = "/Users/Jonny/Downloads/RapGenius/"
common_words_file = "/Users/Jonny/Documents/Scripting/RapResults/common_words"
results_basedir = "/Users/Jonny/Documents/Scripting/RapResults/"
stop_names_file = "/Users/Jonny/Documents/Scripting/RapResults/stop_names"

def get_common_words(file):
    common = []
    f = open(file)
    for line in f:
        common.append(re.split("\s", line)[1].strip())
    return common

# put all the rapper names into a file
def make_exclude_names():
    f = open(stop_names_file, 'w')
    for dir in os.listdir(basedir):
        # dir names are the name of the artist, separated by -, like jay-z
        name1 = re.split('-', dir)
        for n in name1:
            f.write(n)
            f.write("\n")
            print n
    f.close()

def load_exclude_names():
    global rap_exclude_words
    f = open(stop_names_file)
    for line in f:
        rap_exclude_words.append(line.strip())


def get_artist_docs(name):

    default_dir = basedir + name
    rap_docs = ""

    # get a list of all the files in default dir

    for f in os.listdir(default_dir):
        print f
        # go to that dir
        os.chdir(default_dir)
        # open the file
        fi = open(f, 'r')
        # print "reading " + f
        # slurp
        page = fi.read()

        # what does this do?
        dom = DOM(page)

        # we look at the page and get that the thing we want is in the .lyrics div.
        if dom and dom('.lyrics'):
            lyrics =  dom('.lyrics')[0]
        else:
            continue

        p = plaintext(lyrics.content)
        rap_docs += p

    return rap_docs

    # . questions we have, most common 20 words over ALL artists
    # . what are words that appear only for that artist? like mad for biggie or flavor for queen latifah
    # . what are words that appear only for eminem or biggie small?

    # import pdb; pdb.set_trace()
    # Kanye_corpus = vec.M(rap_docs, weight=vec.TFIDF)

# pass in a dict of bad words, return a dict of word counts

def count_one_artist(name, bad_words):

    # ok, this is a bad way to get number of songs for that artist, so we can average out
    # the words per song
    default_dir = basedir + name
    num_songs = len(os.listdir(default_dir))

    # we need the number of songs, this is so annoying
    dict = {}
    docs = vec.count(vec.words(get_artist_docs(name)))
    for w in bad_words:
        if w in docs:
            dict[w] = docs[w]
    dict['num_songs'] = num_songs # this is cheap
    return dict


def get_one_artist_excluding_common(name):

    global rap_exclude_words

    common_exclude_words = get_common_words(common_words_file)
    rap_exclude_words += common_exclude_words
    # ok this is the worse way to do this
    load_exclude_names()

    docs = get_artist_docs(name)
    corpus = vec.Document(docs, exclude=rap_exclude_words, stop_words=False)
    print "for artist: " + name
    for ln in corpus.keywords(top=20): print "%0.08f\t%s" % ln


def get_each_artist_excluding_common():
    global rap_exclude_words
    common_exclude_words = get_common_words(common_words_file)
    rap_exclude_words += common_exclude_words

    for dir in os.listdir(basedir):
        if dir != '.git':
            if dir != ".DS_Store":
        # push the name of the artist onto the exclude words list
                name1  = re.split('-', dir)
                for n in name1:
                    rap_exclude_words.append(n)

                docs = get_artist_docs(dir)
                results_file = results_basedir + dir
                f = open(results_file, 'w')
                corpus = vec.Document(docs, exclude=rap_exclude_words, stop_words=False)
                f.write("for artist: " + dir)
                print "for artist: " + dir
                f.write("\n")
                #for ln in corpus.keywords(top=20):
                #    f.write("%0.08f\t%s" % ln)
                #    print "%0.08f\t%s" % ln
                z = docs.encode('ascii',errors='ignore')
                f.write(z)
                f.close()

get_each_artist_excluding_common()


# print the results for the top 20 words to a file

def get_one_artist_all_words(name):
    docs = ""
    name1  = re.split('-', name)
    for n in name1:
        rap_exclude_words.append(n)
        print "excluding" + n
    docs = get_artist_docs(name)
    corpus = vec.Document(docs, exclude=rap_exclude_words, stop_words=False)
    for ln in corpus.keywords(top=20): print "%0.08f\t%s" % ln

def get_all_artists_all_words():
    docs = ""
    for dir in os.listdir(basedir):
        print "artist" + dir
        if dir != '.git':
        # push the name of the artist onto the exclude words list
            name1  = re.split('-', dir)
            for n in name1:
                rap_exclude_words.append(n)
            # import pdb; pdb.set_trace()
            docs += get_artist_docs(dir)

    corpus = vec.Document(docs, exclude=rap_exclude_words, stop_words=False)
    for ln in corpus.keywords(top=20): print "%0.08f\t%s" % ln

def get_all_artists_all_words_to_file():
    f = open(common_words_file, "w")
    docs = ""

    for dir in os.listdir(basedir):
        if dir != ".DS_Store":
            print "artist" + dir
            if dir != '.git':
            # push the name of the artist onto the exclude words list
                name1  = re.split('-', dir)
                for n in name1:
                    rap_exclude_words.append(n)

                docs += get_artist_docs(dir)

    corpus = vec.Document(docs, exclude=rap_exclude_words, stop_words=False)
    for ln in corpus.keywords(top=20):
        f.write("%0.08f\t%s" % ln)
        print "%0.08f\t%s" % ln
    f.close()

#get_all_artists_all_words_to_file()

if __name__ == '__main__':

    if sys.argv[1:]:
        name = sys.argv[1]

##################################
###################################
def make_song_list(artist_name):
    allfiles = []
    dir = basedir + artist_name
    filenames = os.listdir(dir)
    for f in filenames:
            if re.search( '\.git', f):
                continue
            else:
                allfiles.append(os.path.join(dir,f))
    return allfiles

def scrape_info_from_song(file):
    f = open(file, 'r')
    page = f.read()
    # using beautiful soup to navigate the dom and get
    # back the stuff that we need
    soup = BeautifulSoup(page)
    soup.prettify()
    lyrics = soup.select(".lyrics")
    if lyrics:
        lyrics_string = lyrics[0].text
        lyrics_string = re.sub("\n", " ", lyrics_string)
        return lyrics_string
    else:
        return ""

artisty = []
for artists in soup.find_all(href=re.compile("artist")):
    art = artists.string