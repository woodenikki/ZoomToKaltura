# ZoomToKaltura
## Southern Utah University: Online Teaching and Learning
This program will compare videos in Zoom and Kaltura in the SUU System and clean up the Zoom Cloud storage. 

Given a date range (has to be 1 month), the program will go through all the videos in zoom and compare it against kaltura. If a video is in Zoom AND Kaltura, it will be deleted from Zoom. If the video is NOT in Kaltura, it is downloaded to your machine, uploaded to Kaltura (with the appropriate owner, title, description, and category), and then deleted from your local machine. 

> **NOTE:** The program will have to be run again in order to catch the videos you upload and delete them from zoom.

There is a check in the program - if the zoom email ends in "@ suu.edu", the email is split and the first part of the email (username) is used as the owner in kaltura. If the email has any other extension, the ZoomToKaltura program will skip this video. These need to be done manually, as we need to look up the correct username in the SUU System. 

> A list of these emails will be outputed to **output.log**. Every time the program is run, it will override the information in this file. So after every run, copy the information into the [ZoomToKaltura Manual](https://docs.google.com/spreadsheets/d/1KqdXdzZCwl8VoPhCPy4HNkj3gn54InURtW_ihG_ZytY/edit#gid=0) google sheet file. And a student should get to them soon.

---
## Getting Started

To Clone this repository:

- On GitHub, select **Clone or download**
- **Download ZIP**
- Unzip files into your desired directory
- Open this folder in VSCode
---
### Prerequisites

- Python (latest version)
- install Poetry

```
poetry install
```

- Set up required tools
``` 
poetry add setuptools 
```
---
## Running the tests

> **Note:** Only run the program when all videos in Kaltura are finished Converting

To run our program, we need the start (-s) and end (-e) date parameters. Remember that these should be exactly 1 month apart. 
> Date formatting should be **YYYY-MM-DD**

```
python main.py -s 2020-03-01 -e 2020-04-01
```

--- 
## Output
```
[ZOOM] Duration=0 | Look at deleting this entry: Topic name - 2020-01-01 12:29:25-06:00
```
If a video in zoom has a duration of 0, it might be smart to look into deleting it. You should have enough information to look the video up in Zoom.

---

```
[ZOOM] Found 95 results within your date range...
```
Z2K will show you how many results are found within your date range in Zoom. 

---
```
[MANUAL] email is bad. Check output.log
```
If the email for this video does not end in '@suu.edu', you will need to upload this video manually. A list of these videos will appear in output.log after the program is finished executing.

---
```
Match email@suu.edu Topic 123456789 2020-01-01 12:29:25-06:00
[ZOOM] Deleted meeting with id: (94AK4MgwRGqqxN/HehRXeg==)
```
A match between Zoom and Kaltura was found. This recording has been deleted.
> **Note:** You can always restore a recording from the Zoom trash bin.

---

```
[KALTURA] No match email@suu.edu Someone's Personal Meeting Room 123456789 2020-01-01 12:29:25-06:00
[ZOOM] More than one download
```
More than one file was found, this video was skipped.

---
```
[KALTURA] No match email@suu.edu Topic 903317900 123456789 2020-01-01 12:29:25-06:00
File size: 90636288
```
Zoom video was not found in Kaltura. Your download/upload will depend on the video's file size and your internet speed. 

---



## Authors

* **Jacobsin** - [GitHub](https://github.com/MisterBianco)
* **Nikki Wood** - [GitHub](https://github.com/woodenikki)


## License


- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2020 
