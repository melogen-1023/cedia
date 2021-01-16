import core.source as source


class BiLiBiLi(source.Source):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip,deflate,br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache - control': 'no-cache',
            'Cookie': "_uuid=45CA1842-6425-685D-2423-26463E8F4D7081510infoc; buvid3=DEE28CE4-17F2-4915-A836-BFF9803287E7143088infoc; sid=jipkd042; DedeUserID=353064211; DedeUserID__ckMd5=bfefe483490ae151; SESSDATA=2332db10%2C1623513003%2C0f9cd*c1; bili_jct=5d504ed381b34e5b2b94617bb7e09238; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(u))|R|kYY|0J'uY|~mYu|Jk; CURRENT_QUALITY=112; fingerprint3=de7936e1316b94db956c1dc8517867ac; fingerprint=5f83d6b296bf6b315161c0bcd8d218c8; fingerprint_s=a20b375d310b0f5c8fda47ef94f29696; buivd_fp=DEE28CE4-17F2-4915-A836-BFF9803287E7143088infoc; buvid_fp_plain=DEE28CE4-17F2-4915-A836-BFF9803287E7143088infoc; LIVE_BUVID=AUTO5016083554915657; bp_t_offset_353064211=478189671485581513; _dfcaptcha=90148cd9f70c05e6783b9d44ca986609; bfe_id=61a513175dc1ae8854a560f6b82b37af; msource=pc_web; deviceFingerprint=7682fa2b9c6a747c6290ff635fd4e93b; bp_video_offset_353064211=480318944471965342; PVID=6",
            'user-agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 87.0.4280.141Safari / 537.36'
        }

    def search(self, media_name):
        response = self.session.get(self.url.search_url,
                                    params={
                                        'context': '',
                                        'search_type': 'media_ft',
                                        'page': 1,
                                        'order': '',
                                        'keyword': '星际穿越',
                                        'category_id': '',
                                        '__refresh__': 'true',
                                        '_extra': '',
                                        'highlight': 1,
                                        'single_column': 0
                                    })
        if response.status_code != 200:
            raise Exception(f"search error,request:{response.status_code}")
        self.search_handle(response.json())

    def search_handle(self, data):
        print(data)
