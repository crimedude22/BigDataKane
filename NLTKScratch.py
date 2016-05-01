import nltk
import requests
from bs4 import BeautifulSoup as bs
import re
import pickle

##To do from 4.30: Have to make search function that finds the song links specific to the artist search, right now it is just finding everythign that mentions the artist.

basedir = "/Users/Jonny/Documents/RapData/"

#Class definitions
class Song:
    def __init__(self, url):
        songpage = requests.get(url)
        soup = bs(songpage.text, "html.parser")

        #Extract info
        try:
            title = soup.find(class_="song_header-primary_info-title").get_text()
            mainArtist = soup.find(class_="song_header-primary_info-primary_artist").get_text()
            featlist = soup.find(collection="song.featured_artists").extract()
            featlist = featlist.find_all(href=re.compile("artists"))
            feat = list()
            for i in range(len(featlist)):
                feat.append(featlist[i].get_text())
            album = soup.find(href=re.compile("albums")).get_text()
            year = soup.find(class_="song_album-info-release_year").get_text()
            lyrics = soup.find(class_="lyrics").get_text()

            #Class it up
            self.title = title
            self.artist = mainArtist
            self.album = album
            self.year = year
            self.feat = feat
            self.lyrics = lyrics
        except:
            print("Something went wrong")

class Artist:
    def __init__(self, ArtistName):
        self.name = ArtistName
        #Get the artist page
        urlname = re.sub(' ','-', ArtistName)
        rgurl = "http://genius.com/artists/%s" % str(urlname)
        artistpage = requests.get(rgurl)
        artistsoup = bs(artistpage.text,"html.parser")
        self.url = rgurl

        #Have to go through all the pages...

        atEnd = False
        listcount = 1
        songlinklist = list()
        while atEnd == False:
            print('Getting Link List Page %d' %listcount)
            songlisturl = "http://genius.com/search?page=%d&q=%s" % (listcount, str(re.sub(' ','+',ArtistName)))
            songlistpage = requests.get(songlisturl)
            soup = bs(songlistpage.text,"html.parser")
            songlisttemp = soup.find_all(class_="song_link")
            if not songlisttemp:
                break
            else:
                listcount = listcount + 1
            for j in range(len(songlisttemp)):
                songlinklist.append(songlisttemp[j])
        self.songlinks = songlinklist

        #Build song objects
        songs = list()
        numsongs = len(songlinklist)
        for i in range(len(songlinklist)):
            print("Building Song Object %d of %d" % (i,numsongs))
            songlink = songlinklist[i].get('href')
            songs.append(Song(songlink))
        self.songs = songs

        #Build album objects\
        albumlinklist = artistsoup.find_all(class_="album_link")
        albums = list()
        numalbums = len(albumlinklist)
        for i in range(len(albumlinklist)):
            print("Building Album Object %d of %d" % (i, numalbums))
            albumlink = albumlinklist[i].get('href')
            albums[i] = Album(albumlink)

        #Pickle the created artist object
            #Get to this next time





class Album:
    def __init__(self,url):
        albumpage = requests.get(url)
        albumsoup = bs(albumpage.text,"html.parser")
        songlinklist = albumsoup.find_all(class_="song_link")
        songs = list()
        for i in range(len(songlinklist)):
            songlink = songlinklist[i].get('href')
            songs[i] = Song(songlink)
        self.songs = songs
        self.artist = albumsoup.find(class_="album_artist").get_text()
        self.year = albumsoup.find(class_="release_year").get_text().replace("(","").replace(")","").replace(" ","") #yeah this sucks shut up
        nametemp = albumsoup.find(class_="album_name").contents[0].replace("\n","")
        self.name = nametemp[2:] #Getting rid of leading whitespace...




#Function definitions
#Moving to class function init
def buildArtistFromRG(artist):
    #Get the artist page
    urlname = re.sub(' ','-', artist)
    rgurl = "http://genius.com/artists/%s" % str(urlname)
    artpage = requests.get(rgurl)
    soup = bs(artpage.text, "html.parser")
    #Get the list of links to the artist's songs
    songlinks = list()
    linklist = soup.find_all(class_="song_link")
    for i in range(len(linklist))
        songlinks(i) = linklist[i].get('href')


        #Call "Get song info from rg fxn here


def getSongRG(url):
    #Get song artists, album, year from rapgenius URL, return as combined list
    #[Title, MainArtist, Album, Year, Feat, Lyrics]
    songpage = requests.get(url)
    soup = bs(songpage.text, "html.parser")
    title = soup.find(class_="song_header-primary_info-title").get_text()
    mainArtist = soup.find(class_="song_header-primary_info-primary_artist").get_text()
    featlist = soup.find(collection="song.featured_artists").extract()
    featlist = featlist.find_all(href=re.compile("artists"))
    feat = list()
    for i in range(len(featlist)):
        feat.append(featlist[i].get_text())
    album = soup.find(href=re.compile("albums")).get_text()
    year = soup.find(class_="song_album-info-release_year").get_text()
    lyrics = soup.select(".lyrics")
    lyrics = lyrics[0]
    lyrics_string = lyrics.get_text

    #Class it up
    song = Song(title,mainArtist,album,year,feat,lyrics_string)
    return song
