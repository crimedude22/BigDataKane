"""
The main way to use this at this point is to create an artists object with "x = Artists("Artist Name")"
Which will get all their albums, songs, lyrics, etc. Then you should probably call the saveArtist() method so you don't lose it
Will build some functions to crawl around RG to get artists automatically/recover all saved artist objects automatically...
"""

import copy, os, re, sys, requests
import dill as pickle
from bs4 import BeautifulSoup as bs
#import settings

#Janky ass encoding workaround. Everyone online says it'll cause problems but fuck it
reload(sys)
sys.setdefaultencoding('utf8')

# Temporary workaround while I don't want to deal with paths and modules and shit
class settings:
    BASE_DIR = "/Users/Jonny/Documents/RapData/"
    ARTIST_DIR = "/Users/Jonny/Documents/RapData/Artists/"

basedir = settings.BASE_DIR
global artistdir
artistdir = settings.ARTIST_DIR

#Generic attribute holder class
class attribs:
    pass

#Class definitions
class Song:
    def __init__(self, url, *songfile):
        #Check if we already have this file
        URLcheck = re.compile('https?://')
        if URLcheck.match(url) is None:
            print("Loading Local Song {}\n".format(url))
            self.load(songfile)
        else:
            songpage = requests.get(url)
            soup = bs(songpage.text, "html.parser")

            #Extract info
            try:
                title = soup.find(class_="song_header-primary_info-title").get_text()
                mainArtist = soup.find(class_="song_header-primary_info-primary_artist").get_text()
                album = soup.find(href=re.compile("albums")).get_text()
                year = soup.find(class_="song_album-info-release_year").get_text()
                lyrics = soup.find(class_="lyrics").get_text()
            except:
                print("Something went wrong getting basic song info")
            try: #To get featured artist list
                featlist = soup.find(collection="song.featured_artists").extract()
                featlist = featlist.find_all(href=re.compile("artists"))
                feat = list()
                for i in range(len(featlist)):
                    feat.append(featlist[i].get_text())

            except: #Try to rescue the song object if no featured artists
                    #Class it up
                    self.title = title
                    self.artist = mainArtist
                    self.album = album
                    self.year = year
                    self.lyrics = lyrics
                    print("Classing without featured list")

            try: #Class if featured artists were found
                #Class it up
                self.title = title
                self.artist = mainArtist
                self.album = album
                self.year = year
                self.feat = feat
                self.lyrics = lyrics
            except:
                print("Something went wrong with classing")

    def load(self, songfile):
        try:
            with open(songfile, 'rb') as f:
                af = pickle.load(f)
        except:
            songfile = raw_input('Couldn\'t find Song File, Where it is?: \n >')
            with open(songfile, 'rb') as f:
                sf = pickle.load(f)

        self.album = sf['album']
        self.lyrics = sf['lyrics']
        self.artist = sf['artist']
        self.title = sf['title']
        self.year = sf['year']
        self.feat = sf['feat']
        self.albums = list()



