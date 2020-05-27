# Star imports are naughty but so are 150,000 loc files
import os

from KalturaClient import *
from KalturaClient.exceptions import *
from KalturaClient.Plugins.Core import *


class KalturaMedia:
    def __init__(self, idx, name, userId, creatorId, description, duration, categories):
        self.idx = idx
        self.name = name
        self.userId = userId
        self.creatorId = creatorId
        self.description = description
        self.duration = duration
        self.categories = categories

    def __str__(self):
        pass

    def __repr__(self):
        pass


class Kaltura:

    __CATEGORY_ID__ = "159659192"

    def __init__(self):

        config = KalturaConfiguration()
        self.client = KalturaClient(config)

        ks = self.client.session.start(
            "6184147be1d06271d95021ef265d93c4",
            "0c656633689ee00bb9ce6bef6db1fbe7",
            KalturaSessionType.ADMIN,
            1658221,
            3600,
            "appID:appName-appDomain",
        )

        KalturaMediaEntry.__str__ = media_show
        KalturaMediaEntry.__repr__ = media_show

        self.client.setKs(ks)

    def search(self, userId, name, uuid):

        pager = KalturaFilterPager()

        filter = KalturaMediaEntryFilter()

        filter.categoriesIdsMatchAnd = self.__CATEGORY_ID__
        filter.userIdEqual = userId
        filter.nameEqual = name

        response = self.client.media.list(filter, pager)

        for item in response.objects:
            # print(item)
            if item.description.split("\n")[1].split(" ")[1] == uuid:
                break
        else:
            return False

        return True

    def upload(self, filename, name, description, user):
        upload_token = KalturaUploadToken()
        token = self.client.uploadToken.add(upload_token);

        try:
            upload_token_id = token.id
            file_data =  open(filename, 'rb')
            resume = False
            final_chunk = True
            resume_at = 0
            result = self.client.uploadToken.upload(upload_token_id, file_data, resume, final_chunk, resume_at)
        except KalturaException:
            return False

        media_entry = KalturaMediaEntry()
        media_entry.name = name
        media_entry.description = description
        media_entry.categories = 'Zoom Recordings'
        media_entry.categoriesIds = '159659192'
        media_entry.creatorId = user
        media_entry.userId = user
        media_entry.mediaType = KalturaMediaType.VIDEO
        entry = self.client.media.add(media_entry)

        entry_id = entry.id
        resource = KalturaUploadedFileTokenResource()
        resource.token = upload_token_id

        result = self.client.media.addContent(entry_id, resource)
        try: 
            os.remove(filename)
        except PermissionError:
            print("Failed to delete file, because of windows")
        print(result)

    # def getRecordings(self):
    #     results = []

    #     response = self.client.media.list()

    #     for item in response.objects:

    #         results.append(
    #             KalturaMedia(
    #                 item["id"],
    #                 item["name"],
    #                 item["userId"],
    #                 item["creatorId"],
    #                 item["description"],
    #                 item["duration"],
    #                 item["categories"],
    #             )
    #         )

    #     # print(response.objects[0])
    #     return results
    # id, name, userId, creatorId, description, duration
    # categoriesIds: 159659192


def media_show(self):
    return str(vars(self))
    # return str(vars(self))

    # kal = Kaltura()

    # kal.search("karljarvis", "BIOL 3065 Genetics Lab")

    # for zoomie in zoom.getRecordings():
    #     user = zoomie.email.split("@")[0]
    #     # print(user)
    #     # print(zoomie.topic)
    #     kal_results = kal.search(user, zoomie.topic, zoomie.duration)
    #     print(user)

    #     if len(kal_results) > 1:
    #         print(f"Something is seriously fucked here: {zoomie.idx}")

    #     elif len(kal_results) == 1:
    #         print("its time to dududududududuel")
    #         raise TypeError("Found it boys")
    #         # delete the zoom video

    #     else:
    #         print(">> Time to move a video")
    #         # download the zoom video
    #         # upload the zoom video to kaltura
    #         #   - make owner the correct username
    #         #   - add correct category
    #         # delete the zoom video
