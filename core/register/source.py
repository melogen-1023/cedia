import requests
from core.conf.config import config

class Source:

    def __init__(self, **kwargs):
        self.name = getattr(kwargs, 'name', 'source')
        self.session = requests.Session()  # request instance in requests
        self.path = getattr(kwargs, 'path', 'media')  # 资源存放路径
        self.effective_path = f"{config.storage['root']}/{self.path}"
        # set request headers

    def __str__(self):
        return self.name

    def download(self, keyword):
        return None
