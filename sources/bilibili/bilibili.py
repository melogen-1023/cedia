import core.register.source as source
import json
import requests
import subprocess
import re
import datetime
import sources.const as const
import os
from db.mysql.dba import cedia_dba
from util.snowflake.generator import media_id_generator
from util.log import task_logger
from bs4 import BeautifulSoup


class BiLiBiLi(source.Source):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip,deflate,br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache - control': 'no-cache',
            'Cookie': "_uuid=3B872007-3CB9-1CC5-9A09-D3ED28E0639553737infoc; buvid3=331EC5D1-40B8-4B16-9A07-BDC4AD2D5C3518535infoc; sid=isc27ocb; fingerprint=d03134c24a729aac98b5cdd5e174a40d; buvid_fp=84A3610A-76BF-46D6-B825-757344779C3B185007infoc; buvid_fp_plain=6921B0F7-9C0F-4EAA-9011-79163CCF3CFC155822infoc; DedeUserID=353064211; DedeUserID__ckMd5=bfefe483490ae151; SESSDATA=345fab62%2C1626360179%2C9c0f4*11; bili_jct=2c97647d41c4a55db67c44e51c569763; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(u))|R|JkYm0J'uYu|)Rl~kY; LIVE_BUVID=AUTO2116111019078638; bp_t_offset_353064211=482624671893865369; bp_video_offset_353064211=482652060899420735; bfe_id=393becc67cde8e85697ff111d724b3c8; PVID=3",
            'user-agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 87.0.4280.141Safari / 537.36'
        }
        self.search_url = 'https://api.bilibili.com/x/web-interface/search/type'
        self.video_base_url = None
        self.audio_base_url = None
        self.video_url = None
        self.cover_url = None
        self.media_info = {}
        self.cover_image_suffix = ".jpg"
        self.name = 'bilibili'
        self.effective_path = f"{self.effective_path}/video"

    def download(self, keyword):
        if self.search(keyword) != 0:
            task_logger.info(f"搜索任务失败")
        if self.cover() != 0:
            task_logger.info(f"封面获取任务失败")
        if self.video() != 0:
            task_logger.info(f"音视频处理任务失败")

        return 0

    def __check_and_generate_media_info__(self, media_name, search_info):
        search_media_name = re.match('^<em class="keyword">(.*)</em>$', search_info['title']).group(1)
        if search_media_name != media_name:
            task_logger.info("已搜索到结果，但是搜索项并不是我们想要的。")
            return -1

        self.cover_image_suffix = re.match('^.*(\..*)$', search_info['cover']).group(1)
        cover_image_type = const.image_suffix_type_map[self.cover_image_suffix]
        self.media_info = {'id': media_id_generator.next_id(), 'name': media_name,
                           'date': datetime.date.fromtimestamp(search_info['pubtime']),
                           'content': search_info['desc'], 'kind': 0, 'coverImageType': cover_image_type, 'title': ''}

        if not os.path.exists(f"{self.effective_path}/{self.media_info['id']}"):
            task_logger.info(f"创建{self.media_info['id']}目录")
            os.makedirs(f"{self.effective_path}/{self.media_info['id']}", exist_ok=True)

        return 0

    def search(self, media_name):
        response = self.session.get(self.search_url,
                                    params={
                                        'context': '',
                                        'search_type': 'media_ft',
                                        'page': 1,
                                        'order': '',
                                        'keyword': media_name,
                                        'category_id': '',
                                        '__refresh__': 'true',
                                        '_extra': '',
                                        'highlight': 1,
                                        'single_column': 0
                                    })
        if response.status_code != 200:
            task_logger.warning(f"请求失败,状态码:{response.status_code}")
            return -1
        response_json = response.json()
        check_code = self.__check_and_generate_media_info__(media_name, response_json['data']['result'][0])
        if check_code != 0:
            return check_code
        result_length = len(response_json['data']['result'])
        if result_length == 0:
            task_logger.warning(f'无搜索结果： {media_name}')
            return -1
        self.video_url = response_json['data']['result'][0]['url']
        self.cover_url = response_json['data']['result'][0]['cover']
        return 0

    def cover(self):
        response = self.session.get(f"https:{self.cover_url}")
        with open(f"{self.effective_path}/{self.media_info['id']}/cover{self.cover_image_suffix}", "wb") as f:
            f.write(response.content)
        task_logger.info(f"封面图片保存成功")
        return 0

    def video(self):
        response = self.session.get(self.video_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        play_info_tag = None
        for child in soup.body.children:
            temp_str = ''
            child_str = child.string
            if child_str is None:
                continue
            for i in range(len(child_str)):
                if child_str[i] == '=':
                    break
                temp_str += child_str[i]
            if temp_str == 'window.__playinfo__':
                play_info_tag = child
                break
        if play_info_tag is None:
            task_logger.info(f'无法找到下载地址,__playinfo__:{response.text}')
            return -1
        copy_index_l = 0
        for i in range(len(play_info_tag.string)):
            if play_info_tag.string[i] == '{':
                copy_index_l = i
                break
        play_info_json_str = play_info_tag.string[copy_index_l:len(play_info_tag.string)]
        play_info_json = json.loads(play_info_json_str)
        duration_s = int(play_info_json['data']['dash']['duration'])
        self.media_info['duration'] = int(duration_s / 3600)
        cedia_dba.insert(self.media_info)
        self.video_base_url = play_info_json['data']['dash']['video'][0]['base_url']
        self.audio_base_url = play_info_json['data']['dash']['audio'][0]['base_url']
        video_download_code = self.video_download()
        audio_download_code = self.audio_download()
        ffmpeg_merge_code = self.ffmpeg_merge()
        if video_download_code == 0 and audio_download_code == 0 and ffmpeg_merge_code == 0:
            return 0
        else:
            return -1

    def video_download(self):
        with open(f"{self.effective_path}/{self.media_info['id']}/sample.mp4", 'ab') as f:
            task_logger.info(f"下载视频中...")
            with requests.request('get', self.video_base_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-Dest': 'empty',
                'Access-Control-Request-Headers': 'range',
                'Access-Control-Request-Method': 'GET',
                'Origin': 'https://www.bilibili.com',
                'Referer': self.video_url
                # 'range': 'bytes=132111912-132760487',
            }, stream=True) as r:
                for chunk in r.iter_content(chunk_size=102400):
                    if chunk:
                        f.write(chunk)
                task_logger.info('下载视频完成')
        return 0

    def audio_download(self):
        with open(f"{self.effective_path}/{self.media_info['id']}/sample.mp3", 'ab') as f:
            task_logger.info(f"下载音频中...")
            with requests.request('get', self.audio_base_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-Dest': 'empty',
                'Access-Control-Request-Headers': 'range',
                'Access-Control-Request-Method': 'GET',

                'Origin': 'https://www.bilibili.com',
                'Referer': self.video_url
                # 'range': 'bytes=132111912-132760487', 使用这个键来实现随机下载
            }, stream=True) as r:
                for chunk in r.iter_content(chunk_size=102400):
                    if chunk:
                        f.write(chunk)
                task_logger.info('下载音频完成')
        return 0

    def ffmpeg_merge(self):
        task_logger.info(f"正在合并音视频")
        completed_progress = subprocess.run(
            ["ffmpeg", "-loglevel", "quiet", "-i", f"{self.effective_path}/{self.media_info['id']}/sample.mp4", '-i',
             f"{self.effective_path}/{self.media_info['id']}/sample.mp3",
             f"{self.effective_path}/{self.media_info['id']}/src.mp4"])
        if completed_progress.returncode == 0:
            task_logger.info(f"合并完成")
        else:
            task_logger.warning(f"合并失败")

        os.remove(f"{self.effective_path}/{self.media_info['id']}/sample.mp4")
        os.remove(f"{self.effective_path}/{self.media_info['id']}/sample.mp3")
        return completed_progress.returncode
