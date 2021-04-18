import pandas as pd
import numpy as np
import re
import nltk
from nltk.stem import  WordNetLemmatizer # czy to zaimportowałem powyzej?
from nltk.sentiment import SentimentIntensityAnalyzer # chyba ne
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image


polishrevs = pd.read_csv("polishreviews.csv")
polishrevs

def tokenizer(recki):
    global tokenized
    tokenized = nltk.word_tokenize(recki)
    stopwords = nltk.corpus.stopwords.words("english")
    tokenized = [w for w in tokenized if w not in stopwords]
    tokenized = [i for i in tokenized if len(i) > 2]
    lemmatizer = WordNetLemmatizer()
    tokenized = ' '.join([lemmatizer.lemmatize(w) for w in tokenized])
    tokenized = nltk.word_tokenize(tokenized)


all = str(polishrevs.reviews.str.cat(sep = " "))
tokenizer(all)

len(tokenized) # All reviews have a 23758159 words

# all reviews word cloud
# poland - shape cloud
# polsh colors function
def pl_color_func(word=None, font_size=None,
                     position=None, orientation=None,
                     font_path=None, random_state=None):
    colors = [[351, 73, 48],
              [40, 5, 82]]
    rand = random_state.randint(0, len(colors) - 1)
    return "hsl({}, {}%, {}%)".format(colors[rand][0], colors[rand][1], colors[rand][2])

cloud = str()
cloud = " ".join(tokenized)
mask = np.array(Image.open("poland.png"))
wc = WordCloud(background_color = "white", width = 1000, 
                height= 1000,  mask=mask, collocations = False, 
                min_font_size = 5, max_words = 500, color_func = pl_color_func)
wc.generate(cloud)
plt.imshow(wc, interpolation="bilinear")
plt.axis('off')
plt.savefig("E:\\toke_lemma.png", dpi = 300, quality=100)


# unshapen - easier to read cloud
# black color function
def black_color_func(word=None, font_size=None, 
                   position=None, orientation=None, 
                   font_path=None, random_state=None):
    h = 0 
    s = 0 
    l = 20
    return "hsl({}, {}%, {}%)".format(h, s, l)

mask = np.array(Image.open("unshapen.png"))
wc = WordCloud(background_color = "white", width = 1920, 
                height= 1080,  mask=mask, collocations = False, prefer_horizontal=1, 
                min_font_size = 15, max_words = 1000, color_func = black_color_func) # font_path ="E:\\Czcionki\\Cyberpunk_Regular.ttf",
wc.generate(cloud)
plt.imshow(wc, interpolation="bilinear")
plt.axis('off')
plt.savefig("E:\\unshapen.png", dpi = 300, quality=100)

# visualising most frequent words among all reviews
freqdis = nltk.FreqDist(tokenized) 
freq = freqdis.most_common(50)
word = np.array([ i for i, j in freq ])
frequency = np.array([ j for i, j in freq ])

fig, ax = plt.subplots()
plt.style.use("ggplot")
ax.barh(word[1:41], frequency[1:41], color = "#DC143C")
ax.set_xlabel("Frequency of appearance")
ax.set_ylabel("Word")
ax.set_title("The 40 most common words in all reviews")
# plt.show()
fig.set_size_inches([16, 9])
fig.savefig("E:\\chart_40_words.png",
            quality = 100,
            dpi = 300) 


# collocations in all reviews
bigrams = nltk.collocations.BigramCollocationFinder.from_words(tokenized)
bigrams.ngram_fd.most_common(30)
trigrams = nltk.collocations.TrigramCollocationFinder.from_words(tokenized)
trigrams.ngram_fd.most_common(30)
quadgrams = nltk.collocations.QuadgramCollocationFinder.from_words(tokenized)
quadgrams.ngram_fd.most_common(30)

# visualising structure of reviews and player involvement
# participation of reviews
majority_revs = polishrevs.sort_values(by = "num_reviews", ascending = False)[:4]
minority_revs = polishrevs.sort_values(by = "num_reviews", ascending = False)[4:]
minority_revs = minority_revs["num_reviews"].sum()

major_titles = majority_revs.title.to_list()
major_revs = majority_revs.num_reviews.to_list()

major_revs = np.array(major_revs + [int(minority_revs)])
major_titles = np.array(major_titles + ["Other"])
major_titles[1] = "The Witcher 3: Wild Hunt"

fig, ax = plt.subplots()
plt.pie(major_revs, labels = major_titles, 
        autopct = "%1.1f%%", startangle=90,
        labeldistance=1.15, colors=['#FFC107', '#004D40', '#DD7B7D', '#C6ACC7', '#5F24E3'])
ax.set_title("Participation of reviews of individual games")
plt.show()

# participation of played time
polishrevs["sum_playtime_in_hours"] = round(polishrevs["sum_playtime_in_mins"] / 60)
polishrevs["sum_playtime_in_hours"] = polishrevs["sum_playtime_in_hours"].astype("int")
polishrevs.sort_values(by = "sum_playtime_in_hours", ascending = False)[:10]

majority_hours = polishrevs.sort_values(by = "sum_playtime_in_hours", ascending = False)[:4]
minority_hours = polishrevs.sort_values(by = "sum_playtime_in_hours", ascending = False)[4:]["sum_playtime_in_hours"]
minority_hours = sum(minority_hours)


major_titles = majority_hours.title.to_list()
major_titles = np.array(major_titles + ["Other"])
major_hours = majority_hours.sum_playtime_in_hours.to_list()
major_hours = np.array(major_hours + [int(minority_hours)])
major_titles[1] = "The Witcher 3: Wild Hunt"

fig, ax = plt.subplots()
plt.pie(major_hours, labels = major_titles, 
        autopct = "%1.1f%%", startangle=90,
        labeldistance=1.15, colors=['#FFC107', '#004D40', '#DD7B7D', '#C6ACC7', '#5F24E3'])
ax.set_title("Participation of hours of individual games")
plt.show()


##This is unfinished analysis which I share due to prove my future employer that I can code a bit in Python
## soon I will add an analysis of words without biggest polish titles
## comparision of occurence of particular positive words over time to check are games became better in players opinions (without sentiment analysis this time)
## analysis of words of some most popular polish gamesD
