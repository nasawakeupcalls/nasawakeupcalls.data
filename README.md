# nasawakeupcalls.data

[Chronology of Wakeup Calls][nasa-1] converted to data.

## About

Project declared "cool" by NASA Astronaut and Max-Q lead singer
[Tracy Caldwell Dyson][dyson-1] in a telephone interview 12 Feb 2020.

Data extracts and analysis from the NASA wake-up call project. This is a remix
project. Credit for the source material goes to Colin Fries of the NASA
historical division, and is released as Public Domain by NASA.

More information about the original work and this remix can be found on
<https://nasawakupcalls.github.io> [about][about-1].

## Sources

* [JSON][json-1]. Is our primary data-source, the `_to_csv.py` and
`_to_blog.py` scripts will all generate their data from here.
* [CSV][csv-1]. Exists for easy access (who doesn't like a table?). It's a
good resource to hack on and generate visualizations, but please consider
contributing back to the `json` document itself.
* [Website][website-1]. <https://nasawakeupcalls.github.io> is one of the
outputs of this work, providing a searchable front-end to all of this data. The
website is based on Jekyll and its source can also be found on
[Github][github-2].

## Process and Requirements

When there is an opportunity I will walk people back through what was involved
in creating this dataset.

I had started but as the process of converting the data from PDF to JSON
continued it became more and more laborious and so difficult to develop a
useful audit trail.

[Apache Tika][apache-1] helped immensely. Python was my selected scripting
language.

### Discogs genre tools

The cleaning tools made by Matt in the ipython notebook are commented, but of
less general use, and also hideous (Matt's words!). More information on the
Discogs API, and how to get an API token can be found [here][discogs-1].

## Questions without answers

As someone interested in data integrity, moving this data from something locked
away in PDF to something machine readable has been "interesting".

* Has the process been lossless?
* Has the source material been diluted?
* Has the transformation of this work been worth it?
* It was expensive in terms of hours; how expensive was it?
* How would these costs compare to those in my subject discipline?
* Does this work match that of the current field of digital humanities?
* Is the work sustainable?
* Would I do it again? (Yes, but, I might plan it differently).

## What next

* Playlists. And greater access to the data.
* I want to find more tools to explore the data with.
* Visidata looks good! <https://www.visidata.org/>
* Keeping this list on-going, I am trying to keep track of additions in
[Github][github-1] issues. As the space-program ramps up again, we will need a
different approach.

## Please do

Visit <https://nasawakeupcalls.github.io/> and enjoy what's there.

Please let me know your ideas on how it can be expanded upon.

[about-1]: https://nasawakeupcalls.github.io/about/
[apache-1]: https://tika.apache.org/
[csv-1]: https://github.com/nasawakeupcalls/nasawakeupcalls.data/blob/master/nasawakeupcalls.csv
[discogs-1]: https://www.discogs.com/developers
[dyson-1]: https://www.nasa.gov/astronauts/biographies/tracy-caldwell-dyson
[github-1]: https://github.com/nasawakeupcalls/nasawakeupcalls.data/issues
[github-2]: https://github.com/nasawakeupcalls/nasawakeupcalls.github.io
[json-1]: https://github.com/nasawakeupcalls/nasawakeupcalls.data/blob/master/nasawakeupcalls.json
[nasa-1]: https://history.nasa.gov/wakeup.htm
[website-1]: https://nasawakeupcalls.github.io/
