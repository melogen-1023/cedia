import mysql.connector as connector
from util.snowflake.generator import media_id_generator
import datetime


class CediaDBA:

    def __init__(self):
        self.mysql_cnx = None

    def connect(self, config):
        self.mysql_cnx = connector.connect(**config)

    def insert(self, data):
        cursor = self.mysql_cnx.cursor()
        data = {
            'id': media_id_generator.next_id(),
            'title': 'test',
            'name': 'test',
            'content': 'test',
            'kind': 0,
            'date': datetime.date.today(),
            'duration': 112,
            'coverImageType': 'image/jpg'
        }

        add_media = ("INSERT INTO filmtube_video"
                     "(id,name,content,title,kind,date,duration,coverImageType)"
                     "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                     )

        cursor.execute(add_media, (
            data['id'], data['name'], data['content'], data['title'], data['kind'], data['date'], data['duration'],
            data['coverImageType']))
        self.mysql_cnx.commit()
        cursor.close()


cedia_dba = CediaDBA()