class Artist:
    #Make an object that contains all an artist's albums, which then contain all an artist's songs.
    def __init__(self, ArtistName):
        self.corpus = None
        self.dateCorpus = None
        self.name = ArtistName

        #Check if we already have this artist
        if ArtistName in os.listdir(artistdir):
            self.load()
        else:
            #Get the artist page
            urlname = re.sub(' ', '-', ArtistName)
            rgurl = "http://genius.com/artists/%s" % str(urlname)
            artistpage = requests.get(rgurl)
            artistsoup = bs(artistpage.text, "html.parser")
            self.url = rgurl

            #Build album objects (which contain song objects)
            albumlinklist = artistsoup.find_all(class_="vertical_album_card")
            self.albums = list()
            numalbums = len(albumlinklist)
            for i in range(len(albumlinklist)):
                try:
                    print("Building Album Object %d of %d" % (i+1, numalbums))
                    albumlink = str(albumlinklist[i].get('href'))
                    self.albums.append(Album(albumlink))
                except:
                    print("Failed to get album {}".format(i+1))

    #Because we can't save nested python classes by just picking them,
    #we have to go through each song in each album, save that separately,
    #then flatten the attribute into just its title.
    #We'll build another function to reconstruct the class from these flattened pickles below
    #For now, don't save except if you just loaded the artist from the internet. Something about the way we're loading is shitty and causes pickle to have EOF errors
    def save(self):
        try:
            global artistdir
            artistdir
            thisartistdir = '{}{}'.format(artistdir,self.name.encode("utf-8"))
        except NameError:
            artistdir = raw_input("No Artistdir defined, where should we put the pickled artist?:")
            thisartistdir = '{}{}'.format(artistdir,self.name.encode("utf-8"))

        if not os.path.exists(thisartistdir):
            os.makedirs(thisartistdir)

        tempself = copy.deepcopy(self)

        for i in range(len(tempself.albums)):
            albumdir = '{}{}{}'.format(thisartistdir,"/Albums/",re.sub('/',' ', tempself.albums[i].title.encode("utf-8")))
            try:
                if not os.path.exists(albumdir):
                    os.makedirs(albumdir)
            except:
                newalbumname = raw_input("albumdir didn't work, rename it?:")
                albumdir = '{}{}'.format(thisartistdir,newalbumname)
                if not os.path.exists(albumdir):
                    os.makedirs(albumdir)
            for j in range(len(tempself.albums[i].songs)):
                sfile = '{}{}{}'.format(albumdir,"/",re.sub('/',' ', tempself.albums[i].songs[j].title.encode("utf-8")))
                s = open(sfile, "wb")
                pickle.dump(tempself.albums[i].songs[j].__dict__,s,-1)
                s.close()
                tempself.albums[i].songs[j] = tempself.albums[i].songs[j].title

            albfile = '{}{}{}'.format(thisartistdir,"/",re.sub('/',' ', tempself.albums[i].title.encode("utf-8")))
            s = open(albfile, "wb")
            try:
                pickle.dump(tempself.albums[i].__dict__,s,-1)
            except:
                print('Failed to Pickle {}'.format(tempself.albums[i]))
            s.close()
            tempself.albums[i] = tempself.albums[i].title

        selfile = '{}{}{}'.format(artistdir,self.name,"_object")
        self.selfile = selfile
        s = open(selfile,"wb")
        pickle.dump(tempself.__dict__,s,-1)
        s.close()
        print("Artist Saved: {}".format(self.name))


    def load(self):
        # Find artist file and load it

        # Adding Verbosity for debugging...
        print("Loading {}".format(self.name))

        os.chdir(artistdir)
        afile = os.path.abspath("{}_object".format(self.name))
        f = open(afile.encode("utf-8"),'rb')
        af = pickle.load(f)
        f.close()

        # Assign Attributes And Prepare for Album iter
        self.url = af['url']
        #self.albumlist = af['albums']
        self.albums = list()

        albumlist = os.listdir("{}/{}".format(artistdir,self.name))
        albumlist = [i for i in albumlist if "Albums" not in i]
        albumlist = [i for i in albumlist if ".DS_Store" not in i]
        self.albumlist = albumlist

        for i in self.albumlist:
            # print i
            os.chdir("{}/{}".format(artistdir,self.name))
            # Make attribs for album "object"
            albumd = attribs()

            # Load album file and fill basic attributes
            albfile = os.path.abspath(i.encode("utf-8")).encode("utf-8")
            g = open(albfile,'rb')
            gf = pickle.load(g)
            g.close()

            albumd.artist = gf['artist']
            albumd.year = gf['year']
            albumd.title = gf['title']

            # Now fill songs
            albumd.songs = list()
            songlist = [x.encode("utf-8") for x in gf['songs']]
            os.chdir("{}/{}/Albums/{}/".format(artistdir,self.name,i.encode("utf-8")))
            for j in songlist:
                # print j
                songfile = os.path.abspath(re.sub('/', ' ', j)).encode("utf-8")
                h = open(songfile.encode("utf-8"),'rb')
                hf = pickle.load(h)
                h.close()

                songd = attribs()
                try:
                    songd.artist = hf['artist']
                except:
                    pass
                try:
                    songd.album = hf['album']
                except:
                    pass
                try:
                    songd.title = hf['title']
                except:
                    pass
                try:
                    songd.year = hf['year']
                except:
                    pass
                try:
                    songd.feat = hf['feat']
                except:
                    pass
                try:
                    songd.lyrics = hf['lyrics']
                except:
                    pass

                albumd.songs.append(songd)

            # Attach filled album object to artist
            self.albums.append(albumd)

    # Take slashes out of titles
    def cleanTitles(artist):
        for i in range(len(artist.albums)):
            for j in range(len(artist.albums[i].songs)):
                artist.albums[i].songs[j].title = re.sub('/',' ', artist.albums[i].songs[j].title)
        return artist

    def listAlbums(self):
        for i in range(len(self.albums)):
            print("{}".format(self.albums[i].title))

    def compileCorpus(self):
        self.corpus = str()
        for i in range(len(self.albums)):
            for j in range(len(self.albums[i].songs)):
                # Clean Out Verses by Other People eventually, but....
                try:
                    self.corpus += str(self.albums[i].songs[j].lyrics)
                except:
                    pass

    def compileDateCorpus(self):
        self.dateCorpus = dict()
        for i in range(len(self.albums)):
            albumstr = str()
            for j in range(len(self.albums[i].songs)):
                try:
                    albumstr += str(self.albums[i].songs[j].lyrics)
                except:
                    pass
            try:
                self.dateCorpus.update({int(self.albums[i].year) : albumstr})
            except:
                print("Failed to date album {}".format(self.albums[i].title))

