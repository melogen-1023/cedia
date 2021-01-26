import core.run.task as task
import json
from core.register.register import cedia_register
from db.mysql.dba import cedia_dba
from core.conf.config import config

# python 3.8


if __name__ == '__main__':

    with open('conf.json', 'r', encoding='UTF-8') as f:
        conf = json.load(f)
        dbc = conf['dbc']
        cedia_dba.connect(dbc[0]['config'])
        config.load(storage=conf['storage'])
    with open('tasks.json', encoding='UTF-8') as f:
        tasks = json.load(f)
        data = tasks['data']
        for i in range(len(data)):
            t = task.Task(name=f'cedio#{i}', keyword=data[i]['name'])
            arr = []
            for source_s in data[i]['sources']:
                arr.append(source_s)
            t.set_sources(arr)  # set sources
            cedia_register.append_task(t)  # add task
        cedia_register.execute()
