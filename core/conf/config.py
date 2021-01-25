class Config:
    def __init__(self):
        self.storage = {}

    def load(self, **kwargs):
        if kwargs.get('storage') is None:
            self.storage = {'root': '.'}
        else:
            self.storage = kwargs['storage']


config = Config()
