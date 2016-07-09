from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
import matplotlib.pyplot as plt
import time
import pandas as pd
import settings

basedir = settings.BASE_DIR
analdir = settings.ANAL_DIR

#Make list of word corpus
def wordCorpus(corpus):
    tokenizer = RegexpTokenizer(r"\w+'\w+|\w+")
    return tokenizer.tokenize(corpus)

def stringCorpus(corpus):
    tokenizer = RegexpTokenizer(r"\w+'\w+|\w+")
    wcorpus = tokenizer.tokenize(corpus)
    strcorpus = " ".join(map(str,wcorpus))
    return strcorpus

#Stemmed word copurs
def stemmedCorpus(corpus):
    tokenizer = RegexpTokenizer(r"\w+'\w+|\w+")
    stemmer = SnowballStemmer("english")
    tokens = tokenizer.tokenize(corpus)
    stems = list()
    for i in tokens:
        try:
            stems.append(stemmer.stem(i))
        except:
            pass
    return stems

# Make wordCorpus for all artist corpi
def makeArtistWordCorpi(corpi):
    # corpi is a dict like the one made by makeAllCorpi
    for i in corpi.keys():
        corpi[i] = wordCorpus(corpi[i])
    return corpi

def makeArtistStemmedCorpi(corpi):
    for i in corpi.keys():
        corpi[i] = stemmedCorpus(corpi[i])
    return corpi

def makeArtistStringCorpi(corpi):
    for i in corpi.keys():
        corpi[i] = stringCorpus(corpi[i])
    return corpi

# Split dict into two lists
def splitCorpiDict(corpi):
    artistnames = list()
    corpitemp = list()
    for i in corpi.keys():
        artistnames.append(i)
        corpitemp.append(corpi[i])
    return artistnames,corpitemp
