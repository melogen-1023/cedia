from sources.bilibili.bilibili import BiLiBiLi
from util.log import task_logger


class Register:
    def __init__(self):
        self.sources_s = []  # source_s array
        self.container = []  # task container

    def add_source(self, source):  # every source should register.
        self.sources_s.append(source)

    def get_sources_s(self):
        return self.sources_s

    def init_source(self, source_s):
        if source_s == 'bilibili':
            return BiLiBiLi()

    def append_task(self, task):
        self.container.append(task)

    def execute(self):
        for task in self.container:
            task_logger.info(f"{task.name} is running, keyword is {task.keyword}")
            task.start()


cedia_register = Register()
cedia_register.add_source('bilibili')
