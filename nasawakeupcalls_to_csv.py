#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from pandas import DataFrame


dates_arr = []
program_arr = []
missions_arr = []
artists_arr = []
songs_arr = []


def pretty_json(dict_data):
    """Function docstring."""
    return json.dumps(
        dict_data, sort_keys=True, indent=4, separators=(',', ': '))


def output_rows(program, mission):
    """Function docstring."""
    name = mission.get("Mission")
    calls = mission.get("WakeupCalls", [])
    for call in calls:
        for date, songlist in call.iteritems():
            date_ = date
            for song in songlist:
                dates_arr.append(date_)
                program_arr.append(program)
                missions_arr.append(name)
                artists_arr.append(song["ARTIST"])
                songs_arr.append(song["SONG"])


def list_to_csv():
    """Function docstring."""
    space_rows = {
        "Dates": dates_arr,
        "Program": program_arr,
        'Mission': missions_arr,
        "Artist": artists_arr,
        "Song": songs_arr,
    }
    df = DataFrame(space_rows, columns= [
        'Dates', "Program", 'Mission', 'Artist', 'Song'])
    df.sort_values(by=['Dates'])
    df.to_csv ("nasawakeupcalls.csv", index=None, header=True, encoding='utf8')


def main():
    """Primary entry point of the script."""
    data = None
    with open('nasawakeupcalls.json') as f:
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
