import json
import numpy as np
import pandas as pd

frame = pd.DataFrame(pd.read_csv("games.csv"))
app_ids = frame.iloc[:,0].tolist()
app_ids = np.unique(app_ids)

num_revs = {"id_number" : [], "num_reviews": [], "sum_playtime_in_mins": [], "reviews" : []}

def data_extractor(game_id):
    print("Open json with id" + str(game_id))
    with open("review_"+str(game_id)+".json", 'r', encoding='utf-8') as f:  # here I open every json I downloaded using steam reviews module
        content = json.load(f)

    sum_reviews = str()
    for i in content["reviews"].values():
        sum_reviews = sum_reviews + str(" " + i["review"])

    sum_playtime = int()
    for i in content["reviews"].values():
        review_author = i["author"]
        sum_playtime = sum_playtime + review_author["playtime_forever"]

    num_revs["id_number"].append(game_id)
    num_revs["num_reviews"].append(len(content["reviews"]))
    num_revs["sum_playtime_in_mins"].append(sum_playtime)
    num_revs["reviews"].append(sum_reviews)


for i in app_ids:
    data_extractor(i)


revs = pd.DataFrame(num_revs)


# Merging data from Steam game pages with json reviews data
infos = pd.read_csv("games.csv")
infos.drop_duplicates(inplace = True, ignore_index = True)
inforevs = infos.merge(revs, on = "id_number")
inforevs.dropna(inplace = True)

# cleaning reviews column
inforevs.reviews = inforevs.reviews.str.lower()
inforevs.reviews.replace(to_replace = "[^a-zA-Z \s]", value = " ", inplace = True, regex = True)
inforevs.reviews.replace(to_replace = "[\n]", value = " ", inplace = True, regex = True)
inforevs.reviews.replace(to_replace = " +", value = " ", inplace = True, regex = True)
inforevs.reset_index(drop=True, inplace=True)

# simplifying dates
for i in range(len(inforevs)):
     inforevs.loc[i,"relase_date"] = inforevs.loc[i,"relase_date"][-4:]
inforevs.relase_date = inforevs.relase_date.astype("int64")

inforevs.columns = ['title_id', 'title', 'developer', 'relase_date', 'num_reviews','sum_playtime_in_mins', 'reviews']
inforevs.to_csv("polishreviews.csv")