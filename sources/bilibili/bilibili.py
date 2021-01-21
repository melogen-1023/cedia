import core.source as source
import json
import requests
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
        self.video_url = None
        self.proxies = {
            "http": "http://127.0.0.1:8866",
            "https": "http://127.0.0.1:8866"
        }

    def search(self, media_name):
        response = self.session.get(self.url.search_url,
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
        # print(response.status_code)
        if response.status_code != 200:
            raise Exception(f"search error,request:{response.status_code}")
        self.search_handle(response.json())

    def search_handle(self, data):
        self.video_url = data['data']['result'][0]['url']
        # print(json.dumps(data, indent=4, separators=(',', ':')))

    def video(self):
        # print(self.video_url)
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
            return -1
        # print(play_info_tag.string)
        copy_index_l = 0
        for i in range(len(play_info_tag.string)):
            if play_info_tag.string[i] == '{':
                copy_index_l = i
                break
        play_info_json_str = play_info_tag.string[copy_index_l:len(play_info_tag.string)]
        play_info_json = json.loads(play_info_json_str)
        # print(json.dumps(play_info_json, indent=4, separators=(',', ':')))
        video_base_url = play_info_json['data']['dash']['video'][0]['base_url']
        # print(video_base_url)
        # r = requests.request('get', video_base_url, headers={
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        #     'Sec-Fetch-Mode': 'cors',
        #     'Sec-Fetch-Site': 'cross-site',
        #     'Sec-Fetch-Dest': 'empty',
        #     'Access-Control-Request-Headers': 'range',
        #     'Access-Control-Request-Method': 'GET',
        #     'range': 'bytes=132111912-132760487',
        #     'Origin': 'https://www.bilibili.com',
        #     'Referer': self.video_url
        #
        # }, proxies=self.proxies, verify=False)
        # print(r.status_code)

        with open('./test.mp4', 'ab') as f:

            with requests.request('get', video_base_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-Dest': 'empty',
                'Access-Control-Request-Headers': 'range',
                'Access-Control-Request-Method': 'GET',
                # 'range': 'bytes=132111912-132760487',
                'Origin': 'https://www.bilibili.com',
                'Referer': self.video_url
            }, stream=True) as r:
                print(r.status_code)
                for chunk in r.iter_content(chunk_size=102400):
                    if chunk:
                        f.write(chunk)

    # print(response.text)
