import jwt
import time
import requests
import uuid

from datetime import datetime, timezone


class BadStatus(Exception):
    def __init__(self, message):
        super().__init__(message)


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


class BoomerMedia:
    def __init__(self, idx, email, duration, topic, files, uuid, startTime):
        self.idx = idx
        self.email = email
        self.duration = duration
        self.topic = topic
        self.files = files
        self.meetingId = uuid
        self.startTime = startTime

        # print(self.startTime)
        if self.duration == 0:
            print(
                f"[ZOOM] Duration=0 | Look at deleting this entry: {self.topic} - {utc_to_local(datetime.strptime(self.startTime, '%Y-%m-%dT%H:%M:%SZ'))}"
            )

    def __str__(self):
        return (
            self.email
            + " "
            + self.topic
            + " "
            + str(self.idx)
            + " "
            + str(utc_to_local(datetime.strptime(self.startTime, '%Y-%m-%dT%H:%M:%SZ')))
        )

    def __repr__(self):
        return self.__str__()

    @property
    def userName(self):
        return self.email.split("@")[0]

    @property  # ?????
    def generateDescription(self):
        return (
            "Zoom Recording ID: "
            + str(self.idx)
            + "\n"
            + "UUID: "
            + self.meetingId
            + "\n"
            + "Meeting Time: "
            + self.startTime
        )


class Boomer:

    __ZOOM_API_KEY__ = "API_KEY"
    __ZOOM_API_SECRET__ = "API_SECRET"
    __ZOOM_URL__ = "https://api.zoom.us/v2/"

    def __init__(self):
        self.zoom = requests.Session()
        self.token = self.generateJWT()
        self.zoom.headers.update(
            {
                "Authorization": "Bearer {}".format(self.token),
                "Content-Type": "application/json",
            }
        )
        # print(self.token)

    def generateJWT(self):
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {"iss": self.__ZOOM_API_KEY__, "exp": int(time.time() + 3600)}

        token = jwt.encode(
            payload, self.__ZOOM_API_SECRET__, algorithm="HS256", headers=header
        )
        return token.decode("utf-8")

    def search(self, start, end, token=""):
        return self.zoom.get(
            self.__ZOOM_URL__ + "/accounts/me/recordings",
            params={
                "from": start,
                "to": end,
                "page_size": "10",
                "next_page_token": token,
            },
        )

    def iterateRecordings(self, start, end):
        results = []
        token = ""

        while True:
            response = self.search(start, end, token)

            if response.status_code != 200:
                raise BadStatus("Bad status code")

            response_json = response.json()

            for item in response.json()["meetings"]:
                # print(item)
                results.append(
                    BoomerMedia(
                        item["id"],
                        item["host_email"],
                        item["duration"],
                        item["topic"],
                        item["recording_files"],
                        item["uuid"],
                        item["start_time"],
                    )
                )

            token = response_json["next_page_token"]

            if response_json["page_size"] == 0 or token == "":
                break

        return results

    def downloadRecording(self, meetingId):
        response = self.zoom.get(
            self.__ZOOM_URL__ + f"/meetings/{meetingId}/recordings",
            params={"action": "trash"},
        )

        try:
            recordings = response.json()["recording_files"]
            results = []

            for d in recordings:
                if d.get("recording_type", "") == "shared_screen_with_speaker_view":
                    results.append([d["download_url"], d["file_type"]])

            return results
        except KeyError:
            print("[ZOOM] Key missing", meetingId)
            return []




    def deleteRecording(self, meetingId, dry=False):
        if dry:
            response = self.zoom.delete(
                self.__ZOOM_URL__ + f"/meetings/{meetingId}/recordings",
                params={"action": "trash"},
            )

            if response.status_code != 204:
                pass
                # raise BadStatus(
                #    f"Delete Failed: {response.status_code} - {response.text}"
                # )
                # print("[ZOOM] Delete failed ******!!!!!******")
                

        print(f"[ZOOM] Deleted meeting with id: {meetingId}")

def download_file(url, file_type):
    counter = 0
    local_filename = str(uuid.uuid4()) + "." + file_type.lower()
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
                counter += 1
    print("File size:", counter*8192)
    return local_filename
