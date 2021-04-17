from db.db import db


class CediaDBA:

    def __init__(self):
        self.cursor = db.cursor()

    def insert(self, data):
        add_media = ("INSERT INTO filmtube_video"
                     "(id,name,content,title,kind,date,duration,coverImageType)"
                     "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                     )

        add_media_link = ("INSERT INTO filmtube_video_link"
                          "(videoId, episode, type) "
                          "VALUES (%s,%s,%s)"
                          )

        self.cursor.execute(add_media, (
            data['id'], data['name'], data['content'], data['title'], data['kind'], data['date'], data['duration'],
            data['coverImageType']))
        self.cursor.execute(add_media_link, (data['id'], 1, "video/mp4"))
        db.commit()
