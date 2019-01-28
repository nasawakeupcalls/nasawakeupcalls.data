#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Stage 2 script for manipulating the NASA wakeup call data. This script will
convert date and line delineated data into some sort of JSON structure that as
yet is unknown and will evolve with the data.
"""

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import re
import json
import sys


def flush_section(section):
    print(pretty_json(section))
    section.clear()
    return {}


def pretty_json(dict_data):
    return json.dumps(
        dict_data, sort_keys=True, indent=4, separators=(',', ': '))


def format_contents(contents):
    return contents.replace("\n", "").replace('\\"', "").strip()


def format_and_print_date_match(section, match_object, line):
    """Output what we know when we receive a new Date match."""
    print("")
    if match_object is not None:
        print("MISSION:", mission)
        print("DATE:", match_object.group(0).replace(":", "").strip())
        contents = line.split(match_object.group(0), 1)
        if len(contents) == 2:
            formatted = format_contents(contents[1])
            # Split song if at all possible.
            song_artist = formatted.split(" by ", 1)
            if len(song_artist) == 2:
                print("SONG:", song_artist[0])
                artist_comment = song_artist[1].split("COMMENT:", 1)
                if len(artist_comment) <= 2:
                    print("ARTIST:", artist_comment[0].strip())
                    try:
                        if "TEAM" in artist_comment[1]:
                            print("COMMENT:", artist_comment[1]\
                                .split("TEAM", 1)[0].strip())
                            print("TEAM:", artist_comment[1]\
                                .split("TEAM", 1)[1].replace(":", "").strip())
                        else:
                            comment = artist_comment[1]
                            print("COMMENT:", comment.strip())
                    except IndexError:
                        pass
                else:
                    print("Error!", formatted, "\n", file=sys.stderr)
            else:
                print("Error!", formatted, "\n", file=sys.stderr)
        else:
            print("Error with: {}".format(contents), file=sys.stderr)


def find_mission(section, line):
    """Function docstring."""
    gemini = "^GEMINI.[0-9]{1,2}"
    apollo = "^APOLLO.[0-9]{1,2}"
    skylab = "^SKYLAB.[0-9]{1}"
    space_shuttle = "^STS-[0-9]{1,3}"
    pathfinder = "^MARS.PATHFINDER"
    iss = "^INTERNATIONAL SPACE STATION.[(]ISS[)]"
    spirit = "^MARS SPIRIT"
    opportunity = "^MARS OPPORTUNITY"
    missions = [gemini, apollo, skylab, space_shuttle, iss, pathfinder,
                spirit, opportunity]
    for miss in missions:
        match = re.match(miss, line)
        if match:
            tmp_mission = match.group(0)
            if line.startswith("STS-"):
                tmp_mission = line.split(" ", 1)[0].strip()
            global mission
            mission = tmp_mission


# Global to be used throughout splitter.
mission = None


def split_lines(section, line):

    find_mission(section, line)

    # Regular expressions of interest to us.
    date_expr = "^[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}"
    sol_expr = "^Sol.[0-9]{1,3}.?[0-9]{0,3}:"
    military_expr = "^[0-9]{2}.[0-9]{2}.[0-9]{2}.[0-9]{2}"

    # Find our matches.
    date_match = re.match(date_expr, line)
    sol_match = re.match(sol_expr, line)

    # Turns out this might not be a military thing after all. May be some sort
    # of timestamp related to a recording device.
    military_match = re.match(military_expr, line)

    # Output depending on what we want to do.
    if date_match:
        format_and_print_date_match(
            section=section, match_object=date_match, line=line)
        return
    elif sol_match:
        format_and_print_date_match(
            section=section, match_object=sol_match, line=line)
        return
    if military_match:
        print("There should be no military matches now, and it turns out this "
              "regex related to an audio time-stamp (possibly!) from the "
              "mission records.", file=sys.stderr)
        return
        # Leave the below for now...
        format_and_print_date_match(
            section=section, match_object=military_match, line=line)
        return

    if line.startswith("CAPCOM"):
        capcom = line.split("CAPCOM", 1)[1].replace(":", "").strip().replace("\n", "")
        print("CAPCOM:", capcom)
        return

    if line.startswith("INTRO"):
        intro = line.split("INTRO", 1)[1].replace(":", "").strip()
        print("INTRO:", intro)
        return

    if line.startswith("TIME"):
        intro = line.split("TIME", 1)[1].replace(":", "").strip()
        print("TIME:", intro)
        return

    else:
        # [n] markup denotes missions with no info and reasons why there is
        # no info.
        if line.startswith("[n]"):
            print(line.strip(), file=sys.stderr)
        elif line.startswith("######"):
            """Do nothing."""
        elif line.startswith("-----"):
            """Do nothing."""
        elif line == "\n":
            """Do nothing."""
        else:
            """Do nothing."""
            #print("{}".format(line.strip()), file=sys.stderr)


def main():
    """Primary entry point of the script."""
    parser = argparse.ArgumentParser(description='Process the NASA wakeup calls.')
    parser.add_argument('file', metavar='FILE', type=str, nargs=1,
                        help='wakeup call file to process')

    args = parser.parse_args()

    if not args.file:
        print(parser.print_help())

    section = {}
    try:
        with open(args.file[0]) as file_:
            for line in file_:
                split_lines(section, line)
    except IOError:
        print("IOError: Problem parsing file %s", args.file[0])


if __name__ == "__main__":
    main()
