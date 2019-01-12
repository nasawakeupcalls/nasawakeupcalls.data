#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Stage 1 script for manipulating the NASA wakeup call data."""

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import nltk.data


LINE_SEPARATOR = "-----"
TOKENIZER = nltk.data.load('tokenizers/punkt/english.pickle')


def process_original_lines(line):
    """Remove lines which are just the space character or only start with '\\n'
    """
    if line.endswith("\n"):
        line = line.strip("\x20")
        if not line.startswith("\n"):
            return line
    return None

def process_tokenized(data):
    """Process tokenized data and remove the newlines."""
    newdata = ""
    data = data.split("\n")
    for line in data:
        if LINE_SEPARATOR not in line:
            newdata = "{}{}".format(newdata, line.replace("\n", ""))
        else:
            newdata = "\n\n{}\n{}\n".format(newdata, line)
    return newdata

def main():
    """Primary entry point of the script."""
    parser = argparse.ArgumentParser(description='Process the NASA wakeup calls.')
    parser.add_argument('file', metavar='FILE', type=str, nargs=1,
                        help='wakeup call file to process')

    args = parser.parse_args()

    if not args.file:
        print(parser.print_help())

    data = ""
    try:
        with open(args.file[0]) as file_:
            for line in file_:
                processed = process_original_lines(line)
                if processed:
                    data = data + processed

    except IOError:
        print("IOError: Problem parsing file %s", args.file[0])

    tokenized = u'\n{}\n'.format(LINE_SEPARATOR).join(TOKENIZER.tokenize(data))
    print(tokenized)

if __name__ == "__main__":
    main()
