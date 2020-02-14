#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from pandas import DataFrame


dates_arr = []
program_arr = []
missions_arr = []
artists_arr = []
songs_arr = []
comment_arr = []
genre_arr = []
style_arr = []
year = []
discogs_master = []
discogs_ur = []


def pretty_json(dict_data):
    """Function docstring."""
    return json.dumps(dict_data, sort_keys=True, indent=4, separators=(",", ": "))


def output_rows(program, mission):
    """Function docstring."""
    name = mission.get("Mission")
    calls = mission.get("WakeupCalls", [])
    for call in calls:
        for date, songlist in call.items():
            date_ = date
            for song in songlist:
                dates_arr.append(date_)
                program_arr.append(program)
                missions_arr.append(name)
                artists_arr.append(song["Artist"])
                songs_arr.append(song["Song"])
                comment_arr.append(song.get("Comment", ""))
                genre_arr.append(song.get("Genre", ""))
                style_arr.append(song.get("Style", ""))
                year.append(song.get("Year", ""))
                discogs_master.append(song.get("DiscogsMasterURL", ""))
                discogs_ur.append(song.get("DiscogsURI", ""))


def list_to_csv():
    """Function docstring."""
    space_rows = {
        "Dates": dates_arr,
        "Program": program_arr,
        "Mission": missions_arr,
        "Artist": artists_arr,
        "Song": songs_arr,
        "Comment": comment_arr,
        "Genre": genre_arr,
        "Style": style_arr,
        "Year": year,
        "Discogs Master": discogs_master,
        "Discogs URI": discogs_ur,
    }
    df = DataFrame(
        space_rows,
        columns=[
            "Dates",
            "Program",
            "Mission",
            "Artist",
            "Song",
            "Comment",
            "Genre",
            "Style",
            "Year",
            "Discogs Master",
            "Discogs URI",
        ],
    )
    df.sort_values(by=["Dates"])
    df.to_csv("nasawakeupcalls.csv", index=None, header=True, encoding="utf8")


def main():
    """Primary entry point of the script."""
    data = None
    with open("nasawakeupcalls.json") as f:
        data = json.load(f)
    for program in data["Programs"]:
        program_ = program.get("Title")
        missions = program.get("Missions", [])
        for mission in missions:
            if not mission.get("WakeupCalls"):
                continue
            output_rows(program_, mission)
    list_to_csv()


if __name__ == "__main__":
    main()
