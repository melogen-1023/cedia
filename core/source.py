class Source:
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.session = kwargs['session']  # request instance in requests
        self.url = kwargs['url']  # url class
        # set request headers

    def __str__(self):
        return self.name

    def search(self, media_name):
        self.search_handle({})
        return None

    def search_handle(self,data):
        return None