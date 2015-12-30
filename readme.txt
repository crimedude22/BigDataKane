A set of tools to analyze hip hop lyrics, though you could probably do other shit with it that I don't care about.

Yes the code is terrible.

Requires:
-BeautifulSoup (I think you'll need v4, but who the hell knows)
-SciPy
-MatPlotLib
-sklearn
-nltk

[12/30/15]
The InfoExtract tools are pretty much the only tools that exist. So far they can take a batch of lyric pages from RapGenius, extract the lyrics, and index the lyrics by artist.  Working on having it clean the lyrics of common/useless/the artists name words.

I've opted for using a generalized index system rather than keeping the files distinctly named so that the tools can be modular. Any part of the data can be accessed and iterated upon because of the numeric indices for the lyrics. 



To Do:
-actually implement scraping and crawling of rapgenius instead of doing the shitty downthemall thing
