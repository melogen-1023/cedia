import requests
import core.conf.config as config


class Source:

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        if self.name is None:
            self.name = 'source'
        self.session = requests.Session()  # request instance in requests
        self.effective_path = config.config.storage['root']
        # set request headers

    def __str__(self):
        return self.name

    def download(self, keyword):
        return None