class Album:
    def __init__(self, url, *albfile):
        # Check if we already have this album and are loading it
        URLcheck = re.compile('https?://')
        if URLcheck.match(url) is None:
            print("Loading Local Album {}".format(url))
            self.load(self, albfile)
        else:
            # Otherwise get it from the internet
            albumpage = requests.get(url)
            albumsoup = bs(albumpage.text,"html.parser")
            songlinklist = albumsoup.find_all(class_="song_link")
            songs = list()
            for i in range(len(songlinklist)):
                try:
                    songlink = songlinklist[i].get('href')
                    songs.append(Song(songlink))
                except:
                    print("Failed To Get Song {}".format(i))
            self.songs = songs
            self.artist = albumsoup.find(class_="album_artist").get_text()
            self.year = albumsoup.find(class_="release_year").get_text().replace("(","").replace(")","").replace(" ","") #yeah this sucks shut up
            nametemp = albumsoup.find(class_="album_name").contents[0].replace("\n","")
            self.title = nametemp[2:]  # Getting rid of leading whitespace...

    @staticmethod
    def load(self, albfile):
        #try:
        with open(albfile, 'rb') as f:
            albf = pickle.load(f)
        #except:
        #    albfile = raw_input("Couldn't Find Album File, Where is?")
        #    with open(albfile, 'rb') as f:
        #        albf = pickle.load(f)
        self.file   = albfile
        self.artist = albf['artist'].strip('\n')
        self.year   = albf['year']
        self.title  = albf['title']
        self.songlist = albf['songs']
        self.songs = list()
        for i in self.songlist:
            songfile = '{}{}{}{}{}{}'.format(artistdir,self.artist,'/Albums/',self.title,'/',i)
            self.songs.append(Song(i,songfile.encode("utf-8")))



def makeArtists(artlist):
    artists = list()
    for i in range(len(artlist)):
        print("Making {}".format(artlist[i]))
        artemp = Artist("{}".format(artlist[i]))
        artemp.cleanTitles()
        artemp.save()
        artists.append(artemp)
    return artists

#If we already have them all downloaded...
def loadAllArtists():
    artlist = os.listdir(artistdir)
    artlist = [i for i in artlist if "_object" not in i]
    artlist = [i for i in artlist if ".DS_Store" not in i]
    artists = list()
    for i in artlist:
        artists.append(Artist(i))
    return artists

def makeAllCorpi(artists):
    # artists is a bunch of artist objects in a list
    corpi = dict()
    for i in artists:
        eval('i.compileCorpus()')
        corpse = i.corpus
        corpi[i.name] = corpse
    return corpi

def makeAllDateCorpi(artists):
    corpi = dict()
    for i in artists:
        eval('i.compileDateCorpus()')
        corpse = i.dateCorpus
        corpi[i.name] = corpse
    return corpi
