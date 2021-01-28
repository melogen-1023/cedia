import threading
from core.register.register import cedia_register
from util.log import task_logger


class Task(threading.Thread):
    def __init__(self, **kwargs):
        super().__init__(name=kwargs['name'])
        self.keyword = kwargs['keyword']
        self.sources_s = cedia_register.get_sources_s()  # default sources
        self.sources = []

    def set_sources(self, array):
        if len(array) == 0:
            return
        self.sources_s = array

    def init_sources(self):
        for source_s in self.sources_s:
            self.sources.append(cedia_register.init_source(source_s))

    def run(self):
        self.init_sources()
        for source in self.sources:
            task_logger.info(f"正在使用 {source.name}源")
            if not source.download(keyword=self.keyword):
                task_logger.info(f"已从{source.name}源下载到资源")
                break

