#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import click

from boomer import *
from kaltura import *


@click.command()
@click.option("-s", "--start", required=True, help="Start date for query [YYYY-MM-DD]")
@click.option("-e", "--end", required=True, help="End date for query [YYYY-MM-DD]")
def main(start, end):
    """
    Application to check polarity of Kaltura and Zoom.

    Dates MUST be 1 month apart.
    """
    try:
        datetime.strptime(start, "%Y-%m-%d")
        datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        print("Times are not properly formatted")
        sys.exit()

    zoom = Boomer()
    kal = Kaltura()

    # Something a junior dev could do is look at converting this to an iterator
    # iterate the call to search with the token and yield in between to better
    # chunk response objects.
    results = zoom.iterateRecordings(start, end)

    print(len(results))

    for result in results:
        if result.duration == 0:
            print("this videos duration shows 0")
            continue
        if not result.email.endswith("suu.edu"):
            print("This email is bad")
            continue
        if not kal.search(result.userName, result.topic, result.meetingId):
            print("No match", result)

            downloads = zoom.downloadRecording(result.meetingId)
            if len(downloads) > 1:
                print("More than one download")
            else:
                print(downloads[0][0])
                upload_file = download_file(downloads[0][0] + f"?access_token={zoom.token}", downloads[0][1])
                kal.upload(upload_file, result.topic, result.generateDescription, result.userName)
                
                break
            # break
        else:
            print("Match", result)
            zoom.deleteRecording(
                result.meetingId, False
            )  # Change this to True and Start the Killing

        print("-------------------------------------")
            # break


if __name__ == "__main__":
    main()