from db.db import db


class AudioDAO:
    def __init__(self):
        self.cursor = db.cursor()

    def insert(self, data):
        add_audio_singer = (
            "INSERT INTO cedia_audio_singer(name)"
            "select %s from dual where not exists "
            "(select * from cedia_audio_singer where name = %s)"
        )
        self.cursor.execute(add_audio_singer, (data['singer_name'], data['singer_name']))
        db.commit()

        self.cursor.execute(
            "SELECT id FROM cedia_audio_singer WHERE name = %s ", (data['singer_name'],)
        )
        singer_id = -1
        for qr in self.cursor:
            singer_id = qr[0]

        add_audio_album = (
            "INSERT INTO cedia_audio_album(name,singer)"
            "select %s,%s from dual where not exists "
            "(select * from cedia_audio_album where name = %s)"
        )
        self.cursor.execute(add_audio_album, (data['album_name'], singer_id, data['album_name']))
        db.commit()
        self.cursor.execute(
            "SELECT id FROM cedia_audio_album WHERE name = %s ", (data['album_name'],)
        )
        album_id = -1
        for al in self.cursor:
            album_id = al[0]

        self.cursor.execute(
            "SELECT id from cedia_audio where name = %s", (data['audio_name'],)
        )
        audio_id = None
        for ai in self.cursor:
            audio_id = ai[0]

        if audio_id is not None:
            return 1

        add_audio = (
            "INSERT INTO cedia_audio(id,name,album,type,singer)"
            " values( %s,%s,%s,1,%s)"
        )

        self.cursor.execute(
            add_audio, (data['audio_id'], data['audio_name'], album_id, singer_id)
        )
        db.commit()
        return 0
