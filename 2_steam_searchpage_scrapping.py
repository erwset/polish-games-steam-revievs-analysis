from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import regex as re
import random

data = {"title" : [], "link" : []}

temp = open("links.txt",'r').readlines()
adresses = []
for i in temp:
    adresses.append(i.replace("\n",""))

# Here's a function which gathers links from steam search page if particular title link covers searched game (including dlc, soundtrack etc.).
# I use this if statement because I don't know which game from the list is available on Steam, and result may not be a polish game if I search absent title.
def link_soup(adres):
    url = adres
    cookies = {"birthtime" : "",
        "wants_mature_content" : "1",
        "lastagecheckage" : ""} # here were cookies from my browser to avoid age checking
    headers = {
        "user-agent" : "",
        "referer" : "https://store.steampowered.com/"
        }
    r = requests.get(url, headers = headers)
    print(r.status_code)

    soup = BeautifulSoup(r.content, "html.parser")
    results_container = soup.find("div", id="search_resultsRows")
    query = soup.find("input",  id="term")["value"]

    if results_container is None:
        print("Not found " + str(query))
    else:
        for i in results_container.find_all("a"):
            link = str(i["href"])
            title = str(i.span.string)
            if re.match(query, title):
                data["title"].append(title)
                data["link"].append(link)


for i in adresy:
    time.sleep(random.uniform(1, 1.5))
    link_soup(i)


frame = pd.DataFrame(data)
frame.drop_duplicates(inplace=True)
frame.to_csv("links_and_titles.csv", encoding = "utf-8", index = False)

