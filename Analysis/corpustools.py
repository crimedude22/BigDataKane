from __future__ import print_function
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
import matplotlib.pyplot as plt
import time
import pandas as pd
import settings
import numpy as np
# import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


basedir = settings.BASE_DIR
analdir = settings.ANAL_DIR

def makeAllCorpi(artists):
    # artists is a bunch of artist objects in a list
    corpi = dict()
    for i in artists:
        eval('i.compileCorpus()')
        corpse = i.corpus
        corpi[i.name] = corpse
    return corpi


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
        print("Stemming {}\r".format(i))
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

def loadCorpSplit():
    art = loadAllArtists()
    corpi = makeAllCorpi(art)
    artists,corpil = splitCorpiDict(corpi)
    return artists,corpil


def loadCorpTokenize():
    art = loadAllArtists()
    corpi = makeAllCorpi(art)
    stems = makeArtistStemmedCorpi(corpi)
    artists,corpil = splitCorpiDict(stems)
    return artists,corpil

########################################################
'''
Time-based corpi
'''
def makeAllDateCorpi(artists):
    corpi = dict()
    for i in artists:
        eval('i.compileDateCorpus()')
        corpse = i.dateCorpus
        corpi[i.name] = corpse
    return corpi

def splitDateCorpi(corpi):
    artlist = list()
    yearlist = list()
    albumstrings = list()
    for i in corpi.keys():
        for j,k in corpi[i].items():
            artlist.append(i)
            yearlist.append(j)
            albumstrings.append(k)
    return artlist, yearlist, albumstrings

def reshape3DDateCorpi(artlist,yearlist,tfidf_matrix):
    '''
    Want 3D numpy array, (nyears x nwords x nartists)
    '''
    nyears = len(set(yearlist))
    nwords = tfidf_matrix.shape[1]
    uqartlist = list(set(artlist))

    DC3D = np.zeros([nyears,nwords,len(set(artlist))])

    for ind, i in enumerate(uqartlist):
        idx = [j for j, x in enumerate(artlist) if x == i]
        years = [yearlist[k] for k in idx]
        yearpos = [list(set(yearlist)).index(m) for m in years]
        for n in yearpos:
            DC3D[n,range(nwords),ind] = tfidf_matrix.data[n:(n+1)]
    return DC3D



def ribbonPlot(flattened3d,yearlist):
    y_raw = list(set(yearlist))
    nartists = flattened3d.shape[1]-1
    traces = []
    for i in range(1, nartists):
        z_raw = flattened3d[:,i]
        ci = int(255/nartists*i)
        x = []
        y = []
        z = []
        for j in range(0,len(z_raw)):
            z.append([z_raw[j],z_raw[j]])
            y.append([y_raw[j],y_raw[j]])
            x.append([i*2,i*2+1])
        traces.append(dict(
            z=z,
            x=x,
            y=y,
            colorscale=[[i,'rgb(%d,%d,255)'%(ci, ci)] for i in np.arange(0,1.1,0.1) ],
            showscale=False,
            type='surface',
        ))

    fig = {'data':traces,'layout':{'title':'Frequency of Rare Words by Year'}}
    plot(fig)





