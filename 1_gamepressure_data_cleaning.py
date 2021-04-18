import json
import pandas as pd
import regex as re

with open("gamepressure_list_of_games.json", 'r', encoding='utf-8') as f: 
    dirtytitles = json.load(f)


dirtytitlesdf = pd.DataFrame(dirtytitles)
print(dirtytitlesdf)

# dealing with unwanted nulls
print(dirtytitlesdf.isna().sum())
dirtytitlesdf.dropna(inplace=True)
dirtytitlesdf = dirtytitlesdf.reset_index(drop=True)

# remove "(PC)"
dirtytitlesdf["title"] = dirtytitlesdf["title"].str.replace("(\s\WPC\W)", "", regex=True)

# simplyfying relase_date column
for i in range(len(dirtytitlesdf)):
    if dirtytitlesdf.iloc[i, 1] in (" TBA", " canceled"):
        continue
    one = re.search(("\d\d\d\d"), dirtytitlesdf.iloc[i, 1])
    dirtytitlesdf.iloc[i, 1] = one[0]

dirtytitlesdf.columns = ["title", "year", "genre"]

# prepare a list of links for steam search page
cleandata = dirtytitlesdf[dirtytitlesdf["year"] != " TBA"]
cleandata = cleandata[cleandata["year"] != " canceled"]
cleandata.year = cleandata.year.astype("int64")
cleandata.year.dtype
cleandata = cleandata[cleandata["year"] < 2022]
urls = list(cleandata.title)
urls = [i.replace(" ","+") for i in urls]
urls = ["https://store.steampowered.com/search/?term=" + i.replace("\t", "") for i in urls]
urls
