import logging

f = open("log/search.log", encoding='UTF-8', mode='a')
logging.basicConfig(level=logging.INFO, stream=f,
                    format='%(asctime)s %(name)-12s %(levelname)-8s Thread-%(threadName)-12s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    )
logger = logging.getLogger()

task_logger = logging.getLogger('task')
