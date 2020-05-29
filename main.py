#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import click

from boomer import *
from kaltura import *


log = open("output.log", "w") #a for append.. but transfer this to word document after every run!!!
# https://docs.google.com/spreadsheets/d/1KqdXdzZCwl8VoPhCPy4HNkj3gn54InURtW_ihG_ZytY/edit#gid=0


@click.command()
@click.option("-s", "--start", required=True, help="Start date for query [YYYY-MM-DD]")
@click.option("-e", "--end", required=True, help="End date for query [YYYY-MM-DD]")
def main(start, end):
    """
    Application to check polarity of Kaltura and Zoom.

    Dates MUST be 1 month apart.

    Don't run this until all videos in Kaltura are finished Converting!!
    """
    try:
        datetime.strptime(start, "%Y-%m-%d")
        datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        print("[MAIN] Times are not properly formatted")
        sys.exit()

    zoom = Boomer()
    kal = Kaltura()

    # Something a junior dev could do is look at converting this to an iterator
    # iterate the call to search with the token and yield in between to better
    # chunk response objects.
    results = zoom.iterateRecordings(start, end)

    print("[ZOOM] Found",len(results),"results within your date range...")

    for result in results:
        # print("-------------------------------------")
        if result.duration == 0:
            # print("this videos duration shows 0:", result.meetingId)
            continue
        if not result.email.endswith("suu.edu"):
            print("[MANUAL] email is bad. Check output.log")
            log.write( result.email + result.topic + "," +  "," + str(result.idx) +"," + str(utc_to_local(datetime.strptime(result.startTime, '%Y-%m-%dT%H:%M:%SZ'))) + "\n")
            continue
        if not kal.search(result.userName, result.topic, result.meetingId):
            print("[KALTURA] No match", result)

            downloads = zoom.downloadRecording(result.meetingId)
            if len(downloads) > 1:
                print("[ZOOM] More than one download")
            else:
                # print(downloads[0][0])
                try:
                    upload_file = download_file(downloads[0][0] + f"?access_token={zoom.token}", downloads[0][1])
                    kal.upload(upload_file, result.topic, result.generateDescription, result.userName)
                except IndexError:
                    print("[MAIN|K] Failed to upload file")
               
            # break
        else:
            print("Match", result)
            zoom.deleteRecording(
                result.meetingId, True
            )  # Change this to True and Start the Killing

        print("-------------------------------------")
            # break
        
        
        for root, dirs, files in os.walk("."):
            for currentFile in files:
                # print("processing file: " + currentFile)
                exts = ".mp4"
                if currentFile.lower().endswith(exts):
                    try:
                        os.remove(os.path.join(root, currentFile))
                    except PermissionError:
                        pass
    log.close()                    

if __name__ == "__main__":
    main()