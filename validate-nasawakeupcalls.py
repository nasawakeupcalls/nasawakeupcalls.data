#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json


def pretty_json(dict_data):
    return json.dumps(dict_data, sort_keys=True, indent=4, separators=(",", ": "))


def main():
    """Primary entry point of the script."""
    data = None
    with open("nasawakeupcalls.json") as f:
        data = json.load(f)
    print(pretty_json(data))


if __name__ == "__main__":
    main()
