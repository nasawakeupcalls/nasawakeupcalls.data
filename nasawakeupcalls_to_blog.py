#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import json
import os
import time


dates_arr = []
program_arr = []
missions_arr = []
artists_arr = []
songs_arr = []
comment_arr = []


def my_name_is_sol(date_):
    """Take the Martian landing date and calculate the SOL based on the given
    offset.
    """
    landing_date = date_.split(":")[0]
    offset = date_.split("Sol")[1]
    date = datetime.datetime(int(landing_date.split("-")[0]), int(landing_date.split("-")[1]), int(landing_date.split("-")[2]))
    return date + (datetime.timedelta(days=1, minutes=39, seconds=35)  * int(offset))


def set_file_datetime(file_name, date_):
    if not "Sol" in date_:
        date = datetime.datetime(int(date_.split("-")[0]), int(date_.split("-")[1]), int(date_.split("-")[2]))
        modTime = time.mktime(date.timetuple())
        os.utime(file_name, (modTime, modTime))
        return
    modTime = time.mktime(my_name_is_sol(date_).timetuple())
    os.utime(file_name, (modTime, modTime))


def date_to_human(date_):
    if not "Sol" in date_:
        d_ = datetime.datetime(int(date_.split("-")[0]), int(date_.split("-")[1]), int(date_.split("-")[2]))
        return d_.strftime("%B %d, %Y")
    return my_name_is_sol(date_).strftime("%B %d, %Y")


def pretty_json(dict_data):
    """Function docstring."""
    return json.dumps(
        dict_data, sort_keys=True, indent=4, separators=(',', ': '))


def output_rows(program, mission):
    """Function docstring."""
    mission_name = mission.get("Mission")
    calls = mission.get("WakeupCalls", [])
    for call in calls:
        for date, songlist in call.items():
            date_ = date
            song_details = ""
            comment = ""
            for song in songlist:
                """output a new post..."""
                if song_details != "":
                    song_details = "{}\n{} by {}".format(song_details, song["SONG"], song["ARTIST"])
                else:
                    song_details = "{} by {}".format(song["SONG"], song["ARTIST"])
                if not song.get("Comment"):
                    continue
                if comment != "":
                    comment = "{}\n{}".format(comment, song.get("Comment"))
                else:
                    comment = "{}".format(song.get("Comment"))
            # Write out to the template we created.
            template = None
            path_ = os.path.join("template", "blog.template")
            with open(path_) as blog_template:
                template = blog_template.read()
            template = template.replace("{{ %mission% }}", mission_name)
            template = template.replace("{{ %song_details% }}", song_details)
            if comment == "":
                comment = "No mission comment"
            template = template.replace("{{ %comment% }}", comment.replace("Ibid.\n", "").replace("Ibid.", ""))
            template = template.replace("{{ %date% }}", date_)
            template = template.replace("{{ %date_human% }}", date_to_human(date_))

            date_string = None
            if "Sol" not in date_:
                date_string = date_.replace(" ", "_")
            else:
                date_string = my_name_is_sol(date_).strftime("%Y_%m_%d")
            file_name = os.path.join("posts", "{}-{}.md".format(date_string, mission_name.replace(" ", "_")))
            with open(file_name, "w") as blog_file:
                blog_file.write(template)
            set_file_datetime(file_name, date_)


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


if __name__ == "__main__":
    main()
