from util.log import task_logger


class Container:
    def __init__(self):
        self.tasks = []  # task container

    def append_task(self, task):
        self.tasks.append(task)

    def execute(self):
        for task in self.tasks:
            task_logger.info(f"{task.name}正在运行，关键字是{task.keyword}")
            task.start()


container = Container()
