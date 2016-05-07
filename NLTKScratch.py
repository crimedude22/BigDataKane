#############################
#The main way to use this at this point is to create an artists object with "x = Artists("Artist Name")"
#Which will get all their albums, songs, lyrics, etc. Then you should probably call the saveArtist() method so you don't lose it
#Will build some functions to crawl around RG to get artists automatically/recover all saved artist objects automatically...


import nltk
import requests
from bs4 import BeautifulSoup as bs
import re
import dill as pickle
import os
import copy

##To do from 4.30: Have to make search function that finds the song links specific to the artist search, right now it is just finding everythign that mentions the artist.
#5.6: at least partially answered this by just using albums as the means of finding songs

basedir = "/Users/Jonny/Documents/RapData/"
global artistdir
artistdir = "/Users/Jonny/Documents/RapData/Artists/"

#Class definitions
class Song:
    def __init__(self, url):
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




class Artist:
    #Make an object that contains all an artist's albums, which then contain all an artist's songs.
    def __init__(self, ArtistName):
        self.corpus = None
        self.name = ArtistName
        #Get the artist page
        urlname = re.sub(' ','-', ArtistName)
        rgurl = "http://genius.com/artists/%s" % str(urlname)
        artistpage = requests.get(rgurl)
        artistsoup = bs(artistpage.text,"html.parser")
        self.url = rgurl

        #Build album objects (which contain song objects)
        albumlinklist = artistsoup.find_all(class_="album_link")
        self.albums = list()
        numalbums = len(albumlinklist)
        for i in range(len(albumlinklist)):
            try:
                print("Building Album Object %d of %d" % (i+1, numalbums))
                albumlink = "http://genius.com%s" % str(albumlinklist[i].get('href'))
                self.albums.append(Album(albumlink))
            except:
                print("Failed to get album {}".format(i))



        #Pickle Artist Object
        #Aint working at the moment...
        # try:
        #     artistdir
        # except NameError:
        #     artistdir = input("No Artistdir defined, where should we put the pickled artist?:")
        #
        # afile = '{}{}{}'.format(artistdir, urlname,".pyc")
        # if not os.path.exists(artistdir):
        #     os.makedirs(artistdir)
        # a = open(afile, "w")
        # pickle.dump(self,a,-1)
        # a.close()




    #Because we can't save nested python classes by just picking them,
    #we have to go through each song in each album, save that separately,
    #then flatten the attribute into just its title.
    #We'll build another function to reconstruct the class from these flattened pickles below
    def saveArtist(self):
        try:
            global artistdir
            artistdir
            thisartistdir = '{}{}'.format(artistdir,self.name.encode("utf-8"))
        except NameError:
            artistdir = raw_input("No Artistdir defined, where should we put the pickled artist?:")

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
        s = open(selfile,"wb")
        pickle.dump(tempself.__dict__,s,-1)
        s.close()
        print("Artist Saved: {}".format(self.name))

        #Take slashes out of titles
    def cleanTitles(artist):
        for i in range(len(artist.albums)):
            for j in range(len(artist.albums[i].songs)):
                artist.albums[i].songs[j].title = re.sub('/',' ', artist.albums[i].songs[j].title)
        return artist

    def listAlbums(self):
        for i in range(len(self.albums)):
            print("{}".format(self.albums[i].title))

    # def compileCorpus(self):
    #     self.corpus = list()
    #     for i in range(len(self.albums)):
    #         for j in range(len(self.albums[i].songs)):
    #             #Clean Out Verses by Other People
    #
    #             self.corpus.append(self.albums[i].songs[j].l)

class Album:
    def __init__(self,url):
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
        self.title = nametemp[2:] #Getting rid of leading whitespace...



def makeArtists(artlist):
    artists = list()
    for i in range(len(artlist)):
        print("Making {}".format(artlist[i]))
        artemp = Artist("{}".format(artlist[i]))
        artemp.cleanTitles()
        artemp.saveArtist()
        artists.append(artemp)
    return artists


################
#Zombie Code

        #Walk through RG pages

    # atEnd = False
    # listcount = 1
    # songlinklist = list()
    # while atEnd == False:
    #     print('Getting Link List Page %d' %listcount)
    #     songlisturl = "http://genius.com/search?page=%d&q=%s" % (listcount, str(re.sub(' ','+',ArtistName)))
    #     songlistpage = requests.get(songlisturl)
    #     soup = bs(songlistpage.text,"html.parser")
    #     songlisttemp = soup.find_all(class_="song_link")
    #     if not songlisttemp:
    #         break
    #     else:
    #         listcount = listcount + 1
    #     for j in range(len(songlisttemp)):
    #         songlinklist.append(songlisttemp[j])
    # self.songlinks = songlinklist

    #Build song objects in artist class def
        # songs = list()
        # numsongs = len(songlinklist)
        # for i in range(len(songlinklist)):
        #     print("Building Song Object %d of %d" % (i,numsongs))
        #     songlink = songlinklist[i].get('href')
        #     songs.append(Song(songlink))
        # self.songs = songs