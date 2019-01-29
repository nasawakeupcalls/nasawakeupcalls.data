#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Stage 3 script for turning the primary dataset into something more JSON like
to see what we've got!
"""

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import re
import json
import sys

import shortuuid


def flush_section(section):
    print(pretty_json(section))
    section.clear()
    return {}


def pretty_json(dict_data):
    return json.dumps(
        dict_data, sort_keys=True, indent=4, separators=(',', ': '))

'''
def assign_to_primary(value):
    """Recurse until we are sure that a shortuuid is unique."""
    id_ = shortuuid.uuid()
    if id_ in primary_dict:
        print("INFO: shortuuid isn't unique... recursing.")
        assign_to_primary(value)
    primary_array.append[id_] = value
'''

secondary_dict = {}
tertiary_dict = {}

def split_lines(line):
    """Go through each line and build our dictionary."""
    global tertiary_dict
    global secondary_dict
    global wakeup_calls_arr
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
        line_ = line.replace("MISSION", "", 1).replace('"', "").replace(":", "").strip()
        try:
            if tertiary_dict["MISSION"] != line_:
                if wakeup_calls_arr:
                    tertiary_dict["WakeupCalls"] = wakeup_calls_arr
                    wakeup_calls_arr = []
                    primary_arr.append(tertiary_dict)
                    tertiary_dict = {}
                    pass
        except KeyError:
            pass
        tertiary_dict["MISSION"] = line_
        return
    if line.startswith("INTRO"):
        tertiary_dict["INTRO"] = \
            line.replace("INTRO", "", 1).replace('"', "").replace(":", "").strip()
        return
    for value in vals:
        if line.startswith(value):
            secondary_dict[value] = \
                line.replace(value, "", 1).replace('"', "").replace(":", "").strip()
            return
    if line.startswith("EOE"):
        try:
            tertiary_dict["Title"] = secondary_dict["MISSION"]
        except KeyError:
            pass
        if secondary_dict:
            wakeup_calls_arr.append(secondary_dict)
            secondary_dict = {}
            return
    if not line.startswith("\n"):
        print("Not found: x{}x".format(line), file=sys.stderr)

primary_arr = []
wakeup_calls_arr = []
secondary_dict = {}


def main():
    """Primary entry point of the script."""
    parser = argparse.ArgumentParser(description='Process the NASA wakeup calls.')
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

    print(pretty_json(primary_arr))

if __name__ == "__main__":
    main()
