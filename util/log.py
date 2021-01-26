import logging

logging.basicConfig(filename='log/search.log', level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s Thread-%(threadName)-12s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    )
logger = logging.getLogger()

task_logger = logging.getLogger('task')
