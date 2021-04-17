from db.db import db
from sources.bilibili.bilibili import BiLiBiLi
import json
import core.run.task as task
import core.register.container as container
import sources.netease as netease


def source(source_json):
    source_s = source_json['name']
    if source_s == 'bilibili.bilibili':
        return BiLiBiLi(**source_json)

    if source_s == 'netease.mv':
        return netease.mv.MV(**source_json)


class Config:
    def __init__(self):
        self.storage = {}

    def load(self, dbc, storage):
        if dbc['enable'] == '0':
            return

        db.connect(config={
            'user': dbc['user'],
            'password': dbc['password'],
            'host': dbc['host'],
            'database': dbc['database']
        })
        root_path = storage.get('root', '.')
        self.storage['root'] = root_path
        with open('./tasks.json', encoding='UTF-8') as f:
            tasks = json.load(f)
            data = tasks['data']
            for i in range(len(data)):
                t = task.Task(name=f'cedio#{i}', keyword=data[i]['name'], type=data[i]['type'])
                sources = []
                for j in data[i]['sources']:
                    sources.append(source(j))
                t.set_sources(sources)
                container.container.append_task(t)

    def start(self):
        container.container.execute()


config = Config()
