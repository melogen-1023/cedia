import threading
from core.register.container import container
from util.log import task_logger


class Task(threading.Thread):
    def __init__(self, **kwargs):
        super().__init__(name=kwargs['name'])
        self.keyword = kwargs['keyword']
        self.sources = []

    def set_sources(self, sources):
        self.sources = sources

    def run(self):
        for source in self.sources:
            task_logger.info(f"正在使用 {source.name}源")
            if not source.download(keyword=self.keyword):
                task_logger.info(f"已从{source.name}源下载到资源")
                break
