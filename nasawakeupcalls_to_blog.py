#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import json
import os
import random
import time
from urllib.parse import quote

urls_file = os.path.join("urls", "urls")

# Header for output of a mission dedication.
dedication_title = "#### *Dedication:*"


def my_name_is_sol(date_):
    """Take the Martian landing date and calculate the SOL based on the given
    offset.
    """
    landing_date = date_.split(":")[0]
    offset = date_.split("Sol")[1]
    date = datetime.datetime(
        int(landing_date.split("-")[0]),
        int(landing_date.split("-")[1]),
        int(landing_date.split("-")[2]),
    )
    return date + (datetime.timedelta(days=1, minutes=39, seconds=35) * int(offset))


def set_file_datetime(file_name, date_):
    if "Sol" not in date_:
        date = datetime.datetime(
            int(date_.split("-")[0]), int(date_.split("-")[1]), int(date_.split("-")[2])
        )
        modTime = time.mktime(date.timetuple())
        os.utime(file_name, (modTime, modTime))
        return
    modTime = time.mktime(my_name_is_sol(date_).timetuple())
    os.utime(file_name, (modTime, modTime))


def date_to_human(date_):
    if "Sol" not in date_:
        d_ = datetime.datetime(
            int(date_.split("-")[0]), int(date_.split("-")[1]), int(date_.split("-")[2])
        )
        return d_.strftime("%B %d, %Y")
    return my_name_is_sol(date_).strftime("%B %d, %Y")


def make_genre_url(genre):
    return "[{}](https://www.discogs.com/genre/{})".format(genre, quote(genre))


def make_style_url(style):
    return "[{}](https://www.discogs.com/style/{})".format(style, quote(style))


def make_discogs_uri(discogs):

    link = """<a target="blank_" href="{{ %%uri%% }}">
    <i class="fas fa-compact-disc"
       title="Discogs entry for this song"
       alt="Discogs entry for this song"
       style="font-size: 1.1em;"></i></a>
    """

    return link.replace("{{ %%uri%% }}", discogs)


def pretty_json(dict_data):
    """Function docstring."""
    return json.dumps(dict_data, sort_keys=True, indent=4, separators=(",", ": "))


def output_rows(program, mission):
    """Function docstring."""
    stars = ["✦", "✫", "⊹", "✺", "✧", "✷", "✵"]
    mission_name = mission.get("Mission")
    dedication = mission.get("Dedication")
    calls = mission.get("WakeupCalls", [])
    for call in calls:
        for date, songlist in call.items():
            date_ = date
            song_details = ""
            song_array = ""
            genre_array = ""
            comment = ""
            for song in songlist:
                """output a new post..."""

                # Genre associated with the song, we will append it to the song
                # and it will become part of the front-matter.
                genre = song.get("Genre")
                if genre != None:
                    if genre_array != "":
                        genre_array = '{},"{}"'.format(genre_array, genre)
                    else:
                        genre_array = '"{}"'.format(genre)
                style = song.get("Style")
                genre_style = ""
                if style is not None:
                    style = ": {}".format(make_style_url(style))
                    genre_style = "({}{})".format(make_genre_url(genre), style)
                else:
                    if genre is not None:
                        genre_style = "({})".format(make_genre_url(genre))
                discogs = song.get("DiscogsURI")
                if discogs is not None:
                    discogs = make_discogs_uri(discogs)
                if song_details != "":
                    # Add a newline to create a new entry.
                    song_details = "{}  &nbsp;<br />\n{} {} *by* {} {} {}".format(
                        song_details,
                        random.choice(stars),
                        song["Song"],
                        song["Artist"],
                        genre_style if genre_style else "",
                        discogs if discogs else "",
                    )
                    song_array = '{}, "{} by {}"'.format(
                        song_array, song["Song"], song["Artist"]
                    )
                else:
                    song_details = "{} {} *by* {} {} {}".format(
                        random.choice(stars),
                        song["Song"],
                        song["Artist"],
                        genre_style if genre_style else "",
                        discogs if discogs else "",
                    )
                    song_array = '"{} by {}"'.format(song["Song"], song["Artist"])

                # Page "footer" the last component of the entry which includes
                # the day's wakeup call comment.
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
            template = template.replace("{{ %song_array% }}", song_array)
            template = template.replace("{{ %genre_array% }}", genre_array)
            if comment == "":
                comment = "No mission comment"
            template = template.replace(
                "{{ %comment% }}", comment.replace("Ibid.\n", "").replace("Ibid.", "")
            )
            template = template.replace("{{ %date% }}", date_)
            template = template.replace("{{ %date_computer% }}", date)
            template = template.replace("{{ %date_human% }}", date_to_human(date_))

            if dedication:
                dedication_quote = "{}\n> *{}*".format(dedication_title, dedication)
            else:
                dedication_quote = ""
            template = template.replace("{{ %dedication% }}", dedication_quote)
            date_string = None
            if "Sol" not in date_:
                date_string = date_.replace(" ", "-")
            else:
                date_string = my_name_is_sol(date_).strftime("%Y-%m-%d")
            file_name = os.path.join(
                "posts", "{}-{}.md".format(date_string, mission_name.replace(" ", "_"))
            )
            with open(file_name, "w") as blog_file:
                blog_file.write(template.strip() + "\n")
            with open(urls_file, "a+") as url_listing:
                url_ = '"/{}/{}",'.format(date_string, mission_name.replace(" ", "_"))
                url_listing.write("{}\n".format(url_))
            set_file_datetime(file_name, date_)


def main():
    """Primary entry point of the script."""
    with open(urls_file, "w") as url_listing:
        """Clear the url_listing."""
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


if __name__ == "__main__":
    main()
