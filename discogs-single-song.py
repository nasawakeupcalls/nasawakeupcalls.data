#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import requests

DISCOGS_URL = "https://www.discogs.com"
DISCOGS_API = "https://api.discogs.com/database/search?"


def discogs_api(song=None, artist=None):
    """retrieves the top search result from discogs for a given song &
    artist combination.
    """
    header = {"Authorization": "Discogs token={}".format(DISCOGS_TOKEN.strip())}
    payload = {"per_page": 1, "page": 1}

    if artist is not None:
        payload.update({"artist": artist})
    if song is not None:
        payload.update({"release_title": song})

    req = requests.get(DISCOGS_API, headers=header, params=payload)

    return req.json()["results"]


def get_song_info(song, artist):
    """Searches the discogs database using the data for the given index in the
    data frame.
    """
    if type(song) == float:
        return
    for u in ["unknown", "unidentified", "untitled", "medley"]:
        if u in song.lower():
            return
    if artist == "Unidentified":
        artist = None
    data = discogs_api(song, artist)
    if len(data) == 0:
        return
    else:
        data = data[0]
    results = []
    for key in ["genre", "style", "year", "master_url"]:
        if key not in data:
            continue
        elif type(data[key]) != list:
            if data[key] is not None:
                results.append((key, data[key]))
        elif len(data[key]) == 0:
            continue
        else:
            results.append((key, data[key][0]))
    if "uri" in data:
        if data["uri"] != "None":
            results.append((key, "{}{}".format(DISCOGS_URL, data["uri"])))

    return results, data


with open(
    ".token"
) as token_file:  # Get an API token from discogs and save as token.txt
    DISCOGS_TOKEN = token_file.read()

song = input("Please enter song name: ")
artist = input("Please enter artist name: ")

# For example: results, data = get_song_info(song="planet caravan", artist="black sabbath")
results, data = get_song_info(song=song, artist=artist)

print(json.dumps(data, indent=2, sort_keys=True))
print("")
print("Summary:")
for res in results:
    print("{}: {}".format(res[0], res[1]))
