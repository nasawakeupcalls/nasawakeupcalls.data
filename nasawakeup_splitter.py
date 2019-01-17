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
        print("Mission", mission)
        print("Date", match_object.group(0))
        contents = line.split(match_object.group(0), 1)
        if len(contents) == 2:
            formatted = format_contents(contents[1])
            print("Contents", formatted)
        else:
            print("Error with: {}".format(contents), file=sys.stderr)
        print("")

def find_mission(section, line):

    gemini = "^GEMINI.[0-9]{1,2}"
    apollo = "^APOLLO.[0-9]{1,2}"
    skylab = "^SKYLAB.[0-9]{1}"
    space_shuttle = "^STS-[0-9]{1,3}"
    pathfinder = "^MARS.PATHFINDER"
    spirit = "^MARS SPIRIT"
    opportunity = "^MARS OPPORTUNITY"
    missions = [gemini, apollo, skylab, space_shuttle, pathfinder,
                spirit, opportunity]
    for miss in missions:
        match = re.match(miss, line)
        if match:
            global mission
            mission = match.group(0)
            print("Mission", match.group(0))
            # print("Dates", line.split(match.group(0), 1)[1].strip())

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
              "regexx related to an audio time-stamp (possibly!) from the "
              "mission records.")
        return
        # Leave the below for now...
        format_and_print_date_match(
            section=section, match_object=military_match, line=line)
        return

    '''
    if line.startswith("CAPCOM"):
        capcom = line.split("CAPCOM", 1)[1].replace(":", "").strip().replace("\n", "")
        print("CAPCOM", capcom)
        return


    else:
        return
        if not line.startswith("-----") and not line.startswith("\n"):
            print(line)
        if line.startswith("######"):
            print("#########################")
    '''


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
