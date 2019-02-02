#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Stage 3 script for turning the primary dataset into something more JSON like
to see what we've got!
"""

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import json
import sys


def pretty_json(dict_data):
    return json.dumps(
        dict_data, sort_keys=True, indent=4, separators=(',', ': '))


secondary_dict = {}
tertiary_dict = {}

primary_arr = []
wakeup_calls_arr = []

date_dict = {}

# Consts to create the dictionary keys.
INTRO = "Introduction"
MISSION = "Mission"
WAKEUPCALLS = "WakeupCalls"
COMMENT = "Comment"
IBID = "Ibid."


def convert_to_iso(day):
    """Do a string based conversion to an ISO-ish date."""
    if day.lower().startswith("sol"):
        return day
    day_ = day.replace("-", "/")
    mm, dd, yy = day_.split("/", 2)
    if len(mm) == 1:
        mm = "0{}".format(mm)
    if len(dd) == 1:
        dd = "0{}".format(dd)
    if int(yy) >= 65 and int(yy) <= 99:
        return "19{}-{}-{}".format(yy, mm, dd)
    elif len(yy) == 4:
        return "{}-{}-{}".format(yy, mm, dd)
    else:
        return "20{}-{}-{}".format(yy, mm, dd)


def fix_date(date_):
    """Function docstring"""
    for day, songs in date_.items():
        new_day = convert_to_iso(day)
        date_[new_day] = date_.pop(day)
        return


def de_dupe_comments(day, songs):
    """De-dupe comments in a fairly sensible way for the output."""
    if len(songs) == 1:
        return
    comment_a = None
    for song in songs:
        try:
            comment_b = song[COMMENT]
        except KeyError:
            continue
        if comment_b != comment_a:
            comment_a = comment_b
            continue
        if comment_b == comment_a:
            song[COMMENT] = IBID


def process_and_print_primary_arr(primary_arr):
    """Pre-process the output once it has been formatted into JSON the first
    time around.
    """

    for mission in primary_arr:
        wakeupcalls = mission[WAKEUPCALLS]
        # We have a group of calls here. De-dupe comments.
        for date_ in wakeupcalls:
            fix_date(date_)
            for day, song in date_.items():
                de_dupe_comments(day, song)

    print(pretty_json(primary_arr))


def split_lines(line):
    """Go through each line and build our dictionary."""
    global tertiary_dict
    global secondary_dict
    global wakeup_calls_arr
    global date_dict
    vals = [
        "DATE",
        "SOL",
        "SONG",
        "ARTIST",
        "CAPCOM",
        "COMMENT",
        "TIME",
        "TEAM",
    ]
    if line.startswith("MISSION"):
        line_ = line.replace("MISSION", "", 1)\
            .replace('"', "").replace(":", "", 1).strip()
        try:
            if tertiary_dict[MISSION] != line_:

                if wakeup_calls_arr:
                    tertiary_dict[WAKEUPCALLS] = wakeup_calls_arr
                    wakeup_calls_arr = []
                    primary_arr.append(tertiary_dict)
                    tertiary_dict = {}
                    pass

        except KeyError:
            pass
        tertiary_dict[MISSION] = line_
        return
    if line.startswith("INTRO"):
        intro = line.replace("INTRO", "", 1)\
            .replace('"', "").replace(":", "", 1).strip()
        if intro.lower() != "none":
            tertiary_dict[INTRO] = intro
        return
    for value in vals:
        if line.startswith(value):
            output = line.replace(value, "", 1)\
                .replace('"', "").replace(":", "", 1).strip()
            if value == "DATE" or value == "SOL":
                if output not in date_dict:
                    date_dict[output] = []
                if value == "SOL":
                    secondary_dict[value] = output
                return
            if value == "COMMENT":
                if output != "n/a":
                    secondary_dict[COMMENT] = output
                return
            else:
                secondary_dict[value] = output
                return

    if line.startswith("EOE"):
        try:
            tertiary_dict["Title"] = secondary_dict[MISSION]
        except KeyError:
            pass
        # The secondary dict stores a single wake-up call and we get one per
        # EOE and that gets added to the date dictionary which is per day.
        if secondary_dict:
            if date_dict:
                for d_ in date_dict:
                    date_dict[d_].append(secondary_dict)
                if not wakeup_calls_arr:
                    wakeup_calls_arr.append(date_dict)
                    secondary_dict = {}
                    date_dict = {}
                    return
                else:
                    for w_ in wakeup_calls_arr:
                        for k_ in w_.keys():
                            for date_ in date_dict.keys():
                                if date_ == k_:
                                    w_[k_].append(date_dict[date_][0])
                                    secondary_dict = {}
                                    date_dict = {}
                                    return
                wakeup_calls_arr.append(date_dict)
                secondary_dict = {}
                date_dict = {}
                return
            else:
                print("Error! No DATE dict!", file=sys.stderr)
                return
    if not line.startswith("\n"):
        print("Not found: x{}x".format(line), file=sys.stderr)


def main():
    """Primary entry point of the script."""
    parser = argparse.ArgumentParser(
        description='Process the NASA wakeup calls.')
    parser.add_argument('file', metavar='FILE', type=str, nargs=1,
                        help='wakeup call file to process')
    args = parser.parse_args()
    if not args.file:
        print(parser.print_help())
    try:
        with open(args.file[0]) as file_:
            for line in file_:
                split_lines(line)
    except IOError:
        print("IOError: Problem parsing file %s", args.file[0])
    if wakeup_calls_arr:
        tertiary_dict["WakeupCalls"] = wakeup_calls_arr
        primary_arr.append(tertiary_dict)

    process_and_print_primary_arr(primary_arr)


if __name__ == "__main__":
    main()
