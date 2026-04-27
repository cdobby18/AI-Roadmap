# Libraries
from random import choice, randint, shuffle
import cowsay
import sys
import requests
import json
import urllib.parse
import re

options = ["heads", "tails"]
coin = choice(options)
print(coin)

number = randint(1,10)
print(number)

cards = ["jack", "queen", "king"]
shuffle(cards)
for card in cards:
    print(card)

#if len(sys.argv) == 2:
#  cowsay.trex("hello, " + sys.argv[1])


# API REQUESTS
if len(sys.argv) != 2:
    sys.exit("Missing search term")

term = urllib.parse.quote(sys.argv[1])

# itunes api
response = requests.get(
    f"https://itunes.apple.com/search?entity=song&limit=10&term={term}"
)

data = response.json()

# filter symbols 
def is_clean(title):
    return re.match(r"^[A-Za-z0-9\s\-\(\)\&\.\']+$", title)

# filter result
for result in data["results"]:
    title = result["trackName"]
    artist = result["artistName"]

    if is_clean(title):
        print(f"{title} - {artist}")