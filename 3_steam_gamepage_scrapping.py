from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import regex as re
import random


table = pd.DataFrame(pd.read_csv("links_and_titles.csv"))
games_links = table.iloc[:,1].tolist()
clear_links = []
for i in games_links:
    if re.match("https://store.steampowered.com/bundle", i):
        print("bundle")
    else:
        clear_links.append(i)


games = {"id_number" : [], "title" : [], "developer" : [], "relase_date" : []}


def game_soup(adres):
    cookies = {"birthtime" : "",
        "wants_mature_content" : "1",
        "lastagecheckage" : ""} # here were cookies from my browser to avoid age checking

    url = adres

    headers = {
        "user-agent" : "",
        "referer" : "https://store.steampowered.com/"
        }

    r = requests.get(url, headers = headers, cookies = cookies)
    print(r.status_code)

    soup = BeautifulSoup(r.content, "html.parser")
    if soup.find("div", class_ = "apphub_AppName") is None:
        print("title error")
    else:
        print(soup.find("div", class_ = "apphub_AppName").string)

    if soup.find("div", class_ = "summary column", id = "developers_list") is None or soup.find("div", class_ = "date") is None or soup.find("div", class_ = "apphub_AppName") is None or soup.find("div", class_ = "glance_tags popular_tags") is None:
        print("position isn't fill")
    else:
        gry["id_number"].append(soup.find("div", class_ = "glance_tags popular_tags")["data-appid"])
        gry["title"].append(soup.find("div", class_ = "apphub_AppName").string)
        gry["developer"].append(soup.find("div", class_ = "summary column", id = "developers_list").a.string)
        gry["relase_date"].append(soup.find("div", class_ = "date").string)


for i in clear_links:
    time.sleep(random.uniform(1, 4))
    game_soup(i)


games_df = pd.DataFrame(games)
games_df.to_csv("games.csv", encoding = "utf-8", index = False)