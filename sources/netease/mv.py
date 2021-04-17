from core.register.source import Source
import requests
from util.log import task_logger
from util.snowflake.generator import media_id_generator
from db.mysql.audio import AudioDAO
import os


class MV(Source):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.netease_id = kwargs['netease_id']
        self.limit = 50
        self.sample_video_name = 'src.mp4'
        self.dao = AudioDAO()

    def download(self, keyword):
        r0 = self.session.get('https://cedia-neteasemusic.vercel.app/artist/songs', params={
            'id': self.netease_id,
            'limit': 1  # test_limit
        })
        test_songs_json = r0.json()
        count_songs = test_songs_json['total']
        pages = int(count_songs / self.limit)
        for page in range(pages):
            r = self.session.get('https://cedia-neteasemusic.vercel.app/artist/songs', params={
                'id': self.netease_id,
                'limit': self.limit,
                'offset': page
            })
            songs = r.json()['songs']
            for song in songs:
                if song['mv'] == 0:
                    continue
                self.mv_save(song['mv'], {
                    'singer_name': song['ar'][0]['name'],
                    'album_name': song['al']['name'],
                    'audio_name': song['name'],

                })

    def mv_save(self, mv_id, song_info):
        r = self.session.get('https://cedia-neteasemusic.vercel.app/mv/url', params={
            'id': mv_id
        })
        song_mv_json = r.json()
        download_url = song_mv_json['data']['url']
        audio_id = media_id_generator.next_id()
        song_info['audio_id'] = audio_id
        insert_result = self.dao.insert(song_info)
        if insert_result:
            return
        self.video_download(download_url, audio_id, song_info['audio_name'], song_info['singer_name'],
                            song_info['album_name'])

    def video_download(self, download_url, audio_id, audio_name, singer_name, album_name):
        os.mkdir(f"{self.effective_path}/{audio_id}")
        with open(f"{self.effective_path}/{audio_id}/{self.sample_video_name}", 'ab') as f:
            task_logger.info(f"下载{singer_name}-{album_name}-{audio_name}视频中...")
            with requests.request('get', download_url, stream=True) as r:
                for chunk in r.iter_content(chunk_size=102400):
                    if chunk:
                        f.write(chunk)
                task_logger.info('下载视频完成')
        return 0
